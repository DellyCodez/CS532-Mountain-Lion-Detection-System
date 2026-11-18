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

            overview_btn = gr.Button("Home")
            alerts_btn = gr.Button("Live Alerts")
            map_btn = gr.Button("Monitoring Map")
            sensors_btn = gr.Button("Sensors")
            history_btn = gr.Button("Alert History")
            reports_btn = gr.Button("Reports")

        # MAIN CONTENT
        with gr.Column(scale=4, elem_classes="main-content"):

            page_title = gr.Markdown("# Dashboard Overview")

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

            gr.Markdown(
                "No recent alerts to display."
            )

demo.launch()
