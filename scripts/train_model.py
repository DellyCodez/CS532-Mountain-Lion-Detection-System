"""
Train the custom BirdNET classifier.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from shutil import which


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train a custom BirdNET classifier."
    )

    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=Path("data/raw/my_dataset"),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(
            "models/training/mountain_lion_model"
        ),
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=20,
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=4,
    )

    parser.add_argument(
        "--crop-mode",
        choices=["segments", "full"],
        default="segments",
    )

    parser.add_argument(
        "--validation-split",
        type=float,
        default=0.25,
    )

    parser.add_argument(
        "--birdnet-command",
        default="birdnet-train",
    )

    return parser


def train_model(
    *,
    dataset_dir: Path,
    output_dir: Path,
    epochs: int,
    batch_size: int,
    crop_mode: str,
    validation_split: float,
    birdnet_command: str,
) -> None:
    """Run BirdNET training with validated arguments."""

    if not dataset_dir.is_dir():
        raise FileNotFoundError(
            f"Dataset directory does not exist: {dataset_dir}"
        )

    if epochs <= 0 or batch_size <= 0:
        raise ValueError(
            "epochs and batch_size must be greater than zero"
        )

    if not 0.0 < validation_split < 1.0:
        raise ValueError(
            "validation_split must be between 0 and 1"
        )

    if which(birdnet_command) is None:
        raise RuntimeError(
            f"BirdNET command was not found: "
            f"{birdnet_command}"
        )

    output_dir.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        birdnet_command,
        "--output",
        str(output_dir),
        "--epochs",
        str(epochs),
        "--batch_size",
        str(batch_size),
        "--crop_mode",
        crop_mode,
        "--val_split",
        str(validation_split),
        str(dataset_dir),
    ]

    print(
        "Starting BirdNET custom classifier training..."
    )
    print("Dataset:", dataset_dir)
    print("Output:", output_dir)

    subprocess.run(command, check=True)

    print("Training complete.")


def main() -> None:
    args = build_parser().parse_args()

    train_model(
        dataset_dir=args.dataset_dir,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        crop_mode=args.crop_mode,
        validation_split=args.validation_split,
        birdnet_command=args.birdnet_command,
    )


if __name__ == "__main__":
    main()