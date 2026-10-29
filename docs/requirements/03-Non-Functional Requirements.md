## Non-Functional Requirements

Implementation status reflects the current prototype and does not indicate successful acceptance testing.

### NFR-01 - Location accuracy
The animal detection system shall determine the location of
the detected noise with an accuracy of within 3 meters.

**Implementation Status:** Blocked — depends on unfinished sensor/localization integration. The required 3-meter accuracy remains open for validation.

### NFR-02 - Coverage
The animal detection system shall support sensors covering
an area of 5 square miles.

**Implementation Status:** Blocked — depends on unfinished sensor integration. The required 5-square-mile coverage remains open for validation.

### NFR-03 - Reconfigurability
The MLDS shall be designed so that it can be easily
reconfigured for use in other California parks.

**Implementation Status:** Partially implemented — park and application settings are configurable through environment variables; complete reconfiguration remains to be validated.
