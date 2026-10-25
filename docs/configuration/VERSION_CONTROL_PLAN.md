# Version Control Plan

## Project
Mountain Lion Detection System

## Version Control Tool
GitHub will be used to manage the project files and software versions.

## Main Branch
The `main` branch is intended for reviewed integration and milestone snapshots. Team members should not push unfinished work directly to `main`. A branch tip is not a formally approved deliverable unless the team has reviewed its exact contents.

## Development Branch
The `development` branch will be used for team development and integration before work is added to `main`.

## Branch Protection (verified October 25, 2026)
GitHub's branch listing reports both `main` and `development` as protected. The team created branch rules to:
- Require pull requests and one approving review before merging.
- Require pull-request conversations to be resolved.
- Disallow force pushes and deletion.
- Leave required CI status checks disabled until the team has reliable automated checks.

Administrators may still bypass rules unless administrator bypass is explicitly disabled. The Configuration Manager will recheck protection status before each milestone.

## Task Branches
Team members should use separate branches when working on features, fixes, or documentation changes. Branch names should clearly describe the work being completed.

Examples:
- `alerts`
- `database`
- `user-interface`
- `reports`
- `docs/cm-d2-refresh-2026-10-25` (temporary documentation update branch)

## Pull Requests
When work is ready to be added to the shared project, a pull request should be created so the changes can be reviewed before they are merged. Reference the affected files or requirements, explain any testing performed or why no test is applicable, and obtain independent approval. The PR author should not approve their own changes.

## Version History
GitHub will keep track of the project history through commits and previous versions. For a milestone, use the exact reviewed commit SHA plus the relevant artifact links rather than assuming that everything in the latest branch has been approved.

As of October 25, 2026, `main` and `development` have diverged: `development` is 2 commits ahead and 7 behind `main`. Development leads should reconcile those changes through reviewed integration work, without force pushes. Separate feature/testing branches can remain while their owners need them.

## Configuration Manager Responsibilities
As Configuration Manager, I will:

- Keep the repository organized
- Manage the branch structure
- Keep track of pull requests
- Help maintain the current project version

## Deliverable #2 Maintenance
No new permanent branch is required specifically for Deliverable #2. The CM lead updates the existing plans, checks the latest repository contents and PRs, and reports missing or unreviewed artifacts to the Project Manager. See [Deliverable 2 repository check](DELIVERABLE_2_REPOSITORY_CHECK.md).
