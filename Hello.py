import streamlit as st

def run():
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
        - **Database:** Página conectada ao nosso banco de dados, onde é possível visualizar dados em tabelas.
        - **Monday:** Página para visualizar dados coletados da API do Monday (fluxo do radar).
        """
    )

if __name__ == "__main__":
    run()
