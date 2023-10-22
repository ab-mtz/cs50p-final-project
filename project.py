# imports
from icalendar import Calendar, Event, vCalAddress, vText, Alarm
from datetime import datetime, timedelta
from uuid import uuid1
from pathlib import Path
import tabula
import os, sys
import pytz
import pdfplumber
import re

""" NEXT: """
# Arguments: add name arg and alarm arg
# Refactorize """per day"""
# wite test_ :\
# Correct format,
# Add comments to documentation
# Write instructions to google calendar 
# Think how to manage all calendars (from workers) in one calendar


def main():

    abvs = {
        "D": "Doublon",
        "DG": "Doublon Geschäft",
        "I": "Inventur",
        "IN": "Information",
        "IND": "Indi/HJG/EJG",
        "KA": "Kasse",
        "KP": "Kassenpermanenz",
        "LI": "Lieferzone",
        "M": "Mission",
        "MG": "Mission Geschäft",
        "P": "Permanenz",
        "PG": "Permanenz Geschäft",
        "TL": "TL",
        "U": "Umbau",
        "UG": "Umbau Geschäft",
        "V": "Verkauf"
    }
    utc = pytz.timezone('Europe/Berlin')

# INPUTS: in_file, out_file, worker_name, alert
##### Check arguments

    if not check_arguments(sys.argv):
        raise ValueError("Usage: project.py in_file.pdf out_file.ics")
    else:
        in_file = sys.argv[0]
        out_file = sys.argv[1]

    worker_name = input("Name of worker: ")
   
    """ Extract table from pdf """
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

    """ Filter results from table """
    header, cells = filter_results(table, worker_name)
   
##### Extract and process info
    """ Extracting dates """
    dates = []
    for i in range(5, len(header)):
        if extract_dates(header[i]):
            dates.append(extract_dates(header[i]))
        else:
            pass
    """ Extracting events contained per day """
    day_events = []
    for cell in cells:
        day_events.append(extract_events(cell))

    """ Per day: extracting events and creating events """
    events = []
    for i in range(len(dates)):
        if day_events[i] != None:
            for ev in day_events[i]:
    #### extract name, start_time, end_time
                legende, times = ev.split(" ")
                start, end = times.split("-")
                start_time = tuple(map(int, start.split(":"))) + ((00),)
                # start_datetime = datetime(*date, *start_time, tzinfo=utc)
                start_datetime = datetime(*dates[i], *start_time, tzinfo=utc) 
                end_time = tuple(map(int, end.split(":"))) + ((00),)
                end_datetime = datetime(*dates[i], *end_time, tzinfo=utc)
                event_name = abvs[legende]
                event_description = "Decathlon"
                # print("Legende: ", legende)
                # print("Start date time: ", start_datetime)
                # print("End date time: ", end_datetime)
                """ Create event """
                events.append(create_event(event_name, event_description, start_datetime, end_datetime, alert=5))

                
        #         # print("Parsed date: ", parsed_date)
        #         # start_datetime = date.

        #     print(event)
    
    # Manage multiple events per day
    # for e in day_events 
    # events = [
    #     create_event(event_name, event_description, start_datetime, end_datetime, alert)
    # ]

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
    
    dates = []
    # name = worker_name
    start_times = []
    end_times = []
    event_description = ""

    # Extract the header of the table
    header = table.pop(0)
    # This loops is used to see wich indexes contains the relevant info, so we can filter it later
    # for count, cell in enumerate(header):
    #     print(count, cell)

    relevant_indexes = [5, 8, 11, 14, 17, 20, 23]
    # store content of relevant indexes in header to a list of tuples
    for _ in range(len(relevant_indexes)):
        tup_res = tuple(map(int, header[relevant_indexes[_]].split(".")))
        dates.append(tup_res)
    
    # This method could work as well, we would need to add some filter with regex to get the relevant info
    # res =[]
    # for cell in header:
    #     if cell:
    #         res.append(cell)
    # print(res)
    
    table.pop(0) # Remove the second row wich is useless

    # Extract values from cell that corresponds to the worker in question
    worker_row = []
    for worker in table:
        if worker[0] == worker_name:
            worker_row = worker 
    if not worker_row:
        sys.exit("Worker name not found")
    # print(worker_row)
    # Filter and parse worker_row
    cells = []
    for cell in worker_row:
        if cell:
            if cell != worker_name:
                cells.append(cell)
    return header, cells


def extract_dates(cell):
    _match = ""
    if _match := re.findall(r"\d+\.\d+\.\d+", cell):
        # Date comes in format DD.MM.YY
        day, month, year = map(int, _match[0].split("."))
        year += 2000
      
        return  year, month, day
    

def extract_events(cell):
    #### NEXT: extract description, start_time, end_time
    
    _omisions = ["abwesend", "frei"]
    if cell in _omisions:
        return None    
    elif match := re.findall(r"\w+\s\d{2}:\d{2}-\d{2}:\d{2}", cell): #(\n.+\s.+[-].+)?(\n.+\s.+[-].+)?", cell):
        return match
    # print(matches)


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


