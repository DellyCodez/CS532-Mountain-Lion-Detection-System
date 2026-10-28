"""
Report generation for ranger alert records.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

from app.alerts.alertService import AlertService


class ReportService:
    """Generate tabular and map-ready reports from alerts."""

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

    def __init__(
        self,
        alert_service: AlertService,
    ) -> None:
        self.alert_service = alert_service

    def alerts_dataframe(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> pd.DataFrame:
        """Return alerts with consistent columns."""

        alerts = self.alert_service.list_alerts(
            start_time=start_time,
            end_time=end_time,
        )

        if not alerts:
            return pd.DataFrame(
                columns=self.ALERT_COLUMNS
            )

        dataframe = pd.DataFrame(alerts)

        for column in self.ALERT_COLUMNS:
            if column not in dataframe.columns:
                dataframe[column] = None

        return dataframe[self.ALERT_COLUMNS]

    def by_date_and_classification(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> pd.DataFrame:
        """Group detections by date and classification."""

        dataframe = self.alerts_dataframe(
            start_time=start_time,
            end_time=end_time,
        )

        if dataframe.empty:
            return pd.DataFrame(
                columns=[
                    "date",
                    "classification",
                    "detection_count",
                ]
            )

        dataframe["date"] = pd.to_datetime(
            dataframe["timestamp"],
            errors="coerce",
        ).dt.date

        return (
            dataframe.groupby(
                ["date", "classification"],
                dropna=False,
            )
            .size()
            .reset_index(name="detection_count")
            .sort_values("date")
        )

    def by_sensor_location(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> pd.DataFrame:
        """Group detections by sensor and GPS coordinates."""

        dataframe = self.alerts_dataframe(
            start_time=start_time,
            end_time=end_time,
        )

        if dataframe.empty:
            return pd.DataFrame(
                columns=[
                    "sensor_id",
                    "latitude",
                    "longitude",
                    "detection_count",
                ]
            )

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
        )

    def by_ranger(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> pd.DataFrame:
        """Group reviewed alerts by ranger and classification."""

        dataframe = self.alerts_dataframe(
            start_time=start_time,
            end_time=end_time,
        )

        if dataframe.empty:
            return pd.DataFrame(
                columns=[
                    "ranger_name",
                    "classification",
                    "classified_count",
                ]
            )

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
        )

    def map_points(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
    ) -> list[dict[str, Any]]:
        """Return detections in a format suitable for map plotting."""

        dataframe = self.alerts_dataframe(
            start_time=start_time,
            end_time=end_time,
        )

        if dataframe.empty:
            return []

        return [
            {
                "alert_id": row["alert_id"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "noise_type": row["noise_type"],
                "confidence": row["confidence"],
                "classification": row["classification"],
                "sensor_id": row["sensor_id"],
            }
            for _, row in dataframe.iterrows()
        ]

    def date_report_text(self) -> str:
        report = self.by_date_and_classification()

        if report.empty:
            return "No alert records available."

        return report.to_string(index=False)

    def location_report_text(self) -> str:
        report = self.by_sensor_location()

        if report.empty:
            return "No alert records available."

        return report.to_string(index=False)

    def ranger_report_text(self) -> str:
        report = self.by_ranger()

        if report.empty:
            return "No alert records available."

        return report.to_string(index=False)