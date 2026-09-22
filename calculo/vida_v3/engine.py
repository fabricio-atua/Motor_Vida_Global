# Motor V3 — Vida em Grupo Capital Global
# Cadeia de cálculo conforme a memória técnica do cliente, item 6.8
# ("Sequência consolidada da formulação do simulador"):
#
#   taxa técnica ativa -> fatores de risco (CNAE, porte, capital só em
#   Morte) -> prêmio de risco por vida -> aquisição/retenção -> prêmio
#   comercial sem IOF -> prêmio final (com IOF) -> parcelamento em 12x.
#
# A cadeia é calculada POR VIDA e arredondada a 2 casas em cada passo (mesmo
# princípio do motor V4 anterior) para que os totais do grupo batam
# exatamente com "valor por vida × vidas", sem sobra de centavos.

from calculo.vida_v3 import parametros as p
from calculo.vida_v3 import taxas as t


def premio_risco_cobertura_por_vida(capital_individual, cobertura, segmento, fator_cnae, fator_porte):
    """Prêmio de risco anual por vida de uma cobertura sobre capital (item
    6.8.7). Retorna None se a cobertura não tiver taxa ativa para o
    segmento. O fator de capital (concentração) só incide em MORTE.

    A taxa técnica é calculada AO VIVO a partir da taxa pura (item 6.1 da
    memória: t_tec = t_pura × (1+IBNR) × (1+θ)), não apenas lida de uma
    constante já pronta -- ver taxas.py para de onde vem a taxa pura.

    Devolve também "passos_fatores": o passo a passo (Taxa Pura -> IBNR +
    Oscilação -> Taxa Técnica -> Fator CNAE -> Fator de Porte -> Fator de
    Capital) para exibição no depurador, arredondado a 2 casas em cada
    passo -- mesmo princípio da cadeia comercial, para "premio" bater
    exatamente com o último passo exibido."""
    taxa_pura = t.taxa_pura_ativa(cobertura, segmento)
    if taxa_pura is None:
        return None

    if cobertura == "MORTE":
        fator_capital, subscricao_obrigatoria = p.fator_capital_morte(segmento, capital_individual)
    else:
        fator_capital, subscricao_obrigatoria = 1.0, False

    passos_fatores = []

    valor = round(capital_individual * taxa_pura, 2)
    passos_fatores.append({"label": "Taxa Pura × Capital", "fator": None, "valor": valor})

    valor = round(valor * t.FATOR_PROTECAO_CAPITAL, 2)
    passos_fatores.append({"label": "↳ IBNR (15%) + Oscilação (5%)", "fator": t.FATOR_PROTECAO_CAPITAL, "valor": valor})
    passos_fatores.append({"label": "Taxa Técnica × Capital", "fator": None, "valor": valor, "destaque": True})

    valor = round(valor * fator_cnae, 2)
    passos_fatores.append({"label": "↳ Fator CNAE", "fator": fator_cnae, "valor": valor})

    valor = round(valor * fator_porte, 2)
    passos_fatores.append({"label": "↳ Fator de Porte", "fator": fator_porte, "valor": valor})

    if cobertura == "MORTE":
        valor = round(valor * fator_capital, 2)
        passos_fatores.append({"label": "↳ Fator de Capital Segurado", "fator": fator_capital, "valor": valor})

    taxa_tecnica = t.taxa_ativa(cobertura, segmento)

    return {
        "premio": valor,
        "taxa": taxa_tecnica,
        "fator_capital": fator_capital,
        "subscricao_obrigatoria": subscricao_obrigatoria,
        "passos_fatores": passos_fatores,
    }


