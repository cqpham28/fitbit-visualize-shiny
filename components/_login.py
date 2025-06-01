from shiny import ui


def login_box():
    return ui.div(
        ui.h3("Login", style="text-align: center; margin-bottom: 20px;"),
        ui.input_text("username", "Username"),
        ui.input_password("password", "Password"),
        ui.div(
            ui.input_action_button("btn_login", "Login", class_="btn-success"),
            style="text-align: center; margin-top: 20px;"
        ),
    )

def failed_box():
    return ui.div(
        ui.h3("Login Failed! Try again."),
        ui.input_action_button("btn_get_started", "Back", class_="btn-danger")
    )

def authenticated_layout(username):
    return ui.tags.div(
        ui.tags.div(
            ui.div(
                ui.tags.div(
                    username[0].upper(),
                    style="""
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        background-color: #007bff;
                        color: white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 14px;
                        font-weight: bold;
                        margin-right: 10px;
                    """
                ),
                ui.h4(f"Welcome back, {username}", style="margin: 0;"),
                style="display: flex; align-items: center;"
            ),
            ui.input_action_button("btn_logout", "Logout", class_="btn-danger"),
            style="""
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                background-color: #f0f0f0;
                border-bottom: 1px solid #ddd;
                width: 100%;
                position: fixed;
                top: 0;
                left: 0;
                z-index: 1000;
            """
        ),
        ui.tags.div(
            ui.output_ui("dashboard_content"),
            style="margin-top: 20px; padding: 20px;"
        ),
        style="height: 100vh; width: 100vw; display: flex; flex-direction: column;"
    )