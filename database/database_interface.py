import firebase_admin
from firebase_admin import db, credentials

# Establishes connection with firebase database file
# IMPORTANT  NOTE:: Firebase file can only store 1 MB of data
cred = credentials.Certificate("./service_key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://mountain-lion-project-database-default-rtdb.firebaseio.com/"
})

# Creates ranger entry in database, stores unique ID, name, and hash password for sign in, along with role
# @parameters
# username          - string \ Name of user to be created
# password_hash     - string \ password of user to be created, expected to be hashed before passed in as parameter
# role              - string \ defines role of user within application, i.e. Admin, head ranger, intern, blah blah blah
def create_ranger(username, password_hash, role):
    ref = db.reference("ranger").push()

    ref.set({
        "name": username,
        "password_hash": password_hash,
        "role": role
    })

# Retrieves ranger entry from database, expects password to be hashed before function is called
# @parameters
# username          - string \ Username of whoever is signing on
# password_hash     - string \ Password of user attempting to sign on, must be hashed before passed in as parameter
# @returns
# True/False        - boolean \ Returns true if valid sign in, false otherwise
def get_ranger(username, password_hash):
    ref = db.reference("ranger")
    results = (ref.order_by_child("name").equal_to(username).get())

    if results:
        id, data = next(iter(results.items()))

        if data["password_hash"] == password_hash:
            return True
        else:
            return False
    else:
        return False

# Adds sensor entry to database
# @parameters
# Latitude          - decimal \ I don't personally remember whether in python they're referred to as decimals or longs, in anycase Latitude value of sensor
# Longitude         - decimal \ Longitude value of sensor
# status            - string  \ Status of sensor, active and inactive
def create_sensor(latitude, longitude, status):
    ref = db.reference("sensor").push()
    sensor_id = ref.key

    ref.set({
        "sensor_id": sensor_id,
        "latitude": latitude,
        "longitude": longitude,
        "status": status,
        "last_seen": "NA"
    })

# returns sensor entry from database
# @parameters
# sensor_id         - string \ it is surprisingly annoying to set custom ids, actually I lied but I don't feel like setting it up,
#                            \ so the easiest way to actually call this function is to supply it with input via iterators or... no that's about it personally
#                            \ The intention here is that the sensors will preload to a dropdown or scroll bar in the frontend, and clicking one will
#                            \ retrieve it's ID if for some reason you need only ONE sesnor and not to see all of them
# @return
# data              - dictionary \ returns a dicitonary of all data within the entry, returns None otherwise
def get_sensor(sensor_id):
    results = db.reference(f"sensor/{sensor_id}").get()
    if results:
        return results
    else:
        return None
    
# updates values within sensor entry
# @parameters
# sensor_id         - string \ id of target sensor
# updates           - dicitonary \ a diciontary of updates with keys and values
def update_sensor(sensor_id ,updates):
    db.reference(f"sensor/{sensor_id}").update(updates)

# creates new alert entry within database
# @parameters
# sensor_id         - string \ still contemplating handling sensor ids manually but for now I won't.
# timestamp         - timestamp \ not sure if in python it's referred to as a timestamp or as a date, in anycase its the time the sound was caputred
# longitude         - decimal \ longitude value of the alerted sensor
# latitude          - decimal \ latitude value of the alerted sensor
# confidence        - decimal \ confidence value of the AI agent
# sound_file_path         - string \ path to stored soundfile, file stored locally, not within database
def create_alert(sensor_id, timestamp, longitude, latitude, confidence, sound_file_path):
    ref = db.reference("alerts").push()
    
    ref.set({
        "sensor_id": sensor_id,
        "timestamp": timestamp,
        "longitude": longitude,
        "latitude": latitude,
        "confidence": confidence,
        "sound_file_path": sound_file_path
    })

# retrieves alert from database to be processed
# @parameters
# alert_id          - string \ id of alert, just as before it is expected that this will be initially retrieved via an iterator
# @return
# data              - dictionary \ dictionary containing all data within alert entry, returns None otherwise
def get_alert(alert_id):
    results = db.reference(f"alerts/{alert_id}").get()

    if results:
        return results
    else:
        return None

