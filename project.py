# imports
from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from uuid import uuid1
from pathlib import Path
import tabula
import os, sys
import pytz
import tkinter
import pdfplumber
# import camelot
# import ctypes
# from ctypes.util import find_library
# find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))


def main():
##### Check arguments
    if not check_arguments(sys.argv):
        raise ValueError("Usage: project.py in_file.pdf out_file.ics")
    else:
        in_file = sys.argv[0]
        out_file = sys.argv[1]
   
##### Import from table
    with pdfplumber.open(in_file) as pdf:
        page = pdf.pages[0]
        table = page.extract_table()
    # print rows
    for row in table:
        
        line = ", ".join([str(cell).replace('\n', ' ') for cell in row])
        print(line)

    with open("table_extract.txt", "w") as f:
        for row in table:
            line = ", ".join([str(cell).replace('\n', ' ') for cell in row])
            f.write(line) 
##### Extract and process info

    event_name = 'Arbeit'
    event_description = 'Verkauf'
    utc = pytz.timezone('Europe/Berlin')
    date = (2023, 10, 15)
    start_time = (15, 30, 00)
    end_time = (17, 30, 00)
    start_datetime = datetime(*date, *start_time, tzinfo=utc)
    end_datetime = datetime(*date, *end_time, tzinfo=utc)
    alert = 1
    events = [
        create_event(event_name, event_description, start_datetime, end_datetime, alert)
    ]

    # Save to calendar
    create_and_save_calendar(events, out_file)


#######################################

def check_arguments(args):
    valid_extensions = ["pdf", "ics"]

    if len(args) == 3:
        args.pop(0)
    # Check extensions from args 1 and 2
        try:
            extensions = [file_name.split(".")[-1] for file_name in args]
            if extensions == valid_extensions:
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
    cal.add('prodid', '-//Created by Abraham Martinez//')
    cal.add('version', '2.0')

    for event in events:
        cal.add_component(event)
    # Store to file
    
    with open(out_file, 'wb') as file:
        file.write(cal.to_ical())

if __name__ == "__main__":
    main()


