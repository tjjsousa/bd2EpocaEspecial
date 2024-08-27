from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('mongo/', views.mongo_view, name='mongo_view'),
    #URLS DO PROJETO
    path('clientes/', views.clientes_view, name='clientes_view'),
    path('veiculos/', views.veiculos_view, name='veiculos_view'),
    path('registo_entradas/', views.registo_entradas_view, name='registo_entradas_view'),
    path('restauros/', views.restauros_view, name='restauros_view'),
    path('tarefas_restauro/', views.tarefas_restauro_view, name='tarefas_restauro_view'),
    path('faturacao/', views.faturacao_view, name='faturacao_view'),
    path('saidas_veiculos/', views.saidas_veiculos_view, name='saidas_veiculos_view'),
    path('tipos_mao_obra/', views.tipos_mao_obra_view, name='tipos_mao_obra_view'),
]
