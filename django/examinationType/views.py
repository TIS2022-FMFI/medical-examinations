from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ExaminationType
from django.db import connection

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

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
    success_url = reverse_lazy('examinationtypes')


class ExaminationTypeUpdate(LoginRequiredMixin, UpdateView):
    model = ExaminationType
    fields = '__all__'
    success_url = reverse_lazy('examinationtypes')
    context_object_name = 'examinatonType'


class ExaminationTypeDelete(LoginRequiredMixin, DeleteView):
    model = ExaminationType
    context_object_name = 'examinatonType'
    success_url = reverse_lazy('examinationtypes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT  pe.date datum,
                                e.name menoZamestnanca,
                                e.surname priezviskoZamestnanca
                        FROM passedExamination_passedexaminations pe
                        LEFT JOIN employee_employee e ON e.id=pe.employeeId_id
                        WHERE pe.examinationTypeId_id=%s''', {self.kwargs['pk']})
            context['zavislostiPassedExamination'] = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT p.name nazovPozicie
                        FROM rule_positionrule p
                        LEFT JOIN rule_rule r ON p.ruleId_id=r.id
                        LEFT JOIN rulesExamination_rulesexamination re ON r.id=re.ruleId_id
                        WHERE re.examinationTypeId_id=%s''', {self.kwargs['pk']})
            context['zavislostiPosition'] = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT s.name nazovZmennosti
                        FROM rule_shiftrule s
                        LEFT JOIN rule_rule r ON s.ruleId_id=r.id
                        LEFT JOIN rulesExamination_rulesexamination re ON r.id=re.ruleId_id
                        WHERE re.examinationTypeId_id=%s''', {self.kwargs['pk']})
            context['zavislostiShift'] = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute('''
                        SELECT e.name, e.surname
                        FROM rule_hiddenrule h
                        LEFT JOIN rule_rule r ON h.ruleId_id=r.id
                        LEFT JOIN rulesExamination_rulesexamination re ON r.id=re.ruleId_id
                        LEFT JOIN employee_employee e ON e.hiddenRuleId_id=h.id
                        WHERE re.examinationTypeId_id=%s''', {self.kwargs['pk']})
            context['zavislostiHidden'] = dictfetchall(cursor)
        return context