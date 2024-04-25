import streamlit as st
from utils.showmetrics import *

st.set_page_config(page_title="Monday Farmer Data", page_icon="🚜")
col1, col2 = st.columns([4,1])
col1.markdown(f"# Radar de implantação")
col2.image("./assets/imgs/eshows-logo.png", width=100)

radarMondaydf = renameColumns(getFarmerData(getMondayDataframe()))

if  not radarMondaydf.empty:
    with st.sidebar:
            if (filterFarmer := st.selectbox("Selecione um Farmer", radarMondaydf['Farmer'].unique().tolist(), index=None,placeholder="Farmer")):
                filterHause = st.selectbox("Dados de uma casa", radarMondaydf[radarMondaydf['Farmer'] == filterFarmer]['Nome'].unique().tolist(), index=None, placeholder="Selecione a casa")

    if filterFarmer:
        st.markdown(f"### Radar do {filterFarmer}")
        df = radarMondaydf[radarMondaydf['Farmer'] == filterFarmer].reset_index(drop=True)
        st.dataframe(df, hide_index=True)

        if(checkStopedItens(df)):
            findAndPrintStopedItens(df)
        else:
            st.success("Parece que tudo está completo no radar das suas casas!")

        #rodar query para pegar dados do BD com o ID da casa
        if filterHause:
            tab1, tab2= st.tabs(["Pendências", "Situação Cadastral"])
            with tab1:
                showDataByDayabase(cleanBdDataUsingMonday(radarMondaydf, getRadarDataFromLocal()), radarMondaydf[radarMondaydf['Nome'] == filterHause],df.loc[df['Nome'] == filterHause, 'ID EPM'].iloc[0], filterHause)
            with tab2:
                stringObs = radarMondaydf.loc[radarMondaydf['Nome'] == filterHause, 'Observação Hunting'].astype(str).iloc[0]
                st.markdown("#### Observação do hunter:")
                st.info(stringObs)
                showMissingRegisterValuesFromDatabase(radarMondaydf.loc[radarMondaydf['Nome'] == filterHause, 'ID EPM'].astype(int).iloc[0])

        else:
            st.warning('Selecione dados de uma casa para ver mais campos e próximos passos.')

    else:
        st.markdown("### Radar do Monday")
        st.dataframe(radarMondaydf, hide_index=True)
else:
    st.error("Erro de requisição, não foi possível coletar os dados do Monday.")
