
-- =====================================================
-- CRM ANALYTICS
-- Indicadores comerciais com SQL
-- =====================================================

-- 1. VISÃO GERAL DO PIPELINE
SELECT
    COUNT(*) AS quantidade_negocios,
    ROUND(SUM(montante), 2) AS valor_total_pipeline,
    ROUND(AVG(montante), 2) AS ticket_medio,
    ROUND(MIN(montante), 2) AS menor_negocio,
    ROUND(MAX(montante), 2) AS maior_negocio
FROM negocios;


-- 2. QUANTIDADE E VALOR POR ESTÁGIO
SELECT
    estagio,
    COUNT(*) AS quantidade_negocios,
    ROUND(SUM(montante), 2) AS valor_total,
    ROUND(AVG(montante), 2) AS ticket_medio
FROM negocios
GROUP BY estagio
ORDER BY valor_total DESC;


-- 3. RANKING DOS NEGÓCIOS POR VALOR
SELECT
    nome_negocio,
    montante,
    estagio,
    data_fechamento,
    RANK() OVER (
        ORDER BY montante DESC
    ) AS ranking_valor
FROM negocios
ORDER BY montante DESC;


-- 4. NEGÓCIOS COM FECHAMENTO PREVISTO
SELECT
    nome_negocio,
    montante,
    estagio,
    data_fechamento
FROM negocios
WHERE data_fechamento >= DATE('now')
ORDER BY data_fechamento ASC;


-- 5. PARTICIPAÇÃO DE CADA NEGÓCIO NO PIPELINE
SELECT
    nome_negocio,
    montante,
    ROUND(
        100.0 * montante /
        NULLIF((SELECT SUM(montante) FROM negocios), 0),
        2
    ) AS percentual_pipeline
FROM negocios
ORDER BY percentual_pipeline DESC;


-- 6. CLASSIFICAÇÃO DOS NEGÓCIOS POR VALOR
SELECT
    nome_negocio,
    montante,
    CASE
        WHEN montante >= 7000 THEN 'Alto valor'
        WHEN montante >= 4000 THEN 'Médio valor'
        ELSE 'Baixo valor'
    END AS categoria_valor
FROM negocios
ORDER BY montante DESC;
