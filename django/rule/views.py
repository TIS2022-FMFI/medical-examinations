from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

# from .models import Rule,RuleType

# Create your views here.

# class RuleTypeList(ListView):
#     model = RuleType
#     context_object_name = 'ruletype'
#     # template = 'templates\employee\employee_list'
# class RuleList(ListView):
#     model = Rule
#     context_object_name = 'rules'
#     # template = 'templates\employee\employee_list'


# class RuleDetail(DetailView):
#     model = Rule
#     context_object_name = 'rule'
#     # template = 'templates\employee\employee_detail'


# class RuleCreate(CreateView):
#     model = Rule
#     fields = '__all__'
#     success_url = reverse_lazy('rules')


# class RuleUpdate(UpdateView):
#     model = Rule
#     fields = '__all__'
#     success_url = reverse_lazy('rules')


# class RuleDelete(DeleteView):
#     model = Rule
#     context_object_name = 'rule'
#     success_url = reverse_lazy('rules')
