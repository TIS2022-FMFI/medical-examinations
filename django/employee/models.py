from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=30)                              # varchar(30) NOT NULL
    surname = models.CharField(max_length=30)                           # varchar(30) NOT NULL
    personalNumber = models.CharField(max_length=15)                    # varchar(15) NOT NULL
    userComment = models.TextField(null=True, blank=True)               # text
    exceptionExpirationDate = models.DateField(null=True, blank=True)   # date

    def __str__(self):
        return f'{self.name} {self.surname}'


