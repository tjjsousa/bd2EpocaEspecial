CREATE TABLE registo_entradas (
    id SERIAL PRIMARY KEY,
    veiculo_id VARCHAR(255) NOT NULL,
    data_entrada DATE NOT NULL,
    observacoes TEXT
);

CREATE TABLE restauros (
    id SERIAL PRIMARY KEY,
    veiculo_id VARCHAR(255) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    status VARCHAR(255)
);

CREATE TABLE tipos_mao_obra (
    id SERIAL PRIMARY KEY,
    descricao VARCHAR(255) NOT NULL,
    custo_por_hora DECIMAL(10, 2) NOT NULL
);

CREATE TABLE tarefas_restauro (
    id SERIAL PRIMARY KEY,
    restauro_id integer REFERENCES restauros (id),
    descricao TEXT NOT NULL,
    mao_obra integer REFERENCES tipos_mao_obra (id),
    custo_total DECIMAL(10, 2) NOT NULL,
    tempo NUMERIC(5, 2)
);

CREATE TABLE faturacao (
    id SERIAL PRIMARY KEY,
    restauro_id  integer REFERENCES restauros (id),
    data_emissao DATE NOT NULL,
    valor_total DECIMAL(10, 2) NOT NULL,
    itens TEXT,
    status_pagamento VARCHAR(255)
);

CREATE TABLE saidas_veiculos (
    id SERIAL PRIMARY KEY,
    veiculo_id VARCHAR(255) NOT NULL,
    data_saida DATE NOT NULL,
    condicoes_saida TEXT,
    observacoes TEXT
);