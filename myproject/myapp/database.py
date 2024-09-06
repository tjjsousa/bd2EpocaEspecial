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
    print(cliente_id)
    return Cliente.delete_one({'id': cliente_id})

def apagar_cliente_email(email):
    print(email)
    return Cliente.delete_one({'email': email})

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

def inserir_restauro(veiculo_id, data_inicio, data_fim, status):
    if veiculo_id is None:
        raise ValueError("O campo 'veiculo_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO restauros (veiculo_id, data_inicio, data_fim, status) VALUES (%s, %s, %s, %s)",
                [veiculo_id, data_inicio, data_fim, status]
            )
    finally:
        connection.close()

def editar_restauro(restauro_id, veiculo_id, data_inicio, data_fim, status):
    if restauro_id is None:
        raise ValueError("O campo 'restauro_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE restauros SET veiculo_id = %s, data_inicio = %s, data_fim = %s, status = %s WHERE id = %s",
                [veiculo_id, data_inicio, data_fim, status, restauro_id]
            )
    finally:
        connection.close()

def get_all_restauros():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM restauros")
            result = cursor.fetchall()
            if result:
                return [
                    {
                        'id': row[0],
                        'veiculo_id': row[1],
                        'data_inicio': row[2],
                        'data_fim': row[3],
                        'status': row[4]
                    }
                    for row in result
                ]
            return []
    finally:
        connection.close()

def get_restauro_id(restauro_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM restauros WHERE id = %s", [restauro_id])
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'veiculo_id': result[1],
                    'data_inicio': result[2],
                    'data_fim': result[3],
                    'status': result[4]
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

def inserir_tarefas_restauro(restauro_id, descricao, mao_obra, custo_total, tempo):
    if restauro_id is None or mao_obra is None:
        raise ValueError("Os campos 'restauro_id' e 'mao_obra' não podem ser nulos.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tarefas_restauro (restauro_id, descricao, mao_obra, custo_total, tempo)
                VALUES (%s, %s, %s, %s, %s)""", [restauro_id, descricao, mao_obra, custo_total, tempo])
    finally:
        connection.close()

def get_all_tarefas_restauro():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tarefas_restauro_view")
            result = cursor.fetchall()
            if result:
                
                return [
                    {
                        'id': row[0],
                        'restauro_id': row[1],
                        'descricao': row[2],
                        'mao_obra': row[3],
                        'custo_total': row[4],
                        'tempo': row[5]
                    }
                    for row in result
                ]
            return []
    finally:
        connection.close()

def get_all_tarefas_restauro_id():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tarefas_restauro")
            result = cursor.fetchall()
            if result:
                
                return [
                    {
                        'id': row[0],
                        'restauro_id': row[1],
                        'descricao': row[2],
                        'mao_obra': row[3],
                        'custo_total': row[4],
                        'tempo': row[5]
                    }
                    for row in result
                ]
            return []
    finally:
        connection.close()

def get_tarefa_restauro_id(tarefa_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tarefas_restauro WHERE id = %s", [tarefa_id])
            result = cursor.fetchone()
            if result:
                
                return {
                    'id': result[0],
                    'restauro_id': result[1],
                    'descricao': result[2],
                    'mao_obra': result[3],
                    'custo_total': result[4],
                    'tempo': result[5]
                }
            return None
    finally:
        connection.close()

def editar_tarefa_restauro(tarefa_id, restauro_id, descricao, mao_obra, custo_total, tempo):
    if tarefa_id is None:
        raise ValueError("O campo 'tarefa_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE tarefas_restauro SET restauro_id = %s, descricao = %s, mao_obra = %s, custo_total = %s , tempo = %s WHERE id = %s",
                [restauro_id, descricao, mao_obra, custo_total, tempo , tarefa_id]
            )
    finally:
        connection.close()

def remove_tarefa_restauro(tarefa_id):
    if tarefa_id is None:
        raise ValueError("O campo 'tarefa_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tarefas_restauro WHERE id = %s", [tarefa_id])
    finally:
        connection.close()

#relativo a faturação
def get_faturacao_id(fatura_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM faturacao WHERE id = %s", [fatura_id])
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'restauro_id': result[1],
                    'data_emissao': result[2],
                    'valor_total': result[3],
                    'itens': result[4],
                    'status_pagamento': result[5]
                }
            return None
    finally:
        connection.close()

def editar_faturacao(fatura_id, restauro_id, data_emissao, valor_total, itens, status_pagamento):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE faturacao
                SET restauro_id = %s,
                    data_emissao = %s,
                    valor_total = %s,
                    itens = %s,
                    status_pagamento = %s
                WHERE id = %s
            """, [restauro_id, data_emissao, valor_total, itens, status_pagamento, fatura_id])
            connection.commit()
    finally:
        connection.close()

def inserir_faturacao(restauro_id, data_emissao, valor_total, itens, status_pagamento):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO faturacao (restauro_id, data_emissao, valor_total, itens, status_pagamento)
                VALUES (%s, %s, %s, %s, %s)
            """, [restauro_id, data_emissao, valor_total, itens, status_pagamento])
            connection.commit()
    finally:
        connection.close()

def alterar_estado_para_pago(fatura_id):
    if fatura_id is None:
        raise ValueError("O campo 'fatura_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE faturacao
                SET status_pagamento = 'Pago'
                WHERE id = %s
            """, [fatura_id])
            connection.commit()
    finally:
        connection.close()

