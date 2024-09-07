from django.test import TestCase
from myapp.database import inserir_registo_entrada, editar_registo_entrada, get_registo_entrada_id, remove_registo_entrada,inserir_cliente, get_cliente_id, editar_cliente, apagar_cliente, inserir_restauro, get_restauro_id, editar_restauro, remove_restauro, export_xml, export_json
import mongomock
from unittest import TestCase

class PostgreSQLDatabaseTestCase(TestCase):

    def setUp(self):
        # Setup inicial para testar as funções que interagem com o PostgreSQL
        self.veiculo_id = 'ABC123'
        self.data_entrada = '2024-09-01'
        self.observacoes = 'Primeira entrada de teste'
        
        # Inserir um registo para testar
        inserir_registo_entrada(self.veiculo_id, self.data_entrada, self.observacoes)

    def test_inserir_registo_entrada(self):
        """Testar se o registo de entrada foi inserido corretamente."""
        registo = get_registo_entrada_id(1)  # Assume que o ID é 1 após inserção
        self.assertIsNotNone(registo)
        self.assertEqual(registo['veiculo_id'], self.veiculo_id)
        self.assertEqual(registo['observacoes'], self.observacoes)

    def test_editar_registo_entrada(self):
        """Testar se o registo de entrada pode ser atualizado corretamente."""
        novo_veiculo_id = 'DEF456'
        novas_observacoes = 'Atualização de teste'
        editar_registo_entrada(1, novo_veiculo_id, self.data_entrada, novas_observacoes)
        
        registo = get_registo_entrada_id(1)
        self.assertEqual(registo['veiculo_id'], novo_veiculo_id)
        self.assertEqual(registo['observacoes'], novas_observacoes)

    def test_remove_registo_entrada(self):
        """Testar se o registo de entrada pode ser removido corretamente."""
        remove_registo_entrada(1)
        registo = get_registo_entrada_id(1)
        self.assertIsNone(registo)
class RestaurosDatabaseTestCase(TestCase):

    def setUp(self):
        # Setup inicial para testar as funções de restauros
        self.veiculo_id = 'ABC123'
        self.data_inicio = '2024-09-01'
        self.data_fim = '2024-09-05'
        self.status = 'Em progresso'
        
        # Inserir um restauro
        inserir_restauro(self.veiculo_id, self.data_inicio, self.data_fim, self.status)

    def test_inserir_restauro(self):
        """Testar se o restauro foi inserido corretamente."""
        restauro = get_restauro_id(1)  # Assume que o ID é 1 após inserção
        self.assertIsNotNone(restauro)
        self.assertEqual(restauro['veiculo_id'], self.veiculo_id)
        self.assertEqual(restauro['status'], self.status)

    def test_editar_restauro(self):
        """Testar se o restauro pode ser atualizado corretamente."""
        novo_status = 'Concluído'
        editar_restauro(1, self.veiculo_id, self.data_inicio, self.data_fim, novo_status)
        
        restauro = get_restauro_id(1)
        self.assertEqual(restauro['status'], novo_status)

    def test_remover_restauro(self):
        """Testar se o restauro pode ser removido corretamente."""
        remove_restauro(1)
        restauro = get_restauro_id(1)
        self.assertIsNone(restauro)

class MongoDBTestCase(TestCase):

    def setUp(self):
        # Mock da conexão MongoDB
        self.mongo_client = mongomock.MongoClient()
        self.db = self.mongo_client['mytestdb']
        self.cliente_id = inserir_cliente(
            nome="João Silva",
            endereco="Rua 123",
            telefone="912345678",
            email="joao.silva@example.com"
        )

    def test_inserir_cliente(self):
        """Testar se o cliente foi inserido corretamente no MongoDB."""
        cliente = get_cliente_id(self.cliente_id)
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente['nome'], "João Silva")
        self.assertEqual(cliente['email'], "joao.silva@example.com")

    def test_editar_cliente(self):
        """Testar se o cliente pode ser editado no MongoDB."""
        editar_cliente(self.cliente_id, nome="João Silva Jr.", telefone="987654321")
        cliente = get_cliente_id(self.cliente_id)
        self.assertEqual(cliente['nome'], "João Silva Jr.")
        self.assertEqual(cliente['telefone'], "987654321")

    def test_apagar_cliente(self):
        """Testar se o cliente pode ser apagado do MongoDB."""
        apagar_cliente(self.cliente_id)
        cliente = get_cliente_id(self.cliente_id)
        self.assertIsNone(cliente)
lass ExportTestCase(TestCase):

    def test_export_xml(self):
        """Testar a exportação de dados em formato XML."""
        xml_data = export_xml()
        self.assertIsNotNone(xml_data)

    def test_export_json(self):
        """Testar a exportação de dados em formato JSON."""
        json_data = export_json()
        self.assertIsNotNone(json_data)