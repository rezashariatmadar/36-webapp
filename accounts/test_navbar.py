import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_navbar_profile_rendered(client):
    User = get_user_model()
    user = User.objects.create_user(phone_number='09123456789', password='password', full_name='Test User')
    client.login(phone_number='09123456789', password='password')
    
    response = client.get(reverse('accounts:home'))
    assert response.status_code == 200
    # Check for profile link and dropdown structure
    assert 'پروفایل من' in response.content.decode('utf-8')
    assert 'dropdown dropdown-end' in response.content.decode('utf-8')
    
    # Check for cart icon
    assert reverse('cafe:cart_detail') in response.content.decode('utf-8')
