from django.db import models

class City(models.Model):
    name = models.CharField(max_length=50)                                 # varchar(150) NOT NULL

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50)                                 # varchar(150) NOT NULL
    cityId = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.cityId} {self.name}"

class Rule(models.Model): # abstration
    ...

class PositionRule(models.Model):
    name = models.CharField(max_length=100)
    departmentId = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    ruleId = models.ForeignKey(Rule, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.departmentId} {self.name}"

class ShiftRule(models.Model):
    name = models.CharField(max_length=150)
    ruleId = models.ForeignKey(Rule, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"

class HiddenRule(models.Model):
    ruleId = models.ForeignKey(Rule, on_delete=models.DO_NOTHING)

