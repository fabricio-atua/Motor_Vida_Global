from calculo.transporte.taxas import TAXAS

def calcula_premio_cobertura(capital, taxa):
    return capital * taxa


def calcula_premio_grupo(capital, coberturas, vidas):

    detalhes = {}
    premio_vida = 0

    for cobertura in coberturas:
        taxa = TAXAS[cobertura]
        premio = calcula_premio_cobertura(capital, taxa)

        detalhes[cobertura] = {
            "taxa": taxa,
            "premio": round(premio, 2)
        }

        premio_vida += premio

    premio_grupo = premio_vida * vidas

    return round(premio_vida, 2), round(premio_grupo, 2), detalhes
