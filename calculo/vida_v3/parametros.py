# Motor V3 — Vida em Grupo Capital Global
# Parâmetros de precificação (fatores de risco, aquisição, carregamentos e
# tributos) conforme a memória técnica do cliente (item 6 do documento).

# =====================================================
# FATOR DE CONCENTRAÇÃO DE CAPITAL (item 6.8.5) — incide SOMENTE em MORTE.
# Faixas de capital individual contratado, por segmento.
# (min, max, fator, subscrição_obrigatória)
# =====================================================
FAIXAS_CAPITAL_MORTE = {
    "FUNC": [
        (0,          30_000,       1.00, False),
        (30_000.01,  60_000,       1.04, False),
        (60_000.01,  90_000,       1.05, False),
        (90_000.01,  150_000,      1.07, False),
        (150_000.01, float("inf"), 1.07, True),
    ],
    "SOCIO": [
        (0,          100_000,      1.00, False),
        (100_000.01, 200_000,      1.04, False),
        (200_000.01, 250_000,      1.05, False),
        (250_000.01, float("inf"), 1.05, True),
    ],
}


def fator_capital_morte(segmento, capital_individual):
    """Retorna (fator, subscricao_obrigatoria) para a faixa de capital
    individual do segmento informado. O fator só se aplica à cobertura de
    Morte (item 6.2/6.8.5 da memória técnica)."""
    faixas = FAIXAS_CAPITAL_MORTE[segmento]
    for minimo, maximo, fator, subscricao_obrigatoria in faixas:
        if minimo <= capital_individual <= maximo:
            return fator, subscricao_obrigatoria
    ultima = faixas[-1]
    return ultima[2], ultima[3]


# =====================================================
# FATOR DE PORTE (item 6.2.1 da memória)
# F_porte = 1 + λ × (F_porte_observado − 1)
#
# λ = 50% é premissa prudencial de LANÇAMENTO, não depende de dado do
# cliente -- a própria memória diz: "a incorporação de 50% é uma premissa
# prudencial de lançamento, sujeita à substituição por estudo de
# experiência própria".
#
# F_porte_observado vem da relatividade observada em amostra DE MERCADO
# para a faixa de vidas do grupo (não da experiência própria da
# seguradora, que é nova e não tem emissões) -- a tabela de faixas de
# vidas × relatividade ainda não foi enviada pelo cliente. Enquanto isso,
# o motor usa a referência neutra que a própria memória define
# (F_porte_observado = 1,0000), o que resulta em F_porte = 1,0 sem
# inventar dado de mercado.
#
# O motor chegou a usar como proxy provisório o PORTE FISCAL da empresa
# (Receita Federal), mas isso nunca foi pedido pelo cliente -- é uma
# classificação de faturamento (Lei Complementar 123/2006), sem relação
# com a curva por quantidade de vidas da memória técnica. Removido em
# 22/09/2026.
#
# Tabela antiga preservada só de referência (não é mais aplicada):
#   00 Não informado                  -- fator 1,00
#   01 Microempresa (ME)              -- fator 1,02 (até R$ 360 mil)
#   03 Empresa de Pequeno Porte (EPP) -- fator 1,03 (R$ 360 mil a R$ 4,8 mi)
#   05 Demais                         -- fator 1,04 (acima de R$ 4,8 mi)
#
# DESVIO INTENCIONAL: a memória define F_porte como um fator único "do
# grupo" (quantidade de vidas total, Funcionários + Sócios), não por
# segmento. A STG decidiu separar por segmento (FUNC/SOCIO) para ficar
# consistente com o resto do motor (taxa técnica e Fator de Capital já
# são por segmento) -- decisão de negócio a validar com o cliente.
# =====================================================
LAMBDA_PORTE = 0.5              # λ -- premissa prudencial de lançamento (item 6.2.1)
F_PORTE_OBSERVADO_NEUTRO = 1.0  # referência neutra definida pela própria memória

