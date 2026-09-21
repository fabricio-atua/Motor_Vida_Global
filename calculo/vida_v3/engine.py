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
from calculo.vida_v3.taxas import taxa_ativa, taxa_funeral


def premio_risco_cobertura_por_vida(capital_individual, cobertura, segmento, fator_cnae, fator_porte):
    """Prêmio de risco anual por vida de uma cobertura sobre capital (item
    6.8.7). Retorna None se a cobertura não tiver taxa ativa para o
    segmento. O fator de capital (concentração) só incide em MORTE."""
    taxa = taxa_ativa(cobertura, segmento)
    if taxa is None:
        return None

    if cobertura == "MORTE":
        fator_capital, subscricao_obrigatoria = p.fator_capital_morte(segmento, capital_individual)
    else:
        fator_capital, subscricao_obrigatoria = 1.0, False

    premio = capital_individual * taxa * fator_cnae * fator_porte * fator_capital
    return {
        "premio": premio,
        "taxa": taxa,
        "fator_capital": fator_capital,
        "subscricao_obrigatoria": subscricao_obrigatoria,
    }


def premio_risco_funeral_por_vida(modalidade, limite, fator_porte):
    """Prêmio de risco anual por vida do Funeral (item 6.3/6.8.6): R$/vida,
    sem fator CNAE (só fator de porte). Retorna None se não houver taxa
    para a modalidade/limite."""
    taxa = taxa_funeral(modalidade, limite)
    if taxa is None:
        return None

    return {"premio": taxa * fator_porte, "taxa": taxa}


def custo_aquisicao_anual(parcelas_agenciamento, comissao_pct):
    return p.custo_aquisicao_anual(parcelas_agenciamento, comissao_pct)


def retencao_tarifaria(aquisicao_anual):
    """Retenção = 1 − Aquisição − Despesa Administrativa − Margem − PIS/COFINS
    (item 6.5 da memória técnica)."""
    return 1 - aquisicao_anual - p.DESPESA_ADMINISTRATIVA - p.MARGEM - p.PIS_COFINS


def cadeia_unitaria(premio_risco_puro, retencao):
    """Aplica a formação comercial (item 6.5/6.8.8-6.8.10) a um prêmio de
    risco por vida já calculado (capital × taxa × fatores), devolvendo o
    passo a passo até o prêmio final. Cada passo é arredondado a 2 casas,
    igual à cadeia do motor V4, para os totais do grupo baterem exatamente."""
    passos = []

    valor_risco = round(premio_risco_puro, 2)
    passos.append({"label": "Prêmio de Risco", "fator": None, "valor": valor_risco, "destaque": True})

    fator_retencao = 1 / retencao
    valor_comercial = round(valor_risco * fator_retencao, 2)
    passos.append({"label": "↳ Retenção (aquisição + adm. + margem + PIS/COFINS)", "fator": fator_retencao, "valor": valor_comercial})
    passos.append({"label": "Prêmio Comercial sem IOF", "fator": None, "valor": valor_comercial, "destaque": True})

    fator_iof = 1 + p.IOF
    valor_final = round(valor_comercial * fator_iof, 2)
    passos.append({"label": "↳ IOF", "fator": fator_iof, "valor": valor_final})
    passos.append({"label": "Prêmio Final", "fator": None, "valor": valor_final, "destaque": True})

    return passos, valor_risco, valor_comercial, valor_final
