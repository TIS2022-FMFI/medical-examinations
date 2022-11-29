from django.db import models
from rule.models import Rule
from examinationType.models import ExaminationType


class RulesExamination(models.Model):
    ruleId = models.ForeignKey(Rule, on_delete=models.DO_NOTHING)                           # FOREIGNKEY NOT NULL
    examinationTypeId = models.ForeignKey(ExaminationType, on_delete=models.DO_NOTHING)     # FOREIGNKEY NOT NULL

