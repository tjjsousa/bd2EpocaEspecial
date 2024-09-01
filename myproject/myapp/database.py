from myproject.mongodb_conne import MongoConnection
from django.db import connections , connection
from .utils import generate_uuid_srt
db = MongoConnection().get_db()
Cliente = MongoConnection().get_collection('cliente')
Veiculo = MongoConnection().get_collection('veiculo')

# PostgreSQL connection
pgsql_conn = connections['default']

def inserir_cliente(nome, endereco, telefone, email):
    cliente_doc = {
        'id': generate_uuid_srt(),
        'nome': nome,
        'endereco': endereco,
        'telefone': telefone,
        'email': email
    }
    return Cliente.insert_one(cliente_doc)

    
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

def get_all_veiculos():
    return Veiculo.find()

def inserir_registo_entrada(veiculo_id, data_entrada, observacoes):
    if veiculo_id is None:
        raise ValueError("O campo 'veiculo_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO registo_entradas (veiculo_id, data_entrada, observacoes) VALUES (%s, %s, %s)",
                [veiculo_id, data_entrada, observacoes]
            )
    finally:
        connection.close()

def editar_registo_entrada(registo_id, veiculo_id, data_entrada, observacoes):
    if registo_id is None:
        raise ValueError("O campo 'registo_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE registo_entradas SET veiculo_id = %s, data_entrada = %s, observacoes = %s WHERE id = %s",
                [veiculo_id, data_entrada, observacoes, registo_id]
            )
    finally:
        connection.close()


def get_registo_entrada_id(registo_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM registo_entradas WHERE id = %s", [registo_id])
            result = cursor.fetchone()
            if result:
                # Acesse os elementos da tupla usando índices inteiros
                return {
                    'id': result[0],
                    'veiculo_id': result[1],
                    'data_entrada': result[2],
                    'observacoes': result[3]
                }
            return None
    finally:
        connection.close()

def remove_registo_entrada(registo_id):
    if registo_id is None:
        raise ValueError("O campo 'registo_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM registo_entradas WHERE id = %s", [registo_id])
    finally:
        connection.close()

def inserir_restauro(veiculo_id, data_inicio, data_fim, descricao):
    if veiculo_id is None:
        raise ValueError("O campo 'veiculo_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO restauros (veiculo_id, data_inicio, data_fim, descricao) VALUES (%s, %s, %s, %s)",
                [veiculo_id, data_inicio, data_fim, descricao]
            )
    finally:
        connection.close()

def editar_restauro(restauro_id, veiculo_id, data_inicio, data_fim, descricao):
    if restauro_id is None:
        raise ValueError("O campo 'restauro_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE restauros SET veiculo_id = %s, data_inicio = %s, data_fim = %s, descricao = %s WHERE id = %s",
                [veiculo_id, data_inicio, data_fim, descricao, restauro_id]
            )
    finally:
        connection.close()

def get_restauro_id(restauro_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM restauros WHERE id = %s", [restauro_id])
            result = cursor.fetchone()
            if result:
                # Acesse os elementos da tupla usando índices inteiros
                return {
                    'id': result[0],
                    'veiculo_id': result[1],
                    'data_inicio': result[2],
                    'data_fim': result[3],
                    'descricao': result[4]
                }
            return None
    finally:
        connection.close()

def remove_restauro(restauro_id):
    if restauro_id is None:
        raise ValueError("O campo 'restauro_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM restauros WHERE id = %s", [restauro_id])
    finally:
        connection.close()

