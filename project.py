# imports
from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from uuid import uuid1
from pathlib import Path
import os
import pytz

def main(): 
    # Import from table

    # Extract and process info
    out_path = 'cal_ex.ics'
    event_name = 'Arbeit'
    event_description = 'Verkauf'
    start_time = datetime(2023, 10, 15, 8, 0, 0, tzinfo=pytz.utc)
    end_time = datetime(2023, 10, 15, 10, 0, 0, tzinfo=pytz.utc)
    alert = 1
    events = [
        create_event(event_name, event_description, start_time, end_time, alert)
    ]

    create_and_save_calendar(events, out_path)
    # Save to calendar

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

def create_and_save_calendar(events, out_path):
    # init the calendar
    cal = Calendar()

    # Add properties
    cal.add('prodid', '-//My calendar product//example.com//')
    cal.add('version', '2.0')

    for event in events:
        cal.add_component(event)
    # Store to file
    
    with open(out_path, 'wb') as file:
        file.write(cal.to_ical())

if __name__ == "__main__":
    main()


