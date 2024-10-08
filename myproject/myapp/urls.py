from django.urls import path
from . import views


urlpatterns = [
    #URLS DO PROJETO
    path('', views.index_view, name='index_view'),

    #CLIENTES
    path('clientes/', views.clientes_view, name='clientes_view'),
    #path('clientes_insert/', views.clientes_insert_view, name='clientes_insert_view'),
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
    path('faturacao_view/', views.faturacao_view, name='faturacao_view'),
    #path('faturacao_insert/', views.faturacao_insert_view, name='faturacao_insert_view'),
    path('faturacao_edit/<str:id>/', views.faturacao_edit_view, name='faturacao_edit_view'),
    path('faturacao_delete/<str:id>/', views.faturacao_delete_view, name='faturacao_delete_view'),
    path('faturacao_pago/<int:fatura_id>/', views.alterar_estado_para_pago_view, name='alterar_estado_para_pago_view'),
    #FATURACAO

    #SAIDAS VEICULOS
    path('saidas_veiculos/', views.registo_saidas_view, name='registo_saidas_view'),
    path('saidas_veiculos_insert/', views.registo_saidas_insert_view, name='registo_saidas_insert_view'),
    path('saidas_veiculos_edit/<str:id>/', views.registo_saidas_edit_view, name='registo_saidas_edit_view'),
    path('saidas_veiculos_delete/<str:id>/', views.registo_saidas_delete_view, name='registo_saidas_delete_view'),
    #SAIDAS VEICULOS
    #TIPOS MAO OBRA
    path('registo_tipos_mao_obra/', views.registo_tipos_mao_obra_view, name='registo_tipos_mao_obra_view'),
    path('registo_tipos_mao_obra_insert', views.registo_tipos_mao_obra_insert_view, name='registo_tipos_mao_obra_insert_view'),
    path('registo_tipos_mao_obra_edit/<str:id>', views.registo_tipos_mao_obra_edit_view, name='registo_tipos_mao_obra_edit_view'),
    path('registo_tipos_mao_obra_delete/<str:id>', views.registo_tipos_mao_obra_delete_view, name='registo_tipos_mao_obra_delete_view'),
    #TIPOS MAO OBRA

    path('exportar_tarefas_json/', views.exportar_tarefas_json, name='exportar_tarefas_json'),
    path('exportar_tarefas_xml/', views.exportar_tarefas_xml, name='exportar_tarefas_xml'),

    path('import/', views.import_tarefas_restauro_xml_json, name='import_tarefas_restauro_xml_json'),

]
