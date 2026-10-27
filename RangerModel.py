import os
import csv
import glob
import datetime
import subprocess
import pandas as pd
import gradio as gr


class ParkConfig:
    PARK_NAME = "San Diego County Park Domain"
    STATION_LAT = 32.7157
    STATION_LON = -117.1611

    CUSTOM_MODEL_PATH = "/Users/vpartain/Desktop/WIP/mountain_lion_model.tflite"
    OUTPUT_TEMP_DIR = "/Users/vpartain/Desktop/WIP/results"
    CONFIDENCE_THRESHOLD = 0.40


class SimpleAlertStore:
    def __init__(self):
        self.alerts = []

    def add_alert(self, sensor_id, lat, lon, noise_type, strength, confidence):
        alert = {
            "ID": len(self.alerts) + 1,
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Sensor ID": sensor_id,
            "Latitude": lat,
            "Longitude": lon,
            "Noise Type": noise_type,
            "dB Strength": strength,
            "Confidence": f"{confidence:.2%}",
            "Classification": "Unclassified",  # Req 4
            "Ranger": "Unassigned"
        }
        self.alerts.append(alert)
        return alert

    def update_classification(self, alert_id, classification, ranger_name):
        for alert in self.alerts:
            if alert["ID"] == int(alert_id):
                alert["Classification"] = classification
                alert["Ranger"] = ranger_name
                break

    def get_dataframe(self):
        if not self.alerts:
            return pd.DataFrame(columns=[
                "ID", "Timestamp", "Sensor ID", "Latitude", "Longitude",
                "Noise Type", "dB Strength", "Confidence", "Classification", "Ranger"
            ])
        return pd.DataFrame(self.alerts)


store = SimpleAlertStore()


