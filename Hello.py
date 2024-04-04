import streamlit as st
from streamlit.logger import get_logger
import subprocess

LOGGER = get_logger(__name__)

def installPkgConfig():
    # Define the command to install pkg-config
    command = "sudo apt install pkg-config"

    # Execute the command
    try:
        subprocess.run(command, shell=True, check=True)
        print("pkg-config installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error installing pkg-config:", e)

#datatest-apps
def run():
    installPkgConfig()
    
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
