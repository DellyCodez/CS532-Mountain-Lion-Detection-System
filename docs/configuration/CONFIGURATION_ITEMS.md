# Configuration Item Register — MLDS
**Inventory reviewed:** 2026-10-25 (GitHub state at review).  
**CM owner:** Alexander Hills. **Status:** Working register; not a formally approved baseline.

| Item ID | Item | Current repository location | Responsible role | Status |
| --- | --- | --- | --- | --- |
| CI-01 | Functional and nonfunctional requirements | `docs/requirements/` | Requirements lead | Initial content present |
| CI-02 | Acceptance criteria and requirements traceability | `docs/requirements/08-Acceptance Criteria.md`, `09-Traceability Matrix.md` | Requirements lead | Templates/incomplete |
| CI-03 | System architecture and interface design | `docs/design/` | Design lead / developer | README only on main; owner to upload |
| CI-04 | Database schema / ER diagram | `docs/design/` (planned) | Database lead | Not found on main |
| CI-05 | Sensor transport proof of concept | `development:backend/sensor.py`, `sensor_manager.py` | Development/integration | Prototype, not on main |
| CI-06 | BirdNET and microphone detection prototype | `main:main.py`, `test_model.py`, `training.py` | Development / design | Prototype, separate from backend |
| CI-07 | Audio model and training artifact | `main:mountain_lion_model_*.csv`, `mountain_lion_model_Labels.txt` | Audio owner | Metadata present; model binary absent from tracked main |
| CI-08 | Test plan, cases, results | `docs/testing/` | Test lead | README only on main |
| CI-09 | SDF / review and change evidence | `docs/sdf/` | PM + CM and respective owners | README only on main |
| CI-10 | CM procedures and change records | `docs/configuration/`, `.github/pull_request_template.md` | CM lead | Initial controls on main; expanded CM records in PR #5 pending review |
| CI-11 | Project plan, timesheets, Word notebook, presentation | PM-managed; cross-reference from `docs/sdf/` | Project manager | Not verified in repo; verify with PM |
| CI-12 | Runtime environment and dependencies | `docs/configuration/BUILD_RECORD.md` (planned record) | Development lead | Not reproducibly documented yet |

### Change rules
1. Maintain **one primary repository path** for each artifact; link instead of uploading competing copies.
2. Use a PR for significant artifact revisions and log the change's commit SHA.
3. Update this table when a missing item is first submitted or an owner/path changes.
4. Mark an item “approved” only with explicit team review and a baseline record.
5. Files for the current deliverable should be linked from their folder READMEs.
