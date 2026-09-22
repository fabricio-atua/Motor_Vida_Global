# Motor V3 — Vida em Grupo Capital Global
#
# Taxas técnicas anuais (% do capital segurado, ou R$/vida/ano no caso do
# Funeral), separadas por segmento (Funcionários / Sócios), conforme a
# memória técnica do cliente:
#   Tabelas/Melhoria_V3/STG_Memoria_Alteracoes_Simulador_NTA_2026_FINAL_AUDITADO.docx
#   (seções 4, 5 e 7.3 — "Matriz de convergência das coberturas")
# e a planilha de apoio Tabelas/Melhoria_V3/Taxas NTA - Jardel.xlsx (aba
# 01_Resumo), auditada em 17/09/2026.
#
# IMPORTANTE: estas são as taxas técnicas PROVISÓRIAS do simulador do
# cliente — já incluem IBNR (15% nas coberturas sobre capital, 0% no
# Funeral) e margem de oscilação (5%). Permanecem sujeitas a validação e
# aprovação formal do atuário responsável antes de uso definitivo em
# produção (item 9 da memória técnica — "Deliberações solicitadas ao
# atuário").

# =====================================================
# COBERTURAS SOBRE CAPITAL (% do capital segurado, ao ano)
# None = sem taxa aprovada / bloqueada para o segmento.
#
# item 5 da memória: as coberturas abaixo (IEM, DEIA, VITA, DCF, AA, VR)
# são novas -- não constam da NTA original e precisam ser incluídas nas
# Condições Contratuais e na NTA antes de integrar o produto de verdade.
# Por decisão da STG, ficam fechadas no simulador até isso acontecer:
# IEM, IPDL, DEIA, VITA, AA e VR totalmente bloqueadas (None nos dois
# segmentos, o que já as tira da lista de checkboxes -- ver
# COBERTURAS_BLOQUEADAS). DCF permanece ativa por decisão da STG.
# IPTA, DMH e VIT continuam bloqueadas por nunca terem tido taxa (não é
# fechamento por NTA, é ausência mesmo -- ver item 5 da memória).
#
# As taxas das coberturas fechadas por NTA NÃO foram apagadas -- ficam
# guardadas em TAXAS_FECHADAS_RESERVA logo abaixo, prontas para copiar de
# volta pra cá assim que a cobertura for aprovada e incluída na NTA.
# =====================================================
TAXAS_TECNICAS = {
    "MORTE": {"FUNC": 0.00147798, "SOCIO": 0.00343553},
    "IAC":   {"FUNC": 0.00045260, "SOCIO": 0.00105204},
    "IAF":   {"FUNC": 0.00016691, "SOCIO": 0.00016354},
    "IEA":   {"FUNC": 0.00027395, "SOCIO": 0.00016414},
    "IPA":   {"FUNC": 0.00010766, "SOCIO": 0.00004962},
    "IPTA":  {"FUNC": None,       "SOCIO": None},
    "IPDF":  {"FUNC": 0.00019433, "SOCIO": 0.00045174},
    "IPDL":  {"FUNC": None,       "SOCIO": None},
    "IEM":   {"FUNC": None,       "SOCIO": None},
    "DEIA":  {"FUNC": None,       "SOCIO": None},
    "VITA":  {"FUNC": None,       "SOCIO": None},
    "DCF":   {"FUNC": 0.00067785, "SOCIO": 0.00052722},
    "AA":    {"FUNC": None,       "SOCIO": None},
    "VR":    {"FUNC": None,       "SOCIO": None},
    "DMHO":  {"FUNC": 0.00376193, "SOCIO": 0.00370855},
    "DMH":   {"FUNC": None,       "SOCIO": None},
    "VIT":   {"FUNC": None,       "SOCIO": None},
}

