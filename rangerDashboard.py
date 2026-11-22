import gradio as gr

# CUSTOM CSS

custom_css = """
body, .gradio-container {
    background: #0b0f19 !important;
    color: white !important;
}

.sidebar {
    background: #24292f !important;
    padding: 25px;
    border-radius: 12px;
}

.main-content {
    background: #0b0f19 !important;
    color: #FFFFFF !important;
    padding: 25px;
    
}
.main-content h1,
.main-content h2,
.main-content h3,
.main-content p {
color: #FFFFFF !important;
}

.sidebar button {
    background: #254150 !important;
    color: white !important;
}

.sidebar h1 {
    color: #11ba88 !important;
}
"""


# DASHBOARD
with gr.Blocks(
    title="NotFlock Ranger Dashboard",
    css=custom_css,
    theme=gr.themes.Base(
        primary_hue="green",
        neutral_hue="slate"
        )
        ) as demo:
        
        
    with gr.Row():

        # SIDEBAR
        with gr.Column(scale=1, elem_classes="sidebar"):

            gr.Markdown("# NOTFLOCK")
            gr.Markdown("Ranger Command Center")

            gr.Markdown("### Navigation")

            home_btn = gr.Button("Home")
            alerts_btn = gr.Button("Live Alerts")
            map_btn = gr.Button("Monitoring Map")
            sensors_btn = gr.Button("Sensors")
            history_btn = gr.Button("Alert History")
            reports_btn = gr.Button("Reports")

        # MAIN CONTENT
        with gr.Column(scale=4, elem_classes="main-content"):

            #HOME PAGE
            with gr.Column(visible=True) as home_page:
                gr.Markdown("# Dashboard Overview")
                gr.Markdown("Welcome to the Ranger Command Center")
                
                with gr.Row():

                    with gr.Column():
                        gr.Markdown("### Active Sensors")
                        gr.Markdown("## 12")

                    with gr.Column():
                        gr.Markdown("### Active Alerts")
                        gr.Markdown("## 03")
                        
                gr.Markdown("---")
                gr.Markdown("### Recent Activity")
                gr.Markdown("No recent alerts to display.")


            #LIVE ALERTS PAGE
            with gr.Column(visible=False) as alerts_page:
                gr.Markdown("# Live Alerts")
                gr.Markdown("Mountain lion detection alerts will be shown here")
                gr.Markdown("This page needs to have option for rangers to turn off and classify alarms")


            #MAP PAGE
            with gr.Column(visible=False) as map_page:
                gr.Markdown("# Map Page")
                gr.Markdown("The map area with pins of recent alerts and sensors will be shown on this page")
                gr.Markdown("The map needs to include park and area within 2 miles of the park")

            #SENSORS PAGE
            with gr.Column(visible=False) as sensors_page:
                gr.Markdown("# Sensors Page")
                gr.Markdown("This page will show active sensors")

            #ALERT HISTORY PAGE
            with gr.Column(visible=False) as history_page:
                gr.Markdown("# Alert History Page")
                gr.Markdown("This page will show alerts in past 30 days")

            #REPORTS PAGE
            with gr.Column(visible=False) as reports_page:
                gr.Markdown("# Reports Page")
                gr.Markdown("This page will show reports for this system")
                gr.Markdown("- A Report Showing All Detections by Date & Classification (Definite, Suspected, or False)")
                gr.Markdown("- A reporting showing all detections by sensor location")
                gr.Markdown("- A report showing detection classification by ranger")
                
                        
                        
        def show_home_page():
            return(
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )

        def show_alerts_page():
            return(
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )

        def show_map_page():
            return(
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False)
            )

        def show_sensors_page():
            return(
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )

        def show_history_page():
            return(
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True),
                gr.update(visible=False)
            )

        def show_reports_page():
            return(
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(visible=True)
            )
            
        home_btn.click(
            fn=show_home_page,
            outputs=[home_page,alerts_page,map_page, sensors_page, history_page, reports_page]
        )
        
        alerts_btn.click(
            fn=show_alerts_page,
            outputs=[home_page, alerts_page, map_page, sensors_page, history_page, reports_page]
        )

        map_btn.click(
            fn=show_map_page,
            outputs=[home_page, alerts_page, map_page, sensors_page, history_page, reports_page]
        )

        sensors_btn.click(
            fn=show_sensors_page,
            outputs=[home_page, alerts_page, map_page, sensors_page, history_page, reports_page]
        )

        history_btn.click(
            fn=show_history_page,
            outputs=[home_page, alerts_page, map_page, sensors_page, history_page, reports_page]
        )

        reports_btn.click(
            fn=show_reports_page,
            outputs=[home_page, alerts_page, map_page, sensors_page, history_page, reports_page]
        )
        
        
    demo.launch()
