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
        """
    )

if __name__ == "__main__":
    run()




# Farmer
# Cadastro de show padrão
# 

# Implantação
# Cadastro de show padrão
# Recebeu programação
# Perfi spaces
# Ativou controladoria

# Artistas
# Onboarda artistas
# Prospecção feita