# Faixas de quantidade de vidas x F_porte_observado, por segmento.
# PLACEHOLDER: nem as faixas nem os fatores vieram do cliente -- é só a
# estrutura pronta para quando a tabela real de relatividade de mercado
# chegar. Até lá, toda faixa fica neutra (F_porte_observado = 1,0).
# (min_vidas, max_vidas, F_porte_observado)
FAIXAS_PORTE_OBSERVADO = {
    "FUNC": [
        (0, float("inf"), F_PORTE_OBSERVADO_NEUTRO),  # TODO: faixas e fatores reais pendentes do cliente
    ],
    "SOCIO": [
        (0, float("inf"), F_PORTE_OBSERVADO_NEUTRO),  # TODO: faixas e fatores reais pendentes do cliente
    ],
}


def f_porte_observado(segmento, quantidade_vidas):
    """Retorna o F_porte_observado da faixa de quantidade de vidas do
    segmento (item 6.2.1 da memória, com a ressalva de segmentação acima).
    Estrutura pronta para quando o cliente enviar a tabela real; hoje toda
    faixa é neutra (1,0)."""
    faixas = FAIXAS_PORTE_OBSERVADO[segmento]
    for minimo, maximo, fator in faixas:
        if minimo <= quantidade_vidas <= maximo:
            return fator
    return F_PORTE_OBSERVADO_NEUTRO


def fator_porte(segmento, quantidade_vidas):
    """F_porte = 1 + λ × (F_porte_observado − 1) (item 6.2.1 da memória).
    Sem a tabela de faixas de vidas × relatividade de mercado do cliente,
    usa a referência neutra que a própria memória define
    (F_porte_observado = 1,0000), resultando em F_porte = 1,0. Quando o
    cliente enviar a tabela, basta preencher FAIXAS_PORTE_OBSERVADO -- a
    fórmula já está pronta."""
    observado = f_porte_observado(segmento, quantidade_vidas)
    return 1 + LAMBDA_PORTE * (observado - 1)


# =====================================================
# AQUISIÇÃO — Agenciamento + Comissão (item 6.4 da memória)
# A = a/12 + c × (12 − a)/12
#   a = parcelas integrais de agenciamento: 0 (0%), 1 (100%) ou 2 (200%)
#   c = comissão, limitada a 0%-35%, incide só nas parcelas após o
#       agenciamento (sem comissão nas parcelas de agenciamento)
# =====================================================
COMISSAO_MINIMA = 0.00
COMISSAO_MAXIMA = 0.35

PARCELAS_AGENCIAMENTO = {
    "A": 0,  # 0%   — nenhuma parcela destinada integralmente ao corretor
    "B": 1,  # 100% — 1ª parcela sem IOF destinada ao corretor
    "C": 2,  # 200% — 1ª e 2ª parcelas sem IOF destinadas ao corretor
}

DESCRICOES_CLASSE_AGENCIAMENTO = {
    "A": "A — Sem agenciamento antecipado (0%)",
    "B": "B — Agenciamento de 100% (1ª parcela)",
    "C": "C — Agenciamento de 200% (1ª e 2ª parcelas)",
}

N_PARCELAS = 12


def custo_aquisicao_anual(parcelas_agenciamento, comissao_pct):
    """A = a/12 + c×(12−a)/12 (item 6.4 da memória técnica)."""
    a = parcelas_agenciamento
    c = comissao_pct
    return a / N_PARCELAS + c * (N_PARCELAS - a) / N_PARCELAS


# =====================================================
# CARREGAMENTOS E TRIBUTOS (item 6.5 da memória técnica)
# Retenção = 1 − Aquisição − Despesa Administrativa − Margem − PIS/COFINS
# Prêmio comercial sem IOF = Prêmio de risco ÷ Retenção
# Prêmio final = Prêmio comercial sem IOF × (1 + IOF)
#
# O Pró-Labore da NTA original não existe mais nesta fórmula -- o simulador
# do cliente não o utiliza (item 8 da memória: "Excluir a rubrica ou
# definir formalmente sua incorporação em outro carregamento").
# =====================================================
DESPESA_ADMINISTRATIVA = 0.04  # d — despesas administrativas
MARGEM = 0.05                   # M — margem comercial/técnica
PIS_COFINS = 0.0465             # t_PC — PIS/COFINS, aplicado no gross-up
IOF = 0.0038                    # i_IOF — 0,38%, markup só no final (não gross-up)
