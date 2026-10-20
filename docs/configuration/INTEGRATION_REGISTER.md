# Branch and Integration Register — MLDS
**Checked:** 2026-10-20; **owner:** Configuration Management.

## Verified branch heads
| Branch | Head commit | Protection (at audit) | Current purpose |
| --- | --- | --- | --- |
| `main` | `d4daa89dcdbe2808818e92e1edd1fc462651b90f` | No | Audio/BirdNET prototype and project docs |
| `development` | `3535c03618e06e88179c28def6f7ab63402704ab` | No | Initial sensor networking/backend scaffolding |
| `backend` | `647ddde74719156ea3ee39bacf0e035fd8175a6f` | No | Existing backend experiment |
| `testing` | `6ae376b5585ae856b7bf9e72a6c511e1729aa71a` | No | Existing detection experiment |

These SHAs are dated references, **not live current heads**; refresh them before each milestone.

## Open integration work
- [ ] Austin / Victor / Cesko agree on sensor-to-detector payload, filenames, supported runtime, and error handling.
- [ ] Development owner reconciles `main` and `development` (currently diverged: two commits ahead and seven behind when comparing `development` against `main`).
- [ ] Integrate through a new branch/PR; **do not force-push, overwrite, or blindly merge**.
- [ ] Caleb records a smoke test covering a sample alert across the proposed components.
- [ ] Bobby verifies planned persistence/data-model contract; Hongzhen checks relevant requirements.
- [ ] Independent reviewer checks test evidence; CM records final merge commit.
- [ ] CM/PM update baseline register only after explicit review.

## Known portability blockers to escalate
- Existing prototype files refer to absolute paths on a developer's machine.
- Model `.tflite` binary is not tracked on `main`, so a fresh checkout cannot be assumed to reproduce the detection demo.
- Several backend modules are empty placeholders, including `database_interface.py` and `report_manager.py` on `development`.
- No complete working end-to-end application was verified in GitHub at this audit.

These are **open risks**, not an assertion that no one has worked locally. Owners should push completed work and give CM the branch, commit and PR URL.
