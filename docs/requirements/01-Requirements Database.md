# MLDS Requirements Database

## Overview

This document contains the requirements database for the Mountain Lion Detection System. The database is maintained by the development team and provides a central repository for tracking and managing system requirements throughout development.
The requirements will be reviewed, maintained, and updated as requirements are clarified or changed.

##

| ID | Functional Area | Source | Requirement Text | Priority | Allocation | Release / Increment | Design mapping information | Comments |
| -- | --------------- | ------ | ---------------- | -------- | ---------- | ------------------- | ---------------------------| -------- |
| FR-01 | Alert Processing | Customer Requirement 1 | The MLDS shall receive alert messages from the animal detection system. | TBD | Application Software | Proposed Increment 1 | Sensor Manager / Audio Identifier / Entry Manager | TBD | Initial requirement |
| FR-02 | Alert Processing | Customer Requirement 1 | The MLDS shall receive the detected noise type, noise strength, and location as part of each alert message. | TBD | Application Software | Proposed Increment 1 | Sensor Manager / Audio Identifier / Entry Manager | TBD | Initial requirement |
| FR-03 | Alarm | Customer Requirement 3 | The MLDS shall sound an alarm when an alert message is received. | TBD | Application Software | Proposed Increment 1 | Frontend / alarm-control logic | TBD | Initial requirement |
| FR-04 | Alarm | Customer Requirement 3 | The MLDS shall keep the alarm active until a park ranger turns it off. | TBD | Application Software | Proposed Increment 2 | Frontend / alarm-control logic | TBD | Initial requirement |
| FR-05 | Alarm | Customer Requirement 3 | After the alarm is turned off, the MLDS shall not sound the alarm again until another separate noise is detected at a different location. | TBD | Application Software | Proposed Increment 2 | Frontend / alarm-control logic | TBD | "Different location" requires clarification. |
| FR-06 | Classification | Customer Requirement 4 | The MLDS shall allow a park ranger to classify a mountain lion detection as Definite, Suspected, or False. | TBD | Application Software | Proposed Increment 2 | Frontend / Entry Manager / Database Interface | TBD | Initial requirement |
| FR-07 | Data Retention | Customer Requirement 2 | The MLDS shall retain all mountain lion alert information for 30 days. | TBD | Application Software | Proposed Increments 1 and 3 | Database Interface / retention processing | TBD | Initial requirement |
| FR-08 | Data Retention | Customer Requirement 2 | The MLDS shall retain summary information for alerts older than 30 days but received within one year. | TBD | Application Software | Proposed Increment 3 | Report Manager / Database Interface | TBD | "Summary information" requires clarification. |
| FR-09 | Reporting | Customer Requirement 5 | The MLDS shall allow a park ranger to request a report of detections by date and classification. | TBD | Application Software | Proposed Increment 3 | Frontend / Report Manager / Database Interface | TBD | Initial requirement |
| FR-10 | Reporting | Customer Requirement 5 | The MLDS shall allow a park ranger to request a report of detections by sensor location. | TBD | Application Software | Proposed Increment 3 | Frontend / Report Manager / Database Interface | TBD | Initial requirement |
| FR-11 | Reporting | Customer Requirement 5 | The MLDS shall provide a graphical report showing detections within the park and within two miles of the park. | TBD | Application Software | Proposed Increment 3 | Frontend / Report Manager / Database Interface | TBD | Initial requirement |
| FR-12 | Reporting | Customer Requirement 5 | The MLDS shall provide a report showing detections classified by each park ranger. | TBD | Application Software | Proposed Increment 3 | Frontend / Report Manager / Database Interface | TBD | Initial requirement |
| NFR-01 | Accuracy | Customer Requirement 1 | The animal detection system shall determine the location of the detected noise with an accuracy of within 3 meters. | TBD | Animal Detection System | External dependency; validation schedule pending | Animal Detection System | N/A | External system requirement |
| NFR-02 | Coverage | Customer Requirement 1 | The animal detection system shall support sensors covering an area of 5 square miles. | TBD | Animal Detection System | External dependency; validation schedule pending | Animal Detection System | N/A | Project outline references a 5-mile radius; clarification may be required. |
| NFR-03 | Reconfigurability | Customer Requirement 6 | The MLDS shall be designed so that it can be easily reconfigured for use in other California parks. | TBD | Application Software | External dependency; validation schedule pending | park configuration across affected components | TBD | Initial requirement |

