import streamlit as st
from utils.monday import *
import pandas as pd

def createGlobalDataFrame(df):
    with st.sidebar:
        show = st.checkbox('Visão Geral', value=True)

    if show:
        st.divider()
        st.markdown("### Radar do Monday")
        st.dataframe(df := pd.DataFrame(df), hide_index=True)

def createFilters(df):
    with st.sidebar:
        if(filter := st.checkbox('Criar Filtro', value=False)):
            if (df_column := st.selectbox("Selecione um campo", df.columns.tolist())):
                df_line = st.selectbox("Selecione valor", df[df_column].unique().tolist())
                showMissingValues = st.checkbox('Reportar campos vazios', value=False)
            else:
                st.error("Erro de seleção, escolha um componente válido")
    if filter:
        st.divider()
        st.markdown(f"### Dados de {df_column}:")

        st.dataframe(df_temp := df.loc[df[df_column] == df_line], hide_index=True)

        #printa o nome do Hunter, Farmer e Contratente responsável
        if(df_column not in {"Farmer", "Hunter Responsável", "Nome contratante"} and len(df_column)==1):
            col1, col2, col3 = st.columns(3)
            if {df_temp.loc[df_temp.index[0], 'Hunter Responsável']}:
                col1.write(f"Hunter: Nenhum")
            else: col1.write(f"Hunter: {df_temp.loc[df_temp.index[0], 'Hunter Responsável']}")
            if {df_temp.loc[df_temp.index[0], 'Farmer']}:
                col2.write(f"Farmer: Nenhum")
            else: col2.write(f"Farmer: {df_temp.loc[df_temp.index[0], 'Farmer']}")
            if {df_temp.loc[df_temp.index[0], 'Nome contratante']}:
                col3.write(f"Contratante: Nenhum")
            else: col3.write(f"Contratante: {df_temp.loc[df_temp.index[0], 'Nome contratante']}")

        if showMissingValues:
            if len(df_temp) > 1:
                selected_line = st.sidebar.selectbox("Selecione uma linha", df_temp['Nome'])
                df_temp = df_temp[df_temp['Nome'] == selected_line]

                searchMissingValues(df_temp)
            else:
                searchMissingValues(df_temp)

st.set_page_config(page_title="Monday Global Data", page_icon="🗂️")
col1, col2 = st.columns([4,1])
col1.markdown(f"# Radar de implantação")
col2.image("./assets/imgs/eshows-logo.png", width=100)

# nesse caso radar é uma lista, não um dataframe do tipo pandas
radarMondaydf = getMondayDataframe()
if  not radarMondaydf.empty:
    createGlobalDataFrame(radarMondaydf)
    createFilters(radarMondaydf)
else:
    st.error("Erro de requisição, não foi possível coletar os dados do Monday.")
