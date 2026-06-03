""" SimpleCL parser

Following the intuitive rules, this is a reference parser. (Formal rules TBD)

This simple python script demonstrates the simplicity of the notation for parsing.
"""


import re

NUM = re.compile(r'^-?[0-9](\.[0-9]+)?')

MODE_NORMAL = "normal"
MODE_COMMENT = "multi-line comment"
MODE_DATA = "multi-line data"

COMMENT_START = "#--"
COMMENT_END = "#--#"


class ScSyntaxError(Exception):
    pass

class ScEofError(ScSyntaxError):
    pass


def parseFile(filepath):
    with open(filepath, 'r') as fh:
        lines = [line.rstrip("\n\r") for line in fh]
    return parse(lines)


def parse(lines:list[str]):
    data, _ = parseMap(lines, 0, [], toplevel=True)
    return data


def parseValue(value:str):
    if ''.join(value[0:1]+value[-1:]) in ['""', "''"]:
        return value[1:-1]

    if re.match(NUM, value):
        for t in (int, float):
            try:
                return t(value)
            except ValueError:
                pass

    if value.lower() in ["true", "false"]:
        return True if value.lower() == "true" else False
    
    return value


def parseMultilineComment(lines:list[str], start_idx) -> int:
    i = start_idx

    while i < len(lines):
        try:
            line = lines[i].strip()
            if line == COMMENT_END:
                return i
        finally:
            i+=1

    raise ScEofError(f"EOF: unclosed comment started at line {start_idx}")

def parseMultilineData(lines:list[str], start_idx, head) -> tuple[str,int]:
    i = start_idx
    mldata = []
    marker = "----"
    m = re.match(r"<<\s*(.+)", head)
    if m:
        marker = f"--{m.group(1)}"
    else:
        raise ScSyntaxError(f"Not a multi-line marker: {repr(head)}")
    while i < len(lines):
        try:
            line = lines[i]
            if line == marker:
                return "\n".join(mldata), i
            mldata.append(line)
        finally:
            i+=1

    raise ScEofError(f"EOF: unterminated multiline data started at {start_idx} (expected {repr(marker)})")


def parseMap(lines:list[str], start_idx:int, lead:list, toplevel=False) -> tuple[dict,int]:
    data = {}
    i = start_idx

    while i < len(lines):
        line_no = i+1
        try:
            line = lines[i].strip()

            if line == COMMENT_START:
                i = parseMultilineComment(lines, i)
                continue

            if not line or line.startswith("#"):
                continue

            if line == "]":
                raise ScSyntaxError(f"Error whilst parsing map at {lead} from line {start_idx} : found list closer on line {line_no}")
            if line == "}":
                return data, i

            try:
                k,v = line.split(maxsplit=1)
            except ValueError as e:
                raise ScSyntaxError(f"Expected key-value (map started at line {start_idx}), got {repr(line)}") from e
            location = lead+[k]
            
            if data.get(k) is not None:
                raise KeyError(f"Key '{','.join(location)}' redefined on line {line_no}")

            if v == "[":
                values, i = parseList(lines, i+1, location)
                data[k] = values
            elif v == "{":
                submap, i = parseMap(lines, i+1, location)
                data[k] = submap
            elif v.startswith("<<"):
                mldata,i = parseMultilineData(lines, i+1, v)
                data[k] = mldata
            else:
                data[k] = parseValue(v)

        finally:
            i += 1

    if toplevel:
        return data, i
    raise ScEofError("EOF: Invalid map definition - no closing '}' for map from line " f"{start_idx}")


def parseList(lines:list[str], start_idx:int, lead:list):
    data = []
    i = start_idx
    location = lead + ["[]"]

    while i < len(lines):
        line_no = i+1
        try:
            line = lines[i].strip()

            if line == COMMENT_START:
                i = parseMultilineComment(lines, i)
                continue

            if not line or line.startswith("#"):
                continue

            if line == "]":
                return data, i
            if line == "}":
                raise ScSyntaxError(f"Error whilst parsing list at {location} from line {start_idx} : found map closer on line {line_no}")
            
            if line == "[":
                values, n = parseList(lines, i+1, location)
                i = n
                data.append(values)
            elif line == "{":
                submap, n = parseMap(lines, i+1, location)
                i = n
                data.append(submap)
            elif line.startswith("<<"):
                mldata,i = parseMultilineData(lines, i+1, line)
                data.append(mldata)
            else:
                data.append(parseValue(line))

        finally:
            i += 1

    raise ScEofError(f"EOF: Invalid list definition - no closing ']' for list from line {start_idx}")


def main():
    import sys
    import pprint

    try:
        data = parseFile(sys.argv[1])
        pprint.pprint(data)
    except ScSyntaxError as e:
        print(e)
        exit(1)


if __name__ == "__main__":
    main()