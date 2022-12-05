from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .models import ExaminationType


class ExaminationTypeList(ListView):
    model = ExaminationType
    context_object_name = 'examinatonTypes'


class ExaminationTypeDetail(DetailView):
    model = ExaminationType
    context_object_name = 'examinatonType'
    # template = 'templates\employee\employee_detail'


class ExaminationTypeCreate(CreateView):
    model = ExaminationType
    fields = '__all__'
    success_url = reverse_lazy('examinatontypes')


class ExaminationTypeUpdate(UpdateView):
    model = ExaminationType
    fields = '__all__'
    success_url = reverse_lazy('examinatontypes')
    context_object_name = 'examinatonType'


class ExaminationTypeDelete(DeleteView):
    model = ExaminationType
    context_object_name = 'examinatonType'
    success_url = reverse_lazy('examinationtypes')
