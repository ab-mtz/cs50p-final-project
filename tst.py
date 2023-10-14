from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
import pytz
import os

def create_event(summary, description, start_time, end_time, alarm_minutes=0):
    event = Event()
    event.add('summary', summary)
    event.add('description', description)
    event.add('dtstart', start_time)
    event.add('dtend', end_time)

    if alarm_minutes > 0:
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('trigger', timedelta(minutes=-alarm_minutes))
        event.add_component(alarm)

    return event

def create_and_save_calendar(events, output_file):
    cal = Calendar()
    cal.add('prodid', '-//My calendar product//example.com//')
    cal.add('version', '2.0')

    for event in events:
        cal.add_component(event)

    with open(output_file, 'wb') as f:
        f.write(cal.to_ical())

if __name__ == "__main__":
    # Define your events here
    events = [
        create_event('Event 1', 'Description 1', datetime(2023, 10, 15, 8, 0, 0, tzinfo=pytz.utc), datetime(2023, 10, 15, 10, 0, 0, tzinfo=pytz.utc), alarm_minutes=15),
        create_event('Event 2', 'Description 2', datetime(2023, 10, 16, 14, 0, 0, tzinfo=pytz.utc), datetime(2023, 10, 16, 16, 0, 0, tzinfo=pytz.utc)),
    ]

    create_and_save_calendar(events, 'example2.ics')
