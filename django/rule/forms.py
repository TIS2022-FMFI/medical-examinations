from django.shortcuts import get_object_or_404
from django.db.models import Q
from django import forms
from django.db import connection

from .models import PositionRule, Department, ShiftRule
from rulesExamination.models import RulesExamination
from examinationType.models import ExaminationType

def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cursor.fetchall() 
    ]


class PositionRuleEditForm(forms.Form):
    name = forms.CharField(label="Nazov")
    department = forms.ChoiceField(label = "oddelenie", widget=forms.Select())
    examinatoins = forms.MultipleChoiceField(label="Prehliadky", widget = forms.CheckboxSelectMultiple())

    def __init__(self, positionRuleId, *args, **kwargs):
        super().__init__(*args, **kwargs)

        positionRule = get_object_or_404(PositionRule, id=positionRuleId)
        self.fields['name'].initial = positionRule.name

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    department.id, department.name, 
                    city.name AS cityName
                FROM rule_department AS department
                LEFT JOIN rule_city AS city ON department.cityId_id = city.id
                ORDER BY department.name
            """)
            departments = dictfetchall(cursor)    

        self.fields['department'].choices = [(i['id'], f"{i['name']} {i['cityName']}") for i in departments]
        self.fields['department'].initial = positionRule.departmentId.id

        self.fields['examinatoins'].required = False
        self.fields['examinatoins'].choices = [(i.id, f"{i.name}") for i in ExaminationType.objects.all()]
        self.fields['examinatoins'].initial = [i.examinationTypeId.id for i in RulesExamination.objects.filter(ruleId = positionRule.ruleId)]



class ShiftRuleEditForm(forms.Form):
    name = forms.CharField(label="Nazov")
    examinatoins = forms.MultipleChoiceField(label="Prehliadky", widget = forms.CheckboxSelectMultiple())

    def __init__(self, shiftRuleId, *args, **kwargs):
        super().__init__(*args, **kwargs)

        shiftnRule = get_object_or_404(ShiftRule, id=shiftRuleId)
        self.fields['name'].initial = shiftnRule.name

        self.fields['examinatoins'].required = False
        self.fields['examinatoins'].choices = [(i.id, f"{i.name}") for i in ExaminationType.objects.all()]
        self.fields['examinatoins'].initial = [i.examinationTypeId.id for i in RulesExamination.objects.filter(ruleId = shiftnRule.ruleId)]