# =========================
# TAXA BASE
# =========================
TAXA_BASE = {
    "RCTR": 0.00017,   # 0,017%
    "RCDC": 0.00028     # 0,028%
}

# =========================
# IOF
# =========================
IOF = 0.0738   # 7,38%


# -----------------------------
# FATOR POR UF
# -----------------------------
FATOR_UF = {
    "AC": {"fator_RCTR": 1.10, "fator_RCDC": 1.08},
    "AL": {"fator_RCTR": 1.08, "fator_RCDC": 1.12},
    "AP": {"fator_RCTR": 1.06, "fator_RCDC": 1.08},
    "AM": {"fator_RCTR": 1.06, "fator_RCDC": 1.08},
    "BA": {"fator_RCTR": 1.06, "fator_RCDC": 1.12},
    "CE": {"fator_RCTR": 1.08, "fator_RCDC": 1.12},
    "DF": {"fator_RCTR": 1.01, "fator_RCDC": 0.98},
    "ES": {"fator_RCTR": 1.04, "fator_RCDC": 1.10},
    "GO": {"fator_RCTR": 1.01, "fator_RCDC": 0.98},
    "MA": {"fator_RCTR": 1.08, "fator_RCDC": 1.12},
    "MT": {"fator_RCTR": 1.03, "fator_RCDC": 1.06},
    "MS": {"fator_RCTR": 1.01, "fator_RCDC": 0.98},
    "MG": {"fator_RCTR": 1.03, "fator_RCDC": 1.12},
    "PA": {"fator_RCTR": 1.10, "fator_RCDC": 1.12},
    "PB": {"fator_RCTR": 1.06, "fator_RCDC": 1.08},
    "PR": {"fator_RCTR": 0.98, "fator_RCDC": 1.05},
    "PE": {"fator_RCTR": 1.08, "fator_RCDC": 1.12},
    "PI": {"fator_RCTR": 1.06, "fator_RCDC": 1.06},
    "RJ": {"fator_RCTR": 1.15, "fator_RCDC": 1.30},
    "RN": {"fator_RCTR": 1.06, "fator_RCDC": 1.07},
    "RS": {"fator_RCTR": 0.97, "fator_RCDC": 0.98},
    "RO": {"fator_RCTR": 1.08, "fator_RCDC": 1.07},
    "RR": {"fator_RCTR": 1.06, "fator_RCDC": 1.08},
    "SC": {"fator_RCTR": 0.97, "fator_RCDC": 0.97},
    "SP": {"fator_RCTR": 1.08, "fator_RCDC": 1.25},
    "SE": {"fator_RCTR": 1.03, "fator_RCDC": 0.98},
    "TO": {"fator_RCTR": 1.05, "fator_RCDC": 1.07},
}

