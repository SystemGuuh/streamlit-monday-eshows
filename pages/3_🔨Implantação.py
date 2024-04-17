import streamlit as st
from utils.monday import *
from utils.queries import *
import pandas as pd

#ver pendicas
#status do cadastro pelo bd
#quantidade de dados faltando

#pegar stabilização do monday

def getImplantacaoData(radarMondaydf):
    return radarMondaydf[['ID EPM', 'Nome', 'Relevância do cliente',
                               'Nome contratante', 'E-mail do contratante',
                               'Cidade do Estabelecimento', 'Cadastro de show padrão',
                               'Recebi programação do Hunter?', 'Criar perfil Espaces', 'Ativou controladoria? (ativar três dias antes)',
                               'Observação Hunting', 'Ação']]

def checkStopedItens(df):
    try:
        for coluna in df.columns[6:9]:
            for indice, valor in df[coluna].items():
                if str(valor).lower() == 'parado':
                    return True
        return False
    except Exception as e:
        st.error("Opa, valor inconsistente ou não númerico encontrado no entre colunas 6 e 9 do dataframe")
        return False

def printStopedItens(df):
    stopedItensCount = []
    stopedItensValues = []
    for indice, linha in df.iterrows():
        valor_anterior = None
        count =0
        for coluna in df.columns:
            valor = linha[coluna]
            if valor is None or str(valor) == '':
                nome = linha['Nome']
                stopedItensValues.append(f'- "**{nome}**" está com o campo "**{coluna}**" vazio e precisa ser preenchido.')
                count += 1
                valor_anterior = None
                continue
            elif str(valor).lower() == 'parado' and valor_anterior != 'não aplica':
                nome = linha['Nome']
                stopedItensValues.append(f'- "**{nome}**" está com o campo "**{coluna}**" parado.')
                count += 1
            valor_anterior = valor.lower()
        stopedItensCount.append(count)

    #printa campos parados
    aux = 0
    for indice, linha in df.iterrows():
        if stopedItensCount[indice] > 0:
            with st.expander(f"⚠️ **{linha['Nome']}**: {stopedItensCount[indice]} itens pendentes"):
                st.write('\n'.join(map(str, stopedItensValues[aux:stopedItensCount[indice]])))
            aux = stopedItensCount[indice]

st.set_page_config(page_title="Monday Implantação Data", page_icon="🔨")
col1, col2 = st.columns([4,1])
col1.markdown(f"# Radar de implantação")
col2.image("./assets/imgs/eshows-logo.png", width=100)
if st.button("Atualizar dados BD", type="secondary"): getRadarDataFromDatabse()
st.divider()


radarMondaydf = getImplantacaoData(getMondayDataframe())

if  not radarMondaydf.empty:
    with st.sidebar:
        filterHause = st.selectbox("Selecione uma Casa", radarMondaydf['Nome'].unique().tolist(), index=None,placeholder="Casa")

    if filterHause:
        st.markdown(f"### Radar da casa {filterHause}")
        df = radarMondaydf[radarMondaydf['Nome'] == filterHause].reset_index(drop=True)
        st.dataframe(df, hide_index=True)

        st.divider()
        if(checkStopedItens(df)):
            st.markdown(f"### Próximos passos do {filterHause}")
            printStopedItens(df)
        else:
            st.success("Parece que tudo completo no radar dessa casas!")

    else:
        st.dataframe(radarMondaydf, hide_index=True)


else:
    st.error("Erro de requisição, não foi possível coletar os dados do Monday.")
