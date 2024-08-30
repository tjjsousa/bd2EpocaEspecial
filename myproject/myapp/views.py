from django.shortcuts import render
from .models import MyModel
from .forms import VeiculoForm, ClienteForm
from .models import MongoModel
from .models import Cliente, Veiculo, RegistoEntrada, Restauro, TarefaRestauro, Faturacao, SaidaVeiculo, TipoMaoObra
from .database import inserir_cliente, inserir_veiculo, editar_cliente, editar_veiculo, get_cliente_id, apagar_cliente, get_veiculo_id, apagar_veiculo

def my_view(request):
    data = MyModel.objects.all()
    return render(request, 'myapp/mytemplate.html', {'data': data})


def mongo_view(request):
    data = MongoModel.objects.using('mongo').all()
    return render(request, 'myapp/mongo_template.html', {'data': data})

#VIEWS DO PROJETO

def index_view(request):
    return render(request, 'myapp/index.html')

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

def registo_entradas_view(request):
    data = RegistoEntrada.objects.all()
    return render(request, 'myapp/registo_entradas.html', {'data': data})

def restauros_view(request):
    data = Restauro.objects.all()
    return render(request, 'myapp/restauros.html', {'data': data})

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
