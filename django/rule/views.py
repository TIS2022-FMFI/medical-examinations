from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .models import City, Department, PositionRule, ShiftRule


# ############################          ShiftRule      ###########################
class ShiftRuleList(ListView):
    model = ShiftRule


class ShiftRuleDetail(DetailView):
    model = ShiftRule


class ShiftRuleCreate(CreateView):
    model = ShiftRule
    fields = '__all__'
    success_url = reverse_lazy('shifts')


class ShiftRuleUpdate(UpdateView):
    model = ShiftRule
    fields = '__all__'
    success_url = reverse_lazy('shifts')


class ShiftRuleDelete(DeleteView):
    model = ShiftRule
    success_url = reverse_lazy('shifts')


# ############################          Department      ###########################
class DepartmentList(ListView):
    model = Department


class DepartmentDetail(DetailView):
    model = Department


class DepartmentCreate(CreateView):
    model = Department
    fields = '__all__'
    success_url = reverse_lazy('departments')


class DepartmentUpdate(UpdateView):
    model = Department
    fields = '__all__'
    success_url = reverse_lazy('departments')


class DepartmentDelete(DeleteView):
    model = Department
    success_url = reverse_lazy('departments')


# ############################          City            ###########################
class CityList(ListView):
    model = City


class CityDetail(DetailView):
    model = City


class CityCreate(CreateView):
    model = City
    fields = '__all__'
    success_url = reverse_lazy('cities')


class CityUpdate(UpdateView):
    model = City
    fields = '__all__'
    success_url = reverse_lazy('cities')


class CityDelete(DeleteView):
    model = City
    success_url = reverse_lazy('cities')


# ############################      PositionRule        ###########################
class PositionRuleList(ListView):
    model = PositionRule


class PositionRuleDetail(DetailView):
    model = PositionRule


class PositionRuleCreate(CreateView):
    model = PositionRule
    fields = '__all__'
    success_url = reverse_lazy('rules')


class PositionRuleUpdate(UpdateView):
    model = PositionRule
    fields = '__all__'
    success_url = reverse_lazy('rules')


class PositionRuleDelete(DeleteView):
    model = PositionRule
    success_url = reverse_lazy('rules')
