"""
Measure digital audio level from normalized PCM WAV files.
"""

from __future__ import annotations

import sys
import wave
from array import array
from dataclasses import dataclass
from math import log10, sqrt
from pathlib import Path

from app.audio.preprocessing import PreprocessedAudio


class AudioLevelError(ValueError):
    """Raised when audio level measurement fails."""


@dataclass(frozen=True, slots=True)
class AudioLevel:
    """Measured digital audio level."""

    rms_dbfs: float
    peak_dbfs: float
    sample_count: int
    calibration_offset_db: float | None = None

    @property
    def calibrated_db_spl(self) -> float | None:
        """Return calibrated dB SPL if an offset is configured."""

        if self.calibration_offset_db is None:
            return None

        return self.rms_dbfs + self.calibration_offset_db

    @property
    def alert_strength_db(self) -> float:
        """
        Value stored with the alert.

        Without calibration, this value is dBFS.
        """

        if self.calibrated_db_spl is not None:
            return self.calibrated_db_spl

        return self.rms_dbfs

    @property
    def strength_unit(self) -> str:
        """Return the unit represented by alert_strength_db."""

        if self.calibrated_db_spl is not None:
            return "dB SPL"

        return "dBFS"

    def to_dict(self) -> dict[str, float | int | str | None]:
        """Convert the measurement into a dictionary."""

        return {
            "rms_dbfs": self.rms_dbfs,
            "peak_dbfs": self.peak_dbfs,
            "calibrated_db_spl": self.calibrated_db_spl,
            "alert_strength_db": self.alert_strength_db,
            "strength_unit": self.strength_unit,
            "sample_count": self.sample_count,
            "calibration_offset_db": (
                self.calibration_offset_db
            ),
        }


class AudioLevelMeter:
    """Measure RMS and peak loudness from PCM WAV audio."""

    def __init__(
        self,
        *,
        calibration_offset_db: float | None = None,
    ) -> None:
        self.calibration_offset_db = calibration_offset_db

    def measure(
        self,
        audio: PreprocessedAudio | str | Path,
        *,
        start_seconds: float | None = None,
        end_seconds: float | None = None,
    ) -> AudioLevel:
        """Measure the entire clip or a selected segment."""

        wav_path = self._get_path(audio)

        try:
            with wave.open(
                str(wav_path),
                "rb",
            ) as wav_file:
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                frame_count = wav_file.getnframes()

                self._validate_format(
                    sample_rate=sample_rate,
                    channels=channels,
                    sample_width=sample_width,
                )

                start_frame = self._seconds_to_frame(
                    start_seconds,
                    sample_rate,
                    frame_count,
                    default_frame=0,
                )

                end_frame = self._seconds_to_frame(
                    end_seconds,
                    sample_rate,
                    frame_count,
                    default_frame=frame_count,
                )

                if end_frame <= start_frame:
                    raise AudioLevelError(
                        "Audio measurement segment is empty"
                    )

                wav_file.setpos(start_frame)

                frame_data = wav_file.readframes(
                    end_frame - start_frame
                )

        except (OSError, wave.Error) as error:
            raise AudioLevelError(
                f"Unable to read audio level: {error}"
            ) from error

        samples = array("h")
        samples.frombytes(frame_data)

        if sys.byteorder != "little":
            samples.byteswap()

        if not samples:
            raise AudioLevelError(
                "Audio contains no samples"
            )

        sample_count = len(samples)

        peak_amplitude = max(
            abs(sample)
            for sample in samples
        )

        squared_total = sum(
            sample * sample
            for sample in samples
        )

        rms_amplitude = sqrt(
            squared_total / sample_count
        )

        return AudioLevel(
            rms_dbfs=self._to_dbfs(rms_amplitude),
            peak_dbfs=self._to_dbfs(peak_amplitude),
            sample_count=sample_count,
            calibration_offset_db=(
                self.calibration_offset_db
            ),
        )

    @staticmethod
    def _get_path(
        audio: PreprocessedAudio | str | Path,
    ) -> Path:
        if isinstance(audio, PreprocessedAudio):
            path = audio.processed_path
        else:
            path = Path(audio)

        if not path.exists() or not path.is_file():
            raise AudioLevelError(
                f"Audio file does not exist: {path}"
            )

        return path

    @staticmethod
    def _validate_format(
        *,
        sample_rate: int,
        channels: int,
        sample_width: int,
    ) -> None:
        if sample_rate <= 0:
            raise AudioLevelError(
                "Audio has an invalid sample rate"
            )

        if channels != 1:
            raise AudioLevelError(
                "Audio must be mono before measurement"
            )

        if sample_width != 2:
            raise AudioLevelError(
                "Audio must use 16-bit PCM samples"
            )

    @staticmethod
    def _seconds_to_frame(
        seconds: float | None,
        sample_rate: int,
        frame_count: int,
        *,
        default_frame: int,
    ) -> int:
        if seconds is None:
            return default_frame

        if seconds < 0:
            raise AudioLevelError(
                "Time cannot be negative"
            )

        return min(
            int(seconds * sample_rate),
            frame_count,
        )

    @staticmethod
    def _to_dbfs(
        amplitude: float,
    ) -> float:
        if amplitude <= 0:
            return -100.0

        return max(
            -100.0,
            20.0 * log10(
                amplitude / 32768.0
            ),
        )