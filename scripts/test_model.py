"""
Test a trained BirdNET classifier against audio files.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from app.audio.ingestion import AudioIngestionService
from app.audio.preprocessing import (
    AudioPreprocessingService,
)
from app.config import AppConfig
from app.models.BirdNetClassifier import(
    BirdNetClassifier,
)


SUPPORTED_AUDIO_EXTENSIONS = {
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".wav",
    ".webm",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Test a trained BirdNET classifier."
    )

    parser.add_argument(
        "audio_paths",
        nargs="+",
        type=Path,
        help="Audio files or directories to analyze.",
    )

    parser.add_argument(
        "--model",
        type=Path,
        default=None,
        help="Path to the custom TFLite model.",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.40,
    )

    parser.add_argument(
        "--keep-files",
        action="store_true",
    )

    return parser


def collect_audio_files(
    input_paths: list[Path],
) -> list[Path]:
    """Expand files and directories into audio paths."""

    audio_files: list[Path] = []

    for input_path in input_paths:
        if not input_path.exists():
            raise FileNotFoundError(
                f"Audio path does not exist: {input_path}"
            )

        if input_path.is_file():
            if input_path.suffix.lower() in (
                SUPPORTED_AUDIO_EXTENSIONS
            ):
                audio_files.append(input_path)

        elif input_path.is_dir():
            audio_files.extend(
                path
                for path in input_path.rglob("*")
                if (
                    path.is_file()
                    and path.suffix.lower()
                    in SUPPORTED_AUDIO_EXTENSIONS
                )
            )

    audio_files = sorted(
        {path.resolve() for path in audio_files}
    )

    if not audio_files:
        raise ValueError(
            "No supported audio files were found"
        )

    return audio_files


def test_model(
    *,
    audio_files: list[Path],
    model_path: Path,
    threshold: float,
    keep_files: bool,
) -> None:
    """Run inference against each selected file."""

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "threshold must be between 0.0 and 1.0"
        )

    config = AppConfig.from_environment()

    ingestion_service = AudioIngestionService(
        storage_directory=(
            config.audio.ingestion_directory
        )
    )

    preprocessing_service = AudioPreprocessingService(
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

    classifier = BirdNetClassifier(
        model_path=model_path,
        birdnet_command=config.model.birdnet_command,
        minimum_model_confidence=(
            config.model.minimum_model_confidence
        ),
    )

    for audio_path in audio_files:
        recording = None
        processed_audio = None

        print("\n" + "=" * 60)
        print("Analyzing:", audio_path)

        try:
            recording = ingestion_service.ingest(
                audio_path,
                source="upload",
            )

            processed_audio = (
                preprocessing_service.preprocess(
                    recording
                )
            )

            result = classifier.analyze(
                processed_audio
            )

            detections = result.detections_above(
                threshold
            )

            if not detections:
                print(
                    "No detections above "
                    f"{threshold:.0%} confidence."
                )
                continue

            print("Detections:")

            for detection in detections:
                print(
                    f"- {detection.label}: "
                    f"{detection.confidence:.2%}"
                )

                if detection.start_seconds is not None:
                    end_seconds = (
                        detection.end_seconds or 0.0
                    )

                    print(
                        "  Time: "
                        f"{detection.start_seconds:.2f}s - "
                        f"{end_seconds:.2f}s"
                    )

        finally:
            if not keep_files:
                if processed_audio is not None:
                    preprocessing_service.delete_processed_audio(
                        processed_audio
                    )

                if recording is not None:
                    ingestion_service.delete_recording(
                        recording
                    )


def main() -> None:
    args = build_parser().parse_args()
    config = AppConfig.from_environment()

    model_path = args.model or config.model.model_path

    audio_files = collect_audio_files(
        args.audio_paths
    )

    test_model(
        audio_files=audio_files,
        model_path=model_path,
        threshold=args.threshold,
        keep_files=args.keep_files,
    )


if __name__ == "__main__":
    main()