## Functional Requirements

### FR-01 - Receive alert message
The MLDS shall receive alert messages from the animal detection system.

### FR-02 - Receive alert information
The MLDS shall receive the detected noise type, noise strength, and location.

### FR-03 -  Alarm activate
The MLDS shall sound an alarm when an alert message is received.

### FR-04 -  Alarm maintain
The MLDS shall keep the alarm active until a park ranger turns it off.

### FR-05 - Prevent duplicate alarm
After the alarm is turned off, the MLDS shall not sound the alarm
again until another separate noise is detected at a different location.

### FR-06 - Classify detection
The MLDS shall allow a park ranger to classify a mountain lion
detection as Definite, Suspected, or False.

### FR-07 - Store alert information
The MLDS shall retain all mountain lion alert information for 30 days.

### FR-08 - Store alert summary
The MLDS shall retain summary information for alerts older than
30 days but received within one year.

### FR-09 - Report by date and classification
The MLDS shall allow a park ranger to request a report of
detections by date and classification.

### FR-10 - Report by sensor location
The MLDS shall allow a park ranger to request a report of
detections by sensor location.

### FR-11 -  Report by graphical
The MLDS shall provide a graphical report showing detections
within the park and within two miles of the park.

### FR-12 - Report by ranger
The MLDS shall allow a report by each ranger.
