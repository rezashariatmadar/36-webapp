from django.contrib.auth.models import Group
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser
from cafe.models import CafeOrder, OrderItem
from cowork.models import Booking, Space


class StaffPermission(IsAuthenticated):
    def has_permission(self, request, view):
        has_auth = super().has_permission(request, view)
        if not has_auth:
            return False
        return bool(request.user.is_staff or request.user.is_admin or request.user.is_barista)


class AdminPermission(IsAuthenticated):
    def has_permission(self, request, view):
        has_auth = super().has_permission(request, view)
        if not has_auth:
            return False
        return bool(request.user.is_admin)


def _serialize_user(user: CustomUser):
    return {
        "id": user.id,
        "phone_number": user.phone_number,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "roles": {
            "is_admin": user.is_admin,
            "is_barista": user.is_barista,
            "is_customer": user.is_customer,
        },
    }


class StaffAnalyticsOverviewAPIView(APIView):
    permission_classes = [StaffPermission]

    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        cafe_total = CafeOrder.objects.filter(is_paid=True).aggregate(total=Sum("total_price"))["total"] or 0
        cafe_today = (
            CafeOrder.objects.filter(is_paid=True, created_at__gte=today_start).aggregate(total=Sum("total_price"))["total"] or 0
        )
        top_items = (
            OrderItem.objects.values("menu_item__name")
            .annotate(total_qty=Sum("quantity"), total_rev=Sum("unit_price"))
            .order_by("-total_qty")[:5]
        )
        top_cafe_buyers = (
            CafeOrder.objects.filter(is_paid=True, user__isnull=False)
            .values("user__phone_number", "user__full_name")
            .annotate(total_spent=Sum("total_price"))
            .order_by("-total_spent")[:5]
        )
        cowork_total = Booking.objects.filter(status=Booking.Status.CONFIRMED).aggregate(total=Sum("price_charged"))["total"] or 0
        total_spaces = Space.objects.filter(is_active=True).count()
        active_bookings = Booking.objects.filter(
            status=Booking.Status.CONFIRMED,
            start_time__lte=now,
            end_time__gte=now,
        ).count()
        occupancy_rate = int((active_bookings / total_spaces) * 100) if total_spaces else 0
        top_cowork_members = (
            Booking.objects.filter(status=Booking.Status.CONFIRMED)
            .values("user__phone_number", "user__full_name")
            .annotate(total_spent=Sum("price_charged"), total_bookings=Count("id"))
            .order_by("-total_spent")[:5]
        )
        return Response(
            {
                "cafe_total": int(cafe_total),
                "cafe_today": int(cafe_today),
                "cowork_total": int(cowork_total),
                "occupancy_rate": occupancy_rate,
                "active_bookings": active_bookings,
                "total_spaces": total_spaces,
                "top_items": list(top_items),
                "top_cafe_buyers": list(top_cafe_buyers),
                "top_cowork_members": list(top_cowork_members),
            }
        )


class StaffUsersAPIView(APIView):
    permission_classes = [AdminPermission]

    def get(self, request):
        users = CustomUser.objects.order_by("id")
        query = (request.query_params.get("q") or "").strip()
        role = (request.query_params.get("role") or "").strip()
        is_active = (request.query_params.get("is_active") or "").strip()
        page = max(int(request.query_params.get("page", 1)), 1)
        page_size = min(max(int(request.query_params.get("page_size", 25)), 1), 100)

        if query:
            users = users.filter(Q(phone_number__icontains=query) | Q(full_name__icontains=query))
        if role in {"Admin", "Barista", "Customer"}:
            users = users.filter(groups__name=role)
        if is_active in {"true", "false"}:
            users = users.filter(is_active=(is_active == "true"))

        total = users.count()
        offset = (page - 1) * page_size
        chunk = users[offset : offset + page_size]
        return Response(
            {
                "count": total,
                "page": page,
                "page_size": page_size,
                "results": [_serialize_user(user) for user in chunk],
            }
        )


class StaffUserStatusAPIView(APIView):
    permission_classes = [AdminPermission]

    def patch(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        is_active = request.data.get("is_active")
        if not isinstance(is_active, bool):
            return Response({"detail": "is_active must be boolean."}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = is_active
        user.save(update_fields=["is_active"])
        return Response(_serialize_user(user))


class StaffUserRoleAPIView(APIView):
    permission_classes = [AdminPermission]

    def patch(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        role = request.data.get("role")
        if role not in {"Admin", "Barista", "Customer"}:
            return Response({"detail": "Invalid role."}, status=status.HTTP_400_BAD_REQUEST)

        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)
        user.is_staff = role in {"Admin", "Barista"}
        user.save(update_fields=["is_staff"])
        return Response(_serialize_user(user))

