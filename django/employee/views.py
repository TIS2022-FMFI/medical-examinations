from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection

from .models import Employee
from rule.models import Rule, HiddenRule, PositionRule, City, Department, ShiftRule
from rulesExamination.models import RulesExamination
from examinationType.models import ExaminationType
from passedExamination.models import PassedExaminations


from .forms import ChoiceForm, AbsolvedExaminationsChoiceForm, EditForm

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cursor.fetchall() 
    ]

class EmployeeList(LoginRequiredMixin, ListView):
    # model = Employee
    context_object_name = 'employee_list'
    template_name = 'employee\employee_list.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        
        context['Position_rules_list'] = [dict(name="--")]
        context['Position_rules_list'].extend(PositionRule.objects.all())
        context['Department_rules_list'] = [dict(name="--")]
        context['Department_rules_list'].extend(Department.objects.all())
        context['City_rules_list'] = [dict(name="--")]
        context['City_rules_list'].extend(City.objects.all())
        context['Shift_rules_list'] = [dict(name="--")]
        context['Shift_rules_list'].extend(ShiftRule.objects.all())
        return context

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT employee.id, employee.name, employee.surname, employee.employeeId,
                        position.name as positionName,
                        department.name as departmentName,
                        city.name as cityName,
                        shift.name as shiftName,
                        (
                        SELECT days_to_expiration
                        FROM
                            (
                            SELECT DISTINCT examinationType.id,
                                    (
                                        SELECT CAST(examinationType.periodicity AS SIGNED)*365 - DATEDIFF(now(),passedExamination.date)
                                        FROM passedExamination_passedexaminations passedExamination
                                        WHERE examinationType.id = passedExamination.examinationTypeId_id AND employee.id = passedExamination.employeeId_id
                                        ORDER BY passedExamination.date
                                        LIMIT 1
                                    ) days_to_expiration
                            FROM examinationType_examinationtype examinationType 
                            LEFT JOIN rulesExamination_rulesexamination rulesExamination ON rulesExamination.examinationTypeId_id = examinationType.id
                            LEFT JOIN rule_rule rule_p ON rule_p.id = rulesExamination.ruleId_id 
                            WHERE rule_p.id = position.ruleId_id OR rule_p.id = shift.ruleId_id OR rule_p.id = hidden.ruleId_id
                            LIMIT 1
                            ) t
                        ) days_to_expiration
                FROM employee_employee employee
                LEFT JOIN rule_positionrule position ON employee.positionRuleId_id = position.id
                LEFT JOIN rule_shiftrule shift ON employee.shiftRuleId_id = shift.id
                LEFT JOIN rule_hiddenrule hidden ON employee.hiddenRuleId_id = hidden.id
                LEFT JOIN rule_department as department on position.departmentId_id = department.id
                LEFT JOIN rule_city as city on department.cityId_id = city.id
                ORDER BY days_to_expiration;
            """)
            return dictfetchall(cursor)
        return []


class EmployeeCreate(LoginRequiredMixin, FormView):
    template_name = "employee/employee_form.html"
    form_class = EditForm     

    def get_success_url(self):
        return reverse_lazy('employees')

    def form_valid(self, form):  
        with transaction.atomic(): # start transaction
            employee = Employee.objects.create(
                name = form.cleaned_data['name'],
                surname = form.cleaned_data['surname'],
                employeeId = form.cleaned_data['employeeId'],
                personalNumber = form.cleaned_data['personalNumber'],
                userComment = form.cleaned_data['userComment'],
                exceptionExpirationDate = form.cleaned_data['exceptionExpirationDate'],
                positionRuleId = get_object_or_404(PositionRule, id = form.cleaned_data['positionRuleId']),
                shiftRuleId = get_object_or_404(ShiftRule, id = form.cleaned_data['shiftRuleId']),
                hiddenRuleId = None) 
            employee.save() # save to db
        return super().form_valid(form)



class EmployeeUpdate(LoginRequiredMixin, FormView):
    template_name = 'employee\employee_form_edit.html'
    form_class = EditForm 

    def get_success_url(self):
        # return reverse_lazy('employees')
        return reverse_lazy('employeeUpdate', kwargs={'pk': self.kwargs['pk']})
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['employeeId'] = self.kwargs['pk']
        return form_class(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    employee.id, 
                    positionRule.ruleId_id as positionRuleId, 
                    shiftRule.ruleId_id as shiftRuleId,
                    hiddenRule.ruleId_id as hiddenRuleId
                FROM employee_employee employee
                LEFT JOIN rule_positionrule positionRule ON employee.positionRuleId_id = positionRule.id
                LEFT JOIN rule_shiftrule shiftRule ON employee.shiftRuleId_id = shiftRule.id
                LEFT JOIN rule_hiddenrule hiddenRule ON employee.hiddenRuleId_id = hiddenRule.id
                WHERE employee.id = %s
            """, self.kwargs['pk'])
            employee = dictfetchall(cursor)[0]
            context['employee'] = employee
            
            context['positionRulesExaminations'] = []
            if(employee['positionRuleId'] != None):
                cursor.execute("""
                    SELECT
                        examination.name
                    FROM rulesExamination_rulesexamination rulesExam
                    LEFT JOIN examinationType_examinationtype examination ON rulesExam.examinationTypeId_id = examination.id
                    WHERE rulesExam.ruleId_id = %s
                """, employee['positionRuleId'])
                context['positionRulesExaminations'] = dictfetchall(cursor)

            context['shiftRulesExaminations'] = []
            if(employee['shiftRuleId'] != None):
                cursor.execute("""
                    SELECT
                        examination.name
                    FROM rulesExamination_rulesexamination rulesExam
                    LEFT JOIN examinationType_examinationtype examination ON rulesExam.examinationTypeId_id = examination.id
                    WHERE rulesExam.ruleId_id = %s
                """, employee['shiftRuleId'])
                context['shiftRulesExaminations'] = dictfetchall(cursor)

            context['individualRulesExaminations'] = []
            if(employee['hiddenRuleId'] != None):
                cursor.execute("""
                    SELECT
                        examination.name
                    FROM rulesExamination_rulesexamination rulesExam
                    LEFT JOIN examinationType_examinationtype examination ON rulesExam.examinationTypeId_id = examination.id
                    WHERE rulesExam.ruleId_id = %s
                """, employee['hiddenRuleId'])
                context['individualRulesExaminations'] = dictfetchall(cursor)       
        
        return context

    def form_valid(self, form):  
        with transaction.atomic(): # start transaction
            employee = get_object_or_404(Employee, id=self.kwargs['pk'])
            employee.name = form.cleaned_data['name']
            employee.surname = form.cleaned_data['surname']
            employee.employeeId = form.cleaned_data['employeeId']
            employee.personalNumber = form.cleaned_data['personalNumber']
            employee.userComment = form.cleaned_data['userComment']
            employee.exceptionExpirationDate = form.cleaned_data['exceptionExpirationDate']
            employee.positionRuleId = get_object_or_404(PositionRule, id = form.cleaned_data['positionRuleId'])
            employee.shiftRuleId = get_object_or_404(ShiftRule, id = form.cleaned_data['shiftRuleId'])
            employee.save() # save to db
        return super().form_valid(form)



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

        with transaction.atomic(): # start transaction
            setInDB = set()
            if employee.hiddenRuleId is not None:
                setInDB = set(str(i.examinationTypeId.id) for i in RulesExamination.objects.filter(ruleId = employee.hiddenRuleId.ruleId))

            if employee.hiddenRuleId is None: # create hidden rule if doesnt exists
                rule = Rule.objects.create() 
                hiddenRule = HiddenRule.objects.create(ruleId = rule)
                employee.hiddenRuleId = hiddenRule
                employee.save() # save changes
                
            # to set
            IdsToSet = setInForm - setInDB
            for examination in ExaminationType.objects.filter(id__in = IdsToSet):
                RulesExamination.objects.create(ruleId=employee.hiddenRuleId.ruleId, examinationTypeId = examination)
                
            # to delete
            IdsToDelete = setInDB - setInForm
            for ruleExamination in RulesExamination.objects.filter(ruleId=employee.hiddenRuleId.ruleId).filter(examinationTypeId__in=IdsToDelete):
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
                PassedExaminations.objects.create(employeeId=employee, examinationTypeId=examination, date=dateSetInForm)
        
        return super().form_valid(form)
