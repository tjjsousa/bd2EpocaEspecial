--tarefas restauro view:
CREATE OR REPLACE VIEW tarefas_restauro_view AS (
SELECT tr.id, r.status as restauro_id, tr.descricao, tmo.descricao as mao_obra, tr.custo_total, tr.tempo FROM tarefas_restauro tr
join restauros r ON r.id = tr.restauro_id
join tipos_mao_obra tmo ON tmo.id = tr.mao_obra
);
