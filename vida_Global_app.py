def run():

    import streamlit as st
    import os
    import base64

    from calculo.vida.engine import calcula_premio_grupo
    from calculo.vida.taxas import DESCRICOES, TABELA_COMISSIONAMENTO, faixa_comissao, CARREGAMENTOS
    from calculo.vida.cnae import fator_por_cnae
    from utils.formatacao import moeda, br_para_float
    from utils.cnpj import buscar_dados_cnpj


    # -----------------------------
    # CONFIG LIMITES
    # -----------------------------

    CAPITAL_MAX_FUNC = 100_000
    CAPITAL_MAX_SOCIO = 250_000
    VIDAS_MAX = 600


    # -----------------------------
    # SESSION STATE
    # -----------------------------

    if "capital_func_txt" not in st.session_state:
        st.session_state.capital_func_txt = "100.000,00"

    if "capital_socio_txt" not in st.session_state:
        st.session_state.capital_socio_txt = "200.000,00"

    if "erro_func" not in st.session_state:
        st.session_state.erro_func = False

    if "erro_socio" not in st.session_state:
        st.session_state.erro_socio = False

    if "dados_cnpj" not in st.session_state:
        st.session_state.dados_cnpj = None


    # -----------------------------
    # FUNÇÕES
    # -----------------------------

    def formatar_input(key, limite):

        texto = st.session_state[key]

        # mantém só números
        numeros = "".join(filter(str.isdigit, texto))

        if numeros == "":
            st.session_state[key] = "0,00"
            return

        # impede número absurdo digitando
        numeros = numeros[-9:]

        valor_float = int(numeros) / 100

        estourou = False

        if valor_float > limite:
            valor_float = limite
            estourou = True

        valor_formatado = f"{valor_float:,.2f}"
        valor_formatado = valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")

        st.session_state[key] = valor_formatado

        if key == "capital_func_txt":
            st.session_state.erro_func = estourou

        if key == "capital_socio_txt":
            st.session_state.erro_socio = estourou


    def carregar_logo(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()


    def aplicar_css_inputs():
        st.markdown("""
        <style>

        div[data-testid="stTextInput"] input {
            border-radius: 12px !important;
            background-color: #0e1117 !important;
            border: 1px solid #2c2f36 !important;
            color: white !important;
            padding-left: 42px !important;
        }

        .prefix-rs {
            position: relative;
        }

        .prefix-rs:before {
            content: "R$";
            position: absolute;
            left: 12px;
            top: 9px;
            color: #9aa0a6;
            font-size: 14px;
            pointer-events: none;
        }

        </style>
        """, unsafe_allow_html=True)


    aplicar_css_inputs()

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
            <h1 style="margin:0;">Simulador Vida em Grupo</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")


    # =====================================================
    # EMPRESA SEGURADA (CNPJ / CNAE)
    # =====================================================

    st.subheader("Empresa Segurada")

    col_cnpj1, col_cnpj2 = st.columns([3, 1])

    with col_cnpj1:
        cnpj_input = st.text_input(
            "CNPJ da Empresa",
            placeholder="00.000.000/0000-00"
        )

    with col_cnpj2:
        st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)
        if st.button("Buscar CNPJ"):
            with st.spinner("Consultando CNPJ..."):
                st.session_state.dados_cnpj = buscar_dados_cnpj(cnpj_input)

    dados_cnpj = st.session_state.dados_cnpj
    fator_cnae = None

    if dados_cnpj is None:
        st.caption("Busque o CNPJ para identificar o CNAE e aplicar o agravo/desconto por atividade.")
    elif "erro" in dados_cnpj:
        st.error(dados_cnpj["erro"])
    else:
        fator_cnae, cnae_cadastrado = fator_por_cnae(dados_cnpj["cnae_codigo"])

        st.write(f"**Razão Social:** {dados_cnpj['razao_social']}")
        st.write(f"**CNAE:** {dados_cnpj['cnae_codigo']} — {dados_cnpj['cnae_descricao']}")

        if not cnae_cadastrado:
            st.warning(
                "Este CNAE ainda não tem coeficiente cadastrado na tabela "
                "(Tabelas/tabela_cnae_completa_VG.xlsx). Aplicando fator neutro (1.00)."
            )


    # =====================================================
    # COMISSIONAMENTO
    # =====================================================

    st.markdown("---")
    st.subheader("Comissionamento")

    DESCRICOES_CLASSE = {
        "A": "A — Sem agenciamento antecipado",
        "B": "B — Agenciamento de 100% no 1º mês",
        "C": "C — Agenciamento de 100% no 1º e 2º mês",
    }

    col_classe, col5 = st.columns(2)

    with col_classe:
        classe_corretor = st.selectbox(
            "Classe do Corretor",
            ["A", "B", "C"],
            format_func=lambda c: DESCRICOES_CLASSE[c]
        )

    with col5:
        comissao_pct = st.number_input(
            "Comissão do Corretor (%)",
            min_value=0.01,
            max_value=50.00,
            value=20.00,
            step=0.01,
            format="%.2f"
        )

    tier_comissao = faixa_comissao(comissao_pct / 100)
    codigo_operacao = f"{tier_comissao}-{classe_corretor}" if tier_comissao else None
    dados_coeficiente = TABELA_COMISSIONAMENTO.get(codigo_operacao)

    if dados_coeficiente is None:
        st.error(
            f"Não há coeficiente cadastrado para a Classe {classe_corretor} "
            f"na faixa de comissão até {tier_comissao}%."
            if tier_comissao else
            "Comissão fora da faixa permitida (0,01% a 50,00%)."
        )
        coeficiente = None
    else:
        coeficiente = dados_coeficiente["coeficiente"]


    # =====================================================
    # FUNCIONÁRIOS
    # =====================================================

    st.markdown("---")
    st.subheader("Funcionários")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("**Quantidade de Vidas**")

        vidas_func = st.number_input(
            "vidas_func",
            min_value=0,
            max_value=VIDAS_MAX,
            value=100,
            step=1,
            label_visibility="collapsed"
        )

        st.caption("Limite máximo: 600 vidas")


    with col2:

        st.markdown("**Capital Segurado por Vida**")

        st.text_input(
            "capital_func_txt",
            key="capital_func_txt",
            on_change=formatar_input,
            args=("capital_func_txt", CAPITAL_MAX_FUNC),
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
        "<div style='margin-top:-20px; font-size:16px; color:#ff4b4b;'>Capital máximo permitido: R$ 100.000,00</div>",
        unsafe_allow_html=True
    )

        if st.session_state.erro_func:
            st.warning("O valor digitado excedia o limite e foi ajustado para R$ 100.000,00.")

    # =====================================================
    # SÓCIOS
    # =====================================================

    st.markdown("---")
    st.subheader("Sócios")

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("**Quantidade de Vidas**")

        vidas_socio = st.number_input(
            "vidas_socio",
            min_value=0,
            max_value=VIDAS_MAX,
            value=5,
            step=1,
            label_visibility="collapsed"
        )

        st.caption("Limite máximo: 600 vidas")

    with col4:

        st.markdown("**Capital Segurado por Vida**")

        st.text_input(
            "capital_socio_txt",
            key="capital_socio_txt",
            on_change=formatar_input,
            args=("capital_socio_txt", CAPITAL_MAX_SOCIO),
            label_visibility="collapsed"
        )

        st.markdown("</div>", unsafe_allow_html=True)


        st.markdown(
        "<div style='margin-top:-20px; font-size:16px; color:#ff4b4b;'>Capital máximo permitido: R$ 250.000,00</div>",
        unsafe_allow_html=True
    )

        if st.session_state.erro_socio:
            st.warning("O valor digitado excedia o limite e foi ajustado para R$ 250.000,00.")


    # -----------------------------
    # COBERTURAS
    # -----------------------------

    st.markdown("---")

    st.subheader("Cobertura Básica")
    st.checkbox("MORTE (Obrigatória)", value=True, disabled=True)

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
        if st.checkbox(descricao):
            adicionais.append(codigo)

    coberturas = ["MORTE"] + adicionais


    # -----------------------------
    # BOTÃO CALCULAR
    # -----------------------------

    st.markdown("---")

    if st.button("Calcular Prêmio"):

        capital_func = br_para_float(st.session_state.capital_func_txt)
        capital_socio = br_para_float(st.session_state.capital_socio_txt)

        total_vidas = vidas_func + vidas_socio

        if total_vidas == 0:
            st.error("Informe pelo menos 1 vida.")

        elif fator_cnae is None:
            st.error("Busque um CNPJ válido para identificar o CNAE antes de calcular.")

        elif coeficiente is None:
            st.error("Ajuste a comissão e/ou a classe do corretor para um código válido antes de calcular.")

        else:

            premio_func_vida, premio_func_total, detalhes_func = calcula_premio_grupo(
                capital_func, coberturas, vidas_func
            )

            premio_socio_vida, premio_socio_total, detalhes_socios = calcula_premio_grupo(
                capital_socio, coberturas, vidas_socio
            )

            premio_grupo = premio_func_total + premio_socio_total

            premio_func_comercial = round(premio_func_total * fator_cnae * coeficiente, 2)
            premio_socio_comercial = round(premio_socio_total * fator_cnae * coeficiente, 2)
            premio_comercial_grupo = round(premio_func_comercial + premio_socio_comercial, 2)

            fator_carregamento_total = 1.0
            for fator_carregamento in CARREGAMENTOS.values():
                fator_carregamento_total *= fator_carregamento

            premio_func_final = round(premio_func_comercial * fator_carregamento_total, 2)
            premio_socio_final = round(premio_socio_comercial * fator_carregamento_total, 2)
            premio_final_grupo = round(premio_func_final + premio_socio_final, 2)

            st.success("✅ Cotação Gerada com Sucesso")

            # -----------------------------
            # RESUMO
            # -----------------------------

            st.markdown("---")
            st.subheader("Resumo - Prêmio Puro")

            r1, r2, r3 = st.columns(3)

            r1.metric("Prêmio Funcionários", moeda(premio_func_total))
            r2.metric("Prêmio Sócios", moeda(premio_socio_total))
            r3.metric("Prêmio Puro Total", moeda(premio_grupo))

            st.markdown(
            "<div style='margin-top:-3px; font-size:16px; color:#ff4b4b;'>Nota: Prêmio Puro, sem inclusão de carregamentos.</div>",
            unsafe_allow_html=True)

            st.markdown("---")

            st.subheader(f"Resumo - Prêmio Comercial (Código {codigo_operacao})")

            r4, r5, r6 = st.columns(3)

            r4.metric("Prêmio Comercial Funcionários", moeda(premio_func_comercial))
            r5.metric("Prêmio Comercial Sócios", moeda(premio_socio_comercial))
            r6.metric("Prêmio Comercial Total do Grupo", moeda(premio_comercial_grupo))

            st.markdown("---")

            st.subheader("Resumo - Prêmio Final (com Carregamentos)")

            r7, r8, r9 = st.columns(3)

            r7.metric("Prêmio Final Funcionários", moeda(premio_func_final))
            r8.metric("Prêmio Final Sócios", moeda(premio_socio_final))
            r9.metric("Prêmio Final Total do Grupo", moeda(premio_final_grupo))

            st.markdown("---")

            # -----------------------------
            # DETALHAMENTO
            # -----------------------------


            st.subheader("Detalhamento do Prêmio Puro por Cobertura (por Vida)")

            st.caption(
                "Depurador de cálculo: mostra, linha a linha, a evolução da taxa e do "
                "prêmio de cada cobertura"
            )

            h1, h2, h3, h4 = st.columns([2.5, 1.3, 1.3, 1.3])

            h1.markdown("**Descrição**")
            h2.markdown("**Taxa**")
            h3.markdown("**Funcionários**")
            h4.markdown("**Sócios**")

            st.markdown(
                "<hr style='margin-top:2px;margin-bottom:8px;'>",
                unsafe_allow_html=True
            )

            percentual_cnae = (fator_cnae - 1) * 100

            def linha_detalhe(descricao, taxa_texto, valor_func, valor_soc, destaque=False):
                c1, c2, c3, c4 = st.columns([2.5, 1.3, 1.3, 1.3])

                if destaque:
                    c1.write(f"**{descricao}**")
                else:
                    c1.markdown(
                        f"<span style='color:#9aa0a6'>{descricao}</span>",
                        unsafe_allow_html=True
                    )

                c2.write(taxa_texto)
                c3.write(moeda(valor_func))
                c4.write(moeda(valor_soc))

            for cobertura in detalhes_func.keys():

                taxa_base = detalhes_func[cobertura]["taxa"]
                premio_func_puro = detalhes_func[cobertura]["premio"]
                premio_soc_puro = detalhes_socios[cobertura]["premio"]

                taxa_cnae = taxa_base * fator_cnae
                premio_func_cnae = premio_func_puro * fator_cnae
                premio_soc_cnae = premio_soc_puro * fator_cnae

                premio_func_comercial_cob = round(premio_func_cnae * coeficiente, 2)
                premio_soc_comercial_cob = round(premio_soc_cnae * coeficiente, 2)

                linha_detalhe(
                    cobertura, f"{taxa_base * 100:.5f}%",
                    premio_func_puro, premio_soc_puro, destaque=True
                )

                linha_detalhe(
                    f"↳ CNAE ({percentual_cnae:+.2f}%)",
                    f"{taxa_cnae * 100:.5f}%", premio_func_cnae, premio_soc_cnae
                )

                linha_detalhe(
                    f"↳ Comissionamento (Comissão: {comissao_pct:.2f}%) — Prêmio Comercial",
                    f"{coeficiente:.5f}", premio_func_comercial_cob, premio_soc_comercial_cob
                )

                premio_func_acumulado = premio_func_comercial_cob
                premio_soc_acumulado = premio_soc_comercial_cob

                for nome_carregamento, fator_carregamento in CARREGAMENTOS.items():

                    premio_func_acumulado = premio_func_acumulado * fator_carregamento
                    premio_soc_acumulado = premio_soc_acumulado * fator_carregamento

                    linha_detalhe(
                        f"↳ {nome_carregamento} ({(fator_carregamento - 1) * 100:+.2f}%)",
                        f"{fator_carregamento:.5f}", premio_func_acumulado, premio_soc_acumulado
                    )

                taxa_bruta_pct = taxa_base * fator_cnae * coeficiente * fator_carregamento_total * 100

                linha_detalhe(
                    "↳ Prêmio Bruto",
                    f"{taxa_bruta_pct:.5f}%",
                    round(premio_func_acumulado, 2), round(premio_soc_acumulado, 2)
                )

                st.markdown(
                    "<hr style='margin-top:6px;margin-bottom:6px;'>",
                    unsafe_allow_html=True
                )

            st.markdown("---")
