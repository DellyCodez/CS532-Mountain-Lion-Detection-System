# MLDS Requirements Management

## Overview

This directory contains the requirements for the Mountain Lion Detection System

The requirements are based on the customer-provided MLDS
requirements and will be maintained and updated throughout
development.

## Contents

- 01-Requirements Database.md: requirement register and clarification log.
- 02-Functional Requirements.md: functional requirement definitions.
- 03-Non-Functional Requirements.md: external constraints and reconfigurability.
- 04-User Stories.md: US-01 through US-03.
- 05 use case file: UC-02 Classify Detection.
- 06 use case file: UC-01 Receive Detection Alert.
- 07 use case file: UC-03 View Detection History and Reports.
- 08-Acceptance Criteria.md: AC-001 through AC-015.
- 09-Traceability Matrix.md: requirement, design, acceptance, and planned-test relationships.

## Implementation Status Definitions

- Implemented: reported to work in the current prototype; not equivalent to independently verified acceptance.
- Partially implemented: some functionality exists, but required behavior or integration is incomplete.
- Planned: designed or scoped, but the required behavior is not yet implemented.
- Blocked: fulfillment depends on unfinished database, sensor, or alarm integration, or another explicitly identified prerequisite.

Status assignments below incorporate the team update supplied by the Requirements Manager and the previously inspected code. They describe the current prototype, not the final product. Per-requirement assignments are a proposed translation of the team's capability-level update and require owner review. Verification is tracked separately. NFR-01/NFR-02 remain Open for validation; their Blocked labels describe unfinished dependencies, not failed tests.

Current coverage explicitly includes audio/sensor input, BirdNET/confidence filtering, alarm/acknowledgement/location rules, ranger classification, retention, all four report types, accuracy, coverage, and reconfigurability.
