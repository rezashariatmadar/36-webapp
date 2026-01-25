from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Space, Booking, PricingPlan
from .forms import BookingForm
from django.db.models import Q, Exists, OuterRef
from decimal import Decimal

def space_list(request):
    # Refresh statuses based on current time
    now = timezone.now().date()

    # Check for active bookings efficiently
    active_booking_exists = Booking.objects.filter(
        space=OuterRef('pk'),
        status=Booking.Status.CONFIRMED,
        start_time__lte=now,
        end_time__gte=now
    )

    all_active_spaces = Space.objects.filter(is_active=True).annotate(
        has_active_booking=Exists(active_booking_exists)
    )

    spaces_to_update = []
    for s in all_active_spaces:
        if s.status == Space.Status.UNAVAILABLE:
            continue

        new_status = Space.Status.OCCUPIED if s.has_active_booking else Space.Status.AVAILABLE

        if s.status != new_status:
            s.status = new_status
            spaces_to_update.append(s)

    if spaces_to_update:
        Space.objects.bulk_update(spaces_to_update, ['status'])
        
    # Fetch all active spaces that are NOT individual seats of a parent table
    all_top_level_spaces = Space.objects.filter(is_active=True, parent_table__isnull=True).select_related('pricing_plan').prefetch_related('seats')
    
    # Group spaces by zone for client-side rendering
    zones_with_spaces = []
    for code, label in Space.ZoneType.choices:
        zones_with_spaces.append({
            'code': code,
            'label': label,
            'spaces': [s for s in all_top_level_spaces if s.zone == code]
        })
        
    if request.htmx:
        return render(request, 'cowork/partials/zone_list.html', {
            'zones_with_spaces': zones_with_spaces
        })
        
    return render(request, 'cowork/space_list.html', {
        'zones_with_spaces': zones_with_spaces
    })

@login_required
def book_space(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    plan = space.pricing_plan
    
    if request.method == 'POST':
        form = BookingForm(request.POST, space=space)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.space = space
            
            # --- Price Calculation Logic ---
            price = booking.calculate_price()
            booking.price_charged = price
            
            # Simulate Upfront Payment Check
            booking.status = Booking.Status.CONFIRMED
            
            try:
                booking.save()
                space.refresh_status() # Update seat status based on the new booking
                messages.success(request, "درخواست رزرو شما ثبت شد و توسط مدیریت بررسی خواهد شد.")
                return redirect('cowork:my_bookings')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = BookingForm(space=space)

    # Handle HTMX dynamic preview
    if request.htmx:
        # Update form instance with current data to calculate end_time
        booking_type = request.GET.get('booking_type')
        start_time_str = request.GET.get('start_time')
        
        preview_booking = Booking(space=space, booking_type=booking_type)
        if start_time_str:
            try:
                # Try parsing as Jalali first (from UI)
                import jdatetime
                preview_booking.start_time = jdatetime.datetime.strptime(start_time_str, '%Y-%m-%d').togregorian().date()
            except (ValueError, TypeError):
                # Fallback to Gregorian
                try:
                    from datetime import datetime
                    preview_booking.start_time = datetime.strptime(start_time_str, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    pass
        
        # We'll use the form logic to get the end_time
        temp_form = BookingForm(data=request.GET, space=space)
        calculated_end = None
        calculated_end_jalali = None
        
        if temp_form.is_valid():
            calculated_end = temp_form.cleaned_data.get('end_time')
        else:
            # If not valid, still try to trigger calculation logic
            temp_form.full_clean()
            calculated_end = temp_form.cleaned_data.get('end_time')
            
        # Update preview booking with the calculated end time for accurate price
        if calculated_end:
            preview_booking.end_time = calculated_end
            # calculated_end is already a jdatetime.date from the jforms.jDateField
            calculated_end_jalali = calculated_end.strftime("%Y/%m/%d")
        
        price = preview_booking.calculate_price()

        return render(request, 'cowork/partials/booking_preview.html', {
            'space': space,
            'form': temp_form,
            'price': price,
            'calculated_end': calculated_end,
            'calculated_end_jalali': calculated_end_jalali
        })

    return render(request, 'cowork/book_space.html', {
        'space': space, 
        'form': form,
        'plan': plan
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'cowork/my_bookings.html', {'bookings': bookings})
