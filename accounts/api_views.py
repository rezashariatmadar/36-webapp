from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ProfileForm, UserRegistrationForm
from .models import FreelancerProfile
from .utils import rate_limit


def _session_payload(request):
    csrf_token = get_token(request)
    if not request.user.is_authenticated:
        return {
            "authenticated": False,
            "csrf_token": csrf_token,
            "login_url": "/login/",
        }

    user = request.user
    freelancer_profile = FreelancerProfile.objects.filter(user=user).first()
    return {
        "authenticated": True,
        "csrf_token": csrf_token,
        "login_url": "/login/",
        "logout_url": "/api/auth/logout/",
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
            "freelancer_profile_status": freelancer_profile.status if freelancer_profile else None,
            "freelancer_public_slug": freelancer_profile.public_slug if freelancer_profile else None,
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
