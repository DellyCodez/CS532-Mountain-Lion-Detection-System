"""
Audio normalization before model inference.
"""

from __future__ import annotations

import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from typing import Any
from uuid import uuid4

from app.audio.ingestion import AudioRecording


class AudioPreprocessingError(ValueError):
    """Raised when an audio file cannot be normalized."""


@dataclass(frozen=True, slots=True)
class PreprocessedAudio:
    """Metadata for audio ready for model inference."""

    recording_id: str | None
    source_path: Path
    processed_path: Path
    sample_rate: int
    channels: int
    sample_width_bytes: int
    duration_seconds: float

    def to_dict(self) -> dict[str, Any]:
        """Convert metadata into a dictionary."""

        return {
            "recording_id": self.recording_id,
            "source_path": str(self.source_path),
            "processed_path": str(self.processed_path),
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "sample_width_bytes": self.sample_width_bytes,
            "duration_seconds": self.duration_seconds,
        }


class AudioPreprocessingService:
    """Convert uploaded audio into mono PCM WAV audio."""

    def __init__(
        self,
        output_directory: str | Path = "runtime/preprocessed_audio",
        *,
        target_sample_rate: int = 16_000,
        max_duration_seconds: float = 300.0,
        ffmpeg_binary: str = "ffmpeg",
    ) -> None:
        if target_sample_rate <= 0:
            raise AudioPreprocessingError(
                "target_sample_rate must be greater than zero"
            )

        if max_duration_seconds <= 0:
            raise AudioPreprocessingError(
                "max_duration_seconds must be greater than zero"
            )

        self.output_directory = Path(output_directory)
        self.target_sample_rate = target_sample_rate
        self.max_duration_seconds = max_duration_seconds
        self.ffmpeg_binary = ffmpeg_binary

    def preprocess(
        self,
        recording: AudioRecording | str | Path,
    ) -> PreprocessedAudio:
        """
        Convert audio to mono, 16-bit PCM WAV at 16 kHz.

        The input can be an AudioRecording object or a direct file path.
        """

        recording_id = None

        if isinstance(recording, AudioRecording):
            source_path = recording.stored_path
            recording_id = recording.recording_id
        else:
            source_path = Path(recording)

        self._validate_source_path(source_path)
        self._validate_ffmpeg()

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        processed_path = (
            self.output_directory / f"{uuid4()}.wav"
        )

        command = [
            self.ffmpeg_binary,
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source_path),
            "-vn",
            "-ac",
            "1",
            "-ar",
            str(self.target_sample_rate),
            "-c:a",
            "pcm_s16le",
            "-f",
            "wav",
            str(processed_path),
        ]

        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=120,
            )

        except subprocess.TimeoutExpired as error:
            processed_path.unlink(missing_ok=True)

            raise AudioPreprocessingError(
                "Audio preprocessing timed out"
            ) from error

        except subprocess.CalledProcessError as error:
            processed_path.unlink(missing_ok=True)

            details = (
                error.stderr.strip()
                or "Unknown ffmpeg error"
            )

            raise AudioPreprocessingError(
                f"Audio preprocessing failed: {details}"
            ) from error

        except OSError as error:
            processed_path.unlink(missing_ok=True)

            raise AudioPreprocessingError(
                f"Unable to start ffmpeg: {error}"
            ) from error

        if not processed_path.exists():
            raise AudioPreprocessingError(
                "ffmpeg did not produce a processed audio file"
            )

        metadata = self._read_wav_metadata(
            processed_path
        )

        if (
            metadata.duration_seconds
            > self.max_duration_seconds
        ):
            processed_path.unlink(missing_ok=True)

            raise AudioPreprocessingError(
                "Audio duration exceeds the "
                f"{self.max_duration_seconds:g}-second limit"
            )

        return PreprocessedAudio(
            recording_id=recording_id,
            source_path=source_path,
            processed_path=processed_path,
            sample_rate=metadata.sample_rate,
            channels=metadata.channels,
            sample_width_bytes=metadata.sample_width_bytes,
            duration_seconds=metadata.duration_seconds,
        )

    def delete_processed_audio(
        self,
        audio: PreprocessedAudio,
    ) -> None:
        """Delete normalized audio after model inference."""

        try:
            audio.processed_path.unlink(
                missing_ok=True
            )

        except OSError as error:
            raise AudioPreprocessingError(
                f"Unable to delete processed audio: {error}"
            ) from error

    def _validate_ffmpeg(self) -> None:
        if which(self.ffmpeg_binary) is None:
            raise AudioPreprocessingError(
                "ffmpeg is required for audio preprocessing "
                "but was not found. Install ffmpeg and make "
                "sure it is available on PATH."
            )

    @staticmethod
    def _validate_source_path(
        source_path: Path,
    ) -> None:
        if not source_path.exists():
            raise AudioPreprocessingError(
                f"Audio file does not exist: {source_path}"
            )

        if not source_path.is_file():
            raise AudioPreprocessingError(
                f"Audio path is not a file: {source_path}"
            )

    @staticmethod
    def _read_wav_metadata(
        wav_path: Path,
    ) -> PreprocessedAudio:
        try:
            with wave.open(
                str(wav_path),
                "rb",
            ) as wav_file:
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width_bytes = (
                    wav_file.getsampwidth()
                )
                frame_count = wav_file.getnframes()

        except (OSError, wave.Error) as error:
            raise AudioPreprocessingError(
                f"Unable to read processed WAV file: {error}"
            ) from error

        if sample_rate <= 0 or channels <= 0:
            raise AudioPreprocessingError(
                "Processed audio has invalid WAV metadata"
            )

        duration_seconds = frame_count / sample_rate

        return PreprocessedAudio(
            recording_id=None,
            source_path=wav_path,
            processed_path=wav_path,
            sample_rate=sample_rate,
            channels=channels,
            sample_width_bytes=sample_width_bytes,
            duration_seconds=duration_seconds,
        )