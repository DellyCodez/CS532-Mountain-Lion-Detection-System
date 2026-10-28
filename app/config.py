"""
Application configuration for local and cloud deployments.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ConfigurationError(ValueError):
    """Raised when an environment setting is invalid."""


class StorageMode(str, Enum):
    """Supported alert storage backends."""

    LOCAL = "local"
    FIREBASE = "firebase"

    @classmethod
    def from_value(
        cls,
        value: str | None,
    ) -> "StorageMode":
        normalized = (
            value or cls.LOCAL.value
        ).strip().lower()

        aliases = {
            "local": cls.LOCAL,
            "sqlite": cls.LOCAL,
            "local sqlite": cls.LOCAL,
            "firebase": cls.FIREBASE,
            "firebase cloud": cls.FIREBASE,
            "cloud": cls.FIREBASE,
        }

        try:
            return aliases[normalized]
        except KeyError as error:
            raise ConfigurationError(
                "MLDS_STORAGE_MODE must be local or firebase"
            ) from error


@dataclass(frozen=True, slots=True)
class ParkConfig:
    """Park and ranger-station settings."""

    name: str
    station_latitude: float
    station_longitude: float
    monitored_area_square_miles: float


@dataclass(frozen=True, slots=True)
class ModelConfig:
    """Audio model and inference settings."""

    model_path: Path
    birdnet_command: str
    minimum_model_confidence: float
    alert_confidence_threshold: float


@dataclass(frozen=True, slots=True)
class AudioConfig:
    """Audio upload and preprocessing settings."""

    ingestion_directory: Path
    preprocessing_directory: Path
    max_file_size_mb: int
    target_sample_rate: int
    max_duration_seconds: float


@dataclass(frozen=True, slots=True)
class DatabaseConfig:
    """Local SQLite and Firebase settings."""

    mode: StorageMode
    local_database_path: Path
    firebase_project_id: str | None
    firebase_credentials_path: Path | None
    firebase_storage_bucket: str | None


@dataclass(frozen=True, slots=True)
class UIConfig:
    """Web server settings for local and hosted use."""

    server_name: str
    server_port: int
    share: bool


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Complete application configuration."""

    project_root: Path
    park: ParkConfig
    model: ModelConfig
    audio: AudioConfig
    database: DatabaseConfig
    ui: UIConfig

    @classmethod
    def from_environment(
        cls,
        project_root: str | Path | None = None,
    ) -> "AppConfig":
        """Build configuration from environment variables."""

        root = Path(
            project_root
            or os.getenv("MLDS_PROJECT_ROOT")
            or Path(__file__).resolve().parents[1]
        ).expanduser().resolve()

        runtime_directory = root / "runtime"

        park = ParkConfig(
            name=_get_text(
                "MLDS_PARK_NAME",
                "San Diego County Parks",
            ),
            station_latitude=_get_float(
                "MLDS_STATION_LATITUDE",
                32.7157,
            ),
            station_longitude=_get_float(
                "MLDS_STATION_LONGITUDE",
                -117.1611,
            ),
            monitored_area_square_miles=_get_float(
                "MLDS_MONITORED_AREA_SQUARE_MILES",
                5.0,
            ),
        )

        model = ModelConfig(
            model_path=_get_path(
                "MLDS_MODEL_PATH",
                root
                / "models"
                / "birdnet"
                / "mountain_lion_model.tflite",
            ),
            birdnet_command=_get_text(
                "MLDS_BIRDNET_COMMAND",
                "birdnet-analyze",
            ),
            minimum_model_confidence=_get_float(
                "MLDS_MODEL_MINIMUM_CONFIDENCE",
                0.10,
            ),
            alert_confidence_threshold=_get_float(
                "MLDS_ALERT_CONFIDENCE_THRESHOLD",
                0.40,
            ),
        )

        audio = AudioConfig(
            ingestion_directory=_get_path(
                "MLDS_AUDIO_INGESTION_DIRECTORY",
                runtime_directory / "audio",
            ),
            preprocessing_directory=_get_path(
                "MLDS_AUDIO_PREPROCESSING_DIRECTORY",
                runtime_directory / "preprocessed_audio",
            ),
            max_file_size_mb=_get_int(
                "MLDS_AUDIO_MAX_FILE_SIZE_MB",
                25,
            ),
            target_sample_rate=_get_int(
                "MLDS_AUDIO_TARGET_SAMPLE_RATE",
                16_000,
            ),
            max_duration_seconds=_get_float(
                "MLDS_AUDIO_MAX_DURATION_SECONDS",
                300.0,
            ),
        )

        storage_mode = StorageMode.from_value(
            os.getenv("MLDS_STORAGE_MODE")
        )

        credentials_value = os.getenv(
            "FIREBASE_CREDENTIALS_PATH"
        )

        database = DatabaseConfig(
            mode=storage_mode,
            local_database_path=_get_path(
                "MLDS_LOCAL_DATABASE_PATH",
                runtime_directory / "alerts.db",
            ),
            firebase_project_id=_get_optional_text(
                "FIREBASE_PROJECT_ID"
            ),
            firebase_credentials_path=(
                Path(credentials_value)
                .expanduser()
                .resolve()
                if credentials_value
                else None
            ),
            firebase_storage_bucket=_get_optional_text(
                "FIREBASE_STORAGE_BUCKET"
            ),
        )

        ui = UIConfig(
            server_name=_get_text(
                "MLDS_SERVER_NAME",
                "127.0.0.1",
            ),
            server_port=_get_int(
                "MLDS_SERVER_PORT",
                7860,
            ),
            share=_get_bool(
                "MLDS_GRADIO_SHARE",
                False,
            ),
        )

        config = cls(
            project_root=root,
            park=park,
            model=model,
            audio=audio,
            database=database,
            ui=ui,
        )

        config.validate()
        return config

    def validate(self) -> None:
        """Validate configuration before startup."""

        if not -90.0 <= self.park.station_latitude <= 90.0:
            raise ConfigurationError(
                "Station latitude must be between -90 and 90"
            )

        if not -180.0 <= self.park.station_longitude <= 180.0:
            raise ConfigurationError(
                "Station longitude must be between -180 and 180"
            )

        if self.park.monitored_area_square_miles <= 0:
            raise ConfigurationError(
                "Monitored area must be greater than zero"
            )

        confidence_values = {
            "minimum_model_confidence": (
                self.model.minimum_model_confidence
            ),
            "alert_confidence_threshold": (
                self.model.alert_confidence_threshold
            ),
        }

        for name, value in confidence_values.items():
            if not 0.0 <= value <= 1.0:
                raise ConfigurationError(
                    f"{name} must be between 0.0 and 1.0"
                )

        if self.audio.max_file_size_mb <= 0:
            raise ConfigurationError(
                "Audio file size limit must be greater than zero"
            )

        if self.audio.target_sample_rate <= 0:
            raise ConfigurationError(
                "Audio sample rate must be greater than zero"
            )

        if self.audio.max_duration_seconds <= 0:
            raise ConfigurationError(
                "Audio duration limit must be greater than zero"
            )

        if not 1 <= self.ui.server_port <= 65_535:
            raise ConfigurationError(
                "Server port must be between 1 and 65535"
            )

    def ensure_runtime_directories(self) -> None:
        """Create directories needed during execution."""

        self.audio.ingestion_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.audio.preprocessing_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.database.local_database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


