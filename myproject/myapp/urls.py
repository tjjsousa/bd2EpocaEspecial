from django.urls import path
from . import views


urlpatterns = [
    #URLS DO PROJETO
    path('', views.index_view, name='index_view'),

    #CLIENTES
    path('clientes/', views.clientes_view, name='clientes_view'),
    path('clientes_insert/', views.clientes_insert_view, name='clientes_insert_view'),
    path('clientes_edit/<str:id>', views.clientes_insert_view, name='clientes_edit_view'),
    path('clientes_delete/<str:id>', views.clientes_delete_view, name='clientes_delete_view'),
    #CLIENTES
    #VEICULOS
    path('veiculos/', views.veiculos_view, name='veiculos_view'),
    path('veiculos_insert/', views.veiculos_insert_view, name='veiculos_insert_view'),
    path('veiculos_edit/<str:id>', views.veiculos_insert_view, name='veiculos_edit_view'),
    path('veiculos_delete/<str:id>', views.veiculos_delete_view, name='veiculos_delete_view'),
    #VEICULOS
    #REGISTO ENTRADAS
    path('registo_entradas/', views.registo_entradas_view, name='registo_entradas_view'),
    path('registo_entradas_insert', views.registo_entrada_insert_view, name='registo_entrada_insert_view'),
    path('registo_entradas_edit/<str:id>', views.registo_entrada_edit_view, name='registo_entrada_edit_view'),
    path('registo_entradas_delete/<str:id>', views.registo_entrada_delete_view, name='registo_entrada_delete_view'),
    #REGISTO ENTRADAS
    #RESTAUROS
    path('restauros/', views.restauros_view, name='restauros_view'),
    path('restauros_insert/', views.restauro_insert_view, name='restauro_insert_view'),
    path('restauros_edit/<str:id>/', views.restauro_edit_view, name='restauro_edit_view'),
    path('restauros_delete/<str:id>/', views.restauro_delete_view, name='restauro_delete_view'),
    #RESTAUROS
    #TAREFAS RESTAURO
    path('tarefas_restauro/', views.tarefas_restauro_view, name='tarefas_restauro_view'),
    path('tarefas_restauro_insert/', views.tarefas_restauro_insert_view, name='tarefas_restauro_insert_view'),
    path('tarefas_restauro_edit/<str:id>/', views.tarefas_restauro_edit_view, name='tarefas_restauro_edit_view'),
    path('tarefas_restauro_delete/<str:id>/', views.tarefas_restauro_delete_view, name='tarefas_restauro_delete_view'),
    #TAREFAS RESTAURO
    #FATURACAO
    path('faturacao/', views.faturacao_view, name='faturacao_view'),
    #FATURACAO
    #SAIDAS VEICULOS
    path('saidas_veiculos/', views.saidas_veiculos_view, name='saidas_veiculos_view'),
    #SAIDAS VEICULOS
    #TIPOS MAO OBRA
    path('tipos_mao_obra/', views.tipos_mao_obra_view, name='tipos_mao_obra_view'),
    #TIPOS MAO OBRA
]
