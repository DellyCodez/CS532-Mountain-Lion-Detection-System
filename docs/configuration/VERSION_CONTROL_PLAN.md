# Version Control Plan

## Project and authority
**Project:** CS 532 Mountain Lion Detection System (NotFlock)  
**Configuration Manager:** Alexander Hills  
**Version control:** GitHub

The Project Manager's **Requirements Outline – NotFlock** is the source of truth for Deliverable #2 responsibilities, schedule and submission. This plan specifies the CM-managed Git workflow; it does not replace Lyvette's assignments or create a separate team work plan.

## Branches
| Branch | Role |
| --- | --- |
| `main` | Reviewed integration and milestone reference. Do not directly push unfinished changes. |
| `development` | Shared development/integration before proposing a reviewed merge to `main`. |
| `backend`, `testing` | Existing working branches. Keep them intact until owners have completed their reviews and integration. |
| `docs/cm-d2-refresh-2026-10-25` | Temporary branch for CM documentation PR #8. |

New feature, fix and document branches may be created as needed; **no permanent `development-2` or other special Deliverable #2 branch is required**.

The existing development-to-main sequence is our repository workflow, **not an additional requirement stated in the Project Manager's outline**. If team leads approve a different integration route for a specific change, record it explicitly on the PR before merging.

## Pull-request workflow
1. The owner makes focused changes in a work branch and opens a PR against the agreed integration branch (normally `development` for unfinished/integration work).
2. The owner describes what changed, which files or requirements were affected, what was tested, and any limitations.
3. An independent teammate reviews the code/documents and requests corrections if necessary. Authors do not self-approve.
4. The owner addresses review comments and supplies evidence as appropriate; reviewers verify the latest revision.
5. Once approved, an authorized maintainer merges through GitHub. Promote integrated work to `main` only when the team agrees it is ready.
6. Record the relevant PR and commit for the deliverable. Do not bypass protection to accelerate a deadline.

## Branch protection
[Issue #7](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/issues/7) records the protection setup completed October 25, 2026 for `main` and `development`: pull requests, one approving review, resolved review conversations, and no force push/deletion. Automated status checks are not yet required; administrator bypass may still be possible. A protected branch does not mean all code is already verified.

## Current integration status (checked October 28, 2026)
GitHub comparison of `main` and `development` reports **diverged branches**: `development` is **2 commits ahead and 7 behind `main`**. Do not reset/force-push either branch. Development leads should review a controlled reconciliation.

[Victor's PR #9](https://github.com/DellyCodez/CS532-Mountain-Lion-Detection-System/pull/9) currently proposes changes from `testing` directly into `main`. Its target and requested revisions should be resolved with the owner before approval or integration. This document does not authorize changing his code or merging his PR without review.

## Version and baseline records
GitHub history preserves who changed what. For a deliverable, record:
- Exact commit SHA and branch used as the approved reference.
- Links to the actual project documents or approved external versions.
- PRs/reviewers and unresolved limitations.
- Project Manager confirmation of which revisions were used in the final submission.

Do not treat a README placeholder or a file on an unmerged branch as an approved submission artifact.

## Configuration Manager responsibilities for Deliverable #2
In the Project Manager's schedule, CM maintains GitHub organization/branches and configuration documentation; checks repository organization, accuracy and file access **October 22–23**; and confirms review readiness, current files and gaps **October 24–28**. The Project Manager owns the team's overall deadline, handoff and final review.

See [Configuration Management Plan](CM_PLAN.md) and [Deliverable #2 Repository Check](DELIVERABLE_2_REPOSITORY_CHECK.md).
