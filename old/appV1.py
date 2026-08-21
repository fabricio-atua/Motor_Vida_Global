import streamlit as st
import os
import streamlit.components.v1 as components
import base64

if "capital_txt" not in st.session_state:
    st.session_state.capital_txt = "50.000,00"

from calculo.engine import calcula_premio_grupo
from calculo.taxas import DESCRICOES
from utils.formatacao import moeda


# -----------------------------
# CONFIG
# -----------------------------

CAPITAL_MAX = 250_000
CAPITAL_MIN = 1000

VIDAS_MAX = 600
VIDAS_MIN = 1


def moeda_para_float(valor):
    valor = valor.replace(".", "").replace(",", ".")
    return float(valor)


st.set_page_config(
    page_title="Simulador Vida em Grupo",
    layout="centered"
)

import base64

def carregar_logo(caminho):
    with open(caminho, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "img", "New_logo.png")

logo_base64 = carregar_logo(logo_path)

st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 5px;">
        <img src="data:image/png;base64,{logo_base64}" width="120">
        <h1 style="margin: 0;">Simulador Vida em Grupo</h1>
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown("---")

# -----------------------------
# CAPITAL COM MÁSCARA
# -----------------------------

st.subheader("Capital Segurado por Vida (R$)")

capital_html = f"""
<input 
    type="text" 
    value="{st.session_state.capital_txt}"
    style="
        width: 100%;
        padding: 0.75rem;
        font-size: 1rem;
        border-radius: 10px;
        border: 1px solid #333;
        background-color: #0e1117;
        color: white;
    "
    oninput="
        let v = this.value.replace(/\\D/g,'');

        if (v === '') {{
            this.value = '0,00';
            return;
        }}

        let num = parseFloat(v) / 100;

        // LIMITE MÁXIMO = 250.000
        if (num > 250000) {{
            num = 250000;
        }}

        num = num.toFixed(2) + '';
        num = num.replace('.', ',');
        num = num.replace(/(\\d)(?=(\\d{{3}})+(?!\\d))/g, '$1.');

        this.value = num;
    "
/>
"""

components.html(capital_html, height=65)

st.caption("Valor máximo de Capital Segurado Permitido: R$ 250.000,00.")

# Converte para float
try:
    capital = float(
        st.session_state.capital_txt
        .replace(".", "")
        .replace(",", ".")
    )
except:
    capital = 0


st.markdown("---")
# -----------------------------
# QUANTIDADE DE VIDAS
# -----------------------------

st.subheader("Quantidade de Vidas")

vidas = st.number_input(
    "vidas",
    min_value=VIDAS_MIN,
    max_value=VIDAS_MAX,
    value=100,
    step=1,
    label_visibility="collapsed"
)
st.caption("Limite máximo permitido: 600 vidas")

st.markdown("---")

# -----------------------------
# COBERTURA BÁSICA
# -----------------------------

st.subheader("Cobertura Básica")

st.checkbox("MORTE (Obrigatória)", value=True, disabled=True)


# -----------------------------
# COBERTURAS ADICIONAIS
# -----------------------------
st.subheader("Coberturas Adicionais")

opcoes_adicionais = {
    "IEA": DESCRICOES["IEA"],
    "IPA": DESCRICOES["IPA"],
    "IPTA": DESCRICOES["IPTA"],
    "IPDF": DESCRICOES["IPDF"],
    "IPDL": DESCRICOES["IPDL"],
    "AF": DESCRICOES["AF"],
    "DMHO": DESCRICOES["DMHO"],
    "DMH": DESCRICOES["DMH"]
}

adicionais = []

for codigo, descricao in opcoes_adicionais.items():
    marcado = st.checkbox(descricao)

    if marcado:
        adicionais.append(codigo)

# Junta com básica obrigatória
coberturas = ["MORTE"] + adicionais

st.markdown("---")

# -----------------------------
# BOTÃO CALCULAR
# -----------------------------
if st.button("Calcular Prêmio"):

    # VALIDAÇÕES
    if capital < CAPITAL_MIN:
        st.error("Capital mínimo permitido: R$ 1.000,00")

    elif capital > CAPITAL_MAX:
        st.error("Capital máximo permitido: R$ 250.000,00")

    elif vidas < VIDAS_MIN:
        st.error("Quantidade mínima de vidas: 1")

    elif vidas > VIDAS_MAX:
        st.error("Quantidade máxima permitida: 600 vidas")

    else:

        premio_vida, premio_grupo, detalhes = calcula_premio_grupo(
            capital,
            coberturas,
            vidas
        )

        st.success("✅ Cotação Gerada com Sucesso")

        st.metric(
            label="Prêmio Mensal por Vida",
            value=moeda(premio_vida)
        )

        st.metric(
            label="Prêmio Mensal do Grupo",
            value=moeda(premio_grupo)
        )

        st.subheader("Detalhamento por Cobertura (por vida)")

        for cobertura, dados in detalhes.items():
            st.write(
                f"**{cobertura}** | "
                f"Taxa: {dados['taxa']*100:.5f}% | "
                f"Prêmio: {moeda(dados['premio'])}"
            )


#rode este trecho no terminal para apaarecer o Motor Vida Global
# streamlit run calculo/app.py  