def _get_text(
    variable_name: str,
    default: str,
) -> str:
    value = os.getenv(
        variable_name,
        default,
    ).strip()

    if not value:
        raise ConfigurationError(
            f"{variable_name} cannot be empty"
        )

    return value


def _get_optional_text(
    variable_name: str,
) -> str | None:
    value = os.getenv(variable_name)

    if value is None:
        return None

    value = value.strip()

    return value or None


def _get_path(
    variable_name: str,
    default: Path,
) -> Path:
    value = os.getenv(variable_name)

    if value is None or not value.strip():
        return default

    return Path(value).expanduser().resolve()


def _get_float(
    variable_name: str,
    default: float,
) -> float:
    value = os.getenv(variable_name)

    if value is None:
        return default

    try:
        return float(value)
    except ValueError as error:
        raise ConfigurationError(
            f"{variable_name} must be a number"
        ) from error


def _get_int(
    variable_name: str,
    default: int,
) -> int:
    value = os.getenv(variable_name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError as error:
        raise ConfigurationError(
            f"{variable_name} must be an integer"
        ) from error


def _get_bool(
    variable_name: str,
    default: bool,
) -> bool:
    value = os.getenv(variable_name)

    if value is None:
        return default

    normalized = value.strip().lower()

    if normalized in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return True

    if normalized in {
        "0",
        "false",
        "no",
        "off",
    }:
        return False

    raise ConfigurationError(
        f"{variable_name} must be true or false"
    )