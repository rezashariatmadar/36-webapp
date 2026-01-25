from django.urls import path
from .views import space_list, book_space, my_bookings, map_builder, update_space_coordinates

app_name = 'cowork'

urlpatterns = [
    path('', space_list, name='space_list'),
    path('map-builder/', map_builder, name='map_builder'),
    path('api/update-coords/<int:space_id>/', update_space_coordinates, name='update_space_coordinates'),
    path('book/<int:space_id>/', book_space, name='book_space'),
    path('my-bookings/', my_bookings, name='my_bookings'),
]
