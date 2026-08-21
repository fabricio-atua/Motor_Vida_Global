def run():
    import streamlit as st
    import os
    import base64
    import pandas as pd

    from calculo.vida_Individual.engine import calcula_premio_individual, FATOR_CAPITAL, FATOR_AJUSTE
    from calculo.vida_Individual.taxas import TAXAS, IOF, DESCRICOES
    
    
    from utils.formatacao import moeda, br_para_float

    CAPITAL_MAX = 250_000  # valor máximo do capital segurado

        # -----------------------------
    # SESSION STATE
    # -----------------------------
    if "capital_txt" not in st.session_state:
        st.session_state.capital_txt = "100.000,00"  # valor default do LMI

    # -----------------------------
    # FUNÇÕES
    # -----------------------------
    def formatar_input(key, limite):
        texto = st.session_state[key]
        numeros = "".join(filter(str.isdigit, texto))
        if numeros == "":
            st.session_state[key] = "0,00"
            return
        numeros = numeros[-9:]
        valor_float = int(numeros) / 100
        if valor_float > limite:
            valor_float = limite
        valor_formatado = f"{valor_float:,.2f}"
        valor_formatado = valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")
        st.session_state[key] = valor_formatado

    def carregar_logo(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()

    # -----------------------------
    # LOGO
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(BASE_DIR, "img", "New_logo.png")
    logo_base64 = carregar_logo(logo_path)

    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:12px;">
            <img src="data:image/png;base64,{logo_base64}" width="120">
            <h1 style="margin:0;">Simulador Vida Individual</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")


    # =====================================================
    # SEGURADO
    # =====================================================
    st.subheader("Segurado")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        idade = st.number_input("Idade", min_value=14, max_value=60, value=35, step=5)

    with col2:
        sexo = st.selectbox("Sexo", options=["Selecione a Opção", "Masculino", "Feminino"], index=0)

    with col3:
        st.markdown("Capital Segurado")
        
        # Inicializa session state apenas se ainda não existir
        if "capital_txt" not in st.session_state:
            st.session_state.capital_txt = "100.000,00"

        # Aqui não passamos value se já existe no session state
        st.text_input(
            "capital_txt",
            key="capital_txt",
            on_change=formatar_input,
            args=("capital_txt", CAPITAL_MAX),
            label_visibility="collapsed"
        )
        
        st.caption(f"Capital máximo: R$ {CAPITAL_MAX:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
    # =====================================================
    # COMISSÃO
    # =====================================================
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        comissao = st.number_input("Comissão (%)", min_value=0.0, max_value=100.0, value=10.0)

    # =====================================================
    # COBERTURAS
    # =====================================================
    st.markdown("---")
    st.subheader("Cobertura Básica")
    st.checkbox("M - Morte (Obrigatória)", value=True, disabled=True)

    st.subheader("Coberturas Adicionais")
    adicionais = []
    opcoes = {k: DESCRICOES[k] for k in ["MA","IPA","DC","DG","DIH","DIHU","DMHO","DIT","DITAD","IFPTD","FF"] if k in DESCRICOES}
    for codigo, descricao in opcoes.items():
        if st.checkbox(descricao):
            adicionais.append(codigo)

    coberturas = ["M"] + adicionais

    # =====================================================
    # BOTÃO CALCULAR
    # =====================================================
    st.markdown("---")
    if st.button("Calcular Prêmio"):
        # converte capital para float
        capital = br_para_float(st.session_state.capital_txt)
        if capital > CAPITAL_MAX:
            st.error(f"Capital não pode ultrapassar R$ {CAPITAL_MAX:,.2f}")
            return

        if capital == 0:
            st.error("Informe o capital segurado.")
            return

        # verifica se o sexo foi selecionado
        if sexo == "Selecione a Opção":
            st.error("Selecione o sexo do segurado para calcular o prêmio.")
            return
        sexo_abrev = "F" if sexo == "Feminino" else "M"

        # cálculo do prêmio usando o motor
        premio_puro, detalhes = calcula_premio_individual(capital, idade, sexo_abrev, coberturas)
        premio_total = premio_puro * (1 + comissao / 100) * (1 + IOF)

        st.success("✅ Cotação Gerada com Sucesso")

        # ==================================================
        # TABELA DETALHADA
        # ==================================================
        
        st.markdown("---")
        st.subheader("Resumo Técnico")
        dados = []
        todas = sorted(detalhes.keys(), key=lambda x: (x != "M", x))
        total_adicionais = 0

        for cob in todas:
            taxa = detalhes[cob]["taxa"]
            
            premio_risco = detalhes[cob]["premio"]

            fator_ajuste = FATOR_AJUSTE.get(cob, 1)

            # 🔹 ajuste técnico (% real)
            ajuste_tecnico = fator_ajuste - 1

            # 🔹 prêmio técnico
            premio_tecnico = premio_risco * fator_ajuste

            # 🔹 comercial e final
            premio_comercial = premio_tecnico * (1 + comissao / 100)
            premio_final = premio_comercial * (1 + IOF)

            if cob != "M":
                total_adicionais += premio_final

            tipo = "Básica" if cob == "M" else "Adicionais"

            fator = FATOR_CAPITAL.get(cob, 1)
            fator_formatado = f"{fator:.0%} do Capital"

            dados.append({
                "Idade": idade,
                "Sexo": sexo,
                "Cobertura": tipo,
                "Desc. Cobertura": DESCRICOES.get(cob, cob),
                "Fator Capital": fator_formatado,
                "Taxa": taxa,
                "Prêmio Risco": premio_risco,
                "Ajuste Técnico": ajuste_tecnico,  # 👈 CORRETO
                "Prêmio Técnico": premio_tecnico,
                "Comissão": comissao,
                "Prêmio Comercial": premio_comercial,
                "IOF": IOF,
                "Prêmio Final (ano)": premio_final
            })
            
            tabela = pd.DataFrame(dados)

        st.dataframe(
            tabela.style.format({
                "Taxa": "{:.4%}",
                "Prêmio Risco": "R$ {:,.2f}",
                "Ajuste Técnico": "{:.2%}",
                "Prêmio Técnico": "R$ {:,.2f}",   # 👈 NOVO
                "Comissão": "{:.2f}%",
                "Prêmio Comercial": "R$ {:,.2f}",
                "IOF": "{:.4%}",
                "Prêmio Final (ano)": "R$ {:,.2f}"
            }).hide(axis="index")
        )

        # ==================================================
        # RESUMO EXECUTIVO
        # ==================================================
        st.markdown("---")
        st.subheader("Resumo Executivo")

        # 🔹 Cobertura Básica
        linha_basica = tabela.loc[tabela["Cobertura"] == "Básica"].iloc[0]
        idade_basica = linha_basica["Idade"]
        sexo_basica = linha_basica["Sexo"]
        taxa_final_basica = linha_basica["Taxa"]
        premio_final_basica = linha_basica["Prêmio Final (ano)"]

        # 🔹 Total coberturas adicionais
        premio_final_adicionais = tabela.loc[tabela["Cobertura"] == "Adicionais", "Prêmio Final (ano)"].sum()

        # 🔹 Prêmio total geral
        premio_total_geral = premio_final_basica + premio_final_adicionais

        # 🔹 Prêmio comercial total (Básica + Adicionais)
        premio_comercial_total = tabela["Prêmio Comercial"].sum()

        # 🔹 Exibição formatada
        st.markdown(f"""
        **Cobertura Básica**  
        - Idade: {idade_basica}  
        - Sexo: {sexo_basica}  
        - Prêmio Risco: R$ {linha_basica['Prêmio Risco']:,.2f}  
        - Prêmio Técnico: R$ {linha_basica['Prêmio Técnico']:,.2f}  
        - Comissão: {linha_basica['Comissão']:,.2f}%  
        - Prêmio Comercial: R$ {linha_basica['Prêmio Comercial']:,.2f}  
        - Prêmio Final (ano): R$ {premio_final_basica:,.2f}

        **Coberturas Adicionais (Total)**  
        - Prêmio Final (ano): R$ {premio_final_adicionais:,.2f}

        ### 💰 Prêmio Total (Ano): R$ {premio_total_geral:,.2f}
        """)