from myproject.mongodb_conne import MongoConnection
from django.db import connections
from .utils import generate_uuid_srt
db = MongoConnection().get_db()
Cliente = MongoConnection().get_collection('cliente')
Veiculo = MongoConnection().get_collection('veiculo')

def inserir_cliente(nome, endereco, telefone, email):
    cliente_doc = {
        'id': generate_uuid_srt(),
        'nome': nome,
        'endereco': endereco,
        'telefone': telefone,
        'email': email
    }
    return Cliente.insert_one(cliente_doc)

def inserir_veiculo(cliente, marca, modelo, matricula, cor, ano):
    veiculo_doc = {
        'id': generate_uuid_srt(),
        'cliente': cliente,
        'marca': marca,
        'modelo': modelo,
        'matricula': matricula,
        'cor': cor,
        'ano': ano
    }
    return Veiculo.insert_one(veiculo_doc)