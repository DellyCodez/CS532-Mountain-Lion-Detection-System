# Configuration Management Plan

## Project and ownership
**Project:** CS 532 Mountain Lion Detection System (NotFlock)  
**Configuration Manager:** Alexander Hills  
**Tool and engineering library:** [GitHub repository](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System)

### Relationship to the Project Manager's plan
Lyvette's **Requirements Outline – NotFlock**, specifically its **Deliverable #2 (October 29, 2026)** responsibilities and October 22–28 schedule, is the authoritative **team work plan**. This document defines only how Configuration Management (CM) supports that plan. It does **not** reassign teammates, maintain a parallel schedule, or govern notebook/presentation submission.

The Project Manager coordinates team progress, deliverables, risks, schedule, final review and submission. The individual design, software, database, requirements, testing and QA owners prepare/review their assigned materials. CM verifies the GitHub repository, configuration documentation, accessible versions and change history, and reports missing or unreviewed files to the Project Manager.

## Deliverable #2: CM responsibilities from the Project Manager's plan
- **Throughout Deliverable #2:** maintain and update GitHub organization; update branches as needed; maintain configuration documentation.
- **October 22–23:** verify GitHub is organized and current, documentation is accurate, and relevant project files can be accessed.
- **October 24–28:** confirm the repository is ready for review, check that the latest project documents and files are available, and identify missing files.
- **At handoff:** give the Project Manager a brief repository status and links to the correct revisions; do not independently approve another owner's deliverable or claim that the team's final submission is complete.

## Items under configuration control
- Requirements and acceptance/traceability documentation.
- Architecture, interface and database design files.
- Source code, configuration, dependencies and build instructions.
- Test plans, test cases and recorded results where provided by the owners.
- Commit history, pull-request decisions and deliverable revision identifiers.

An item not yet present in the repository may exist locally, in another branch, or in a Project Manager-managed document. Record it as **not verified in the checked location**, not as unfinished work by the owner.

## Repository access and file organization
The repository is **public** as checked October 28, 2026. Collaborator access is administered by the repository owner. Avoid committing credentials, private data, machine-specific temporary files, or restricted assets. Keep project documentation in the relevant existing `docs/` folders; use reviewed external links when the Project Manager keeps an artifact elsewhere.

## Branch and change controls
- `main`: reviewed project integration and milestone snapshots, not automatically an approved final deliverable.
- `development`: team integration branch before proposed promotion to `main`, according to the existing Version Control Plan; any exception should be agreed with the Project Manager/development leads.
- `backend` and `testing`: existing work branches; preserve owners' unfinished work.
- `docs/cm-d2-refresh-2026-10-25`: temporary branch for the CM documentation updates in [PR #8](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/pull/8).

GitHub branch protection for `main` and `development` was documented in [issue #7](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/issues/7) on October 25. The configured workflow requires pull requests, at least one independent approving review and resolution of review conversations. Required automated CI checks have not been established. Admin bypass may remain possible; do not bypass the process just to merge.

Propose a focused change on an appropriate work branch, explain its effect and verification in a PR, receive an independent review, and merge only into the agreed integration target. **Do not create a separate permanent Deliverable #2 branch or a second project plan.** See [Version Control Plan](VERSION_CONTROL_PLAN.md).

## Configuration baselines and change history
Git commits and pull requests provide traceability; a branch tip alone is **not** an approved milestone baseline. At the approved handoff, record the exact commit/revision, links to the artifacts used by the Project Manager, reviewers/approval status and outstanding exceptions. Do not mark a baseline approved without that evidence.

## Build and environment records
As the software owners provide them, retain the supported environment, dependencies, build/run steps, inputs and outputs. CM checks their location and version; technical correctness and test execution belong to the responsible development/test roles.

## Current repository check
The [Deliverable #2 Repository Check](DELIVERABLE_2_REPOSITORY_CHECK.md) contains GitHub-only observations checked October 28, 2026. The listed gaps are **verification gaps on `main`**, not a new task schedule or assertions that team members have not worked on them.

**Status:** CM documents are revised in PR #8 and require independent review. Full Deliverable #2 acceptance, final submission and an approved milestone baseline are not claimed.
