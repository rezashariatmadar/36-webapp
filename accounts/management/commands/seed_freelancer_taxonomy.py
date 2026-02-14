from django.core.management.base import BaseCommand

from accounts.models import FreelancerFlair, FreelancerSpecialtyTag


SPECIALTIES = [
    "UI/UX Design",
    "Frontend Development",
    "Backend Development",
    "Mobile Development",
    "SEO Strategy",
    "Content Marketing",
    "Brand Design",
    "Product Management",
    "Video Editing",
    "Photography",
]

FLAIRS = [
    {"name": "Top Rated", "color_token": "#6d79ff", "icon_name": "sparkles"},
    {"name": "Verified", "color_token": "#22c55e", "icon_name": "badge-check"},
    {"name": "Remote", "color_token": "#0ea5e9", "icon_name": "wifi"},
    {"name": "Urgent Available", "color_token": "#f97316", "icon_name": "zap"},
]


def _slugify_ascii(value: str) -> str:
    return (
        value.lower()
        .replace("&", "and")
        .replace("/", "-")
        .replace(" ", "-")
        .replace("_", "-")
    )


class Command(BaseCommand):
    help = "Seed default freelancer specialties and flairs."

    def handle(self, *args, **options):
        for index, name in enumerate(SPECIALTIES):
            obj, created = FreelancerSpecialtyTag.objects.get_or_create(
                slug=_slugify_ascii(name),
                defaults={
                    "name": name,
                    "is_active": True,
                    "sort_order": index,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created specialty: {obj.name}"))

        for index, flair in enumerate(FLAIRS):
            obj, created = FreelancerFlair.objects.get_or_create(
                slug=_slugify_ascii(flair["name"]),
                defaults={
                    "name": flair["name"],
                    "color_token": flair["color_token"],
                    "icon_name": flair["icon_name"],
                    "is_active": True,
                    "sort_order": index,
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created flair: {obj.name}"))

        self.stdout.write(self.style.SUCCESS("Freelancer taxonomy seed complete."))

