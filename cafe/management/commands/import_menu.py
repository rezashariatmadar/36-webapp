import csv
import re
from pathlib import Path

from django.core.management.base import BaseCommand

from cafe.models import MenuCategory, MenuItem


class Command(BaseCommand):
    help = "Imports menu items from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            default="36 menu.csv",
            help="Path to CSV menu file (defaults to `36 menu.csv` in repo root).",
        )

    def _resolve_file_path(self, raw_path):
        path = Path(raw_path)
        if path.is_absolute():
            return path
        return Path.cwd() / path

    def _parse_price(self, raw_price):
        normalized = (raw_price or "").strip().replace(",", "").replace("٬", "")
        match = re.search(r"\d+", normalized)
        return int(match.group()) if match else 0

    def handle(self, *args, **options):
        file_path = self._resolve_file_path(options["file"])
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f'File "{file_path}" not found.'))
            return

        current_category = None
        category_order = 0
        created_categories = 0
        updated_categories = 0
        created_items = 0
        updated_items = 0

        with file_path.open("r", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if not row or not row[0].strip():
                    continue

                # Handle BOM if present in the first value.
                name = row[0].lstrip("\ufeff").strip()
                if not name:
                    continue

                is_category_row = len(row) == 1 or (len(row) > 1 and not row[1].strip())
                if is_category_row:
                    category_order += 10
                    current_category, created = MenuCategory.objects.update_or_create(
                        name=name,
                        defaults={"order": category_order},
                    )
                    if created:
                        created_categories += 1
                    else:
                        updated_categories += 1
                    continue

                if current_category is None:
                    self.stdout.write(
                        self.style.WARNING(f'Skipping item "{name}" because no category was found yet.')
                    )
                    continue

                price = self._parse_price(row[1])
                _, created = MenuItem.objects.update_or_create(
                    name=name,
                    category=current_category,
                    defaults={"price": price, "is_available": True},
                )
                if created:
                    created_items += 1
                else:
                    updated_items += 1

        self.stdout.write(self.style.SUCCESS("Menu import complete."))
        self.stdout.write(
            f"Categories: created={created_categories}, updated={updated_categories}, total={MenuCategory.objects.count()}"
        )
        self.stdout.write(
            f"Menu items: created={created_items}, updated={updated_items}, total={MenuItem.objects.count()}"
        )
