# PDF to ICS - Worktime Planning

Convert a PDF worktime plan into an ICS (iCalendar) file for easy integration with calendar apps.

## Overview

This Python program is designed to simplify the process of adding your work shifts to your calendar application. It works by extracting data from a PDF file containing your work schedule and creating an ICS (iCalendar) file that you can import into most calendar apps, such as Google Calendar, Apple Calendar, or Outlook.

## Usage

### Prerequisites

- Python 3
- Required Python libraries (install with `pip install pdfplumber icalendar`)

### Instructions

1. Clone or download this repository to your local machine.

2. Navigate to the project directory in your terminal.

3. Run the program with the following command, replacing `input_file.pdf` with your PDF file:
    python project.py input_file.pdf

4. You will be prompted to enter your name. This is used to generate an ICS file with your work shifts.

5. The program will process the PDF file, extract your work schedule, and create an ICS file.

6. Import the generated ICS file into your preferred calendar application.

## Notes

- The program is designed to work with specific PDF file structures. Make sure you use the correct PDF file format.

- The program includes a predefined list of shift codes and their corresponding descriptions. You can customize this list in the code to match your specific needs.

## Example

- An example ICS file is named as `{your_name}_start_date_end_date.ics`.

## Author

- Abraham Martinez - bmtzs@me.com

