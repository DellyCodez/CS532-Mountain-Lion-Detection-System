"""
Business logic for creating, retrieving, and classifying alerts.

This service does not directly depend on SQLite or Firebase.
A storage repository is injected so both database types can use it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from math import isfinite
from typing import Any, Mapping, Protocol
from uuid import uuid4


class AlertServiceError(ValueError):
    """Raised when alert data is invalid."""


class AlertNotFoundError(AlertServiceError):
    """Raised when an alert cannot be found."""


class InvalidClassificationError(AlertServiceError):
    """Raised when an invalid ranger classification is submitted."""


class AlertRepository(Protocol):
    """
    Interface that both SQLite and Firebase storage must implement.
    """

    def create_alert(
        self,
        alert: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """Save and return a newly created alert."""
        ...

    def get_alert(
        self,
        alert_id: str,
    ) -> Mapping[str, Any] | None:
        """Return an alert by ID."""
        ...

    def update_alert(
        self,
        alert_id: str,
        updates: Mapping[str, Any],
    ) -> Mapping[str, Any] | None:
        """Update and return an alert."""
        ...

    def list_alerts(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[Mapping[str, Any]]:
        """Return stored alerts."""
        ...


@dataclass(frozen=True, slots=True)
class Alert:
    """
    Standard alert format used throughout the application.
    """

    alert_id: str
    timestamp: datetime
    sensor_id: str
    latitude: float
    longitude: float
    noise_type: str
    confidence: float
    db_strength: float | None = None
    classification: str = "Unclassified"
    ranger_name: str = "Unassigned"
    source: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the alert into a dictionary for SQLite or Firebase.
        """

        return {
            "alert_id": self.alert_id,
            "timestamp": self.timestamp.astimezone(
                timezone.utc
            ).isoformat(),
            "sensor_id": self.sensor_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "noise_type": self.noise_type,
            "confidence": self.confidence,
            "db_strength": self.db_strength,
            "classification": self.classification,
            "ranger_name": self.ranger_name,
            "source": self.source,
            "metadata": dict(self.metadata),
        }


