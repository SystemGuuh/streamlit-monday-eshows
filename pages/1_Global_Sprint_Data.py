import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.sheets import *

# Pensar em como armazenar o resultado da primeira chamada da função getGSheet, se não teremos erro de requisição excessiva
def getGSheet():
    # Pegando planilha do google sheets
    gsheets_reader = GSheetsReader()
    sprintMetrics = gsheets_reader.sprintMetrics()
    sprintMetrics = sprintMetrics.drop(columns=[col for col in sprintMetrics.columns if 'Unnamed' in col])
    return sprintMetrics

def plotting_Data(df):
    with st.sidebar:
        sprint_selected = st.selectbox("Sprint cicle:", ['Artistas','Contratantes'])

    df['Sprint'] = df['Sprint'].fillna('')
    df_Points = df.drop(columns=['Sprint Start Date','Estimated Effort','Burndown Speed','Required Burndown Speed','Avarege Cycle Time','Weighted Cycle Time'])
    df_Porcent = df.drop(columns=['Sprint Start Date','Estimated Effort','Burndown Speed',' Total Story Points','Total Sprint Effort','Required Burndown Speed'])
    df_Complete = df.drop(columns=['Sprint Start Date','Estimated Effort','Burndown Speed',' Total Story Points','Total Sprint Effort','Required Burndown Speed', 'Avarege Cycle Time', 'Weighted Cycle Time'])
    
    #Separando dados artistas e contratantes
    if sprint_selected == 'Artistas':
        df_Points = df_Points[df_Points['Sprint'].str.contains('A')]
        df_Porcent = df_Porcent[df_Porcent['Sprint'].str.contains('A')]
        df_Complete = df_Complete[df_Complete['Sprint'].str.contains('A')]
    if sprint_selected == 'Contratantes':
        df_Points = df_Points[df_Points['Sprint'].str.contains('C')]
        df_Porcent = df_Porcent[df_Porcent['Sprint'].str.contains('C')]
        df_Complete = df_Complete[df_Complete['Sprint'].str.contains('C')]

    #removendo caracter A ou C da coluna Sprint
    if sprint_selected == 'Artistas':
        df_Points['Sprint'] = df_Points['Sprint'].str.replace('A','').astype(int)
        df_Porcent['Sprint'] = df_Porcent['Sprint'].str.replace('A','').astype(int)
        df_Complete['Sprint'] = df_Complete['Sprint'].str.replace('A','').astype(int)
    if sprint_selected == 'Contratantes':
        df_Points['Sprint'] = df_Points['Sprint'].str.replace('C','').astype(int)
        df_Porcent['Sprint'] = df_Porcent['Sprint'].str.replace('C','').astype(int)
        df_Complete['Sprint'] = df_Complete['Sprint'].str.replace('C','').astype(int)

    # Realizando a pivotagem
    df_Points_pivot = df_Points.set_index('Sprint').stack().unstack(0)

    st.markdown("## 1. Relação Tarefas feitas e tarefas totais")
    st.dataframe(df_Points_pivot, hide_index=True)
    st.line_chart(df_Points, x='Sprint', y=(' Total Story Points','Total Sprint Effort'), color=["#ffcc00", "#ff6600"])
    
    st.divider()
    st.markdown("## 2. Relação Tarefas feitas e não feitas")
    df_Points['Lost Points'] = df_Points['Total Sprint Effort'] - df_Points[' Total Story Points']
    df_Points = df_Points.drop(columns=['Total Sprint Effort'])
     # Realizando a pivotagem
    df_Points_pivot = df_Points.set_index('Sprint').stack().unstack(0)
    st.dataframe(df_Points_pivot, hide_index=True)
    st.bar_chart(df_Points, x='Sprint', y=(' Total Story Points','Lost Points'), color=["#ffcc00", "#ff6600"])

    st.divider()
    st.markdown("## 3. Relação % usada da sprint")

    #ajustando % e adicionando coluna de 100%
    df_Porcent['Complete'] = 100
    df_Porcent['Avarege Cycle Time'] = df_Porcent['Avarege Cycle Time']*100
    df_Porcent['Weighted Cycle Time'] = df_Porcent['Weighted Cycle Time']*100


    # Realizando a pivotagem
    df_aux = df_Porcent.drop(columns=['Avarege Cycle Time', 'Complete', 'Percent Complete'])
    df_Porcent_pivot = df_aux.set_index('Sprint').stack().unstack(0)
    st.dataframe(df_Porcent_pivot, hide_index=True)
    st.line_chart(df_Porcent, x='Sprint', y=('Avarege Cycle Time','Weighted Cycle Time', 'Complete'), color=["#ffcc00", "#fc0f03","#ff6600"])

    st.divider()
    st.markdown("## 4. Relação Porcentagem de tempo não usado")
    df_Porcent['Remaining'] = df_Porcent['Complete'] - df_Porcent['Weighted Cycle Time']
    df_Porcent = df_Porcent.drop(columns=['Avarege Cycle Time', 'Complete', 'Percent Complete'])
     # Realizando a pivotagem
    df_Porcent_pivot = df_Porcent.set_index('Sprint').stack().unstack(0)
    st.dataframe(df_Porcent_pivot, hide_index=True)
    st.bar_chart(df_Porcent, x='Sprint', y=('Weighted Cycle Time','Remaining'), color=["#ffcc00", "#ff6600"])

    st.divider()
    st.markdown("## 5. Porcentagem completa da sprint")
    df_Complete['Complete'] = 100
    df_Complete['Percent Complete'] = df_Complete['Percent Complete']*100


    # Realizando a pivotagem
    df_aux = df_Complete.drop(columns=['Complete'])
    df_Complete_pivot = df_aux.set_index('Sprint').stack().unstack(0)
    st.dataframe(df_Complete_pivot, hide_index=True)
    st.line_chart(df_Complete, x='Sprint', y=('Complete', 'Percent Complete'), color=["#fc0f03", "#ffcc00"])

st.set_page_config(page_title="Plotting Sprint", page_icon="📈")
st.markdown("# Plotting Sprint Data")

plotting_Data(getGSheet())