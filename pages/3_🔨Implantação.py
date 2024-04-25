import streamlit as st
from utils.showmetrics import *

st.set_page_config(page_title="Monday Implantação Data", page_icon="🔨")
col1, col2 = st.columns([4,1])
col1.markdown(f"# Radar de implantação")
col2.image("./assets/imgs/eshows-logo.png", width=100)
st.divider()

radarMondaydf = renameColumns(getImplantacaoData(getMondayDataframe()))

if  not radarMondaydf.empty:
    with st.sidebar:
        filterHause = st.selectbox("Selecione uma Casa", radarMondaydf['Nome'].unique().tolist(), index=None,placeholder="Casa")

    if filterHause:
        st.markdown(f"### Radar da casa {filterHause}")
        df = radarMondaydf[radarMondaydf['Nome'] == filterHause].reset_index(drop=True)
        st.dataframe(df, hide_index=True)


        if(checkStopedItens(df)):
            findAndPrintStopedItens(df)
        else:
            st.success("Parece que tudo completo no radar dessa casas!")

        tab1, tab2= st.tabs(["Pendências", "Situação Cadastral"])
        with tab1:
            showDataByDayabase(cleanBdDataUsingMonday(radarMondaydf, getRadarDataFromLocal()), radarMondaydf[radarMondaydf['Nome'] == filterHause],df.loc[df['Nome'] == filterHause, 'ID EPM'].iloc[0], filterHause)
        with tab2:
            stringObs = radarMondaydf.loc[radarMondaydf['Nome'] == filterHause, 'Observação Hunting'].astype(str).iloc[0]
            st.markdown("#### Observação do hunter:")
            st.info(stringObs)
            showMissingRegisterValuesFromDatabase(radarMondaydf.loc[radarMondaydf['Nome'] == filterHause, 'ID EPM'].astype(int).iloc[0])

    else:
        st.dataframe(radarMondaydf, hide_index=True)


else:
    st.error("Erro de requisição, não foi possível coletar os dados do Monday.")
