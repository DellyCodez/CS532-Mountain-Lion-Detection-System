# User Stories

## US-01 Receive Detection Alerts

I want to receive notifications of possible mountain lion activity so that I can review and respond to a detection.

Related requirements: FR-01 through FR-05.

## US-02 Classify Detections

I want to classify a detection as Definite, Suspected, or False so that the detection record reflects my assessment.

Related requirement: FR-06.

## US-03 Review Detection History and Reports

I want to request detection reports by date and classification, sensor location, park map, and classifying ranger so that I can analyze recorded activity.

Related requirements: FR-09 through FR-12; FR-07 and FR-08 provide supporting retention.


## Current Prototype Support

US-01: Audio input, preprocessing, BirdNET analysis and confidence filtering are reported Implemented. Full sensor input is Planned and alarm integration is Partially implemented.

US-02: Implemented in the current in-memory prototype; persistent history is not established.

US-03: Partially implemented for in-memory tabular reports; map reporting is Planned and persistent retention is Blocked by unfinished storage.

These are team-reported implementation states, not acceptance-test results.
