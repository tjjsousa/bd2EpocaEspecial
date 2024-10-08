from django.shortcuts import render , redirect
from datetime import date
from .forms import VeiculoForm, ClienteForm , RegistoEntradaForm , RestauroForm , TarefaRestauroForm, FaturacaoForm, TipoMaoObraForm, RegistoSaidasForm
from .models import Cliente, Veiculo, RegistoEntrada, Restauro, TarefaRestauro, Faturacao, SaidaVeiculo, TipoMaoObra
from .database import get_tarefa_restauro_id_id, apagar_cliente,alterar_estado_para_pago, inserir_faturacao, editar_faturacao , remove_faturacao ,get_faturacao_id , get_all_tipos_mao_obra , get_all_tarefas_restauro, get_tarefa_restauro_id , remove_tarefa_restauro , editar_tarefa_restauro, inserir_tarefas_restauro , inserir_cliente , inserir_veiculo, editar_cliente, editar_veiculo, get_cliente_id, apagar_cliente_email, get_veiculo_id, apagar_veiculo , inserir_registo_entrada, get_registo_entrada_id, remove_registo_entrada, get_all_veiculos , editar_registo_entrada , inserir_restauro , get_restauro_id , remove_restauro , editar_restauro , get_all_restauros, inserir_tipos_mao_obra, editar_tipos_mao_obra, get_tipo_mao_obra_id, remove_tipos_mao_obra, inserir_registo_saidas, editar_registo_saidas, remove_registo_saidas, get_registo_saidas_id, export_xml, export_json
from django.http import JsonResponse , HttpResponseNotFound , HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import xml.etree.ElementTree as ET
from decimal import Decimal
from django.contrib import messages
from django.conf import settings
from django.db import connection



#VIEWS DO PROJETO
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def index_view(request):
    return render(request, 'myapp/index.html')

#CLIENTES
def clientes_view(request):
    
    user_email = request.session.get('user', {}).get('email')
    cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)

    if request.session.get('user', {}).get('isAdmin', True):
        # Administradores podem ver todos os clientes
        clientes = Cliente.objects.using('mongo').all()
    else:
        # Utilizadores normais só podem ver os seus registos
        clientes = Cliente.objects.using('mongo').filter(email=user_email)

        
    
    data = clientes
    return render(request, 'myapp/clientes.html', {'data': data})

def clientes_insert_view(request, id = None):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    data = Cliente.objects.using('mongo').all()
    if request.method == "GET":
        if id:
            cliente = get_cliente_id(id)
            form = ClienteForm(initial={
                'nome': cliente['nome'],
                'endereco': cliente['endereco'],
                'telefone': cliente['telefone'],
                'email': cliente['email']
            }
                )
        else:
            form = ClienteForm(request.POST or None)
        return render(request, 'myapp/inserir_clientes.html', {'data': data, 'form': form, 'id': id})
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            if id:
                editar_cliente(cliente_id=id, nome=form.cleaned_data['nome'], endereco=form.cleaned_data['endereco'], telefone=form.cleaned_data['telefone'], email=form.cleaned_data['email'])
                return redirect('clientes_view')
            else:
                inserir_cliente(nome=form.cleaned_data['nome'], endereco=form.cleaned_data['endereco'], telefone=form.cleaned_data['telefone'], email=form.cleaned_data['email'])
                return redirect('clientes_view')
        else:
            return render(request, 'myapp/inserir_clientes.html', {'data': data, 'form': form, 'id': id})

def clientes_delete_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    apagar_cliente(id)

    data = Cliente.objects.using('mongo').all()
    return render(request, 'myapp/clientes.html', {'data': data})
#CLIENTES

#VEICULOS
def veiculos_view(request):

    user_email = request.session.get('user', {}).get('email')
    cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)
    clientes = Cliente.objects.using('mongo').all()
    clientes_dicts = [cliente.__dict__ for cliente in clientes]

    if request.session.get('user', {}).get('isAdmin', True):
        # Administradores podem ver todos os veículos
        veiculos = Veiculo.objects.using('mongo').all()
    else:
        # Utilizadores normais só podem ver os seus veículos
        cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)
        veiculos = Veiculo.objects.using('mongo').filter(cliente=cliente_aux[0].id)

    veiculo_dicts = [veiculo.__dict__ for veiculo in veiculos]
    data = []
    
    for veiculo in veiculo_dicts:
        for cliente in clientes_dicts:
            if veiculo['cliente'] == cliente['id']:
                veiculo['cliente'] = cliente['nome']
                data.append(veiculo)


    return render(request, 'myapp/veiculos.html', {'data': veiculos})

