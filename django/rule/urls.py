from django.urls import path
from .views import PositionRuleList, PositionRuleDetail, PositionRuleCreate, PositionRuleUpdate, PositionRuleDelete

urlpatterns = [
    path('', PositionRuleList.as_view(), name='positionRules'),
    path('<int:pk>/', PositionRuleDetail.as_view(), name='positionRule'),
    path('create/', PositionRuleCreate.as_view(), name='positionRuleCreate'),
    path('update/<int:pk>/', PositionRuleUpdate.as_view(), name='positionRuleUpdate'),
    path('delete/<int:pk>/', PositionRuleDelete.as_view(), name='positionRuleDelete'),
]