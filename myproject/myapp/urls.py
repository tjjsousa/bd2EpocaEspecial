from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index_view'),
    path('mongo/', views.mongo_view, name='mongo_view'),
    #URLS DO PROJETO
    path('clientes/', views.clientes_view, name='clientes_view'),
    path('clientes_insert/', views.clientes_insert_view, name='clientes_insert_view'),
    path('clientes_edit/<str:id>', views.clientes_insert_view, name='clientes_edit_view'),
    path('clientes_delete/<str:id>', views.clientes_delete_view, name='clientes_delete_view'),
    path('veiculos/', views.veiculos_view, name='veiculos_view'),
    path('veiculos_insert/', views.veiculos_insert_view, name='veiculos_insert_view'),
    path('veiculos_edit/<str:id>', views.veiculos_insert_view, name='veiculos_edit_view'),
    path('veiculos_delete/<str:id>', views.veiculos_delete_view, name='veiculos_delete_view'),
    path('registo_entradas/', views.registo_entradas_view, name='registo_entradas_view'),
    path('restauros/', views.restauros_view, name='restauros_view'),
    path('tarefas_restauro/', views.tarefas_restauro_view, name='tarefas_restauro_view'),
    path('faturacao/', views.faturacao_view, name='faturacao_view'),
    path('saidas_veiculos/', views.saidas_veiculos_view, name='saidas_veiculos_view'),
    path('tipos_mao_obra/', views.tipos_mao_obra_view, name='tipos_mao_obra_view'),
]
