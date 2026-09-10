import os
import re

import pandas as pd

_CAMINHO_TABELA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "Tabelas", "Motor_Relatividades_CNAE_v3.xlsx"
))

_ABA_RESULTADOS = "08_RESULTADOS"


def _normalizar_codigo(codigo_cnae):
    """Reduz o código CNAE a 7 dígitos, aceitando tanto o formato numérico puro
    (ex: 1113301, como devolvido pela BrasilAPI) quanto o formato oficial com
    máscara (ex: 0111-3/01, como usado na planilha do motor)."""
    digitos = re.sub(r"\D", "", str(codigo_cnae))
    return digitos.zfill(7)


def _carregar_tabela_cnae():
    df = pd.read_excel(_CAMINHO_TABELA, sheet_name=_ABA_RESULTADOS, header=2)
    df = df.dropna(subset=["Cód. CNAE"])
    df["codigo"] = df["Cód. CNAE"].apply(_normalizar_codigo)
    return df.set_index("codigo")


_TABELA_CNAE = _carregar_tabela_cnae()


def consultar_cnae(codigo_cnae):
    """Retorna a linha da aba 08_RESULTADOS (descrição, seção, divisão, fonte e
    relatividade final) para o código informado, ou None se o código não
    existir na tabela. Aceita o código no formato numérico puro (ex: 1113301)
    ou com máscara (ex: 0111-3/01)."""
    codigo = _normalizar_codigo(codigo_cnae)

    if codigo not in _TABELA_CNAE.index:
        return None

    return _TABELA_CNAE.loc[codigo].to_dict()


def fator_por_cnae(codigo_cnae):
    """Retorna (fator, cadastrado) lendo a coluna "Relat. Final" da aba
    08_RESULTADOS de Tabelas/Motor_Relatividades_CNAE_v3.xlsx.

    A relatividade é calculada, por subclasse CNAE, a partir do Índice Composto
    (IC) de Gravidade/Frequência/Custo publicado pelo FAP/MPS (aba
    04_MOTOR_CÁLCULO), relativizado a IC_ref=50 e limitado entre 0,75 (desagravo
    máximo) e 1,40 (agravo máximo) — parâmetros da aba 01_PARÂMETROS. Subclasses
    sem dado FAP usam o fallback do coeficiente CNAE-STG original (Baixo=0,90 |
    Médio=1,00 | Alto=1,15), identificável pela coluna "Fonte" = "CNAE-STG".
    Metodologia completa na aba 02_METODOLOGIA do arquivo.

    - CNAE não encontrado na tabela: retorna (1.0, False) — fator neutro, não cadastrado.
    - CNAE encontrado (fonte FAP/MPS ou fallback CNAE-STG): retorna (Relat. Final, True).
    """
    info = consultar_cnae(codigo_cnae)

    if info is None:
        return 1.0, False

    relatividade = info.get("Relat. Final")

    if relatividade is None or (isinstance(relatividade, float) and pd.isna(relatividade)):
        return 1.0, False

    return float(relatividade), True
