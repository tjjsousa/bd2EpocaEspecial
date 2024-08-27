from django.db import models
from djongo import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class MongoModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = "mongo_model"


#TABELAS DO PROJETO

# Model para a tabela Clientes
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

    class Meta:
        db_table = "clientes"

# Model para a tabela Veiculos
class Veiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30)
    matricula = models.CharField(max_length=20)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        db_table = "veiculos"

# Model para a tabela RegistoEntradas
class RegistoEntrada(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_entrada = models.DateField()
    observacoes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "registo_entradas"

# Model para a tabela Restauros
class Restauro(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "restauros"

# Model para a tabela TarefasRestauro
class TarefaRestauro(models.Model):
    restauro = models.ForeignKey(Restauro, on_delete=models.CASCADE)
    descricao = models.TextField()
    mao_obra = models.CharField(max_length=100)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "tarefas_restauro"

# Model para a tabela Faturacao
class Faturacao(models.Model):
    restauro = models.ForeignKey(Restauro, on_delete=models.CASCADE)
    data_emissao = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    itens = models.TextField(null=True, blank=True)
    status_pagamento = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "faturacao"

# Model para a tabela SaidasVeiculos
class SaidaVeiculo(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_saida = models.DateField()
    condicoes_saida = models.TextField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "saidas_veiculos"

# Model para a tabela TiposMaoObra
class TipoMaoObra(models.Model):
    descricao = models.CharField(max_length=100)
    custo_por_hora = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "tipos_mao_obra"