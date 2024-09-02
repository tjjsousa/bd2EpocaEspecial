from django import forms
from .models import Cliente, Veiculo, RegistoEntrada, Restauro, TarefaRestauro, Faturacao, SaidaVeiculo, TipoMaoObra

class ClienteForm(forms.Form):
    nome = forms.CharField(max_length=100)
    endereco = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)

class VeiculoForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.using('mongo').all(), empty_label="Selecione um cliente", to_field_name="id")
    marca = forms.CharField(max_length=100)
    modelo = forms.CharField(max_length=100)
    matricula = forms.CharField(max_length=100)
    cor = forms.CharField(max_length=100)
    ano = forms.IntegerField()

class RegistoEntradaForm(forms.Form):
    veiculo_id = forms.CharField(widget=forms.HiddenInput())
    data_entrada = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    observacoes = forms.CharField(max_length=100)

class RestauroForm(forms.Form):
    veiculo_id = forms.CharField(widget=forms.HiddenInput())
    data_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    status = forms.CharField(max_length=255)

class TarefaRestauroForm(forms.Form):
    restauro_id = forms.CharField(widget=forms.HiddenInput())
    descricao = forms.CharField(max_length=100)
    mao_obra = forms.CharField(max_length=100) #widget=forms.HiddenInput()
    custo_total = forms.FloatField()

class FaturacaoForm(forms.Form):
    restauro_id = forms.CharField(widget=forms.HiddenInput())
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    valor = forms.FloatField()
    observacoes = forms.CharField(max_length=100)

class TipoMaoObraForm(forms.Form):
    descricao = forms.CharField(max_length=100)
    custo_por_hora = forms.FloatField()

class RegistoSaidasForm(forms.Form):
    veiculo_id = forms.CharField(widget=forms.HiddenInput())
    data_saida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    condicoes_saida = forms.CharField(max_length=100)
    observacoes = forms.CharField(max_length=100)