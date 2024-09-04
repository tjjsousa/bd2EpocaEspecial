INSERT INTO registo_entradas (veiculo_id, data_entrada, observacoes)
VALUES 
('ABC1234', '2024-09-01', 'Sem observações no momento.'),
('XYZ5678', '2024-09-02', 'Problemas no motor.'),
('DEF9101', '2024-09-03', 'Necessário pintura e troca de óleo.');



INSERT INTO restauros (veiculo_id, data_inicio, data_fim, status)
VALUES 
('ABC1234', '2024-09-01', '2024-09-10', 'Finalizado'),
('XYZ5678', '2024-09-02', NULL, 'Em Progresso'),
('DEF9101', '2024-09-03', '2024-09-08', 'Finalizado');



INSERT INTO tarefas_restauro (restauro_id, descricao, mao_obra, custo_total, tempo)
VALUES 
(1, 'Troca de óleo', 'Mecânico', 120.00, 2.0),
(1, 'Pintura completa', 'Pintor', 450.00, 8.0),
(2, 'Revisão elétrica', 'Eletricista', 300.00, 3.5);




INSERT INTO faturacao (restauro_id, data_emissao, valor_total, itens, status_pagamento)
VALUES 
(1, '2024-09-12', 570.00, 'Troca de óleo, Pintura completa', 'Pago'),
(2, '2024-09-15', 300.00, 'Revisão elétrica', 'Pendente'),
(3, '2024-09-10', 200.00, 'Troca de pneus', 'Pago');



INSERT INTO faturacao (restauro_id, data_emissao, valor_total, itens, status_pagamento)
VALUES 
(1, '2024-09-12', 570.00, 'Troca de óleo, Pintura completa', 'Pago'),
(2, '2024-09-15', 300.00, 'Revisão elétrica', 'Pendente'),
(3, '2024-09-10', 200.00, 'Troca de pneus', 'Pago');



INSERT INTO saidas_veiculos (veiculo_id, data_saida, condicoes_saida, observacoes)
VALUES 
('ABC1234', '2024-09-12', 'Veículo em perfeito estado', 'Cliente satisfeito.'),
('XYZ5678', '2024-09-15', 'Pendências elétricas', 'Retorno agendado.'),
('DEF9101', '2024-09-10', 'Revisado e pronto', 'Sem observações adicionais.');



INSERT INTO tipos_mao_obra (descricao, custo_por_hora)
VALUES 
('Mecânico', 50.00),
('Pintor', 45.00),
('Eletricista', 60.00),
('Lavagem', 25.00);
