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
