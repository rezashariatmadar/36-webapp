from cowork.models import Space, PricingPlan
import random

print("Starting population...")

# Ensure a default pricing plan
plan, _ = PricingPlan.objects.get_or_create(
    name="Standard Plan",
    defaults={
        'daily_rate': 150000,
        'hourly_rate': 25000,
        'monthly_rate': 3500000
    }
)

# 1. Main Shared Area (Center) - Desks
# Grid of 4x3 desks in the middle
start_x, start_y = 35, 30
gap_x, gap_y = 8, 6

count = 1
created_count = 0
for row in range(3):
    for col in range(4):
        s, created = Space.objects.get_or_create(
            name=f"Desk A{count}",
            defaults={
                'zone': Space.ZoneType.DESK,
                'pricing_plan': plan,
                'x_pos': start_x + (col * gap_x),
                'y_pos': start_y + (row * gap_y),
                'status': random.choice([Space.Status.AVAILABLE, Space.Status.AVAILABLE, Space.Status.OCCUPIED])
            }
        )
        if created: created_count += 1
        count += 1

# 2. Long Table (Top)
# 6 seats in a row
start_x, start_y = 30, 15
gap_x = 5
for i in range(6):
    s, created = Space.objects.get_or_create(
        name=f"Long Table {i+1}",
        defaults={
            'zone': Space.ZoneType.LONG_TABLE,
            'pricing_plan': plan,
            'x_pos': start_x + (i * gap_x),
            'y_pos': start_y,
            'status': Space.Status.AVAILABLE
        }
    )
    if created: created_count += 1

# 3. Private Rooms (Right Side)
# 3 rooms vertical
start_x, start_y = 85, 25
gap_y = 15
for i in range(3):
    s, created = Space.objects.get_or_create(
        name=f"Private Room {i+1}",
        defaults={
            'zone': Space.ZoneType.PRIVATE_ROOM_3,
            'pricing_plan': plan,
            'x_pos': start_x,
            'y_pos': start_y + (i * gap_y),
            'status': random.choice([Space.Status.AVAILABLE, Space.Status.OCCUPIED])
        }
    )
    if created: created_count += 1

print(f"Spaces populated successfully! Created {created_count} new spaces.")
