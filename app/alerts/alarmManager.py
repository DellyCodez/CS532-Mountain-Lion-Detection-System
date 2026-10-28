"""
Alarm state management for ranger notifications.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from math import asin, cos, radians, sin, sqrt
from typing import Any, Mapping


class AlarmManagerError(ValueError):
    """Raised when an alarm operation receives invalid data."""


@dataclass(frozen=True, slots=True)
class AlarmEvent:
    """Result of an alarm operation."""

    alarm_active: bool
    should_sound: bool
    message: str
    alert_id: str | None = None
    triggered_at: datetime | None = None
    acknowledged_at: datetime | None = None


class AlarmManager:
    """Manage alarm state independently from alert storage."""

    def __init__(
        self,
        *,
        minimum_separation_meters: float = 3.0,
    ) -> None:
        if minimum_separation_meters < 0:
            raise AlarmManagerError(
                "minimum_separation_meters cannot be negative"
            )

        self.minimum_separation_meters = (
            minimum_separation_meters
        )

        self._active = False
        self._active_alert_id: str | None = None
        self._active_triggered_at: datetime | None = None
        self._active_location: tuple[float, float] | None = None
        self._last_acknowledged_location: (
            tuple[float, float] | None
        ) = None

    @property
    def is_active(self) -> bool:
        return self._active

    def trigger(
        self,
        alert: Mapping[str, Any],
    ) -> AlarmEvent:
        """Process an alert and determine whether the alarm should sound."""

        alert_id = self._required_text(
            alert.get("alert_id"),
            "alert_id",
        )

        location = self._location_from_alert(alert)
        now = datetime.now(timezone.utc)

        if self._active:
            return AlarmEvent(
                alarm_active=True,
                should_sound=False,
                message=(
                    "Alarm is already active. Ranger acknowledgement "
                    "is required before it can be silenced."
                ),
                alert_id=alert_id,
                triggered_at=self._active_triggered_at,
            )

        if self._last_acknowledged_location is not None:
            distance = self._distance_meters(
                self._last_acknowledged_location,
                location,
            )

            if distance < self.minimum_separation_meters:
                return AlarmEvent(
                    alarm_active=False,
                    should_sound=False,
                    message=(
                        "Alert is at the previously acknowledged "
                        "location. A different location is required "
                        "to reactivate the alarm."
                    ),
                    alert_id=alert_id,
                    acknowledged_at=now,
                )

        self._active = True
        self._active_alert_id = alert_id
        self._active_triggered_at = now
        self._active_location = location

        return AlarmEvent(
            alarm_active=True,
            should_sound=True,
            message=(
                "ALARM TRIGGERED. Ranger acknowledgement is required."
            ),
            alert_id=alert_id,
            triggered_at=now,
        )

    def acknowledge(self) -> AlarmEvent:
        """Silence the alarm until a different location triggers it."""

        if not self._active:
            return AlarmEvent(
                alarm_active=False,
                should_sound=False,
                message="No active alarm needs acknowledgement.",
                alert_id=self._active_alert_id,
            )

        acknowledged_at = datetime.now(timezone.utc)

        self._active = False
        self._last_acknowledged_location = (
            self._active_location
        )

        return AlarmEvent(
            alarm_active=False,
            should_sound=False,
            message=(
                "Alarm acknowledged and silenced. A new alert at "
                "a different location can trigger it again."
            ),
            alert_id=self._active_alert_id,
            triggered_at=self._active_triggered_at,
            acknowledged_at=acknowledged_at,
        )

    def reset(self) -> None:
        """Reset state for a new monitoring session."""

        self._active = False
        self._active_alert_id = None
        self._active_triggered_at = None
        self._active_location = None
        self._last_acknowledged_location = None

    @staticmethod
    def _required_text(
        value: Any,
        field_name: str,
    ) -> str:
        if value is None or not str(value).strip():
            raise AlarmManagerError(
                f"{field_name} is required"
            )

        return str(value).strip()

    @staticmethod
    def _location_from_alert(
        alert: Mapping[str, Any],
    ) -> tuple[float, float]:
        try:
            latitude = float(alert["latitude"])
            longitude = float(alert["longitude"])
        except (KeyError, TypeError, ValueError) as error:
            raise AlarmManagerError(
                "Alert must contain valid latitude and longitude"
            ) from error

        if not -90 <= latitude <= 90:
            raise AlarmManagerError(
                "latitude must be between -90 and 90"
            )

        if not -180 <= longitude <= 180:
            raise AlarmManagerError(
                "longitude must be between -180 and 180"
            )

        return latitude, longitude

    @staticmethod
    def _distance_meters(
        first: tuple[float, float],
        second: tuple[float, float],
    ) -> float:
        """Calculate the distance between two GPS coordinates."""

        earth_radius_meters = 6_371_000.0

        first_latitude, first_longitude = first
        second_latitude, second_longitude = second

        latitude_delta = radians(
            second_latitude - first_latitude
        )

        longitude_delta = radians(
            second_longitude - first_longitude
        )

        first_latitude = radians(first_latitude)
        second_latitude = radians(second_latitude)

        haversine = (
            sin(latitude_delta / 2) ** 2
            + cos(first_latitude)
            * cos(second_latitude)
            * sin(longitude_delta / 2) ** 2
        )

        return (
            2
            * earth_radius_meters
            * asin(sqrt(haversine))
        )