def veiculos_insert_view(request, id=None):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    veiculos = Veiculo.objects.using('mongo').all()
    clientes = Cliente.objects.using('mongo').all()

    if request.method == "GET":
        if id:
            veiculo = get_veiculo_id(id)
            form = VeiculoForm(initial={
                'cliente': veiculo['cliente'],
                'marca': veiculo['marca'],
                'modelo': veiculo['modelo'],
                'matricula': veiculo['matricula'],
                'cor': veiculo['cor'],
                'ano': veiculo['ano']
            })
        else:
            form = VeiculoForm()
        return render(request, 'myapp/inserir_veiculos.html', {'veiculos': veiculos, 'form': form, 'id': id, 'clientes': clientes})

    if request.method == "POST":
        form = VeiculoForm(request.POST)
        if form.is_valid():
            if id:
                editar_veiculo(
                    veiculo_id=id,
                    cliente=form.cleaned_data['cliente'],
                    marca=form.cleaned_data['marca'],
                    modelo=form.cleaned_data['modelo'],
                    matricula=form.cleaned_data['matricula'],
                    cor=form.cleaned_data['cor'],
                    ano=form.cleaned_data['ano']
                )
            else:
                inserir_veiculo(
                    cliente=form.cleaned_data['cliente'],
                    marca=form.cleaned_data['marca'],
                    modelo=form.cleaned_data['modelo'],
                    matricula=form.cleaned_data['matricula'],
                    cor=form.cleaned_data['cor'],
                    ano=form.cleaned_data['ano']
                )
            return redirect('veiculos_view')  # Redireciona para a página de lista de veículos após sucesso
        else:
            return render(request, 'myapp/inserir_veiculos.html', {'veiculos': veiculos, 'form': form, 'id': id, 'clientes': clientes})

def veiculos_delete_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    apagar_veiculo(id)
    data = Veiculo.objects.using('mongo').all()
    return render(request, 'myapp/veiculos.html', {'data': data})
#VEICULOS

#REGISTO DE ENTRADAS
def registo_entrada_insert_view(request):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        form = RegistoEntradaForm(request.POST)
        if form.is_valid():
            veiculo_id = form.cleaned_data.get('veiculo_id')
            data_entrada = form.cleaned_data.get('data_entrada')
            observacoes = form.cleaned_data.get('observacoes')
            
            if veiculo_id is None:
                form.add_error('veiculo_id', 'O campo Veículo ID é obrigatório.')
            else:
                # Inserir o registro de entrada
                inserir_registo_entrada(veiculo_id, data_entrada, observacoes)
                return redirect('registo_entradas_view')
    else:
        form = RegistoEntradaForm()
    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/registo_entrada_form.html', {'form': form, 'veiculos': veiculos})

def registo_entradas_view(request):
    data = RegistoEntrada.objects.all()
    return render(request, 'myapp/registo_entradas.html', {'data': data})

def registo_entrada_edit_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    registro = get_registo_entrada_id(id)
    if request.method == "POST":
        form = RegistoEntradaForm(request.POST)
        if form.is_valid():
            veiculo_id = form.cleaned_data.get('veiculo_id')
            data_entrada = form.cleaned_data.get('data_entrada')
            observacoes = form.cleaned_data.get('observacoes')
            
            if veiculo_id is None:
                form.add_error('veiculo_id', 'O campo Veículo ID é obrigatório.')
            else:
                # Atualizar o registro de entrada
                editar_registo_entrada(id, veiculo_id, data_entrada, observacoes)
                return redirect('registo_entradas_view')
    else:
        form = RegistoEntradaForm(initial={
            'veiculo_id': registro['veiculo_id'],
            'data_entrada': registro['data_entrada'],
            'observacoes': registro['observacoes']
        })
    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/registo_entrada_form.html', {'form': form, 'veiculos': veiculos})

