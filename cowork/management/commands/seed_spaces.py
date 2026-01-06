from django.core.management.base import BaseCommand
from cowork.models import Space, PricingPlan

class Command(BaseCommand):
    help = 'Seeds the database with EXACT pricing and spaces.'

    def handle(self, *args, **options):
        # 1. Long Table Plan (Daily Only)
        long_table_plan, _ = PricingPlan.objects.update_or_create(
            name='Long Table (Daily Only)',
            defaults={'daily_rate': 300000}
        )
        
        # 2. Individual Desk Plan
        desk_plan, _ = PricingPlan.objects.update_or_create(
            name='Individual Desk',
            defaults={
                'daily_rate': 450000,
                'monthly_rate': 5940000
            }
        )
        
        # 3. Meeting Room (Contact for Price)
        meeting_plan, _ = PricingPlan.objects.update_or_create(
            name='Meeting Room',
            defaults={'is_contact_for_price': True}
        )
        
        # 4. VIP Office (2-seat)
        vip_2_plan, _ = PricingPlan.objects.update_or_create(
            name='VIP Office (2-Seat)',
            defaults={
                'daily_rate': 300000,
                'monthly_rate': 14080000,
                'six_month_rate': 71040000,
                'yearly_rate': 88800000
            }
        )
        
        # 5. VIP Office (3-seat)
        vip_3_plan, _ = PricingPlan.objects.update_or_create(
            name='VIP Office (3-Seat)',
            defaults={
                'daily_rate': 300000,
                'monthly_rate': 17380000,
                'six_month_rate': 88320020, # Corrected based on user input
                'yearly_rate': 110400000
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Pricing Plans updated with exact rates.'))

        # 6. Create Spaces
        # Meeting Room
        Space.objects.update_or_create(
            name='اتاق جلسه اصلی',
            defaults={
                'zone': Space.ZoneType.MEETING_ROOM,
                'capacity': 8,
                'pricing_plan': meeting_plan
            }
        )

        # VIP Offices
        Space.objects.update_or_create(
            name='اتاق VIP دو نفره',
            defaults={
                'zone': Space.ZoneType.PRIVATE_ROOM,
                'capacity': 2,
                'pricing_plan': vip_2_plan
            }
        )
        Space.objects.update_or_create(
            name='اتاق VIP سه نفره',
            defaults={
                'zone': Space.ZoneType.PRIVATE_ROOM,
                'capacity': 3,
                'pricing_plan': vip_3_plan
            }
        )

        # Individual Desks (12 units)
        for i in range(1, 13):
            Space.objects.update_or_create(
                name=f'میز شخصی {i}',
                defaults={
                    'zone': Space.ZoneType.DESK,
                    'capacity': 1,
                    'pricing_plan': desk_plan
                }
            )

        # Monthly Tables (6 tables x 4 seats) = 24 seats
        for t in range(1, 7):
            for s in range(1, 5):
                Space.objects.update_or_create(
                    name=f'میز ثابت {t}-{s}',
                    defaults={
                        'zone': Space.ZoneType.DESK,
                        'capacity': 1,
                        'pricing_plan': desk_plan
                    }
                )

        # Communal Long Table (10 seats)
        for i in range(1, 11):
            Space.objects.update_or_create(
                name=f'میز اشتراکی {i}',
                defaults={
                    'zone': Space.ZoneType.LONG_TABLE,
                    'capacity': 1,
                    'pricing_plan': long_table_plan
                }
            )

        self.stdout.write(self.style.SUCCESS('All spaces updated with Persian names and correct associations.'))