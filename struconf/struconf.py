""" StruConf parser

Following the intuitive rules, this is a reference parser. (Formal rules TBD)

This simple python script demonstrates the simplicity of the notation for parsing.
"""


import re

NUM = re.compile(r'^[0-9](\.[0-9]+)+')


class ScSyntaxError(Exception):
    pass

class ScEofError(ScSyntaxError):
    pass


def parseFile(filepath):
    with open(filepath, 'r') as fh:
        lines = [line.strip() for line in fh]
    return parse(lines)


def parse(lines:list[str]):
    data, _ = parseMap(lines, 0, [])
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


def parseMap(lines:list[str], start_idx:int, lead:list) -> tuple[dict,int]:
    data = {}
    i = start_idx
    while i < len(lines):
        line_no = i+1
        try:
            line = lines[i]
            if not line or line.startswith("#"):
                continue

            if line == "]":
                raise ScSyntaxError(f"Error whilst parsing map from line {start_idx} : found list closer on line {line_no}")
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
                values, n = parseList(lines, i+1, location)
                i = n
                data[k] = values
            elif v == "{":
                submap, n = parseMap(lines, i+1, location)
                i = n
                data[k] = submap
            else:
                data[k] = parseValue(v)

        finally:
            i += 1

    if lines [-1:] != ["}"]:
        raise ScEofError("EOF: Invalid map definition - no closing '}'")
    
    return data, i


def parseList(lines:list[str], start_idx:int, lead:list):
    data = []
    i = start_idx
    location = lead + ["[]"]

    while i < len(lines):
        line_no = i+1
        try:
            line = lines[i]
            if not line or line.startswith("#"):
                continue

            if line == "]":
                return data, i
            if line == "}":
                raise ScSyntaxError(f"Error whilst parsing list from line {start_idx} : found map closer on line {line_no}")
            
            if line == "[":
                values, n = parseList(lines, i+1, location)
                i = n
                data.append(values)
            elif line == "{":
                submap, n = parseMap(lines, i+1, location)
                i = n
                data.append(submap)
            else:
                data.append(parseValue(line))

        finally:
            i += 1

    if lines [-1:] != ["]"]:
        raise ScEofError("EOF: Invalid list definition - no closing ']'")
    
    return data, i


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