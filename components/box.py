from shiny import ui
from utils import get_base64_image



#===========================#
def box_auth_token(user_name):
    fullName = "Cuong Pham"
    gender = "Male"
    age = 27
    time_left = 8 * 3600  # 8 hours in seconds
    image_base64 = get_base64_image(user_name)
    timer_id = f"timer_{user_name.replace(' ', '_')}"
    return ui.HTML(f"""
        <div style="
            padding-top: 10px;
            width: 180px;
            height: 180px;
            background-color: #e8e8e0;
            border-radius: 15px;
            text-align: center;
            transition: transform 0.2s;
        ">
            <img src="data:image/png;base64,{image_base64}" 
                style="
                    width: 80px;
                    height: 80px;
                    background-color: #bbb;
                    border-radius: 50%;
                    margin-top: 5px;
                    margin-bottom: 10px;
                "
            />
            <div style="font-family: monospace; font-size: 15px; color: black;">
                {fullName}
            </div>
            <div style='
                background-color: #11f329;
                border: 1px solid black;
                color: #155724;
                padding: 5px;
                margin: 5px;
                border-radius: 10px;
                font-family: monospace;
                font-size: 12px;
                font-weight: bold;
                text-align: center;
                margin-top: 10px;
                user-select: none;
            '>
                TOKEN ACTIVE<br>
                <span id="{timer_id}" style="font-weight: bold;">00:00:00</span>
            </div>
        </div>
        <script>
        setTimeout(function() {{
            function getTimeRemaining(endtime) {{
                const total = Date.parse(endtime) - Date.parse(new Date());
                const seconds = Math.floor((total / 1000) % 60);
                const minutes = Math.floor((total / 1000 / 60) % 60);
                const hours = Math.floor((total / (1000 * 60 * 60)));
                return {{ total, hours, minutes, seconds }};
            }}

            function initializeClock(id, endtime) {{
                const timeSpan = document.getElementById(id);
                function updateClock() {{
                    const t = getTimeRemaining(endtime);
                    if (t.total <= 0) {{
                        clearInterval(timeinterval);
                        timeSpan.innerHTML = "EXPIRED";
                        timeSpan.parentElement.style.backgroundColor = "#fff3cd";
                        timeSpan.parentElement.style.color = "#856404";
                        return;
                    }}
                    timeSpan.innerHTML =
                        ('0' + t.hours).slice(-2) + ':' +
                        ('0' + t.minutes).slice(-2) + ':' +
                        ('0' + t.seconds).slice(-2);
                }}
                updateClock();
                const timeinterval = setInterval(updateClock, 1000);
            }}

            const deadline = new Date(Date.parse(new Date()) + {time_left} * 1000);
            initializeClock("{timer_id}", deadline);
        }}, 100);
        </script>
    """)




#===========================#
def box_info(info):
    """
    Creates a styled layout box with a floating title and interaction
    """
    return ui.div(
        # Container div with fixed size and padding
        ui.div(
            # Status display
            ui.tags.div(f"Storage: {info['firebase']}",
                style="""
                    margin-top: 4px;
                    font-size: 12px; 
                    color: green; 
                """
            ),
            # Date selector (shorter width)
            ui.input_select(
                "selected_day", "Select a day:",
                choices=info['choices'],  # Replace with actual dates
                selected=info['choices'][0],
            ),
            # Action button (smaller)
            ui.input_action_button(
                id="button_fetch",
                label="Fetch Data",
                class_="btn btn-sm btn-secondary",  # Smaller button styling
                style="""
                    width: 100px;
                    height: 40px;
                    font-size: 12px;
                    padding: 2px 2px;
                """
            ),
            style="""
                box-sizing: border-box;
                display: flex;
                flex-direction: column;
                gap: 8px;
                padding: 2px;
            """
        ),
    )

