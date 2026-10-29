# Acceptance Criteria

These criteria retain the current 15 requirements. They are not test results. Unresolved acceptance definitions must be confirmed before final acceptance.

## AC-001 FR-01

Implementation status: Partially implemented.

Status basis: Audio ingestion/preprocessing and BirdNET confidence filtering are reported working. The specified external sensor-alert/TCP interface remains planned.

Related requirement: FR-01. Related story: US-01. Related use case: UC-01.

Given an operating MLDS and a valid external alert, the alert is received.

Planned Test Plan reference: Pending detailed-case review: no explicit external-alert receipt row.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-002 FR-02

Implementation status: Partially implemented.

Status basis: Alert fields exist, but sound-strength input/automatic measurement and source-location integration remain incomplete. Confidence is not sound strength.

Related requirement: FR-02. Related story: US-01. Related use case: UC-01.

For a valid alert, noise type, sound strength, and detected-noise location match the transmitted values. Confidence must not substitute for sound strength.
Planned Test Plan reference: BRD-06.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-003 FR-03

Implementation status: Partially implemented.

Status basis: Standalone AlarmManager exists; connection to the current prototype flow and audible alarm behavior remain incomplete.

Related requirement: FR-03. Related story: US-01. Related use case: UC-01.

Given a valid alert eligible under FR-05, MLDS produces an audible alarm.

Planned Test Plan reference: CON-01, CON-02, CON-03, UI-01.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-004 FR-04

Implementation status: Partially implemented.

Status basis: Acknowledgement logic exists in AlarmManager; Ranger UI and persistent acknowledgement integration remain incomplete.

Related requirement: FR-04. Related story: US-01. Related use case: UC-01.

The alarm remains active until the ranger turns it off; it stops after that action.

Planned Test Plan reference: CON-04, UI-06.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-005 FR-05

Implementation status: Partially implemented.

Status basis: Location-separation logic exists; integration and approved definitions of separate noise/different location remain pending.

Related requirement: FR-05. Related story: US-01. Related use case: UC-01.

After shutoff, repeated noise at the same location does not reactivate the alarm. Another separate noise at a different location can reactivate it.

Planned Test Plan reference: CON-05.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-006 FR-06

Implementation status: Implemented.

Status basis: Team reports classification as working in the prototype, with ranger-name association; storage is in memory only.

Related requirement: FR-06. Related story: US-02. Related use case: UC-02.

Each permitted classification (Definite, Suspected, False) is recorded against the selected detection.

Planned Test Plan reference: UI-02, DAT-05.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-007 FR-07

Implementation status: Blocked.

Status basis: Full 30-day retention depends on unfinished persistent storage. Storage capability itself is planned.

Related requirement: FR-07. Related story: US-03 (supporting). Related use case: UC-03 (supporting).

All mountain-lion alert information received within the most recent 30 days is retained and retrievable. Confirm the time basis and exact boundary.

Planned Test Plan reference: DAT-01, DAT-02, DAT-06.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-008 FR-08

Implementation status: Blocked.

Status basis: Older-alert summaries depend on unfinished persistent storage and a defined summary structure/transition process.

Related requirement: FR-08. Related story: US-03 (supporting). Related use case: UC-03 (supporting).

Alerts older than 30 days but received within one year retain the agreed summary information.

Planned Test Plan reference: DAT-03, DAT-04.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-009 FR-09

Implementation status: Partially implemented.

Status basis: Date/classification reports operate on in-memory records. Required query/detail behavior and persistent history remain incomplete.

Related requirement: FR-09. Related story: US-03. Related use case: UC-03.

A report by date and classification returns the matching detections without unrelated records.

Planned Test Plan reference: UI-03, UI-07, UI-08.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-010 FR-10

Implementation status: Partially implemented.

Status basis: Sensor/location reporting exists for in-memory records. Specific-location selection and persistent history remain incomplete.

Related requirement: FR-10. Related story: US-03. Related use case: UC-03.

A report requested for a specific sensor location returns detections associated with that location.

Planned Test Plan reference: CON-07, UI-04, UI-08.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-011 FR-11

Implementation status: Planned.

Status basis: Map-point preparation exists, but the graphical park map and 2-mile surrounding-area behavior remain planned.

Related requirement: FR-11. Related story: US-03. Related use case: UC-03.

The graphical report shows detections on a park map and in the area within 2 miles of the park. Confirm the park boundary and distance rule.

Planned Test Plan reference: CON-07, UI-05.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-012 FR-12

Implementation status: Partially implemented.

Status basis: Ranger reporting operates on in-memory records. Persistent history and the explicit detailed test mapping remain pending.

Related requirement: FR-12. Related story: US-03. Related use case: UC-03.

The requested report correctly associates detection classifications with each classifying ranger.
Planned Test Plan reference: Pending.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-013 NFR-01

Implementation status: Blocked.

Status basis: Provisional dependency status: external sensor/localization integration and validation evidence are unfinished. Validation remains Open; no accuracy failure is inferred.

Related requirement: NFR-01. Related story: N/A - external constraint. Related use case: N/A.

Under agreed external-system validation conditions, detected-noise location error relative to reference locations is no more than 3 meters.

Planned Test Plan reference: Pending: no explicit 3-meter accuracy row.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-014 NFR-02

Implementation status: Blocked.

Status basis: Provisional dependency status: external sensor integration and coverage evidence are unfinished. Validation remains Open; conflicting area definitions remain unresolved.

Related requirement: NFR-02. Related story: N/A - external constraint. Related use case: N/A.

Agreed external-system evidence demonstrates support for sensor deployment across the customer-required 5-square-mile area.

Planned Test Plan reference: REC-01, REC-03, REC-04, REC-06.

Verification status: Not yet verified. Detailed test-case steps and results require review.

## AC-015 NFR-03

Implementation status: Partially implemented.

Status basis: Environment-based configuration exists, but complete deployment/reconfiguration criteria and persistence integration remain incomplete.

Related requirement: NFR-03. Related story: N/A - cross-cutting constraint. Related use case: N/A.

Using the agreed configuration procedure, MLDS is reconfigured for another California park and the required functions operate with that park configuration.

Planned Test Plan reference: REC-05.

Verification status: Not yet verified. Detailed test-case steps and results require review.

