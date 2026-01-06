from django.urls import path
from .views import RegisterView, CustomLoginView, LogoutView, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
