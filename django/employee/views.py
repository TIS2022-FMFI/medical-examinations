# from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django import forms
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Employee
from rule.models import Rule, HiddenRule
from rulesExamination.models import RulesExamination
from examinationType.models import ExaminationType

# Create your views here.

class EmployeeList(LoginRequiredMixin, ListView):
    model = Employee
    context_object_name = 'employees'
    # template = 'templates\employee\employee_list'



class EmployeeCreate(LoginRequiredMixin, CreateView):
    model = Employee
    fields = ("name", "surname", "employeeId", "personalNumber", "userComment", "exceptionExpirationDate", "positionRuleId", "shiftRuleId")
    success_url = reverse_lazy('employees')



class EmployeeUpdate(LoginRequiredMixin, UpdateView):
    model = Employee
    fields = ("name", "surname", "employeeId", "personalNumber", "userComment", "exceptionExpirationDate", "positionRuleId", "shiftRuleId")
    # success_url = reverse_lazy('employees')
    context_object_name = 'employee'
    template_name = 'employee\employee_form_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employee = context['employee']
        
        employeesPositionRulesExaminations = RulesExamination.objects.filter(ruleId = employee.positionRuleId.ruleId)
        context['positionRulesExaminations'] = employeesPositionRulesExaminations
         
        employeesShiftRulesExaminations = RulesExamination.objects.filter(ruleId = employee.shiftRuleId.ruleId)
        context['shiftRulesExaminations'] = employeesShiftRulesExaminations

        if(employee.hiddenRuleId is not None):
            employeesIndividualRulesExaminations = RulesExamination.objects.filter(ruleId = employee.hiddenRuleId.ruleId)
        else: 
            employeesIndividualRulesExaminations = []
        context['individualRulesExaminations'] = employeesIndividualRulesExaminations  
 
        return context



class EmployeeDelete(LoginRequiredMixin, DeleteView):
    model = Employee
    context_object_name = 'employee'
    success_url = reverse_lazy('employees')



class ChoiceForm(forms.Form):
    choicesField = forms.MultipleChoiceField(
            widget  = forms.CheckboxSelectMultiple()
        )

    def __init__(self, employeeId, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choicesField'].required = False

        employee = get_object_or_404(Employee, id=employeeId)
        initials = []
        if(employee.hiddenRuleId is not None):
            initials = [i.examinationTypeId.id for i in RulesExamination.objects.filter(ruleId = employee.hiddenRuleId.ruleId)]

        self.fields['choicesField'].choices = [(i.id, f"{i.name}") for i in ExaminationType.objects.all()]
        self.fields['choicesField'].initial = initials

    
class EmployeeHiddenRuleEdit(LoginRequiredMixin, FormView):
    template_name = "employee/employee_hidenRule_edit.html"
    form_class = ChoiceForm        

    def get_success_url(self):
        return reverse_lazy('employeeUpdate', kwargs={'pk': self.kwargs['pk']})

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['employeeId'] = self.kwargs['pk']
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        employee = get_object_or_404(Employee, id=self.kwargs['pk'])
        setInForm = set(form.cleaned_data['choicesField'])

        setInDB = set()
        if(employee.hiddenRuleId is not None): 
            setInDB = set(str(i.examinationTypeId.id) for i in RulesExamination.objects.filter(ruleId = employee.hiddenRuleId.ruleId))
        

        with transaction.atomic(): # start transaction
            if(employee.hiddenRuleId is None): # create hidden rule if doesnt exists
                rule = Rule.objects.create() 
                hiddenRule = HiddenRule.objects.create(ruleId = rule)
                employee.hiddenRuleId = hiddenRule
                employee.save() # save changes
                
            # to set
            IdsToSet = setInForm - setInDB
            for examinationId in IdsToSet:
                examination = get_object_or_404(ExaminationType, id=examinationId)
                RulesExamination.objects.create(ruleId=employee.hiddenRuleId.ruleId, examinationTypeId = examination)
                
            # to delete
            allValidRulesExaminations = RulesExamination.objects.filter(ruleId=employee.hiddenRuleId.ruleId)
            IdsToDelete = setInDB - setInForm
            for ruleExamination in allValidRulesExaminations:
                if(str(ruleExamination.examinationTypeId.id) in IdsToDelete):
                    ruleExamination.delete()
        

        return super().form_valid(form)

        
        

        


        

        