def analyze_audio_clip(audio_file_path):
    os.makedirs(ParkConfig.OUTPUT_TEMP_DIR, exist_ok=True)

    old_files = glob.glob(os.path.join(ParkConfig.OUTPUT_TEMP_DIR, "*.txt")) + glob.glob(
        os.path.join(ParkConfig.OUTPUT_TEMP_DIR, "*.csv"))
    for f in old_files:
        try:
            os.remove(f)
        except OSError:
            pass

    try:
        subprocess.run([
            "birdnet-analyze",
            "--classifier", ParkConfig.CUSTOM_MODEL_PATH,
            "--output", ParkConfig.OUTPUT_TEMP_DIR,
            "--min_conf", "0.10",
            audio_file_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        result_files = glob.glob(os.path.join(ParkConfig.OUTPUT_TEMP_DIR, "*.txt")) + glob.glob(
            os.path.join(ParkConfig.OUTPUT_TEMP_DIR, "*.csv"))
        if not result_files:
            return False, 0.0, []

        high_confidence_matches = []
        max_confidence = 0.0

        with open(result_files[0], "r") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                conf = float(row.get("Confidence", 0))
                species = row.get("Common Name", "") or row.get("Scientific Name", "") or "Mountain Lion"

                if conf > max_confidence:
                    max_confidence = conf

                if conf >= ParkConfig.CONFIDENCE_THRESHOLD:
                    start = row.get("Start (s)", "N/A")
                    end = row.get("End (s)", "N/A")
                    high_confidence_matches.append({
                        "start": start,
                        "end": end,
                        "confidence": conf,
                        "species": species
                    })

        is_detected = len(high_confidence_matches) > 0
        return is_detected, max_confidence, high_confidence_matches

    except Exception as e:
        print(f"Detection Engine Error: {e}")
        return False, 0.0, []


def process_transmission(audio_path, sensor_id, lat, lon):
    if not audio_path:
        return "Please select an audio file.", store.get_dataframe(), None

    detected, conf, matches = analyze_audio_clip(audio_path)

    if detected:
        species_label = matches[0]["species"] if matches else "Mountain Lion"
        store.add_alert(sensor_id, float(lat), float(lon), species_label, 78.5, conf)

        status_msg = f"ALARM TRIGGERED: Mountain Lion Detected at {sensor_id} ({conf:.2%} Confidence)!"
        return status_msg, store.get_dataframe()
    else:
        return "System Clear: No Mountain Lion signature detected.", store.get_dataframe()


def classify_selected_alert(alert_id, classification, ranger_name):
    if not alert_id:
        return "Please enter a valid Alert ID.", store.get_dataframe()

    store.update_classification(alert_id, classification, ranger_name)
    return f"Alert #{alert_id} successfully classified as '{classification}' by {ranger_name}.", store.get_dataframe()


def generate_report_5a():
    df = store.get_dataframe()
    if df.empty:
        return "No alert records available."
    return df.groupby(["Timestamp", "Classification"]).size().reset_index(name="Detections Count").to_string(
        index=False)


def generate_report_5b():
    df = store.get_dataframe()
    if df.empty:
        return "No alert records available."
    return df.groupby(["Sensor ID", "Latitude", "Longitude"]).size().reset_index(name="Total Detections").to_string(
        index=False)


def generate_report_5d():
    df = store.get_dataframe()
    if df.empty:
        return "No alert records available."
    return df.groupby(["Ranger", "Classification"]).size().reset_index(name="Classified Count").to_string(index=False)


with gr.Blocks(title=f"Ranger Platform - {ParkConfig.PARK_NAME}") as app:
    gr.Markdown(f"# Ranger Control Platform - {ParkConfig.PARK_NAME}")

    with gr.Tabs():
        with gr.Tab("Live Dashboard"):
            status_banner = gr.Textbox(label="System Status / Alarm Banner",
                                       value="System Operational - Monitoring Active", interactive=False)

            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("Process Transmission")
                    audio_input = gr.Audio(sources=["upload", "microphone"], type="filepath",
                                           label="Sensor Transmission Clip")
                    sensor_input = gr.Textbox(value="SENSOR-01", label="Sensor ID")
                    lat_input = gr.Number(value=32.7180, label="Latitude")
                    lon_input = gr.Number(value=-117.1630, label="Longitude")
                    btn_run = gr.Button("Analyze Clip", variant="primary")

                with gr.Column(scale=2):
                    gr.Markdown("Active Detections Log")
                    alerts_table = gr.Dataframe(value=store.get_dataframe(), interactive=False)

            gr.Markdown("---")
            gr.Markdown("Ranger Classification Triage")
            with gr.Row():
                alert_id_input = gr.Number(label="Alert ID to Classify", precision=0)
                ranger_name_input = gr.Textbox(value="Ranger Smith", label="Ranger Name")
                btn_def = gr.Button("Definite", variant="stop")
                btn_sus = gr.Button("Suspected")
                btn_fal = gr.Button("False Alarm")

            triage_status = gr.Textbox(label="Triage Action Result", interactive=False)

            btn_run.click(process_transmission, inputs=[audio_input, sensor_input, lat_input, lon_input],
                          outputs=[status_banner, alerts_table])
            btn_def.click(lambda aid, rname: classify_selected_alert(aid, "Definite", rname),
                          inputs=[alert_id_input, ranger_name_input], outputs=[triage_status, alerts_table])
            btn_sus.click(lambda aid, rname: classify_selected_alert(aid, "Suspected", rname),
                          inputs=[alert_id_input, ranger_name_input], outputs=[triage_status, alerts_table])
            btn_fal.click(lambda aid, rname: classify_selected_alert(aid, "False", rname),
                          inputs=[alert_id_input, ranger_name_input], outputs=[triage_status, alerts_table])

        with gr.Tab("Reports"):
            gr.Markdown("System Reports")
            with gr.Row():
                btn_r5a = gr.Button("Report by Date & Classification")
                btn_r5b = gr.Button("Report by Sensor Location")
                btn_r5d = gr.Button("Report by Ranger")

            report_output = gr.Textbox(label="Generated Report Output", lines=10, interactive=False)

            btn_r5a.click(generate_report_5a, outputs=report_output)
            btn_r5b.click(generate_report_5b, outputs=report_output)
            btn_r5d.click(generate_report_5d, outputs=report_output)

if __name__ == "__main__":
    app.launch(inbrowser=True)