def registo_entrada_delete_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        #registo = get_object_or_404(RegistoEntrada, id=id)
        remove_registo_entrada(id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
#REGISTO DE ENTRADAS

#RESTAUROS
def restauro_insert_view(request):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        form = RestauroForm(request.POST)
        if form.is_valid():
            veiculo_id = form.cleaned_data.get('veiculo_id')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            status = form.cleaned_data.get('status')
            
            if veiculo_id is None:
                form.add_error('veiculo_id', 'O campo Veículo ID é obrigatório.')
            elif data_inicio > date.today():
                form.add_error('data_inicio', 'A data de início não pode ser maior do que a data atual.')
            elif data_fim < data_inicio:
                form.add_error('data_fim', 'A data de fim não pode ser menor do que a data de início.')
            else:
                # Inserir o registro de entrada
                inserir_restauro(veiculo_id, data_inicio, data_fim, status)
                return redirect('restauros_view')
    else:
        form = RestauroForm()
    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/restauro_form.html', {'form': form, 'veiculos': veiculos})

def restauro_edit_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if id :
        aux = get_restauro_id(id)
        if aux is None:
            return custom_404(request, None)
        if aux.get('status') == "Concluído":
            return custom_404(request, None)
    
    restauros = get_restauro_id(id)
    if request.method == "POST":
        form = RestauroForm(request.POST)
        if form.is_valid():
            veiculo_id = form.cleaned_data.get('veiculo_id')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            status = form.cleaned_data.get('status')
            
            if veiculo_id is None:
                form.add_error('veiculo_id', 'O campo Veículo ID é obrigatório.')
            else:
                # Atualizar o registro de entrada
                editar_restauro(id, veiculo_id, data_inicio, data_fim, status)
                return redirect('restauros_view')
    else:
        form = RestauroForm(initial={
            'veiculo_id': restauros['veiculo_id'],
            'data_inicio': restauros['data_inicio'],
            'data_fim': restauros['data_fim'],
            'status': restauros['status']
        })
    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/restauro_form.html', {'form': form, 'veiculos': veiculos})

def restauro_delete_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        #restauro = get_object_or_404(Restauro, id=id)
        remove_restauro(id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def restauros_view(request):

    user_email = request.session.get('user', {}).get('email')
    cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)

    if request.session.get('user', {}).get('isAdmin', True):
        # Administradores podem ver todos os veículos
        veiculos = Veiculo.objects.using('mongo').all()
    else:
        # Utilizadores normais só podem ver os seus veículos
        cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)
        veiculos = Veiculo.objects.using('mongo').filter(cliente=cliente_aux[0].id)


    restauros = Restauro.objects.all()
    veiculo_dicts = [veiculo.__dict__ for veiculo in veiculos]
    restauros_dicts = [restauro.__dict__ for restauro in restauros]
    data = []

    for restauro in restauros_dicts:
        for veiculo in veiculo_dicts:
            if veiculo['id'] == restauro['veiculo_id']:
                restauro['veiculo_id'] = veiculo['matricula']
                data.append(restauro)

    restauros = data
    
    return render(request, 'myapp/restauros.html', {'restauros': restauros})
#RESTAUROS

#TAREFAS DE RESTAURO    
def tarefas_restauro_insert_view(request):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        restauro_id = request.POST.get('restauro_id')
        descricao = request.POST.get('descricao')
        mao_obra_id = request.POST.get('mao_obra')
        custo_total = request.POST.get('custo_total')
        tempo = request.POST.get('tempo')

        if restauro_id and mao_obra_id:
            inserir_tarefas_restauro(restauro_id, descricao, mao_obra_id, custo_total, tempo)
            return redirect('tarefas_restauro_view')
        else:
            form.add_error(None, 'Restauro e Mão de Obra são obrigatórios.')
    else:
        form = TarefaRestauroForm()

    tipos_mao_obra = get_all_tipos_mao_obra()
    restauros = Restauro.objects.all()
    veiculos = Veiculo.objects.using('mongo').all()
    veiculo_dicts = [veiculo.__dict__ for veiculo in veiculos]
    data = []

    #Verificar se o restauro está concluído
    for restauro in restauros:
        aux = str(restauro.status)
        if aux != "Concluído":
            data.append(restauro)


    for restauro in restauros:
        aux2 = str(restauro.veiculo_id)
        print(aux2)
        for veiculo in veiculo_dicts:
            if veiculo['id'] == aux2:
                restauro.veiculo_id = veiculo['matricula']
                data.append(restauro)
            


    return render(request, 'myapp/tarefas_restauro_form.html', {'form': form, 'restauros': restauros, 'tipos_mao_obra': tipos_mao_obra})

