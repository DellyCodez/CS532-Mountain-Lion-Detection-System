## Use case: Receive Detection Alert

**Primary Actor:** 
Park Ranger

**Supporting Actor:** 
Animal Detection System

**Precondition:** 
The MLDS control program is operating and able to receive alert messages.

**Trigger:** 
The MLDS receives an alert message from the animal detection system.

### Main

1. The animal detection system sends an alert message to the MLDS.
2. The MLDS receives the alert message.
3. The MLDS sounds an alarm.
4. The park ranger reviews the alert.
5. The park ranger turns off the alarm.
6. The MLDS stops the alarm.

**Postcondition:** 
The alarm is turned off, and the alert has been received by the MLDS.


The phone/BirdNET prototype boundary and treatment of alerts received while the alarm is suppressed require confirmation.


## Prototype Input and Implementation Status

The prototype ingests/preprocesses recorded or uploaded audio and runs BirdNET with configured confidence filtering; these capabilities are reported Implemented. They support the external-system simulation rather than proving the final external alert interface.

This end-to-end use case is Partially implemented: sensor/TCP integration is Planned and alarm activation/acknowledgement integration is incomplete. Validate threshold boundaries without equating confidence to sound strength. Keep the separate-noise/different-location rule after acknowledgement; no time-only exception is approved here.