def premio_risco_funeral_por_vida(modalidade, limite):
    """Prêmio de risco anual por vida do Funeral: taxa técnica fixa em
    R$/vida (calculada ao vivo a partir da taxa pura, item 6.1), sem
    nenhum carregamento adicional (nem Fator CNAE, nem Fator de Porte).

    ATENÇÃO: os itens 6.3 e 6.8.6 da memória técnica do cliente definem
    PR_funeral = N × taxa_funeral × F_porte -- ou seja, o Fator de Porte
    FAZ parte da fórmula oficial do Funeral lá (só o Fator CNAE é excluído
    explicitamente). A STG decidiu não aplicar esse nem nenhum outro
    carregamento adicional ao Funeral, divergindo desses itens por opção
    de negócio -- não é uma leitura literal da memória técnica.

    Retorna None se não houver taxa para a modalidade/limite."""
    taxa_pura = t.taxa_funeral_pura(modalidade, limite)
    if taxa_pura is None:
        return None

    passos_fatores = []

    valor = round(taxa_pura, 2)
    passos_fatores.append({"label": "Taxa Pura Funeral (R$/vida)", "fator": None, "valor": valor})

    valor = round(valor * t.FATOR_PROTECAO_FUNERAL, 2)
    passos_fatores.append({"label": "↳ IBNR (0%) + Oscilação (5%)", "fator": t.FATOR_PROTECAO_FUNERAL, "valor": valor})
    passos_fatores.append({"label": "Taxa Técnica Funeral (R$/vida)", "fator": None, "valor": valor, "destaque": True})

    taxa_tecnica = t.taxa_funeral(modalidade, limite)

    return {"premio": valor, "taxa": taxa_tecnica, "passos_fatores": passos_fatores}


def custo_aquisicao_anual(parcelas_agenciamento, comissao_pct):
    return p.custo_aquisicao_anual(parcelas_agenciamento, comissao_pct)


def retencao_tarifaria(aquisicao_anual):
    """Retenção = 1 − Aquisição − Despesa Administrativa − Margem − PIS/COFINS
    (item 6.5 da memória técnica)."""
    return 1 - aquisicao_anual - p.DESPESA_ADMINISTRATIVA - p.MARGEM - p.PIS_COFINS


def cadeia_unitaria(premio_risco_puro, retencao, parcelas_agenciamento=None, comissao_pct=None):
    """Aplica a formação comercial (item 6.5/6.8.8-6.8.10) a um prêmio de
    risco por vida já calculado (capital × taxa × fatores), devolvendo o
    passo a passo até o prêmio final. Cada passo é arredondado a 2 casas,
    igual à cadeia do motor V4, para os totais do grupo baterem exatamente.

    Se parcelas_agenciamento/comissao_pct forem informados, inclui também
    (item 6.4) o detalhamento em R$ de quanto do prêmio comercial vai para
    Agenciamento (a/12) e para Comissão (c×(12−a)/12) -- informativo, não
    altera a retenção já aplicada acima."""
    passos = []

    valor_risco = round(premio_risco_puro, 2)
    passos.append({"label": "Prêmio de Risco", "fator": None, "valor": valor_risco, "destaque": True})

    fator_retencao = 1 / retencao
    valor_comercial = round(valor_risco * fator_retencao, 2)
    passos.append({"label": "↳ Retenção (aquisição + adm. + margem + PIS/COFINS)", "fator": fator_retencao, "valor": valor_comercial})

    if parcelas_agenciamento is not None and comissao_pct is not None:
        agenciamento_pct = parcelas_agenciamento / p.N_PARCELAS
        comissao_efetiva_pct = comissao_pct * (p.N_PARCELAS - parcelas_agenciamento) / p.N_PARCELAS

        valor_agenciamento = round(valor_comercial * agenciamento_pct, 2)
        passos.append({"label": "↳ Agenciamento (a/12)", "fator": agenciamento_pct, "valor": valor_agenciamento})

        valor_comissao = round(valor_comercial * comissao_efetiva_pct, 2)
        passos.append({"label": "↳ Comissão (c×(12−a)/12)", "fator": comissao_efetiva_pct, "valor": valor_comissao})

    passos.append({"label": "Prêmio Comercial sem IOF", "fator": None, "valor": valor_comercial, "destaque": True})

    fator_iof = 1 + p.IOF
    valor_final = round(valor_comercial * fator_iof, 2)
    passos.append({"label": "↳ IOF", "fator": fator_iof, "valor": valor_final})
    passos.append({"label": "Prêmio Final", "fator": None, "valor": valor_final, "destaque": True})

    return passos, valor_risco, valor_comercial, valor_final
