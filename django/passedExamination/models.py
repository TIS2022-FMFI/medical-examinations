from django.db import models
from employee.models import Employee
from examinationType.models import ExaminationType


class PassedExaminations(models.Model):
    employeeId = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)                   # FOREIGNKEY NOT NULL
    examinationTypeId = models.ForeignKey(ExaminationType, on_delete=models.DO_NOTHING)     # FOREIGNKEY NOT NULL
    date = models.DateField()                                                               # date NOT NULL


    def __str__(self):
        return f'{self.employeeId} - {self.examinationTypeId} - {self.date}'

