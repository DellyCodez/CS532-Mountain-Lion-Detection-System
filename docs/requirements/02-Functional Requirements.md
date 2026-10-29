## Functional Requirements

### FR-01 - Receive alert message
The MLDS shall receive alert messages from the animal detection system.

**Implementation Status:** Partially implemented — audio input works; external sensor/TCP integration is planned.

### FR-02 - Receive alert information
The MLDS shall receive the detected noise type, noise strength, and location.

**Implementation Status:** Partially implemented — alert fields exist; sound-strength and source-location integration remain incomplete.

### FR-03 -  Alarm activate
The MLDS shall sound an alarm when an alert message is received.

**Implementation Status:** Partially implemented — alarm logic exists; application integration and audible output remain incomplete.

### FR-04 -  Alarm maintain
The MLDS shall keep the alarm active until a park ranger turns it off.

**Implementation Status:** Partially implemented — acknowledgement logic exists; integration with the ranger interface is pending.

### FR-05 - Prevent duplicate alarm
After the alarm is turned off, the MLDS shall not sound the alarm
again until another separate noise is detected at a different location.

**Implementation Status:** Partially implemented — location-based suppression logic exists; integration and rule clarification are pending.

### FR-06 - Classify detection
The MLDS shall allow a park ranger to classify a mountain lion
detection as Definite, Suspected, or False.

**Implementation Status:** Implemented — classification works in the current prototype using in-memory storage.

### FR-07 - Store alert information
The MLDS shall retain all mountain lion alert information for 30 days.

**Implementation Status:** Blocked — persistent 30-day retention depends on unfinished database integration.

### FR-08 - Store alert summary
The MLDS shall retain summary information for alerts older than
30 days but received within one year.

**Implementation Status:** Blocked — summary retention depends on unfinished persistence and summary processing.

### FR-09 - Report by date and classification
The MLDS shall allow a park ranger to request a report of
detections by date and classification.

**Implementation Status:** Partially implemented — reports use in-memory records; full reporting behavior remains incomplete.

### FR-10 - Report by sensor location
The MLDS shall allow a park ranger to request a report of
detections by sensor location.

**Implementation Status:** Partially implemented — sensor/location grouping exists; specific-location selection and persistent reporting remain incomplete.

### FR-11 -  Report by graphical
The MLDS shall provide a graphical report showing detections
within the park and within two miles of the park.

**Implementation Status:** Planned — graphical map reporting and park-boundary handling are not yet implemented.

### FR-12 - Report by ranger
The MLDS shall allow a report of detections classified by each ranger.

**Implementation Status:** Partially implemented — ranger reports use in-memory records; persistent reporting remains incomplete.
