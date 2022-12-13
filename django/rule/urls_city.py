from django.urls import path
from .views import CityList, CityDetail, CityCreate, CityUpdate, CityDelete

urlpatterns = [
    path('', CityList.as_view(), name='cities'),
    path('<int:pk>/', CityDetail.as_view(), name='city'),
    path('create/', CityCreate.as_view(), name='cityCreate'),
    path('update/<int:pk>/', CityUpdate.as_view(), name='cityUpdate'),
    path('delete/<int:pk>/', CityDelete.as_view(), name='cityDelete'),
]