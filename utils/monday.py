import toml
import requests
import streamlit as st
from monday import MondayClient
import pandas as pd
from utils.dbconnect import *
from utils.queries import GET_RADAR_FROM_BD

def load_api_key():
    return st.secrets['monday']['api_key']

def makeRequestByQuery(query):
    headers = {"Authorization": load_api_key()}
    query3 = query
    apiUrl = "https://api.monday.com/v2"
    data = {'query' : query3}
    r = requests.post(url=apiUrl, json=data, headers=headers)
    return r.json()

def crateMondayResquest():
    monday = MondayClient(load_api_key())
    boardQuery = monday.boards.fetch_boards_by_id(6303323231)

    response_data = makeRequestByQuery("""
            query {
                boards (ids: 6303323231) {
                    items_page{
                            items{
                                name
                                group{
                                    title
                                }
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

def processDataFromARequest():
    # Extrair dados do dicionário para uma lista de dicionários
    response_data = crateMondayResquest()["data"]["boards"][0]["items_page"]
    dados_formatados = []
    for item in response_data["items"]:
        if item["group"]["title"] == "Implantação" or item["group"]["title"] == "Estabilização":
            dicionario_item = {"Nome": item["name"]}
            for coluna in item["column_values"]:
                titulo_coluna = coluna["column"]["title"]
                texto_coluna = coluna["text"]
                dicionario_item[titulo_coluna] = texto_coluna
            dados_formatados.append(dicionario_item)

    return dados_formatados

def getMondayDataframe():
    try:
        df = pd.DataFrame(processDataFromARequest())

        #removing ID EPM without value
        df['ID EPM'] = df['ID EPM'].replace('', pd.NA)
        df = df.dropna(subset=['ID EPM'])

        return df
    except Exception as e:
        st.error(f"Ocorreu um erro ao tentar coletar dados")
        return pd.DataFrame()

def cleanBdDataUsingMonday(mondayDf, bdDf):
    try:
        cleanBdDf = bdDf[bdDf['ID_CASA'].isin(mondayDf['ID EPM'].astype(int))]
        cleanBdDf = cleanBdDf.reset_index(drop=True)
        return cleanBdDf
    except Exception as e:
        st.error('Algo deu errado, há valores incongruentes no monday.')
        return pd.DataFrame()

def searchMissingValues(df):
    for index, row in df.iterrows():
                for column in df.columns:
                    value = row[column]
                    if pd.isnull(value) or value == "":
                        st.error(f"Na linha {index+1}, a coluna '{column}' precisa ser preenchida.")

def getMissingRegisterValue(id):
    conn = get_mysql_connection()
    if conn.is_connected():
        query= f"SELECT C.ID AS ID_CASA, C.OBS_ERRO_CADASTRO AS ERRO_CADASTRO FROM T_COMPANIES C WHERE C.ID = {id}"
        df = getDfFromQuery(query, conn)
        return df

def getStatusCompany(id):
    conn = get_mysql_connection()
    if conn.is_connected():
        query= f"""SELECT	TC.ID, SC.STATUS AS status
                FROM T_COMPANIES AS TC
                        INNER JOIN T_STATUS_COMPANIES SC ON TC.FK_STATUS_COMPANY = SC.ID
                WHERE TC.ID =  {id}"""
        df = getDfFromQuery(query, conn)
        return df

def getRadarDataFromLocal():
    return pd.read_csv('./assets/csvs/bdRadar.csv')

def renameColumns(df):
    df = df.rename(columns={'Volume (qts gigs a eshows terá na casa?)': 'Volume'})
    return df
