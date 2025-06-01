import os
import matplotlib.pyplot as plt
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
from dotenv import load_dotenv
from components._layout import fullpage_centered_background, box_container, layout_box
from components._login import login_box, failed_box, authenticated_layout
from components import box
from components._plot import Fetch_Visualize
import utils


#===========================#
load_dotenv()

VALID_USERNAME = os.getenv("VALID_USERNAME", "")
VALID_PASSWORD = os.getenv("VALID_PASSWORD", "")
FIREBASE_PROJECT = os.getenv("FIREBASE_PROJECT", "")
FIREBASE_COLLECTION = os.getenv("FIREBASE_COLLECTION", "")


login_state = reactive.Value("pending")

app_ui = ui.page_fluid(
    ui.panel_title("Fitbit Shiny App"),
    ui.output_ui("main_content")
)

##
firecloudClient = utils.firebase_init(FIREBASE_PROJECT, FIREBASE_COLLECTION)
vis = Fetch_Visualize(firecloudClient, "IT-1-p001")


#===========================#
def server(input, output, session):

    @output
    @render.ui
    def main_content():
        if login_state() == "pending":
            return fullpage_centered_background(box_container(login_box()))
        elif login_state() == "authenticated":
            return authenticated_layout(input.username())
        else:
            return fullpage_centered_background(box_container(failed_box()))

    @output
    @render.ui
    def dashboard_content():
        if login_state() == "authenticated":

            return ui.div(
                layout_box(
                    id=1, 
                    title="User OAuth Token", 
                    colspan=1, 
                    rowspan=1, 
                    content=box.box_auth_token(
                        user_name = input.username()
                    )
                ),
                layout_box(
                    id=2, 
                    title="Data Source", 
                    colspan=2, 
                    rowspan=1, 
                    content=box.box_info(
                        info={
                            'firebase': firecloudClient.collection("test-streamlit"),
                            'choices': vis.day_ATS,
                        } 
                    )
                ),
                layout_box(
                    id=3, 
                    title="Intra-day Steps Activities",
                    colspan=3, 
                    rowspan=1, 
                    content=output_widget("plot_intraSteps_line")
                ),
                layout_box(
                    id=4, 
                    title="Total Steps",
                    colspan=1, 
                    rowspan=1, 
                    content=output_widget("plot_Steps_gauge")
                    
                ),
                layout_box(
                    id=5, 
                    title="Intra-day Heart Rates", 
                    colspan=3,
                    rowspan=2, 
                    content=output_widget("plot_HR_line")           
                ),
                layout_box(
                    id=6, 
                    title="Heart Rate Distribution",
                    colspan=3,
                    rowspan=1, 
                    content=output_widget("plot_HR_distribution")           
                ),
                layout_box(
                    id=7, 
                    title="Total Distances",
                    colspan=1,
                    rowspan=1, 
                    content=output_widget("plot_Distances_gauge")
                ),
                layout_box(
                    id=8, 
                    title="Time - Active Zones", 
                    colspan=2,
                    rowspan=1, 
                    content=output_widget("plot_ActiveMinutes_bar"), 
                ),
                layout_box(
                    id=9, 
                    title="Distance - Active Zones", 
                    colspan=2,
                    rowspan=1, 
                    content=output_widget("plot_ActiveDistances_bar"), 
                ),
                style="""
                    display: grid;
                    grid-template-columns: repeat(7, 210px);
                    grid-template-rows: repeat(3, 220px);
                    gap: 3px;
                    max-width: 100%;
                    over-flow: hidden;
                """
            )
    

    @output
    @render_widget
    @reactive.event(input.button_fetch)
    def plot_intraSteps_line():
        # Use the selected day input to filter data
        (df, total_step) = vis.data_ATS[input.selected_day()]
        fig = vis.plot_ActivityTimeSeries(df)
        return fig


    @output
    @render_widget
    @reactive.event(input.button_fetch)
    def plot_Steps_gauge():
        # Use the selected day input to filter data
        (df, total_step) = vis.data_ATS[input.selected_day()]
        fig = vis.plot_gauge(
            suffix=' (steps)', 
            title="(out of 10K)",
            value=total_step, 
            max_value=10000
        )
        return fig


    @output
    @render_widget
    @reactive.event(input.button_fetch)
    def plot_HR_line():
        # Use the selected day input to filter data
        df = vis.data_HRTS[input.selected_day()]
        fig = vis.plot_HeartRateTimeSeries(df)
        return fig


    @output
    @render_widget
    @reactive.event(input.button_fetch)
    def plot_HR_distribution():
        # Use the selected day input to filter data
        df = vis.data_HRTS[input.selected_day()]
        fig = vis.plot_HeartRateDistribution(df)
        return fig


    @output
    @render_widget
    @reactive.event(input.button_fetch)
    def plot_Distances_gauge():
        # Use the selected day input to filter data
        (df_activeDistances, _) = vis.data_A[input.selected_day()]
        distance = df_activeDistances[df_activeDistances['activity']=='tracker'].get('distance').values

        fig = vis.plot_gauge(
            suffix=' (km)', 
            title="(out of 8.05)",
            value=float(distance), 
            max_value=8.05
        )
        return fig


    @output
    @render_widget
    @reactive.event(input.button_fetch)
    def plot_ActiveMinutes_bar():
        # Use the selected day input to filter data
        (_, activeMinutes) = vis.data_A[input.selected_day()]
        fig = vis.plot_ActiveMinutes(activeMinutes)
        return fig


    @output
    @render_widget
    @reactive.event(input.button_fetch)
    def plot_ActiveDistances_bar():
        # Use the selected day input to filter data
        (df_activeDistances, _) = vis.data_A[input.selected_day()]
        fig = vis.plot_ActiveDistances(df_activeDistances)
        return fig





    @reactive.Effect
    def _init_login():
        login_state.set("pending")

    @reactive.Effect
    @reactive.event(input.btn_login)
    def _handle_login():
        username = input.username()
        password = input.password()
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            login_state.set("authenticated")
        else:
            login_state.set("failed")

    @reactive.Effect
    @reactive.event(input.btn_get_started)
    def _handle_back():
        login_state.set("pending")

    @reactive.Effect
    @reactive.event(input.btn_logout)
    def _handle_logout():
        login_state.set("pending")





#######################3
app = App(app_ui, server)
