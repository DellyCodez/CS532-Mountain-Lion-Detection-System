"""
Application startup and temporary development repository.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Mapping

from app.alerts.alertService import (
    AlertRepository,
    AlertService,
)
from app.audio.ingestion import AudioIngestionService
from app.audio.preprocessing import AudioPreprocessingService
from app.config import AppConfig
from app.models.BirdNetClassifier import BirdNetClassifier
from app.ui.rangerUI import RangerUI


class InMemoryAlertRepository:
    """
    Temporary repository used until SQLite and Firebase are implemented.

    This allows the application to run during development.
    It will later be replaced by the storage factory.
    """

    def __init__(self) -> None:
        self._alerts: dict[str, dict[str, Any]] = {}

    def create_alert(
        self,
        alert: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        alert_copy = deepcopy(dict(alert))
        alert_id = str(alert_copy["alert_id"])

        self._alerts[alert_id] = alert_copy

        return deepcopy(alert_copy)

    def get_alert(
        self,
        alert_id: str,
    ) -> Mapping[str, Any] | None:
        alert = self._alerts.get(alert_id)

        if alert is None:
            return None

        return deepcopy(alert)

    def update_alert(
        self,
        alert_id: str,
        updates: Mapping[str, Any],
    ) -> Mapping[str, Any] | None:
        if alert_id not in self._alerts:
            return None

        self._alerts[alert_id].update(
            deepcopy(dict(updates))
        )

        return deepcopy(
            self._alerts[alert_id]
        )

    def list_alerts(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[Mapping[str, Any]]:
        results: list[Mapping[str, Any]] = []

        for alert in self._alerts.values():
            timestamp = self._parse_timestamp(
                alert.get("timestamp")
            )

            if start_time is not None:
                if timestamp is None or timestamp < start_time:
                    continue

            if end_time is not None:
                if timestamp is None or timestamp > end_time:
                    continue

            results.append(deepcopy(alert))

        return sorted(
            results,
            key=lambda alert: str(
                alert.get("timestamp", "")
            ),
            reverse=True,
        )

    @staticmethod
    def _parse_timestamp(
        value: Any,
    ) -> datetime | None:
        if isinstance(value, datetime):
            return value

        if not isinstance(value, str):
            return None

        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None


def build_application(
    config: AppConfig | None = None,
) -> RangerUI:
    """Build the Ranger application and its services."""

    config = config or AppConfig.from_environment()
    config.ensure_runtime_directories()

    # Temporary in-memory backend.
    # This will later be replaced with the storage factory.
    repository: AlertRepository = (
        InMemoryAlertRepository()
    )

    alert_service = AlertService(
        repository=repository,
        confidence_threshold=(
            config.model.alert_confidence_threshold
        ),
    )

    ingestion_service = AudioIngestionService(
        storage_directory=(
            config.audio.ingestion_directory
        ),
        max_file_size_mb=(
            config.audio.max_file_size_mb
        ),
    )

    preprocessing_service = (
        AudioPreprocessingService(
            output_directory=(
                config.audio.preprocessing_directory
            ),
            target_sample_rate=(
                config.audio.target_sample_rate
            ),
            max_duration_seconds=(
                config.audio.max_duration_seconds
            ),
        )
    )

    classifier = BirdNetClassifier(
        model_path=config.model.model_path,
        birdnet_command=config.model.birdnet_command,
        minimum_model_confidence=(
            config.model.minimum_model_confidence
        ),
    )

    return RangerUI(
        alert_service=alert_service,
        ingestion_service=ingestion_service,
        preprocessing_service=(
            preprocessing_service
        ),
        classifier=classifier,
        park_name=config.park.name,
        confidence_threshold=(
            config.model.alert_confidence_threshold
        ),
    )


def run() -> None:
    """Load configuration and launch the Ranger UI."""

    config = AppConfig.from_environment()

    ranger_ui = build_application(config)

    ranger_ui.launch(
        server_name=config.ui.server_name,
        server_port=config.ui.server_port,
        share=config.ui.share,
    )


if __name__ == "__main__":
    run()