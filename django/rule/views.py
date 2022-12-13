from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .models import PositionRule

# Create your views here.


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
