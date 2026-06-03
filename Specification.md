# Simple Config Language - Specification

Simple Config Language is intended to be extremely simple, such that a full parser can be implemented with a minimal amounts of code and very reduced complexity.

## Syntax errors

Syntax errors in the data being parsed mean the data is invalid as a whole and should not be used. This invalid status should be propagated or signalled somehow to the caller of the parsing routine.

## Value types

There are 6 value types:

* string - the default type for any scalar value
* int - a plain integer. Use the default size of the implementation language. If in doubt, use 32 bits
* float - numeric floating point. Use the default size of the implementation language. If in doubt, use 32 bits
* boolean - a boolean type
* list - and ordered sequence of values
* map - an association of names to values

List and map are complex types, the rest are scalar (simple) types.

## Lines

The configuration data string is split at along CR/LF boundaries. The following consitute a single line end:

* CR (\x0D)
* LF (\x0A)
* CRLF (\x0D0A)

When a sequence LFCR (reversed CRLF) is found, it should be treated as a single LF boundary, followed by a single CR boundary.

Usually (unless otherwise specified), lines are stripped of leading and trailing whitespace, before being processed.

## Comments

SimpleCL supports empty lines and comment lines as being ignored.

An empty line is ignored.

A line starting with `#` is a comment line and is ignored.

A line starting with `#--` starts the beginning of a multiline comment. All subsequent lines are ignored until a `#--#` is encountered on a line on its own (leading and trailing whitespace are allowable)

## Values

Values are pieces of data which appear either associated to a name in a map, or as a distinct item in a list.

A value can be one of the six main value types.

### Scalar values

Scalar values may feature as-is , or encased in double quote marks on either side, or single quotes on either side. If quote marks are found on both sides, these are treated as encapsulating quote marks - they are removed, and everything in between them is retained as-is. If the quote marks mismatch, or only appear on one side, they are considered to be part of the data. Any other quote marks in the data are retained as-is.

If a value is numerical, it wil be parsed to an int if no decimal, or to a float when a decimal is present. If the value is numerical but with encapsulating quotes, it is retained as a string.

### Complex values / nested

Values that indicate the start of a complex type are

* `{` which denotes the start of a nested map
* `[` which denotes the start of a nested list
* `<< MARKERTEXT` which denotes the start of multi-line data

Such values must not be quoted, otherwise they are merely treated as string values.

## Root Map

The top level lines of the data belong to the Root Map - a single unnamed map that is returned from parsing.

Any map other than the Root Map must be terminated by a line containing a single `}` character, optionally with trailing and/or leading whitespace. The Root Map may be terminated by encountering End OF File (EOF)

## Complex types

A complex type must be closed by its own closer character.

A map must be closed with a `}` character. If a `]` is encountered alone on a line as a closer before a Map is closed, this is a syntax error.

A list must be closed with a `]` character. If a `}` is encountered alone on a line as a closer before a List is closed, this is a syntax error.

When a complex type is nested under another, the child type _must_ encounter its own closer in order to close, and for parsing to resume at the parent level.

## Map

A map entry line always specifies a key name, followed by any amout of whitespaced, followed by a value.

A map key name can be any non-zero number of ASCII characters, digits, the underscore, or the hyphen; that is any string matching the regular expression: `^[a-zA-Z0-9_-]+$`

A map may not define the same key twice.

## List

A list entry line consists of any kind of value. Lists contain an ordered discrete number of items.

### Multiline data

Multiline data is reatined as-is: the trailing and leading whitespace is left untouched.

A multiline data marker starts with `<<` and is followed by a piece of marker text e.g. `<< EOTEXT`. Marker labels must adhere to the same convention of map key names: alphanumeric, dash, and underscore.

To close the multiline data section, the section must be closed with its corresponding marker, two hyphens followed by the marker text e.g. `--EOTEXT`. This must be on its own on a line, with no leading whitespace.
