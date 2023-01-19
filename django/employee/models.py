from django.db import models
from rule.models import PositionRule, ShiftRule, HiddenRule
from django.urls import reverse


class Employee(models.Model):
    name = models.CharField(max_length=30)                              # varchar(30) NOT NULL
    surname = models.CharField(max_length=30)                           # varchar(30) NOT NULL
    employeeId = models.CharField(max_length=15)                        # varchar(15) NOT NULL
    personalNumber = models.CharField(max_length=15)                    # varchar(15) NOT NULL
    userComment = models.TextField(null=True, blank=True)               # text
    exceptionExpirationDate = models.DateField(null=True, blank=True)   # date

    positionRuleId = models.ForeignKey(PositionRule, on_delete=models.DO_NOTHING)   # FOREIGNKEY NOT NULL
    shiftRuleId = models.ForeignKey(ShiftRule, on_delete=models.DO_NOTHING)         # FOREIGNKEY NOT NULL
    hiddenRuleId = models.ForeignKey(HiddenRule, on_delete=models.DO_NOTHING, null=True, blank=True)   # FOREIGNKEY


    def __str__(self):
        return f'{self.name} {self.surname}'

    def get_absolute_url(self):
        return reverse('employeeUpdate', kwargs={'pk': self.pk})


