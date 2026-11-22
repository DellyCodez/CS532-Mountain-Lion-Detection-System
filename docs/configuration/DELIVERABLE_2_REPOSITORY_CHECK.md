# Deliverable #2 — Configuration Manager Repository Check

**Project:** CS 532 Mountain Lion Detection System (NotFlock)  
**Configuration Manager:** Alexander Hills  
**Checked:** October 28, 2026  
**Deliverable #2 due:** October 29, 2026 (per Project Manager's Requirements Outline – NotFlock)  
**Scope:** GitHub organization, branch/PR history, configuration documents and file availability **in the reviewed repository locations**. This is **not** Lyvette's project plan or a team-wide task-assignment tracker.

## What the Project Manager assigned to Configuration Management

| Project Manager's timeframe | CM check | Status / next action |
| --- | --- | --- |
| Deliverable #2 overall | Maintain GitHub organization, update branches and configuration documentation | Branches/CM files inspected; revised CM documents pending independent review in [PR #8](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/pull/8) |
| October 22–23 | Verify GitHub organization is current, documents are accurate and files are accessible | GitHub locations checked; unverified project artifacts noted below |
| October 24–28 | Confirm repository ready for review, latest documents/files available and gaps identified | PRs and repository contents reviewed October 28; report unresolved file/review gaps to Lyvette |

The Project Manager owns work assignments, schedule, project notebook, presentation, final coordination and submission. Design, requirements, database, software, test and QA owners remain responsible for producing and validating their own work. This check **does not** reassign them.

## GitHub configuration status (October 28)

| Item | Verified finding |
| --- | --- |
| Repository | [CS532-Mountain-Lion-Detection-System](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System), public |
| Branches | `main`, `development`, `backend`, `testing`, plus the temporary CM documentation branch |
| Branch protection | [Issue #7](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/issues/7) documents configured protection for `main` and `development`; do not bypass reviews |
| Integration | GitHub comparison: `development` is 2 commits ahead / 7 behind `main`; reconciliation needs development-lead review, not a force push |
| CM documentation | `docs/configuration/CM_PLAN.md` and `VERSION_CONTROL_PLAN.md` exist on `main`; corrected revisions proposed in [PR #8](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/pull/8), not merged |
| Active code review | [PR #9](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/pull/9) is open from `testing` to `main` and still needs the team to resolve its review/integration path |
| Approved Deliverable #2 baseline | **Not verified**; obtain exact accepted revision and Project Manager confirmation |

## Document availability on `main` (checked October 28)

| Location checked | Finding | CM action |
| --- | --- | --- |
| `docs/design/` | README only in this branch; architecture/design and database model not visible here | Request accessible current link/revision from the responsible owner or Project Manager; do not assert the work does not exist |
| `docs/testing/` | README only in this branch; test plan/cases not visible here | Request accessible current link/revision; do not interpret absence from `main` as failure to test |
| `docs/requirements/08-Acceptance Criteria.md` | The October 25 inspection found placeholders | Recheck the reviewed revision or obtain verified alternate copy |
| `docs/requirements/09-Traceability Matrix.md` | The October 25 inspection found placeholders | Recheck the reviewed revision or obtain verified alternate copy |
| Notebook, schedule, presentation, timesheets | Not independently verified in GitHub; may be maintained outside the repository | Ask the Project Manager for the reviewed versions, not a new GitHub task plan |

## CM handoff checklist (only CM-owned tasks)
- [x] Check existing branches and current integration status.
- [x] Review the repository's organization and the documentation visible in checked locations.
- [x] Update the existing CM and Version Control Plans to reflect the Project Manager's Deliverable #2 responsibilities (changes in PR #8).
- [x] Identify file-access and review gaps without marking other owners' work incomplete.
- [ ] Obtain independent review and authorized merge of PR #8.
- [ ] Confirm with the Project Manager the reviewed version or accessible link for any artifacts used in the final submission.
- [ ] Record the exact accepted milestone commit/version and known exceptions after approval.

**Important:** This is a CM verification record, not a replacement project plan, not a claim that other team members have missed their assignments, and not evidence of successful full-system testing. Team-wide assignments remain in Lyvette's Requirements Outline – NotFlock.
