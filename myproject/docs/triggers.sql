-- Novo Trigger para atualização
CREATE OR REPLACE TRIGGER trg_calcular_custo_total_update
BEFORE UPDATE ON tarefas_restauro
FOR EACH ROW
EXECUTE FUNCTION calcular_custo_total();


-- Trigger que dispara ao atualizar o status para 'Concluído'
CREATE TRIGGER trg_criar_faturacao
BEFORE UPDATE ON restauros
FOR EACH ROW
WHEN (OLD.status = 'Em processamento' AND NEW.status = 'Concluído')
EXECUTE FUNCTION criar_faturacao();


-- Trigger que chama a função ao inserir uma nova linha nas tarefas_restauro
CREATE OR REPLACE TRIGGER trg_calcular_custo_total
BEFORE INSERT ON tarefas_restauro
FOR EACH ROW
EXECUTE FUNCTION calcular_custo_total();



-- Cria o trigger que chama a função antes de atualizar a tabela
CREATE TRIGGER trigger_update_data_fim
BEFORE UPDATE ON restauros
FOR EACH ROW
EXECUTE FUNCTION update_data_fim();



-- 2. Criar o trigger que chama a função após uma atualização na tabela faturacao
CREATE TRIGGER after_update_faturacao
AFTER UPDATE ON faturacao
FOR EACH ROW
WHEN (OLD.status_pagamento IS DISTINCT FROM NEW.status_pagamento)
EXECUTE FUNCTION create_saida_veiculo();

