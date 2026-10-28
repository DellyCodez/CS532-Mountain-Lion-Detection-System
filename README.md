# NotFlock - Mountain Lion Detection System

**CS 532 Software Engineering | San Diego State University**

NotFlock is a team project focused on helping California State Park rangers monitor possible mountain lion activity using sound detection. The system is designed to analyze audio, send alerts when a possible mountain lion sound is detected, and give rangers a way to review and track those detections.

## Main Features

- **Audio detection:** Analyze recordings for possible mountain lion sounds.
- **Detection alerts:** Provide information such as the sound type, strength, and location.
- **Ranger classification:** Allow rangers to mark detections as Definite, Suspected, or False.
- **Detection history:** Keep records of alerts and ranger classifications.
- **Reports:** View detection activity by date, sensor location, or ranger.

## How It Works

1. An audio recording is captured by a sensor or submitted for analysis.
2. The detection system analyzes the sound for possible mountain lion activity.
3. A possible detection is sent to the ranger system as an alert.
4. Rangers review and classify the alert.
5. Detection records can be used to generate reports.

## Technologies

The project uses **Python** for development, with **BirdNET** for audio analysis and **Gradio** for the audio interface.

## Repository Structure

| Location | Contents |
| --- | --- |
| [`main.py`](main.py) | Python audio detection application |
| [`docs/requirements/`](docs/requirements/) | Functional and non-functional requirements, use cases, and traceability |
| [`docs/design/`](docs/design/) | System architecture and interface design documentation |
| [`docs/testing/`](docs/testing/) | Test documentation |
| [`docs/configuration/`](docs/configuration/) | Configuration Management and Version Control Plans |
| [`docs/sdf/`](docs/sdf/) | Software Development Folder documentation |

---

*CS 532 Software Engineering team project — SDSU*
