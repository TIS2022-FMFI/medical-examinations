from django.db import models
from rule.models import Rule
from employee.models import Employee


class EmployeesRule(models.Model):
    ruleId = models.ForeignKey(Rule, on_delete=models.DO_NOTHING)               # FOREIGNKEY NOT NULL
    employeeId = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)       # FOREIGNKEY NOT NULL
