from django.db import models


class ExaminationType(models.Model):
    name = models.CharField(max_length=300)         # varchar(300) NOT NULL
    periodicity = models.PositiveIntegerField()     # integer UNSIGNED NOT NULL

    def __str__(self):
        return self.name
