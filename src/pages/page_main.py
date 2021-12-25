import streamlit as st
from streamlit_folium import folium_static
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from src.model.plot import plot_activity, plot_data, plot_heatmap
from src.model.process import process_activity, process_data
from src.strava_api import get_activity, get_data


def run_page_main():
    list_methods = ["login"]
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

        elif login_method == "token":
            strava_client_id = st.text_input("Client ID")
            strava_client_secret = st.text_input("Client secret")
            strava_refresh_token = st.text_input("Refresh token")

    if (user == "demo") | ((user != "demo") & (password == st.secrets[user]["pass"])):
        sport = st.select_slider("", list_sport)
        my_dataset = get_data(app=True, user=user)
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
        c2_1, _1, c2_3, _2, = st.columns([1, 2, 1, 2])
        list_years = ["2018", "2019", "2020", "2021"]
        with c2_1:
            year_1 = st.selectbox("", list_years)
            fig_heatmap_1 = plot_heatmap(df, year_1)
            folium_static(fig_heatmap_1, 500)
        with c2_3:
            year_2 = st.selectbox("", list_years, 1)
            fig_heatmap_2 = plot_heatmap(df, year_2)
            folium_static(fig_heatmap_2, 500)
        _1.text("")
        _2.text("")
        st.header("")

        st.header("Activity Performance")

        df_act_list = df.copy().reset_index(drop=True)
        cols_float = [
            "distance (km)",
            "moving_time (min)",
            "total_elev_gain (m)",
            "avg_speed (km/h)",
            "average_cadence",
            "average_heartrate",
            "max_heartrate",
        ]
        df_act_list = df_act_list[["date", "name"] + cols_float + ["id"]]
        df_act_list.loc[:, "date"] = df_act_list["date"].dt.strftime("%d-%m-%Y")
        # st.dataframe(df_act_list.style.format(subset=cols_float, formatter="{:.2f}"))

        gb = GridOptionsBuilder.from_dataframe(df_act_list)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_selection("single")
        grid_response = AgGrid(
            df_act_list,
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
