from django.urls import path
from .views import DepartmentList, DepartmentDetail, DepartmentCreate, DepartmentUpdate, DepartmentDelete

urlpatterns = [
    path('', DepartmentList.as_view(), name='departments'),
    path('<int:pk>/', DepartmentDetail.as_view(), name='department'),
    path('create/', DepartmentCreate.as_view(), name='departmentCreate'),
    path('update/<int:pk>/', DepartmentUpdate.as_view(), name='departmentUpdate'),
    path('delete/<int:pk>/', DepartmentDelete.as_view(), name='departmentDelete'),
]