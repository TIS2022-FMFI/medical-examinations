from django.shortcuts import get_object_or_404
from django.db.models import Q
from django import forms
from django.db import connection

from .models import Employee
from rulesExamination.models import RulesExamination
from examinationType.models import ExaminationType
from rule.models import ShiftRule




def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row)) 
        for row in cursor.fetchall() 
    ]

class DateInput(forms.DateInput):
    input_type = 'date'


class EditForm(forms.Form):
    name = forms.CharField(label="Meno", max_length=30)
    surname = forms.CharField(label="Priezvisko", max_length=30)
    employeeId = forms.CharField(label="Identifikačné číslo zamestnanca", max_length=15)
    personalNumber = forms.CharField(label="Osobné číslo", max_length=15)
    userComment = forms.CharField(label="Poznámka uživatela", widget=forms.Textarea, required=False)
    exceptionExpirationDate = forms.DateField(label = "Dátum vypršania obmedzenia", widget=DateInput, required=False)
    positionRuleId = forms.ChoiceField(label = "Pozíca/Oddelenie/Mesto", widget=forms.Select())
    shiftRuleId = forms.ChoiceField(label = "Zmennosť", widget=forms.Select())

    def __init__(self, employeeId = None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    position.id, position.name, 
                    department.name AS departmentName,
                    city.name AS cityName
                FROM rule_positionrule AS position
                LEFT JOIN rule_department AS department ON position.departmentId_id = department.id
                LEFT JOIN rule_city AS city ON department.cityId_id = city.id
                ORDER BY department.name
            """)
            positions = dictfetchall(cursor)   

        self.fields['positionRuleId'].choices = [(i['id'], f"{i['name']}/{i['departmentName']}/{i['cityName']}") for i in positions]
        self.fields['positionRuleId'].choices.append((None, "---"))
        self.fields['positionRuleId'].inital = None
        self.fields['shiftRuleId'].choices = [(i.id, f"{i.name}") for i in ShiftRule.objects.all()]
        self.fields['shiftRuleId'].choices.append((None, "---"))
        self.fields['shiftRuleId'].inital = None
        
        if(employeeId != None):
            employee = get_object_or_404(Employee, id=employeeId)
            self.fields['name'].initial = employee.name
            self.fields['surname'].initial = employee.surname
            self.fields['employeeId'].initial = employee.employeeId
            self.fields['personalNumber'].initial = employee.personalNumber
            self.fields['userComment'].initial = employee.userComment
            self.fields['exceptionExpirationDate'].initial = employee.exceptionExpirationDate
            if(employee.positionRuleId != None): self.fields['positionRuleId'].initial = employee.positionRuleId.id
            if(employee.shiftRuleId != None): self.fields['shiftRuleId'].initial = employee.shiftRuleId.id


class ChoiceForm(forms.Form):
    choicesField = forms.MultipleChoiceField(
            required=False, 
            widget=forms.CheckboxSelectMultiple()
        )

    def __init__(self, employeeId, *args, **kwargs):
        super().__init__(*args, **kwargs)
        employee = get_object_or_404(Employee, id=employeeId)

        initials = []
        if(employee.hiddenRuleId is not None):
            initials = [i.examinationTypeId.id for i in RulesExamination.objects.filter(ruleId = employee.hiddenRuleId.ruleId)]

        self.fields['choicesField'].choices = [(i.id, f"{i.name}") for i in ExaminationType.objects.all()]
        self.fields['choicesField'].initial = initials



class AbsolvedExaminationsChoiceForm(forms.Form):
    choicesField = forms.MultipleChoiceField(
            widget  = forms.CheckboxSelectMultiple()
        )
    date = forms.DateField(widget=DateInput)

    def __init__(self, employeeId, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choicesField'].required = False

        employee = get_object_or_404(Employee, id=employeeId)

        choices = set((i.examinationTypeId.id, f"{i.examinationTypeId.name}") 
                        for i in RulesExamination.objects.filter(
                            Q(ruleId = employee.hiddenRuleId.ruleId) |
                            Q(ruleId = employee.shiftRuleId.ruleId) |
                            Q(ruleId = employee.hiddenRuleId.ruleId)
                            ))
        self.fields['choicesField'].choices = choices