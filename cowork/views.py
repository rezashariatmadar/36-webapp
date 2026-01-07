from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Space, Booking, PricingPlan
from .forms import BookingForm
from django.db.models import Q
from decimal import Decimal

def space_list(request):
    spaces = Space.objects.filter(is_active=True).select_related('pricing_plan')
    zone = request.GET.get('zone')
    
    if zone:
        spaces = spaces.filter(zone=zone)
    
    if request.htmx:
        return render(request, 'cowork/partials/space_items.html', {'spaces': spaces})
        
    return render(request, 'cowork/space_list.html', {
        'spaces': spaces,
        'zones': Space.ZoneType.choices
    })

@login_required
def book_space(request, space_id):
    space = get_object_or_404(Space, id=space_id)
    plan = space.pricing_plan
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.space = space
            
            # --- Price Calculation Logic ---
            b_type = booking.booking_type
            price = 0
            if b_type == Booking.BookingType.HOURLY:
                diff = booking.end_time - booking.start_time
                hours = Decimal(diff.total_seconds() / 3600)
                price = plan.hourly_rate * hours
            elif b_type == Booking.BookingType.DAILY:
                price = plan.daily_rate
            elif b_type == Booking.BookingType.MONTHLY:
                price = plan.monthly_rate
            elif b_type == Booking.BookingType.SIX_MONTH:
                price = plan.six_month_rate
            elif b_type == Booking.BookingType.YEARLY:
                price = plan.yearly_rate
                
            booking.price_charged = price
            
            # Simulate Upfront Payment Check
            # In a real app, we'd redirect to a payment gateway here
            # For this version, we'll mark as CONFIRMED (Paid) upon POST
            booking.status = Booking.Status.CONFIRMED
            
            try:
                booking.save()
                messages.success(request, f"رزرو شما با موفقیت ثبت شد. مبلغ {int(price)} تومان دریافت شد.")
                return redirect('cowork:my_bookings')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = BookingForm()

    return render(request, 'cowork/book_space.html', {
        'space': space, 
        'form': form,
        'plan': plan
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'cowork/my_bookings.html', {'bookings': bookings})
