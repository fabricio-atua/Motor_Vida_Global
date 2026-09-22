def run():

    import streamlit as st
    import os
    import base64
    from datetime import date, timedelta

    from calculo.vida_v3.engine import (
        premio_risco_cobertura_por_vida,
        premio_risco_funeral_por_vida,
        custo_aquisicao_anual,
        retencao_tarifaria,
        cadeia_unitaria,
    )
    from calculo.vida_v3.taxas import (
        DESCRICOES, TAXAS_TECNICAS, COBERTURAS_BLOQUEADAS,
        DESCRICOES_FUNERAL, LIMITES_FUNERAL,
    )
    from calculo.vida_v3 import parametros as p3
    from calculo.vida_v3.cnae import fator_por_cnae, consultar_cnae
    from utils.formatacao import moeda, br_para_float
    from utils.cnpj import buscar_dados_cnpj


    # -----------------------------
    # CONFIG LIMITES
    # -----------------------------

    CAPITAL_MAX_FUNC = 100_000
    CAPITAL_MAX_SOCIO = 250_000
    VIDAS_MAX = 600


    # -----------------------------
    # SESSION STATE (prefixo v3_ para não colidir com o motor V4)
    # -----------------------------

    if "v3_capital_func_txt" not in st.session_state:
        st.session_state.v3_capital_func_txt = "100.000,00"

    if "v3_capital_socio_txt" not in st.session_state:
        st.session_state.v3_capital_socio_txt = "200.000,00"

    if "v3_erro_func" not in st.session_state:
        st.session_state.v3_erro_func = False

    if "v3_erro_socio" not in st.session_state:
        st.session_state.v3_erro_socio = False

    if "v3_dados_cnpj" not in st.session_state:
        st.session_state.v3_dados_cnpj = None

    if "v3_data_inicio" not in st.session_state:
        st.session_state.v3_data_inicio = date.today()

    if "v3_data_termino" not in st.session_state:
        st.session_state.v3_data_termino = st.session_state.v3_data_inicio + timedelta(days=365)


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

        estourou = False

        if valor_float > limite:
            valor_float = limite
            estourou = True

        valor_formatado = f"{valor_float:,.2f}"
        valor_formatado = valor_formatado.replace(",", "X").replace(".", ",").replace("X", ".")

        st.session_state[key] = valor_formatado

        if key == "v3_capital_func_txt":
            st.session_state.v3_erro_func = estourou

        if key == "v3_capital_socio_txt":
            st.session_state.v3_erro_socio = estourou


    def atualizar_termino():
        st.session_state.v3_data_termino = st.session_state.v3_data_inicio + timedelta(days=365)


    def rotulo_campo(texto):
        st.markdown(
            f"<div style='font-weight:600; font-size:13px; line-height:1.3; "
            f"margin-bottom:6px; min-height:34px;'>{texto}</div>",
            unsafe_allow_html=True
        )


    def carregar_logo(caminho):
        with open(caminho, "rb") as f:
            return base64.b64encode(f.read()).decode()


    def aplicar_css_inputs():
        st.markdown("""
        <style>

        div[data-testid="stTextInput"] input {
            border-radius: 12px !important;
            background-color: #FFFFFF !important;
            border: 1px solid #d2d4d9 !important;
            color: #31333F !important;
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

        hr {
            margin: 8px 0 16px 0 !important;
        }

        h1, h2, h3 {
            margin-top: 0.2rem !important;
            margin-bottom: 0.2rem !important;
            padding-top: 4px !important;
            padding-bottom: 4px !important;
        }

        div[data-testid="stVerticalBlock"],
        div[data-testid="stHorizontalBlock"] {
            gap: 0.5rem !important;
        }

        div[data-testid="stMainBlockContainer"] {
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
        }

        div[data-testid="stMetricValue"] div {
            font-weight: 400 !important;
        }

        label[data-testid="stMetricLabel"] p {
            font-weight: 700 !important;
        }

        div[data-testid="stExpander"] summary p {
            color: #ff4b4b !important;
            font-weight: 700 !important;
            font-size: 18px !important;
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
            <h1 style="margin:0;">Simulador Vida em Grupo — V3</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.warning(
        "⚠ Taxas provisórias. As taxas dependem de validação do Atuário responsável antes de uso "
        "definitivo em produção."
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
            placeholder="00.000.000/0000-00",
            key="v3_cnpj_input"
        )

    with col_cnpj2:
        st.markdown("<div style='margin-top:28px'></div>", unsafe_allow_html=True)
        if st.button("Buscar CNPJ", key="v3_buscar_cnpj"):
            with st.spinner("Consultando CNPJ..."):
                st.session_state.v3_dados_cnpj = buscar_dados_cnpj(cnpj_input)

    dados_cnpj = st.session_state.v3_dados_cnpj
    fator_cnae = None

    if dados_cnpj is None:
        st.caption("Busque o CNPJ para identificar o CNAE e aplicar o fator único de relatividade ocupacional.")
    elif "erro" in dados_cnpj:
        st.error(dados_cnpj["erro"])
    else:
        fator_cnae, cnae_cadastrado = fator_por_cnae(dados_cnpj["cnae_codigo"])

        st.write(f"**Razão Social:** {dados_cnpj['razao_social']}")
        st.write(f"**CNAE:** {dados_cnpj['cnae_codigo']} — {dados_cnpj['cnae_descricao']}")
        st.write(f"**Porte:** {dados_cnpj.get('porte') or 'Não informado'}")
        st.write("**Fonte:** BrasilAPI (dados da Receita Federal)")

        if not cnae_cadastrado:
            st.warning(
                "Este CNAE não foi encontrado na tabela de relatividades "
                "(Tabelas/Motor_Relatividades_CNAE_v3.xlsx). Aplicando fator neutro (1,0000)."
            )


    # =====================================================
    # VIGÊNCIA E AQUISIÇÃO (AGENCIAMENTO + COMISSÃO)
    # =====================================================

    st.markdown("---")

    caixa_vigencia, caixa_aquisicao = st.columns(2)

    with caixa_vigencia:
        with st.container(border=True):
            st.markdown("**Vigência**")

            col_dt1, col_dt2 = st.columns(2)

            with col_dt1:
                st.date_input(
                    "Início",
                    key="v3_data_inicio",
                    format="DD/MM/YYYY",
                    on_change=atualizar_termino
                )

            with col_dt2:
                st.date_input(
                    "Término",
                    key="v3_data_termino",
                    format="DD/MM/YYYY"
                )

            dias_vigencia = (st.session_state.v3_data_termino - st.session_state.v3_data_inicio).days

            if dias_vigencia <= 0:
                meses_vigencia = None
            else:
                DIAS_POR_MES = 365.25 / 12
                meses_vigencia = round(dias_vigencia / DIAS_POR_MES)

    with caixa_aquisicao:
        with st.container(border=True):
            st.markdown("**Aquisição (Agenciamento + Comissão) — sempre 12 parcelas**")

            col_classe, col_comissao = st.columns(2)

            with col_classe:
                classe_agenciamento = st.selectbox(
                    "Agenciamento",
                    ["A", "B", "C"],
                    format_func=lambda c: p3.DESCRICOES_CLASSE_AGENCIAMENTO[c],
                    key="v3_classe_agenciamento"
                )

            with col_comissao:
                comissao_pct = st.number_input(
                    "Comissão (%)",
                    min_value=0.00,
                    max_value=35.00,
                    value=20.00,
                    step=0.01,
                    format="%.2f",
                    key="v3_comissao_pct"
                )

            parcelas_agenciamento = p3.PARCELAS_AGENCIAMENTO[classe_agenciamento]
            aquisicao_anual = custo_aquisicao_anual(parcelas_agenciamento, comissao_pct / 100)

            st.caption(
                f"Custo de aquisição anual: A = a/12 + c×(12−a)/12 = **{aquisicao_anual * 100:.4f}%** "
                f"(a={parcelas_agenciamento}, c={comissao_pct:.2f}%). Sem comissão nas parcelas de agenciamento."
            )

    if meses_vigencia is None:
        st.error("A Data de Término deve ser posterior à Data de Início.")


    # -----------------------------
    # COBERTURAS
    # -----------------------------

    st.markdown("---")

    st.subheader("Cobertura Básica")
    st.checkbox("MORTE (Obrigatória)", value=True, disabled=True)

    st.subheader("Coberturas Complementares")

    opcoes_complementares = {
        "IAC": DESCRICOES["IAC"],
        "IAF": DESCRICOES["IAF"],
    }

    complementares = []

    for codigo, descricao in opcoes_complementares.items():
        if st.checkbox(f"Cobertura: {descricao}", key=f"v3_comp_{codigo}"):
            complementares.append(codigo)

    iac_selecionado = "IAC" in complementares
    iaf_selecionado = "IAF" in complementares

    st.subheader("Coberturas Adicionais")

    def rotulo_disponibilidade(codigo):
        taxas = TAXAS_TECNICAS[codigo]
        if taxas["SOCIO"] is None and taxas["FUNC"] is not None:
            return " (somente Funcionários — sem taxa para Sócios)"
        if taxas["FUNC"] is None and taxas["SOCIO"] is not None:
            return " (somente Sócios — sem taxa para Funcionários)"
        return ""

    opcoes_adicionais = {
        codigo: descricao for codigo, descricao in DESCRICOES.items()
        if codigo not in ("MORTE", "IAC", "IAF") and codigo not in COBERTURAS_BLOQUEADAS
    }

    adicionais = []

    for codigo, descricao in opcoes_adicionais.items():
        if st.checkbox(f"Cobertura: {descricao}{rotulo_disponibilidade(codigo)}", key=f"v3_adic_{codigo}"):
            adicionais.append(codigo)

    if COBERTURAS_BLOQUEADAS:
        st.caption(
            "Bloqueadas nesta versão (sem taxa aprovada em nenhum segmento): "
            + ", ".join(sorted(COBERTURAS_BLOQUEADAS)) + "."
        )

    coberturas = ["MORTE"] + complementares + adicionais

    st.subheader("Assistência Funeral")
    st.caption("Precificação por vida e por limite contratado — sem distinção entre Funcionários e Sócios.")

    def campo_qtd_limite(chave_prefixo):
        col_qtd, col_limite = st.columns(2)
        with col_qtd:
            rotulo_campo("Quantidade de Vidas")
            qtd = st.number_input(
                f"{chave_prefixo}_qtd", min_value=0, max_value=VIDAS_MAX, value=0, step=1,
                label_visibility="collapsed", key=f"{chave_prefixo}_qtd"
            )
        with col_limite:
            rotulo_campo("Limite contratado")
            limite = st.selectbox(
                f"{chave_prefixo}_limite", LIMITES_FUNERAL, format_func=lambda v: moeda(v),
                label_visibility="collapsed", key=f"{chave_prefixo}_limite"
            )
        return qtd, limite

    col_af_ind, col_af_fam = st.columns(2)

    with col_af_ind:
        af_individual = st.checkbox(DESCRICOES_FUNERAL["INDIVIDUAL"], key="v3_af_individual")
        qtd_ind, limite_ind = 0, LIMITES_FUNERAL[0]
        if af_individual:
            qtd_ind, limite_ind = campo_qtd_limite("v3_af_ind")

    with col_af_fam:
        af_familiar = st.checkbox(DESCRICOES_FUNERAL["FAMILIAR"], key="v3_af_familiar")
        qtd_fam, limite_fam = 0, LIMITES_FUNERAL[0]
        if af_familiar:
            qtd_fam, limite_fam = campo_qtd_limite("v3_af_fam")

    funeral_selecionado = []

    if af_individual and qtd_ind > 0:
        funeral_selecionado.append(("INDIVIDUAL", limite_ind, qtd_ind))

    if af_familiar and qtd_fam > 0:
        funeral_selecionado.append(("FAMILIAR", limite_fam, qtd_fam))


    # =====================================================
    # FUNCIONÁRIOS E SÓCIOS
    # =====================================================

    st.markdown("---")

    caixa_func, caixa_socio = st.columns(2)

    num_campos_grupo = 2 + (1 if iac_selecionado else 0) + (1 if iaf_selecionado else 0)

    with caixa_func:
        with st.container(border=True):
            st.markdown("**Funcionários**")

            colunas_func = st.columns(num_campos_grupo)
            idx = 0

            with colunas_func[idx]:
                rotulo_campo("Quantidade de Vidas Totais")

                vidas_func = st.number_input(
                    "v3_vidas_func",
                    min_value=0,
                    max_value=VIDAS_MAX,
                    value=100,
                    step=1,
                    label_visibility="collapsed",
                    key="v3_vidas_func"
                )

                st.caption("Máx: 600 vidas")
            idx += 1

            qtd_conjuges_func = 0
            if iac_selecionado:
                with colunas_func[idx]:
                    rotulo_campo("Quantidade de Cônjuges")

                    qtd_conjuges_func = st.number_input(
                        "v3_qtd_conjuges_func",
                        min_value=0,
                        max_value=VIDAS_MAX,
                        value=50,
                        step=1,
                        label_visibility="collapsed",
                        key="v3_qtd_conjuges_func"
                    )
                idx += 1

            qtd_filhos_func = 0
            if iaf_selecionado:
                with colunas_func[idx]:
                    rotulo_campo("Quantidade de Filhos")

                    qtd_filhos_func = st.number_input(
                        "v3_qtd_filhos_func",
                        min_value=0,
                        max_value=VIDAS_MAX,
                        value=25,
                        step=1,
                        label_visibility="collapsed",
                        key="v3_qtd_filhos_func"
                    )
                idx += 1

            with colunas_func[idx]:
                rotulo_campo("Capital Segurado por Vida")

                st.text_input(
                    "v3_capital_func_txt",
                    key="v3_capital_func_txt",
                    on_change=formatar_input,
                    args=("v3_capital_func_txt", CAPITAL_MAX_FUNC),
                    label_visibility="collapsed"
                )

                st.markdown(
                    "<div style='font-size:13px; color:#ff4b4b;'>Máx: R$ 100.000,00</div>",
                    unsafe_allow_html=True
                )

                if st.session_state.v3_erro_func:
                    st.warning("O valor digitado excedia o limite e foi ajustado para R$ 100.000,00.")

    with caixa_socio:
        with st.container(border=True):
            st.markdown("**Sócios**")

            colunas_socio = st.columns(num_campos_grupo)
            idx = 0

            with colunas_socio[idx]:
                rotulo_campo("Quantidade de Vidas Totais")

                vidas_socio = st.number_input(
                    "v3_vidas_socio",
                    min_value=0,
                    max_value=VIDAS_MAX,
                    value=5,
                    step=1,
                    label_visibility="collapsed",
                    key="v3_vidas_socio"
                )

                st.caption("Máx: 600 vidas")
            idx += 1

            qtd_conjuges_socio = 0
            if iac_selecionado:
                with colunas_socio[idx]:
                    rotulo_campo("Quantidade de Cônjuges")

                    qtd_conjuges_socio = st.number_input(
                        "v3_qtd_conjuges_socio",
                        min_value=0,
                        max_value=VIDAS_MAX,
                        value=vidas_socio,
                        step=1,
                        label_visibility="collapsed",
                        key="v3_qtd_conjuges_socio"
                    )
                idx += 1

            qtd_filhos_socio = 0
            if iaf_selecionado:
                with colunas_socio[idx]:
                    rotulo_campo("Quantidade de Filhos")

                    qtd_filhos_socio = st.number_input(
                        "v3_qtd_filhos_socio",
                        min_value=0,
                        max_value=VIDAS_MAX,
                        value=vidas_socio,
                        step=1,
                        label_visibility="collapsed",
                        key="v3_qtd_filhos_socio"
                    )
                idx += 1

            with colunas_socio[idx]:
                rotulo_campo("Capital Segurado por Vida")

                st.text_input(
                    "v3_capital_socio_txt",
                    key="v3_capital_socio_txt",
                    on_change=formatar_input,
                    args=("v3_capital_socio_txt", CAPITAL_MAX_SOCIO),
                    label_visibility="collapsed"
                )

                st.markdown(
                    "<div style='font-size:13px; color:#ff4b4b;'>Máx: R$ 250.000,00</div>",
                    unsafe_allow_html=True
                )

                if st.session_state.v3_erro_socio:
                    st.warning("O valor digitado excedia o limite e foi ajustado para R$ 250.000,00.")


    # -----------------------------
    # BOTÃO CALCULAR
    # -----------------------------

    st.markdown("---")

    if st.button("Calcular Prêmio", key="v3_calcular"):

        capital_func = br_para_float(st.session_state.v3_capital_func_txt)
        capital_socio = br_para_float(st.session_state.v3_capital_socio_txt)

        total_vidas = vidas_func + vidas_socio

        if total_vidas == 0:
            st.error("Informe pelo menos 1 vida.")

        elif total_vidas < 2:
            st.error("O grupo mínimo exige ao menos 2 vidas (Funcionários + Sócios).")

        elif fator_cnae is None:
            st.error("Busque um CNPJ válido para identificar o CNAE antes de calcular.")

        elif meses_vigencia is None:
            st.error("Corrija a Vigência da Apólice (Data de Término deve ser posterior à Data de Início).")

        elif not coberturas and not funeral_selecionado:
            st.error("Selecione ao menos uma cobertura.")

        else:

            fator_porte_grupo = p3.fator_porte(dados_cnpj.get("codigo_porte"))
            retencao = retencao_tarifaria(aquisicao_anual)

            if retencao <= 0:
                st.error("Retenção tarifária inválida (≤ 0). Reduza a comissão e/ou o agenciamento.")
                st.stop()

            vidas_por_cobertura_func = {"IAC": qtd_conjuges_func, "IAF": qtd_filhos_func}
            vidas_por_cobertura_socio = {"IAC": qtd_conjuges_socio, "IAF": qtd_filhos_socio}

            def montar_itens(segmento, capital, coberturas_sel, vidas_padrao, vidas_por_cobertura):
                """Monta a lista de coberturas sobre capital de um segmento, já
                com a cadeia comercial aplicada. O Funeral não entra aqui -- não
                é segmentado por Funcionários/Sócios (ver montar_itens_funeral)."""
                itens = []

                for cobertura in coberturas_sel:
                    resultado = premio_risco_cobertura_por_vida(
                        capital, cobertura, segmento, fator_cnae, fator_porte_grupo
                    )
                    if resultado is None:
                        itens.append({
                            "codigo": cobertura,
                            "descricao": DESCRICOES[cobertura],
                            "disponivel": False,
                            "vidas": vidas_por_cobertura.get(cobertura, vidas_padrao),
                        })
                        continue

                    vidas_item = vidas_por_cobertura.get(cobertura, vidas_padrao)
                    passos_comercial, risco, comercial, final = cadeia_unitaria(resultado["premio"], retencao)

                    itens.append({
                        "codigo": cobertura,
                        "descricao": DESCRICOES[cobertura],
                        "disponivel": True,
                        "taxa": resultado["taxa"],
                        "subscricao_obrigatoria": resultado["subscricao_obrigatoria"],
                        "vidas": vidas_item,
                        "passos": resultado["passos_fatores"] + passos_comercial,
                        "risco": risco, "comercial": comercial, "final": final,
                    })

                return itens

            def montar_itens_funeral(funeral_sel):
                """Monta os itens de Auxílio Funeral, sem distinção de segmento --
                uma única quantidade de vidas e um único limite por modalidade."""
                itens = []

                for modalidade, limite, qtd_vidas in funeral_sel:
                    resultado = premio_risco_funeral_por_vida(modalidade, limite, fator_porte_grupo)
                    if resultado is None:
                        continue

                    passos_comercial, risco, comercial, final = cadeia_unitaria(resultado["premio"], retencao)

                    itens.append({
                        "codigo": f"AF_{modalidade}_{limite}",
                        "descricao": f"{DESCRICOES_FUNERAL[modalidade]} — limite {moeda(limite)}",
                        "taxa": resultado["taxa"],
                        "vidas": qtd_vidas,
                        "passos": resultado["passos_fatores"] + passos_comercial,
                        "risco": risco, "comercial": comercial, "final": final,
                    })

                return itens

            itens_func = montar_itens("FUNC", capital_func, coberturas, vidas_func, vidas_por_cobertura_func)
            itens_socio = montar_itens("SOCIO", capital_socio, coberturas, vidas_socio, vidas_por_cobertura_socio)
            itens_funeral = montar_itens_funeral(funeral_selecionado)

            def total_segmento(itens, chave):
                return round(sum(item[chave] * item["vidas"] for item in itens if item["disponivel"]), 2)

            def total_funeral(chave):
                return round(sum(item[chave] * item["vidas"] for item in itens_funeral), 2)

            premio_func_risco = total_segmento(itens_func, "risco")
            premio_func_comercial = total_segmento(itens_func, "comercial")
            premio_func_final = total_segmento(itens_func, "final")

            premio_socio_risco = total_segmento(itens_socio, "risco")
            premio_socio_comercial = total_segmento(itens_socio, "comercial")
            premio_socio_final = total_segmento(itens_socio, "final")

            premio_funeral_risco = total_funeral("risco")
            premio_funeral_comercial = total_funeral("comercial")
            premio_funeral_final = total_funeral("final")

            premio_risco_grupo = round(premio_func_risco + premio_socio_risco + premio_funeral_risco, 2)
            premio_comercial_grupo = round(premio_func_comercial + premio_socio_comercial + premio_funeral_comercial, 2)
            premio_final_grupo = round(premio_func_final + premio_socio_final + premio_funeral_final, 2)

            st.success("✅ Cotação Gerada com Sucesso")

            houve_subscricao_obrigatoria = any(
                item.get("subscricao_obrigatoria") for item in itens_func + itens_socio
            )
            if houve_subscricao_obrigatoria:
                st.warning(
                    "Capital individual em faixa de subscrição obrigatória (item 6.8.5 da memória técnica) — "
                    "encaminhar para análise de subscrição antes da emissão."
                )

            # -----------------------------
            # RESUMO
            # -----------------------------

            def linha_fina():
                st.markdown(
                    "<hr style='margin:6px 0; border:none; border-top:1px solid #2c2f36;'>",
                    unsafe_allow_html=True
                )

            linha_fina()
            st.subheader("Prêmio de Risco Anual")

            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Funcionários", moeda(premio_func_risco))
            r2.metric("Sócios", moeda(premio_socio_risco))
            r3.metric("Assistência Funeral", moeda(premio_funeral_risco))
            r4.metric("Total", moeda(premio_risco_grupo))

            st.markdown(
                "<div style='margin-top:-3px; font-size:14px; color:#ff4b4b;'>"
                "Prêmio de risco já com fator CNAE, fator de porte e fator de capital (só em Morte) — "
                "sem aquisição, carregamentos ou IOF.</div>",
                unsafe_allow_html=True
            )

            linha_fina()
            st.subheader("Prêmio Comercial sem IOF — Anual")

            r5, r6, r7, r8 = st.columns(4)
            r5.metric("Funcionários", moeda(premio_func_comercial))
            r6.metric("Sócios", moeda(premio_socio_comercial))
            r7.metric("Assistência Funeral", moeda(premio_funeral_comercial))
            r8.metric("Total", moeda(premio_comercial_grupo))

            linha_fina()
            st.subheader("Prêmio Final — Anual (com IOF)")

            r9, r10, r11, r12 = st.columns(4)
            r9.metric("Funcionários", moeda(premio_func_final))
            r10.metric("Sócios", moeda(premio_socio_final))
            r11.metric("Assistência Funeral", moeda(premio_funeral_final))
            r12.metric("Total", moeda(premio_final_grupo))

            linha_fina()
            st.subheader(f"Parcela Mensal ({p3.N_PARCELAS}x) — Vigência de {meses_vigencia:.0f} meses")

            parcela_mensal_grupo = round(premio_final_grupo / p3.N_PARCELAS, 2)
            st.metric(" ", moeda(parcela_mensal_grupo), label_visibility="collapsed")

            linha_fina()

            with st.expander("Composição Tarifária"):
                st.markdown(
                    f"- Aquisição (agenciamento + comissão): **{aquisicao_anual * 100:.4f}%**\n"
                    f"- Despesa Administrativa: **{p3.DESPESA_ADMINISTRATIVA * 100:.2f}%**\n"
                    f"- Margem: **{p3.MARGEM * 100:.2f}%**\n"
                    f"- PIS/COFINS: **{p3.PIS_COFINS * 100:.2f}%**\n"
                    f"- IOF (aplicado após a formação do comercial): **{p3.IOF * 100:.2f}%**\n"
                    f"- Fator CNAE: **{fator_cnae:.5f}**\n"
                    f"- Fator de Porte ({dados_cnpj.get('porte') or 'NÃO INFORMADO'}): **{fator_porte_grupo:.5f}**\n"
                )

            # -----------------------------
            # DETALHAMENTO
            # -----------------------------

            st.subheader("Depurador das taxas por Cobertura (Por Vida / Anual)")

            LARGURAS_COLUNAS = ["30%", "15%", "15%", "20%", "20%"]

            def linha_html(col1, col2, col3, col4, col5, negrito=False):
                peso = "font-weight:bold;" if negrito else ""
                celulas = [col1, col2, col3, col4, col5]
                divs = "".join(
                    f"<div style='flex:0 0 {LARGURAS_COLUNAS[i]}; padding:2px 8px; "
                    f"box-sizing:border-box; {peso}'>{celulas[i]}</div>"
                    for i in range(5)
                )
                return f"<div style='display:flex; align-items:center;'>{divs}</div>"

            st.markdown(
                linha_html("<strong>Descrição</strong>", "<strong>Taxa/Funcionários</strong>",
                           "<strong>Taxa/Sócios</strong>", "<strong>Funcionários (por vida)</strong>",
                           "<strong>Sócios (por vida)</strong>"),
                unsafe_allow_html=True
            )
            st.markdown("<hr style='margin-top:2px;margin-bottom:4px;'>", unsafe_allow_html=True)

            def linha_detalhe(descricao, taxa_func_texto, taxa_soc_texto, valor_func, valor_soc, destaque=False):
                taxa_func_conteudo = taxa_func_texto if taxa_func_texto else "&nbsp;"
                taxa_soc_conteudo = taxa_soc_texto if taxa_soc_texto else "&nbsp;"
                if not destaque:
                    descricao = f"<span style='color:#9aa0a6'>{descricao}</span>"
                st.markdown(
                    linha_html(descricao, taxa_func_conteudo, taxa_soc_conteudo,
                               moeda(valor_func), moeda(valor_soc), negrito=destaque),
                    unsafe_allow_html=True
                )

            codigos_exibidos = []
            for item in itens_func:
                if item["codigo"] not in codigos_exibidos:
                    codigos_exibidos.append(item["codigo"])
            for item in itens_socio:
                if item["codigo"] not in codigos_exibidos:
                    codigos_exibidos.append(item["codigo"])

            por_codigo_func = {item["codigo"]: item for item in itens_func}
            por_codigo_socio = {item["codigo"]: item for item in itens_socio}

            for codigo in codigos_exibidos:
                item_f = por_codigo_func.get(codigo)
                item_s = por_codigo_socio.get(codigo)
                descricao = (item_f or item_s)["descricao"]

                disponivel_f = item_f is not None and item_f["disponivel"]
                disponivel_s = item_s is not None and item_s["disponivel"]

                def formatar_taxa(item):
                    if item is None:
                        return ""
                    return f"{item['taxa'] * 100:.5f}%"

                taxa_func_texto = formatar_taxa(item_f) if disponivel_f else ""
                taxa_soc_texto = formatar_taxa(item_s) if disponivel_s else ""

                linha_detalhe(
                    descricao, taxa_func_texto, taxa_soc_texto,
                    item_f["risco"] if disponivel_f else 0.0,
                    item_s["risco"] if disponivel_s else 0.0,
                    destaque=True
                )

                if not disponivel_f and item_f is None and item_s is not None:
                    linha_detalhe("Sem taxa para Funcionários — não precificada", "", "", 0.0, 0.0)
                if not disponivel_s and item_s is None and item_f is not None:
                    linha_detalhe("Sem taxa para Sócios — não precificada", "", "", 0.0, 0.0)

                passos_f = item_f["passos"] if disponivel_f else []
                passos_s = item_s["passos"] if disponivel_s else []
                max_passos = max(len(passos_f), len(passos_s))

                for i in range(max_passos):
                    passo_f = passos_f[i] if i < len(passos_f) else None
                    passo_s = passos_s[i] if i < len(passos_s) else None
                    referencia = passo_f or passo_s

                    fator_f = passo_f["fator"] if passo_f else None
                    fator_s = passo_s["fator"] if passo_s else None
                    taxa_func_txt = f"{fator_f:.5f}" if fator_f is not None else ""
                    taxa_soc_txt = f"{fator_s:.5f}" if fator_s is not None else ""

                    linha_detalhe(
                        referencia["label"], taxa_func_txt, taxa_soc_txt,
                        passo_f["valor"] if passo_f else 0.0,
                        passo_s["valor"] if passo_s else 0.0,
                        destaque=referencia.get("destaque", False)
                    )

                st.markdown("<hr style='margin-top:6px;margin-bottom:6px;'>", unsafe_allow_html=True)

            # -----------------------------
            # DEPURADOR DO FUNERAL (sem segmentação Funcionários/Sócios)
            # -----------------------------

            if itens_funeral:
                st.subheader("Depurador do Auxílio Funeral (grupo total)")

                LARGURAS_FUNERAL = ["36%", "18%", "23%", "23%"]

                def linha_html_funeral(col1, col2, col3, col4, negrito=False):
                    peso = "font-weight:bold;" if negrito else ""
                    celulas = [col1, col2, col3, col4]
                    divs = "".join(
                        f"<div style='flex:0 0 {LARGURAS_FUNERAL[i]}; padding:2px 8px; "
                        f"box-sizing:border-box; {peso}'>{celulas[i]}</div>"
                        for i in range(4)
                    )
                    return f"<div style='display:flex; align-items:center;'>{divs}</div>"

                st.markdown(
                    linha_html_funeral("<strong>Descrição</strong>", "<strong>Taxa/Fator</strong>",
                                        "<strong>Valor por Vida</strong>", "<strong>Valor Total</strong>"),
                    unsafe_allow_html=True
                )
                st.markdown("<hr style='margin-top:2px;margin-bottom:4px;'>", unsafe_allow_html=True)

                def linha_funeral(descricao, taxa_texto, valor_vida, valor_total, destaque=False):
                    if not destaque:
                        descricao = f"<span style='color:#9aa0a6'>{descricao}</span>"
                    st.markdown(
                        linha_html_funeral(descricao, taxa_texto or "&nbsp;", moeda(valor_vida), moeda(valor_total), negrito=destaque),
                        unsafe_allow_html=True
                    )

                for item in itens_funeral:
                    linha_funeral(
                        f"{item['descricao']} — {item['vidas']} vida(s)", "Valor Fixo por IS",
                        item["risco"], round(item["risco"] * item["vidas"], 2), destaque=True
                    )

                    for passo in item["passos"]:
                        fator = passo["fator"]
                        taxa_txt = f"{fator:.5f}" if fator is not None else ""
                        linha_funeral(
                            passo["label"], taxa_txt, passo["valor"],
                            round(passo["valor"] * item["vidas"], 2),
                            destaque=passo.get("destaque", False)
                        )

                    st.markdown("<hr style='margin-top:6px;margin-bottom:6px;'>", unsafe_allow_html=True)
