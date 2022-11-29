from django.urls import path
from .views import EmployeeList, EmployeeDetail, EmployeeCreate, EmployeeUpdate, EmployeeDelete

urlpatterns = [
    path('', EmployeeList.as_view(), name='employees'),
    path('<int:pk>/', EmployeeDetail.as_view(), name='employee'),
    path('create/', EmployeeCreate.as_view(), name='employeeCreate'),
    path('update/<int:pk>/', EmployeeUpdate.as_view(), name='employeeUpdate'),
    path('delete/<int:pk>/', EmployeeDelete.as_view(), name='employeeDelete'),
]