from shiny import ui



def fullpage_centered_background(content=None, bg_color="#f5f5f5"):
    return ui.tags.div(
        content,
        style=f"""
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: {bg_color};
        """
    )

def box_container(content, width="400px", padding="20px", bg_color="white"):
    return ui.tags.div(
        content,
        style=f"""
            max-width: {width};
            width: 100%;
            padding: {padding};
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            background-color: {bg_color};
        """
    )



def layout_box(id, title=None, colspan=1, rowspan=1, content=None):
    """
    Creates a layout box with an optional floating title above the border.
    """
    return ui.div(
        [
            # Title positioned above the box
            ui.div(
                title or f"Box {id}",
                style="""
                    position: absolute;
                    top: -12px;  /* Adjust as needed */
                    left: 10px;
                    background-color: #b1f7f8;  /* Or match background */
                    padding: 2px 5px;
                    font-weight: bold;
                    font-size: 14px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                """
            ),
            # Box content
            ui.div(
                content or f"(placeholder)",
                style="""
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    padding-top: 5px;
                """
            )
        ],
        id=f"box-{id}",
        style=f"""
            grid-column: span {colspan};
            grid-row: span {rowspan};
            position: relative;  /* Allow absolute positioning of title */
            border: 2px solid #ddd;
            border-radius: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            background-color: #fff;
            font-size: 14px;
            margin: 5px;
            padding: 5px;
        """
    )

