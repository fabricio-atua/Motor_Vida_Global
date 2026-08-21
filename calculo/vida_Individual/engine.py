from calculo.vida_Individual.taxas import TAXAS

FATOR_CAPITAL = {
    "M"    : 1.0, # Multiplicador para cobertura de Morte - Básica
    "IPA"  : 1.0, # 100% do capital
    "DC"   : 0.2, # 20% do capital
    "DG"   : 0.2, # 20% do capital
    "DIH"  : 0.1, # 10% do capital
    "DIHU" : 0.1, # 10% do capital
    "DMHO" : 0.1, # 10% do capital
    "DIT"  : 0.1, # 10% do capital
    "DITAD": 0.8, # 80% do capital 
    "IFPTD": 1.0, # 100% do capital
    "FF"   : 0.2,  # 20% do capital
    "MA"   : 1.0  # 100% do capital
}

# =====================================================
# FATOR DE AJUSTE TÉCNICO PARA AJUSTAR AS COBERTURAS
# =====================================================
FATOR_AJUSTE = {
    "M"    : 1.0, 
    "IPA"  : 1.0, 
    "DC"   : 1.0, 
    "DG"   : 1.0, 
    "DIH"  : 1.0, 
    "DIHU" : 1.0, 
    "DMHO" : 1.0, 
    "DIT"  : 1.0, 
    "DITAD": 1.0, 
    "IFPTD": 1.0, 
    "FF"   : 1.0, 
    "MA"   : 1.0  
}

def calcula_premio_cobertura(capital, taxa):
    return capital * taxa


def calcula_premio_individual(capital, idade, sexo, coberturas):

    detalhes = {}
    premio_total = 0

    for cobertura in coberturas:

        taxa_func = TAXAS.get(cobertura)

        if taxa_func is None:
            raise ValueError(f"Cobertura inválida: {cobertura}")

        taxa = taxa_func(idade, sexo)

        fator = FATOR_CAPITAL.get(cobertura, 1)

        capital_cobertura = capital * fator

        premio = calcula_premio_cobertura(capital_cobertura, taxa)

        detalhes[cobertura] = {
            "taxa": taxa,
            "capital": capital_cobertura,
            "premio": round(premio, 2)
        }

        premio_total += premio

    return round(premio_total, 2), detalhes