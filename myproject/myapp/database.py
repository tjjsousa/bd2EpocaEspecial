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

    
def editar_cliente(cliente_id, nome = None, endereco = None, telefone = None, email = None):
    
    cliente_doc = {
        'nome': nome,
        'endereco': endereco,
        'telefone': telefone,
        'email': email
    }
    return Cliente.update_one({'id': str(cliente_id)}, {"$set": cliente_doc})

def get_cliente_id(cliente_id):
    return Cliente.find_one({'id': cliente_id})

def apagar_cliente(cliente_id):
    return Cliente.delete_one({'id': cliente_id})


def editar_veiculo(veiculo_id, cliente, marca, modelo, matricula, cor, ano):
    veiculo_doc = {
        'cliente': cliente,
        'marca': marca,
        'modelo': modelo,
        'matricula': matricula,
        'cor': cor,
        'ano': ano
    }
    return Veiculo.update_one({'id': str(veiculo_id)}, {"$set": veiculo_doc})

def get_veiculo_id(veiculo_id):
    return Veiculo.find_one({'id': veiculo_id})

def apagar_veiculo(veiculo_id):
    return Veiculo.delete_one({'id': veiculo_id})

