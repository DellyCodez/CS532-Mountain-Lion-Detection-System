# NotFlock - Mountain Lion Detection System

**CS 532 Software Engineering | San Diego State University**

NotFlock is our team project for helping California State Park rangers monitor possible mountain lion activity through sound detection. The goal is to use audio analysis to identify possible mountain lion sounds, notify rangers, and give them a way to review and keep track of detections.

## How the System Works

1. A sensor or uploaded recording provides an audio clip.
2. The detection program analyzes the sound for a possible mountain lion match.
3. A possible detection produces an alert with information such as the sound type, strength, and location.
4. A ranger reviews the alert and classifies it as **Definite**, **Suspected**, or **False**.
5. Detection records can be used to view activity history and generate reports.

This is the system workflow described in our requirements. The code is organized into different components as the team develops and connects them.

## Technologies

We use **Python** for development, **BirdNET** for audio analysis, and **Gradio** for the Python-based interface.

## Finding Files in This Repository

| Location | What to look for |
| --- | --- |
| [`main.py`](main.py) | Audio detection prototype |
| [Backend code (`development` branch)](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/tree/development/backend) | Sensor and backend component files |
| [`RangerModel.py` (`testing` branch)](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/blob/testing/RangerModel.py) | Ranger interface and alert-handling code |
| [`docs/requirements/`](docs/requirements/) | Functional and non-functional requirements, user stories, use cases, and traceability |
| [`docs/design/`](docs/design/) | System and interface design documentation |
| [`docs/testing/`](docs/testing/) | Testing documentation |
| [`docs/configuration/`](docs/configuration/) | Configuration Management and Version Control Plans |
| [`docs/sdf/`](docs/sdf/) | Software Development Folder documentation |

The **branch selector** on GitHub lets you switch between `main`, `development`, `backend`, and `testing` to view work in each area. Files in a working branch may be different from the reviewed files in `main`.

## How Our Team Uses GitHub

We use GitHub to keep our code and documentation organized and to track changes made by different team members.

| Branch | Purpose |
| --- | --- |
| `main` | Reviewed project files and documentation |
| `development` | Combining and checking team changes before adding them to `main` |
| `backend` | Work on backend components |
| `testing` | Audio detection and ranger interface work |

When a team member makes changes, they commit their work to a branch and open a **pull request**. Another teammate reviews the changed files, leaves comments if something needs fixing, and approves the PR when it is ready. The changes are then merged into the agreed branch. This helps us keep track of what changed and avoid accidentally replacing someone else's work.

The Project Manager coordinates the team's assignments and deliverables. The Configuration Manager helps keep the repository, branches, and version history organized. More detail is in our [Version Control Plan](docs/configuration/VERSION_CONTROL_PLAN.md).
