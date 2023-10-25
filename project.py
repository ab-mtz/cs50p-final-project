from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
import os, sys
import pytz
import pdfplumber
import re

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
    "V": "Verkauf",
}
utc = pytz.timezone("Europe/Berlin")
event_description = "WORK"

# NEXT::: Description and Video

def main():
    # INPUTS: in_file, out_file, worker_name, alert
    # Check arguments
    if not check_arguments(sys.argv):
        raise ValueError("Usage: project.py input_file.pdf")
    else:
        in_file = sys.argv[0]

    # Prompt the user to introduce the worker's name
    worker_name = input("Name of worker: ")

    # Extract table from pdf
    try:
        with pdfplumber.open(in_file) as pdf:
            page = pdf.pages[0]
            table = page.extract_table()
    except:
        print("PDF file not found")

    ##### Check if the pdf structure corresponds to the expected one
    # presumably there are 25 cells per row in this file's structure

    #  Check the correct lenght of rows from pdf's table
    for row in table:
        if len(row) != 25:
            sys.exit(
                "The pdf file can't be processed, make sure to use the correct pdf file"
            )
    ##### print rows
    # for row in table:
    #     line = ""
    #     line = ", ".join([str(cell).replace('\n', ' ') for cell in row])
    #     print(line +"\n")
    #     print(len(row))

    ###### Write results into a document to register and analize it for the next steps
    # with open("table_extract.txt", "w") as f:
    #     for row in table:
    #         line = ""
    #         line = ", ".join([str(cell).replace('\n', ' ') for cell in row])
    #         f.write(line + "\n")

    """ Filter results from table """
    header, cells = filter_results(table, worker_name)

##### Extract and process info
    #  Extracting dates
    dates = []
    for i in range(5, len(header)):
        if extract_dates(header[i]):
            dates.append(extract_dates(header[i]))
        else:
            pass

    #  Extracting events contained per day
    day_events = []
    for cell in cells:
        day_events.append(extract_events(cell))
    
    if not any(day_events):
        sys.exit("----------- There are not events for this worker -----------")

    #  Per day: extracting events and creating events
    events = []
    for i in range(len(dates)):
        if day_events[i] != None:
            for ev in day_events[i]:
                #### extract name, start_time, end_time
                legende, times = ev.split(" ")
                # split times
                start, end = times.split("-")
                # convert the time string to tuple and add the seconds field
                start_time = tuple(map(int, start.split(":"))) + ((00),)
                # create a datetime obj to store the start of the event
                start_datetime = datetime(*dates[i], *start_time, tzinfo=utc)
                # convert the time string to tuple and add the seconds field
                end_time = tuple(map(int, end.split(":"))) + ((00),)
                # create a datetime obj to store the end of the event
                end_datetime = datetime(*dates[i], *end_time, tzinfo=utc)
                # Assing the event name from the legende
                event_name = abvs[legende]  #

                ##### Create event
                events.append(
                    create_event(
                        event_name,
                        event_description,
                        start_datetime,
                        end_datetime,
                        alert=5,
                    )
                )
    # build dates
    st_date = f"{dates[0][0]}-{dates[0][1]}-{dates[0][2]}"
    end_date = f"{dates[6][0]}-{dates[6][1]}-{dates[6][2]}"

    ### Create output file name
    out_file = f"{end_date}_{st_date}_{worker_name.capitalize()}.ics"

    # Save to calendar
    create_and_save_calendar(events, out_file)
    print(f"\n=========== The calendar has been successfully created and saved as '{out_file}' ===========")


#######################################


def check_arguments(args):
    """Check that a command-line argument is given and it's the name of a file wich extension is pdf"""
    valid_extensions = ["pdf", "PDF"]
    if len(args) == 2:
        args.pop(0)
        # Check extensions from arg 1
        try:
            _, extension = args[0].split(".")

            if extension in valid_extensions:
                return True
        except:
            return False
    else:
        return False


def filter_results(table, worker_name):
    """ Take the extracted table from the pdf file and extracts the header of the table and the row corresponding to the specified worker's name """
    _dates = []
    # name = worker_name
    start_times = []
    end_times = []
    event_description = ""

    # Extract the header of the table
    header = table.pop(0)
    # This loops was used to see wich indexes contains the relevant info, so we can filter it later
    # for count, cell in enumerate(header):
    #     print(count, cell)

    relevant_indexes = [5, 8, 11, 14, 17, 20, 23]
    # store content of relevant indexes in header to a list of tuples
    for _ in range(len(relevant_indexes)):
        tup_res = tuple(map(int, header[relevant_indexes[_]].split(".")))
        _dates.append(tup_res)

    table.pop(0)  # Remove the second row wich is useless

    # Extract values from cell that corresponds to the worker in question
    worker_row = []
    for worker in table:
        if worker[0].lower() == worker_name.lower():
            worker_row = worker
    if not worker_row:
        sys.exit("Worker name not found")

    # Filter and parse worker_row
    cells = []
    for cell in worker_row:
        if cell:
            if cell != worker_name:
                cells.append(cell)
    return header, cells


def extract_dates(cell):
    """ Search trough regex the matching date formatted information (DD.MM:YY) and returns the values YYYY, MM and DD as a tupple"""
    _match = ""
    if _match := re.findall(r"\d+\.\d+\.\d+", cell):
        # Date comes in format DD.MM.YY
        day, month, year = map(int, _match[0].split("."))
        year += 2000
        return year, month, day


def extract_events(cell):
    """ Extract the event or events contained in a cell as list """
    _omisions = ["abwesend", "frei"]
    if cell in _omisions:
        return None
    elif _match := re.findall(r"\w+\s\d{2}:\d{2}-\d{2}:\d{2}", cell):  
        return _match


# def all_none(day_events):
#    return not any(day_events)

def create_event(name, description, start_time, end_time, alert):
    """ Creates an event object with the information extracted from the table and processed by the other functions """
    event = Event()
    event.add("summary", name)
    event.add("description", description)
    event.add("dtstart", start_time)
    event.add("dtend", end_time)
    if alert:  # Think about corner cases: check_alert
        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        valid_alert = alert if alert >= 0 else 0
        alert_time = timedelta(minutes=-int(valid_alert))
        alarm.add("trigger", alert_time)
        event.add_component(alarm)
    return event


def create_and_save_calendar(events, out_file):
    """ Create a calendar object with the events and stores it as an ics file """
    # init the calendar
    cal = Calendar()

    # Add properties
    cal.add("prodid", "-//Created by Abraham Martinez//")
    cal.add("version", "2.0")

    for event in events:
        cal.add_component(event)
    # Store to file
    with open(out_file, "wb") as file:
        file.write(cal.to_ical())


if __name__ == "__main__":
    main()
