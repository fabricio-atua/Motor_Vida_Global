import streamlit as st

st.set_page_config(layout="wide")

st.sidebar.title("Seleção de Produto")

produto = st.sidebar.selectbox(
    "Produto:",
    [
        "Vida Em Grupo",
        #"Vida Individual",
        #"Transporte"
    ]
)

if produto == "Vida Em Grupo":
    import vida_Global_app
    vida_Global_app.run()

#elif produto == "Vida Individual":
#    import vida_individual_app
#    vida_individual_app.run()

#elif produto == "Transporte":
#    import transporte_app
#    transporte_app.run()