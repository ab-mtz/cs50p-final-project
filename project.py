# imports
from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from uuid import uuid1
from pathlib import Path
import os
import pytz
 
# Import from table

# Extract and process info

# Save to calendar

### create a New calendar and add events
# init the calendar
cal = Calendar()

# Add properties
cal.add('prodid', '-//My calendar product//example.com//')
cal.add('version', '2.0')


# Add subcomponents
week_shifts = []

event = Event()
event.add('name', 'Schicht')
event.add('description', 'V')
event.add('dtstart', datetime(2023, 10, 14, 19, 10, 0, tzinfo=pytz.utc))
event.add('dtend', datetime(2023, 10, 14, 21, 0, 0, tzinfo=pytz.utc))

week_shifts.append(event)
for shift in week_shifts:
    cal.add_component(shift)

# Creatinga alarm

alert = 1
alarm = Alarm()
alarm.add('action', 'DISPLAY')

alert_time = timedelta(minutes=-int(alert))
alarm.add('trigger', alert_time)

cal.add_component(alarm)


# Store to file
 
f = open(os.path.join('example.ics'), 'wb')
f.write(cal.to_ical())
f.close()


