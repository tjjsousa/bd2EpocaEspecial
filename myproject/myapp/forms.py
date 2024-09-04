from django import forms
from .models import Cliente, Veiculo, RegistoEntrada, Restauro, TarefaRestauro, Faturacao, SaidaVeiculo, TipoMaoObra


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone' , 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }
class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['marca', 'modelo', 'matricula', 'cor', 'ano', 'cliente']  # Adicione 'cliente' se necessário
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),  # Use Select para campos de chave estrangeira
        
        }
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
    restauro = forms.CharField(widget=forms.HiddenInput())
    descricao = forms.CharField(max_length=255)
    mao_obra = forms.CharField(max_length=255)
    custo_total = forms.CharField(max_length=255)
    tempo = forms.CharField(max_length=255)


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