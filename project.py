# imports
from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from uuid import uuid1
from pathlib import Path
import os, sys
import pytz

def main(): 
    # check arguments
    if not check_arguments(sys.argv):
        raise ValueError("Usage: project.py in_file.pdf out_file.ics")
    else:
        in_file = sys.argv[0]
        out_file = sys.argv[1]
   
    # Import from table

    # Extract and process info
    
    event_name = 'Arbeit'
    event_description = 'Verkauf'
    start_time = datetime(2023, 10, 15, 8, 0, 0, tzinfo=pytz.utc)
    end_time = datetime(2023, 10, 15, 10, 0, 0, tzinfo=pytz.utc)
    alert = 1
    events = [
        create_event(event_name, event_description, start_time, end_time, alert)
    ]

    create_and_save_calendar(events, out_file)
    # Save to calendar
def check_arguments(args):
    valid_extensions = ["pdf", "ics"]

    if len(args) == 3:
        args.pop(0)
    # Check extensions from args 1 and 2
        try:
            extensions = [file_name.split(".")[-1] for file_name in args]
            print(extensions)
            if extensions == valid_extensions:
                print("list are equals") 
                return True, extensions
        except: 
            return False
    else:
        return False
    ### create a New calendar and add events
def create_event(name, description, start_time, end_time, alert):
    event = Event()
    event.add('summary', name)
    event.add('description', description)
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    if alert:
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alert_time = timedelta(minutes=-int(alert))
        alarm.add('trigger', alert_time)
        event.add_component(alarm)
    return event

def create_and_save_calendar(events, out_file):
    # init the calendar
    cal = Calendar()

    # Add properties
    cal.add('prodid', '-//My calendar product//example.com//')
    cal.add('version', '2.0')

    for event in events:
        cal.add_component(event)
    # Store to file
    
    with open(out_file, 'wb') as file:
        file.write(cal.to_ical())

if __name__ == "__main__":
    main()


