# -----------------------------
# Import required Python modules
# -----------------------------

import os              # Used for working with folders and file paths
import csv             # Used to read CSV/TSV result files
import glob            # Used to find files matching a pattern
import datetime        # Used to record the date and time of alerts
import subprocess      # Used to run the external BirdNET command
import pandas as pd    # Used to organize alert data in tables
import gradio as gr    # Used to create the web-based user interface


# -----------------------------
# Application configuration
# -----------------------------

class ParkConfig:
    """
    Stores settings used throughout the application.

    Keeping settings in one class makes them easier to find and change.
    """

    # Name displayed in the application title and heading
    PARK_NAME = "San Diego County Park Domain"

    # Default location of the monitoring station
    STATION_LAT = 32.7157
    STATION_LON = -117.1611

    # Location of the custom BirdNET model file
    CUSTOM_MODEL_PATH = "/models/birdnet/mountain_lion_model.tflite"

    # Folder where BirdNET temporarily saves its results
    OUTPUT_TEMP_DIR = "/results"

    # Minimum confidence required before a detection becomes an alert
    #
    # For example, 0.40 means the model must be at least 40% confident.
    CONFIDENCE_THRESHOLD = 0.40


# -----------------------------
# Alert storage
# -----------------------------

class SimpleAlertStore:
    """
    Stores alerts while the program is running.

    This is an in-memory storage system, meaning that alerts are kept
    in a Python list and will disappear when the program closes.
    """

    def __init__(self):
        """
        Creates an empty list for storing alerts.
        """
        self.alerts = []

    def add_alert(self, sensor_id, lat, lon, noise_type, strength, confidence):
        """
        Creates a new alert and adds it to the alert list.

        Parameters:
            sensor_id:
                Name or ID of the sensor that submitted the recording.

            lat:
                Latitude where the sensor is located.

            lon:
                Longitude where the sensor is located.

            noise_type:
                Type of sound detected, such as "Mountain Lion".

            strength:
                Sound strength in decibels.

            confidence:
                Confidence score returned by the detection model.

        Returns:
            The newly created alert as a dictionary.
        """

        # Create a dictionary containing all information about the alert
        alert = {
            # Give the alert a number based on how many alerts already exist
            "ID": len(self.alerts) + 1,

            # Save the current date and time
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            # Store information about the sensor and its location
            "Sensor ID": sensor_id,
            "Latitude": lat,
            "Longitude": lon,

            # Store information about the detected sound
            "Noise Type": noise_type,
            "dB Strength": strength,

            # Convert a decimal such as 0.85 into a percentage such as 85.00%
            "Confidence": f"{confidence:.2%}",

            # Every new alert starts as unclassified
            "Classification": "Unclassified",

            # No ranger has reviewed the alert yet
            "Ranger": "Unassigned"
        }

        # Add the new alert to the list
        self.alerts.append(alert)

        # Return the alert in case another part of the program needs it
        return alert

    def update_classification(self, alert_id, classification, ranger_name):
        """
        Updates the classification and ranger assigned to an alert.

        Parameters:
            alert_id:
                The ID number of the alert to update.

            classification:
                The review result, such as "Definite", "Suspected",
                or "False".

            ranger_name:
                The name of the ranger reviewing the alert.
        """

        # Look through every alert in the list
        for alert in self.alerts:

            # Compare the current alert's ID with the requested ID
            #
            # int(alert_id) converts the input into an integer because
            # Gradio may provide the number in another format.
            if alert["ID"] == int(alert_id):

                # Update the alert's classification
                alert["Classification"] = classification

                # Record which ranger reviewed it
                alert["Ranger"] = ranger_name

                # Stop searching once the correct alert is found
                break

    def get_dataframe(self):
        """
        Converts the stored alerts into a pandas DataFrame.

        A DataFrame is a table-like data structure that Gradio can display.
        """

        # If there are no alerts, return an empty table with the correct columns
        if not self.alerts:
            return pd.DataFrame(columns=[
                "ID",
                "Timestamp",
                "Sensor ID",
                "Latitude",
                "Longitude",
                "Noise Type",
                "dB Strength",
                "Confidence",
                "Classification",
                "Ranger"
            ])

        # Convert the list of dictionaries into a table
        return pd.DataFrame(self.alerts)


# Create one shared alert store for the entire application
store = SimpleAlertStore()


# -----------------------------
# Audio analysis
# -----------------------------

