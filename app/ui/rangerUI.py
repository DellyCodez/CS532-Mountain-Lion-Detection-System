"""
Gradio user interface for the Mountain Lion Detection System.
"""

from __future__ import annotations

from typing import Any
from app.audio.levelMeter import AudioLevelMeter
import gradio as gr
import pandas as pd

from app.alerts.alertService import (
    AlertService,
    AlertServiceError,
)
from app.audio.ingestion import (
    AudioIngestionError,
    AudioIngestionService,
    AudioRecording,
)
from app.audio.preprocessing import (
    AudioPreprocessingError,
    AudioPreprocessingService,
    PreprocessedAudio,
)
from app.models.baseClassifier import (
    BaseClassifier,
    ClassifierError,
)


class RangerUI:
    """Build and run the Ranger Gradio application."""

    ALERT_COLUMNS = [
        "alert_id",
        "timestamp",
        "sensor_id",
        "latitude",
        "longitude",
        "noise_type",
        "confidence",
        "db_strength",
        "classification",
        "ranger_name",
    ]

    DETECTION_COLUMNS = [
        "label",
        "confidence",
        "start_seconds",
        "end_seconds",
    ]

    def __init__(
        self,
        alert_service: AlertService,
        ingestion_service: AudioIngestionService,
        preprocessing_service: AudioPreprocessingService,
        classifier: BaseClassifier,
        *,
        park_name: str = "San Diego County Parks",
        confidence_threshold: float = 0.40,
    ) -> None:
        self.alert_service = alert_service
        self.ingestion_service = ingestion_service
        self.preprocessing_service = preprocessing_service
        self.classifier = classifier
        self.park_name = park_name
        self.confidence_threshold = confidence_threshold

        self.app = self.build()

    def build(self) -> gr.Blocks:
        """Build and return the Gradio application."""

        with gr.Blocks(
            title=f"Ranger Platform - {self.park_name}"
        ) as app:
            gr.Markdown(
                f"# Ranger Control Platform - "
                f"{self.park_name}"
            )

            with gr.Tabs():
                with gr.Tab("Live Dashboard"):
                    status_banner = gr.Textbox(
                        label="System Status",
                        value=(
                            "System operational - "
                            "monitoring active"
                        ),
                        interactive=False,
                        lines=2,
                    )

                    with gr.Row():
                        with gr.Column(scale=1):
                            gr.Markdown(
                                "### Process Audio Transmission"
                            )

                            audio_input = gr.Audio(
                                sources=[
                                    "upload",
                                    "microphone",
                                ],
                                type="filepath",
                                label="Audio Recording",
                            )

                            audio_source = gr.Radio(
                                choices=[
                                    "upload",
                                    "microphone",
                                    "sensor",
                                ],
                                value="upload",
                                label="Audio Source",
                            )

                            sensor_input = gr.Textbox(
                                value="SENSOR-01",
                                label="Sensor ID",
                            )

                            with gr.Row():
                                latitude_input = gr.Number(
                                    value=32.7180,
                                    label="Latitude",
                                )

                                longitude_input = gr.Number(
                                    value=-117.1630,
                                    label="Longitude",
                                )

                            db_strength_input = gr.Number(
                                value=None,
                                label="Sound Strength dB",
                                info=(
                                    "Leave blank when the source "
                                    "does not provide dB data."
                                ),
                            )

                            analyze_button = gr.Button(
                                "Analyze Audio",
                                variant="primary",
                            )

                        with gr.Column(scale=2):
                            gr.Markdown(
                                "### Model Detections"
                            )

                            detections_table = gr.Dataframe(
                                headers=self.DETECTION_COLUMNS,
                                datatype=[
                                    "str",
                                    "number",
                                    "number",
                                    "number",
                                ],
                                interactive=False,
                                value=self._empty_detections(),
                            )

                            gr.Markdown(
                                "### Alert Log"
                            )

                            alerts_table = gr.Dataframe(
                                headers=self.ALERT_COLUMNS,
                                interactive=False,
                                value=self._alerts_dataframe(),
                            )

                    gr.Markdown(
                        "### Ranger Classification"
                    )

                    with gr.Row():
                        alert_id_input = gr.Textbox(
                            label="Alert ID",
                            placeholder=(
                                "Paste the alert ID here"
                            ),
                        )

                        ranger_name_input = gr.Textbox(
                            value="Ranger Smith",
                            label="Ranger Name",
                        )

                        classification_input = gr.Dropdown(
                            choices=[
                                "Definite",
                                "Suspected",
                                "False",
                            ],
                            label=(
                                "Classification "
                                "(False = False Alarm)"
                            ),
                            value="Suspected",
                        )

                        classify_button = gr.Button(
                            "Save Classification"
                        )

                    triage_status = gr.Textbox(
                        label="Classification Status",
                        interactive=False,
                    )

                    analyze_button.click(
                        fn=self.process_audio,
                        inputs=[
                            audio_input,
                            audio_source,
                            sensor_input,
                            latitude_input,
                            longitude_input,
                            db_strength_input,
                        ],
                        outputs=[
                            status_banner,
                            detections_table,
                            alerts_table,
                        ],
                    )

                    classify_button.click(
                        fn=self.classify_alert,
                        inputs=[
                            alert_id_input,
                            classification_input,
                            ranger_name_input,
                        ],
                        outputs=[
                            triage_status,
                            alerts_table,
                        ],
                    )

                with gr.Tab("Reports"):
                    gr.Markdown("### System Reports")

                    with gr.Row():
                        date_report_button = gr.Button(
                            "Report by Date and Classification"
                        )

                        location_report_button = gr.Button(
                            "Report by Sensor Location"
                        )

                        ranger_report_button = gr.Button(
                            "Report by Ranger"
                        )

                    report_output = gr.Textbox(
                        label="Generated Report",
                        lines=15,
                        interactive=False,
                    )

                    date_report_button.click(
                        fn=self.generate_date_report,
                        outputs=report_output,
                    )

                    location_report_button.click(
                        fn=self.generate_location_report,
                        outputs=report_output,
                    )

                    ranger_report_button.click(
                        fn=self.generate_ranger_report,
                        outputs=report_output,
                    )

                with gr.Tab("Settings"):
                    gr.Markdown("### System Settings")

                    database_mode = gr.Radio(
                        choices=[
                            "Local SQLite",
                            "Firebase Cloud",
                        ],
                        value="Local SQLite",
                        label="Database Mode",
                    )

                    database_status = gr.Textbox(
                        label="Database Configuration Status",
                        value=(
                            "The storage backend will be connected "
                            "after the SQLite and Firebase stores "
                            "are implemented."
                        ),
                        interactive=False,
                        lines=3,
                    )

                    database_mode.change(
                        fn=self.database_mode_message,
                        inputs=database_mode,
                        outputs=database_status,
                    )

                    gr.Markdown(
                        f"Model: {self.classifier.model_name}\n\n"
                        f"Alert threshold: "
                        f"{self.confidence_threshold:.0%}"
                    )

        return app

    def launch(
        self,
        *,
        server_name: str | None = None,
        server_port: int | None = None,
        share: bool = False,
    ) -> None:
        """Launch the Ranger UI."""

        launch_kwargs: dict[str, Any] = {
            "share": share,
        }

        if server_name is not None:
            launch_kwargs["server_name"] = server_name

        if server_port is not None:
            launch_kwargs["server_port"] = server_port

        self.app.launch(**launch_kwargs)

    def process_audio(
        self,
        audio_path: str | None,
        audio_source: str,
        sensor_id: str,
        latitude: float,
        longitude: float,
        db_strength: float | None,
    ) -> tuple[str, pd.DataFrame, pd.DataFrame]:
        """
        Ingest, preprocess, classify, and create an alert
        when the confidence threshold is reached.
        """

        if not audio_path:
            return (
                "Please upload or record an audio file first.",
                self._empty_detections(),
                self._alerts_dataframe(),
            )

        recording: AudioRecording | None = None
        processed_audio: PreprocessedAudio | None = None

        try:
            recording = self.ingestion_service.ingest(
                audio_path,
                source=audio_source,
                sensor_id=sensor_id,
            )

            processed_audio = (
                self.preprocessing_service.preprocess(
                    recording
                )
            )

            result = self.classifier.analyze(
                processed_audio
            )

            detections = result.detections_above(
                self.confidence_threshold
            )

            detections_table = (
                self._detections_dataframe(detections)
            )

            if not detections:
                return (
                    "System clear - no detection met the "
                    f"{self.confidence_threshold:.0%} "
                    "alert threshold.",
                    detections_table,
                    self._alerts_dataframe(),
                )

            best_detection = max(
                detections,
                key=lambda detection: detection.confidence,
            )

            alert = self.alert_service.create_alert(
                sensor_id=sensor_id,
                latitude=latitude,
                longitude=longitude,
                noise_type=best_detection.label,
                confidence=best_detection.confidence,
                db_strength=db_strength,
                source=audio_source,
                metadata={
                    "recording_id": recording.recording_id,
                    "original_filename": (
                        recording.original_filename
                    ),
                },
            )

            if alert is None:
                return (
                    "System clear - no alert was created.",
                    detections_table,
                    self._alerts_dataframe(),
                )

            status = (
                "ALARM TRIGGERED - "
                f"{best_detection.label} detected at "
                f"{sensor_id} with "
                f"{best_detection.confidence:.2%} "
                "confidence."
            )

            return (
                status,
                detections_table,
                self._alerts_dataframe(),
            )

        except (
            AudioIngestionError,
            AudioPreprocessingError,
            ClassifierError,
            AlertServiceError,
            TypeError,
            ValueError,
        ) as error:
            return (
                f"Unable to process audio: {error}",
                self._empty_detections(),
                self._alerts_dataframe(),
            )

        finally:
            if processed_audio is not None:
                self.preprocessing_service.delete_processed_audio(
                    processed_audio
                )

            if recording is not None:
                self.ingestion_service.delete_recording(
                    recording
                )

    def classify_alert(
        self,
        alert_id: str,
        classification: str,
        ranger_name: str,
    ) -> tuple[str, pd.DataFrame]:
        """Save a ranger classification."""

        try:
            updated_alert = self.alert_service.classify_alert(
                alert_id=alert_id,
                classification=classification,
                ranger_name=ranger_name,
            )

            return (
                "Alert successfully classified as "
                f"'{updated_alert['classification']}' by "
                f"{updated_alert['ranger_name']}.",
                self._alerts_dataframe(),
            )

        except AlertServiceError as error:
            return (
                f"Unable to classify alert: {error}",
                self._alerts_dataframe(),
            )

    def generate_date_report(self) -> str:
        """Generate a date and classification report."""

        dataframe = self._alerts_dataframe()

        if dataframe.empty:
            return "No alert records available."

        return (
            dataframe.groupby(
                [
                    "timestamp",
                    "classification",
                ],
                dropna=False,
            )
            .size()
            .reset_index(name="detection_count")
            .to_string(index=False)
        )

    def generate_location_report(self) -> str:
        """Generate a sensor-location report."""

        dataframe = self._alerts_dataframe()

        if dataframe.empty:
            return "No alert records available."

        return (
            dataframe.groupby(
                [
                    "sensor_id",
                    "latitude",
                    "longitude",
                ],
                dropna=False,
            )
            .size()
            .reset_index(name="detection_count")
            .to_string(index=False)
        )

    def generate_ranger_report(self) -> str:
        """Generate a ranger classification report."""

        dataframe = self._alerts_dataframe()

        if dataframe.empty:
            return "No alert records available."

        return (
            dataframe.groupby(
                [
                    "ranger_name",
                    "classification",
                ],
                dropna=False,
            )
            .size()
            .reset_index(name="classified_count")
            .to_string(index=False)
        )

    @staticmethod
    def database_mode_message(
        database_mode: str,
    ) -> str:
        """Show the currently selected database mode."""

        return (
            f"Selected mode: {database_mode}. "
            "The storage factory will connect this setting "
            "to the active database backend."
        )

    def _alerts_dataframe(self) -> pd.DataFrame:
        """Load alerts and convert them into a table."""

        alerts = self.alert_service.list_alerts()

        if not alerts:
            return pd.DataFrame(
                columns=self.ALERT_COLUMNS
            )

        dataframe = pd.DataFrame(alerts)

        for column in self.ALERT_COLUMNS:
            if column not in dataframe.columns:
                dataframe[column] = None

        return dataframe[self.ALERT_COLUMNS]

    @classmethod
    def _detections_dataframe(
        cls,
        detections: tuple[Any, ...],
    ) -> pd.DataFrame:
        """Convert detections into a table."""

        if not detections:
            return cls._empty_detections()

        return pd.DataFrame(
            [
                {
                    "label": detection.label,
                    "confidence": detection.confidence,
                    "start_seconds": (
                        detection.start_seconds
                    ),
                    "end_seconds": (
                        detection.end_seconds
                    ),
                }
                for detection in detections
            ],
            columns=cls.DETECTION_COLUMNS,
        )

    @classmethod
    def _empty_detections(cls) -> pd.DataFrame:
        """Return an empty detections table."""

        return pd.DataFrame(
            columns=cls.DETECTION_COLUMNS
        )