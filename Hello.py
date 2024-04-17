import streamlit as st
from utils.monday import get_mysql_connection, getDfFromQuery
from utils.queries import GET_RADAR_FROM_BD
import threading
from datetime import datetime
import pytz

def getRadarDataFromDatabse():
    conn = get_mysql_connection()
    if conn.is_connected():
        radarBdDf = getDfFromQuery(GET_RADAR_FROM_BD, conn)
        radarBdDf.to_csv('./assets/csvs/bdRadar.csv', index=False)

    #marca a ultima atualzização do BD
    now = datetime.now(pytz.timezone('America/Sao_Paulo'))
    timestamp = now.strftime("Database update at: %d/%m/%Y %H:%M:%S")
    with open('./assets/csvs/UltimaAtualizacao.txt', 'w') as file:
        file.write(str(timestamp))

#colocar para printar o horário e dia da ultima atualização do bd
def run():
    print("tread1")
    st.set_page_config(
        page_title="Eshows Data",
        page_icon="🎤",
        layout="wide"
    )
    col1, col2 = st.columns([4,1])
    col2.image("./assets/imgs/eshows-logo.png", width=100)
    col1.write("# Radar de Implementação")

    st.markdown(
        """
        #### Visualização dos dados do Radar de Implementação:
        - **Visão Geral do Monday:** Página para visualizar dados coletados do Radar.
        - **Hunter:** Página para visualizar dados pertinentes a Hunters.
        - **Farmer:** Página para visualizar dados pertinentes a Farmers.
        - **Implementação:** Página para visualizar dados de implantantação.

        ### Outras orientações
        - O botão **"Atualizar dados BD"** roda uma query para atualizar os dados usado do banco, pode demorar até 1 minuto.
        """
    )

if __name__ == "__main__":
    gettingData = threading.Thread(target=getRadarDataFromDatabse)
    mainProgram = threading.Thread(target=run())

    gettingData.start()
    mainProgram.start()


# Artistas
# Onboarda artistas
# Prospecção feita
