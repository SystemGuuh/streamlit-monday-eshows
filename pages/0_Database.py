import streamlit as st
from utils.queries import *
from utils.dbConn import get_mysql_connection, execute_query
import pandas as pd

def consultBarChart(consulta, conn):
    result, column_names = execute_query(consulta, conn)
    df = pd.DataFrame(result, columns=column_names)
    st.bar_chart(df, x=str(column_names[0]), y=str(column_names[1]))

def getDfFromQuery(consulta, conn):
    result, column_names = execute_query(consulta, conn)
    return pd.DataFrame(result, columns=column_names)

def consultArtistas(conn):
    st.write("Quantidade de projetos por estilo musical:")
    consultBarChart(GET_ESTILOS_POR_PROJETO, conn)

    col1, col2 = st.columns([4, 1])
    with col1:
        st.write("Quantidade de usuários por UF:")
        consultBarChart(GET_USER_POR_LOCAL, conn)
    with col2:
        distinct_uf = getDfFromQuery(GET_USER_POR_LOCAL, conn)
        sprint_selected = st.selectbox("", distinct_uf["UF"].unique().tolist())
        st.write("Quantidade: ", distinct_uf.loc[distinct_uf['UF'] == sprint_selected, 'Quantidade'].values[0])

def consultContratantes(conn):
    st.write("Quantidade de propostas por estilo musical:")
    consultBarChart(GET_ESTILOS_POR_PROPOSTA, conn)

    st.write("Cache médio por UF:")
    consultBarChart(GET_CACHE_MEDIO_OPORTUNIDADES, conn)

st.set_page_config(page_title="Database", page_icon="📊")
st.markdown("# Analisando dados do banco Eshows")
st.sidebar.header("Database")

with st.sidebar:
    sprint_selected = st.selectbox("Ver dados:", ['Artistas', 'Contratantes'])

conn = get_mysql_connection()
if conn.is_connected():
    if sprint_selected == 'Artistas':
        consultArtistas(conn)
    elif sprint_selected == 'Contratantes':
        consultContratantes(conn)
    conn.close()
else:
    st.error("Failed to connect to MySQL database")
