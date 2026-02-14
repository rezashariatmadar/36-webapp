from django.urls import path

from .api_views import BlogPostDetailAPIView, BlogPostsAPIView, BlogTagsAPIView

app_name = "blog_api"

urlpatterns = [
    path("posts/", BlogPostsAPIView.as_view(), name="posts"),
    path("posts/<slug:slug>/", BlogPostDetailAPIView.as_view(), name="post_detail"),
    path("tags/", BlogTagsAPIView.as_view(), name="tags"),
]

