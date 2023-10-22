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
            "Zeitraum",
            "30.01.23",
            "-",
            "05.02.23",
            "Mo",
            "30.01.23",
            "",
            "Di",
            "31.01.23",
            "",
            "Mi",
            "01.02.23",
            "",
            "Do",
            "02.02.23",
            "",
            "Fr",
            "03.02.23",
            "",
            "Sa",
            "04.02.23",
            "",
            "So",
            "05.02.23",
            "",
        ],
        [
            "D-BY",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        [
            "Jarvis",
            None,
            None,
            None,
            "frei",
            None,
            None,
            "frei",
            None,
            None,
            "frei",
            None,
            None,
            "frei",
            None,
            None,
            "V 15:00-18:00\n2660_T06 - IN 18:00-19:00",
            None,
            None,
            "V 14:00-19:00",
            None,
            None,
            "frei",
            None,
            None,
        ],
        [
            "Enrique",
            None,
            None,
            None,
            "IN 10:00-18:00",
            None,
            None,
            "IN 10:00-16:15\nMG 16:15-18:00",
            None,
            None,
            "frei",
            None,
            None,
            "IN 11:15-19:15",
            None,
            None,
            "IN 10:00-18:00",
            None,
            None,
            "IN 11:15-19:15",
            None,
            None,
            "frei",
            None,
            None,
        ],
        [
            "Marina",
            None,
            None,
            None,
            "frei",
            None,
            None,
            "IN 16:15-19:15",
            None,
            None,
            "IN 13:30-19:15",
            None,
            None,
            "frei",
            None,
            None,
            "frei",
            None,
            None,
            "frei",
            None,
            None,
            "frei",
            None,
            None,
        ],
        [
            "Lena",
            None,
            None,
            None,
            "frei",
            None,
            None,
            "frei",
            None,
            None,
            "V 14:00-19:00",
            None,
            None,
            "frei",
            None,
            None,
            "V 14:00-19:00",
            None,
            None,
            "frei",
            None,
            None,
            "frei",
            None,
            None,
        ],
        [
            "Marco M.",
            None,
            None,
            None,
            "V 11:00-19:00",
            None,
            None,
            "V 11:15-18:00\nDG 18:00-19:15",
            None,
            None,
            "DG 09:00-10:30\nV 10:30-17:00",
            None,
            None,
            "2660_T06 - IN 10:00-11:15\nV 11:15-18:00",
            None,
            None,
            "frei",
            None,
            None,
            "V 11:00-19:00",
            None,
            None,
            "frei",
            None,
            None,
        ],
        [
            "Solveig",
            None,
            None,
            None,
            "DG 11:00-12:30\nV 12:30-19:00",
            None,
            None,
            "DG 09:00-10:30\nV 10:30-17:00",
            None,
            None,
            "2660_T06 - IN 10:00-13:30\nV 13:30-18:00",
            None,
            None,
            "frei",
            None,
            None,
            "V 11:00-17:30\nDG 17:30-19:00",
            None,
            None,
            "DG 09:00-10:30\nV 10:30-17:00",
            None,
            None,
            "abwesend",
            None,
            None,
        ],
        [
            "Andrea",
            None,
            None,
            None,
            "V 11:00-18:15\n2660_T06 - IN 18:15-19:15",
            None,
            None,
            "abwesend",
            None,
            None,
            "frei",
            None,
            None,
            "V 11:00-19:00",
            None,
            None,
            "abwesend",
            None,
            None,
            "V 10:00-18:00",
            None,
            None,
            "frei",
            None,
            None,
        ],
        [
            "Paula",
            None,
            None,
            None,
            "V 10:00-18:00",
            None,
            None,
            "V 11:00-17:30\nDG 17:30-19:00",
            None,
            None,
            "DG 09:00-10:30\nV 10:30-14:00\nM 14:00-16:00\nV 16:00-17:00",
            None,
            None,
            "abwesend",
            None,
            None,
            "frei",
            None,
            None,
            "2660_T06 - IN 10:00-11:15\nV 11:15-12:00\nM 12:00-15:00\nV 15:00-18:00",
            None,
            None,
            "frei",
            None,
            None,
        ],
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
