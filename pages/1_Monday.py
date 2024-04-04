import streamlit as st
from utils.monday import *
import pandas as pd
from monday import MondayClient

def crateMondayResquest():
    monday = MondayClient(load_api_key())
    boardQuery = monday.boards.fetch_boards_by_id(6303323231)

    response_data = makeRequestByQuery("""
            query {
                boards (ids: 6303323231) {
                    groups {
                        title
                        id
                    }
                    items_page{
                            items {
                                name 
                            column_values {
                            column {
                                title
                            } 
                            text 
                            } 
                        }
                    }
                }
            }
            """)

    return response_data

def processDataFromARequest(response_data):
    value = response_data["items"][0]["name"]
    
    # Extrair dados do dicionário para uma lista de dicionários
    dados_formatados = []
    for item in response_data["items"]:
        dicionario_item = {"Nome": item["name"]}
        for coluna in item["column_values"]:
            titulo_coluna = coluna["column"]["title"]
            texto_coluna = coluna["text"]
            dicionario_item[titulo_coluna] = texto_coluna
        dados_formatados.append(dicionario_item)

    return dados_formatados
    
st.set_page_config(page_title="Monday data", page_icon="🗂️")

if df := processDataFromARequest(crateMondayResquest()["data"]["boards"][0]["items_page"]):
    st.markdown("## Dados do Rada de Implementação")
    st.dataframe(df := pd.DataFrame(df), hide_index=True)

    with st.sidebar:
        if(filter := st.checkbox('Ativar filtros', value=False)):
            if (df_column := st.selectbox("Selecione um campo", df.columns.tolist())):
                df_line = st.selectbox("Selecione valor", df[df_column].unique().tolist())
                showMissingValues = st.checkbox('Reportar campos vazios:', value=False)
            else:
                st.error("Connection erro, try again later")

if(filter == True):
    st.divider()
    st.markdown(f"### Dados de {df_column}:")
    st.dataframe(df_temp := df.loc[df[df_column] == df_line], hide_index=True)

    if(df_column not in {"Farmer", "Hunter Responsável", "Nome contratante"}):
        col1, col2, col3 = st.columns(3)
        col1.write(f"Hunter: {df_temp.loc[df_temp.index[0], 'Hunter Responsável']}")
        col2.write(f"Farmer: {df_temp.loc[df_temp.index[0], 'Farmer']}")
        col3.write(f"Contratante: {df_temp.loc[df_temp.index[0], 'Nome contratante']}")

    if showMissingValues:
        if len(df_temp) > 1:
            selected_line = st.sidebar.selectbox("Selecione uma linha", df_temp['Nome'])
            df_temp = df_temp[df_temp['Nome'] == selected_line]

            for index, row in df_temp.iterrows():  
                    for column, value in row.iteritems():  
                        if pd.isnull(value) or value == "":
                            st.error(f"Na linha {index}, a coluna '{column}' está vazia ou contém um valor ausente.")
else:
    st.error("Select filter to see more informations")



    


        