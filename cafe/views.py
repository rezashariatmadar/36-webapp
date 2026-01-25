from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Sum, Count, F
from django.utils.translation import gettext_lazy as _
from .models import MenuCategory, MenuItem, CafeOrder, OrderItem
from cowork.models import Booking, Space, PricingPlan
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

def is_staff_member(user):
    return user.is_authenticated and (user.is_staff or user.groups.filter(name__in=['Barista', 'Admin']).exists())

# --- Analytics Dashboard ---

@user_passes_test(is_staff_member)
def admin_dashboard(request):
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
    
    return render(request, 'dashboard.html', context)

# --- Customer Views ---

def menu_view(request):
    categories = MenuCategory.objects.prefetch_related('items').all()
    cart = request.session.get('cart', {})
    cart_items_count = sum(cart.values()) if isinstance(cart, dict) else 0
    return render(request, 'cafe/menu.html', {
        'categories': categories,
        'cart_count': cart_items_count,
        'cart_data': cart
    })

def add_to_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    cart[item_id_str] = cart.get(item_id_str, 0) + 1
    request.session['cart'] = cart
    
    if request.htmx:
        # If the request comes from the CART page, we might want to refresh the whole list
        # otherwise we return the item-specific control
        if 'cart' in request.META.get('HTTP_REFERER', ''):
            return cart_detail(request)
            
        item = get_object_or_404(MenuItem, id=item_id)
        quantity = cart[item_id_str]
        return render(request, 'cafe/partials/item_quantity_control.html', {
            'item': item,
            'quantity': quantity,
            'cart_count': sum(cart.values())
        })
        
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'cafe:menu'
    return redirect(next_url)

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})
    item_id_str = str(item_id)
    if item_id_str in cart:
        if cart[item_id_str] > 1:
            cart[item_id_str] -= 1
        else:
            del cart[item_id_str]
        request.session['cart'] = cart
    
    if request.htmx:
        if 'cart' in request.META.get('HTTP_REFERER', ''):
            return cart_detail(request)
            
        item = get_object_or_404(MenuItem, id=item_id)
        quantity = cart.get(item_id_str, 0)
        return render(request, 'cafe/partials/item_quantity_control.html', {
            'item': item,
            'quantity': quantity,
            'cart_count': sum(cart.values())
        })

    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'cafe:cart_detail'
    return redirect(next_url)

def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0

    # Fetch all items in one query
    fetched_items = MenuItem.objects.filter(id__in=cart.keys())
    items_dict = {str(item.id): item for item in fetched_items}

    for item_id, quantity in cart.items():
        item = items_dict.get(str(item_id))

        if item:
            subtotal = item.price * quantity
            total += subtotal
            items.append({'item': item, 'quantity': quantity, 'subtotal': subtotal})
        else:
            logger.warning(f"Item with ID {item_id} found in cart but does not exist in database.")
            continue
            
    context = {'items': items, 'total': total, 'cart_count': sum(cart.values())}
    if request.htmx:
        return render(request, 'cafe/partials/cart_list.html', context)
        
    return render(request, 'cafe/cart.html', context)

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart: return redirect('cafe:menu')
    
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
            for item_id, quantity in cart.items():
                try:
                    menu_item = MenuItem.objects.get(id=item_id)
                    OrderItem.objects.create(order=order, menu_item=menu_item, quantity=quantity, unit_price=menu_item.price)
                except MenuItem.DoesNotExist: continue
        request.session['cart'] = {}
        messages.success(request, _("Order placed!"))
        return redirect('cafe:order_list')
    
    return render(request, 'cafe/checkout.html', {
        'suggested_location': suggested_location
    })

@login_required
def order_list(request):
    orders = CafeOrder.objects.filter(user=request.user).prefetch_related('items__menu_item')
    return render(request, 'cafe/order_list.html', {'orders': orders})

# --- Staff/Barista Views ---

from accounts.utils import admin_required, barista_required, customer_required
from rest_framework import serializers, viewsets

# --- API Serializers ---

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# --- Barista Views ---

@barista_required
def manual_order_entry(request):
    """View for Baristas to enter orders for walk-in customers."""
    if request.method == 'POST':
        customer_phone = request.POST.get('phone_number')
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
            for key, value in request.POST.items():
                if key.startswith('qty_') and int(value) > 0:
                    item_id = int(key.replace('qty_', ''))
                    quantity = int(value)
                    item = MenuItem.objects.get(id=item_id)
                    OrderItem.objects.create(
                        order=order, 
                        menu_item=item, 
                        quantity=quantity, 
                        unit_price=item.price
                    )
        
        messages.success(request, "سفارش با موفقیت ثبت شد.")
        return redirect('cafe:barista_dashboard')
        
    categories = MenuCategory.objects.prefetch_related('items').all()
    initial_phone = request.GET.get('phone_number', '')
    return render(request, 'cafe/manual_order.html', {
        'categories': categories,
        'initial_phone': initial_phone
    })

@barista_required
def manage_menu_stock(request):
    """View for Baristas to toggle item availability."""
    items = MenuItem.objects.all().order_by('category', 'name')
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(MenuItem, id=item_id)
        item.is_available = not item.is_available
        item.save()
        return redirect('cafe:manage_menu')
    return render(request, 'cafe/manage_menu.html', {'items': items})

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
    
    if request.htmx:
        return render(request, 'cafe/partials/order_list.html', {'orders': active_orders})
        
    return render(request, 'cafe/barista_dashboard.html', {'orders': active_orders})

@user_passes_test(is_staff_member)
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(CafeOrder, id=order_id)
    if new_status in CafeOrder.Status.values:
        order.status = new_status
        order.save()
    
    if request.htmx:
        return barista_dashboard(request)
        
    return redirect('cafe:barista_dashboard')

@user_passes_test(is_staff_member)
def toggle_order_payment(request, order_id):
    order = get_object_or_404(CafeOrder, id=order_id)
    order.is_paid = not order.is_paid
    if order.is_paid:
        order.settled_at = timezone.now()
    else:
        order.settled_at = None
    order.save()
    
    if request.htmx:
        return barista_dashboard(request)
        
    return redirect('cafe:barista_dashboard')
