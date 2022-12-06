# from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Employee

# Create your views here.


class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    # template = 'templates\employee\employee_list'


class EmployeeDetail(LoginRequiredMixin, DetailView):
    model = Employee
    context_object_name = 'employee'
    # template = 'templates\employee\employee_detail'


class EmployeeCreate(LoginRequiredMixin, CreateView):
    model = Employee
    fields = '__all__'
    success_url = reverse_lazy('employees')


class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    fields = '__all__'
    success_url = reverse_lazy('employees')


class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee
    context_object_name = 'employee'
    success_url = reverse_lazy('employees')
