-- Função para criar a faturação quando o status muda para "Concluído"
CREATE OR REPLACE FUNCTION criar_faturacao()
RETURNS TRIGGER AS $$
DECLARE
    total_faturacao DECIMAL(10, 2) := 0.0;
    tarefa_record RECORD;
    faturacao_itens TEXT := '';
BEGIN
    -- Verifica se o status passou de 'Em processamento' para 'Concluído'
    IF OLD.status = 'Em processamento' AND NEW.status = 'Concluído' THEN
        -- Cursor para iterar sobre todas as tarefas associadas ao restauro
        FOR tarefa_record IN
            SELECT descricao, custo_total
            FROM tarefas_restauro
            WHERE restauro_id = NEW.id
        LOOP
            -- Soma o custo total de cada tarefa ao valor total da faturação
            total_faturacao := total_faturacao + tarefa_record.custo_total;
            
            -- Adiciona a descrição da tarefa aos itens da faturação
            faturacao_itens := faturacao_itens || tarefa_record.descricao || ': ' || tarefa_record.custo_total || ';\n';
        END LOOP;
        
        -- Insere um novo registro na tabela faturacao
        INSERT INTO faturacao (restauro_id, data_emissao, valor_total, itens, status_pagamento)
        VALUES (NEW.id, CURRENT_DATE, total_faturacao, faturacao_itens, 'Pendente');
    END IF;

    -- Retorna a nova linha (NEW) para a atualização continuar
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Função que será usada pelo trigger
CREATE OR REPLACE FUNCTION calcular_custo_total()
RETURNS TRIGGER AS $$
DECLARE
    custo_hora DECIMAL(10, 2);
BEGIN
    -- Obtém o custo por hora da tabela tipos_mao_obra com base no id da mão de obra
    SELECT custo_por_hora INTO custo_hora 
    FROM tipos_mao_obra 
    WHERE id = NEW.mao_obra;
    
    -- Calcula o custo total (custo por hora * tempo)
    NEW.custo_total := custo_hora * NEW.tempo;

    -- Retorna a nova linha com o custo atualizado
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Cria a função que será chamada pelo trigger
CREATE OR REPLACE FUNCTION update_data_fim()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o status mudou para 'Concluído'
    IF NEW.status = 'Concluído' THEN
        -- Atualiza a data_fim para a data atual
        NEW.data_fim = CURRENT_DATE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- 1. Criar a função que será chamada pelo trigger
CREATE OR REPLACE FUNCTION create_saida_veiculo()
RETURNS TRIGGER AS $$
BEGIN
    -- Verificar se o status_pagamento foi atualizado para "Pago"
    IF NEW.status_pagamento = 'Pago' THEN
        -- Inserir um novo registro na tabela saidas_veiculos
        INSERT INTO saidas_veiculos (veiculo_id, data_saida, condicoes_saida, observacoes)
        VALUES (
            (SELECT veiculo_id FROM restauros WHERE id = NEW.restauro_id),
            CURRENT_DATE,
            'Condições padrão',  
            'Saída gerada automaticamente após pagamento'
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- obter tarefas de restauro json format
CREATE OR REPLACE FUNCTION obter_tarefas_restauro_json()
RETURNS JSON LANGUAGE plpgsql AS $$
BEGIN
    RETURN (
        SELECT json_agg(
            json_build_object(
                'id', t.id,
                'restauro_id', t.restauro_id,
                'descricao', t.descricao,
                'mao_obra', t.mao_obra,
                'custo_total', t.custo_total,
                'tempo', t.tempo
            )
        )
        FROM tarefas_restauro t
    );
END $$;

-- obter tarefas de restauro xml format
CREATE OR REPLACE FUNCTION obter_tarefas_restauro_xml()
RETURNS TEXT LANGUAGE plpgsql AS $$
BEGIN
    RETURN (
        SELECT XMLSERIALIZE(
            CONTENT 
            XMLELEMENT(
                NAME "tarefas",
                XMLAGG(
                    XMLELEMENT(
                        NAME "tarefa",
                        XMLELEMENT(NAME "id", t.id),
                        XMLELEMENT(NAME "restauro_id", t.restauro_id),
                        XMLELEMENT(NAME "descricao", t.descricao),
                        XMLELEMENT(NAME "mao_obra", t.mao_obra),
                        XMLELEMENT(NAME "custo_total", t.custo_total),
                        XMLELEMENT(NAME "tempo", t.tempo)
                    )
                )
            ) AS TEXT
        )
        FROM tarefas_restauro t
    );
END $$;