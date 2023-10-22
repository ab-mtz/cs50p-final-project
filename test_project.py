# from project.py import check_arguments


# def test_check_arguments():
#     args = ["project.py", "in_file.pdf"]
#     assert check_arguments(args) == True

#     args = ["project.py", "invalid.pdf"]
#     assert check_arguments(args) == False

import os
import pytest
from project import extract_dates, extract_events, create_event, create_and_save_calendar

# Define test cases for the extract_dates function
def test_extract_dates():
    date = "01.02.03"
    result = extract_dates(date)
    assert result == (2003, 2, 1)

    date = "15.06.23"
    result = extract_dates(date)
    assert result == (2023, 6, 15)

    date = "10.12.99"
    result = extract_dates(date)
    assert result == (2099, 12, 10)

# Define test cases for the extract_events function
def test_extract_events():
    cell = "Event 01: 09:00-12:00"
    result = extract_events(cell)
    assert result == ["Event 01: 09:00-12:00"]

    cell = "abwesend"
    result = extract_events(cell)
    assert result == None

    cell = "Event 02: 14:00-17:30\nEvent 03: 18:00-19:30"
    result = extract_events(cell)
    assert result == ["Event 02: 14:00-17:30", "Event 03: 18:00-19:30"]

# Define test cases for the create_event function
def test_create_event():
    name = "Sample Event"
    description = "This is a sample event"
    start_time = datetime(2023, 5, 15, 9, 0)
    end_time = datetime(2023, 5, 15, 12, 0)
    alert = 15

    event = create_event(name, description, start_time, end_time, alert)

    assert event.get("summary") == name
    assert event.get("description") == description
    assert event.get("dtstart").dt == start_time
    assert event.get("dtend").dt == end_time

# Define test cases for create_and_save_calendar function
def test_create_and_save_calendar(tmpdir):
    events = [create_event("Event 01", "Description 01", datetime(2023, 5, 15, 9, 0), datetime(2023, 5, 15, 12, 0), 15)]

    out_file = os.path.join(tmpdir, "test_calendar.ics")
    create_and_save_calendar(events, out_file)

    # Check if the file was created
    assert os.path.isfile(out_file)

    # Check if the file contains valid iCalendar data
    with open(out_file, "r") as f:
        ical_data = f.read()
    assert ical_data.startswith("BEGIN:VCALENDAR")

# # Run the tests
# if __name__ == '__main__':
#     pytest.main()
