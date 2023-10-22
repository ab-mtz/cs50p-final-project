from project.py import check_arguments


def test_check_arguments():
    args = ["project.py", "in_file.pdf"]
    assert check_arguments(args) == True

    args = ["project.py", "invalid.pdf"]
    assert check_arguments(args) == False