def analyze_audio_clip(audio_file_path):
    """
    Sends an audio file to BirdNET for analysis.

    Parameters:
        audio_file_path:
            The path to the uploaded or recorded audio file.

    Returns:
        A tuple containing:

        1. Whether a high-confidence detection was found.
        2. The highest confidence score found.
        3. A list of detections that passed the confidence threshold.
    """

    # Create the output folder if it does not already exist
    os.makedirs(ParkConfig.OUTPUT_TEMP_DIR, exist_ok=True)

    # Find old BirdNET result files from previous analyses
    old_files = (
        glob.glob(os.path.join(ParkConfig.OUTPUT_TEMP_DIR, "*.txt"))
        + glob.glob(os.path.join(ParkConfig.OUTPUT_TEMP_DIR, "*.csv"))
    )

    # Delete old result files so that we only read the newest analysis
    for f in old_files:
        try:
            os.remove(f)
        except OSError:
            # Ignore the file if it cannot be removed
            pass

    try:
        # Run BirdNET as an external command.
        #
        # --classifier tells BirdNET to use the custom mountain lion model.
        # --output tells BirdNET where to save its results.
        # --min_conf 0.10 allows BirdNET to save results with at least 10%
        # confidence. The program later applies the stricter 40% threshold.
        subprocess.run(
            [
                "birdnet-analyze",
                "--classifier",
                ParkConfig.CUSTOM_MODEL_PATH,
                "--output",
                ParkConfig.OUTPUT_TEMP_DIR,
                "--min_conf",
                "0.10",
                audio_file_path
            ],

            # If BirdNET fails, Python raises an error
            check=True,

            # Hide BirdNET's normal terminal output
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Find the result files created by BirdNET
        result_files = (
            glob.glob(os.path.join(ParkConfig.OUTPUT_TEMP_DIR, "*.txt"))
            + glob.glob(os.path.join(ParkConfig.OUTPUT_TEMP_DIR, "*.csv"))
        )

        # If BirdNET did not create a result file, return an empty result
        if not result_files:
            return False, 0.0, []

        # This list will contain only detections meeting the required threshold
        high_confidence_matches = []

        # Track the highest confidence score found in the entire result file
        max_confidence = 0.0

        # Open the first result file created by BirdNET
        with open(result_files[0], "r") as f:

            # BirdNET commonly saves tab-separated values.
            # DictReader lets us access each value using its column name.
            reader = csv.DictReader(f, delimiter="\t")

            # Read each detection returned by BirdNET
            for row in reader:

                # Read the confidence value and convert it from text to a number
                conf = float(row.get("Confidence", 0))

                # Use the common name when available.
                # If it is missing, use the scientific name.
                # If both are missing, use "Mountain Lion".
                species = (
                    row.get("Common Name", "")
                    or row.get("Scientific Name", "")
                    or "Mountain Lion"
                )

                # Keep track of the strongest detection
                if conf > max_confidence:
                    max_confidence = conf

                # Only keep detections that meet the required confidence level
                if conf >= ParkConfig.CONFIDENCE_THRESHOLD:

                    # Read the beginning and ending time of the detection
                    start = row.get("Start (s)", "N/A")
                    end = row.get("End (s)", "N/A")

                    # Save the important information about this detection
                    high_confidence_matches.append({
                        "start": start,
                        "end": end,
                        "confidence": conf,
                        "species": species
                    })

        # A detection exists if at least one result passed the threshold
        is_detected = len(high_confidence_matches) > 0

        # Return the results to the calling function
        return is_detected, max_confidence, high_confidence_matches

    except Exception as e:
        # Print the error in the terminal for troubleshooting
        print(f"Detection Engine Error: {e}")

        # Return a safe "no detection" result if something goes wrong
        return False, 0.0, []


# -----------------------------
# Transmission processing
# -----------------------------

def process_transmission(audio_path, sensor_id, lat, lon):
    """
    Processes an uploaded audio recording.

    This function:
        1. Checks whether an audio file was provided.
        2. Sends the file to the detection model.
        3. Creates an alert if a high-confidence detection is found.
        4. Updates the dashboard table.
    """

    # Make sure the user selected an audio file
    if not audio_path:
        return "Please select an audio file.", store.get_dataframe(), None

    # Analyze the recording using BirdNET
    detected, conf, matches = analyze_audio_clip(audio_path)

    # If at least one detection passed the confidence threshold...
    if detected:

        # Use the species name from the first detection
        species_label = (
            matches[0]["species"]
            if matches
            else "Mountain Lion"
        )

        # Add the detection to the alert store
        #
        # The current code uses 78.5 as the sound strength.
        # In a complete system, this value could come from the sensor.
        store.add_alert(
            sensor_id,
            float(lat),
            float(lon),
            species_label,
            78.5,
            conf
        )

        # Create the message shown at the top of the dashboard
        status_msg = (
            f"ALARM TRIGGERED: Mountain Lion Detected at "
            f"{sensor_id} ({conf:.2%} Confidence)!"
        )

        # Return the status message and updated alert table
        return status_msg, store.get_dataframe()

    else:
        # Show this message when no detection meets the threshold
        return (
            "System Clear: No Mountain Lion signature detected.",
            store.get_dataframe()
        )


# -----------------------------
# Ranger classification
# -----------------------------

def classify_selected_alert(alert_id, classification, ranger_name):
    """
    Assigns a classification to an alert.

    Parameters:
        alert_id:
            The ID of the alert selected by the user.

        classification:
            The ranger's decision.

        ranger_name:
            The ranger making the decision.
    """

    # Make sure the user entered an alert ID
    if not alert_id:
        return "Please enter a valid Alert ID.", store.get_dataframe()

    # Update the selected alert in the alert store
    store.update_classification(
        alert_id,
        classification,
        ranger_name
    )

    # Return a confirmation message and the updated table
    return (
        f"Alert #{alert_id} successfully classified as "
        f"'{classification}' by {ranger_name}.",
        store.get_dataframe()
    )


# -----------------------------
# Report generation
# -----------------------------

def generate_report_5a():
    """
    Creates a report grouped by timestamp and classification.
    """

    # Get all stored alerts as a DataFrame
    df = store.get_dataframe()

    # If there are no alerts, tell the user
    if df.empty:
        return "No alert records available."

    # Group alerts by timestamp and classification.
    # size() counts how many records are in each group.
    return (
        df.groupby(["Timestamp", "Classification"])
        .size()
        .reset_index(name="Detections Count")
        .to_string(index=False)
    )


def generate_report_5b():
    """
    Creates a report showing the number of detections at each sensor location.
    """

    # Get all stored alerts
    df = store.get_dataframe()

    # If there are no alerts, tell the user
    if df.empty:
        return "No alert records available."

    # Group alerts by sensor ID and geographical location
    return (
        df.groupby(["Sensor ID", "Latitude", "Longitude"])
        .size()
        .reset_index(name="Total Detections")
        .to_string(index=False)
    )


def generate_report_5d():
    """
    Creates a report showing how many alerts each ranger classified.
    """

    # Get all stored alerts
    df = store.get_dataframe()

    # If there are no alerts, tell the user
    if df.empty:
        return "No alert records available."

    # Group alerts by ranger and classification
    return (
        df.groupby(["Ranger", "Classification"])
        .size()
        .reset_index(name="Classified Count")
        .to_string(index=False)
    )


# -----------------------------
# Gradio user interface
# -----------------------------

# Create the main Gradio application.
# The title appears in the browser tab.
with gr.Blocks(
    title=f"Ranger Platform - {ParkConfig.PARK_NAME}"
) as app:

    # Add the main heading to the page
    gr.Markdown(
        f"# Ranger Control Platform - {ParkConfig.PARK_NAME}"
    )

    # Create tabs so the application can have separate sections
    with gr.Tabs():

        # =============================
        # Live Dashboard tab
        # =============================

        with gr.Tab("Live Dashboard"):

            # Displays system messages and alarm notifications
            status_banner = gr.Textbox(
                label="System Status / Alarm Banner",
                value="System Operational - Monitoring Active",
                interactive=False
            )

            # Place two columns side by side
            with gr.Row():

                # -----------------------------
                # Left column: audio processing
                # -----------------------------

                with gr.Column(scale=1):

                    gr.Markdown("Process Transmission")

                    # Allows the user to upload an audio file or record one
                    # from a microphone.
                    #
                    # type="filepath" means Gradio passes the file path
                    # to the Python function.
                    audio_input = gr.Audio(
                        sources=["upload", "microphone"],
                        type="filepath",
                        label="Sensor Transmission Clip"
                    )

                    # Text field for identifying the sensor
                    sensor_input = gr.Textbox(
                        value="SENSOR-01",
                        label="Sensor ID"
                    )

                    # Input for the sensor's latitude
                    lat_input = gr.Number(
                        value=32.7180,
                        label="Latitude"
                    )

                    # Input for the sensor's longitude
                    lon_input = gr.Number(
                        value=-117.1630,
                        label="Longitude"
                    )

                    # Button that starts audio analysis
                    btn_run = gr.Button(
                        "Analyze Clip",
                        variant="primary"
                    )

                # -----------------------------
                # Right column: alert table
                # -----------------------------

                with gr.Column(scale=2):

                    gr.Markdown("Active Detections Log")

                    # Displays all alerts currently stored in memory
                    alerts_table = gr.Dataframe(
                        value=store.get_dataframe(),
                        interactive=False
                    )

            # Add a horizontal divider between dashboard sections
            gr.Markdown("---")

            # Section for ranger review
            gr.Markdown("Ranger Classification Triage")

            # Put ranger classification controls in one row
            with gr.Row():

                # Input for the alert number the ranger wants to review
                alert_id_input = gr.Number(
                    label="Alert ID to Classify",
                    precision=0
                )

                # Input for the ranger's name
                ranger_name_input = gr.Textbox(
                    value="Ranger Smith",
                    label="Ranger Name"
                )

                # Buttons for the possible classifications
                btn_def = gr.Button(
                    "Definite",
                    variant="stop"
                )

                btn_sus = gr.Button("Suspected")
                btn_fal = gr.Button("False Alarm")

            # Displays the result of the ranger's classification action
            triage_status = gr.Textbox(
                label="Triage Action Result",
                interactive=False
            )

            # When the Analyze Clip button is clicked:
            #
            # 1. Read the audio, sensor ID, latitude, and longitude.
            # 2. Send them to process_transmission().
            # 3. Update the status banner and alert table.
            btn_run.click(
                process_transmission,
                inputs=[
                    audio_input,
                    sensor_input,
                    lat_input,
                    lon_input
                ],
                outputs=[
                    status_banner,
                    alerts_table
                ]
            )

            # When the Definite button is clicked, classify the alert
            # as a definite detection.
            btn_def.click(
                lambda aid, rname:
                    classify_selected_alert(
                        aid,
                        "Definite",
                        rname
                    ),
                inputs=[
                    alert_id_input,
                    ranger_name_input
                ],
                outputs=[
                    triage_status,
                    alerts_table
                ]
            )

            # When the Suspected button is clicked, classify the alert
            # as suspected.
            btn_sus.click(
                lambda aid, rname:
                    classify_selected_alert(
                        aid,
                        "Suspected",
                        rname
                    ),
                inputs=[
                    alert_id_input,
                    ranger_name_input
                ],
                outputs=[
                    triage_status,
                    alerts_table
                ]
            )

            # When the False Alarm button is clicked, classify the alert
            # as false.
            btn_fal.click(
                lambda aid, rname:
                    classify_selected_alert(
                        aid,
                        "False",
                        rname
                    ),
                inputs=[
                    alert_id_input,
                    ranger_name_input
                ],
                outputs=[
                    triage_status,
                    alerts_table
                ]
            )

        # =============================
        # Reports tab
        # =============================

        with gr.Tab("Reports"):

            # Heading for the reporting section
            gr.Markdown("System Reports")

            # Put report buttons in one row
            with gr.Row():

                # Creates a report grouped by date and classification
                btn_r5a = gr.Button(
                    "Report by Date & Classification"
                )

                # Creates a report grouped by sensor location
                btn_r5b = gr.Button(
                    "Report by Sensor Location"
                )

                # Creates a report grouped by ranger and classification
                btn_r5d = gr.Button(
                    "Report by Ranger"
                )

            # Area where the generated report text will appear
            report_output = gr.Textbox(
                label="Generated Report Output",
                lines=10,
                interactive=False
            )

            # Connect each report button to its report function
            btn_r5a.click(
                generate_report_5a,
                outputs=report_output
            )

            btn_r5b.click(
                generate_report_5b,
                outputs=report_output
            )

            btn_r5d.click(
                generate_report_5d,
                outputs=report_output
            )


# -----------------------------
# Start the application
# -----------------------------

# This condition ensures that the application starts only when this
# file is run directly, not when it is imported by another Python file.
if __name__ == "__main__":

    # Launch the Gradio application.
    #
    # inbrowser=True automatically opens the application in a browser window.
    app.launch(inbrowser=True)