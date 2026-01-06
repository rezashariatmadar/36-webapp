from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.contrib.auth.models import Group

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Assign user to 'Customer' group by default
        customer_group, created = Group.objects.get_or_create(name='Customer')
        self.object.groups.add(customer_group)
        return response

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'

def home_view(request):
    return render(request, 'home.html')