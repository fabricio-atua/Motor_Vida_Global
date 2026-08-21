import requests

BRASILAPI_CNPJ_URL = "https://brasilapi.com.br/api/cnpj/v1/{cnpj}"


def limpar_cnpj(cnpj):
    return "".join(filter(str.isdigit, cnpj))


def buscar_dados_cnpj(cnpj):
    """Consulta a BrasilAPI e retorna razão social, CNAE principal/secundários.

    Em caso de falha (CNPJ inválido, não encontrado ou erro de rede),
    retorna {"erro": <mensagem>} em vez de lançar exceção.
    """
    cnpj_limpo = limpar_cnpj(cnpj)

    if len(cnpj_limpo) != 14:
        return {"erro": "CNPJ inválido. Deve conter 14 dígitos."}

    try:
        resposta = requests.get(BRASILAPI_CNPJ_URL.format(cnpj=cnpj_limpo), timeout=8)
    except requests.RequestException:
        return {"erro": "Não foi possível conectar ao serviço de consulta de CNPJ."}

    if resposta.status_code == 404:
        return {"erro": "CNPJ não encontrado."}

    if resposta.status_code != 200:
        return {"erro": f"Erro ao consultar CNPJ (HTTP {resposta.status_code})."}

    dados = resposta.json()

    return {
        "cnpj": cnpj_limpo,
        "razao_social": dados.get("razao_social"),
        "nome_fantasia": dados.get("nome_fantasia"),
        "situacao_cadastral": dados.get("descricao_situacao_cadastral"),
        "cnae_codigo": dados.get("cnae_fiscal"),
        "cnae_descricao": dados.get("cnae_fiscal_descricao"),
        "cnaes_secundarios": dados.get("cnaes_secundarios") or [],
    }
