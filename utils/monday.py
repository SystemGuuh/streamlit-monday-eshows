import toml
import requests
import streamlit as st

def load_api_key():
    return st.secrets['monday']['api_key']

def makeRequestByQuery(query):
    headers = {"Authorization": load_api_key()} 
    query3 = query
    apiUrl = "https://api.monday.com/v2"
    data = {'query' : query3}
    r = requests.post(url=apiUrl, json=data, headers=headers)
    return r.json()
