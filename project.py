# import tabula
from ics import Calendar, Event


# path = "sample.pdf"

# table = tabula.read_pdf(path, pages=1)

# print(table[0])

### create a New calendar and add events

c = Calendar()
e = Event()
e.name = "Work"
e.begin = '2023-10-13 10:00:00'
e.events.end = '2023-10-13 18:00:00'

c.events.add(e)
c.events

print(event)