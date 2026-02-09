from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Sum, Count, F, Max
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.conf import settings
from django.core.cache import cache
from .models import MenuCategory, MenuItem, CafeOrder, OrderItem
from cowork.models import Booking, Space, PricingPlan
from django.utils import timezone
from datetime import timedelta
import logging
from django.shortcuts import Http404

logger = logging.getLogger(__name__)

CART_SCHEMA_VERSION = 1
MAX_CART_ITEMS = 50
MAX_PER_ITEM = 20
CAFE_SPA_PATH = "/app/cafe"
STAFF_SPA_PATH = "/app/staff"

def is_staff_member(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name__in=['Barista', 'Admin']).exists())


def _get_cart(request):
    """
    Retrieves a validated cart from session, resetting if schema changed or malformed.
    """
    cart = request.session.get('cart', {})
    version = request.session.get('cart_v')
    if not isinstance(cart, dict):
        cart = {}
    if version != CART_SCHEMA_VERSION:
        request.session['cart_v'] = CART_SCHEMA_VERSION
        # keep existing cart if it was a dict; otherwise cleared above
        request.session['cart'] = cart
    return cart


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session['cart_v'] = CART_SCHEMA_VERSION

# --- Analytics Dashboard ---

@user_passes_test(is_staff_member)
def admin_dashboard(request):
    cache_key = "dashboard:metrics"
    context = cache.get(cache_key)
    if not context:
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # 1. Cafe Analytics
        cafe_total_sales = CafeOrder.objects.filter(is_paid=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
        cafe_today_sales = CafeOrder.objects.filter(is_paid=True, created_at__gte=today_start).aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        top_selling_items = OrderItem.objects.values('menu_item__name').annotate(
            total_qty=Sum('quantity'),
            total_rev=Sum(F('quantity') * F('unit_price'))
        ).order_by('-total_qty')[:5]
        
        top_cafe_buyers = CafeOrder.objects.filter(is_paid=True, user__isnull=False).values(
            'user__phone_number', 'user__full_name'
        ).annotate(
            total_spent=Sum('total_price')
        ).order_by('-total_spent')[:5]

        # 2. Coworking Analytics
        cowork_total_rev = Booking.objects.filter(status=Booking.Status.CONFIRMED).aggregate(Sum('price_charged'))['price_charged__sum'] or 0
        
        total_spaces = Space.objects.filter(is_active=True).count()
        active_bookings_count = Booking.objects.filter(
            status=Booking.Status.CONFIRMED,
            start_time__lte=now,
            end_time__gte=now
        ).count()
        
        occupancy_rate = (active_bookings_count / total_spaces * 100) if total_spaces > 0 else 0
        
        top_cowork_members = Booking.objects.filter(status=Booking.Status.CONFIRMED).values(
            'user__phone_number', 'user__full_name'
        ).annotate(
            total_spent=Sum('price_charged'),
            total_bookings=Count('id')
        ).order_by('-total_spent')[:5]

        context = {
            'cafe_total': cafe_total_sales,
            'cafe_today': cafe_today_sales,
            'top_items': top_selling_items,
            'top_cafe_buyers': top_cafe_buyers,
            
            'cowork_total': cowork_total_rev,
            'occupancy_rate': int(occupancy_rate),
            'active_bookings': active_bookings_count,
            'top_cowork_members': top_cowork_members,
            'total_spaces': total_spaces,
        }
        cache.set(cache_key, context, 60)
    
    return render(request, 'dashboard.html', context)

# --- Customer Views ---

def menu_view(request):
    categories = MenuCategory.objects.prefetch_related('items').all()
    has_menu_items = MenuItem.objects.filter(is_available=True).exists()
    cart = _get_cart(request)
    cart_items_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return render(request, 'cafe/menu.html', {
        'categories': categories,
        'has_menu_items': has_menu_items,
        'cart_count': cart_items_count,
        'cart_data': cart
    })

def add_to_cart(request, item_id):
    cart = _get_cart(request)
    item_id_str = str(item_id)
    item = get_object_or_404(MenuItem, id=item_id)

    if not item.is_available:
        messages.error(request, _("Item is currently unavailable."))
        return redirect(request.META.get('HTTP_REFERER', CAFE_SPA_PATH))

    current_total = sum(cart.values())
    if current_total >= MAX_CART_ITEMS:
        messages.error(request, _("Cart limit reached."))
        return redirect(request.META.get('HTTP_REFERER', CAFE_SPA_PATH))

    cart[item_id_str] = cart.get(item_id_str, 0) + 1
    if cart[item_id_str] > MAX_PER_ITEM:
        cart[item_id_str] = MAX_PER_ITEM
        messages.warning(request, _("Maximum quantity per item reached."))

    _save_cart(request, cart)
    
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or CAFE_SPA_PATH
    return redirect(next_url)

def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    item_id_str = str(item_id)
    if item_id_str in cart:
        if cart[item_id_str] > 1:
            cart[item_id_str] -= 1
        else:
            del cart[item_id_str]
        _save_cart(request, cart)
    
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or CAFE_SPA_PATH
    return redirect(next_url)

def cart_detail(request):
    cart = _get_cart(request)
    items = []
    total = 0

    # Fetch all items in one query
    fetched_items = MenuItem.objects.filter(id__in=cart.keys())
    items_dict = {str(item.id): item for item in fetched_items}

    for item_id, quantity in list(cart.items()):
        item = items_dict.get(str(item_id))

        if item:
            subtotal = item.price * quantity
            total += subtotal
            items.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})
        else:
            logger.warning(f"Item with ID {item_id} found in cart but does not exist in database.")
            cart.pop(str(item_id), None)
            _save_cart(request, cart)
            continue
            
    context = {'items': items, 'total': total, 'cart_count': sum(cart.values())}
    return render(request, 'cafe/cart.html', context)

