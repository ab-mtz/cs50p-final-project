from project import check_arguments, extract_dates, extract_events, create_event
import pytest


def test_check_arguments():
    args = ["project.py", "in_file.pdf"]
    result = check_arguments(args)
    assert result == True

    args2 = ["project.py", "in_file.txt"]
    result2 = check_arguments(args2)
    assert result2 == None

    args3 = ["project.py", "in_file.pdf", "extra_argument.txt"]
    result3 = check_arguments(args2)
    assert result3 == False


def test_extract_dates():
    cell = "30.01.23"
    result = extract_dates(cell)
    assert result == (2023, 1, 30)
    
    cell = "05.02.23"
    result = extract_dates(cell)
    assert result == (2023, 2, 5)


def test_extract_events():
    cell = "IN 10:00-16:15\nMG 16:15-18:00"
    result = extract_events(cell)
    assert result == ['IN 10:00-16:15', 'MG 16:15-18:00']

def test_create_event():
    name = "Test Event"
    description = "This is a test event with an alert."
    start_time = datetime(2023, 10, 22, 10, 0)
    end_time = datetime(2023, 10, 22, 11, 0)
    alert = 15  # 15 minutes before the event
    event = create_event(name, description, start_time, end_time, alert)
    assert event["summary"] == name
    assert event["description"] == description
    assert event["dtstart"].dt == start_time
    assert event["dtend"].dt == end_time
    assert "VALARM" in event  # Alarm should be added
    alarm = event.walk("VALARM")[0]
    assert alarm["action"] == "DISPLAY"
    assert alarm["trigger"].dt == (start_time - timedelta(minutes=alert))