# =====================================================
# RESERVA — taxas técnicas das coberturas fechadas por falta de NTA
# (IEM, IPDL, DEIA, VITA, AA, VR), preservadas aqui para reativação futura
# sem precisar buscar de novo na planilha/memória técnica. Para reabrir
# uma cobertura, copie o par FUNC/SOCIO daqui de volta para a entrada
# correspondente em TAXAS_TECNICAS acima.
# =====================================================
TAXAS_FECHADAS_RESERVA = {
    "IEM":  {"FUNC": 0.00150865, "SOCIO": 0.00350678},
    "IPDL": {"FUNC": 0.00066381, "SOCIO": None},
    "DEIA": {"FUNC": 0.00006688, "SOCIO": 0.00003753},
    "VITA": {"FUNC": 0.00962349, "SOCIO": None},
    "AA":   {"FUNC": 0.00150865, "SOCIO": 0.00350674},
    "VR":   {"FUNC": 0.00150865, "SOCIO": None},
}

# Parâmetros de proteção técnica aplicados na taxa pura para chegar na taxa
# técnica acima (item 6.1 da memória) — mantidos aqui só para rastreabilidade
# e exibição; a taxa já vem pronta em TAXAS_TECNICAS.
IBNR_CAPITAL = 0.15
OSCILACAO_CAPITAL = 0.05

DESCRICOES = {
    "MORTE": "Morte",
    "IAC":   "IAC - Inclusão Automática de Cônjuge",
    "IAF":   "IAF - Inclusão Automática de Filhos",
    "IEA":   "IEA - Indenização Especial por Morte Acidental",
    "IPA":   "IPA - Invalidez Permanente Total ou Parcial por Acidente",
    "IPTA":  "IPTA - Invalidez Permanente Total por Acidente",
    "IPDF":  "IPDF - Invalidez Permanente Total por Doença Funcional",
    "IPDL":  "IPDL - Invalidez Permanente Total por Doença Laborativa",
    "IEM":   "IEM - Indenização Extraordinária por Morte",
    "DEIA":  "DEIA - Despesas Extraordinárias por Invalidez por Acidente",
    "VITA":  "VITA - Verba por Incapacidade Temporária por Acidente",
    "DCF":   "DCF - Doenças Congênitas de Filhos",
    "AA":    "AA - Auxílio Alimentação",
    "VR":    "VR - Verbas Rescisórias",
    "DMHO":  "DMHO - Despesas Médicas Hospitalares e Odontológicas",
    "DMH":   "DMH - Despesas Médicas Hospitalares",
    "VIT":   "VIT - Verba por Incapacidade Temporária",
}

# Coberturas totalmente bloqueadas (sem taxa em nenhum segmento) — não devem
# nem aparecer como opção habilitada na tela (item 5 da memória).
COBERTURAS_BLOQUEADAS = {
    cobertura for cobertura, taxas in TAXAS_TECNICAS.items()
    if taxas["FUNC"] is None and taxas["SOCIO"] is None
}

# =====================================================
# AUXÍLIO FUNERAL — R$/vida/ano, por modalidade e limite contratado
# (item 6.3 da memória; mesma base para Funcionários e Sócios — "todos os
# segurados", conforme aba 01_Resumo). IBNR 0%, oscilação 5%.
# =====================================================
IBNR_FUNERAL = 0.00
OSCILACAO_FUNERAL = 0.05

TAXAS_FUNERAL = {
    "INDIVIDUAL": {
        5_000:  6.602925,
        7_000:  9.244095,
        10_000: 13.205850,
        12_000: 15.847020,
    },
    "FAMILIAR": {
        5_000:  13.567425,
        7_000:  18.994395,
        10_000: 27.134850,
        12_000: 32.561820,
    },
}

DESCRICOES_FUNERAL = {
    "INDIVIDUAL": "Assistência Funeral Individual",
    "FAMILIAR": "Assistência Funeral Familiar",
}

LIMITES_FUNERAL = [5_000, 7_000, 10_000, 12_000]


def taxa_ativa(cobertura, segmento):
    """Taxa técnica anual ativa da cobertura para o segmento (item 6.8.2 da
    memória) -- None se a cobertura estiver bloqueada para esse segmento."""
    return TAXAS_TECNICAS.get(cobertura, {}).get(segmento)


def taxa_funeral(modalidade, limite):
    """Taxa técnica anual em R$/vida do Funeral (item 6.3) -- None se a
    modalidade/limite não tiver taxa cadastrada."""
    return TAXAS_FUNERAL.get(modalidade, {}).get(limite)