@login_required
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect(CAFE_SPA_PATH)
    
    # Try to find an active booking for this user to pre-fill the delivery location
    now = timezone.now()
    active_booking = Booking.objects.filter(
        user=request.user,
        status=Booking.Status.CONFIRMED,
        start_time__lte=now,
        end_time__gte=now
    ).first()
    
    suggested_location = ""
    if active_booking:
        suggested_location = active_booking.space.name

    if request.method == 'POST':
        notes = request.POST.get('notes', '')
        with transaction.atomic():
            order = CafeOrder.objects.create(user=request.user, notes=notes)

            # Optimization: Fetch all items at once to avoid N+1 queries
            item_ids = [int(k) for k in cart.keys() if str(k).isdigit()]
            menu_items = MenuItem.objects.in_bulk(item_ids)

            order_items = []
            total_price = 0

            for item_id_str, quantity in cart.items():
                if not str(item_id_str).isdigit():
                    continue
                item_id = int(item_id_str)
                try:
                    quantity = int(quantity)
                except (ValueError, TypeError):
                    continue

                if quantity < 1 or quantity > MAX_PER_ITEM:
                    continue

                if item_id in menu_items:
                    menu_item = menu_items[item_id]
                    if not menu_item.is_available:
                        messages.error(request, _("One or more items are unavailable. Please update your cart."))
                        transaction.set_rollback(True)
                        return redirect(CAFE_SPA_PATH)

                    # Create OrderItem instance
                    order_items.append(OrderItem(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        unit_price=menu_item.price
                    ))
                    total_price += menu_item.price * quantity

            if order_items:
                OrderItem.objects.bulk_create(order_items)

            # Update total price once
            order.total_price = total_price
            order.save()

        _save_cart(request, {})
        messages.success(request, _("Order placed!"))
        return redirect(CAFE_SPA_PATH)
    
    return render(request, 'cafe/checkout.html', {
        'suggested_location': suggested_location
    })

@login_required
def order_list(request):
    orders = CafeOrder.objects.filter(user=request.user).prefetch_related('items__menu_item')
    return render(request, 'cafe/order_list.html', {'orders': orders})

@login_required
@require_POST
def reorder_order(request, order_id):
    """
    Rebuilds the cart from a past order.
    """
    order = get_object_or_404(CafeOrder.objects.prefetch_related('items__menu_item'), id=order_id, user=request.user)
    cart = {}
    for item in order.items.all():
        # clamp to max per item to stay within limits
        qty = min(item.quantity, MAX_PER_ITEM)
        cart[str(item.menu_item_id)] = qty
    _save_cart(request, cart)
    messages.success(request, _("Order added to cart. You can review and checkout again."))
    return redirect(CAFE_SPA_PATH)

# --- Staff/Barista Views ---

from accounts.utils import admin_required, barista_required, customer_required, normalize_digits
from rest_framework import serializers, viewsets, permissions
from rest_framework.response import Response

# --- API Serializers ---

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class PublicMenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'is_available']

class StaffOrAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and is_staff_member(user))


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [StaffOrAdminPermission]


class PublicMenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only menu API for kiosks/public clients, cached for 60s.
    """
    queryset = MenuItem.objects.filter(is_available=True).select_related('category')
    serializer_class = PublicMenuItemSerializer
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        cache_key = "api:public_menu_items"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, 60)
        return response

# --- Barista Views ---

@barista_required
def manual_order_entry(request):
    """View for Baristas to enter orders for walk-in customers."""
    if request.method == 'POST':
        customer_phone = normalize_digits(request.POST.get('phone_number'))
        notes = request.POST.get('notes', 'Walk-in Guest')
        
        user = None
        if customer_phone:
            from accounts.models import CustomUser
            user = CustomUser.objects.filter(phone_number=customer_phone).first()
            
        with transaction.atomic():
            order = CafeOrder.objects.create(
                user=user,
                notes=notes,
                is_paid=True # Assume paid for walk-ins usually
            )
            
            # Extract items and quantities
            # Expecting keys like 'qty_5' where 5 is the item ID
            item_quantities = {}
            for key, value in request.POST.items():
                if not key.startswith('qty_'):
                    continue
                try:
                    qty_val = int(value)
                    item_id = int(key.replace('qty_', ''))
                except (ValueError, TypeError):
                    continue

                if qty_val <= 0 or qty_val > MAX_PER_ITEM:
                    continue

                item_quantities[item_id] = qty_val

            if item_quantities:
                items = MenuItem.objects.in_bulk(list(item_quantities.keys()))
                items_to_create = []

                for item_id, quantity in item_quantities.items():
                    if item_id in items:
                        item = items[item_id]
                        items_to_create.append(OrderItem(
                            order=order,
                            menu_item=item,
                            quantity=quantity,
                            unit_price=item.price
                        ))

                if items_to_create:
                    OrderItem.objects.bulk_create(items_to_create)
                    order.update_total_price()
        
        messages.success(request, "سفارش با موفقیت ثبت شد.")
        return redirect(STAFF_SPA_PATH)
        
    categories = MenuCategory.objects.prefetch_related('items').all()
    has_menu_items = MenuItem.objects.filter(is_available=True).exists()
    initial_phone = request.GET.get('phone_number', '')
    return render(request, 'cafe/manual_order.html', {
        'categories': categories,
        'has_menu_items': has_menu_items,
        'initial_phone': initial_phone
    })

@barista_required
def manage_menu_stock(request):
    """View for Baristas to toggle item availability."""
    items = MenuItem.objects.all().order_by('category', 'name')
    categories = MenuCategory.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action', 'toggle')
        if action == 'create_item':
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            price_raw = request.POST.get('price', '').strip()
            category_id = request.POST.get('category_id', '').strip()
            new_category = request.POST.get('new_category', '').strip()
            is_available = request.POST.get('is_available') == 'on'

            if not name or not price_raw:
                messages.error(request, "نام و قیمت را وارد کنید.")
                return redirect(STAFF_SPA_PATH)

            try:
                price = Decimal(price_raw)
            except InvalidOperation:
                messages.error(request, "قیمت نامعتبر است.")
                return redirect(STAFF_SPA_PATH)

            if price < 0:
                messages.error(request, "قیمت نمی‌تواند منفی باشد.")
                return redirect(STAFF_SPA_PATH)

            category = None
            if new_category:
                max_order = MenuCategory.objects.aggregate(
                    max_order=Max('order')
                )['max_order'] or 0
                category, _ = MenuCategory.objects.get_or_create(
                    name=new_category,
                    defaults={'order': max_order + 10}
                )
            elif category_id:
                category = get_object_or_404(MenuCategory, id=category_id)
            else:
                messages.error(request, "دسته‌بندی را انتخاب کنید.")
                return redirect(STAFF_SPA_PATH)

            MenuItem.objects.create(
                name=name,
                description=description,
                category=category,
                price=price,
                is_available=is_available
            )
            messages.success(request, "آیتم جدید اضافه شد.")
            return redirect(STAFF_SPA_PATH)

        item_id = request.POST.get('item_id')
        try:
            item = get_object_or_404(MenuItem, id=int(item_id))
        except (TypeError, ValueError):
            messages.error(request, "شناسه آیتم نامعتبر است.")
            return redirect(STAFF_SPA_PATH)
        item.is_available = not item.is_available
        item.save()
        return redirect(STAFF_SPA_PATH)

    return render(request, 'cafe/manage_menu.html', {
        'items': items,
        'categories': categories
    })

@barista_required
def customer_lookup(request):
    """Simple search for Baristas to find customer profiles."""
    query = request.GET.get('q', '')
    customers = []
    if query:
        customers = CustomUser.objects.filter(
            Q(phone_number__icontains=query) | Q(full_name__icontains=query)
        ).filter(groups__name='Customer')[:10]
    return render(request, 'cafe/customer_lookup.html', {'customers': customers, 'query': query})

@user_passes_test(is_staff_member)
def barista_dashboard(request):
    active_orders = CafeOrder.objects.filter(~Q(status__in=[CafeOrder.Status.DELIVERED, CafeOrder.Status.CANCELLED])).prefetch_related('items__menu_item').order_by('created_at')
    return render(request, 'cafe/barista_dashboard.html', {'orders': active_orders})

@user_passes_test(is_staff_member)
@require_POST
def update_order_status(request, order_id, new_status):
    if new_status not in CafeOrder.Status.values:
        return HttpResponseBadRequest("Invalid status")

    with transaction.atomic():
        order = CafeOrder.objects.select_for_update().get(id=order_id)
        previous = order.status
        order.status = new_status
        order.save()
    logger.info(
        "Order status changed",
        extra={"order_id": order_id, "from": previous, "to": new_status, "actor": request.user.id, "ip": request.META.get("REMOTE_ADDR")}
    )
    
    return redirect(STAFF_SPA_PATH)

@user_passes_test(is_staff_member)
@require_POST
def toggle_order_payment(request, order_id):
    with transaction.atomic():
        order = CafeOrder.objects.select_for_update().get(id=order_id)
        previous = order.is_paid
        order.is_paid = not order.is_paid
        if order.is_paid:
            order.settled_at = timezone.now()
        else:
            order.settled_at = None
        order.save()
    logger.info(
        "Order payment toggled",
        extra={"order_id": order_id, "from": previous, "to": order.is_paid, "actor": request.user.id, "ip": request.META.get("REMOTE_ADDR")}
    )
    
    return redirect(STAFF_SPA_PATH)