def tarefas_restauro_edit_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    
    tarefa_restauro = get_tarefa_restauro_id(id)
    if request.method == "POST":

        restauro_id = request.POST.get('restauro_id')
        descricao = request.POST.get('descricao')
        mao_obra = request.POST.get('mao_obra')
        custo_total = request.POST.get('custo_total')
        tempo = request.POST.get('tempo')
                    
        if restauro_id is None:
            form.add_error('restauro_id', 'O campo Restauro ID é obrigatório.')
        else:
            # Atualizar o registro de entrada
            editar_tarefa_restauro(id, restauro_id, descricao, mao_obra, custo_total,tempo)
            return redirect('tarefas_restauro_view')
    else:
        form = TarefaRestauroForm(initial={
            'restauro_id': tarefa_restauro['restauro_id'],
            'descricao': tarefa_restauro['descricao'],
            'mao_obra': tarefa_restauro['mao_obra'],
            'custo_total': tarefa_restauro['custo_total'],
            'tempo': tarefa_restauro['tempo']
        })
    
    restauros = Restauro.objects.all()
    veiculos = Veiculo.objects.using('mongo').all()
    veiculo_dicts = [veiculo.__dict__ for veiculo in veiculos]
    data = []

    #Verificar se o restauro está concluído
    for restauro in restauros:
        aux = str(restauro.status)
        if aux != "Concluído":
            data.append(restauro)


    for restauro in restauros:
        aux2 = str(restauro.veiculo_id)
        print(aux2)
        for veiculo in veiculo_dicts:
            if veiculo['id'] == aux2:
                restauro.veiculo_id = veiculo['matricula']
                data.append(restauro)
            

    # Buscar todos os veículos do MongoDB
    tipos_mao_De_obra = get_all_tipos_mao_obra()
    
    return render(request, 'myapp/tarefas_restauro_form.html', {'form': form, 'restauros': restauros , 'tipos_mao_obra': tipos_mao_De_obra})


def tarefas_restauro_view(request):
    data = []
    restauro = get_all_restauros()

    user_email = request.session.get('user', {}).get('email')
    cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)
    clientes = Cliente.objects.using('mongo').all()
    clientes_dicts = [cliente.__dict__ for cliente in clientes]

    if request.session.get('user', {}).get('isAdmin', True):
        data = get_all_tarefas_restauro()
        

    else:
        # Utilizadores normais só podem ver os seus veículos
        cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)
        veiculos = Veiculo.objects.using('mongo').filter(cliente=cliente_aux[0].id)
        for veiculo in veiculos:
            for aux in Restauro.objects.all().filter(veiculo_id=veiculo.id):
                data.append(get_tarefa_restauro_id_id(aux.id))


    return render(request, 'myapp/tarefas_restauro.html', {'data': data , 'restauro': restauro})

def tarefas_restauro_delete_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        #restauro = get_object_or_404(Restauro, id=id)
        remove_tarefa_restauro(id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


#FATURAÇÃO
def faturacao_view(request): 

    user_email = request.session.get('user', {}).get('email')
    cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)

    if request.session.get('user', {}).get('isAdmin', True):
        # Administradores podem ver todos os veículos
        veiculos = Veiculo.objects.using('mongo').all()
    else:
        # Utilizadores normais só podem ver os seus veículos
        cliente_aux = Cliente.objects.using('mongo').filter(email=user_email)
        veiculos = Veiculo.objects.using('mongo').filter(cliente=cliente_aux[0].id)

    restauros = Restauro.objects.all()
    faturacao = Faturacao.objects.all()
    data = []

    for veiculo in veiculos:
        for restauro in restauros:
            if restauro.veiculo_id == veiculo.id:
                for fatura in faturacao:
                    if fatura.restauro_id == restauro.id:
                        data.append(fatura)


    
    return render(request, 'myapp/faturacao.html', {'data': data}) 