def remove_faturacao(fatura_id):
    if fatura_id is None:
        raise ValueError("O campo 'fatura_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM faturacao WHERE id = %s", [fatura_id])
    finally:
        connection.close()

#relativo a tipos de mão de obra
def inserir_tipos_mao_obra(descricao, custo_por_hora):
    if descricao is None:
        raise ValueError("O campo descrição não pode ser nulo.")

    if custo_por_hora is None:
        raise ValueError("O campo custo_por_hora não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tipos_mao_obra (descricao, custo_por_hora) VALUES (%s, %s)",
                [descricao, custo_por_hora]
            )
    finally:
        connection.close()

def editar_tipos_mao_obra(id, descricao, custo_por_hora):
    if id is None:
        raise ValueError("O campo 'id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE tipos_mao_obra SET descricao = %s, custo_por_hora = %s WHERE id = %s",
                [descricao, custo_por_hora, id]
            )
    finally:
        connection.close()

def get_tipo_mao_obra_id(id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tipos_mao_obra WHERE id = %s", [id])
            result = cursor.fetchone()
            if result:
                # Acesse os elementos da tupla usando índices inteiros
                return {
                    'id': result[0],
                    'descricao': result[1],
                    'custo_por_hora': result[2]
                }
            return None
    finally:
        connection.close()

def remove_tipos_mao_obra(id):
    if id is None:
        raise ValueError("O campo 'id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tipos_mao_obra WHERE id = %s", [id])
    finally:
        connection.close()


#relativo a saidas de veiculos
def inserir_registo_saidas(veiculo_id, data_saida, condicoes_saida, observacoes):
    if veiculo_id is None:
        raise ValueError("O campo 'veiculo_id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO saidas_veiculos (veiculo_id, data_saida, condicoes_saida, observacoes) VALUES (%s, %s, %s, %s)",
                [veiculo_id, data_saida, condicoes_saida, observacoes]
            )
    finally:
        connection.close()

def editar_registo_saidas(id, veiculo_id, data_saida, condicoes_saida, observacoes):
    if id is None:
        raise ValueError("O campo 'id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE saidas_veiculos SET veiculo_id = %s, data_saida = %s, condicoes_saida = %s, observacoes = %s WHERE id = %s",
                [veiculo_id, data_saida, condicoes_saida, observacoes, id]
            )
    finally:
        connection.close()

def remove_registo_saidas(id):
    if id is None:
        raise ValueError("O campo 'id' não pode ser nulo.")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM saidas_veiculos WHERE id = %s", [id])
    finally:
        connection.close()

def get_registo_saidas_id(id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM saidas_veiculos WHERE id = %s", [id])
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'veiculo_id': result[1],
                    'data_saida': result[2],
                    'condicoes_saida': result[3],
                    'observacoes': result[4]
                }
            return None
    finally:
        connection.close()
        
        
def get_all_tipos_mao_obra():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tipos_mao_obra")
            result = cursor.fetchall()
            if result:
                # Acesse os elementos da tupla usando índices inteiros
                return [
                    {
                        'id': row[0],
                        'descricao': row[1],
                        'custo_por_hora': row[2]
                    }
                    for row in result
                ]
            return []
    finally:
        connection.close()


def export_xml():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT obter_tarefas_restauro_xml()")
            result = cursor.fetchall()
            if result:
                return result

            return None
    finally:
        connection.close()

def export_json():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT obter_tarefas_restauro_json()")
            result = cursor.fetchall()
            if result:
                return result

            return None
    finally:
        connection.close()    