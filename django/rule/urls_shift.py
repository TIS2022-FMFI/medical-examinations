from django.urls import path
from .views import ShiftRuleList, ShiftRuleDetail, ShiftRuleCreate, ShiftRuleUpdate, ShiftRuleDelete

urlpatterns = [
    path('', ShiftRuleList.as_view(), name='shifts'),
    path('<int:pk>/', ShiftRuleDetail.as_view(), name='shift'),
    path('create/', ShiftRuleCreate.as_view(), name='shiftCreate'),
    path('update/<int:pk>/', ShiftRuleUpdate.as_view(), name='shiftUpdate'),
    path('delete/<int:pk>/', ShiftRuleDelete.as_view(), name='shiftDelete'),
]