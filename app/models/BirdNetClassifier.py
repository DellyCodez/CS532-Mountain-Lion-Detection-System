"""
BirdNET command-line classifier adapter.
"""

from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.audio.preprocessing import PreprocessedAudio
from app.models.baseClassifier import (
    AudioDetection,
    BaseClassifier,
    ClassificationResult,
    ClassifierError,
)


class BirdNetClassifierError(ClassifierError):
    """Raised when BirdNET cannot analyze audio."""


class BirdNetClassifier(BaseClassifier):
    """Run a BirdNET custom classifier and parse its output."""

    def __init__(
        self,
        model_path: str | Path,
        output_directory: str | Path = (
            "runtime/birdnet_results"
        ),
        *,
        birdnet_command: str = "birdnet-analyze",
        minimum_model_confidence: float = 0.10,
        timeout_seconds: int = 120,
        keep_raw_output: bool = False,
    ) -> None:
        super().__init__(
            model_name="BirdNET Custom Classifier"
        )

        self.model_path = Path(model_path)
        self.output_directory = Path(output_directory)
        self.birdnet_command = birdnet_command
        self.minimum_model_confidence = (
            minimum_model_confidence
        )
        self.timeout_seconds = timeout_seconds
        self.keep_raw_output = keep_raw_output

        if not 0.0 <= minimum_model_confidence <= 1.0:
            raise BirdNetClassifierError(
                "minimum_model_confidence must be between "
                "0.0 and 1.0"
            )

        if timeout_seconds <= 0:
            raise BirdNetClassifierError(
                "timeout_seconds must be greater than zero"
            )

    def analyze(
        self,
        audio: PreprocessedAudio,
    ) -> ClassificationResult:
        """Analyze normalized audio with BirdNET."""

        self.validate_audio(audio)
        self._validate_model()
        self._validate_command()

        analysis_directory = (
            self.output_directory / str(uuid4())
        )

        analysis_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        command = [
            self.birdnet_command,
            "--classifier",
            str(self.model_path),
            "--output",
            str(analysis_directory),
            "--min_conf",
            str(self.minimum_model_confidence),
            str(audio.processed_path),
        ]

        try:
            subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )

            result_files = self._find_result_files(
                analysis_directory
            )

            detections = self._parse_result_files(
                result_files
            )

            metadata: dict[str, Any] = {
                "minimum_model_confidence": (
                    self.minimum_model_confidence
                ),
                "result_file_count": len(result_files),
            }

            if self.keep_raw_output:
                metadata["raw_output_directory"] = str(
                    analysis_directory
                )

            return ClassificationResult(
                model_name=self.model_name,
                processed_audio=audio,
                detections=tuple(detections),
                metadata=metadata,
            )

        except subprocess.TimeoutExpired as error:
            raise BirdNetClassifierError(
                "BirdNET analysis timed out"
            ) from error

        except subprocess.CalledProcessError as error:
            details = (
                error.stderr.strip()
                or "Unknown BirdNET error"
            )

            raise BirdNetClassifierError(
                f"BirdNET analysis failed: {details}"
            ) from error

        except OSError as error:
            raise BirdNetClassifierError(
                f"Unable to run BirdNET: {error}"
            ) from error

        finally:
            if not self.keep_raw_output:
                shutil.rmtree(
                    analysis_directory,
                    ignore_errors=True,
                )

    def _validate_model(self) -> None:
        if not self.model_path.exists():
            raise BirdNetClassifierError(
                "BirdNET model does not exist: "
                f"{self.model_path}"
            )

        if not self.model_path.is_file():
            raise BirdNetClassifierError(
                "BirdNET model path is not a file: "
                f"{self.model_path}"
            )

    def _validate_command(self) -> None:
        if shutil.which(self.birdnet_command) is None:
            raise BirdNetClassifierError(
                "BirdNET command was not found: "
                f"{self.birdnet_command}"
            )

    @staticmethod
    def _find_result_files(
        analysis_directory: Path,
    ) -> list[Path]:
        result_files = sorted(
            analysis_directory.glob("*.txt")
        )

        result_files.extend(
            sorted(
                analysis_directory.glob("*.csv")
            )
        )

        if not result_files:
            raise BirdNetClassifierError(
                "BirdNET completed but did not create "
                "a result file"
            )

        return result_files

    @classmethod
    def _parse_result_files(
        cls,
        result_files: list[Path],
    ) -> list[AudioDetection]:
        detections: list[AudioDetection] = []

        for result_file in result_files:
            try:
                with result_file.open(
                    "r",
                    encoding="utf-8-sig",
                    newline="",
                ) as file:
                    sample = file.read(4096)
                    file.seek(0)

                    delimiter = cls._detect_delimiter(
                        sample
                    )

                    reader = csv.DictReader(
                        file,
                        delimiter=delimiter,
                    )

                    for row in reader:
                        detection = cls._parse_row(
                            row
                        )

                        if detection is not None:
                            detections.append(
                                detection
                            )

            except (OSError, csv.Error) as error:
                raise BirdNetClassifierError(
                    "Unable to parse BirdNET output "
                    f"'{result_file}': {error}"
                ) from error

        return detections

    @staticmethod
    def _detect_delimiter(
        sample: str,
    ) -> str:
        first_line = (
            sample.splitlines()[0]
            if sample
            else ""
        )

        if "\t" in first_line:
            return "\t"

        return ","

    @classmethod
    def _parse_row(
        cls,
        row: dict[str, Any],
    ) -> AudioDetection | None:
        confidence_value = cls._get_field(
            row,
            "confidence",
            "score",
            "probability",
        )

        if confidence_value is None:
            return None

        confidence = cls._parse_confidence(
            confidence_value
        )

        if confidence is None:
            return None

        label = cls._get_field(
            row,
            "common name",
            "scientific name",
            "species",
            "label",
            "class",
        )

        if not label:
            label = "Unknown"

        start_seconds = cls._parse_optional_float(
            cls._get_field(
                row,
                "start (s)",
                "start",
                "start seconds",
                "start_s",
            )
        )

        end_seconds = cls._parse_optional_float(
            cls._get_field(
                row,
                "end (s)",
                "end",
                "end seconds",
                "end_s",
            )
        )

        return AudioDetection(
            label=label,
            confidence=confidence,
            start_seconds=start_seconds,
            end_seconds=end_seconds,
        )

    @staticmethod
    def _get_field(
        row: dict[str, Any],
        *field_names: str,
    ) -> str | None:
        normalized_row = {
            BirdNetClassifier._normalize_field_name(
                key
            ): value
            for key, value in row.items()
            if key is not None
        }

        for field_name in field_names:
            normalized_name = (
                BirdNetClassifier._normalize_field_name(
                    field_name
                )
            )

            value = normalized_row.get(
                normalized_name
            )

            if value is not None and str(value).strip():
                return str(value).strip()

        return None

    @staticmethod
    def _normalize_field_name(
        field_name: str,
    ) -> str:
        return (
            field_name.strip()
            .casefold()
            .replace("_", " ")
            .replace("-", " ")
        )

    @staticmethod
    def _parse_confidence(
        value: Any,
    ) -> float | None:
        try:
            text = str(value).strip()
            is_percentage = text.endswith("%")

            if is_percentage:
                text = text[:-1].strip()

            confidence = float(text)

            if is_percentage:
                confidence /= 100.0
            elif confidence > 1.0:
                confidence /= 100.0

            if not 0.0 <= confidence <= 1.0:
                return None

            return confidence

        except (TypeError, ValueError):
            return None

    @staticmethod
    def _parse_optional_float(
        value: str | None,
    ) -> float | None:
        if value is None:
            return None

        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return None

        return parsed if parsed >= 0.0 else None