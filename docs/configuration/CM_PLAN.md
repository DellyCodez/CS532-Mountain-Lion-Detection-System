# Configuration Management Plan

## Project
Mountain Lion Detection System

## Configuration Manager
Alexander Hills

## Configuration Management Tool
GitHub will be used to keep track of project files and software versions.

## Repository
CS532-Mountain-Lion-Detection-System

## Access
As of October 25, 2026, the repository is **public**, not private. Collaborator permissions are managed by the repository owner. The project manager/team should confirm whether public visibility is appropriate. Do not commit credentials, private information, or restricted data.

## Project Items Under Configuration Control
The project will keep track of:

- Requirements documentation
- Source code
- Design documentation
- Test information
- Configuration files
- Software versions and builds

## Engineering Library
The project repository will be used to organize and maintain the software and project information.

The library will contain the current project files and the history of software versions.

## Version Control
Software versions will be maintained throughout development.

Important project baseline versions will be kept so previous versions of the software can be identified when needed. The head of `main` is not automatically a formally approved release: for each deliverable, record the reviewed commit, included files, approvals, and any known missing items before calling it a baseline.

## Branch and Pull Request Controls (checked October 25, 2026)
- `main`: intended for reviewed integration and project snapshots.
- `development`: intended for ongoing integration before promotion to `main`.
- `backend` and `testing`: existing work branches; coordinate with their owners before changing or removing them.
- GitHub currently reports **`main` and `development` as protected**. The team configured pull-request review with one approval and conversation resolution, with force pushes and deletion disabled. Administrators may still have bypass permission unless separately restricted.
- Changes should be proposed through a focused task branch and a pull request. An independent teammate reviews before merge. Configuration changes are documented and significant requirement/test impacts are noted.
- `main` and `development` currently contain different work; do not overwrite either branch or merge unfinished components without a developer review.
- Deliverable #2 does **not** require a separate permanent `development-2` branch. Update this plan and the existing repository records for each milestone.

See [Version Control Plan](VERSION_CONTROL_PLAN.md) for the working procedure and [Deliverable 2 repository check](DELIVERABLE_2_REPOSITORY_CHECK.md) for evidence and open items.

## Change History
Changes to the software will be tracked so the team can identify what was changed during development.

Changes to controlled software should be reviewed and approved before the updated software is placed back into the controlled project files.

## Build Information
As development continues, the team will document:

- Build environment
- Build inputs
- Build procedure
- Build outputs

## Deliverable #2 Configuration Checks (October 25, 2026)
For the October 29 milestone, the Configuration Manager verifies the GitHub structure, branch and pull request status, configuration documentation, file locations, and availability of the latest reviewed project documents. The Project Manager coordinates the team plan and final submission; the Configuration Manager does not replace that plan.

The current repository check found:
- `docs/design/` contains a README but not a committed architecture diagram or database model on `main`.
- `docs/testing/` contains a README but not a committed test plan/cases on `main`.
- Requirements traceability and acceptance criteria still contain placeholders needing review by the requirements owner.
- Notebook, presentation, schedules, and timesheets may be maintained outside GitHub and have **not been verified** here.

Owners should provide a file/PR link, revision and review status to the Project Manager. CM records unresolved gaps rather than marking incomplete or external work finished. See [Deliverable 2 repository check](DELIVERABLE_2_REPOSITORY_CHECK.md).

**Document status:** Updated for Deliverable #2, pending review through a GitHub pull request. No formal milestone baseline or full-system test result is claimed.
