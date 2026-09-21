import streamlit as st

st.set_page_config(layout="wide")

st.sidebar.title("Seleção de Produto")

produto = st.sidebar.selectbox(
    "Produto:",
    [
        "Vida Em Grupo-V2",
        "Vida Em Grupo (V3 - Beta)",
        #"Vida Individual",
        #"Transporte"
    ]
)

if produto == "Vida Em Grupo-V2":
    import vida_Global_app
    vida_Global_app.run()

elif produto == "Vida Em Grupo (V3 - Beta)":
    import vida_global_v3_app
    vida_global_v3_app.run()

#elif produto == "Vida Individual":
#    import vida_individual_app
#    vida_individual_app.run()

#elif produto == "Transporte":
#    import transporte_app
#    transporte_app.run()