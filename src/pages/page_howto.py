import json
import requests

import streamlit as st


def run_page_howto():
    st.header("Token Guide")
    st.write(
        """
    Following [this](https://developers.strava.com/docs/getting-started/#oauth) link, the necessary Refresh Token can be generated.
    Alternatively, the following instructions can be used to easily generate the token.
    """
    )
    st.subheader("")

    st.text("1. Enable API.")
    st.write("https://www.strava.com/settings/api")
    st.subheader("")

    st.text("2. Enter the following.")
    st.write(
        """
    Application Name: App (or any name)\n
    Website: https://www.strava.com (or any link)\n
    Authorization Callback Domain: localhost\n

    Image: Add any image
    """
    )
    st.subheader("")

    st.text("3. Note the Client ID and Client Secret.")
    st.subheader("")

    st.text("4. Enter Client ID, click generated link below and authorize.")
    c1_1, c1_2 = st.columns([1, 5])
    client_id = c1_1.text_input("Enter Client ID", "").strip()
    c1_2.header("")
    st.write(
        f"https://www.strava.com/oauth/authorize?client_id={client_id}&redirect_uri=http://localhost&response_type=code&scope=activity:read_all",
    )
    st.subheader("")

    st.text("5. This will fail, but copy the URL. Enter URL and Client Secret.")
    c2_1, c2_2 = st.columns([1, 1])
    failed = c2_1.text_input("Enter URL", "").strip()
    client_secret = c2_1.text_input("Enter Client Secret", "").strip()
    c2_2.text("")
    if failed:
        auth = failed.split("&")[1][5:]

    payload = {}
    headers = {}
    if client_secret:
        url = f"https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={auth}&grant_type=authorization_code"
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)
        if data["refresh_token"]:
            refresh = data["refresh_token"]

    st.subheader("")
    st.text("6. Save Refresh Token below.")
    if client_secret:
        st.text_input("Save Refresh Token", refresh)
    st.subheader("")

    st.text("7. Use Client ID, Client Secret and Refresh Token to login.")
    st.subheader("")
    st.subheader("")

    st.text("Note: Login data not stored.")
