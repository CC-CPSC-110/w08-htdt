# How to Design Tasks: Iteration
In this lecture, we will be learning how to `iterate` through a file and `parse` text into usable data classes.

Today we'll be working with real, live data from TransLink. You'll notice that some of the data is similar to what we've already been working with.

Go to [GTFS.org](https://gtfs.org/) for the general specification.
Go to [TransLink's data portal](https://www.translink.ca/about-us/doing-business-with-translink/app-developer-resources/gtfs/gtfs-data) for a data download.

I'm moving **recursion** to next class so we can talk about the midterm.

## Opening Files
Python makes opening and reading files relatively easy:
```python
f = open("demofile.txt")
```

This will open a file for reading. However, it doesn't really "look" like a file that you might be used to opening. First, you have to read the file. This means that the data that is in the file will be passed through and interpreted for display.

If you read the file in an interpreter, you'll see the contents:
```python
>>> f = open("demofile.txt")
>>> f.read()
'Hello, world!'
```

But if you read it again, you'll see nothing:
```python
>>> f.read()
''
```

That's because the file buffer has been exhausted. In other words, we have already read through all the data (as expressed in bytes) of the file. We would have to re-open the file if we wanted to read it again.

The more typical way to read a file is line by line. This is because most files have a **structure** to them, rather than just being full of arbitrary strings. One common file structure is *CSV* or [Comma-Separated Values] (https://en.wikipedia.org/wiki/Comma-separated_values). You can think of it like a spreadsheet but with commas between the values.

## CSV Format
All CSVs have values that are separated by commas. Typically, there is a header row followed by value rows.
```
column1,column2,column3
value1,value2,value3
```
| column1 | column2 | column3 |
|---------|---------|---------|
| value1  | value2  | value3  |
| value4  | value5  | value6  |


### Reading CSVs with Python
A common way to read CSVs looks like this:
```python
with open("demo.csv", 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(line)
```
The `with` manages errors and other resource problems.

### Writing CSVs with Python
A common way to write CSVs looks like this:
```python
demo_data = """column1,column2,column3
value1,value2,value3
"""
with open("demo.csv", 'w') as file:
        file.write(demo_data)
file.close()
```
The `with` manages errors and other resource problems.

### Splitting Lines
However, we usually want to access the data, so we want to split it into a list:
```python
with open("demo.csv", 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(line.split(","))

['column1', 'column2', 'column3\n']
['value1', 'value2', 'value3\n']
```

### List comprehensions
To get rid of any pesky extra whitespace, we will use a syntax called a **List Comprenesion**. It's basically a short way of writing a for-loop.
```python
with open("demo.csv", 'r') as file:
    lines = file.readlines()
    for line in lines:
        print([value.strip() for value in line.split(",")])


with open("demo.csv", 'r') as file:
    lines = file.readlines()
    rows = []
    for line in lines:
        for value in lines.split(","):
            rows.append(value.strip()
    print(rows)

['column1', 'column2', 'column3']
['value1', 'value2', 'value3']
```

### Simple Comprehensions
A comprehension applies some transformation to each item in a list.
```python
>>> nums = [1, 2, 3]
>>> doubles = [2 * n for n in nums]
>>> print(doubles)
[2, 4, 6]
```

### Worksheet Exercise 1
Take a moment to complete the first set of exercise questions.

## Parsing Types
Now that we have a way of splitting the lines, we will usually need to transform and interpret the data as particular types. Let's say we have a CSV of latitude-longitude values:

```python
lat,lon
49.0,-123.0
49.1,-123.1
49.2,-123.2
```

### Reading lines
We get a `List[List[str]]` when we print `rows`. But we want each value to be processed as a `float`.

```python
with open("type.csv", 'r') as file:
    rows = [line.strip().split(",") for line in file]
    print(rows)

[['lat', 'lon'], ['49.0', '-123.0'], ['49.1', '-123.1'], ['49.2', '-123.2']]
```

### Interpreting lines
But we want each value below the header to be processed as a `float`.

```python
with open("type.csv", 'r') as file:
    rows = [line.strip().split(",") for line in file]
    floats = [[float(f) for f in row] for row in rows[1:]]
    print([rows[0]] + floats)

[['lat', 'lon'], [49.0, -123.0], [49.1, -123.1], [49.2, -123.2]]
```

### How to Design Tasks: Data Design
Although the previous code "works", we want to use good data design principles to make our code easy to test, read, and generalize. Let's make a `LatLon` class:

```python
@dataclass
class LatLon:
    lat: float
    lon: float
```

### How to Design Tasks: Data Design
Now let's make a `CSV` class:

```python
@dataclass
class CSV:
    header: List[str]
    rows: List[Any]
```

### How to Design Tasks: Task Design
We should decompose our program into the smallest groups of tasks.

```python
def open_CSV(filename: str) -> List[List[str]]:
    with open(filename, 'r') as file:
        rows = [line.strip().split(",") for line in file]
        return rows

# Command Pattern
def parse_CSV(filename: str) -> CSV:
    csv = open_CSV(filename)
    header = csv[0]
    floats = [
        LatLon(float(row[0]), float(row[1])) 
            for row in csv[1:]
    ]
    return CSV(header, floats)

csv = parse_CSV("type.csv")
 
```


## Real-world example of a CSV

Go to TransLink's data portal at:

[https://www.translink.ca/about-us/doing-business-with-translink/app-developer-resources/gtfs/gtfs-realtime](https://www.translink.ca/about-us/doing-business-with-translink/app-developer-resources/gtfs/gtfs-data)

And click on **Download**.

You should get a copy of the latest static TransLink data. Unzip it and browse through the files. Although it may look confusing at first, we will slowly learn how to read and understand this data today.

## Browse the Data
First, let's see how we would import this data into Excel or Google Sheets. Open a browser and import the data from `stops.txt` into Google Sheets.

### Data preview
You should see something like this:

| stop_id | stop_code | stop_name                              | stop_desc | stop_lat  | stop_lon   | zone_id | stop_url | location_type | parent_station | wheelchair_boarding |
|---------|-----------|----------------------------------------|-----------|-----------|------------|---------|-----------|---------------|----------------|----------------------|
| 1       | 50001     | Westbound Davie St @ Bidwell St        |           | 49.286458 | -123.140424| BUS ZN  |           | 0             |                | 1                    |
| 10000   | 59326     | Northbound No. 5 Rd @ McNeely Dr       |           | 49.179962 | -123.09149 | BUS ZN  |           | 0             |                | 1                    |
| 10001   | 59324     | Northbound No. 5 Rd @ Woodhead Rd      |           | 49.18267  | -123.091448| BUS ZN  |           | 0             |                | 1                    |


### Raw data
Now, let's just look at the raw data:

```python
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,wheelchair_boarding
1,50001,Westbound Davie St @ Bidwell St,,49.286458,-123.140424,BUS ZN,,0,,1
10000,59326,Northbound No. 5 Rd @ McNeely Dr,,49.179962,-123.09149,BUS ZN,,0,,1
10001,59324,Northbound No. 5 Rd @ Woodhead Rd,,49.18267,-123.091448,BUS ZN,,0,,1
```
It looks confusing, but we can make sense of it.

### Header
This line is the header.
```python
stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,wheelchair_boarding
```
As you can see, it looks like the top row of a spreadsheet, but each column is separated by a comma.

### Row
This line is the row.
```python
1,50001,Westbound Davie St @ Bidwell St,,49.286458,-123.140424,BUS ZN,,0,,1
```
Each value corresponds to a column in the header.

### Use open_CSV()
We can use our previously-defined `open_CSV()` to look at our file:

```python
from csv_class_io import open_CSV
rows = open_CSV("stops.txt")
for row in rows[:4]:
    print(row[0:3])
```

### How to Design Tasks: Data Design
Let's look up what each of these mean. Go to [gtfs.org](https://gtfs.org/).
```python
['stop_id', 'stop_code', 'stop_name']
['1', '50001', 'Westbound Davie St @ Bidwell St']
['10000', '59326', 'Northbound No. 5 Rd @ McNeely Dr']
['10001', '59324', 'Northbound No. 5 Rd @ Woodhead Rd']
```


### How to Design Tasks: Data Design
We can start our `Stop` class with the data specification.
```python
@dataclass
class Stop:
    stop_id: str
    stop_code: str
    stop_name: str
```


### Exercise: Finish the Data Design for `Stop`
By looking up the rest of the columns, finish the class for `Stop`.

### Solution: Finish the Data Design for `Stop`
```python
@dataclass
class Stop:
    stop_id: str             # Unique ID of the stop
    stop_code: str           # Code identifier for the stop
    stop_name: str           # Name of the stop
    stop_desc: str           # Description of the stop
    stop_lat: float          # Latitude (-90 to 90)
    stop_lon: float          # Longitude (-180 to 180)
    zone_id: str             # Zone ID associated with the stop
    stop_url: str            # Valid URL 
    location_type: int       # Type of location
    parent_station: str      # ID of the parent station
    wheelchair_boarding: int # Accessibility level
```

### Enumerations
You might have noticed that some of the types have stronger specifications. We want to model that as well. 

Enumerations are used where we want to only have specific values.

```python
from enum import Enum
@dataclass
class LocationType(Enum):
    """Enum to define different location types for a stop."""
    STOP = 0       # Standard stop
    STATION = 1    # Station
    ENTRANCE = 2   # Entrance/exit
    GENERIC = 3    # Generic node
    BOARDING = 4   # Boarding area
```

### Exercise: Make an `Enum` for `wheelchair_boarding`
The other `Enum` in this list is `wheelchair_boarding`. Make an `Enum` for it.

### Solution: Make an `Enum` for `wheelchair_boarding`
```python
@dataclass
class WheelChairBoarding(Enum):
    INHERIT = 0        # Parentless means none, otherwise inherit
    ACCESSIBLE = 1     # Some accessible path or vehicles
    INACCESSIBLE = 2   # No accessible paths or vehicles
```

### Update the Data Design for `Stop`
```python
@dataclass
class Stop:
    stop_id: str                # Unique ID of the stop
    stop_code: str              # Code identifier for the stop
    stop_name: str              # Name of the stop
    stop_desc: str              # Description of the stop
    stop_lat: float             # Latitude (-90 to 90)
    stop_lon: float             # Longitude (-180 to 180)
    zone_id: str                # Zone ID associated with the stop
    stop_url: str               # Valid URL 
    location_type: LocationType # Type of location
    parent_station: str         # ID of the parent station
    wheelchair_boarding: WheelChairBoarding # Accessibility level
```

### Run `stop_parser.py`
Why do we care to do this? In the example file, you'll see I've made a database query function. We parse CSVs so that we can query the data. Try it out.

```python
query(stop_id="10003")
query(stop_code="50011")
query(stop_name="Westbound Davie St @ Bidwell St")
```

### Read `stop_parser.py`
You'll see that I've made some validation functions. You don't need to know how they work, but you should understand the input and output of them. We can update our `Stop` class to have more restricted types.

```python
@dataclass
class StopTyped:
    stop_id: str 
    stop_code: str
    stop_name: str
    stop_desc: str | None
    stop_lat: Latitude
    stop_lon: Longitude
    zone_id: str
    stop_url: URL | None
    location_type: LocationType
    parent_station: str
    wheelchair_boarding: WheelChairBoarding
```