# =========================
# COBERTURAS ADICIONAIS
# =========================
COBERTURAS_ADICIONAIS = {
    "RCTR-C": {
        "54001": {
            "nome": "OPERAÇÕES DE CARGA/DESCARGA/IÇAMENTO",
            "taxa": 0.00002,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54002": {
            "nome": "VIAGEM RODOVIÁRIA COM PERCURSO COMPLEMENTAR FLUVIAL",
            "taxa": 0.00003,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54003": {
            "nome": "EXTENSÃO DE COBERTURA AO VALOR DOS IMPOSTOS SUSPENSOS E/OU BENEFÍCIOS",
            "taxa": 0.00001,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54004": {
            "nome": "TRANSPORTE DE CARGAS EXCEPCIONAIS/ESPECIAIS",
            "taxa": 0.00005,
            "exige_lmi": True,
            "franquia": 0.15,
            "ativa": True
        },
        "54005": {
            "nome": "AVARIAS NÃO ATRIBUÍDAS A ACIDENTES RODOVIÁRIOS",
            "taxa": 0.00003,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54006": {
            "nome": "OPERAÇÕES DE CARGA E DESCARGA (SEM APARELHAGEM/MÁQUINAS ESPECIAIS)",
            "taxa": 0.00002,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54007": {
            "nome": "PARALISAÇÃO DE MÁQUINAS FRIGORÍFICAS",
            "taxa": 0.00003,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54009": {
            "nome": "PRORROGAÇÃO DO PRAZO DE COBERTURA (INCÊNDIO/EXPLOSÃO)",
            "taxa": 0.00001,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54010": {
            "nome": "DESPESAS COM LIMPEZA, CONTENÇÃO E DESTINAÇÃO DE PRODUTOS POLUENTES",
            "taxa": 0.00004,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54013": {
            "nome": "DESPESAS DE CONTENÇÃO DE PRODUTOS PERIGOSOS/POLUENTES/CONTAMINANTES",
            "taxa": 0.00005,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "54014": {
            "nome": "ADICIONAL DE FRETE",
            "taxa": 0.00001,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
    },

    "RC-DC": {
        "55001": {
            "nome": "ROUBO NO DEPÓSITO DO TRANSPORTADOR",
            "taxa": 0.00003,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "55003": {
            "nome": "EXTENSÃO DE COBERTURA AO VALOR DOS IMPOSTOS SUSPENSOS E/OU BENEFÍCIOS",
            "taxa": 0.00001,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "55004": {
            "nome": "FURTO QUALIFICADO",
            "taxa": 0.00003,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
        "55015": {
            "nome": "PERDA DE FRETE",
            "taxa": 0.00001,
            "exige_lmi": True,
            "franquia": 0.10,
            "ativa": True
        },
    }
}

# =========================
# TABELA VIAGENS POR MÊS
# =========================
TBL_VIAGENS_MES = {
    "Ate_10": {
        "faixa": (0, 10),
        "f_rctr": 1.05,
        "f_rcdc": 1.05
    },
    "11_30": {
        "faixa": (11, 30),
        "f_rctr": 1.00,
        "f_rcdc": 1.00
    },
    "31_80": {
        "faixa": (31, 80),
        "f_rctr": 0.97,
        "f_rcdc": 0.99
    },
    "81_150": {
        "faixa": (81, 150),
        "f_rctr": 0.95,
        "f_rcdc": 0.98
    },
    "151_300": {
        "faixa": (151, 300),
        "f_rctr": 0.93,
        "f_rcdc": 0.97
    },
    "301_600": {
        "faixa": (301, 600),
        "f_rctr": 0.91,
        "f_rcdc": 0.96
    },
    "601_1.500": {
        "faixa": (601, 1500),
        "f_rctr": 0.89,
        "f_rcdc": 0.95
    },
    "Acima_1.500": {
        "faixa": (1501, float("inf")),
        "f_rctr": 0.87,
        "f_rcdc": 0.94
    }
}

# =========================
# TABELA DISTÂNCIA (KM)
# =========================
TBL_DISTANCIA = {
    "Ate_200": {
        "faixa": (0, 200),
        "f_rctr": 0.95,
        "f_rcdc": 0.95
    },
    "201_500": {
        "faixa": (201, 500),
        "f_rctr": 1.00,
        "f_rcdc": 1.00
    },
    "501_1.000": {
        "faixa": (501, 1000),
        "f_rctr": 1.08,
        "f_rcdc": 1.10
    },
    "Acima_1.000": {
        "faixa": (1001, float("inf")),
        "f_rctr": 1.15,
        "f_rcdc": 1.18
    }
}

# =========================
# TABELA OPERAÇÃO NOTURNA (%)
# =========================
TBL_NOTURNO = {
    "0_10": {
        "faixa": (0, 10),
        "f_rctr": 1.00,
        "f_rcdc": 1.00
    },
    "11_30": {
        "faixa": (11, 30),
        "f_rctr": 1.00,
        "f_rcdc": 1.05
    },
    "31_60": {
        "faixa": (31, 60),
        "f_rctr": 1.00,
        "f_rcdc": 1.10
    },
    "Acima_60": {
        "faixa": (61, float("inf")),
        "f_rctr": 1.00,
        "f_rcdc": 1.18
    }
}

# =========================
# TABELA ROTA CRÍTICA
# =========================
TBL_ROTA_CRITICA = {
    "Não": {
        "f_rctr": 1.00,
        "f_rcdc": 1.00
    },
    "Sim": {
        "f_rctr": 1.00,
        "f_rcdc": 1.35
    }
}

# =========================
# TABELA IDADE MÉDIA DA FROTA
# =========================
TBL_IDADE_FROTA = {
    "Ate_5": {
        "faixa": (0, 5),
        "f_rctr": 0.95,
        "f_rcdc": 1.00
    },
    "6_10": {
        "faixa": (6, 10),
        "f_rctr": 1.00,
        "f_rcdc": 1.00
    },
    "11_15": {
        "faixa": (11, 15),
        "f_rctr": 1.10,
        "f_rcdc": 1.00
    },
    "Acima_15": {
        "faixa": (16, float("inf")),
        "f_rctr": 1.20,
        "f_rcdc": 1.00
    }
}

# =========================
# TABELA % TERCEIROS NA FROTA
# =========================
TBL_PCT_TERCEIROS = {
    "Ate_20": {
        "faixa": (0, 20),
        "f_rctr": 1.00,
        "f_rcdc": 1.00
    },
    "21_50": {
        "faixa": (21, 50),
        "f_rctr": 1.05,
        "f_rcdc": 1.00
    },
    "51_80": {
        "faixa": (51, 80),
        "f_rctr": 1.09,
        "f_rcdc": 1.00
    },
    "Acima_80": {
        "faixa": (81, float("inf")),
        "f_rctr": 1.18,
        "f_rcdc": 1.00
    }
}

# =========================
# TABELA VALOR DE SINISTRO (HISTÓRICO)
# =========================
TBL_VALOR_SINISTRO = {
    "Zero": {
        "faixa": (0, 0),
        "f_rctr": 1.00,
        "f_rcdc": 1.00
    },
    "Até_50K": {
        "faixa": (0.01, 50000),
        "f_rctr": 1.03,
        "f_rcdc": 1.05
    },
    "50K_200K": {
        "faixa": (50001, 200000),
        "f_rctr": 1.08,
        "f_rcdc": 1.10
    },
    "200K_500K": {
        "faixa": (200001, 500000),
        "f_rctr": 1.15,
        "f_rcdc": 1.21
    },
    "Acima_500K": {
        "faixa": (500001, float("inf")),
        "f_rctr": 1.20,
        "f_rcdc": 1.25
    }
}

# =========================
# MERCADORIAS
# =========================
MERCADORIAS = {
'M001':{'descricao':'Aço Longo, aço bruto, aço plano e aço em geral (ligas, chapas, bobinas, tubos, lingotes, etc)','familia_comercial':'Metais/Minerais','subfamilia_tecnico':'Metais','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M002':{'descricao':'Açúcar (todos os tipos e variações)','familia_comercial':'Alimentos','subfamilia_tecnico':'Alimentos/Bebidas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M003':{'descricao':'Aeronaves, suas partes e peças','familia_comercial':'Especial/Projeto','subfamilia_tecnico':'Aeronáutico','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M004':{'descricao':'Álcool etílico e para fins medicinais/farmacêuticos','familia_comercial':'Perigosos/Combustíveis','subfamilia_tecnico':'Álcool','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M005':{'descricao':'Algodão (fardo, pluma e caroço)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M006':{'descricao':'Alimentos e bebidas refrigerados (sucos naturais, iogurte, queijos, frios, massas frescas e laticínios em geral)','familia_comercial':'Alimentos/Perecíveis','subfamilia_tecnico':'Refrigerados','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M007':{'descricao':'Alimentos em geral não refrigerados (biscoitos, salgadinhos, snacks), inclui ração animal','familia_comercial':'Alimentos/Perecíveis','subfamilia_tecnico':'Refrigerados','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M008':{'descricao':'Alumínio em geral (perfis, tarugos, tubos, vergalhões, chapas, bobinas, folhas, lingotes, etc)','familia_comercial':'Metais/Minerais','subfamilia_tecnico':'Metais','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M009':{'descricao':'Amianto (asbestos), qualquer tipo, forma e/ou quantidade','familia_comercial':'Perigosos/Combustíveis','subfamilia_tecnico':'Amianto','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M010':{'descricao':'Animais vivos e/ou sêmen (para fins reprodutivos ou não)','familia_comercial':'Animais/Biológicos','subfamilia_tecnico':'Animais vivos/biológicos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M011':{'descricao':'Armas, armamentos e munições','familia_comercial':'Controlados/Restritos','subfamilia_tecnico':'Armas e munições','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M012':{'descricao':'Artigos de cordoaria, feltros, falsos tecidos, fios especiais, cordéis e cordas','familia_comercial':'Têxtil/Moda','subfamilia_tecnico':'Têxtil','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M013':{'descricao':'Artigos de higiene e limpeza (inclusive aparelhos e lâminas de barbear)','familia_comercial':'Higiene/Limpeza','subfamilia_tecnico':'Higiene','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M014':{'descricao':'Artigos escolares, artigos de papelaria em geral','familia_comercial':'Papel/Madeira','subfamilia_tecnico':'Papel/Madeira','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M015':{'descricao':'Artigos esportivos e de proteção','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M016':{'descricao':'Artigos para fumantes, fósforos, isqueiros, fluido para isqueiros e cinzeiros em geral','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M017':{'descricao':'Auto peças em geral para veiculos leves, pesados e motocicletas','familia_comercial':'Automotivo/Veículos','subfamilia_tecnico':'Veículos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M018':{'descricao':'Azulejos, cerâmicas, cristais, granitos, ladrilhos, louças, porcelanas, mármores, pisos cerâmicos','familia_comercial':'Frágeis','subfamilia_tecnico':'Vidros/Louças/Cerâmicas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M019':{'descricao':'Bebidas alcoólicas (Cerveja, Chopp, Soft Drinks e similares)','familia_comercial':'Alimentos/Bebidas','subfamilia_tecnico':'Bebidas alcoólicas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M020':{'descricao':'Bebidas alcoólicas especiais (Vinho, Whisky, Vodka e destilados em geral)','familia_comercial':'Alimentos/Bebidas','subfamilia_tecnico':'Bebidas alcoólicas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M021':{'descricao':'Bebidas em geral (exceto alcoolicas ), sucos pasteurizados, refrigerantes e similares','familia_comercial':'Alimentos','subfamilia_tecnico':'Alimentos/Bebidas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M022':{'descricao':'Borracha em geral e seus derivados','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M023':{'descricao':'Brinquedos e Bicicletas (inclusive partes, peças e acessórios)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M024':{'descricao':'Café de qualquer tipo (em pó, em graos, solúvel etc.)','familia_comercial':'Alimentos','subfamilia_tecnico':'Alimentos/Bebidas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M025':{'descricao':'Calçados (tênis, sapato, chinelo, sandália, solado, palmilha, correia)','familia_comercial':'Têxtil/Moda','subfamilia_tecnico':'Têxtil','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M026':{'descricao':'Cargas diversas não especificadas, exceto produtos perigosos (químimos inflamáveis e/ou explosivos)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M027':{'descricao':'Cargas radioativas e nucleares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M028':{'descricao':'Carnes de todos os tipos, bovina, suina, aves e similares (frigorificada, in natura e/ou charque)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M029':{'descricao':'Cartuchos para impressoras e copiadoras','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M030':{'descricao':'Carvão qualquer tipo','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M031':{'descricao':'Cassiterita, estanho e níquel (qualquer tipo)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M032':{'descricao':'CDs, DVDs, LDs, LPs e Blu-ray','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M033':{'descricao':'Celulose em geral, fibra curta, fibra longa e similares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M034':{'descricao':'Chapéu, boné e demais artefatos de uso semelhante','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M035':{'descricao':'Chumbo de qualquer tipo','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M036':{'descricao':'Cigarros, tabacos, fumo e seus derivados','familia_comercial':'Alimentos/Bebidas','subfamilia_tecnico':'Tabaco/cigarros','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M037':{'descricao':'Cobre de qualquer tipo(metal)','familia_comercial':'Metais/Minerais','subfamilia_tecnico':'Metais','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M038':{'descricao':'Colchões, almofadas e similares','familia_comercial':'Móveis/Decoração','subfamilia_tecnico':'Móveis/colchões','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M039':{'descricao':'Combustíveis em geral (etanol, gasolina e oleo diesel)','familia_comercial':'Perigosos/Combustíveis','subfamilia_tecnico':'Combustíveis','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M040':{'descricao':'Computadores (notebook, desktop, tablet), incluindo suas partes, peças e periféricos','familia_comercial':'Eletrônicos/Tecnologia','subfamilia_tecnico':'Computação/portáteis','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M041':{'descricao':'Confecções, fios de seda, fios de algodão e fios têxteis','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M042':{'descricao':'Cortiça e suas obras','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M043':{'descricao':'Cosméticos, Perfumes e Bronzeadores','familia_comercial':'Higiene/Limpeza','subfamilia_tecnico':'Higiene','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M044':{'descricao':'Couro cru, wetblue (semi-acabado) ou beneficiado e peles','familia_comercial':'Têxtil/Moda','subfamilia_tecnico':'Têxtil','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M045':{'descricao':'Defensivos agrícolas, fertilizantes, adubos, agrotóxicos e sementes','familia_comercial':'Animais/Biológicos','subfamilia_tecnico':'Animais vivos/biológicos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M046':{'descricao':'Demais produtos alimentícios não especificados (não refrigerados e/ou in natura)','familia_comercial':'Alimentos/Perecíveis','subfamilia_tecnico':'Refrigerados','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M047':{'descricao':'Dinheiro, valores em espécie, cheques, titulos e similares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M048':{'descricao':'Doces em geral (balas, chicletes, biscoitos, chocolates etc.)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M049':{'descricao':'Eletrodomésticos e eletrôeletronicos em geral (linha branca e linha marrom)','familia_comercial':'Eletrônicos/Tecnologia','subfamilia_tecnico':'Linha branca/marrom','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M050':{'descricao':'Embalagens Metálicas, embalagens de papel, embalagens plásticas e latas','familia_comercial':'Papel/Madeira','subfamilia_tecnico':'Papel/Madeira','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M051':{'descricao':'Embarcações e estruturas flutuantes','familia_comercial':'Metais/Minerais','subfamilia_tecnico':'Metais','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M052':{'descricao':'Empilhadeiras, escavadeiras, retroescavadeiras, carregadeiras, tratores agrícolas e de terraplanagem','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M053':{'descricao':'Empresas de mineração de carvão ou produtoras de petróleo e gás que não possuam plano de combate ao aquecimento global (*)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M054':{'descricao':'Equipamentos de Ginástica, Peso Livre, Bicicletas Ergométricas, Esteiras e similares','familia_comercial':'Máquinas/Equipamentos','subfamilia_tecnico':'Industrial','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M055':{'descricao':'Espelhos e vidros em geral','familia_comercial':'Frágeis','subfamilia_tecnico':'Vidros/Louças/Cerâmicas','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M056':{'descricao':'Estruturas e peças de concreto pré-fabricadas (lajes, vigas, postes e paineis)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M057':{'descricao':'Explosivos, materiais e/ou sustâncias radioativas','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M058':{'descricao':'Farinha de peixe, fibra vegetal e copra','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M059':{'descricao':'Farinha de trigo e grãos em geral','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M060':{'descricao':'Fechaduras, ferramentas manuais e ferragens de uso geral (chave de fenda e similares)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M061':{'descricao':'Ferramentas elétricas em geral (furadeiras, parafusadeiras, lixadeiras e similares)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M062':{'descricao':'Ferro, ferro fundido e derivados','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M063':{'descricao':'Fios e cabos eletricos, fios e cabos telefônicos e/ou telecom','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M064':{'descricao':'Fraldas descartáveis, lenços umedecidos e similares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M065':{'descricao':'Frutas Secas (não refrigeradas), cascas de cítricos, cascas de melão, castanhas e similares','familia_comercial':'Alimentos/Perecíveis','subfamilia_tecnico':'Refrigerados','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M066':{'descricao':'Frutas, legumes e verduras em geral','familia_comercial':'Alimentos/Perecíveis','subfamilia_tecnico':'Hortifruti','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M067':{'descricao':'Gomas, resinas, sucos e extratos vegetais','familia_comercial':'Químicos','subfamilia_tecnico':'Químicos/Resinas/Tintas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M068':{'descricao':'Guarda-chuva, guarda-sol, bengalas e similares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M069':{'descricao':'Indústria de móveis em geral, móveis de madeira e similares','familia_comercial':'Móveis/Decoração','subfamilia_tecnico':'Móveis/colchões','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M070':{'descricao':'Joias, pérolas, pedras preciosas, metais e minerais preciosos e/ou semipreciosos','familia_comercial':'Controlados/Restritos','subfamilia_tecnico':'Joias e valores','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M071':{'descricao':'Leite em pó, leite condensado, creme de leite, leite de coco e similares','familia_comercial':'Alimentos','subfamilia_tecnico':'Alimentos/Bebidas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M072':{'descricao':'Leite longa vida, leite de soja e similares','familia_comercial':'Alimentos','subfamilia_tecnico':'Alimentos/Bebidas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M073':{'descricao':'Livros e revistas em geral','familia_comercial':'Papel/Madeira','subfamilia_tecnico':'Papel/Madeira','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M074':{'descricao':'Madeira em geral, inclui esquadrias, compensados e folheados','familia_comercial':'Papel/Madeira','subfamilia_tecnico':'Papel/Madeira','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M075':{'descricao':'Malas, mochilas, bolsas e bagagens (sem conteudo)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M076':{'descricao':'Máquinas e equipamentos industriais, suas partes e peças','familia_comercial':'Máquinas/Equipamentos','subfamilia_tecnico':'Industrial','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M077':{'descricao':'Materiais de construção e acabamento, louças sanitárias, pias, cubas e similares','familia_comercial':'Frágeis','subfamilia_tecnico':'Vidros/Louças/Cerâmicas','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M078':{'descricao':'Materiais de escritório em geral','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M079':{'descricao':'Materiais de infraestrutura para construção e manutenção de ferrovias e rodovias (inclui aparelhos mecânicos, suas partes e peças)','familia_comercial':'Construção','subfamilia_tecnico':'Materiais de construção','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M080':{'descricao':'Materiais e equipamentos elétricos para geração, transmissão e distribuição de energia elétrica (transformadores e similares)','familia_comercial':'Máquinas/Equipamentos','subfamilia_tecnico':'Industrial','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M081':{'descricao':'Materiais e/ou aparelhos de iluminação não eletrica, parafina, velas de cera, lampiões, lampadas de acetileno etc.','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M082':{'descricao':'Materiais elétricos residenciais e/ou industriais (interruptores, fusíveis e similares)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M083':{'descricao':'Material de construção, estruturas metálicas pré-fabricadas, placas de ancoragem e postes metálicos','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M084':{'descricao':'Matérias á base de amido e/ou fécula, cola e/ou enzimas','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M085':{'descricao':'Medicamentos, vitaminas em geral de uso humano e veterinário','familia_comercial':'Farmacêutico/Médico','subfamilia_tecnico':'Farma/Hospitalar','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M086':{'descricao':'Mineradoras cuja receita advenham da extração e venda de carvão (*)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M087':{'descricao':'Minério de Molibdênio (qualquer tipo)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M088':{'descricao':'Minérios, escórias e cinzas','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M089':{'descricao':'Modems, roteadores, switch de rede cabeada e/ou sem fio','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M090':{'descricao':'Móveis e mobiliário para consultório médico e/ou odontologico (para uso cirúrgico ou não)','familia_comercial':'Móveis/Decoração','subfamilia_tecnico':'Móveis/colchões','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M091':{'descricao':'Mudanças em geral','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M092':{'descricao':'Obras de arte, decoração, antiguidades, coleções e raridades','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M093':{'descricao':'Óleo automotivo e similares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M094':{'descricao':'Óleo Lubrificante em geral','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M095':{'descricao':'Óleos Comestíveis (inclusive Azeite)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M096':{'descricao':'Ovos em geral','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M097':{'descricao':'Óxido e dióxido de titânio','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M098':{'descricao':'Painel solar, placas fotovoltaicas e demais equipamentos destinados ao setor energia solar','familia_comercial':'Máquinas/Equipamentos','subfamilia_tecnico':'Industrial','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M099':{'descricao':'Pão de forma, bisnaguinhas, bolos e demais produtos industrializados (similares)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M100':{'descricao':'Papel e cartão obras de pasta de celulose, de papel ou de cartão','familia_comercial':'Papel/Madeira','subfamilia_tecnico':'Papel/Madeira','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M101':{'descricao':'Papel sulfite, cartolina, carta e similares (resmas de papel)','familia_comercial':'Papel/Madeira','subfamilia_tecnico':'Papel/Madeira','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M102':{'descricao':'Pasta de madeira e/ou de outras matérias fibrosas, papel para reciclagem (inclui desperdícios e aparas)','familia_comercial':'Papel/Madeira','subfamilia_tecnico':'Papel/Madeira','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M103':{'descricao':'Penas, penugem, peruca de cabelo, flores artificiais','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M104':{'descricao':'Pescados e/ou qualquer tipo de carga e/ou produto obtido pela operação de embarcações de pesca','familia_comercial':'Metais/Minerais','subfamilia_tecnico':'Metais','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M105':{'descricao':'Pilhas, baterias e acumuladores em geral','familia_comercial':'Químicos','subfamilia_tecnico':'Baterias/Pilhas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M106':{'descricao':'Pneus e câmaras de ar','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M107':{'descricao':'Pneus, câmaras de ar, borracha pneumática e similares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M108':{'descricao':'Polietileno, polipropileno, poliuretano, tolueno de isocianato (TDI), policloreto de vinila, polimeros e seus derivados','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M109':{'descricao':'Processadores, microprocessadores, pentes de memória RAM, placas de audio, video e similares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M110':{'descricao':'Produtos e artigos médicos, artigos farmacêuticos e hospitalares (exceto medicamentos e vitaminas)','familia_comercial':'Farmacêutico/Médico','subfamilia_tecnico':'Farma/Hospitalar','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M111':{'descricao':'Produtos fotográficos, câmeras fotográficas, filmadoras de qualquer tipo (inclusive filmes)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M112':{'descricao':'Produtos químicos de origem orgânica','familia_comercial':'Químicos','subfamilia_tecnico':'Químicos/Resinas/Tintas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M113':{'descricao':'Produtos Químicos, Petroquimicos e Farmacos (materia prima), PVC, resinas termoplásticas e similares','familia_comercial':'Químicos','subfamilia_tecnico':'Químicos/Resinas/Tintas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M114':{'descricao':'Projetos relacionados a construção e operação de minas de carvão ou centrais termoelétricas a carvão (*)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M115':{'descricao':'Reatores, lampâdas, luminárias alogênas, fluorescentes e/ou LED','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M116':{'descricao':'Relógios em geral (exceto smartwatch / relogios inteligentes)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M117':{'descricao':'Roupas prontas e tecidos para moldes (alfaiataria)','familia_comercial':'Têxtil/Moda','subfamilia_tecnico':'Têxtil','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M118':{'descricao':'STP - Stock Through Put e Project Cargo','familia_comercial':'Especial/Projeto','subfamilia_tecnico':'STP/Project Cargo','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M119':{'descricao':'Sucata de metais em geral','familia_comercial':'Metais/Minerais','subfamilia_tecnico':'Metais','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M120':{'descricao':'Tapetes e outros revestimentos para pavimentos de matérias têxteis','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M121':{'descricao':'Telefones celulares, smartphones, suas partes, peças e acessórios (incluindo smartwatch e/ou relógio inteligente)','familia_comercial':'Eletrônicos/Tecnologia','subfamilia_tecnico':'Smartphones e acessórios','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M122':{'descricao':'Tintas, vernizes, vorantes, massas acrílicas, pigmentos e similares','familia_comercial':'Químicos','subfamilia_tecnico':'Químicos/Resinas/Tintas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M123':{'descricao':'Tubos e canos hidraulicos, conexões de PVC e Resinas','familia_comercial':'Químicos','subfamilia_tecnico':'Químicos/Resinas/Tintas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M124':{'descricao':'Urna funerária, caixão funerário e similares (exceto acessorios fixos ou móveis compostas por metais preciosos)','familia_comercial':'Móveis/Decoração','subfamilia_tecnico':'Móveis/colchões','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M125':{'descricao':'Veículo Transportador','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M126':{'descricao':'Veículos aquaticos leves, jet ski, moto aquática, paddle board, prancha de surf e similares','familia_comercial':'Automotivo/Veículos','subfamilia_tecnico':'Veículos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M127':{'descricao':'Veículos automotores em geral, utilitários, motocicletas, motonetas, triciclos e quadriciclos (novos e usados)','familia_comercial':'Automotivo/Veículos','subfamilia_tecnico':'Veículos','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M128':{'descricao':'Veículos trafegando/rodando por meios próprios','familia_comercial':'Automotivo/Veículos','subfamilia_tecnico':'Veículos rodando por meios próprios','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M129':{'descricao':'Zinco (todos os tipos)','familia_comercial':'Metais/Minerais','subfamilia_tecnico':'Metais','distancia_categoria':'Baixa Distância','f_rctr':1,'f_rcdc':0.98},
'M130':{'descricao':'Medicamentos termolábeis / vacinas / biológicos','familia_comercial':'Farmacêutico/Médico','subfamilia_tecnico':'Termolábeis/biológicos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M131':{'descricao':'Baterias de lítio / módulos de lítio','familia_comercial':'Químicos','subfamilia_tecnico':'Baterias/Pilhas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M132':{'descricao':'Painéis solares','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M133':{'descricao':'Inversores / equipamentos fotovoltaicos','familia_comercial':'Máquinas/Equipamentos','subfamilia_tecnico':'Industrial','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M134':{'descricao':'Bebidas alcoólicas (vinhos, destilados, cervejas)','familia_comercial':'Alimentos/Bebidas','subfamilia_tecnico':'Bebidas alcoólicas','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M135':{'descricao':'Proteína animal refrigerada/congelada','familia_comercial':'Alimentos/Perecíveis','subfamilia_tecnico':'Refrigerados','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M136':{'descricao':'Defensivos agrícolas (agrotóxicos) - específicos','familia_comercial':'Agrícola/Insumos','subfamilia_tecnico':'Defensivos/Fertilizantes/Sementes','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M137':{'descricao':'Fertilizantes / adubos (granulados, líquidos)','familia_comercial':'Agrícola/Insumos','subfamilia_tecnico':'Defensivos/Fertilizantes/Sementes','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M138':{'descricao':'Carga fracionada mista (multi-mercadoria)','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M139':{'descricao':'Resíduos perigosos / classe I','familia_comercial':'Diversos','subfamilia_tecnico':'Diversos','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1},
'M140':{'descricao':'Vidros automotivos (parabrisas e similares)','familia_comercial':'Frágeis','subfamilia_tecnico':'Vidros/Louças/Cerâmicas','distancia_categoria':'Alta Distância','f_rctr':1.02,'f_rcdc':1.08},
'M141':{'descricao':'Eletrônicos portáteis de alto valor (notebooks premium, etc.)','familia_comercial':'Eletrônicos/Tecnologia','subfamilia_tecnico':'Computação/portáteis','distancia_categoria':'Crítica Distância','f_rctr':1.05,'f_rcdc':1.15},
'M142':{'descricao':'Cigarros e derivados (separado - alto roubo)','familia_comercial':'Alimentos/Bebidas','subfamilia_tecnico':'Tabaco/cigarros','distancia_categoria':'Média Distancia','f_rctr':1,'f_rcdc':1}
}