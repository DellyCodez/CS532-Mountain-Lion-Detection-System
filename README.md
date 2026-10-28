# CS 532 - Mountain Lion Detection System (NotFlock)

This is our team project for CS 532 Software Engineering at SDSU. We are working on a system that uses audio recordings to help California State Park rangers identify possible mountain lion activity.

The idea is to analyze sounds, flag possible detections, and give rangers a way to review alerts, classify them, and look at activity reports. **The project is still in development**, so not every feature is working together yet.

## What we have so far

- **Audio detection:** [`main.py`](main.py) contains an early Gradio demo that records audio through a microphone and uses BirdNET to check for possible mountain lion sounds.
- **Backend:** Additional backend work is being developed on the [`development` branch](../../tree/development).
- **Ranger interface:** Work on the alert and ranger interface is on the [`testing` branch](../../tree/testing) and is being reviewed in [pull request #9](../../pull/9).
- **Documentation:** We are keeping our requirements and project plans in the `docs` folder while the team works on the remaining parts.

The audio demo currently uses a locally configured model and file paths, so it is not a complete setup that will run on every computer without changes. We are still working on integration, testing, and getting the project files ready for review.

## Where to find the documents

| Folder | What's in it |
| --- | --- |
| [`docs/requirements`](docs/requirements/) | Requirements, user stories, use cases, acceptance criteria, and traceability |
| [`docs/configuration`](docs/configuration/) | Configuration Management Plan, Version Control Plan, and repository checks |
| [`docs/design`](docs/design/) | Design and architecture documents as they are added |
| [`docs/testing`](docs/testing/) | Test plans and results as they are added |
| [`docs/sdf`](docs/sdf/) | Software Development Folder materials |

Some folders may only have a README until the team's files are added or reviewed.

## How we use GitHub

We use `main` for reviewed project work, `development` to bring team changes together, and other branches for individual tasks. Team members open pull requests so changes can be reviewed before they are merged.

Our Project Manager coordinates the team schedule and final deliverables. GitHub is where we keep track of the code, documentation, and changes.

*Project status updated October 28, 2026.*
