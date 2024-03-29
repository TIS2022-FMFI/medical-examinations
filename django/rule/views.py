from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import connection

from .models import City, Department, PositionRule, ShiftRule, Rule
from .forms import PositionRuleEditForm, ShiftRuleEditForm
from rulesExamination.models import RulesExamination
from examinationType.models import ExaminationType



def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# ############################          ShiftRule      ###########################
class ShiftRuleList(LoginRequiredMixin, ListView):
    model = ShiftRule
    ordering = ['name']


class ShiftRuleDetail(LoginRequiredMixin, DetailView):
    model = ShiftRule


class ShiftRuleCreate(LoginRequiredMixin, FormView):
    template_name = "rule/shiftrule_form.html"
    form_class = ShiftRuleEditForm     

    def get_success_url(self):
        return reverse_lazy('shifts')

    def form_valid(self, form):
        examinationsSetInForm = set(form.cleaned_data['examinatoins'])

        with transaction.atomic(): # start transaction
            rule = Rule.objects.create()
            shiftRule = ShiftRule.objects.create(
                name = form.cleaned_data['name'],
                ruleId = rule
            )
            for examination in ExaminationType.objects.filter(id__in = examinationsSetInForm):
                RulesExamination.objects.create(ruleId=shiftRule.ruleId, examinationTypeId = examination)
    
        return super().form_valid(form)


class ShiftRuleUpdate(LoginRequiredMixin, FormView):
    template_name = "rule/shiftrule_form.html"
    form_class = ShiftRuleEditForm     

    def get_success_url(self):
        return reverse_lazy('shifts')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['shiftRuleId'] = self.kwargs['pk']
        return form_class(**kwargs)

    def form_valid(self, form):
        shiftRule = get_object_or_404(ShiftRule, id=self.kwargs['pk'])

        nameSetInForm = form.cleaned_data['name']
        examinationsSetInForm = set(form.cleaned_data['examinatoins'])

        examinationsSetInDB = set(str(i.examinationTypeId.id) for i in RulesExamination.objects.filter(ruleId = shiftRule.ruleId))

        with transaction.atomic(): # start transaction
            shiftRule.name = nameSetInForm
            shiftRule.save() # save changes
        
            # to set
            IdsToSet = examinationsSetInForm - examinationsSetInDB
            for examination in ExaminationType.objects.filter(id__in = IdsToSet):
                RulesExamination.objects.create(ruleId=shiftRule.ruleId, examinationTypeId = examination)
                
            # to delete
            IdsToDelete = examinationsSetInDB - examinationsSetInForm
            for ruleExamination in RulesExamination.objects.filter(ruleId=shiftRule.ruleId).filter(examinationTypeId__in=IdsToDelete):
                ruleExamination.delete()
    
        return super().form_valid(form)


class ShiftRuleDelete(LoginRequiredMixin, DeleteView):
    model = ShiftRule
    success_url = reverse_lazy('shifts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT *
                        FROM employee_employee e
                        WHERE e.shiftRuleId_id=%s''', {self.kwargs['pk']})
            context['zavislosti'] = dictfetchall(cursor)
        return context

    


# ############################          Department      ###########################
class DepartmentList(LoginRequiredMixin, ListView):
    # model = Department
    template_name = "rule\department_list.html"
    context_object_name = 'departments_list'

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    department.id, department.name,
                    city.id cityId, city.name cityName
                FROM rule_department department
                LEFT JOIN rule_city city ON department.cityId_id = city.id
                ORDER BY department.name, city.name
            """)
            return dictfetchall(cursor)
        return []


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT *
                        FROM rule_positionrule p
                        WHERE p.departmentId_id=%s''', {self.kwargs['pk']})
            context['zavislosti'] = dictfetchall(cursor)
        return context


# ############################          City            ###########################
class CityList(LoginRequiredMixin, ListView):
    model = City
    ordering = ['name']


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT *
                        FROM rule_department d
                        WHERE d.cityId_id=%s''', {self.kwargs['pk']})
            context['zavislosti'] = dictfetchall(cursor)
        return context


# ############################      PositionRule        ###########################
class PositionRuleList(LoginRequiredMixin, ListView):
    #model = PositionRule
    template_name = 'rule/positionrule_list.html'

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT 	p.id position_id, p.name position_name,
		                d.id department_id, d.name department_name,
                        c.id city_id, c.name city_name
                FROM rule_positionrule p
                LEFT JOIN rule_department d ON p.departmentId_id = d.id  
                LEFT JOIN rule_city c ON d.cityId_id = c.id
                ORDER BY p.name, d.name, c.name
                ''')
            return dictfetchall(cursor)



class PositionRuleDetail(LoginRequiredMixin, DetailView):
    model = PositionRule


class PositionRuleCreate(LoginRequiredMixin, FormView):
    template_name = "rule/positionrule_form.html"
    form_class = PositionRuleEditForm     

    def get_success_url(self):
        return reverse_lazy('positionRules')

    def form_valid(self, form):

        examinationsSetInForm = set(form.cleaned_data['examinatoins'])

        with transaction.atomic(): # start transaction
            rule = Rule.objects.create()
            positionRule = PositionRule.objects.create(
                name = form.cleaned_data['name'],
                departmentId = get_object_or_404(Department, id = form.cleaned_data['department']),
                ruleId = rule
            )
            # to set
            for examination in ExaminationType.objects.filter(id__in = examinationsSetInForm):
                RulesExamination.objects.create(ruleId=positionRule.ruleId, examinationTypeId = examination)
                
        return super().form_valid(form)


class PositionRuleUpdate(LoginRequiredMixin, FormView):
    template_name = "rule/positionrule_form.html"
    form_class = PositionRuleEditForm     

    def get_success_url(self):
        return reverse_lazy('positionRules')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['positionRuleId'] = self.kwargs['pk']
        return form_class(**kwargs)

    def form_valid(self, form):
        positionRule = get_object_or_404(PositionRule, id=self.kwargs['pk'])

        nameSetInForm = form.cleaned_data['name']
        departmentIdSetInForm = form.cleaned_data['department']
        examinationsSetInForm = set(form.cleaned_data['examinatoins'])

        with transaction.atomic(): # start transaction
            examinationsSetInDB = set(str(i.examinationTypeId.id) for i in RulesExamination.objects.filter(ruleId = positionRule.ruleId))
            departmentSetInForm = get_object_or_404(Department, id = departmentIdSetInForm)

            positionRule.name = nameSetInForm
            positionRule.departmentId = departmentSetInForm
            positionRule.save() # save changes
        
            # to set
            IdsToSet = examinationsSetInForm - examinationsSetInDB
            for examination in ExaminationType.objects.filter(id__in = IdsToSet):
                RulesExamination.objects.create(ruleId=positionRule.ruleId, examinationTypeId = examination)
                
            # to delete
            IdsToDelete = examinationsSetInDB - examinationsSetInForm
            for ruleExamination in RulesExamination.objects.filter(ruleId=positionRule.ruleId).filter(examinationTypeId__in=IdsToDelete):
                ruleExamination.delete()
    
        return super().form_valid(form)


class PositionRuleDelete(LoginRequiredMixin, DeleteView):
    model = PositionRule
    success_url = reverse_lazy('rules')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT *
                        FROM employee_employee e
                        WHERE e.positionRuleId_id=%s''', {self.kwargs['pk']})
            context['zavislosti'] = dictfetchall(cursor)
        return context
