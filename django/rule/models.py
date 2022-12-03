from django.db import models


class RuleType(models.Model):
    name = models.CharField(max_length=150)                                 # varchar(150) NOT NULL


class Locality(models.Model):
    name = models.CharField(max_length=150)                                 # varchar(150) NOT NULL


class Rule(models.Model):
    ruleTypeId = models.ForeignKey(RuleType, on_delete=models.DO_NOTHING)   # FOREIGNKEY NOT NULL
    localityId = models.ForeignKey(Locality, on_delete=models.DO_NOTHING)   # FOREIGNKEY NOT NULL
    name = models.CharField(max_length=150)                                 # varchar(150) NOT NULL
