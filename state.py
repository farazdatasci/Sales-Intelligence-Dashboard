import streamlit as st

def init_state():
    if "df" not in st.session_state:
        st.session_state.df = None

    if "filters" not in st.session_state:
        st.session_state.filters = {
            "group": [],
            "area": [],
            "product": []
        }