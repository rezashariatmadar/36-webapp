from django.urls import path

from .views import book_space, my_bookings, space_list

app_name = 'cowork'

urlpatterns = [
    path('', space_list, name='space_list'),
    path('book/<int:space_id>/', book_space, name='book_space'),
    path('my-bookings/', my_bookings, name='my_bookings'),
]
