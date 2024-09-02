from django.shortcuts import render , redirect
from .forms import VeiculoForm, ClienteForm , RegistoEntradaForm , RestauroForm
from .models import Cliente, Veiculo, RegistoEntrada, Restauro, TarefaRestauro, Faturacao, SaidaVeiculo, TipoMaoObra
from .database import inserir_cliente, inserir_veiculo, editar_cliente, editar_veiculo, get_cliente_id, apagar_cliente, get_veiculo_id, apagar_veiculo , inserir_registo_entrada, get_registo_entrada_id, remove_registo_entrada, get_all_veiculos , editar_registo_entrada , inserir_restauro , get_restauro_id , remove_restauro , editar_restauro , get_all_restauros
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

#VIEWS DO PROJETO

def index_view(request):
    return render(request, 'myapp/index.html')

#CLIENTES
def clientes_view(request):
    data = Cliente.objects.using('mongo').all()
    return render(request, 'myapp/clientes.html', {'data': data})

def clientes_insert_view(request, id = None):
    
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
            else:
                inserir_cliente(nome=form.cleaned_data['nome'], endereco=form.cleaned_data['endereco'], telefone=form.cleaned_data['telefone'], email=form.cleaned_data['email'])
            return render(request, 'myapp/inserir_clientes.html', {'data': data, 'form': form, 'id': id})
        else:
            return render(request, 'myapp/inserir_clientes.html', {'data': data, 'form': form, 'id': id})

def clientes_delete_view(request, id):
    apagar_cliente(id)
    data = Cliente.objects.using('mongo').all()
    return render(request, 'myapp/clientes.html', {'data': data})
#CLIENTES

#VEICULOS
def veiculos_view(request):
    clientes = Cliente.objects.using('mongo').all()
    clientes_dicts = [cliente.__dict__ for cliente in clientes]
    veiculos = Veiculo.objects.using('mongo').all()
    veiculo_dicts = [veiculo.__dict__ for veiculo in veiculos]
    data = []
    
    for veiculo in veiculo_dicts:
        for cliente in clientes_dicts:
            if veiculo['cliente'] == cliente['id']:
                veiculo['cliente'] = cliente['nome']
                data.append(veiculo)

    return render(request, 'myapp/veiculos.html', {'data': veiculos})

def veiculos_insert_view(request, id = None):
    data = Veiculo.objects.using('mongo').all()
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
            }
                )
        else:
            form = VeiculoForm(request.POST or None)
        return render(request, 'myapp/inserir_veiculos.html', {'data': data, 'form': form, 'id': id})
    if request.method == "POST":
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            if id:
                editar_veiculo(veiculo_id=id, cliente= form.data['cliente'], marca=form.data['marca'], modelo=form.data['modelo'], matricula=form.data['matricula'], cor=form.data['cor'], ano=form.data['ano'])
            else:
                inserir_veiculo(cliente= form.data['cliente'], marca=form.data['marca'], modelo=form.data['modelo'], matricula=form.data['matricula'], cor=form.data['cor'], ano=form.data['ano'])
            return render(request, 'myapp/inserir_veiculos.html', {'data': data, 'form': form, 'id': id})
        else:
            return render(request, 'myapp/inserir_veiculos.html', {'data': data, 'form': form,  'id': id})

def veiculos_delete_view(request, id):
    apagar_veiculo(id)
    data = Veiculo.objects.using('mongo').all()
    return render(request, 'myapp/veiculos.html', {'data': data})
#VEICULOS

#REGISTO DE ENTRADAS
def registo_entrada_insert_view(request):
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
    if request.method == "POST":
        #registo = get_object_or_404(RegistoEntrada, id=id)
        remove_registo_entrada(id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
#REGISTO DE ENTRADAS

#RESTAUROS
def restauro_insert_view(request):
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
                # Inserir o registro de entrada
                inserir_restauro(veiculo_id, data_inicio, data_fim, status)
                return redirect('restauros_view')
    else:
        form = RestauroForm()
    
    # Buscar todos os veículos do MongoDB
    veiculos = get_all_veiculos()
    
    return render(request, 'myapp/restauro_form.html', {'form': form, 'veiculos': veiculos})

def restauro_edit_view(request, id):
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
    if request.method == "POST":
        #restauro = get_object_or_404(Restauro, id=id)
        remove_restauro(id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def restauros_view(request):
    restauros = Restauro.objects.all()
    return render(request, 'myapp/restauros.html', {'restauros': restauros})
#RESTAUROS

#TAREFAS DE RESTAURO    
def tarefas_restauro_view(request):
    data = TarefaRestauro.objects.all()
    return render(request, 'myapp/tarefas_restauro.html', {'data': data})

def faturacao_view(request):
    data = Faturacao.objects.all()
    return render(request, 'myapp/faturacao.html', {'data': data})

def saidas_veiculos_view(request):
    data = SaidaVeiculo.objects.all()
    return render(request, 'myapp/saidas_veiculos.html', {'data': data})

def tipos_mao_obra_view(request):
    data = TipoMaoObra.objects.all()
    return render(request, 'myapp/tipos_mao_obra.html', {'data': data})
