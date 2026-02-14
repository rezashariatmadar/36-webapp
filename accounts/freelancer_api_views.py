from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    FreelancerFlair,
    FreelancerProfile,
    FreelancerServiceOffering,
    FreelancerSpecialtyTag,
)


def _serialize_specialty(tag: FreelancerSpecialtyTag):
    return {
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug,
    }


def _serialize_flair(flair: FreelancerFlair):
    return {
        "id": flair.id,
        "name": flair.name,
        "slug": flair.slug,
        "color_token": flair.color_token,
        "icon_name": flair.icon_name,
    }


def _serialize_service(service: FreelancerServiceOffering):
    return {
        "id": service.id,
        "title": service.title,
        "description": service.description,
        "delivery_mode": service.delivery_mode,
        "starting_price": service.starting_price,
        "response_time_hours": service.response_time_hours,
        "is_active": service.is_active,
        "sort_order": service.sort_order,
    }


def _serialize_public_profile(profile: FreelancerProfile):
    services = profile.services.filter(is_active=True).order_by("sort_order", "id")
    return {
        "id": profile.id,
        "public_slug": profile.public_slug,
        "full_name": profile.user.full_name,
        "headline": profile.headline,
        "introduction": profile.introduction,
        "work_types": profile.work_types,
        "city": profile.city,
        "province": profile.province,
        "contact_cta_text": profile.contact_cta_text,
        "contact_cta_url": profile.contact_cta_url,
        "specialties": [_serialize_specialty(item) for item in profile.specialties.all()],
        "custom_specialties": profile.custom_specialties or [],
        "flairs": [_serialize_flair(item) for item in profile.flairs.all()],
        "services": [_serialize_service(item) for item in services],
    }


def _serialize_owner_profile(profile: FreelancerProfile):
    return {
        **_serialize_public_profile(profile),
        "is_public": profile.is_public,
        "status": profile.status,
        "moderation_note": profile.moderation_note,
        "specialty_ids": [item.id for item in profile.specialties.all()],
        "flair_ids": [item.id for item in profile.flairs.all()],
    }


def _profile_queryset():
    return (
        FreelancerProfile.objects.filter(status=FreelancerProfile.Status.PUBLISHED, is_public=True)
        .select_related("user")
        .prefetch_related("specialties", "flairs", "services")
        .distinct()
    )


def _safe_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _ensure_profile(user):
    profile = FreelancerProfile.objects.filter(user=user).first()
    if profile:
        return profile

    base_slug = f"freelancer-{user.id}"
    candidate = base_slug
    counter = 1
    while FreelancerProfile.objects.filter(public_slug=candidate).exists():
        counter += 1
        candidate = f"{base_slug}-{counter}"

    profile = FreelancerProfile.objects.create(user=user, public_slug=candidate)
    return profile


class PublicFreelancersAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = (request.query_params.get("q") or "").strip()
        tag_slug = (request.query_params.get("tag") or "").strip()
        flair_slug = (request.query_params.get("flair") or "").strip()
        work_type = (request.query_params.get("work_type") or "").strip()
        city = (request.query_params.get("city") or "").strip()
        page = max(_safe_int(request.query_params.get("page"), 1), 1)
        page_size = min(max(_safe_int(request.query_params.get("page_size"), 12), 1), 100)

        profiles = _profile_queryset()
        if tag_slug:
            profiles = profiles.filter(specialties__slug=tag_slug)
        if flair_slug:
            profiles = profiles.filter(flairs__slug=flair_slug)
        if city:
            profiles = profiles.filter(city__icontains=city)

        profile_list = list(profiles)
        if query:
            query_cf = query.casefold()
            profile_list = [
                profile
                for profile in profile_list
                if any(
                    query_cf in value.casefold()
                    for value in [
                        profile.user.full_name or "",
                        profile.headline or "",
                        profile.introduction or "",
                        profile.public_slug or "",
                    ]
                )
                or any(query_cf in item.casefold() for item in (profile.custom_specialties or []))
            ]
        if work_type:
            profile_list = [profile for profile in profile_list if work_type in (profile.work_types or [])]

        total = len(profile_list)
        offset = (page - 1) * page_size
        chunk = profile_list[offset : offset + page_size]
        return Response(
            {
                "count": total,
                "page": page,
                "page_size": page_size,
                "results": [_serialize_public_profile(profile) for profile in chunk],
            }
        )


class PublicFreelancerSpecialtiesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        specialties = FreelancerSpecialtyTag.objects.filter(is_active=True).order_by("sort_order", "name")
        return Response({"specialties": [_serialize_specialty(item) for item in specialties]})


class PublicFreelancerFlairsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        flairs = FreelancerFlair.objects.filter(is_active=True).order_by("sort_order", "name")
        return Response({"flairs": [_serialize_flair(item) for item in flairs]})


class PublicFreelancerDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        profile = get_object_or_404(_profile_queryset(), public_slug=slug)
        return Response({"profile": _serialize_public_profile(profile)})


class OwnerFreelancerProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = _ensure_profile(request.user)
        profile.refresh_from_db()
        return Response({"profile": _serialize_owner_profile(profile)})

    def patch(self, request):
        profile = _ensure_profile(request.user)
        payload = request.data

        updatable_fields = {
            "public_slug",
            "headline",
            "introduction",
            "work_types",
            "city",
            "province",
            "is_public",
            "contact_cta_text",
            "contact_cta_url",
            "custom_specialties",
        }
        for field_name in updatable_fields:
            if field_name in payload:
                setattr(profile, field_name, payload.get(field_name))

        specialty_ids = payload.get("specialty_ids")
        flair_ids = payload.get("flair_ids")

        try:
            profile.full_clean()
            profile.save()
        except ValidationError as exc:
            return Response({"errors": exc.message_dict}, status=status.HTTP_400_BAD_REQUEST)

        if specialty_ids is not None:
            specialties = list(FreelancerSpecialtyTag.objects.filter(id__in=specialty_ids, is_active=True))
            profile.specialties.set(specialties)
        if flair_ids is not None:
            flairs = list(FreelancerFlair.objects.filter(id__in=flair_ids, is_active=True))
            profile.flairs.set(flairs)

        if profile.status == FreelancerProfile.Status.REJECTED:
            profile.status = FreelancerProfile.Status.DRAFT
            profile.save(update_fields=["status", "updated_at"])

        profile.refresh_from_db()
        return Response({"profile": _serialize_owner_profile(profile)})


class OwnerFreelancerSubmitAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = _ensure_profile(request.user)
        if not profile.headline or not profile.introduction:
            return Response(
                {"detail": "headline and introduction are required before submit."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if profile.status == FreelancerProfile.Status.PUBLISHED:
            return Response({"detail": "Profile is already published."}, status=status.HTTP_400_BAD_REQUEST)

        profile.status = FreelancerProfile.Status.PENDING_APPROVAL
        profile.moderation_note = ""
        profile.save(update_fields=["status", "moderation_note", "updated_at"])
        return Response({"profile": _serialize_owner_profile(profile)})


class OwnerFreelancerSpecialtiesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        specialties = FreelancerSpecialtyTag.objects.filter(is_active=True).order_by("sort_order", "name")
        return Response({"specialties": [_serialize_specialty(item) for item in specialties]})


class OwnerFreelancerFlairsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        flairs = FreelancerFlair.objects.filter(is_active=True).order_by("sort_order", "name")
        return Response({"flairs": [_serialize_flair(item) for item in flairs]})


class OwnerFreelancerServicesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = _ensure_profile(request.user)
        if profile.services.count() >= 20:
            return Response({"detail": "At most 20 services are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        payload = request.data
        service = FreelancerServiceOffering(
            profile=profile,
            title=payload.get("title", ""),
            description=payload.get("description", ""),
            delivery_mode=payload.get("delivery_mode", FreelancerServiceOffering.DeliveryMode.REMOTE),
            starting_price=payload.get("starting_price") or 0,
            response_time_hours=payload.get("response_time_hours") or 24,
            is_active=bool(payload.get("is_active", True)),
            sort_order=payload.get("sort_order") or 0,
        )
        try:
            service.full_clean()
            service.save()
        except ValidationError as exc:
            return Response({"errors": exc.message_dict}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"service": _serialize_service(service)}, status=status.HTTP_201_CREATED)


class OwnerFreelancerServiceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, service_id):
        profile = _ensure_profile(request.user)
        service = get_object_or_404(FreelancerServiceOffering, id=service_id, profile=profile)
        payload = request.data

        updatable_fields = {
            "title",
            "description",
            "delivery_mode",
            "starting_price",
            "response_time_hours",
            "is_active",
            "sort_order",
        }
        for field_name in updatable_fields:
            if field_name in payload:
                setattr(service, field_name, payload.get(field_name))

        try:
            service.full_clean()
            service.save()
        except ValidationError as exc:
            return Response({"errors": exc.message_dict}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"service": _serialize_service(service)})

    def delete(self, request, service_id):
        profile = _ensure_profile(request.user)
        service = get_object_or_404(FreelancerServiceOffering, id=service_id, profile=profile)
        service.delete()
        return Response({"detail": "Deleted."})
