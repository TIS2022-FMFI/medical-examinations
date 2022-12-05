from django.urls import path
from .views import ExaminationTypeList, ExaminationTypeDetail, ExaminationTypeCreate, ExaminationTypeUpdate, ExaminationTypeDelete

urlpatterns = [
    path('', ExaminationTypeList.as_view(), name='examinationtypes'),
    path('<int:pk>/', ExaminationTypeDetail.as_view(), name='examinationtype'),
    path('create/', ExaminationTypeCreate.as_view(), name='examinationTypeCreate'),
    path('update/<int:pk>/', ExaminationTypeUpdate.as_view(), name='examinationTypeUpdate'),
    path('delete/<int:pk>/', ExaminationTypeDelete.as_view(), name='examinationTypeDelete'),
]