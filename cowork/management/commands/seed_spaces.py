from django.core.management.base import BaseCommand
from cowork.models import Space, PricingPlan

class Command(BaseCommand):
    help = 'Seeds the database with EXACT pricing and spaces.'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing spaces and plans...')
        Space.objects.all().delete()
        PricingPlan.objects.all().delete()

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
                'six_month_rate': 88320000,
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

        # VIP Offices (2-Seat) - 6 Units
        for i in range(1, 7):
            parent_room, _ = Space.objects.update_or_create(
                name=f'اتاق VIP دو نفره {i}',
                defaults={
                    'zone': Space.ZoneType.PRIVATE_ROOM_2,
                    'capacity': 2,
                    'pricing_plan': vip_2_plan,
                    'sort_order': i
                }
            )
            for s in range(1, 3):
                Space.objects.update_or_create(
                    name=f'صندلی {s} - اتاق {i} (2 نفره)',
                    defaults={
                        'zone': Space.ZoneType.PRIVATE_ROOM_2,
                        'capacity': 1,
                        'pricing_plan': vip_2_plan,
                        'parent_table': parent_room,
                        'sort_order': s
                    }
                )

        # VIP Offices (3-Seat) - 4 Units
        for i in range(1, 5):
            parent_room, _ = Space.objects.update_or_create(
                name=f'اتاق VIP سه نفره {i}',
                defaults={
                    'zone': Space.ZoneType.PRIVATE_ROOM_3,
                    'capacity': 3,
                    'pricing_plan': vip_3_plan,
                    'sort_order': i
                }
            )
            for s in range(1, 4):
                Space.objects.update_or_create(
                    name=f'صندلی {s} - اتاق {i} (3 نفره)',
                    defaults={
                        'zone': Space.ZoneType.PRIVATE_ROOM_3,
                        'capacity': 1,
                        'pricing_plan': vip_3_plan,
                        'parent_table': parent_room,
                        'sort_order': s
                    }
                )

        # Individual Desks (12 units)
        for i in range(1, 13):
            Space.objects.update_or_create(
                name=f'میز شخصی {i}',
                defaults={
                    'zone': Space.ZoneType.DESK,
                    'capacity': 1,
                    'pricing_plan': desk_plan,
                    'sort_order': i
                }
            )

        # Monthly Tables (6 tables x 4 seats) = 24 seats
        for t in range(1, 7):
            parent_table, _ = Space.objects.update_or_create(
                name=f'میز ثابت شماره {t}',
                defaults={
                    'zone': Space.ZoneType.SHARED_DESK,
                    'capacity': 4,
                    'pricing_plan': desk_plan,
                    'sort_order': t
                }
            )
            for s in range(1, 5):
                Space.objects.update_or_create(
                    name=f'میز ثابت {t}-{s}',
                    defaults={
                        'zone': Space.ZoneType.SHARED_DESK,
                        'capacity': 1,
                        'pricing_plan': desk_plan,
                        'parent_table': parent_table,
                        'sort_order': s
                    }
                )

        # Communal Long Table (10 seats)
        for i in range(1, 11):
            Space.objects.update_or_create(
                name=f'میز اشتراکی {i}',
                defaults={
                    'zone': Space.ZoneType.LONG_TABLE,
                    'capacity': 1,
                    'pricing_plan': long_table_plan,
                    'sort_order': i
                }
            )

        self.stdout.write(self.style.SUCCESS('All spaces updated with Persian names and correct associations.'))