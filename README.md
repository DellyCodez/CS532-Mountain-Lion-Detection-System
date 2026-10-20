# CS 532 - Mountain Lion Detection System

This repository is for the CS 532 Software Engineering team project.

The Mountain Lion Detection System is being designed to help park rangers monitor possible mountain lion activity. Planned functionality includes receiving sensor alerts, ranger acknowledgement and classification, storing detection history, and generating reports.

## Current project status (audit: October 20, 2026)
This is a **work-in-progress student project**, not a completed or validated release. The `main` branch contains an audio detection prototype; `development` contains early sensor networking work not yet integrated with `main`. See the [integration register](docs/configuration/INTEGRATION_REGISTER.md).

## Project documents
- [Requirements](docs/requirements/README.md)
- [System architecture and database design](docs/design/README.md)
- [Testing plans and evidence](docs/testing/README.md)
- [Software Development Folder / notebook evidence](docs/sdf/README.md)
- [Configuration management and handoff records](docs/configuration/README.md)

## Git workflow
Work on a separate branch; open a PR for review before merging. The intended roles for `main` and `development` are recorded in the [version control plan](docs/configuration/VERSION_CONTROL_PLAN.md). Branch-protection settings may still need to be enabled by the repository owner. The latest branch is **not** automatically an approved release.

## Running the software
A verified, reproducible end-to-end run procedure has not yet been committed. Developers should document the environment, model files and dependencies in the [build record](docs/configuration/BUILD_RECORD.md). Avoid committing secrets, large raw audio files, and machine-specific file paths.
