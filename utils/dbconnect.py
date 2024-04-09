import mysql.connector
import streamlit as st
import pandas as pd

def get_mysql_connection():
    mysql_config = st.secrets["mysql"]
    
    # Create MySQL connection
    conn = mysql.connector.connect(
        host=mysql_config['host'],
        port=mysql_config['port'],
        database=mysql_config['database'],
        user=mysql_config['username'],
        password=mysql_config['password']
    )    
    return conn

def execute_query(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    
    # Obter nomes das colunas
    column_names = [col[0] for col in cursor.description]
    
    # Obter resultados
    result = cursor.fetchall()
    
    cursor.close()
    return result, column_names

def getDfFromQuery(consulta, conn):
    result, column_names = execute_query(consulta, conn)
    return pd.DataFrame(result, columns=column_names)