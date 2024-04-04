import streamlit as st
from streamlit_gsheets import GSheetsConnection

class GSheetsReader:
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)
    
    def taskControl(self):
        df = self.conn.read(worksheet="SprintTaskControl", ttl=0)
        return df
    
    def sprintMetrics(self):
        df = self.conn.read(worksheet="SprintMetrics", ttl=0)
        return df