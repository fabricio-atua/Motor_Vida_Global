from calculo.vida.taxas import TAXAS

def calcula_premio_cobertura(capital, taxa):
    return capital * taxa


def calcula_premio_grupo(capital, coberturas, vidas, vidas_por_cobertura=None):
    """vidas_por_cobertura permite que uma cobertura (ex: IAC/IAF, estendidas a
    cônjuge/filhos) use uma quantidade de vidas diferente da do grupo (ex: nem
    todo funcionário tem cônjuge/filho cadastrado). Coberturas ausentes do dict
    usam a quantidade de vidas padrão do grupo."""

    vidas_por_cobertura = vidas_por_cobertura or {}

    detalhes = {}
    premio_vida = 0
    premio_grupo = 0

    for cobertura in coberturas:
        taxa = TAXAS[cobertura]
        premio = calcula_premio_cobertura(capital, taxa)
        vidas_desta_cobertura = vidas_por_cobertura.get(cobertura, vidas)

        detalhes[cobertura] = {
            "taxa": taxa,
            "premio": round(premio, 2),
            "vidas": vidas_desta_cobertura
        }

        premio_vida += premio
        premio_grupo += premio * vidas_desta_cobertura

    return round(premio_vida, 2), round(premio_grupo, 2), detalhes
