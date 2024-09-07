from django.db import models


class Cliente(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
   # role = models.CharField(max_length=50)
    isAdmin = models.BooleanField(default=False)

    class Meta:
        db_table = "cliente"
        managed = False
    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30)
    matricula = models.CharField(max_length=20)
    cliente = models.CharField(max_length=250)

    class Meta:
        db_table = "veiculo"
        managed = False
    def __str__(self):
        return self.marca + " " + self.modelo
        
class RegistoEntrada(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_entrada = models.DateField()
    observacoes = models.TextField(null=True, blank=True)
    
    class Meta:
        db_table = "registo_entradas"
        managed = True

class Restauro(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "restauros"
        managed = True

class TipoMaoObra(models.Model):
    descricao = models.CharField(max_length=100)
    custo_por_hora = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "tipos_mao_obra"
        managed = True
        
class TarefaRestauro(models.Model):
    restauro = models.ForeignKey(Restauro, on_delete=models.CASCADE)
    descricao = models.TextField()
    mao_obra = models.ForeignKey(TipoMaoObra, on_delete=models.CASCADE)
    tempo = models.DecimalField(max_digits=5, decimal_places=2)
    custo_total = models.DecimalField(max_digits=10, decimal_places=2)
    restauro_id_id = models.CharField(max_length=50)

    class Meta:
        db_table = "tarefas_restauro"
        managed = True

class Faturacao(models.Model):
    restauro = models.ForeignKey(Restauro, on_delete=models.CASCADE)
    data_emissao = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    itens = models.TextField(null=True, blank=True)
    status_pagamento = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = "faturacao"
        managed = True

class SaidaVeiculo(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_saida = models.DateField()
    condicoes_saida = models.TextField(null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "saidas_veiculos"
        managed = True



