from datetime import time

import pandas as pd
import polyline
import streamlit as st


def decode(x):
    try:
        return polyline.decode(x)
    except TypeError:
        pass


def process_activity(data):
    df = pd.json_normalize(data)
    data_cols = [col for col in df.columns if "data" in col]
    df = df[data_cols]
    df = df.apply(pd.Series.explode)
    df.columns = [col.split(".")[0] for col in df.columns]
    return df


def process_data(my_dataset, user, app=True):
    activities = pd.json_normalize(my_dataset)

    activities["map.polyline"] = activities["map.summary_polyline"].apply(decode)
    activities["start_date_local"] = pd.to_datetime(activities["start_date_local"])
    activities["time"] = activities["start_date_local"].dt.time
    activities["date"] = activities["start_date_local"].dt.normalize()
    activities["year"] = activities["start_date_local"].dt.year.astype(str)

    activities.loc[:, "distance"] /= 1000  # convert from m to km
    activities.loc[:, "average_speed"] *= 3.6  # convert from m/s to km/h
    activities.loc[:, "max_speed"] *= 3.6  # convert from m/s to km/h
    activities.loc[:, "moving_time"] /= 60  # convert from s to min

    activities["pace (min/km)"] = activities.moving_time / activities.distance

    activities = round(activities, 2)
    activities = activities.rename(
        columns={
            "distance": "distance (km)",
            "average_speed": "avg_speed (km/h)",
            "max_speed": "max_speed (km/h)",
            "moving_time": "moving_time (min)",
            "total_elevation_gain": "total_elev_gain (m)",
        }
    )

    activities = activities.set_index("start_date_local").sort_index(ascending=False)
    runs = activities.loc[activities["type"] == "Run"]
    rides = activities.loc[activities["type"] == "Ride"]
    swims = activities.loc[activities["type"] == "Swim"]

    if user == "demo":
        for (sport, name) in [(runs, "run"), (rides, "ride"), (swims, "swim")]:

            sport.loc[
                sport.between_time(time(0), time(11)).index, "name"
            ] = f"Morning {name}"
            sport.loc[
                sport.between_time(time(11), time(14)).index, "name"
            ] = f"Afternoon {name}"
            sport.loc[
                sport.between_time(time(14), time(18)).index, "name"
            ] = f"Evening {name}"
            sport.loc[
                sport.between_time(time(18), time(0)).index, "name"
            ] = f"Night {name}"

            if name != "swim":
                if app:
                    sport.loc[:, "map.polyline"] = sport["map.polyline"].apply(
                        lambda x: mask_loc(x)
                    )
                else:
                    sport.loc[:, "map.polyline"] = sport["map.polyline"].apply(
                        lambda x: mask_loc(x, False)
                    )

    return activities, runs, rides, swims


def mask_loc(x, app=True):
    if app:
        lat_jit = st.secrets["demo"]["lat_jit"]
        lon_jit = st.secrets["demo"]["lon_jit"]
    else:
        from config import lat_jit, lon_jit

    return [(coord[0] + lat_jit, coord[1] + lon_jit) for coord in x]
