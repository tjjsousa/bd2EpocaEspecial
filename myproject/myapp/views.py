from django.shortcuts import render
from .models import MyModel
from .forms import VeiculoForm, ClienteForm
from .models import MongoModel
from .models import Cliente, Veiculo, RegistoEntrada, Restauro, TarefaRestauro, Faturacao, SaidaVeiculo, TipoMaoObra
from .database import inserir_cliente, inserir_veiculo

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

def clientes_insert_view(request):
    data = Cliente.objects.using('mongo').all()
    if request.method == "GET":
        form = ClienteForm(request.POST or None)
        return render(request, 'myapp/inserir_clientes.html', {'data': data, 'form': form})
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            inserir_cliente(nome=form.cleaned_data['nome'], endereco=form.cleaned_data['endereco'], telefone=form.cleaned_data['telefone'], email=form.cleaned_data['email'])
            return render(request, 'myapp/inserir_clientes.html', {'data': data, 'form': form})
        else:
            return render(request, 'myapp/inserir_clientes.html', {'data': data, 'form': form})
    
def veiculos_view(request):
    data = Veiculo.objects.using('mongo').all()
    return render(request, 'myapp/veiculos.html', {'data': data})

def veiculos_insert_view(request):
    data = Veiculo.objects.using('mongo').all()
    if request.method == "GET":
        form = VeiculoForm(request.POST or None)
        return render(request, 'myapp/inserir_veiculos.html', {'data': data, 'form': form})
    if request.method == "POST":
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.cleaned_data
            inserir_veiculo(cliente= form.data['cliente'], marca=form.data['marca'], modelo=form.data['modelo'], matricula=form.data['matricula'], cor=form.data['cor'], ano=form.data['ano'])
            return render(request, 'myapp/inserir_veiculos.html', {'data': data, 'form': form})
        else:
            return render(request, 'myapp/inserir_veiculos.html', {'data': data, 'form': form})

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
