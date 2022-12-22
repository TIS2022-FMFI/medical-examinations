from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import City, Department, PositionRule, ShiftRule


# ############################          ShiftRule      ###########################
class ShiftRuleList(LoginRequiredMixin, ListView):
    model = ShiftRule


class ShiftRuleDetail(LoginRequiredMixin, DetailView):
    model = ShiftRule


class ShiftRuleCreate(LoginRequiredMixin, CreateView):
    model = ShiftRule
    fields = '__all__'
    success_url = reverse_lazy('shifts')


class ShiftRuleUpdate(LoginRequiredMixin, UpdateView):
    model = ShiftRule
    fields = '__all__'
    success_url = reverse_lazy('shifts')


class ShiftRuleDelete(LoginRequiredMixin, DeleteView):
    model = ShiftRule
    success_url = reverse_lazy('shifts')


# ############################          Department      ###########################
class DepartmentList(LoginRequiredMixin, ListView):
    model = Department


class DepartmentDetail(LoginRequiredMixin, DetailView):
    model = Department


class DepartmentCreate(LoginRequiredMixin, CreateView):
    model = Department
    fields = '__all__'
    success_url = reverse_lazy('departments')


class DepartmentUpdate(LoginRequiredMixin, UpdateView):
    model = Department
    fields = '__all__'
    success_url = reverse_lazy('departments')


class DepartmentDelete(LoginRequiredMixin, DeleteView):
    model = Department
    success_url = reverse_lazy('departments')


# ############################          City            ###########################
class CityList(LoginRequiredMixin, ListView):
    model = City


class CityDetail(LoginRequiredMixin, DetailView):
    model = City


class CityCreate(LoginRequiredMixin, CreateView):
    model = City
    fields = '__all__'
    success_url = reverse_lazy('cities')


class CityUpdate(LoginRequiredMixin, UpdateView):
    model = City
    fields = '__all__'
    success_url = reverse_lazy('cities')


class CityDelete(LoginRequiredMixin, DeleteView):
    model = City
    success_url = reverse_lazy('cities')


# ############################      PositionRule        ###########################
class PositionRuleList(LoginRequiredMixin, ListView):
    model = PositionRule


class PositionRuleDetail(LoginRequiredMixin, DetailView):
    model = PositionRule


class PositionRuleCreate(LoginRequiredMixin, CreateView):
    model = PositionRule
    fields = '__all__'
    success_url = reverse_lazy('rules')


class PositionRuleUpdate(LoginRequiredMixin, UpdateView):
    model = PositionRule
    fields = '__all__'
    success_url = reverse_lazy('rules')


class PositionRuleDelete(LoginRequiredMixin, DeleteView):
    model = PositionRule
    success_url = reverse_lazy('rules')