class AlertService:
    """
    Handles alert business rules independently of the database.
    """

    VALID_CLASSIFICATIONS = {
        "Definite",
        "Suspected",
        "False",
    }

    def __init__(
        self,
        repository: AlertRepository,
        confidence_threshold: float = 0.40,
    ) -> None:
        if not 0.0 <= confidence_threshold <= 1.0:
            raise AlertServiceError(
                "confidence_threshold must be between 0.0 and 1.0"
            )

        self.repository = repository
        self.confidence_threshold = confidence_threshold

    def create_alert(
        self,
        *,
        sensor_id: str,
        latitude: float,
        longitude: float,
        noise_type: str,
        confidence: float,
        db_strength: float | None = None,
        timestamp: datetime | None = None,
        source: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> Alert | None:
        """
        Create and save an alert when confidence meets the threshold.

        Returns None when the confidence is below the threshold.
        """

        sensor_id = self._validate_text(
            sensor_id,
            "sensor_id",
        )

        noise_type = self._validate_text(
            noise_type,
            "noise_type",
        )

        latitude = self._validate_coordinate(
            latitude,
            "latitude",
            -90.0,
            90.0,
        )

        longitude = self._validate_coordinate(
            longitude,
            "longitude",
            -180.0,
            180.0,
        )

        confidence = self._validate_number(
            confidence,
            "confidence",
        )

        if not 0.0 <= confidence <= 1.0:
            raise AlertServiceError(
                "confidence must be between 0.0 and 1.0"
            )

        if confidence < self.confidence_threshold:
            return None

        if db_strength is not None:
            db_strength = self._validate_number(
                db_strength,
                "db_strength",
            )

            if db_strength < 0.0:
                raise AlertServiceError(
                    "db_strength cannot be negative"
                )

        alert_time = timestamp or datetime.now(timezone.utc)

        if alert_time.tzinfo is None:
            alert_time = alert_time.replace(
                tzinfo=timezone.utc
            )
        else:
            alert_time = alert_time.astimezone(
                timezone.utc
            )

        alert = Alert(
            alert_id=str(uuid4()),
            timestamp=alert_time,
            sensor_id=sensor_id,
            latitude=latitude,
            longitude=longitude,
            noise_type=noise_type,
            confidence=confidence,
            db_strength=db_strength,
            source=source,
            metadata=dict(metadata or {}),
        )

        self.repository.create_alert(
            alert.to_dict()
        )

        return alert

    def classify_alert(
        self,
        *,
        alert_id: str,
        classification: str,
        ranger_name: str,
    ) -> Mapping[str, Any]:
        """
        Classify an alert as Definite, Suspected, or False.
        """

        alert_id = self._validate_text(
            alert_id,
            "alert_id",
        )

        ranger_name = self._validate_text(
            ranger_name,
            "ranger_name",
        )

        classification = self._normalize_classification(
            classification
        )

        existing_alert = self.repository.get_alert(
            alert_id
        )

        if existing_alert is None:
            raise AlertNotFoundError(
                f"Alert '{alert_id}' was not found"
            )

        updates = {
            "classification": classification,
            "ranger_name": ranger_name,
            "reviewed_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }

        updated_alert = self.repository.update_alert(
            alert_id,
            updates,
        )

        if updated_alert is None:
            raise AlertNotFoundError(
                f"Alert '{alert_id}' was not found"
            )

        return updated_alert

    def get_alert(
        self,
        alert_id: str,
    ) -> Mapping[str, Any] | None:
        """
        Retrieve one alert by its ID.
        """

        alert_id = self._validate_text(
            alert_id,
            "alert_id",
        )

        return self.repository.get_alert(
            alert_id
        )

    def list_alerts(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[Mapping[str, Any]]:
        """
        Retrieve alerts, optionally within a time range.
        """

        if (
            start_time is not None
            and end_time is not None
            and start_time > end_time
        ):
            raise AlertServiceError(
                "start_time cannot be after end_time"
            )

        return self.repository.list_alerts(
            start_time=start_time,
            end_time=end_time,
        )

    @classmethod
    def _normalize_classification(
        cls,
        classification: str,
    ) -> str:
        """
        Convert UI labels into the required stored values.
        """

        classification = cls._validate_text(
            classification,
            "classification",
        )

        if classification.lower() == "false alarm":
            classification = "False"
        else:
            classification = classification.capitalize()

        if classification not in cls.VALID_CLASSIFICATIONS:
            raise InvalidClassificationError(
                "classification must be one of: "
                "Definite, Suspected, or False"
            )

        return classification

    @staticmethod
    def _validate_text(
        value: Any,
        field_name: str,
    ) -> str:
        """
        Validate a required text field.
        """

        if value is None:
            raise AlertServiceError(
                f"{field_name} is required"
            )

        value = str(value).strip()

        if not value:
            raise AlertServiceError(
                f"{field_name} is required"
            )

        return value

    @staticmethod
    def _validate_number(
        value: Any,
        field_name: str,
    ) -> float:
        """
        Convert and validate a numeric field.
        """

        try:
            number = float(value)
        except (TypeError, ValueError) as error:
            raise AlertServiceError(
                f"{field_name} must be a number"
            ) from error

        if not isfinite(number):
            raise AlertServiceError(
                f"{field_name} must be finite"
            )

        return number

    @classmethod
    def _validate_coordinate(
        cls,
        value: Any,
        field_name: str,
        minimum: float,
        maximum: float,
    ) -> float:
        """
        Validate latitude or longitude.
        """

        number = cls._validate_number(
            value,
            field_name,
        )

        if not minimum <= number <= maximum:
            raise AlertServiceError(
                f"{field_name} must be between "
                f"{minimum} and {maximum}"
            )

        return number