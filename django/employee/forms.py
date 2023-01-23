from django.shortcuts import get_object_or_404
from django.db.models import Q
from django import forms

from .models import Employee
from rule.models import Rule, HiddenRule
from rulesExamination.models import RulesExamination
from examinationType.models import ExaminationType
from passedExamination.models import PassedExaminations


class ChoiceForm(forms.Form):
    choicesField = forms.MultipleChoiceField(
            widget  = forms.CheckboxSelectMultiple()
        )

    def __init__(self, employeeId, *args, **kwargs):
        super().__init__(*args, **kwargs)
        employee = get_object_or_404(Employee, id=employeeId)
        initials = []
        if(employee.hiddenRuleId is not None):
            initials = [i.examinationTypeId.id for i in RulesExamination.objects.filter(ruleId = employee.hiddenRuleId.ruleId)]

        self.fields['choicesField'].choices = [(i.id, f"{i.name}") for i in ExaminationType.objects.all()]
        self.fields['choicesField'].initial = initials


class DateInput(forms.DateInput):
    input_type = 'date'

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