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

# INPUTS: in_file, out_file, worker_name, alert
##### Check arguments

    if not check_arguments(sys.argv):
        raise ValueError("Usage: project.py in_file.pdf out_file.ics")
    else:
        in_file = sys.argv[0]
        out_file = sys.argv[1]
   
##### Import from table
    try:
        with pdfplumber.open(in_file) as pdf:
            page = pdf.pages[0]
            table = page.extract_table()
    except:
        print("PDF file not found")        
    
# Check if the pdf structure corresponds to the expected one
# presumably there are 25 cells per row in this file's structure 
    for row in table:
        if len(row) != 25:
            sys.exit("The pdf file can't be processed")
    # print rows
    # for row in table:
    #     line = ""
    #     line = ", ".join([str(cell).replace('\n', ' ') for cell in row])
    #     print(line +"\n")
    #     print(len(row))

    # Write results into a document to register and analize it for the next steps
    # with open("table_extract.txt", "w") as f:
    #     for row in table:
    #         line = ""
    #         line = ", ".join([str(cell).replace('\n', ' ') for cell in row])
    #         f.write(line + "\n") 


    filter_results(table, worker_name="Enrique")




##### Extract and process info
    # Create a Class????
    event_name = 'Arbeit' # constant
    event_description = 'Verkauf'
    utc = pytz.timezone('Europe/Berlin') # constant 
    date = (2023, 10, 15)
    start_time = (15, 30, 00)
    end_time = (17, 30, 00)
    start_datetime = datetime(*date, *start_time, tzinfo=utc)
    end_datetime = datetime(*date, *end_time, tzinfo=utc)
    alert = 1#Engloba lo anterior entregado por una funcion 
    

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


def filter_results(table, worker_name):
    ### Values to extract:
    # event_name = 'Arbeit' # constant
    # event_description = 'Verkauf'
    # utc = pytz.timezone('Europe/Berlin') # constant 
    # date = (2023, 10, 15)
    # start_time = (15, 30, 00)
    # end_time = (17, 30, 00)
    # start_datetime = datetime(*date, *start_time, tzinfo=utc)
    # end_datetime = datetime(*date, *end_time, tzinfo=utc)

    # Extract the header of the table
    header = table.pop(0)
    # This loops is used to see wich indexes contains the relevant info, so we can filter it later
    # for count, cell in enumerate(header):
    #     print(count, cell)
        
    info_indexes = [5, 8, 11, 14, 17, 20, 23]
    # print relevant indexes
    dates = []
    for _ in range(len(info_indexes)):
        dates.append(header[info_indexes[_]])
        print(header[info_indexes[_]])
    # print(header)
    table.pop(0) # Remove the second row wich is useless
    # print("Content: \n", table)


    ### create a New calendar and add events
def create_event(name, description, start_time, end_time, alert):
    event = Event()
    event.add('summary', name)
    event.add('description', description)
    event.add('dtstart', start_time)
    event.add('dtend', end_time)
    if alert:     # Think about corner cases: check_alert
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        valid_alert = alert if alert >= 0 else 0
        alert_time = timedelta(minutes=-int(valid_alert))
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


