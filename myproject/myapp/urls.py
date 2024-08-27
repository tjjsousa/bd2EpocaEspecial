from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_view, name='my_view'),
    path('mongo/', views.mongo_view, name='mongo_view'),
]