import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

#datatest-apps
def run():
    st.set_page_config(
        page_title="Eshows Data",
        page_icon="🎤",
    )

    st.write("# Rada de implementação")

    st.markdown(
        """
        Visualização de dados do radar de implementação:
        - Database: page connected to our database, its possible to run querys and analise data
        - Monday: page to see data colected from monday API(flow de radar)
    """
    )


if __name__ == "__main__":
    run()