def alterar_estado_para_pago_view(request, fatura_id):
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if fatura_id :
        faturacao = get_faturacao_id(fatura_id)
        if faturacao is None:
            return custom_404(request, None)
        if faturacao.get('status_pagamento') == "Pago":
            return custom_404(request, None)
    
    try:
        alterar_estado_para_pago(fatura_id)
        return redirect('faturacao_view')
    except Exception as e:
        return render(request, 'myapp/404.html', {'message': str(e)})

def faturacao_insert_view(request):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        form = FaturacaoForm(request.POST)
        if form.is_valid():
            veiculo_id = form.cleaned_data.get('veiculo_id')
            data = form.cleaned_data.get('data')
            valor = form.cleaned_data.get('valor')
            
            if veiculo_id is None:
                form.add_error('veiculo_id', 'O campo Veículo ID é obrigatório.')
            else:
                # Inserir o registro de entrada
                inserir_faturacao(veiculo_id, data, valor)
                return redirect('faturacao_view')
    else:
        form = FaturacaoForm()
    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/faturacao_form.html', {'form': form, 'veiculos': veiculos})



def faturacao_edit_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    registro = get_faturacao_id(id)
    if request.method == "POST":
        form = FaturacaoForm(request.POST)
        if form.is_valid():
            veiculo_id = form.cleaned_data.get('veiculo_id')
            data = form.cleaned_data.get('data')
            valor = form.cleaned_data.get('valor')
            
            if veiculo_id is None:
                form.add_error('veiculo_id', 'O campo Veículo ID é obrigatório.')
            else:
                # Atualizar o registro de entrada
                editar_faturacao(id, veiculo_id, data, valor)
                return redirect('faturacao_view')
    else:
        form = FaturacaoForm(initial={
            'veiculo_id': registro['veiculo_id'],
            'data': registro['data'],
            'valor': registro['valor']
        })

