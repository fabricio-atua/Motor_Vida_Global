import streamlit as st
from pathlib import Path
from utils.formatacao import moeda 
import pandas as pd


from calculo.transporte.taxas import (
    TAXA_BASE,
    IOF,
    FATOR_UF,
    COBERTURAS_ADICIONAIS,
    TBL_VIAGENS_MES,
    TBL_DISTANCIA, # A Principo não utilizado, mas pode ser interessante para futuras melhorias
    TBL_NOTURNO,
    TBL_ROTA_CRITICA,
    TBL_IDADE_FROTA,
    TBL_PCT_TERCEIROS,
    TBL_VALOR_SINISTRO,
    MERCADORIAS
)

def run():

    # -----------------------------
    # LOGO
    # -----------------------------
    BASE_DIR = Path(__file__).resolve().parent
    logo_path = BASE_DIR / "img" / "New_logo.png"

    if logo_path.exists():
        st.image(str(logo_path), width=120)
    else:
        st.warning("Logo não encontrado na pasta img.")

    st.title("COTAÇÃO AUTOMÁTICA - Transporte (RCTR-C / RC-DC)")
    
    st.markdown("---")

    # =====================================
    # 1) Produto / Comissão / GR
    # =====================================
    st.header("Produto e GR")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        produto = st.selectbox(
            "Produto",
            ["RCTR-C", "RC-DC", "RCTR-C + RC-DC"]
        )

    with col2:
        comissao = st.number_input(
            "Comissão do corretor (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0
        )

    with col3:
        possui_gr = st.selectbox("Possui GR?", ["Sim", "Não"])

    with col4:
        empresa_gr = None
        if possui_gr == "Sim":
            lista_empresas_gr = ["Buonny","GRISTEC","BRK","Omnilink","SASCAR","Outra"]
            empresa_gr = st.selectbox("Empresa de GR", [""] + lista_empresas_gr)
            if empresa_gr == "Outra":
                empresa_gr = st.text_input("Informe o nome da empresa")

    st.markdown("---")

    # =====================================
    # 2) Função Bloco de Viagens
    # =====================================
    def bloco_viagens(tipo_produto):
        st.header(f"Informações de Viagens - {tipo_produto}")

        col1, col2, col3 = st.columns(3)

        with col1:
            valor_mensal = st.number_input(
                f"Valor transportado mensal (R$)",
                min_value=0.0,
                value=2000000.0,
                step=50000.0,
                format="%.2f",
                key=f"valor_mensal_{tipo_produto}"
            )

        with col2:
            viagens_mes = st.selectbox(
                f"Viagens por mês",
                list(TBL_VIAGENS_MES.keys()),
                key=f"viagens_mes_{tipo_produto}"
            )

        with col3:
            maior_valor_viagem = st.number_input(
                f"Maior valor por viagem (R$)",
                min_value=0.0,
                value=80000.0,
                step=50000.0,
                format="%.2f",
                key=f"maior_valor_viagem_{tipo_produto}"
            )

        st.write("Valor mensal:", moeda(valor_mensal))
        st.write("Maior valor por viagem:", moeda(maior_valor_viagem))

        # Busca fator de viagens na tabela
        fator_viagens = TBL_VIAGENS_MES[viagens_mes]
        fator_rctr = fator_viagens["f_rctr"]
        fator_rcdc = fator_viagens["f_rcdc"]

        return {
            "valor_mensal": valor_mensal,
            "viagens_mes": viagens_mes,
            "maior_valor_viagem": maior_valor_viagem,
            "fator_rctr": fator_rctr,
            "fator_rcdc": fator_rcdc
        }

    # =====================================
    # Chamadas dos Blocos de Viagens
    dados_rctr = None
    dados_rcdc = None

    if produto == "RCTR-C":
        dados_rctr = bloco_viagens("RCTR-C")

    elif produto == "RC-DC":
        dados_rcdc = bloco_viagens("RC-DC")

    elif produto == "RCTR-C + RC-DC":
        dados_rctr = bloco_viagens("RCTR-C")
        st.divider()  # separador visual
        dados_rcdc = bloco_viagens("RC-DC")

    st.markdown("---")

    # =====================================
    # 3) Mercadorias
    # =====================================
    st.header("Mercadorias Transportadas")

    # Inicializa lista e controle de linhas
    if "num_linhas_merc" not in st.session_state:
        st.session_state.num_linhas_merc = 1

    mercadorias = []
    mix_total = 0

    opcoes_mercadorias = {codigo: dados["descricao"] for codigo, dados in MERCADORIAS.items()}
    lista_codigos = [""] + list(opcoes_mercadorias.keys())

    # Renderiza dinamicamente as linhas
    for i in range(st.session_state.num_linhas_merc):
        col1, col2 = st.columns([3, 1])

        with col1:
            codigo_merc = st.selectbox(
                f"Mercadoria {i+1}",
                options=lista_codigos,
                format_func=lambda x: "Selecione a Mercadoria" if x == "" else opcoes_mercadorias[x],
                key=f"merc_{i}"
            )

        with col2:
            mix = st.number_input(
                f"Mix % {i+1}",
                min_value=0.0,
                max_value=100.0,
                step=1.0,
                key=f"mix_{i}"
            )

        if codigo_merc != "":
            f_rctr = MERCADORIAS[codigo_merc]["f_rctr"]
            f_rcdc = MERCADORIAS[codigo_merc]["f_rcdc"]

            mercadorias.append({
                "codigo": codigo_merc,
                "descricao": opcoes_mercadorias[codigo_merc],
                "mix": mix,
                "f_rctr": f_rctr,
                "f_rcdc": f_rcdc
            })

            # Se ainda não atingiu 5 linhas, adiciona mais uma linha quando a atual for preenchida
            if st.session_state.num_linhas_merc < 5  and i == st.session_state.num_linhas_merc - 1:
                st.session_state.num_linhas_merc += 1

        mix_total += mix

    # Mostra total do mix
    st.write("Total Mix (%):", round(mix_total, 2))

    if mix_total > 100:
        st.error("⚠ O total do mix não pode ultrapassar 100%")
    elif mix_total < 100:
        st.warning("O total do mix ainda não atingiu 100%")
    else:
        st.success("✔ Total do mix fechado em 100%")

    st.markdown("---")

    # =====================================
    # 4) Rotas
    # =====================================
    st.header("Rotas")

    # Inicializa controle de linhas dinâmicas
    if "num_linhas_rotas" not in st.session_state:
        st.session_state.num_linhas_rotas = 1

    rotas = []
    soma_rotas = 0
    ufs_disponiveis = [""] + list(FATOR_UF.keys())

    # Renderiza dinamicamente as linhas
    for i in range(st.session_state.num_linhas_rotas):
        col1, col2, col3 = st.columns(3)

        with col1:
            uf_origem = st.selectbox(
                f"UF Origem {i+1}",
                options=ufs_disponiveis,
                key=f"origem_{i}"
            )

        with col2:
            uf_destino = st.selectbox(
                f"UF Destino {i+1}",
                options=ufs_disponiveis,
                key=f"destino_{i}"
            )

        with col3:
            pct = st.number_input(
                f"% Viagens {i+1}",
                min_value=0.0,
                max_value=100.0,
                step=1.0,
                key=f"pct_{i}"
            )

        soma_rotas += pct

        if uf_origem != "" and uf_destino != "":
            # Buscar fatores para origem e destino
            fator_origem_rctr = FATOR_UF.get(uf_origem, {}).get("fator_RCTR", 1.0)
            fator_destino_rctr = FATOR_UF.get(uf_destino, {}).get("fator_RCTR", 1.0)
            fator_origem_rcdc = FATOR_UF.get(uf_origem, {}).get("fator_RCDC", 1.0)
            fator_destino_rcdc = FATOR_UF.get(uf_destino, {}).get("fator_RCDC", 1.0)

            rotas.append({
                "origem": uf_origem,
                "destino": uf_destino,
                "percentual": pct,
                "fator_origem_rctr": fator_origem_rctr,
                "fator_destino_rctr": fator_destino_rctr,
                "fator_origem_rcdc": fator_origem_rcdc,
                "fator_destino_rcdc": fator_destino_rcdc
            })

            # Se ainda não atingiu 5 linhas e estamos na última linha preenchida, adiciona próxima
            if st.session_state.num_linhas_rotas < 5 and i == st.session_state.num_linhas_rotas - 1:
                st.session_state.num_linhas_rotas += 1

    # Mostrar soma das rotas
    st.write("Soma % rotas:", round(soma_rotas, 2))

    if soma_rotas > 100:
        st.error("⚠ A soma das rotas não pode ultrapassar 100%")
    elif soma_rotas < 100:
        st.warning("A soma das rotas ainda não atingiu 100%")
    else:
        st.success("✔ Soma das rotas fechada em 100%")

    #########################################################
    # 4.1) Operação Noturna e Rota Crítica

    st.subheader("Informações Complementares da Viagem")

    col1, col2, col3, col4 = st.columns(4)

    #########################################################
    # COLUNA 1 - NOTURNO
    with col1:
        opcoes_noturno = list(TBL_NOTURNO.keys())

        def _label_faixa_noturna(x):
            faixa_min, faixa_max = TBL_NOTURNO[x]["faixa"]
            faixa_max_str = "Acima de 60%" if faixa_max == float("inf") else f"{faixa_max}%"
            return f"{faixa_min}% a {faixa_max_str}"

        faixa_noturna = st.selectbox(
            "Viagens noturnas (faixa)",
            options=opcoes_noturno,
            format_func=_label_faixa_noturna
        )

        fator_noturno_rctr = TBL_NOTURNO[faixa_noturna]["f_rctr"]
        fator_noturno_rcdc = TBL_NOTURNO[faixa_noturna]["f_rcdc"]

    #########################################################
    # COLUNA 2 - ROTA CRÍTICA
    with col2:
        opcoes_rota_critica = list(TBL_ROTA_CRITICA.keys())

        rota_critica = st.selectbox(
            "Rota Crítica",
            options=opcoes_rota_critica
        )

        fator_rota_rctr = TBL_ROTA_CRITICA[rota_critica]["f_rctr"]
        fator_rota_rcdc = TBL_ROTA_CRITICA[rota_critica]["f_rcdc"]

    st.markdown("---")

    # =====================================
    # 5) Frota
    # =====================================
    st.header("Frota")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        idade_frota = st.selectbox(
            "Idade média da frota",
            list(TBL_IDADE_FROTA.keys())
        )
        # Buscar fatores da idade da frota
        fator_idade_rctr = TBL_IDADE_FROTA[idade_frota]["f_rctr"]
        fator_idade_rcdc = TBL_IDADE_FROTA[idade_frota]["f_rcdc"]

    with col2:
        pct_terceiros = st.selectbox(
            "% terceiros/agregados",
            list(TBL_PCT_TERCEIROS.keys())
        )
        # Buscar fatores da % de terceiros
        fator_terceiros_rctr = TBL_PCT_TERCEIROS[pct_terceiros]["f_rctr"]
        fator_terceiros_rcdc = TBL_PCT_TERCEIROS[pct_terceiros]["f_rcdc"]

    st.markdown("---")

    # =====================================
    # 6) Sinistros (últimos 36 meses)
    # =====================================
    st.header("Sinistros (últimos 36 meses)")

    # Inicializa variáveis
    valor_total_sinistros = 0.0
    houve_roubo = "Não"
    valor_roubo = 0.0
    qtd_sinistros = 0

    # Primeiras 2 informações em colunas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        teve_sinistro = st.radio("Teve sinistro?", ["Não", "Sim"], index=0, horizontal=True)

    with col2:
        if teve_sinistro == "Sim":
            qtd_sinistros = st.number_input(
                "Qtd de sinistros",
                min_value=1,
                step=1
            )

    with col3:
        if teve_sinistro == "Sim":
            valor_total_sinistros = st.number_input(
                "Valor total de sinistros 36m (R$)",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                value=valor_total_sinistros
            )

    # Sub-colunas para roubo/desaparecimento
    subcol1, subcol2 = st.columns([1, 1])
    with subcol1:
        houve_roubo = st.radio(
            "Roubo/desaparecimento?",
            ["Não", "Sim"],
            index=0,
            horizontal=True
        )

    #with subcol2:
    #    if houve_roubo == "Sim":
    #        valor_roubo = st.number_input(
    #            "Valor específico de roubo/desaparecimento 36m (R$)",
    #            min_value=0.0,
    #            step=100.0,
    #            format="%.2f",
    #            value=valor_roubo
    #        )

    def calcular_fator_sinistro(valor, tipo="f_rctr"):
        """
        Busca na tabela TBL_VALOR_SINISTRO a faixa correspondente
        ao valor de sinistro e retorna o fator correspondente (RCTR ou RCDC)
        """
        for faixa, dados in TBL_VALOR_SINISTRO.items():
            min_val, max_val = dados["faixa"]
            if min_val <= valor <= max_val:
                return dados[tipo]
        return 1.0

    # Pegar os fatores relativos
    fator_sinistro_rctr = calcular_fator_sinistro(valor_total_sinistros, "f_rctr")
    fator_sinistro_rcdc = calcular_fator_sinistro(valor_total_sinistros, "f_rcdc")

    st.markdown("---") 

    # =====================================
    # 7) Coberturas Adicionais
    # =====================================
    st.header("Coberturas Adicionais (Informar Cobertura + LMI + Franquia padrão)")

    # Inicializa controle de linhas dinâmicas por tipo de produto
    for tipo in ["RCTR-C", "RC-DC"]:
        key_linhas = f"num_linhas_cob_{tipo}"
        if key_linhas not in st.session_state:
            st.session_state[key_linhas] = 1

    # Função para renderizar coberturas de forma dinâmica
    def render_coberturas(tipo, max_adicionais):
        coberturas = COBERTURAS_ADICIONAIS[tipo]
        st.subheader(f"{tipo} (até {max_adicionais} adicionais)")

        selecionadas = []

        for i in range(st.session_state[f"num_linhas_cob_{tipo}"]):
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

            opcoes = [""] + [
                f"{codigo} - {info['nome']}" 
                for codigo, info in coberturas.items() 
                if info["ativa"] and codigo not in selecionadas
            ]

            with col1:
                selecao = st.selectbox(f"Cobertura {i+1}", opcoes, key=f"{tipo}_{i}")

            if selecao != "":
                codigo_selecionado = selecao.split(" - ")[0]
                info = coberturas[codigo_selecionado]
                selecionadas.append(codigo_selecionado)

                # Input LMI
                with col2:
                    lmi = st.number_input(
                        f"LMI ",
                        min_value=0.0,
                        value=0.0,
                        step=100.0,
                        format="%.2f",
                        key=f"LMI_{codigo_selecionado}"
                    )

                # Franquia
                with col3:
                    franquia = st.number_input(
                        f"Franquia ",
                        min_value=5.0,
                        max_value=100.0,
                        value=info['franquia']*100,
                        step=0.5,
                        format="%.2f",
                        key=f"franquia_{codigo_selecionado}"
                    )

                # Adiciona próxima linha se ainda não atingiu o limite
                if st.session_state[f"num_linhas_cob_{tipo}"] < max_adicionais and i == st.session_state[f"num_linhas_cob_{tipo}"] - 1:
                    st.session_state[f"num_linhas_cob_{tipo}"] += 1

            else:
                with col2: st.write("")
                with col3: st.write("")
                with col4: st.write("")

    # Renderizar conforme produto
    if produto == "RCTR-C":
        render_coberturas("RCTR-C", 5)
    elif produto == "RC-DC":
        render_coberturas("RC-DC", 4)
    elif produto == "RCTR-C + RC-DC":
        render_coberturas("RCTR-C", 5)
        render_coberturas("RC-DC", 4)

    st.markdown("---")



    # =================================================================================================================================================================================
    # CRIAÇÃO DO JSON COMPLETO
    # =================================================================================================================================================================================

    dados_cotacao = {}

    # Função para capturar coberturas adicionais do session_state
    def capturar_coberturas_adicionais(prod):
        coberturas_json = []
        coberturas = COBERTURAS_ADICIONAIS.get(prod, {})
        for codigo, info in coberturas.items():
            key_lmi = f"LMI_{codigo}"
            key_franquia = f"franquia_{codigo}"
            if key_lmi in st.session_state and st.session_state[key_lmi] > 0:
                lmi_val = st.session_state[key_lmi]
                franquia_val = st.session_state.get(key_franquia, info['franquia']*100)
                coberturas_json.append({
                    "codigo": codigo,
                    "nome": info["nome"],
                    "lmi": lmi_val,
                    "franquia": franquia_val,
                    "taxa": info["taxa"]
                })
        return coberturas_json

    # Mapear produto para chave da taxa base
    produto_para_taxa = {
        "RCTR-C": "RCTR",
        "RC-DC": "RCDC"
    }

    # =========================
    # Produto selecionado com taxa base
    # =========================
    if produto in ["RCTR-C", "RC-DC"]:
        dados_cotacao["produto_selecionado"] = {
            "nome": produto,
            "taxa_base": TAXA_BASE[produto_para_taxa[produto]]
        }
    elif produto == "RCTR-C + RC-DC":
        # Duplo produto: taxa base separada por produto
        dados_cotacao["produto_selecionado"] = {
            "nome": produto,
            "taxa_base": {
                "RCTR-C": TAXA_BASE[produto_para_taxa["RCTR-C"]],
                "RC-DC": TAXA_BASE[produto_para_taxa["RC-DC"]]
            }
        }

    # =========================
    # RCTR-C
    # =========================
    if dados_rctr is not None:
        dados_cotacao["RCTR-C"] = {
            **dados_rctr,
            "rotas": rotas,
            "fator_noturno": fator_noturno_rctr,
            "fator_rota_critica": fator_rota_rctr,
            "idade_frota": idade_frota,
            "pct_terceiros": pct_terceiros,
            "sinistro": {
                "teve_sinistro": teve_sinistro,
                "qtd_sinistros": qtd_sinistros,
                "valor_total_sinistros": valor_total_sinistros,
                "houve_roubo": houve_roubo,
                "valor_roubo": valor_roubo,
                "fator_rctr": fator_sinistro_rctr                
            },
            "mercadorias": mercadorias,
            "frota": {
                "idade_frota": idade_frota,
                "pct_terceiros": pct_terceiros,
                "fator_idade_rctr": fator_idade_rctr,
                "fator_terceiros_rctr": fator_terceiros_rctr                
            },
            "coberturas_adicionais": capturar_coberturas_adicionais("RCTR-C")
        }

    # =========================
    # RC-DC
    # =========================
    if dados_rcdc is not None:
        dados_cotacao["RC-DC"] = {
            **dados_rcdc,
            "rotas": rotas,
            "fator_noturno": fator_noturno_rcdc,
            "fator_rota_critica": fator_rota_rcdc,
            "idade_frota": idade_frota,
            "pct_terceiros": pct_terceiros,
            "sinistro": {
                "teve_sinistro": teve_sinistro,
                "qtd_sinistros": qtd_sinistros,
                "valor_total_sinistros": valor_total_sinistros,
                "houve_roubo": houve_roubo,
                "valor_roubo": valor_roubo,
                "fator_rcdc": fator_sinistro_rcdc
            },
            "mercadorias": mercadorias,
            "frota": {
                "idade_frota": idade_frota,
                "pct_terceiros": pct_terceiros,
                "fator_idade_rcdc": fator_idade_rcdc,
                "fator_terceiros_rcdc": fator_terceiros_rcdc
            },
            "coberturas_adicionais": capturar_coberturas_adicionais("RC-DC")
        }

    # Adiciona informações gerais
    dados_cotacao["comissao"] = comissao
    dados_cotacao["possui_gr"] = possui_gr
    dados_cotacao["empresa_gr"] = empresa_gr
    dados_cotacao["iof"] = IOF  

    # Debug
    #st.divider()
    #st.subheader("Debug - Dados Capturados Completo")
    #st.json(dados_cotacao)


    # =================================================================================================================================================================================
    # CALCULOS DO PRÊMIO E TAXAS
    # =================================================================================================================================================================================
    def calcular_tabela_validacao(produto_json, produto_nome, produto_selecionado, comissao_pct, iof_pct):
        
        # 1️⃣ Taxa base
        taxa_base_data = produto_selecionado["taxa_base"]
        taxa_base = taxa_base_data[produto_nome] if isinstance(taxa_base_data, dict) else taxa_base_data

        # 2️⃣ Fatores principais
        fator_viagens = produto_json["fator_rctr"] if produto_nome == "RCTR-C" else produto_json["fator_rcdc"]
        fator_noturno = produto_json["fator_noturno"]
        fator_rota_critica = produto_json["fator_rota_critica"]

        # 3️⃣ Fatores frota
        fator_idade = produto_json["frota"].get(f"fator_idade_rctr" if produto_nome=="RCTR-C" else "fator_idade_rcdc", 1)
        fator_terceiros = produto_json["frota"].get(f"fator_terceiros_rctr" if produto_nome=="RCTR-C" else "fator_terceiros_rcdc", 1)
        #fator_frota = fator_idade * fator_terceiros

        # 4️⃣ Fator mercadorias (média ponderada)
        mercadorias = produto_json["mercadorias"]
        total_mix = sum(m["mix"] for m in mercadorias)
        fator_mercadoria = 1
        if total_mix > 0:
            fator_mercadoria = sum(
                (m["f_rctr"] if produto_nome=="RCTR-C" else m["f_rcdc"]) * m["mix"] / total_mix
                for m in mercadorias
            )

        # 5️⃣ Fator sinistro
        fator_sinistro = produto_json["sinistro"].get(f"fator_rctr" if produto_nome=="RCTR-C" else "fator_rcdc", 1)

        # 5.1️⃣ Fator UF/rota (média ponderada por % de viagens, entre origem e destino)
        rotas = produto_json.get("rotas", [])
        total_pct_rotas = sum(r["percentual"] for r in rotas)
        fator_uf = 1
        if total_pct_rotas > 0:
            chave_origem = "fator_origem_rctr" if produto_nome == "RCTR-C" else "fator_origem_rcdc"
            chave_destino = "fator_destino_rctr" if produto_nome == "RCTR-C" else "fator_destino_rcdc"
            fator_uf = sum(
                ((r[chave_origem] + r[chave_destino]) / 2) * r["percentual"] / total_pct_rotas
                for r in rotas
            )

        # 6️⃣ Taxa final
        taxa_final = taxa_base * fator_viagens * fator_noturno * fator_rota_critica * fator_idade * fator_terceiros * fator_mercadoria * fator_sinistro * fator_uf

        # 7️⃣ Prêmio de risco
        valor_anual = produto_json["valor_mensal"]*12
        premio_risco = valor_anual * taxa_final

        # 8️⃣ Prêmio comercial (com comissão)
        premio_comercial = premio_risco * (1 + comissao_pct / 100)

        # 9️⃣ Prêmio final (com IOF)
        premio_final = premio_comercial * (1 + iof_pct)

        # 10️⃣ Coberturas adicionais individuais
        coberturas_df = []
        for c in produto_json["coberturas_adicionais"]:
            premio_risco_cob = c["lmi"] * c["taxa"] * 12
            premio_comercial_cob = premio_risco_cob * (1 + comissao_pct / 100)
            premio_final_cob = premio_comercial_cob * (1 + iof_pct)
            coberturas_df.append({
                "Produto": produto_nome,
                "Cobertura": c["codigo"] + " - " + c["nome"],
                "LMI": c["lmi"],
                "Taxa": c["taxa"],
                "Prêmio Risco": premio_risco_cob,
                "Prêmio Comercial": premio_comercial_cob,
                "Prêmio Final Anual": premio_final_cob
            })

    # =================================================================================================================================================================================
    # CRIA A TABELA DE VALIDAÇÃO
    # =================================================================================================================================================================================
        # 11️⃣ Tabela principal
        tabela_principal = pd.DataFrame([{
            "Produto": produto_nome,
            "Tx Base": taxa_base,
            "FT qtd Viagens": fator_viagens,
            "FT Noturno": fator_noturno,
            "FT Rota Crítica": fator_rota_critica,
            "FT Idade Frota": fator_idade,
            "FT Terceiros": fator_terceiros,
            "FT Merc": fator_mercadoria,
            "FT Sinistro": fator_sinistro,
            "FT UF/Rota": fator_uf,
            "Taxa Final": taxa_final,
            "IS Estimada Anual": valor_anual,
            "Prêmio Risco": premio_risco,
            "Comissão" : comissao_pct / 100,
            "Prêmio Comercial": premio_comercial,
            "IOF": iof_pct,
            "Prêmio Final Anual": premio_final
        }])

        return tabela_principal, pd.DataFrame(coberturas_df)
    

    # ======================================================================================================================
    # EXIBIÇÃO
    # ======================================================================================================================

    st.header("📊 Tabela de Validação do Cálculo")

    produtos = []
    if "RCTR-C" in dados_cotacao:
        produtos.append("RCTR-C")
    if "RC-DC" in dados_cotacao:
        produtos.append("RC-DC")

    for p in produtos:

        tabela_principal, tabela_coberturas = calcular_tabela_validacao(
            dados_cotacao[p],
            p,
            dados_cotacao["produto_selecionado"],
            comissao_pct=dados_cotacao["comissao"],
            iof_pct=dados_cotacao["iof"]
        )

        st.subheader(f"{p} - Cobertura Principal")

        st.dataframe(
            tabela_principal
                .style
                .format({
                    "Taxa Base": "{:.6%}",
                    "Taxa Final": "{:.6%}",
                    "IS Estimada Anual": "R$ {:,.2f}",
                    "Prêmio Risco": "R$ {:,.2f}",
                    "Prêmio Comercial": "R$ {:,.2f}",
                    "Prêmio Final Anual": "R$ {:,.2f}",
                    "Comissão": "{:.2%}",
                    "IOF": "{:.2%}"
                })
                .hide(axis="index")
        )

        if not tabela_coberturas.empty:

            st.subheader(f"{p} - Coberturas Adicionais")

            st.dataframe(
                tabela_coberturas
                    .style
                    .format({
                        "LMI": "R$ {:,.2f}",
                        "Taxa": "{:.6%}",
                        "Prêmio Risco": "R$ {:,.2f}",
                        "Prêmio Comercial": "R$ {:,.2f}",
                        "Prêmio Final Anual": "R$ {:,.2f}"
                    })
                    .hide(axis="index")
            )

        # ======================================================================================================================
        # RESUMO EXECUTIVO
        # ======================================================================================================================

        st.subheader(f"{p} - Resumo Executivo")

        # 🔹 Dados da cobertura básica
        taxa_final_basica = tabela_principal["Taxa Final"].iloc[0]
        premio_final_basica = tabela_principal["Prêmio Final Anual"].iloc[0]

        # 🔹 Total coberturas adicionais
        premio_final_adicionais = 0
        if not tabela_coberturas.empty:
            premio_final_adicionais = tabela_coberturas[
                tabela_coberturas["Cobertura"] != "TOTAL GERAL"
            ]["Prêmio Final Anual"].sum()

        # 🔹 Prêmio total geral
        premio_total_geral = premio_final_basica + premio_final_adicionais

        # 🔥 Exibição formatada
        st.markdown(f"""
        **Cobertura Básica ({p})**  
        - Taxa Final: {taxa_final_basica:,.7f}  
        - Prêmio Final: R$ {premio_final_basica:,.2f}

        **Coberturas Adicionais (Total)**  
        - Prêmio Final: R$ {premio_final_adicionais:,.2f}

        ### 💰 Prêmio Total Geral: R$ {premio_total_geral:,.2f}
        
        ---
        ---

        """)            