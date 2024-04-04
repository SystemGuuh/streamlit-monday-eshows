import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

#datatest-apps
def run():
    st.set_page_config(
        page_title="Eshows Data",
        page_icon="🎤",
    )

    st.write("# Sprints and Database data!")

    st.markdown(
        """
        Select an option:
        - Sprint Metrics: upload .csv files to analise the a sprint data, files can be generated in our [Scrum Data Dheet](https://docs.google.com/spreadsheets/d/1QHdAKnDqC_1pfwPu89BH1-zxe0Saj8xhqqDfb5nl10Y/edit?usp=sharing)
        - Sprint Data: upload .csv files to analise the data from every sprint, files can be generated in our [Scrum Data Dheet](https://docs.google.com/spreadsheets/d/1QHdAKnDqC_1pfwPu89BH1-zxe0Saj8xhqqDfb5nl10Y/edit?usp=sharing)
        - Database: page connected to our database, its possible to run querys and analise data
        - Monday: page to see data colected from monday API(flow de radar)
    """
    )


if __name__ == "__main__":
    run()
