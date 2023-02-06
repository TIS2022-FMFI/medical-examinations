from django.urls import path
from .views import EmployeeList, EmployeeCreate, EmployeeUpdate, EmployeeHiddenRuleEdit, EmployeeDelete, EmployeesAbsolvedExaminationsMenu

urlpatterns = [
    path('', EmployeeList.as_view(), name='employees'),
    path('create/', EmployeeCreate.as_view(), name='employeeCreate'),
    path('<int:pk>/', EmployeeUpdate.as_view(), name='employeeUpdate'),
    path('custom-eaxminations/<int:pk>/', EmployeeHiddenRuleEdit.as_view(), name='employeeExaminationsUpdate'),
    path('delete/<int:pk>/', EmployeeDelete.as_view(), name='employeeDelete'),
    path('absolved-examinations/<int:pk>/', EmployeesAbsolvedExaminationsMenu.as_view(), name='employeeAbsolvedEdit'),
]