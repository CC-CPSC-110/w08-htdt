"""A simple parsing program."""
from typing import List
from cs110 import expect, summarize

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


def strip(strings: List[str]) -> List[str]:
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

summarize()

if __name__ == "__main__":
    with open("stops.csv", 'r') as file:
        lines = file.readlines()
        for line in lines:
            # print(line)
            columns = splitter(line, ",")
            clean_columns = strip(columns)
            print(clean_columns)
