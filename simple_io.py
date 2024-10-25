demo_data = """column1,column2,column3
value1,value2,value3
"""
with open("demo.csv", 'w') as file:
        file.write(demo_data)
file.close()

type_data = """lat,lon
49.0,-123.0
49.1,-123.1
49.2,-123.2
"""

with open("type.csv", 'w') as file:
        file.write(type_data)
file.close()

print(f"\n{'-'*80}\n")

with open("demo.csv", 'r') as file:
    lines = file.readlines()
    for i in range(0, len(lines)):
        print(f"Line {i:>2}: {lines[i]}")

print(f"\n{'-'*80}\n")     

with open("demo.csv", 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(line.split(","))
    
    
print(f"\n{'-'*80}\n")

with open("demo.csv", 'r') as file:
    lines = file.readlines()
    for line in lines:
        print([value.strip() for value in line.split(",")])

print(f"\n{'-'*80}\n")

with open("type.csv", 'r') as file:
    rows = [line.strip().split(",") for line in file]
    print(rows)

print(f"\n{'-'*80}\n")

with open("type.csv", 'r') as file:
    rows = [line.strip().split(",") for line in file]
    floats = [[float(f) for f in row] for row in rows[1:]]
    print([rows[0]] + floats)
    

