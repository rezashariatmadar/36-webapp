from django.shortcuts import render
from .models import MenuCategory

def menu_view(request):
    categories = MenuCategory.objects.prefetch_related('items').all()
    return render(request, 'cafe/menu.html', {'categories': categories})