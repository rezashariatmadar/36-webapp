import jdatetime
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import BookingForm
from .models import Booking, Space


def _as_price(value):
    if value is None:
        return 0
    return int(value)


def _serialize_plan(plan):
    if not plan:
        return None
    return {
        "id": plan.id,
        "name": plan.name,
        "daily_rate": _as_price(plan.daily_rate),
        "hourly_rate": _as_price(plan.hourly_rate),
        "monthly_rate": _as_price(plan.monthly_rate),
        "six_month_rate": _as_price(plan.six_month_rate),
        "yearly_rate": _as_price(plan.yearly_rate),
        "is_contact_for_price": plan.is_contact_for_price,
    }


def _serialize_space(space):
    return {
        "id": space.id,
        "name": space.name,
        "zone": space.zone,
        "status": space.status,
        "capacity": space.capacity,
        "is_nested": space.is_nested,
        "plan": _serialize_plan(space.pricing_plan),
        "seats": [
            {
                "id": seat.id,
                "name": seat.name,
                "status": seat.status,
                "capacity": seat.capacity,
                "plan": _serialize_plan(seat.pricing_plan),
            }
            for seat in space.seats.all()
        ],
    }


def _serialize_booking(booking):
    return {
        "id": booking.id,
        "space_id": booking.space_id,
        "space_name": booking.space.name,
        "booking_type": booking.booking_type,
        "status": booking.status,
        "price_charged": _as_price(booking.price_charged),
        "start_time": booking.start_time.strftime("%Y-%m-%d") if booking.start_time else None,
        "end_time": booking.end_time.strftime("%Y-%m-%d") if booking.end_time else None,
        "start_time_jalali": booking.start_time_jalali,
        "end_time_jalali": booking.end_time_jalali,
    }


def _to_jalali_string(value):
    if not value:
        return None
    return jdatetime.date.fromgregorian(date=value).strftime("%Y/%m/%d")


def _refresh_space_statuses():
    now = timezone.now().date()
    active_booking_exists = Booking.objects.filter(
        space=OuterRef("pk"),
        status=Booking.Status.CONFIRMED,
        start_time__lte=now,
        end_time__gte=now,
    )
    active_spaces = Space.objects.filter(is_active=True).annotate(has_active_booking=Exists(active_booking_exists))

    spaces_to_update = []
    for space in active_spaces:
        if space.status == Space.Status.UNAVAILABLE:
            continue
        new_status = Space.Status.OCCUPIED if space.has_active_booking else Space.Status.AVAILABLE
        if space.status != new_status:
            space.status = new_status
            spaces_to_update.append(space)

    if spaces_to_update:
        Space.objects.bulk_update(spaces_to_update, ["status"])


class CoworkSpacesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        _refresh_space_statuses()
        spaces = (
            Space.objects.filter(is_active=True, parent_table__isnull=True)
            .select_related("pricing_plan")
            .prefetch_related("seats__pricing_plan")
        )

        zones = []
        for code, label in Space.ZoneType.choices:
            zone_spaces = [space for space in spaces if space.zone == code]
            zones.append(
                {
                    "code": code,
                    "label": label,
                    "spaces": [_serialize_space(space) for space in zone_spaces],
                }
            )
        return Response({"zones": zones, "has_spaces": any(zone["spaces"] for zone in zones)})


class CoworkBookingPreviewAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        space_id = request.query_params.get("space_id")
        if not space_id:
            return Response({"detail": "space_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        space = get_object_or_404(Space, id=space_id)
        form_data = {
            "booking_type": request.query_params.get("booking_type"),
            "start_time": request.query_params.get("start_time"),
        }
        form = BookingForm(data=form_data, space=space)
        if not form.is_valid():
            return Response(
                {"valid": False, "errors": form.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        preview_booking = Booking(
            space=space,
            booking_type=form.cleaned_data["booking_type"],
            start_time=form.cleaned_data["start_time"],
            end_time=form.cleaned_data["end_time"],
        )
        price = preview_booking.calculate_price()
        return Response(
            {
                "valid": True,
                "price": _as_price(price),
                "start_time": preview_booking.start_time.strftime("%Y-%m-%d"),
                "end_time": preview_booking.end_time.strftime("%Y-%m-%d"),
                "end_time_jalali": _to_jalali_string(preview_booking.end_time),
            }
        )


class CoworkBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        space_id = request.data.get("space_id")
        if not space_id:
            return Response({"detail": "space_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        space = get_object_or_404(Space, id=space_id)
        form_data = {
            "booking_type": request.data.get("booking_type"),
            "start_time": request.data.get("start_time"),
        }
        form = BookingForm(data=form_data, space=space)
        if not form.is_valid():
            return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

        booking = form.save(commit=False)
        booking.user = request.user
        booking.space = space
        booking.status = Booking.Status.PENDING_PAYMENT
        booking.price_charged = booking.calculate_price()
        booking.save()
        space.refresh_status()
        return Response(
            {
                "booking": _serialize_booking(booking),
                "detail": "رزرو ثبت شد اما نهایی نیست. برای تایید نهایی لطفا تماس بگیرید.",
                "requires_admin_approval": True,
            },
            status=status.HTTP_201_CREATED,
        )


class CoworkMyBookingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).select_related("space").order_by("-start_time")
        return Response({"bookings": [_serialize_booking(booking) for booking in bookings]})
