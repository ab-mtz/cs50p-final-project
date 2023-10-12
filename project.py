# import tabula
from ics import Calendar, Event


# path = "sample.pdf"

# table = tabula.read_pdf(path, pages=1)

# print(table[0])

### create a New calendar and add events
c = Calendar()
e = Event()
a = Alarm()
# 
def create_event(*ev):
    e.name = "Work"
    e.begin = '2023-10-13 10:00:00'
    e.end = '2023-10-13 18:00:00'
    a.trigger = '2023-10-13 9:30:00'
    # e.duration({"hours":8})


c.events.add(e, a)
# c.events
print(c)