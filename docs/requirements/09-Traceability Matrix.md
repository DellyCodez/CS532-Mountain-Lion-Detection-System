# Requirements Traceability Matrix

Planned Tests summarizes the intended requirement-level checks; detailed test-case steps and results still require review. Implementation Status describes the current prototype and does not indicate successful acceptance testing. AC refers to 08-Acceptance Criteria.md.

| Requirement | User Story | Use Case | Design Component | Test Plan Requirement | Test Case | Planned Tests | Implementation Status | AC |
|---|---|---|---|---|---|---|---|---|
| FR-01 | US-01 | UC-01 | Sensor Manager / Audio Ingestion | Pending | Pending confirmation | Confirm receipt of a valid external sensor alert; detailed test mapping pending. | Partially implemented | AC-001 |
| FR-02 | US-01 | UC-01 | Sensor Manager / Detection & Alert Manager | Req-4 (partial) | BRD-06 (partial: probability is not sound strength) | Check noise type, sound strength, and detected-noise location; resolve probability/strength mismatch. | Partially implemented | AC-002 |
| FR-03 | US-01 | UC-01 | Alarm Manager / Ranger Control Platform | Req-7 | CON-01, CON-02, CON-03, UI-01 | Check alarm activation for an eligible received alert. | Partially implemented | AC-003 |
| FR-04 | US-01 | UC-01 | Alarm Manager / Ranger Control Platform | Req-8 | CON-04, UI-06 | Check that the alarm continues until ranger acknowledgement/shutoff. | Partially implemented | AC-004 |
| FR-05 | US-01 | UC-01 | Alarm Manager / Sensor and Location Processing | Req-9 | CON-05 | Check suppression after shutoff and reactivation for a separate noise at a different location; definitions pending. | Partially implemented | AC-005 |
| FR-06 | US-02 | UC-02 | Ranger Control Platform / Alert Service | Req-10 | UI-02, DAT-05 | Check Definite, Suspected, and False classifications and ranger association. | Implemented | AC-006 |
| FR-07 | US-03 (supporting) | UC-03 (supporting) | Database Interface / Persistent Storage | Req-5 | DAT-01, DAT-02, DAT-06 | Check complete alert retention within 30 days and persistence across restart; boundary definition pending. | Blocked | AC-007 |
| FR-08 | US-03 (supporting) | UC-03 (supporting) | Database Interface / Report Manager | Req-6 | DAT-03, DAT-04 | Check summary retention after 30 days and within one year; summary fields and boundaries pending. | Blocked | AC-008 |
| FR-09 | US-03 | UC-03 | Report Manager / Ranger Control Platform | Req-11 and Req-12 | UI-03, UI-07, UI-08 | Check reports by date and classification against known records. | Partially implemented | AC-009 |
| FR-10 | US-03 | UC-03 | Report Manager / Ranger Control Platform | Req-13 | CON-07, UI-04, UI-08 | Check reports for a selected sensor location. | Partially implemented | AC-010 |
| FR-11 | US-03 | UC-03 | Report Manager / Ranger Control Platform / Location Data | Req-14 | CON-07, UI-05 | Check graphical park-map detections and the surrounding 2-mile area. | Planned | AC-011 |
| FR-12 | US-03 | UC-03 | Report Manager / Ranger Control Platform | Not explicit | Pending confirmation | Check detection classifications by ranger; detailed test mapping pending. | Partially implemented | AC-012 |
| NFR-01 | N/A - external constraint | N/A | External Animal Detection and Sensor System | Not explicit | Pending confirmation | Compare detected-noise locations with reference positions against the 3-meter requirement; detailed test mapping pending. | Blocked | AC-013 |
| NFR-02 | N/A - external constraint | N/A | External Sensor System / Sensor Manager / Sensor Configuration | Req-1 | REC-01, REC-03, REC-04, REC-06 | Validate external sensor coverage of 5 square miles; reconcile conflicting area descriptions. | Blocked | AC-014 |
| NFR-03 | N/A - cross-cutting constraint | N/A | App Configuration / Sensor Manager / Modular Architecture | Req-15 | REC-05 | Check reconfiguration for another California park; measurable acceptance conditions pending. | Partially implemented | AC-015 |
