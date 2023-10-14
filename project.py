# imports
from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from uuid import uuid1
from pathlib import Path
import os
import pytz
 
# Import from table

# Extract and process info
def main():
    shift_data = 1
    alert_data = 1

# Save to calendar
### create a New calendar and add events
    # init the calendar
    cal = Calendar()

    # Add properties
    cal.add('prodid', '-//My calendar product//example.com//')
    cal.add('version', '2.0')
    shift = create_event(shift_data)
    cal.add_component(shift)
    alert = set_alarm(alert_data)
    cal.add_component(alert) 
    print(cal.content_lines)

    # directory = Path.cwd() / 'MyCalendar'
# try:
#    directory.mkdir(parents=True, exist_ok=False)
# except FileExistsError:
#    print("Folder already exists")
# else:
#    print("Folder was created")
 
 # Store to file
    try:
        f = open(os.path.join('example.ics'), 'wb')
        f.write(cal.to_ical())
        f.close()
    except:
        print("error saving file")
# Add subcomponents

def create_event(s):
    event = Event()
    event.add('name', 'Schicht')
    event.add('description', 'V')
    event.add('dtstart', datetime(2023, 10, 14, 19, 10, 0, tzinfo=pytz.utc))
    event.add('dtend', datetime(2023, 10, 14, 21, 0, 0, tzinfo=pytz.utc))
    return

    # Creatinga alarm
def set_alarm(a):
    # if alert:
    alert = a
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alert_time = timedelta(minutes=-int(alert))
    alarm.add('trigger', alert_time)
    return

# read from calendar

# e = open('MyCalendar/example.ics', 'rb')
# ecal = icalendar.Calendar.from_ical(e.read())
# for component in ecal.walk():
#    print(component.name)
# e.close()
# if __name__ == "__main__":
    main()