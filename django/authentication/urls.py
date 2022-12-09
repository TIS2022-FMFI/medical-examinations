from django.urls import path

from .views import CustomLoginView, RegisterView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="authentication/password_reset.html"), 
        name='password_reset'), # submit email form

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="authentication/password_reset_sent.html"), 
        name='password_reset_done'), # Email sent succesfully msg
    
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_form.html"), 
        name='password_reset_confirm'), # link to password reset from email

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset_complete.html"), 
        name='password_reset_complete'), # password succesfully changed msg
]