from django.urls import path
from .views import PassedExaminationsList, PassedExaminationDelete

urlpatterns = [
    path('employee/<int:pk>/', PassedExaminationsList.as_view(), name='employeesPassedExaminations'),
    path('delete/<int:pk>/<int:employeeId>/', PassedExaminationDelete.as_view(), name='passedExaminationDelete'),
]