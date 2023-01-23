# from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import connection
from django.shortcuts import get_object_or_404

from .models import Employee
from rule.models import Rule, HiddenRule
from rulesExamination.models import RulesExamination
from examinationType.models import ExaminationType
from passedExamination.models import PassedExaminations

from .forms import ChoiceForm, AbsolvedExaminationsChoiceForm

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cursor.fetchall() 
    ]


# Create your views here.

class EmployeeList(LoginRequiredMixin, ListView):
    # model = Employee
    context_object_name = 'employee_list'
    template_name = 'employee\employee_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super(EmployeeList, self).get_context_data(**kwargs)
    #     # print(context)
    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT * FROM employee_employee")
    #         print(cursor.fetchall())
    #         # context['employees'] = cursor.fetchall()
    #     # print(context)
    #     return context
    
    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    employee.id, employee.name, employee.surname, employee.employeeId,
                    position.name as positionName,
                    department.name as departmentName,
                    city.name as cityName,
                    shift.name as shiftName
                FROM employee_employee as employee
                LEFT JOIN rule_positionrule as position on employee.positionRuleId_id = position.ruleId_id
                LEFT JOIN rule_department as department on position.departmentId_id = department.id
                LEFT JOIN rule_city as city on department.cityId_id = city.id
                LEFT JOIN rule_shiftrule as shift on employee.shiftRuleId_id = shift.ruleId_id
                ORDER BY employee.id
            """)
            return dictfetchall(cursor)
        return []




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


class EmployeesAbsolvedExaminationsMenu(LoginRequiredMixin, FormView):
    template_name = "employee/employee_abdolvedExaminations_edit.html"
    form_class = AbsolvedExaminationsChoiceForm 

    def get_success_url(self):
        return reverse_lazy('employeeUpdate', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = Employee.objects.get(id=self.kwargs['pk'])
        return context

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['employeeId'] = self.kwargs['pk']
        return form_class(**kwargs)

    def form_valid(self, form):
        employee = get_object_or_404(Employee, id=self.kwargs['pk'])
        examinationsSetInForm = set(form.cleaned_data['choicesField'])
        dateSetInForm = form.cleaned_data['date']

        with transaction.atomic(): # start transaction   
            examinations = ExaminationType.objects.filter(id__in = examinationsSetInForm)
            for examination in examinations:
                print(examination, examination.id)
                PassedExaminations.objects.create(employeeId=employee, examinationTypeId=examination, date=dateSetInForm)
        
        return super().form_valid(form)
