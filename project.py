import tabula


path = "C:\Users\abmtz\Downloads\arbetizeit.pdf"

table = tabula.read_pdf(path, pages=1)

print(table[0])