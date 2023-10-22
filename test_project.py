from project import check_arguments
import pytest


def test_check_arguments():
    args = ["project.py", "in_file.pdf"]
    result = check_arguments(args)
    assert  result == True

    args2 = ["project.py", "in_file.txt"]
    result2 = check_arguments(args2)
    assert result2 == None    

    args3 = ["project.py", "in_file.pdf", "extra_argument.txt"]
    result3 = check_arguments(args2)
    assert result3 == False    
    
def test_filter_results():
    with 