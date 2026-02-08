from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST
from .models import CustomUser
from .utils import admin_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

VALID_ROLES = ('Admin', 'Barista', 'Customer')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'full_name', 'is_active', 'is_staff']

class UserListAPI(APIView):
    def get(self, request):
        if not (request.user.is_authenticated and request.user.is_admin):
            return Response({"detail": "Permission denied"}, status=403)
        qs = CustomUser.objects.order_by("id")
        if "page" in request.GET or "page_size" in request.GET:
            page = max(int(request.GET.get("page", 1)), 1)
            page_size = min(max(int(request.GET.get("page_size", 25)), 1), 100)
            offset = (page - 1) * page_size
            total = qs.count()
            users = qs[offset:offset + page_size]
            serializer = UserSerializer(users, many=True)
            return Response({
                "count": total,
                "page": page,
                "page_size": page_size,
                "results": serializer.data,
            })
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

@admin_required
def admin_user_list(request):
    users = CustomUser.objects.all().prefetch_related('groups')
    
    # Group users by roles for hierarchical model
    roles_with_users = [
        {
            'name': 'Admin',
            'label': 'مدیران سیستم',
            'users': [u for u in users if u.is_admin],
            'class': 'badge-primary'
        },
        {
            'name': 'Barista',
            'label': 'باریستاها',
            'users': [u for u in users if u.is_barista and not u.is_admin],
            'class': 'badge-accent'
        },
        {
            'name': 'Customer',
            'label': 'مشتریان',
            'users': [u for u in users if u.is_customer and not u.is_admin and not u.is_barista],
            'class': 'badge-ghost'
        },
        {
            'name': 'Unassigned',
            'label': 'بدون نقش',
            'users': [u for u in users if not u.groups.exists() and not u.is_superuser],
            'class': 'badge-neutral'
        }
    ]
    
    return render(request, 'accounts/admin_user_list.html', {
        'roles_with_users': roles_with_users,
        'total_count': users.count()
    })

@admin_required
@require_POST
def toggle_user_status(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f"User {user.phone_number} status updated.")
    return redirect('accounts:user_list')

@admin_required
def change_user_role(request, user_id, new_role):
    user = get_object_or_404(CustomUser, id=user_id)

    if new_role not in VALID_ROLES:
        messages.error(request, "Invalid role selected.")
        return redirect('accounts:user_list')
        
    try:
        # Clear existing functional groups
        user.groups.clear()
        
        # Add new group
        group, _ = Group.objects.get_or_create(name=new_role)
        user.groups.add(group)
        
        # Update is_staff flag if needed
        if new_role in ('Admin', 'Barista'):
            user.is_staff = True
        else:
            user.is_staff = False
        user.save()
        
        messages.success(request, f"User {user.phone_number} promoted to {new_role}.")
    except Exception as e:
        messages.error(request, f"Error updating role: {e}")
        
    return redirect('accounts:user_list')

def home_view(request):
    return render(request, 'home.html')
