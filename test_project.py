from project import (
    check_arguments,
    extract_dates,
    filter_results,
    extract_events,
    create_event,
)
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


def test_filter_results():
    table = [
        [
            "Zeitraum", "30.01.23", "-", "05.02.23", "Mo", "30.01.23", "",
            "Di", "31.01.23", "", "Mi", "01.02.23", "", "Do", "02.02.23", "",
            "Fr", "03.02.23", "", "Sa", "04.02.23", "", "So", "05.02.23", "",
        ],
        [
            "D-BY", None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None,
        ],
        [
            "Jarvis", None, None, None, "frei", None, None, "frei", None, None, "frei", None, None, "frei", None,
            None, "V 15:00-18:00\n2660_T06 - IN 18:00-19:00", None, None, "V 14:00-19:00", None, None, "frei", None, None,
        ],
        [
            "Enrique", None, None, None, "IN 10:00-18:00", None, None, "IN 10:00-16:15\nMG 16:15-18:00", None,
            None, "frei", None, None, "IN 11:15-19:15", None, None, "IN 10:00-18:00", None, None, "IN 11:15-19:15",
            None, None, "frei", None, None,
        ],
        [
            "Marina", None, None, None, "frei", None, None, "IN 16:15-19:15", None, None, "IN 13:30-19:15", None,
            None, "frei", None, None, "frei", None, None, "frei", None, None, "frei", None, None,
        ]
    ]
    _, result = filter_results(table, "Enrique")
    assert result == [
        "IN 10:00-18:00",
        "IN 10:00-16:15\nMG 16:15-18:00",
        "frei",
        "IN 11:15-19:15",
        "IN 10:00-18:00",
        "IN 11:15-19:15",
        "frei",
    ]


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
    assert result == ["IN 10:00-16:15", "MG 16:15-18:00"]
