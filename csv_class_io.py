"""Example of a CSV parser."""
from dataclasses import dataclass
from typing import List, Any
from cs110 import expect, summarize

@dataclass
class LatLon:
    """
    Represents a geographical point with latitude and longitude coordinates.

    Attributes:
        lat (float): Latitude of the point.
        lon (float): Longitude of the point.

    Example:
        >>> point = LatLon(49.2827, -123.1207)
        >>> print(point)
        LatLon(lat=49.2827, lon=-123.1207)
    """
    lat: float
    lon: float


@dataclass
class CSV:
    """
    Represents the structure of a CSV file with a header and rows of data.

    Attributes:
        header (List[str]): The header row of the CSV file.
        rows (List[Any]): The rows of the CSV, containing LatLon objects.

    Example:
        >>> header = ["Latitude", "Longitude"]
        >>> rows = [LatLon(49.2827, -123.1207)]
        >>> csv_data = CSV(header, rows)
        >>> print(csv_data)
        CSV(header=["Latitude", "Longitude"], rows=[LatLon(lat=49.2827, lon=-123.1207)])
    """
    header: List[str]
    rows: List[Any]


def open_CSV(filename: str) -> List[List[str]]:
    """
    Opens a CSV file and reads its contents into a list of lists, where each inner list represents a row.

    Args:
        filename (str): The name of the CSV file to open.

    Returns:
        List[List[str]]: A list of rows, each represented as a list of strings.

    Example:
        Assuming `type.csv` contains:
        Latitude,Longitude
        49.2827,-123.1207

        >>> data = open_CSV("type.csv")
        >>> print(data)
        [["Latitude", "Longitude"], ["49.2827", "-123.1207"]]
    """
    with open(filename, 'r') as file:
        rows = [line.strip().split(",") for line in file]
        return rows


def parse_CSV(filename: str) -> CSV:
    """
    Parses a CSV file into a structured CSV object with a header and rows as LatLon objects.

    Args:
        filename (str): The name of the CSV file to parse.

    Returns:
        CSV: A CSV object with a header and LatLon instances as rows.

    Example:
        Assuming `type.csv` contains:
        Latitude,Longitude
        49.2827,-123.1207

        >>> parsed_data = parse_CSV("type.csv")
        >>> print(parsed_data)
        CSV(header=["Latitude", "Longitude"], rows=[LatLon(lat=49.2827, lon=-123.1207)])
    """
    csv = open_CSV(filename)
    header = csv[0]
    floats = [LatLon(float(row[0]), float(row[1])) for row in csv[1:]]
    return CSV(header, floats)

expect(open_CSV("type.csv"), [["lat", "lon"], ["49.0", "-123.0"], ["49.1", "-123.1"], ["49.2", "-123.2"]])
expect(parse_CSV("type.csv"), CSV(header=["lat", "lon"], rows=[LatLon(lat=49.0, lon=-123.0), LatLon(lat=49.1, lon=-123.1), LatLon(lat=49.2, lon=-123.2)]))
# summarize()