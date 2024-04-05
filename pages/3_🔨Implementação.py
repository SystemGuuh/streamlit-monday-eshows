import streamlit as st
from utils.monday import *
from utils.queries import *
import pandas as pd


st.set_page_config(page_title="Monday data", page_icon="🗂️")
col1, col2 = st.columns([4,1])
col1.markdown(f"# Radar de implantação")
col2.image("./assets/imgs/eshows-logo.png", width=100)
st.divider()

st.markdown("### Radar do Monday")
radarMondaydf = getMondayDataframe()
st.dataframe(radarMondaydf, hide_index=True)


radarBdDf = getRadarDataFromLocal()

st.markdown('## Radar do banco de dados')
radarBdDfClean = cleanBdDataUsingMonday(radarMondaydf, radarBdDf)
st.dataframe(radarBdDfClean, hide_index=True)