## Use Case: View Detection History

**Primary Actor:** 
Park Ranger

**Precondition:** 
Detection information is available in the MLDS.

**Trigger:** 
The park ranger requests a detection report.

### Main Flow

1. The park ranger selects a report type.
2. The park ranger provides the information required for the selected report.
3. The MLDS retrieves the applicable detection information.
4. The MLDS generates the requested report.
5. The MLDS presents the report to the park ranger.

### Report Types

- Detection report by date and classification.
- Detection report by sensor location.
- Graphical detection report showing detections within the park and within two miles of the park.
- Report showing detections classified by each ranger.

**Postcondition:** 
The requested report is presented to the park ranger.
