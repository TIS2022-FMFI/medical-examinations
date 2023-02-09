from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.db import connection
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from .models import PassedExaminations
from employee.models import Employee


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cursor.fetchall() 
    ]


# Create your views here.
class PassedExaminationsList(LoginRequiredMixin, ListView):
    context_object_name = 'context'
    template_name = 'passedExamination\passedExamination_list.html'

    def get_queryset(self):
        context = dict()
        
        context['employee'] = get_object_or_404(Employee, id=self.kwargs['pk'])
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    passed.id, passed.date,
                    examination.name as examinationName
                FROM employee_employee AS employee
                LEFT JOIN passedExamination_passedexaminations AS passed ON employee.id = passed.employeeId_id
                LEFT JOIN examinationType_examinationtype AS examination ON passed.examinationTypeId_id = examination.id
                WHERE employee.id = %s
                ORDER BY passed.date DESC
            """, [self.kwargs['pk']])
            context['passed_list'] = dictfetchall(cursor)
            if(context['passed_list'][0]['id'] == None): context['passed_list'] = []
        return context

class PassedExaminationDelete(LoginRequiredMixin, DeleteView):
    model = PassedExaminations
    context_object_name = 'passedExamination'
    template_name = "passedExamination/passedExamination_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('employeesPassedExaminations', kwargs={'pk': self.kwargs['employeeId']})

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['employee'] = get_object_or_404(Employee, id=self.kwargs['employeeId'])
        return context