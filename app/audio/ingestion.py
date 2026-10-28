"""
Audio file ingestion for uploads, microphones, and sensor recordings.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from shutil import copy2
from typing import Any
from uuid import uuid4


class AudioIngestionError(ValueError):
    """Raised when an audio file cannot be accepted."""


@dataclass(frozen=True, slots=True)
class AudioRecording:
    """Metadata for an ingested audio recording."""

    recording_id: str
    original_filename: str
    stored_path: Path
    source: str
    received_at: datetime
    size_bytes: int
    sensor_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert recording metadata into a dictionary."""

        return {
            "recording_id": self.recording_id,
            "original_filename": self.original_filename,
            "stored_path": str(self.stored_path),
            "source": self.source,
            "received_at": self.received_at.astimezone(
                timezone.utc
            ).isoformat(),
            "size_bytes": self.size_bytes,
            "sensor_id": self.sensor_id,
        }


class AudioIngestionService:
    """Validate and safely stage audio files for analysis."""

    ALLOWED_EXTENSIONS = frozenset(
        {
            ".aac",
            ".flac",
            ".m4a",
            ".mp3",
            ".ogg",
            ".wav",
            ".webm",
        }
    )

    ALLOWED_SOURCES = frozenset(
        {
            "upload",
            "microphone",
            "sensor",
        }
    )

    def __init__(
        self,
        storage_directory: str | Path = "runtime/audio",
        *,
        max_file_size_mb: int = 25,
    ) -> None:
        if max_file_size_mb <= 0:
            raise AudioIngestionError(
                "max_file_size_mb must be greater than zero"
            )

        self.storage_directory = Path(storage_directory)
        self.max_file_size_bytes = max_file_size_mb * 1024 * 1024

    def ingest(
        self,
        audio_path: str | Path,
        *,
        source: str = "upload",
        sensor_id: str | None = None,
    ) -> AudioRecording:
        """
        Validate and copy an audio file into the runtime directory.

        Gradio can provide the audio path from a computer, phone upload,
        microphone recording, or local sensor process.
        """

        source = self._validate_source(source)
        source_path = self._validate_input_path(audio_path)

        self._validate_extension(source_path)
        self._validate_file_size(source_path)

        if sensor_id is not None:
            sensor_id = sensor_id.strip()

            if not sensor_id:
                raise AudioIngestionError(
                    "sensor_id cannot be empty when provided"
                )

        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        recording_id = str(uuid4())

        destination = (
            self.storage_directory
            / f"{recording_id}{source_path.suffix.lower()}"
        )

        try:
            copy2(source_path, destination)
        except OSError as error:
            raise AudioIngestionError(
                f"Unable to stage audio file: {error}"
            ) from error

        return AudioRecording(
            recording_id=recording_id,
            original_filename=source_path.name,
            stored_path=destination,
            source=source,
            received_at=datetime.now(timezone.utc),
            size_bytes=destination.stat().st_size,
            sensor_id=sensor_id,
        )

    def delete_recording(
        self,
        recording: AudioRecording,
    ) -> None:
        """Delete a staged audio file after processing."""

        try:
            recording.stored_path.unlink(
                missing_ok=True
            )
        except OSError as error:
            raise AudioIngestionError(
                f"Unable to delete staged audio file: {error}"
            ) from error

    @classmethod
    def _validate_source(
        cls,
        source: str,
    ) -> str:
        if source is None:
            raise AudioIngestionError(
                "source is required"
            )

        normalized_source = str(source).strip().lower()

        if normalized_source not in cls.ALLOWED_SOURCES:
            allowed_sources = ", ".join(
                sorted(cls.ALLOWED_SOURCES)
            )

            raise AudioIngestionError(
                f"source must be one of: {allowed_sources}"
            )

        return normalized_source

    @staticmethod
    def _validate_input_path(
        audio_path: str | Path,
    ) -> Path:
        if audio_path is None:
            raise AudioIngestionError(
                "Please upload or record an audio file first"
            )

        path = Path(audio_path)

        if not path.exists():
            raise AudioIngestionError(
                f"Audio file does not exist: {path}"
            )

        if not path.is_file():
            raise AudioIngestionError(
                f"Audio path is not a file: {path}"
            )

        return path

    @classmethod
    def _validate_extension(
        cls,
        path: Path,
    ) -> None:
        if path.suffix.lower() not in cls.ALLOWED_EXTENSIONS:
            allowed_extensions = ", ".join(
                sorted(cls.ALLOWED_EXTENSIONS)
            )

            raise AudioIngestionError(
                f"Unsupported audio format '{path.suffix}'. "
                f"Allowed formats: {allowed_extensions}"
            )

    def _validate_file_size(
        self,
        path: Path,
    ) -> None:
        try:
            file_size = path.stat().st_size
        except OSError as error:
            raise AudioIngestionError(
                f"Unable to read audio file metadata: {error}"
            ) from error

        if file_size == 0:
            raise AudioIngestionError(
                "The audio file is empty"
            )

        if file_size > self.max_file_size_bytes:
            max_size_mb = self.max_file_size_bytes / (
                1024 * 1024
            )

            raise AudioIngestionError(
                f"Audio file exceeds the "
                f"{max_size_mb:g} MB limit"
            )