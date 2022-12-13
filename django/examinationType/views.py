from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import ExaminationType


class ExaminationTypeList(LoginRequiredMixin, ListView):
    model = ExaminationType
    context_object_name = 'examinatonTypes'


class ExaminationTypeDetail(LoginRequiredMixin, DetailView):
    model = ExaminationType
    context_object_name = 'examinatonType'
    # template = 'templates\employee\employee_detail'


class ExaminationTypeCreate(LoginRequiredMixin, CreateView):
    model = ExaminationType
    fields = '__all__'
    success_url = reverse_lazy('examinatontypes')


class ExaminationTypeUpdate(LoginRequiredMixin, UpdateView):
    model = ExaminationType
    fields = '__all__'
    success_url = reverse_lazy('examinatontypes')
    context_object_name = 'examinatonType'


class ExaminationTypeDelete(LoginRequiredMixin, DeleteView):
    model = ExaminationType
    context_object_name = 'examinatonType'
    success_url = reverse_lazy('examinationtypes')
