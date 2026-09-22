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
# FATOR DE PORTE (item 6.2.1 da memória) -- PROXY PROVISÓRIO DA STG
#
# A memória técnica do cliente define a curva de porte pela QUANTIDADE DE
# VIDAS do grupo segurado (F_porte = 1 + 50% × (F_porte_observado − 1)),
# mas os anexos recebidos trazem só a fórmula -- não a tabela de faixas de
# vidas × relatividade observada na amostra de mercado.
#
# Enquanto essa tabela não chega, a STG decidiu usar como proxy provisório
# o PORTE FISCAL da empresa (Receita Federal, já disponível na consulta de
# CNPJ). Os fatores abaixo são julgamento de negócio da STG (revisados em
# 22/09/2026), não uma exigência da memória técnica -- devem ser
# substituídos pela curva de porte por vidas assim que o cliente enviar a
# tabela real, e permanecem pendentes de validação atuarial até lá.
#
# Código do porte fiscal (Receita Federal / BrasilAPI, campo
# "codigo_porte"), com a faixa de faturamento anual bruto que define cada
# classificação (Lei Complementar 123/2006 -- Estatuto Nacional da
# Microempresa e da Empresa de Pequeno Porte):
#   00 Não informado         -- sem faixa (dado ausente no cadastro)
#   01 Microempresa (ME)     -- até R$ 360 mil
#   03 Empresa de Pequeno Porte (EPP) -- R$ 360 mil a R$ 4,8 milhões
#   05 Demais                -- acima de R$ 4,8 milhões (ou entidade que
#                                não se enquadra em ME/EPP: órgão público,
#                                sem fins lucrativos, etc.)
# =====================================================
FATORES_PORTE_FISCAL = {
    0: {"nome": "Não informado", "faturamento_anual": None, "fator": 1.00},
    1: {"nome": "Microempresa (ME)", "faturamento_anual": "até R$ 360 mil", "fator": 1.05},
    3: {"nome": "Empresa de Pequeno Porte (EPP)", "faturamento_anual": "R$ 360 mil a R$ 4,8 milhões", "fator": 1.04},
    5: {"nome": "Demais", "faturamento_anual": "acima de R$ 4,8 milhões", "fator": 1.05},
}


def fator_porte(codigo_porte):
    """Fator de porte aplicado à apólice (item 6.2.1 da memória) -- proxy
    provisório da STG baseado no porte fiscal da Receita Federal, até o
    cliente enviar a curva de porte por quantidade de vidas. Código não
    reconhecido, ausente ou None: fator neutro (1,0)."""
    try:
        codigo = int(codigo_porte)
    except (TypeError, ValueError):
        return 1.0
    entrada = FATORES_PORTE_FISCAL.get(codigo)
    return entrada["fator"] if entrada else 1.0


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