def faturacao_delete_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        #registro = get_object_or_404(Faturacao, id=id)
        remove_faturacao(id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/faturacao_form.html', {'form': form, 'veiculos': veiculos})

#FATURAÇÃO


#TIPOS MAO OBRA

def registo_tipos_mao_obra_insert_view(request):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        form = TipoMaoObraForm(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data.get('descricao')
            custo_por_hora = form.cleaned_data.get('custo_por_hora')
            
            
            # Inserir o registro de entrada
            inserir_tipos_mao_obra(descricao, custo_por_hora)
            return redirect('registo_tipos_mao_obra_view')
    else:
        form = TipoMaoObraForm()
    
    return render(request, 'myapp/tipos_mao_obra_form.html', {'form': form})

def registo_tipos_mao_obra_view(request):
    data = TipoMaoObra.objects.all()
    return render(request, 'myapp/tipos_mao_obra.html', {'data': data})

def registo_tipos_mao_obra_edit_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    registro = get_tipo_mao_obra_id(id)
    if request.method == "POST":
        form = TipoMaoObraForm(request.POST)
        if form.is_valid():
            descricao = form.cleaned_data.get('descricao')
            custo_por_hora = form.cleaned_data.get('custo_por_hora')
            
           
            # Atualizar o registro de entrada
            editar_tipos_mao_obra(id, descricao, custo_por_hora)
            return redirect('registo_tipos_mao_obra_view')
    else:
        form = TipoMaoObraForm(initial={
            'descricao': registro['descricao'],
            'custo_por_hora': registro['custo_por_hora']
        })
    
    return render(request, 'myapp/tipos_mao_obra_form.html', {'form': form})

def registo_tipos_mao_obra_delete_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        #registro = get_object_or_404(TipoMaoObra, id=id)
        remove_tipos_mao_obra(id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
#TIPOS MAO OBRA


#SAIDA DE VEICULOS
def registo_saidas_insert_view(request):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        form = RegistoSaidasForm(request.POST)
        if form.is_valid():
            veiculo_id = form.cleaned_data.get('veiculo_id')
            data_saida = form.cleaned_data.get('data_saida')
            condicoes_saida = form.cleaned_data.get('condicoes_saida')
            observacoes = form.cleaned_data.get('observacoes')
            
            if veiculo_id is None:
                form.add_error('veiculo_id', 'O campo Veículo ID é obrigatório.')
            else:
                # Inserir o registro de entrada
                inserir_registo_saidas(veiculo_id, data_saida, condicoes_saida, observacoes)
                return redirect('registo_saidas_view')
    else:
        form = RegistoSaidasForm()
    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/registo_saidas_form.html', {'form': form, 'veiculos': veiculos})

def registo_saidas_view(request):
    data = SaidaVeiculo.objects.all()
    return render(request, 'myapp/saidas_veiculos.html', {'data': data})

def registo_saidas_edit_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    registro = get_registo_saidas_id(id)
    if request.method == "POST":
        form = RegistoSaidasForm(request.POST)
        if form.is_valid():
            veiculo_id = form.cleaned_data.get('veiculo_id')
            data_saida = form.cleaned_data.get('data_saida')
            condicoes_saida = form.cleaned_data.get('condicoes_saida')
            observacoes = form.cleaned_data.get('observacoes')
            
            if veiculo_id is None:
                form.add_error('veiculo_id', 'O campo Veículo ID é obrigatório.')
            else:
                # Atualizar o registro de entrada
                editar_registo_saidas(id, veiculo_id, data_saida, condicoes_saida, observacoes)
                return redirect('registo_saidas_view')
    else:
        form = RegistoSaidasForm(initial={
            'veiculo_id': registro['veiculo_id'],
            'data_saida': registro['data_saida'],
            'condicoes_saida': registro['condicoes_saida'],
            'observacoes': registro['observacoes']
        })
    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/registo_saidas_form.html', {'form': form, 'veiculos': veiculos})

def registo_saidas_delete_view(request, id):
    
    if not request.session.get('user', {}).get('isAdmin', False):
        return custom_404(request, None)
    
    if request.method == "POST":
        #registro = get_object_or_404(SaidaVeiculo, id=id
        print(id)
        remove_registo_saidas(id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
#SAIDA DE VEICULOS


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError

def exportar_tarefas_json(request):
    request = json.dumps(export_json()[0][0], ensure_ascii=False, indent=4)
    if request:
        response = HttpResponse (content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=tarefas_restauro.json'
        response.write(request)
        return response

def exportar_tarefas_xml(request):
    request = export_xml()[0][0]
    if request:
        response = HttpResponse (content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=tarefas_restauro.xml'
        response.write(request)
        return response


def import_tarefas_restauro_xml_json(request):
    if request.method == 'POST':
        file = request.FILES['file']
        if file.name.endswith('.json'):
            import_from_json(file)
        elif file.name.endswith('.xml'):
            import_from_xml(file)
        else:
            messages.error(request, 'Formato de arquivo não suportado.')
            return redirect('tarefas_restauro_view')
        
        messages.success(request, 'Tarefas de restauro importadas com sucesso.')
        return redirect('tarefas_restauro_view')
    return render(request, 'tarefas_restauro.html')

def import_from_json(file):
    data = json.load(file)
    with connection.cursor() as cursor:
        for tarefa in data:
            cursor.execute("""
                INSERT INTO tarefas_restauro (id, restauro_id, descricao, mao_obra, custo_total, tempo)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                restauro_id = EXCLUDED.restauro_id,
                descricao = EXCLUDED.descricao,
                mao_obra = EXCLUDED.mao_obra,
                custo_total = EXCLUDED.custo_total,
                tempo = EXCLUDED.tempo
            """, (tarefa['id'], tarefa['restauro_id'], tarefa['descricao'], tarefa['mao_obra'], tarefa['custo_total'], tarefa['tempo']))

def import_from_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    with connection.cursor() as cursor:
        for tarefa in root.findall('tarefa'):
            id = tarefa.find('id').text
            restauro_id = tarefa.find('restauro_id').text
            descricao = tarefa.find('descricao').text
            mao_obra = tarefa.find('mao_obra').text
            custo_total = tarefa.find('custo_total').text
            tempo = tarefa.find('tempo').text

            cursor.execute("""
                INSERT INTO tarefas_restauro (id, restauro_id, descricao, mao_obra, custo_total, tempo)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                restauro_id = EXCLUDED.restauro_id,
                descricao = EXCLUDED.descricao,
                mao_obra = EXCLUDED.mao_obra,
                custo_total = EXCLUDED.custo_total,
                tempo = EXCLUDED.tempo
            """, (id, restauro_id, descricao, mao_obra, custo_total, tempo))