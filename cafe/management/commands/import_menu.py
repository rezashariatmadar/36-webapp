import csv
import os
from django.core.management.base import BaseCommand
from cafe.models import MenuCategory, MenuItem

class Command(BaseCommand):
    help = 'Imports menu items from 36 menu.csv'

    def handle(self, *args, **options):
        file_path = '36 menu.csv'
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File "{file_path}" not found.'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            current_category = None
            category_order = 0
            
            for row in reader:
                if not row or not row[0].strip():
                    continue
                
                name = row[0].strip()
                
                # If row has 1 column or empty second column, it's a category
                if len(row) == 1 or not row[1].strip():
                    category_order += 10
                    current_category, created = MenuCategory.objects.get_or_create(
                        name=name,
                        defaults={'order': category_order}
                    )
                    self.stdout.write(self.style.SUCCESS(f'Category: {name}'))
                    continue
                
                # It's a menu item
                price_str = row[1].strip().replace(',', '')
                
                # Handle price ranges or special strings
                if '–' in price_str or '-' in price_str:
                    # Take the first number in range
                    import re
                    match = re.search(r'\d+', price_str)
                    price = int(match.group()) if match else 0
                else:
                    try:
                        price = int(price_str)
                    except ValueError:
                        price = 0
                
                if current_category:
                    item, created = MenuItem.objects.update_or_create(
                        name=name,
                        category=current_category,
                        defaults={'price': price}
                    )
                    self.stdout.write(f'  Item: {name} - {price} T')
                else:
                    self.stdout.write(self.style.WARNING(f'Skipping item "{name}" because no category was found yet.'))
