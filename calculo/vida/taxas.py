TAXAS = {
    "MORTE": 0.000082,
    "IEA"  : 0.000025,
    "IPA"  : 0.000038,
    "IPTA" : 0.000018,
    "IPDF" : 0.000037,
    "IPDL" : 0.000037,
    "AF"   : 0.000082,
    "DMHO" : 0.002224,
    "DMH"  : 0.002224
}


DESCRICOES = {
    "MORTE" : "Morte",
    "IEA"   : "IEA - Indenização Especial por Morte Acidental",
    "IPA"   : "IPA - Invalidez Permanente Total ou Parcial por Acidente",
    "IPTA"  : "IPTA - Invalidez Permanente Total por Acidente",
    "IPDF"  : "IPDF - Invalidez Permanente Total por Doença Funcional",
    "IPDL"  : "IPDL - Invalidez Permanente Total por Doença Laborativa",
    "AF"    : "AF - Auxílio Funeral",
    "DMHO"  : "DMHO - Despesas Médicas Hospitalares e Odontológicas",
    "DMH"   : "DMH - Despesas Médicas Hospitalares"
}


# =====================================================
# TABELA DE COMISSIONAMENTO / AGENCIAMENTO
# Fonte: Tabelas/Tabela_exemplo_corretor.jpeg
# Coeficiente multiplica o Prêmio Puro para chegar no Prêmio Comercial
# Ordenada por classe de corretor (A, B, C); dentro de cada classe, por faixa de comissão
# =====================================================
TABELA_COMISSIONAMENTO = {
    # Classe A - sem agenciamento antecipado
    "1-A":  {"corretagem": 0.01, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 0.73810},
    "10-A": {"corretagem": 0.10, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 0.84286},
    "15-A": {"corretagem": 0.15, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 0.91429},
    "20-A": {"corretagem": 0.20, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 1.00000},
    "25-A": {"corretagem": 0.25, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 1.10000},
    "30-A": {"corretagem": 0.30, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 1.22857},
    "35-A": {"corretagem": 0.35, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 1.38571},
    "40-A": {"corretagem": 0.40, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 1.59524},
    "45-A": {"corretagem": 0.45, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 1.87619},
    "50-A": {"corretagem": 0.50, "ag_1_mes": 0.00, "ag_2_mes": 0.00, "coeficiente": 2.27143},

    # Classe B - agenciamento de 100% no 1º mês
    "10-B": {"corretagem": 0.10, "ag_1_mes": 1.00, "ag_2_mes": 0.00, "coeficiente": 0.95238},
    "15-B": {"corretagem": 0.15, "ag_1_mes": 1.00, "ag_2_mes": 0.00, "coeficiente": 1.03810},
    "20-B": {"corretagem": 0.20, "ag_1_mes": 1.00, "ag_2_mes": 0.00, "coeficiente": 1.14286},
    "25-B": {"corretagem": 0.25, "ag_1_mes": 1.00, "ag_2_mes": 0.00, "coeficiente": 1.26667},
    "30-B": {"corretagem": 0.30, "ag_1_mes": 1.00, "ag_2_mes": 0.00, "coeficiente": 1.41905},
    "35-B": {"corretagem": 0.35, "ag_1_mes": 1.00, "ag_2_mes": 0.00, "coeficiente": 1.61429},
    "40-B": {"corretagem": 0.40, "ag_1_mes": 1.00, "ag_2_mes": 0.00, "coeficiente": 1.87619},
    "45-B": {"corretagem": 0.45, "ag_1_mes": 1.00, "ag_2_mes": 0.00, "coeficiente": 2.23333},

    # Classe C - agenciamento de 100% no 1º e 2º mês
    "10-C": {"corretagem": 0.10, "ag_1_mes": 1.00, "ag_2_mes": 1.00, "coeficiente": 1.10000},
    "15-C": {"corretagem": 0.15, "ag_1_mes": 1.00, "ag_2_mes": 1.00, "coeficiente": 1.20476},
    "20-C": {"corretagem": 0.20, "ag_1_mes": 1.00, "ag_2_mes": 1.00, "coeficiente": 1.32857},
    "25-C": {"corretagem": 0.25, "ag_1_mes": 1.00, "ag_2_mes": 1.00, "coeficiente": 1.48571},
    "30-C": {"corretagem": 0.30, "ag_1_mes": 1.00, "ag_2_mes": 1.00, "coeficiente": 1.67619},
    "35-C": {"corretagem": 0.35, "ag_1_mes": 1.00, "ag_2_mes": 1.00, "coeficiente": 1.92857},
}


# =====================================================
# FAIXAS DE COMISSÃO
# Cada faixa cobre até o percentual "nominal" da tabela acima;
# o corretor digita a comissão livremente (0,01% a 50,00%) e a
# faixa correspondente determina qual linha da tabela usar.
# =====================================================
FAIXAS_COMISSAO = [
    (0.0001, 0.0100, "1"),
    (0.0101, 0.1000, "10"),
    (0.1001, 0.1500, "15"),
    (0.1501, 0.2000, "20"),
    (0.2001, 0.2500, "25"),
    (0.2501, 0.3000, "30"),
    (0.3001, 0.3500, "35"),
    (0.3501, 0.4000, "40"),
    (0.4001, 0.4500, "45"),
    (0.4501, 0.5000, "50"),
]


def faixa_comissao(comissao_pct):
    for minimo, maximo, tier in FAIXAS_COMISSAO:
        if minimo <= comissao_pct <= maximo:
            return tier
    return None


# O agravo/desconto por CNAE agora é calculado em calculo/vida/cnae.py,
# lendo a coluna "coeficiente" (derivada da classificação de risco por
# Grupo CNAE) em Tabelas/tabela_cnae_completa_VG.xlsx.


# =====================================================
# CARREGAMENTOS DO PRÊMIO COMERCIAL (VIDA GLOBAL)
# Aplicados em sequência sobre o Prêmio Comercial para chegar no Prêmio Final.
# =====================================================
CARREGAMENTOS = {
    "Despesas Operacionais":    1.0200,
    "Despesas Administrativas": 1.0500,
    "Impostos":                 1.0465,
    "Lucro":                    1.0500,
    "IOF":                      1.0380,
}