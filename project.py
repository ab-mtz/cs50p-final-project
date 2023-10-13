# imports
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import pytz
 
# init the calendar
cal = Calendar()

# Add properties
cal.add('prodid', '-//My calendar product//example.com//')
cal.add('version', '2.0')

### create a New calendar and add events

# Add subcomponents
event = Event()
event.add('name', 'Work')
event.add('description', 'V')
event.add('dtstart', datetime(2023, 10, 14, 9, 0, 0, tzinfo=pytz.utc))
event.add('dtend', datetime(2023, 10, 14, 19, 0, 0, tzinfo=pytz.utc))

# 
# def create_event(*ev):
#     e.name = "Work"
#     e.begin = '2023-10-13 10:00:00'
#     e.end = '2023-10-13 18:00:00'
#     a.trigger = '2023-10-13 9:30:00'
#     # e.duration({"hours":8})
cal.add_component(event)
# c.events

# Write to disk
directory = Path.cwd() / 'MyCalendar'
try:
   directory.mkdir(parents=True, exist_ok=False)
except FileExistsError:
   print("Folder already exists")
else:
   print("Folder was created")
 
f = open(os.path.join(directory, 'example.ics'), 'wb')
f.write(cal.to_ical())
f.close()

# read from calendar

# e = open('MyCalendar/example.ics', 'rb')
# ecal = icalendar.Calendar.from_ical(e.read())
# for component in ecal.walk():
#    print(component.name)
# e.close()
