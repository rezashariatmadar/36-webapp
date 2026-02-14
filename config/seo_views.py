from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone

from accounts.models import FreelancerProfile
from blog.models import BlogPost


def sitemap_xml(request):
    now = timezone.now()
    urls = [
        request.build_absolute_uri("/"),
        request.build_absolute_uri("/blog/"),
        request.build_absolute_uri("/freelancers/"),
    ]

    blog_urls = (
        BlogPost.objects.filter(status=BlogPost.Status.PUBLISHED)
        .filter(Q(published_at__isnull=True) | Q(published_at__lte=now))
        .values_list("slug", flat=True)
        .order_by("-published_at", "-id")
    )
    urls.extend(request.build_absolute_uri(f"/blog/{slug}/") for slug in blog_urls)

    freelancer_urls = (
        FreelancerProfile.objects.filter(
            status=FreelancerProfile.Status.PUBLISHED,
            is_public=True,
        )
        .values_list("public_slug", flat=True)
        .order_by("-updated_at", "-id")
    )
    urls.extend(request.build_absolute_uri(f"/freelancers/{slug}/") for slug in freelancer_urls)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        lines.extend(["<url>", f"<loc>{url}</loc>", "</url>"])
    lines.append("</urlset>")

    return HttpResponse("\n".join(lines), content_type="application/xml; charset=utf-8")


def robots_txt(request):
    body = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "Disallow: /admin/",
            "Disallow: /api/",
            f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        ]
    )
    return HttpResponse(body, content_type="text/plain; charset=utf-8")
