from csv_class_io import open_CSV, CSV
rows = open_CSV("stops.txt")
for row in rows[:4]:
    print(row[0:5])


