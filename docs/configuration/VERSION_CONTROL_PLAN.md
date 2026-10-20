# Version Control Plan
## Mountain Lion Detection System — CS 532
**Maintained by:** Alexander Hills (Configuration Management)  
**Source control:** GitHub

### Branch roles
| Branch | Intended use | Promotion |
| --- | --- | --- |
| `main` | Reviewed integration/submission snapshot; not proof every feature is done | Merge reviewed PRs; record milestone SHA |
| `development` | Combine and test changes before promotion | PR from feature branch; review before merge |
| `backend`, `testing` | Existing legacy/work branches; coordinate their integration, do not overwrite | Use reviewed PRs; retire only when owners agree |
| `feature/*`, `fix/*`, `docs/*`, `cm/*` | Short-lived work | PR to `development` or, for CM-only submissions, `main` as agreed |

### Required change procedure
1. Pull the latest target branch and create a clearly named working branch.
2. Make focused changes; do not commit virtual environments, secrets, private keys, temporary files, or giant datasets/model binaries. Where required, document how external artifacts can be obtained.
3. Commit with a clear explanation (examples: `docs: add architecture overview`, `fix: correct sensor payload parsing`).
4. Open a pull request using the repository PR template. Reference relevant requirement IDs, issues, affected documents, tests, and risks.
5. Obtain an independent team review. For behavior changes, attach a test result or explain why tests could not run. CM checks artifact/version tracking.
6. Resolve comments, merge using the agreed method, and record the result in the change log or release record.
7. For a milestone, record the approved `main` commit in the baseline register. Only then create a tag/release when authorized.

### Branch protection — action required
As of 2026-10-20, GitHub reports `main`, `development`, `backend`, and `testing` are unprotected, with no rulesets. Repository owner should configure **Settings > Rules > Rulesets** (or Branches, where applicable):
- Protect `main`: require pull requests and at least one approval; prevent force pushes and branch deletion.
- Protect `development`: require PR-based changes; use independent review where feasible.
- If team size/reviewer availability limits enforcement, document any exception rather than silently bypassing review.
- Add required status checks *after* reliable CI tests are available. Do not require a nonexistent CI check.
- Verify the rules are **active** on the repository plan; a configured but unenforced rule is not sufficient.

**This file documents the intended controls; it does not itself change GitHub settings.**

### Current integration concern (snapshot 2026-10-20)
`main` and `development` have diverged. GitHub comparison: `development` is two commits ahead and seven behind `main`; the `development` side includes sensor networking files not present in `main`. Plan the merge with Austin/Victor/Cesko and Caleb rather than force-pushing either branch. See [INTEGRATION_REGISTER.md](INTEGRATION_REGISTER.md).

### Naming and document versioning
- Use stable paths, for example `docs/design/architecture.md` and `docs/testing/test-plan.md`. Record the approved commit rather than appending `final-final-v2` to filenames.
- Changes to approved requirements need an updated traceability matrix and test impact review.
- Tag format proposed: `d2-2026-10-29` and `d3-2026-12-03`, **only after** team approval.
- PR history, [CHANGE_LOG.md](CHANGE_LOG.md), and [BASELINE_REGISTER.md](BASELINE_REGISTER.md) provide the traceable record.

### CM lead checklist for each pull request
- Correct target branch, descriptive title, reasonable scope
- Correct artifact path, no unexpected deletion or duplicate
- Requirement/test/design impact recorded
- Independent reviewer identified and review completed
- Build/test evidence or an explicit limitation
- Merge changes the correct baseline/register entries where needed