# removes alert from database, usually done in conjunction with create_acknowledged_event()
# @parameters
# alert_id          - string \ id of alert
def remove_alert(alert_id):
    db.reference(f"alerts/{alert_id}").delete()

# creates an aknowledged event entry within database, these will be considered as the alert objects within the ER diagram
# @parameters
# alert_id          - string \ id of alert to be cataloged, the alert itself will be removed, but the data within it will be stored
# ranger_id         - string \ id of ranger who acknowledged alert
# classification    - string \ expected to be either confirmed, false alarm, or unsure
def create_acknowledged_event(alert_id, ranger_id, classification):
    ref = db.reference("acknowledged_events").push()
    alert_data = get_alert(alert_id)

    ref.set(alert_data)
    ref.update({
        "ranger_id": ranger_id,
        "classification": classification
    })
    remove_alert(alert_id)

# gets acknowledged event data from database
# @parameters
# event_id          - string \ id of event to be pulled
# @return
# data              - dictionary \ returns a dictionary of all data stored within event, returns None otherwise
def get_event(event_id):
    results = db.reference(f"acknowledged_events/{event_id}").get()
    if results:
        return results
    else:
        return None

# creates report object, a summary of all events selected, removes used alerts if the report is periodic, does not if it is manual
# @parameters
# start_time        - timestamp \ start time of report to be generated
# end_time          - timestamp \ end time of report to be generated
# report_type       - string    \ probably could be an ENUM, in anycase, states whether the report is manual or periodic
def create_report(start_time, end_time, report_type):
    ref = db.reference("acknowledged_events")

    results = (
        ref.order_by_child("timestamp")
        .start_at(start_time)
        .end_at(end_time)
        .get()
    )
    if not results:
        return None # Invalid timestamps, or no alerts between given timestamps
    
    alerts = list(results.values()) # extracts dictionary of alerts

    alerts_summary = {} # creates empty dictionary to store summary of alerts
    ranger_summary = {} # creates empty dictionary to store "classification by ranger"

    for alert in alerts:
        sensor_id = alert["sensor_id"]
        classification = alert["classification"]
        confidence = alert["confidence"]
        ranger_id = alert["ranger_id"]

        if ranger_id not in ranger_summary:
            ranger_summary[ranger_id] = {
                "detected": 0,
                "suspected": 0,
                "false": 0
            }

        if sensor_id not in alerts_summary: # prepares entry in alerts_summary to be placed in report
            alerts_summary[sensor_id] = {
                "longitude": alert["longitude"],
                "latitude": alert["latitude"],
                "total": 0,
                "detected": 0,
                "suspected": 0,
                "false": 0,
                "average_confidence": 0.0 # Sums through each iteration, divided by total on final pass before being saved
            }

        # Increments values of each sensor within alerts_summary, to be later used for a heatmap report
        entry = alerts_summary[sensor_id]
        entry["total"] += 1
        entry[classification] += 1
        entry["average_confidence"] += confidence

        # Increments classification rating of ranger, per ranger, so if ranger jimmy gets 5 detected and 2 suspected but Tommy got 2 detected and 0 suspected then its recorded as such
        ranger = ranger_summary[ranger_id]
        ranger[classification] += 1

    # Averages confidence
    for sensor_id, entry in alerts_summary.items():
        if entry["total"] > 0:
            entry["average_confidence"] = round(entry["average_confidence"] / entry["total"], 2)

    ref = db.reference("reports").push()

    ref.set(alerts_summary)
    ref.update(ranger_summary)

    # Deletes utilized entries, only on periodic reports
    if report_type == "periodic":
        delete_targets = {event_id: None for event_id in results.keys()}
        db.reference("acknowledged_events").update(delete_targets)

# gets report data from database
# @parameters
# report_id         - string \  id of report to be retrieved
# @return
# data              - dictionary \ dictionary of all data within selected report object, returns None otherwise
def get_report(report_id):
    results = db.reference(f"reports/{report_id}").get()
    if results:
        return results
    else:
        return None
