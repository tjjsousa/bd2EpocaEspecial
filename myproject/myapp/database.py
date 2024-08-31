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


def get_registo_entrada_id(registo_id):
    with pgsql_conn.cursor() as cursor:
        cursor.execute("SELECT * FROM registo_entrada WHERE id = %s", [registo_id])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None

def remove_registo_entrada(registo_id):
    with pgsql_conn.cursor() as cursor:
        cursor.execute("DELETE FROM registo_entrada WHERE id = %s", [registo_id])
        pgsql_conn.commit()
        return cursor.rowcount
