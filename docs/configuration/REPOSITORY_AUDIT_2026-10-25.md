# Repository Configuration Audit — October 25, 2026
**Project:** CS 532 Mountain Lion Detection System (NotFlock)  
**CM lead:** Alexander Hills  
**Deliverable:** #2, due October 29, 2026  
**Basis:** Read-only inspection of GitHub branch metadata, the `main` and `development` tracked file trees, open PRs/issues, and current documentation. This is a **repository/document-control audit**, not a software functional test or an approval decision.

## 1. Executive status
**CM documentation prepared for review; milestone is not yet baselined or ready for sign-off.** Existing CM/VC plans were found on `main`. The expanded plans and registers are being prepared under [PR #5](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/pull/5). That PR has a reviewer requested but no submitted review recorded as of this audit. The audit does not certify that Deliverable 2 is complete.

## 2. Verified configuration-control findings
| Check | Observation, October 25 | Action / owner |
| --- | --- | --- |
| Repository | [DellyCodez/CS532-Mountain-Lion-Detection-System](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System), **public** | Lyvette/team decide if visibility is appropriate; do not commit private information |
| Branches | `main`, `development`, `backend`, `testing`, `cm/deliverable-2-controls` | CM records names and coordinates handoff; no extra D2 branch necessary |
| Branch protection | All five branches report `protected: false`; ruleset list empty | Repo owner/CM enable and verify protection; [issue #7](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/issues/7) |
| CM documents | Initial plans on `main`; enhanced registers/templates in open PR #5 | Independent teammate reviews and approves prior to merge |
| PR control | PRs #1–#4 merged; PR #5 open (CM documentation) | Record any later reviewed merge SHA in change log |
| Integration | `development` is 2 commits ahead and 7 behind `main` | Austin, Victor and backend contributor coordinate integration through a reviewed PR; no force push |
| Source/version | `main` at `d4daa89dcdbe2808818e92e1edd1fc462651b90f`; `development` at `3535c03618e06e88179c28def6f7ab63402704ab` | Baseline references only; **not team-approved releases** |
| Build inputs | Model metadata and Python scripts on `main`, sensor TCP proof of concept on `development`; `.tflite` binary absent from tracked `main` | Austin/Victor provide dependencies, model source and runnable instructions |
| Repository hygiene | Tracked `.idea/` local IDE settings and empty root file `To`; prior `.gitignore` excluded all PNG/JPG diagrams | CM proposes documented cleanup; this PR adjusts ignore rules to allow diagrams under `docs/`; do not remove others' tracked files without review |

## 3. Required D2 artifacts — observed repository status
| Artifact | Team owner | Evidence on `main` | Follow-up |
| --- | --- | --- | --- |
| System architecture, interface/components and ranger designs | Victor with Austin | `docs/design/README.md` only | Upload actual files/diagrams, give PR/link and reviewer |
| Database data model and ERD | Bobby | No ERD/data-model file under `docs/design/` | Add model, keys/relationships and version link |
| Test plan and numbered unit/integration cases | Caleb | `docs/testing/README.md` only | Upload plan/cases and expected results; do not mislabel them as executed |
| Final acceptance criteria and requirements traceability | Hongzhen | `08-Acceptance Criteria.md` contains `xxx`/`...`; `09-Traceability Matrix.md` contains `TBD`/`xx` | Replace placeholders with real requirement-to-test/design mappings |
| Updated project schedule, notebook, presentation, timesheets | Lyvette/team | Not verified in repository; may be held outside GitHub | Confirm editable files, exact revisions and Canvas submission responsibility |
| CM plan, version control, item/change/baseline/integration records | Alex | Proposed in [PR #5](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/pull/5) | Complete independent review and update status after merger |

These findings do **not** mean teammates have not worked locally or in other tools. Only committed repository artifacts were verified; ask owners for links instead of marking their work absent everywhere.

## 4. Configuration Manager verification performed
- [x] Inspected current repository tree and five branches.
- [x] Compared `main` and `development` and recorded integration gap.
- [x] Checked active branch flags and ruleset listing.
- [x] Examined PR #5 request and its review status.
- [x] Checked documentation placeholder folders and traceability entries.
- [x] Prepared updated D2 configuration-control documentation and handoff tracker.
- [ ] Independently approved PR #5 and merged into `main`.
- [ ] Confirmed branch protections actively enforced in repository settings.
- [ ] Verified actual design/database/test artifacts, with owner links and review evidence.
- [ ] Captured an approved D2 milestone commit, notebook revision, and release/baseline sign-off.

## 5. Submission handoff protocol
1. Each artifact owner posts an actual file path or external link plus commit/PR, review status, and unresolved gaps in [issue #6](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/issues/6).
2. CM confirms that the path exists in the reviewed branch, the filename/version matches the project notebook, and the review is recorded.
3. PM confirms the final Word notebook/presentation and each member's personal peer-review submission.
4. After formal team sign-off, CM captures the exact milestone commit and approval in [BASELINE_REGISTER.md](BASELINE_REGISTER.md). Do not tag an unfinished or unapproved version.

**Known limitation:** No reproducible end-to-end execution or test run was performed for this document audit. No branch-setting changes, teammate approvals, or external Canvas submissions are claimed.
