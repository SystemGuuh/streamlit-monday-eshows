import streamlit as st
from utils.queries import *

def connect():
    # Initialize connection.
    conn = st.connection('mysql', type='sql')
    return conn

def consultBarChart(consulta, conn):
    df = conn.query(consulta, ttl=0)
    column_name = df.columns.tolist()
    st.bar_chart(df, x=str(column_name[0]), y=str(column_name[1]))

def getDfFromQuery(consulta, conn):
    return conn.query(consulta, ttl=0)

def consultArtistas(conn):
    st.write("Quantidade de projetos por estilo musical:")
    consultBarChart(GET_ESTILOS_POR_PROJETO, conn)

    col1, col2 = st.columns([4,1])
    with col1:
        st.write("Quantidade de usuários por UF:")
        consultBarChart(GET_USER_POR_LOCAL, conn)
    with col2:
        distinct_uf = getDfFromQuery(GET_USER_POR_LOCAL, conn)
        sprint_selected = st.selectbox("", distinct_uf["UF"].unique().tolist())
        st.write("Quantidade: ", distinct_uf.loc[distinct_uf['UF'] == sprint_selected, 'Quantidade'].values[0])
    #Artistas novos ao longo dos meses
    #Cache médio de artistas por local
    #Shows por local

def consultContratantes(conn):
    st.write("Quantidade de propostas por estilo musical:")
    consultBarChart(GET_ESTILOS_POR_PROPOSTA, conn)

    st.write("Cache médio por UF:")
    consultBarChart(GET_CACHE_MEDIO_OPORTUNIDADES, conn)
    #Contratante por local
    #Novos contratantes por mes
    #Cache médio de contratante por regiao
    #Contratos por região


st.set_page_config(page_title="Database", page_icon="📊")
st.markdown("# Analisando dados do banco Eshows")
st.sidebar.header("Database")

with st.sidebar:
    sprint_selected = st.selectbox("Ver dados:", ['Artistas','Contratantes'])

if sprint_selected == 'Artistas':
    consultArtistas(connect())
if sprint_selected == 'Contratantes':
    consultContratantes(connect())