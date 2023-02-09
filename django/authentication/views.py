# from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password

from django.urls import reverse_lazy

from django.contrib.auth import views as auth_views

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    # success_url = reverse_lazy('employees') # toto neslo! neviem preco ???
    
    def get_success_url(self):
        # return super().get_success_url()
        return reverse_lazy('employees')

class MyUserCreationForm(forms.Form):
    name = forms.CharField(label="Meno", max_length=150)
    email = forms.EmailField(label="Email", required=True)


class RegisterView(LoginRequiredMixin, FormView):
    template_name = 'authentication/register.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('employees')
    
    def form_valid(self, form):
        User.objects.create(
            username=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            password=make_password(User.objects.make_random_password()))
        return super(RegisterView, self).form_valid(form)


class MyPasswordResetView(auth_views.PasswordResetView):
    email_template_name = "authentication/password_reset_email.html"