from project import check_arguments, extract_dates
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


    # ,
    #     "-",
    #     "05.02.23",
    #     "Mo",
    #     "30.01.23",
    #     "",
    #     "Di",
    #     "31.01.23",
    #     "",
    #     "Mi",
    #     "01.02.23",
    #     "",
    #     "Do",
    #     "02.02.23",
    #     "",
    #     "Fr",
    #     "03.02.23",
    #     "",
    #     "Sa",
    #     "04.02.23",
    #     "",
    #     "So",
    #     "05.02.23",
    #     "",
    # ]