from project import check_arguments
import pytest


def test_check_arguments():
    args = ["project.py", "in_file.pdf"]
    result = check_arguments(args)
    assert  result == True

    args = ["project.py", "in_file.txt"]
    result = check_arguments(args)
    assert result == False    
