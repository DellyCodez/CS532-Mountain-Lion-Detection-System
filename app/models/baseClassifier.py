"""
Common interface and result types for audio classifiers.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from math import isfinite
from typing import Any, Mapping

from app.audio.preprocessing import PreprocessedAudio


class ClassifierError(ValueError):
    """Raised when classifier data is invalid."""


@dataclass(frozen=True, slots=True)
class AudioDetection:
    """One detected sound event returned by a classifier."""

    label: str
    confidence: float
    start_seconds: float | None = None
    end_seconds: float | None = None
    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        label = self.label.strip()

        if not label:
            raise ClassifierError(
                "Detection label cannot be empty"
            )

        object.__setattr__(
            self,
            "label",
            label,
        )

        if not isfinite(self.confidence):
            raise ClassifierError(
                "Detection confidence must be finite"
            )

        if not 0.0 <= self.confidence <= 1.0:
            raise ClassifierError(
                "Detection confidence must be between "
                "0.0 and 1.0"
            )

        if self.start_seconds is not None:
            self._validate_time(
                self.start_seconds,
                "start_seconds",
            )

        if self.end_seconds is not None:
            self._validate_time(
                self.end_seconds,
                "end_seconds",
            )

        if (
            self.start_seconds is not None
            and self.end_seconds is not None
            and self.end_seconds < self.start_seconds
        ):
            raise ClassifierError(
                "end_seconds cannot be before start_seconds"
            )

    def to_dict(self) -> dict[str, Any]:
        """Convert the detection into a dictionary."""

        return {
            "label": self.label,
            "confidence": self.confidence,
            "start_seconds": self.start_seconds,
            "end_seconds": self.end_seconds,
            "metadata": dict(self.metadata),
        }

    @staticmethod
    def _validate_time(
        value: float,
        field_name: str,
    ) -> None:
        if not isfinite(value):
            raise ClassifierError(
                f"{field_name} must be finite"
            )

        if value < 0.0:
            raise ClassifierError(
                f"{field_name} cannot be negative"
            )


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    """Complete result returned after analyzing audio."""

    model_name: str
    processed_audio: PreprocessedAudio
    detections: tuple[AudioDetection, ...]
    analyzed_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: Mapping[str, Any] = field(
        default_factory=dict
    )

    @property
    def best_detection(self) -> AudioDetection | None:
        """Return the highest-confidence detection."""

        if not self.detections:
            return None

        return max(
            self.detections,
            key=lambda detection: detection.confidence,
        )

    def detections_above(
        self,
        threshold: float,
    ) -> tuple[AudioDetection, ...]:
        """Return detections at or above a threshold."""

        if not 0.0 <= threshold <= 1.0:
            raise ClassifierError(
                "threshold must be between 0.0 and 1.0"
            )

        return tuple(
            detection
            for detection in self.detections
            if detection.confidence >= threshold
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert the classification result into a dictionary."""

        best_detection = self.best_detection

        return {
            "model_name": self.model_name,
            "recording_id": (
                self.processed_audio.recording_id
            ),
            "processed_audio": (
                self.processed_audio.to_dict()
            ),
            "detections": [
                detection.to_dict()
                for detection in self.detections
            ],
            "best_detection": (
                best_detection.to_dict()
                if best_detection is not None
                else None
            ),
            "analyzed_at": self.analyzed_at.astimezone(
                timezone.utc
            ).isoformat(),
            "metadata": dict(self.metadata),
        }


class BaseClassifier(ABC):
    """
    Abstract interface implemented by each audio model.

    BirdNET, YAMNet, or another classifier will inherit
    from this class.
    """

    def __init__(
        self,
        model_name: str,
    ) -> None:
        model_name = model_name.strip()

        if not model_name:
            raise ClassifierError(
                "model_name cannot be empty"
            )

        self.model_name = model_name

    @abstractmethod
    def analyze(
        self,
        audio: PreprocessedAudio,
    ) -> ClassificationResult:
        """
        Analyze normalized audio.

        Implementations should return model predictions.
        AlertService decides whether a prediction creates
        an alert.
        """

    def filter_detections(
        self,
        result: ClassificationResult,
        *,
        threshold: float,
        labels: set[str] | None = None,
    ) -> tuple[AudioDetection, ...]:
        """Filter detections by confidence and optional labels."""

        detections = result.detections_above(
            threshold
        )

        if labels is None:
            return detections

        normalized_labels = {
            label.strip().casefold()
            for label in labels
        }

        return tuple(
            detection
            for detection in detections
            if detection.label.casefold()
            in normalized_labels
        )

    @staticmethod
    def validate_audio(
        audio: PreprocessedAudio,
    ) -> None:
        """Validate normalized audio before inference."""

        if not isinstance(audio, PreprocessedAudio):
            raise ClassifierError(
                "audio must be a PreprocessedAudio instance"
            )

        if not audio.processed_path.exists():
            raise ClassifierError(
                "Processed audio does not exist: "
                f"{audio.processed_path}"
            )

        if audio.sample_rate <= 0:
            raise ClassifierError(
                "Processed audio must have a valid sample rate"
            )

        if audio.channels <= 0:
            raise ClassifierError(
                "Processed audio must have at least one channel"
            )

        if audio.duration_seconds <= 0.0:
            raise ClassifierError(
                "Processed audio must have a positive duration"
            )