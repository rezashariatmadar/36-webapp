from django.urls import path
from .views import menu_view

app_name = 'cafe'

urlpatterns = [
    path('menu/', menu_view, name='menu'),
]
