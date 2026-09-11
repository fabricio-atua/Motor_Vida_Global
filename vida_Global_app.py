def run():

    import streamlit as st
    import os
    import base64
    from datetime import date, timedelta

    from calculo.vida.engine import calcula_premio_grupo
    from calculo.vida.taxas import DESCRICOES, TABELA_COMISSIONAMENTO, faixa_comissao, CARREGAMENTOS, TRIBUTACAO
    from calculo.vida.cnae import fator_por_cnae, consultar_cnae
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

    if "data_inicio" not in st.session_state:
        st.session_state.data_inicio = date.today()

    if "data_termino" not in st.session_state:
        st.session_state.data_termino = st.session_state.data_inicio + timedelta(days=365)


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


    def atualizar_termino():
        st.session_state.data_termino = st.session_state.data_inicio + timedelta(days=365)


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

        /* layout mais compacto: reduz espaçamento entre seções */
        hr {
            margin: 8px 0 !important;
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
        info_cnae = consultar_cnae(dados_cnpj["cnae_codigo"])

        st.write(f"**Razão Social:** {dados_cnpj['razao_social']}")
        st.write(f"**CNAE:** {dados_cnpj['cnae_codigo']} — {dados_cnpj['cnae_descricao']}")

        if not cnae_cadastrado:
            st.warning(
                "Este CNAE não foi encontrado na tabela de relatividades "
                "(Tabelas/Motor_Relatividades_CNAE_v3.xlsx). Aplicando fator neutro (1.00)."
            )
        elif info_cnae.get("Fonte") == "CNAE-STG":
            st.caption(
                f"Classe de risco: {info_cnae.get('Classe')} — relatividade "
                f"{fator_cnae:.5f} (sem dado FAP/MPS para esta subclasse; "
                "usando fallback do coeficiente CNAE-STG)."
            )
        else:
            st.caption(
                f"Classe de risco: {info_cnae.get('Classe')} — relatividade "
                f"{fator_cnae:.5f} (calculada via FAP/MPS)."
            )


    # =====================================================
    # VIGÊNCIA E COMISSIONAMENTO
    # =====================================================

    st.markdown("---")

    DESCRICOES_CLASSE = {
        "A": "A — Sem agenciamento antecipado",
        "B": "B — Agenciamento de 100% no 1º mês",
        "C": "C — Agenciamento de 100% no 1º e 2º mês",
    }

    caixa_vigencia, caixa_comissionamento = st.columns(2)

    with caixa_vigencia:
        with st.container(border=True):
            st.markdown("**Vigência**")

            col_dt1, col_dt2 = st.columns(2)

            with col_dt1:
                st.date_input(
                    "Início",
                    key="data_inicio",
                    format="DD/MM/YYYY",
                    on_change=atualizar_termino
                )

            with col_dt2:
                st.date_input(
                    "Término",
                    key="data_termino",
                    format="DD/MM/YYYY"
                )

            dias_vigencia = (st.session_state.data_termino - st.session_state.data_inicio).days

            if dias_vigencia <= 0:
                meses_vigencia = None
            else:
                DIAS_POR_MES = 365.25 / 12
                meses_vigencia = dias_vigencia / DIAS_POR_MES

    with caixa_comissionamento:
        with st.container(border=True):
            st.markdown("**Comissionamento**")

            col_classe, col5 = st.columns(2)

            with col_classe:
                classe_corretor = st.selectbox(
                    "Classe do Corretor",
                    ["A", "B", "C"],
                    format_func=lambda c: DESCRICOES_CLASSE[c]
                )

            with col5:
                comissao_pct = st.number_input(
                    "Comissão (%)",
                    min_value=0.01,
                    max_value=50.00,
                    value=20.00,
                    step=0.01,
                    format="%.2f"
                )

    if meses_vigencia is None:
        st.error("A Data de Término deve ser posterior à Data de Início.")

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
    # FUNCIONÁRIOS E SÓCIOS
    # =====================================================

    st.markdown("---")

    caixa_func, caixa_socio = st.columns(2)

    with caixa_func:
        with st.container(border=True):
            st.markdown("**Funcionários**")

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

                st.markdown(
                    "<div style='font-size:16px; color:#ff4b4b;'>Capital máximo permitido: R$ 100.000,00</div>",
                    unsafe_allow_html=True
                )

                if st.session_state.erro_func:
                    st.warning("O valor digitado excedia o limite e foi ajustado para R$ 100.000,00.")

    with caixa_socio:
        with st.container(border=True):
            st.markdown("**Sócios**")

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

                st.markdown(
                    "<div style='font-size:16px; color:#ff4b4b;'>Capital máximo permitido: R$ 250.000,00</div>",
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

    st.subheader("Coberturas Complementares")

    st.caption(
        "Estendem a cobertura de Morte ao cônjuge (IAC) e aos filhos dependentes (IAF), "
        "usando o mesmo capital segurado e a mesma quantidade de vidas do grupo "
        "(Funcionários/Sócios) ao qual se aplicam."
    )

    opcoes_complementares = {
        "IAC": DESCRICOES["IAC"],
        "IAF": DESCRICOES["IAF"],
    }

    complementares = []

    for codigo, descricao in opcoes_complementares.items():
        if st.checkbox(f"Cobertura: {descricao}"):
            complementares.append(codigo)

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
        if st.checkbox(f"Cobertura: {descricao}"):
            adicionais.append(codigo)

    coberturas = ["MORTE"] + complementares + adicionais


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

        elif meses_vigencia is None:
            st.error("Corrija a Vigência da Apólice (Data de Término deve ser posterior à Data de Início).")

        else:

            premio_func_vida, premio_func_total, detalhes_func = calcula_premio_grupo(
                capital_func, coberturas, vidas_func
            )

            premio_socio_vida, premio_socio_total, detalhes_socios = calcula_premio_grupo(
                capital_socio, coberturas, vidas_socio
            )

            # Prêmio Puro = prêmio base já com o efeito do CNAE (mesma definição usada no depurador)
            premio_func_puro = round(premio_func_total * fator_cnae, 2)
            premio_socio_puro = round(premio_socio_total * fator_cnae, 2)
            premio_puro_grupo = round(premio_func_puro + premio_socio_puro, 2)

            # Formação da Taxa Comercial pela NTA (item 13): gross-up por divisão,
            # TC = TP / (1 − β − T), um carregamento por vez (Despesas Administrativas,
            # Margem de Lucro, Pró-Labore); agenciamento/corretagem (β_age/β_cor) seguem
            # via TABELA_COMISSIONAMENTO/comissão digitada, como camada à parte.
            fator_carregamento_liquido = 1.0
            for beta in CARREGAMENTOS.values():
                fator_carregamento_liquido *= 1 / (1 - beta)

            fator_comissao_digitada = 1 + (comissao_pct / 100)

            fator_liquido = fator_carregamento_liquido * coeficiente * fator_comissao_digitada

            fator_bruto = fator_liquido
            for tributo in TRIBUTACAO.values():
                fator_bruto *= 1 / (1 - tributo)

            premio_func_liquido = round(premio_func_puro * fator_liquido, 2)
            premio_socio_liquido = round(premio_socio_puro * fator_liquido, 2)
            premio_liquido_grupo = round(premio_func_liquido + premio_socio_liquido, 2)

            premio_func_bruto = round(premio_func_puro * fator_bruto, 2)
            premio_socio_bruto = round(premio_socio_puro * fator_bruto, 2)
            premio_bruto_grupo = round(premio_func_bruto + premio_socio_bruto, 2)

            st.success("✅ Cotação Gerada com Sucesso")

            # -----------------------------
            # RESUMO
            # -----------------------------

            def linha_fina():
                st.markdown(
                    "<hr style='margin:6px 0; border:none; border-top:1px solid #2c2f36;'>",
                    unsafe_allow_html=True
                )

            linha_fina()
            st.subheader("Prêmio Puro - Total Geral")

            r1, r2, r3 = st.columns(3)

            r1.metric("Prêmio Funcionários", moeda(premio_func_puro))
            r2.metric("Prêmio Sócios", moeda(premio_socio_puro))
            r3.metric("Prêmio Puro Total", moeda(premio_puro_grupo))

            st.markdown(
            "<div style='margin-top:-3px; font-size:16px; color:#ff4b4b;'>Nota: Prêmio Puro já com o fator do CNAE, sem inclusão de carregamentos.</div>",
            unsafe_allow_html=True)

            linha_fina()

            st.subheader("Prêmio Líquido - Total Geral")

            r4, r5, r6 = st.columns(3)

            r4.metric("Prêmio Líquido Funcionários", moeda(premio_func_liquido))
            r5.metric("Prêmio Líquido Sócios", moeda(premio_socio_liquido))
            r6.metric("Prêmio Líquido Total do Grupo", moeda(premio_liquido_grupo))

            linha_fina()

            st.subheader("Prêmio Bruto - Total")

            r7, r8, r9 = st.columns(3)

            r7.metric("Prêmio Bruto Funcionários", moeda(premio_func_bruto))
            r8.metric("Prêmio Bruto Sócios", moeda(premio_socio_bruto))
            r9.metric("Prêmio Bruto Total do Grupo", moeda(premio_bruto_grupo))

            linha_fina()

            if meses_vigencia is not None:

                st.subheader("Prêmio Bruto Projetado - Vigência")

                premio_bruto_projetado = round(premio_bruto_grupo * meses_vigencia, 2)

                st.metric(
                    f"Prêmio Bruto Total da Vigência ({meses_vigencia:.1f} meses)",
                    moeda(premio_bruto_projetado)
                )

                st.markdown(
                    "<div style='margin-top:-3px; font-size:16px; color:#ff4b4b;'>"
                    "Nota: projeção simples (Prêmio Bruto mensal × meses de vigência), "
                    "sem recálculo atuarial da taxa para o período.</div>",
                    unsafe_allow_html=True
                )

                linha_fina()

            # -----------------------------
            # DETALHAMENTO
            # -----------------------------


            st.subheader("Depurador das taxas por Cobertura (Por Vida)")

            st.caption(
                "Depurador de cálculo: mostra, linha a linha, a evolução da taxa e do "
                "prêmio de cada cobertura"
            )

            LARGURAS_COLUNAS = ["39%", "20.3%", "20.3%", "20.3%"]

            def linha_html(col1, col2, col3, col4, negrito=False):
                peso = "font-weight:bold;" if negrito else ""
                celulas = [col1, col2, col3, col4]
                divs = "".join(
                    f"<div style='flex:0 0 {LARGURAS_COLUNAS[i]}; padding:2px 8px; "
                    f"box-sizing:border-box; {peso}'>{celulas[i]}</div>"
                    for i in range(4)
                )
                return f"<div style='display:flex; align-items:center;'>{divs}</div>"

            st.markdown(
                linha_html("<strong>Descrição</strong>", "<strong>Taxa Mensal</strong>",
                           "<strong>Funcionários</strong>", "<strong>Sócios</strong>"),
                unsafe_allow_html=True
            )

            st.markdown(
                "<hr style='margin-top:2px;margin-bottom:4px;'>",
                unsafe_allow_html=True
            )

            def linha_detalhe(descricao, taxa_texto, valor_func, valor_soc, destaque=False):
                taxa_conteudo = taxa_texto if taxa_texto else "&nbsp;"

                if not destaque:
                    descricao = f"<span style='color:#9aa0a6'>{descricao}</span>"

                st.markdown(
                    linha_html(descricao, taxa_conteudo, moeda(valor_func), moeda(valor_soc), negrito=destaque),
                    unsafe_allow_html=True
                )

            resumo_coberturas = []

            for cobertura in detalhes_func.keys():

                taxa_base = detalhes_func[cobertura]["taxa"]
                premio_func_puro = detalhes_func[cobertura]["premio"]
                premio_soc_puro = detalhes_socios[cobertura]["premio"]

                linha_detalhe(
                    DESCRICOES[cobertura], f"{taxa_base * 100:.5f}",
                    premio_func_puro, premio_soc_puro, destaque=True
                )

                taxa_acumulada = taxa_base * fator_cnae
                func_acumulado = premio_func_puro * fator_cnae
                soc_acumulado = premio_soc_puro * fator_cnae

                linha_detalhe(
                    "↳ CNAE",
                    f"{fator_cnae:.5f}", func_acumulado, soc_acumulado
                )

                linha_detalhe(
                    "Prêmio Puro", "",
                    func_acumulado, soc_acumulado, destaque=True
                )

                resumo_puro_func, resumo_puro_soc = func_acumulado, soc_acumulado

                # Despesas Administrativas, Margem de Lucro, Pró-Labore -> Prêmio Líquido
                # (gross-up por divisão, um carregamento por linha, conforme NTA item 13)
                for nome_carregamento, beta in CARREGAMENTOS.items():

                    fator_carregamento = 1 / (1 - beta)

                    taxa_acumulada *= fator_carregamento
                    func_acumulado *= fator_carregamento
                    soc_acumulado *= fator_carregamento

                    linha_detalhe(
                        f"↳ {nome_carregamento}",
                        f"{fator_carregamento:.5f}", func_acumulado, soc_acumulado
                    )

                linha_detalhe(
                    "Prêmio Líquido", "",
                    round(func_acumulado, 2), round(soc_acumulado, 2), destaque=True
                )

                # Comissão -> Prêmio Líquido (após o fator de comissão)
                taxa_acumulada *= coeficiente
                func_acumulado *= coeficiente
                soc_acumulado *= coeficiente

                linha_detalhe(
                    "↳ Comissão",
                    f"{coeficiente:.5f}", func_acumulado, soc_acumulado
                )

                fator_comissao_digitada = 1 + (comissao_pct / 100)
                taxa_acumulada *= fator_comissao_digitada
                func_acumulado *= fator_comissao_digitada
                soc_acumulado *= fator_comissao_digitada

                linha_detalhe(
                    "↳ Comissão Digitada",
                    f"{fator_comissao_digitada:.5f}", func_acumulado, soc_acumulado
                )

                linha_detalhe(
                    "Prêmio Líquido", "",
                    round(func_acumulado, 2), round(soc_acumulado, 2), destaque=True
                )

                resumo_liquido_func = round(func_acumulado, 2)
                resumo_liquido_soc = round(soc_acumulado, 2)

                # Tributação (IOF e encargos) -> Prêmio Bruto (gross-up por divisão, NTA item 12)
                for nome_tributo, tributo in TRIBUTACAO.items():

                    fator_tributo = 1 / (1 - tributo)

                    taxa_acumulada *= fator_tributo
                    func_acumulado *= fator_tributo
                    soc_acumulado *= fator_tributo

                    linha_detalhe(
                        f"↳ {nome_tributo}",
                        f"{fator_tributo:.5f}", func_acumulado, soc_acumulado
                    )

                linha_detalhe(
                    "Prêmio Bruto", "",
                    round(func_acumulado, 2), round(soc_acumulado, 2), destaque=True
                )

                resumo_coberturas.append({
                    "cobertura": cobertura,
                    "taxa_base": taxa_base,
                    "puro_func": premio_func_puro, "puro_soc": premio_soc_puro,
                    "cnae_func": resumo_puro_func, "cnae_soc": resumo_puro_soc,
                    "liquido_func": resumo_liquido_func, "liquido_soc": resumo_liquido_soc,
                    "bruto_func": round(func_acumulado, 2), "bruto_soc": round(soc_acumulado, 2),
                })

                st.markdown(
                    "<hr style='margin-top:6px;margin-bottom:6px;'>",
                    unsafe_allow_html=True
                )

            st.markdown("---")

            # -----------------------------
            # RESUMO DO CÁLCULO POR COBERTURA
            # -----------------------------
            # Desativado a pedido do usuário (2026-08-24): a explicação em bullets
            # já foi validada, mas por ora fica oculta. Trocar para True reativa.

            EXIBIR_RESUMO_POR_COBERTURA = False

            if EXIBIR_RESUMO_POR_COBERTURA:

                st.subheader("Resumo do Cálculo por Cobertura")

                st.caption(
                    "Explicação simplificada de como o prêmio de cada cobertura é calculado, "
                    "passo a passo, do prêmio puro ao prêmio bruto final."
                )

                percentual_cnae_resumo = (fator_cnae - 1) * 100
                fator_tributacao_total = 1.0
                for tributo in TRIBUTACAO.values():
                    fator_tributacao_total *= 1 / (1 - tributo)
                percentual_iof_resumo = (fator_tributacao_total - 1) * 100

                def moeda_md(valor):
                    return moeda(valor).replace("$", "\\$")

                for item in resumo_coberturas:
                    st.markdown(f"**{item['cobertura']}**")
                    st.markdown(
                        f"- Capital × Taxa ({item['taxa_base'] * 100:.5f}%) = "
                        f"{moeda_md(item['puro_func'])} / {moeda_md(item['puro_soc'])}\n"
                        f"- Desconto/Agravo CNAE ({percentual_cnae_resumo:+.2f}%) = "
                        f"{moeda_md(item['cnae_func'])} / {moeda_md(item['cnae_soc'])}\n"
                        f"- Carregamentos e Comissão ({comissao_pct:.2f}%) = "
                        f"{moeda_md(item['liquido_func'])} / {moeda_md(item['liquido_soc'])}\n"
                        f"- IOF ({percentual_iof_resumo:+.2f}%) = "
                        f"{moeda_md(item['bruto_func'])} / {moeda_md(item['bruto_soc'])} (Prêmio Bruto final)"
                    )
                    st.markdown(
                        "<hr style='margin-top:6px;margin-bottom:6px;'>",
                        unsafe_allow_html=True
                    )
