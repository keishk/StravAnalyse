import streamlit as st
from streamlit_folium import folium_static
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from src.model.plot import plot_activity, plot_data, plot_heatmap
from src.model.process import process_activity, process_data
from src.strava_api import get_activity, get_data


def run_page_main():
    list_methods = ["login", "token"]
    list_users = ["demo", "k1", "c1"]
    list_sport = ["run", "swim", "ride"]
    list_metrics = [
        "avg_speed (km/h)",
        "distance (km)",
        "moving_time (min)",
        "pace (min/km)",
        "total_elev_gain (m)",
    ]

    with st.sidebar:
        login_method = st.selectbox("Login method", list_methods)
        if login_method == "login":
            user = st.selectbox("User", list_users)
            password = st.text_input("Password", type="password")
            client_id = None
            client_secret = None
            refresh_token = None
            submit_token = None

        elif login_method == "token":
            with st.form("token_form"):
                client_id = st.text_input("Client ID")
                client_secret = st.text_input("Client secret")
                refresh_token = st.text_input("Refresh token")
                submit_token = st.form_submit_button("Submit")
                user = "None"
                password = "None"

    if any(
        (
            user == "demo",
            (login_method == "login")
            & (user != "demo")
            & (password == st.secrets[user]["pass"]),
            submit_token,
        )
    ):
        my_dataset = get_data(
            app=True,
            login_method=login_method,
            user=user,
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
        )
        sport = st.select_slider("", list_sport)
        _, runs, rides, swims = process_data(my_dataset, user=user)
        if sport == "run":
            df = runs
        elif sport == "ride":
            df = rides
        elif sport == "swim":
            df = swims

        st.header("Overall Performance")
        c1_1, c1_2, c1_3, c1_4 = st.columns(4)
        x = c1_1.selectbox("Set x-axis", ["date"] + list_metrics)
        y = c1_2.selectbox("Set y-axis", list_metrics)
        color = c1_3.selectbox("Set color", ["year"])
        c1_4.text("")
        line = c1_4.checkbox("Show best fit", True)
        fig_data = plot_data(df, x, y, color, line)
        st.plotly_chart(fig_data, True)
        st.header("")

        st.header("Activity Heatmap")
        c2_1, c2_2, = st.columns(2)
        list_years = ["2018", "2019", "2020", "2021"]
        with c2_1:
            year_1 = st.selectbox("", list_years, len(list_years) - 2)
            fig_heatmap_1 = plot_heatmap(df, year_1)
            folium_static(fig_heatmap_1, 500)
        with c2_2:
            year_2 = st.selectbox("", list_years, len(list_years) - 1)
            fig_heatmap_2 = plot_heatmap(df, year_2)
            folium_static(fig_heatmap_2, 500)

        st.header("")

        st.header("Activity Performance")

        df_display = df.copy().reset_index(drop=True)
        cols_float = [
            "distance (km)",
            "moving_time (min)",
            "total_elev_gain (m)",
            "avg_speed (km/h)",
        ]
        cols_device = [
            "average_cadence",
            "average_heartrate",
            "max_heartrate",
        ]
        if cols_device[0] in df_display:
            df_display = df_display[
                ["date", "name"] + cols_float + cols_device + ["id"]
            ]
        else:
            df_display = df_display[["date", "name"] + cols_float + ["id"]]

        df_display.loc[:, "date"] = df_display["date"].dt.strftime("%m-%d-%Y")

        gb = GridOptionsBuilder.from_dataframe(df_display)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_selection("single")
        grid_response = AgGrid(
            df_display,
            gridOptions=gb.build(),
            height=305,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            fit_columns_on_grid_load=True,
            theme="streamlit",
        )
        try:
            select_aggrid = grid_response["selected_rows"][0]["id"]
            data_activity = get_activity(user, select_aggrid, True)
            df_activity = process_activity(data_activity)
            df_activity = df_activity[
                [
                    "time",
                    "velocity_smooth",
                    "heartrate",
                    "distance",
                    "altitude",
                    "cadence",
                    "moving",
                    "grade_smooth",
                ]
            ]
            c3_1, c3_2, c3_3, c3_4 = st.columns(4)
            x_activity = c3_1.selectbox("Set x-axis", df_activity.columns, 0)
            y1_activity = c3_2.selectbox("Set y1-axis", df_activity.columns, 1)
            y2_activity = c3_3.selectbox("Set y2-axis", df_activity.columns, 2)
            c3_4.text("")
            fig_activity = plot_activity(
                df_activity, x_activity, y1_activity, y2_activity
            )
            st.plotly_chart(fig_activity, True)
        except IndexError:
            pass

    else:
        st.warning("Enter password.")

