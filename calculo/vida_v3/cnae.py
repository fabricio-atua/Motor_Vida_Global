import os
import re

import pandas as pd

_CAMINHO_TABELA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "Tabelas", "Motor_Relatividades_CNAE_v3.xlsx"
))

_ABA_MOTOR = "04_MOTOR_CÁLCULO"

# Colunas por posição (mais robusto que por nome -- a planilha usa cabeçalhos
# de duas linhas com acentuação, ex.: "Relat.\nFinal"):
#   A=0 Cód.CNAE | K=10 Relat. Final (já limitada a 0,75-1,40 pelo Excel) | N=13 Fonte
_COL_CODIGO = 0
_COL_RELAT_FINAL = 10
_COL_FONTE = 13

# Piso e teto operacionais do fator CNAE único de lançamento (item 6.2.1 da
# memória técnica): 0,60 (desagravo máximo) a 1,15 (agravo máximo), aplicados
# aqui por cima da coluna "Relat. Final" da planilha compartilhada com o V4.
#
# ATENÇÃO: essa coluna já vem limitada pelo Excel aos limites ANTIGOS do V4
# (0,75-1,40, definidos na aba 01_PARÂMETROS, células C1/C2). Isso significa
# que um CNAE com relatividade bruta entre 0,60 e 0,75 chega aqui já travado
# em 0,75 -- o piso de 0,60 abaixo nunca é alcançado para esses casos. Decisão
# consciente (a alternativa seria ler a relatividade bruta pré-limite, coluna
# J, mas foi pedido explicitamente usar a "Relat. Final").
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
        "relat_final": pd.to_numeric(df.iloc[:, _COL_RELAT_FINAL], errors="coerce"),
        "fonte": df.iloc[:, _COL_FONTE],
    })
    tabela = tabela.dropna(subset=["relat_final"])
    return tabela.set_index("codigo")


_TABELA_CNAE = _carregar_tabela_cnae()


def consultar_cnae(codigo_cnae):
    """Retorna a relatividade final (Relat. Final, já limitada pelo Excel a
    0,75-1,40) e a fonte (FAP/MPS ou fallback CNAE-STG) para o código
    informado, ou None se o código não existir na tabela. Aceita formato
    numérico puro ou com máscara."""
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
    - CNAE encontrado: retorna a relatividade final (FAP/MPS ou fallback
      CNAE-STG, já limitada pelo Excel a 0,75-1,40) recortada ao intervalo
      [0,60 ; 1,15] (True) -- ver nota sobre o piso de 0,60 no comentário
      de PISO_CNAE acima.
    """
    info = consultar_cnae(codigo_cnae)

    if info is None:
        return 1.0, False

    relat_final = info.get("relat_final")

    if relat_final is None or (isinstance(relat_final, float) and pd.isna(relat_final)):
        return 1.0, False

    fator = max(PISO_CNAE, min(TETO_CNAE, float(relat_final)))
    return fator, True
