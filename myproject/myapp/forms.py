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
    
