import streamlit as st

from src.pages.page_howto import run_page_howto
from src.pages.page_main import run_page_main
from src.setup.layout import setup_page

title = "StravAnalyse"
setup_page(title)


with st.sidebar:
    st.title(title)
    st.header("")
    page = st.selectbox("Select page", ["Main", "Token Guide"])

if page == "Main":
    run_page_main()

elif page == "Token Guide":
    run_page_howto()
