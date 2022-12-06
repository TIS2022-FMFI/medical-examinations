# from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # return super().get_success_url()
        return reverse_lazy('employees')
