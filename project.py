import tabula


path = "sample.pdf"

table = tabula.read_pdf(path, pages=1)

print(table[0])