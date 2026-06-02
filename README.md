# StruConf : a minimual structured config notation

A minimal, well-defined, human-readable config notation with easy-to-implement parsing rules.

* INI is not well-defined and doesn't typically support deep-nesting
* JSON is tedious for hand-editing
* YAML is complex to implement fully

You may want a self-implemented parser for any reason including

* security/auditability - with supply-chain attacks on the rise, a parser in your SOUP dependencies should not be one of them
* minimality - if your system is resource-constrained, a bespoke parser for your needs may make sense
* language support - your language may not have the parser you need

amongst others.

## Licensing and identity

The specification is licensed CC-BY 4.0 . The reference code is licensed LGPL v3.0 .

For purposes of clarity:

* The name of the format specified here is "StruConf".
* The specific subname of the specification as implemented in this copy of the repo is "Reference"
* Its full name is "StruConf.Reference"

If forked, the full name MUST be different. It is recommended you change the subname to suit your project if you modify the specification.

## Example

```tcl
# Comments start with a '#'

main {                  # By convention, a "main" section is declared
                        #   '{' must be followed by a new line

                        # Indentation is conventional, but not required
                        #   New-line _is_ syntactic, though.

    output   ./bin      # normal key-value.
                        # after comment is removed, any whitespace after value is removed

    sources  [          #  key to list of values
                        #   '[' must be followed by a new line
        ./src           # each value lives on its own line
        ./lib/lib-src
        ./my files/src
                        # Note that a list value can only be a string
    ]

    opts {
        opener  "{"     # use quote mark to indicate literal data
        closer  '}'     # the line MUST end with the same quote mark opener
        spacer  " "
        quotemark """
        singles   '''

    }
    quote   "Say "yes"" # -> Say "yes"
    cite    ""Hark!""   # -> "Hark!"
                        # Anything between the opening and closing marks are raw data.

    types {
    # Special values
    # If it looks like a number, it is a number, else it is a string
    count 5          # a number
    id "5"           # clearly intended to be a string
    happy true       # a boolean
    know_it "false"  # a string
    }
}

```

The implementation that you produce will determine what the parsed data should look like. The above equivalent in JSON would be

```json
{ "main" : {
    "output" : "./bin",
    "sources" : ["./src", "./lib/lib-src", "./my files/src"],
    "opt": [
      "opener": "{",
      "closer": "}",
      "spacer": " ",
      "quotemark": "\"",
      "singles": "'"
    }
    "quote": "Say \"yes\"",
    "cite": "\"Hark!\"",
    "types": {
        "count": 5,
        "id": "5"
    }
}
}
```

This highlights:

* line-by-line parsing
* availability of maps and lists
* no syntactical whitespace management
* no comma management
* Easy to hand-edit
* No "eval" temptations

Relative to mainstream config notations:

* Slightly more verbose than INI, but with greater clarity
* No multi-line values support, but that discourages its abuse into a DSL
* Comments officially supported !
