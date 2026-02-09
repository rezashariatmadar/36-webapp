from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.middleware.csrf import get_token
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .forms import ProfileForm, UserRegistrationForm
from .utils import rate_limit

VALID_ROLES = ("Admin", "Barista", "Customer")


def _session_payload(request):
    csrf_token = get_token(request)
    if not request.user.is_authenticated:
        return {
            "authenticated": False,
            "csrf_token": csrf_token,
            "login_url": "/app/account",
        }

    user = request.user
    return {
        "authenticated": True,
        "csrf_token": csrf_token,
        "login_url": "/app/account",
        "logout_url": reverse("accounts:logout"),
        "user": {
            "id": user.id,
            "phone_number": user.phone_number,
            "full_name": user.full_name,
            "national_id": user.national_id,
            "birth_date": user.birth_date.strftime("%Y-%m-%d") if user.birth_date else None,
            "roles": {
                "is_admin": user.is_admin,
                "is_barista": user.is_barista,
                "is_customer": user.is_customer,
            },
        },
    }


class SessionMeAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(_session_payload(request))


class SessionLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not rate_limit(request, scope="api_login", limit=10, window_seconds=300):
            return Response({"detail": "Too many login attempts. Please wait a few minutes."}, status=429)

        phone_number = (request.data.get("phone_number") or "").strip()
        password = request.data.get("password") or ""
        if not phone_number or not password:
            return Response({"detail": "phone_number and password are required."}, status=400)

        user = authenticate(request, username=phone_number, password=password)
        if not user:
            return Response({"detail": "Invalid credentials."}, status=400)
        if not user.is_active:
            return Response({"detail": "User account is inactive."}, status=403)

        login(request, user)
        return Response(_session_payload(request))


class SessionLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(_session_payload(request))


class SessionRegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not rate_limit(request, scope="api_register", limit=5, window_seconds=900):
            return Response({"detail": "Too many sign-up attempts. Please try again later."}, status=429)

        form = UserRegistrationForm(data=request.data)
        if not form.is_valid():
            return Response({"errors": form.errors}, status=400)

        user = form.save()
        customer_group, _ = Group.objects.get_or_create(name="Customer")
        user.groups.add(customer_group)
        login(request, user)
        return Response(_session_payload(request), status=201)


class SessionProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(_session_payload(request))

    def patch(self, request):
        form = ProfileForm(data=request.data, instance=request.user)
        if not form.is_valid():
            return Response({"errors": form.errors}, status=400)

        form.save()
        return Response(_session_payload(request))


class StaffUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "phone_number", "full_name", "is_active", "is_staff", "role"]

    def get_role(self, obj):
        if obj.is_admin:
            return "Admin"
        if obj.is_barista:
            return "Barista"
        if obj.is_customer:
            return "Customer"
        return "Unassigned"


class StaffUserListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not (request.user.is_authenticated and request.user.is_admin):
            return Response({"detail": "Permission denied"}, status=403)
        qs = CustomUser.objects.prefetch_related("groups").order_by("id")
        if "page" in request.GET or "page_size" in request.GET:
            page = max(int(request.GET.get("page", 1)), 1)
            page_size = min(max(int(request.GET.get("page_size", 25)), 1), 100)
            offset = (page - 1) * page_size
            total = qs.count()
            users = qs[offset:offset + page_size]
            serializer = StaffUserSerializer(users, many=True)
            return Response(
                {
                    "count": total,
                    "page": page,
                    "page_size": page_size,
                    "results": serializer.data,
                }
            )
        serializer = StaffUserSerializer(qs, many=True)
        return Response(serializer.data)


class StaffUserStatusAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, user_id):
        if not (request.user.is_authenticated and request.user.is_admin):
            return Response({"detail": "Permission denied"}, status=403)
        target = get_object_or_404(CustomUser, id=user_id)
        if target.id == request.user.id:
            return Response({"detail": "Cannot change your own active status."}, status=400)
        target.is_active = not target.is_active
        target.save(update_fields=["is_active"])
        return Response(StaffUserSerializer(target).data)


class StaffUserRoleAPIView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, user_id):
        if not (request.user.is_authenticated and request.user.is_admin):
            return Response({"detail": "Permission denied"}, status=403)
        new_role = (request.data.get("role") or "").strip()
        if new_role not in VALID_ROLES:
            return Response({"detail": "Invalid role selected."}, status=400)

        target = get_object_or_404(CustomUser, id=user_id)
        target.groups.clear()
        group, _ = Group.objects.get_or_create(name=new_role)
        target.groups.add(group)
        target.is_staff = new_role in ("Admin", "Barista")
        target.save(update_fields=["is_staff"])
        return Response(StaffUserSerializer(target).data)
