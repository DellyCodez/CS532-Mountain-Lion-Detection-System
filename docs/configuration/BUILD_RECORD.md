# Build, Runtime, and Release Record — MLDS

**Status as of 2026-10-20:** an end-to-end reproducible build has **not** been verified. This document lists required information; unchecked items are not completed evidence.

## Known repository inputs
- `main.py`, `training.py`, `test_model.py`: experimental audio detection files on `main`.
- `mountain_lion_model_Labels.txt`, `mountain_lion_model_Params.csv`, `mountain_lion_model_sample_counts.csv`: model metadata on `main`.
- `backend/sensor.py`, `backend/sensor_manager.py`: TCP proof-of-concept on `development`.
- Model `.tflite` file is ignored by `.gitignore` and absent from tracked `main` at the audit.
- Example audio and output under `backend/` and `results/` reflect experiments, not acceptance-test evidence.

## To be supplied by development / test owners
- [ ] Supported OS and Python version:
- [ ] Dependency/lock file and exact install command:
- [ ] Runtime configuration and required ports:
- [ ] External audio model/dataset source, version, integrity/checksum, licensing/access restrictions:
- [ ] Steps to run the prototype on a fresh checkout:
- [ ] Sample input and expected output:
- [ ] Smoke-test procedure, outcome, tester and date:
- [ ] Known unresolved problems:
- [ ] Version/commit SHA being demonstrated:
- [ ] Evidence link under `docs/testing/`:

## Release gate
No version should be called ready for demonstration until the build record identifies a runnable entry point, dependencies and required model inputs. Record test evidence and the approved commit in [BASELINE_REGISTER.md](BASELINE_REGISTER.md). Do not commit local environment paths, secrets, or private key files.
