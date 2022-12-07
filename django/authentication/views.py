# from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    # success_url = reverse_lazy('employees') # toto neslo! neviem preco ???
    
    def get_success_url(self):
        # return super().get_success_url()
        return reverse_lazy('employees')



class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class RegisterView(FormView):
    template_name = 'authentication/register.html'
    form_class = MyUserCreationForm
    success_url = reverse_lazy('employees')
    def form_valid(self, form):
        form.save()
        return super(RegisterView, self).form_valid(form)
