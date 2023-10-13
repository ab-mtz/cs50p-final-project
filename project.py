# imports
from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
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
event.add_component(event)

# Creatinga alarm

### working yet ###
alert = 20
if alert and unicode(alert).isnumeric()
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')

    alert_time = timedelta(minutes=-int(alert))
    alarm.add('trigger', alert_time)

    event.add_component(alarm)
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
