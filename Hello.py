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
        - **Visão Geral do Monday:** Página para visualizar dados coletados do Radar.
        - **Hunter:** Página para visualizar dados pertinentes a Hunters.
        - **Farmer:** Página para visualizar dados pertinentes a Farmers.
        - **Implementação:** Página para visualizar dados de implantantação.

        ### Outras orientações
        - O botão **"Atualizar dados BD"** roda uma query para atualizar os dados usado do banco, pode demorar até 1 minuto.
        """
    )

if __name__ == "__main__":
    run()




# Farmer
# Cadastro de show padrão
# 



# Artistas
# Onboarda artistas
# Prospecção feita