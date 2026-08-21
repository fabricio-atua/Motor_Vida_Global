def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def br_para_float(valor_str):
    try:
        return float(valor_str.replace(".", "").replace(",", "."))
    except:
        return 0.0
