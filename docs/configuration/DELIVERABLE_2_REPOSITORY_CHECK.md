# Deliverable #2 — GitHub Repository Check
**Project:** CS 532 Mountain Lion Detection System (NotFlock)  
**Configuration Manager:** Alexander Hills  
**Checked:** October 25, 2026  
**Milestone:** Deliverable #2, October 29, 2026  
**Scope:** Files and branch/PR metadata committed to the GitHub repository. This is not an application test, an approval of the notebook, or a replacement for the Project Manager's project plan.

## GitHub organization and version control
| Check | Verified status |
| --- | --- |
| Repository | [DellyCodez/CS532-Mountain-Lion-Detection-System](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System), public |
| Branches | `main`, `development`, `backend`, `testing` |
| Protected branches | `main` and `development` report `protected: true` in GitHub. The team set PR review with one approval, conversation resolution, and disabled force pushes/deletion in the GitHub interface. Administrator bypass may remain possible. |
| Task branches | `backend` and `testing` remain unprotected work branches; this is not itself a release blocker |
| Existing CM files | `docs/configuration/CM_PLAN.md` and `VERSION_CONTROL_PLAN.md` present on `main` |
| Pull requests | PRs #1–#4 merged; PR #5 (earlier CM handoff proposal) closed **without merging** after the Project Manager took over the team plan |
| Integration risk | `development` is 2 commits ahead and 7 behind `main`. Development owners should review reconciliation, not force-merge or reset branches. |
| Formal milestone approval | No approved Deliverable #2 commit/baseline verified |

## Project document availability on `main`
| Required material | Checked location | Finding | Owner follow-up |
| --- | --- | --- | --- |
| System architecture and interfaces | `docs/design/` | README only; actual architecture/diagram not committed to `main` | Design/development leads provide versioned artifact or verified external link |
| Database model/ER diagram | `docs/design/` | No data model/ERD committed to `main` | Database lead supplies model and revision |
| Test plan and test cases | `docs/testing/` | README only; test plan/cases not committed to `main` | Test lead supplies plan and cases |
| Requirements traceability | `docs/requirements/09-Traceability Matrix.md` | Rows include `TBD` and `xx` placeholders | Requirements lead completes mapping |
| Acceptance criteria | `docs/requirements/08-Acceptance Criteria.md` | Criteria still have `xxx`, `XX`, and `...` placeholders | Requirements lead completes criteria |
| Notebook, schedule, presentation and time records | Project Manager-managed | Not verified in repository; files may be held elsewhere | Project Manager confirms source files and submission versions |

**Important:** "Not committed to `main`" does not establish that a teammate has not prepared work in another branch, locally, or in an external document. Record an external file only after confirming its accessible link and version.

## Configuration Manager follow-up
- [x] Verified repository organization, branch names and two protected branches.
- [x] Reviewed existing CM / Version Control Plans and corrected the stale repository-visibility statement in the proposed updates.
- [x] Reviewed PR history and documented the divergent integration branches.
- [x] Identified document availability and placeholder problems and recorded them here.
- [ ] Obtain independent PR review and merge updated CM documentation into protected `main`.
- [ ] Receive the latest artifact URLs/revisions from team leads and verify they match the final Project Notebook.
- [ ] Confirm with the Project Manager which deliverable documents were formally reviewed and accepted.
- [ ] Record exact approved milestone commit/revision and any unresolved exceptions at final handoff.

The Configuration Manager will coordinate file-version verification and report outstanding gaps. Team deliverables, schedule and submission decisions remain with the Project Manager and respective component leads.
