import requests
import urllib3

import streamlit as st


# get rid of insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_data(
    app, login_method, user, client_id=None, client_secret=None, refresh_token=None
):
    auth_url = "https://www.strava.com/oauth/token"
    activites_url = "https://www.strava.com/api/v3/athlete/activities"

    # POST request, so needs payload
    if app:
        if login_method == "login":
            payload = {
                "client_id": st.secrets[user]["strava_client_id"],
                "client_secret": st.secrets[user]["strava_client_secret"],
                "refresh_token": st.secrets[user]["strava_refresh_token"],
                "grant_type": "refresh_token",
                "f": "json",
            }
        else:
            payload = {
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
                "f": "json",
            }

    else:
        from config import strava_client_id, strava_client_secret, strava_refresh_token

        payload = {
            "client_id": strava_client_id,
            "client_secret": strava_client_secret,
            "refresh_token": strava_refresh_token,
            "grant_type": "refresh_token",
            "f": "json",
        }

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()["access_token"]
    header = {"Authorization": "Bearer " + access_token}
    param = {"per_page": 200, "page": 1}
    my_dataset = requests.get(activites_url, headers=header, params=param).json()
    return my_dataset


def get_activity(user, activity_id, app):
    auth_url = "https://www.strava.com/oauth/token"
    activites_url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams?keys=time,distance,latlng,altitude,velocity_smooth,heartrate,cadence,watts,temp,moving,grade_smooth&key_by_type=true"

    # POST request, so needs payload
    if app:
        payload = {
            "client_id": st.secrets[user]["strava_client_id"],
            "client_secret": st.secrets[user]["strava_client_secret"],
            "refresh_token": st.secrets[user]["strava_refresh_token"],
            "grant_type": "refresh_token",
            "f": "json",
        }
    else:
        from config import strava_client_id, strava_client_secret, strava_refresh_token

        payload = {
            "client_id": strava_client_id,
            "client_secret": strava_client_secret,
            "refresh_token": strava_refresh_token,
            "grant_type": "refresh_token",
            "f": "json",
        }

    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()["access_token"]
    header = {"Authorization": "Bearer " + access_token}
    param = {"per_page": 200, "page": 1}
    data = requests.get(activites_url, headers=header, params=param).json()
    return data

