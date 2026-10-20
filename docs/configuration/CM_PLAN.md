# Configuration Management Plan
## Mountain Lion Detection System — CS 532
**Configuration manager:** Alexander Hills  
**Working revision:** CM plan update proposed for Deliverable 2, October 2026  
**Tool:** Git and GitHub

### 1. Purpose and scope
Configuration management (CM) keeps the requirements, design documents, source code, testing evidence, and build information identifiable and recoverable. The goal is to know what version the team is using, what changed, who reviewed it, and which artifacts belong to each project deliverable.

### 2. Repository access
Repository: [DellyCodez/CS532-Mountain-Lion-Detection-System](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System). **Current verified visibility: public (2026-10-20).** Our previous plan incorrectly called it private. Whether to make it private is a team/project-manager decision; do not post credentials, personal information, or confidential customer information while it is public. Team members should use their own GitHub accounts so contributions remain attributable.

### 3. Configuration items
Controlled items are listed in [CONFIGURATION_ITEMS.md](CONFIGURATION_ITEMS.md), including:
- Customer and derived requirements, use cases, acceptance criteria, traceability
- Architecture, interface and database design
- Python source and supporting files
- Test plans, test cases, evidence and reports
- Model/dataset references and reproducible build inputs
- CM records, project notebook versions, and submitted milestone packages

Actual files have one primary location in the repository (see the register). Git commit IDs identify exact file versions. Avoid duplicate "final" documents.

### 4. Branches and change control
Use `main` for team-reviewed submissions/integration milestones; `development` for integration work; short-lived `feature/`, `fix/`, `docs/` or `cm/` branches for changes. See [VERSION_CONTROL_PLAN.md](VERSION_CONTROL_PLAN.md). A change request (GitHub issue or descriptive PR) should explain what changed, why, affected requirements/artifacts, and evidence of review. A teammate other than the author reviews each PR. The CM lead checks naming, file placement, baseline impact, and review status before merging approved changes. **Branch protection was not enabled as of 2026-10-20; documented policy is not yet technically enforced.**

### 5. Engineering library
Use `docs/requirements/`, `docs/design/`, `docs/testing/`, `docs/sdf/`, and `docs/configuration/`. Each owner uploads their editable artifact and adds a link in the relevant folder README. The project manager owns the final Word project notebook and Canvas submission; GitHub should contain enough version information and supporting evidence to trace the contents.

### 6. Baselines and releases
A baseline is a team-approved set of artifacts at a fixed commit SHA, not merely the latest branch head. Record approved versions in [BASELINE_REGISTER.md](BASELINE_REGISTER.md) with date, reviewer/approval, covered files, known limitations, and (after approval) tag/release identifier if one is created. **No formal approved baseline has been verified yet.** Do not label experimental code as a tested release.

### 7. Status accounting and audits
Maintain [CHANGE_LOG.md](CHANGE_LOG.md), [CONFIGURATION_ITEMS.md](CONFIGURATION_ITEMS.md), and the [Deliverable 2 checklist](DELIVERABLE_2_CHECKLIST.md). Before each milestone, check the branch/PR status, document locations, traceability, tests, reproducible build info, peer reviews, team hours, and notebook handoff. Record mismatches as open actions rather than silently marking them complete.

### 8. Build and release records
For each version to be demonstrated, developers provide the environment, exact dependency versions, model location/checksum if external, configuration, build/run steps, smoke-test evidence, and known issues. Record these in [BUILD_RECORD.md](BUILD_RECORD.md). Sensitive credentials and machine-specific paths must not be committed.

### 9. Responsibilities
- **Configuration manager (Alex):** maintain this plan, item/baseline/change registers, branches/PR process, artifact handoff checks.
- **Project manager (Lyvette):** schedule, timesheets, project plan and notebook/presentation submission.
- **Requirements lead (Hongzhen):** requirement changes, acceptance criteria and traceability.
- **Design lead (Victor):** architecture/interface artifacts and design reviews.
- **Development lead (Austin):** integration, implementation, environment and build procedure.
- **Database/QA lead (Bobby):** data model and QA review evidence.
- **Test lead (Caleb):** test plan/cases, execution evidence and defect records.

This plan describes proposed team practice until reviewed and accepted through the pull request.
