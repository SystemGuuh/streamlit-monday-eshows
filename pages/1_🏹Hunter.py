import streamlit as st
from utils.monday import *
from utils.queries import *
import pandas as pd
import threading

def getHunterData(radarMondaydf):
    return radarMondaydf[['ID EPM', 'Nome', 'Relevância do cliente', 
                               'Nome contratante', 'E-mail do contratante', 
                               'Cidade do Estabelecimento', 'GMV estimado', 
                               'Início da parceria', 'Tipo de negociação', 'Carência?', 
                               'Carência até (data)', 'Formulário Hub', 'Grupo no Whatsapp',
                                'Companie criado?', 'Criação da marca', 'Login criado?', 
                                'Cadastro de show padrão (QUEM VAI FAZER?)', 
                                'Coletar contatos de artista', 'Coletar programação', 
                                'Recebi programação do Hunter?', 
                                'Estrutura da programação (dias da semana)', 
                                'Volume (qts dias a eshows terá na casa?)',
                                'Cliente irá atuar de forma independente?',
                                'Propostas lançadas?', 'Hunter Responsável']]

def createView(df, hunter):
     return df[df['Hunter Responsável'] == hunter].reset_index(drop=True)

def checkNextSteps(df):
     searchMissingValues(df)


st.set_page_config(page_title="Monday Hunter Data", page_icon="🏹")
col1, col2 = st.columns([4,1])
col1.markdown(f"# Radar de implantação")
col2.image("./assets/imgs/eshows-logo.png", width=100)


radarMondaydf = getHunterData(getMondayDataframe())
radarBdDf = getRadarDataFromLocal()
radarBdDfClean = cleanBdDataUsingMonday(radarMondaydf, radarBdDf)

if  not radarMondaydf.empty:
    with st.sidebar:
            if (showRadarMonday := st.checkbox('Visão Geral Monday', value=True)):
                if (filterHunter := st.selectbox("Selecione Hunter", radarMondaydf['Hunter Responsável'].unique().tolist(), index=None,placeholder="Hunter")):
                    filterHause = st.selectbox("Dados ausentes de uma casa", radarMondaydf[radarMondaydf['Hunter Responsável'] == filterHunter]['Nome'].unique().tolist(), index=None, placeholder="Selecione a casa")


    if showRadarMonday:
        if filterHunter:
            st.divider()
            st.markdown(f"### Radar do {filterHunter}")
            df = createView(radarMondaydf ,filterHunter)
            st.dataframe(df, hide_index=True)
            if filterHause:
                checkNextSteps(df[df['Nome']==filterHause])
        else:
            st.divider()
            st.markdown("### Radar do Monday")
            st.dataframe(radarMondaydf, hide_index=True)
else:  st.error("Erro de requisição, não foi possível coletar os dados do Monday.")   