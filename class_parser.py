"""A simple parsing program."""
import math
from typing import List, Any
from typing_extensions import Self
from cs110 import expect, summarize
from dataclasses import dataclass

@dataclass
class LatLong:
    """A class to describe a location on the globe."""
    latitude: float   #  -90 to  90
    longitude: float  # -180 to 180
    
    def distance(self, other: Self) -> float:
        dist_lat = self.latitude - other.latitude
        dist_lon = self.longitude - other.longitude
        return math.sqrt(dist_lat ** 2 + dist_lon ** 2)


@dataclass
class BusStop:
    """A class to describe a Bus stop."""
    number: int
    connections: List[str]
    coordinates: LatLong


def strip_long(strings: List[str]) -> List[str]:
    """
    Purpose: strips whitespace from every string.
    Example:
        strip(["asdf\n", "  hello"]) -> ["asdf, "hello"]
    """
    output = []
    for string in strings:
        output.append(string.strip())
    return output


def strip(columns: List[str]) -> List[str]:
    """
    Purpose: strips whitespace from every string.
    Example:
        strip(["asdf\n", "  hello"]) -> ["asdf, "hello"]
    """
    return [c.strip() for c in columns]


def splitter(line: str, delimiter: str) -> List[str]:
    """
    Purpose: Splits a line based on a delimiter.
    Examples:
        splitter("number,connections,lat,long",             ",") -> ['number', 'connections', 'lat', 'long']
        splitter('51916,"[044,084]",49.273342,-123.239004', ",") -> ["51916","[044,084]","49.273342","-123.239004"]
    """
    chunks = []
    chunk = ""
    inside_quote = False
    for char in line:
        if char == "\"" and not inside_quote:
            inside_quote = True
            continue
        if char == "\"" and inside_quote:
            inside_quote = False
            continue

        if char == delimiter and not inside_quote:
            chunks.append(chunk)
            chunk = ""
        else:
            chunk += char
            
    chunks.append(chunk)
    return chunks

expect(splitter("number,connections,lat,long",             ","), ['number', 'connections', 'lat', 'long'])
expect(splitter('51916,"[044,084]",49.273342,-123.239004', ","), ["51916","[044,084]","49.273342","-123.239004"])

def parseLatLong(column: List[str], lat_index: int, long_index: int) -> LatLong:
    """
    Purpose: Creates a LatLong.
    Example:
        parseLatLong(["a","b","49.0","-129.0"], 2, 3) -> LatLong(latitude=49.0,longitude=-129.0)
    """
    lat  = float(column[lat_index])
    long = float(column[long_index])
    return LatLong(lat, long)

expect(parseLatLong(["a","b","49.0","-129.0"], 2, 3), LatLong(latitude=49.0,longitude=-129.0))


def parseConnections(conn: str) -> List[str]:
    """
    Purpose: To parse a connection column.
    Examples:
        parseConnections("[002,001]") -> ["002", "001"]
    """
    conn = conn.replace("[", "")
    conn = conn.replace("]", "")
    return conn.split(",")

expect(parseConnections("[002,001]"), ["002","001"])

def parseBusStop(column: List[str]) -> BusStop:
    """
    Purpose: to construct a BusStop
    Examples:
        parseBusStop(["01","[001,002]","49.0","-123.0"]) -> BusStop(1,["001","002"],LatLong(49.0,-123.0))
        
    """
    number = int(column[0])
    connections = parseConnections(column[1])
    latlong = parseLatLong(column, 2, 3)
    
    return BusStop(number, connections,latlong)

expect(parseBusStop(["01","[001,002]","49.0","-123.0"]), BusStop(1,["001","002"],LatLong(49.0,-123.0)))


if __name__ == "__main__":
    with open("stops.csv", 'r') as file:
        lines = file.readlines()
        stops = []
        for line in lines[1:]:
            # print(line)
            columns = splitter(line, ",")
            clean_columns = strip(columns)
            stops.append(parseBusStop(clean_columns))
    print(stops)
    summarize()