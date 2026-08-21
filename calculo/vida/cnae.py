import os
import pandas as pd

_CAMINHO_TABELA = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "Tabelas", "tabela_cnae_completa_VG.xlsx"
))


def _carregar_tabela_cnae():
    df = pd.read_excel(_CAMINHO_TABELA, sheet_name="CNAE", dtype=str)
    # o Excel pode converter a coluna código pra número e comer o zero à
    # esquerda quando a planilha é editada manualmente — corrige na leitura.
    df["codigo"] = df["codigo"].str.strip().str.zfill(7)
    return df.set_index("codigo")


_TABELA_CNAE = _carregar_tabela_cnae()


def consultar_cnae(codigo_cnae):
    """Retorna a linha da tabela oficial (descrição, hierarquia e coeficiente)
    para o código informado, ou None se o código não existir na tabela.
    Aceita o código com ou sem zero à esquerda (ex: 600001 ou 0600001)."""
    codigo = str(codigo_cnae).strip().zfill(7)

    if codigo not in _TABELA_CNAE.index:
        return None

    return _TABELA_CNAE.loc[codigo].to_dict()


def fator_por_cnae(codigo_cnae):
    """Retorna (fator, cadastrado) lendo a coluna "coeficiente" da tabela
    Tabelas/tabela_cnae_completa_VG.xlsx para o CNAE informado.

    O "coeficiente" é derivado da coluna "classificacao_risco" (Baixo/Médio/Alto),
    atribuída por Grupo CNAE (3 dígitos) com base em risco ocupacional geral —
    uma classificação de bom senso, não
    uma transcrição literal do Anexo V do Decreto 3.048/99 ou de qualquer outra
    tabela oficial. Revisar/ajustar linha a linha na planilha antes de usar em
    produção; qualquer edição manual do "coeficiente" tem prioridade, já que a
    leitura é sempre feita diretamente dessa coluna.

    - CNAE não encontrado na tabela ou com "coeficiente" em branco:
      retorna (1.0, False) — fator neutro, ainda não classificado.
    - CNAE com "coeficiente" preenchido: retorna (valor, True).
    """
    info = consultar_cnae(codigo_cnae)

    if info is None:
        return 1.0, False

    coeficiente = info.get("coeficiente")

    if coeficiente is None or (isinstance(coeficiente, float) and pd.isna(coeficiente)):
        return 1.0, False

    return float(coeficiente), True
