import streamlit as st


def setup_page(name: str):
    """
    Setup commands for Streamlit app.
    Sets tab title, tab icon.
    Hides footer, removes padding and removes setting options.
    """
    favicon = "src/setup/favicon.ico"
    st.set_page_config(
        page_title=name,
        page_icon=favicon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    hide_streamlit_style = """<style>footer {visibility: hidden;}</style>"""
    hide_padding = f"""<style>.reportview-container .main .block-container{{padding-top: 0;}}</style>"""
    hide_decoration_bar_style = """<style>header {visibility: hidden;}</style>"""

    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    st.markdown(hide_padding, unsafe_allow_html=True)
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)
