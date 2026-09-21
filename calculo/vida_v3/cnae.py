import os
import re

import pandas as pd

_CAMINHO_TABELA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "Tabelas", "Motor_Relatividades_CNAE_v3.xlsx"
))

_ABA_MOTOR = "04_MOTOR_CÁLCULO"

# Colunas por posição (mais robusto que por nome -- a planilha usa cabeçalhos
# de duas linhas com acentuação, ex.: "Relat.\nBruta"):
#   A=0 Cód.CNAE | J=9 Relat. Bruta (pré-limite) | N=13 Fonte
_COL_CODIGO = 0
_COL_RELAT_BRUTA = 9
_COL_FONTE = 13

# Piso e teto operacionais do fator CNAE único de lançamento (item 6.2.1 da
# memória técnica): 0,60 (desagravo máximo) a 1,15 (agravo máximo). O motor
# V4 usa os limites antigos (0,75-1,40) definidos na própria planilha de
# origem (aba 01_PARÂMETROS, células C1/C2); o V3 lê a relatividade BRUTA
# (antes desse clamp) na mesma planilha compartilhada e aplica aqui o novo
# limite, sem alterar o arquivo usado pelo V4.
PISO_CNAE = 0.60
TETO_CNAE = 1.15


def _normalizar_codigo(codigo_cnae):
    """Reduz o código CNAE a 7 dígitos, aceitando tanto o formato numérico
    puro (ex: 1113301) quanto o formato oficial com máscara (ex: 0111-3/01)."""
    digitos = re.sub(r"\D", "", str(codigo_cnae))
    return digitos.zfill(7)


def _carregar_tabela_cnae():
    df = pd.read_excel(_CAMINHO_TABELA, sheet_name=_ABA_MOTOR, header=3)

    tabela = pd.DataFrame({
        "codigo": df.iloc[:, _COL_CODIGO].apply(_normalizar_codigo),
        "relat_bruta": pd.to_numeric(df.iloc[:, _COL_RELAT_BRUTA], errors="coerce"),
        "fonte": df.iloc[:, _COL_FONTE],
    })
    tabela = tabela.dropna(subset=["relat_bruta"])
    return tabela.set_index("codigo")


_TABELA_CNAE = _carregar_tabela_cnae()


def consultar_cnae(codigo_cnae):
    """Retorna a relatividade bruta e a fonte (FAP/MPS ou fallback
    CNAE-STG) para o código informado, ou None se o código não existir na
    tabela. Aceita formato numérico puro ou com máscara."""
    codigo = _normalizar_codigo(codigo_cnae)

    if codigo not in _TABELA_CNAE.index:
        return None

    return _TABELA_CNAE.loc[codigo].to_dict()


def fator_por_cnae(codigo_cnae):
    """Retorna (fator, cadastrado): fator único F_CNAE (item 6.2 da memória
    técnica), aplicado apenas às coberturas calculadas sobre capital -- nunca
    ao Auxílio Funeral, que é cobrado em R$/vida.

    - CNAE não encontrado na tabela: retorna (1.0, False) -- fator neutro
      (item 6.8.13 -- regra de validação: "CNAE deve existir na tabela
      operacional").
    - CNAE encontrado: retorna a relatividade bruta (FAP/MPS ou fallback
      CNAE-STG) limitada ao intervalo [0,60 ; 1,15], (True).
    """
    info = consultar_cnae(codigo_cnae)

    if info is None:
        return 1.0, False

    relat_bruta = info.get("relat_bruta")

    if relat_bruta is None or (isinstance(relat_bruta, float) and pd.isna(relat_bruta)):
        return 1.0, False

    fator = max(PISO_CNAE, min(TETO_CNAE, float(relat_bruta)))
    return fator, True
