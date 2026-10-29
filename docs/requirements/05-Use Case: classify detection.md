## Use case: Classify Detection

**Primary Actor:** 
Park Ranger

**Precondition:** 
A mountain lion detection exists in the MLDS.

**Trigger:** 
The park ranger chooses to classify a detection.

### Main

1. The park ranger selects a mountain lion detection.
2. The MLDS presents the detection information.
3. The park ranger classifies the detection as definite, suspected, or false.
4. The MLDS records the selected classification.

**Postcondition:** 
The mountain lion detection has a recorded classification.

## Proposed Exception Handling

If the record cannot be found or saved, MLDS indicates that the classification was not completed. Confirm this exception behavior with software and test owners.

Persistent identity, history, and authentication design require confirmation. This use case does not independently introduce a login requirement.


## Implementation Status

Implemented in the current prototype, based on the team update: classification and ranger-name association use in-memory records. Persistent history and identity remain unverified.
