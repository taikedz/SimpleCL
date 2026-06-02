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

```
# Comments start with a '#'
# Comments MUST be on their own line

# A simple key-value
# As much whitespace after the key can exist until value data is found
version       "1.0"

# Here, we create a "main" section pointing at a map
main {                  
    #   '{' must be followed by a new line

    # Indentation is conventional, but not required
    #   New-line _is_ syntactic, though.

    # normal key-value.
    output   ./bin      

    #  key to list of values
    #   '[' must be followed by a new line
    sources  [         

        # each value lives on its own line
        ./src
        ./lib/lib-src
        ./my files/src
    ]

    # Maps can nest into maps
    opts {
        opener  "{"
        closer  '}'
        spacer  " "

    # Indentation is optional (but recommended!)

    quotemark   """
    singles     '''
    }

    # Anything between the opening and closing marks are raw data.
    # To include quotes as the raw data, include them within the edge quotes
    quote   "Say "yes""
    cite    ""Hark!""

    types {
    # Special values
    # If it looks like a number, it is a number, else it is a string
    
    # a number
    count 5          
    
    # clearly intended to be a string
    id "5"           
    
    # a boolean
    happy true       
    
    # a string
    know_it "false"  
    }

    # Lists can contain maps, which can further contain other complex types
    steps [
        {
            name up
            command ./service.sh up
            opts [
                --daemon
            ]
        }
        {
            name down
            command ./service.sh down
        }
    ]
}
```

The implementation that you produce will determine what the parsed data should look like. The above equivalent in JSON would be

```
{'main': {'cite': '"Hark!"',
          'opts': {'closer': '}',
                   'opener': '{',
                   'quotemark': '"',
                   'singles': "'",
                   'spacer': ' '},
          'output': './bin',
          'quote': 'Say "yes"',
          'sources': ['./src', './lib/lib-src', './my files/src'],
          'steps': [{'command': './service.sh up',
                     'name': 'up',
                     'opts': ['--daemon']},
                    {'command': './service.sh down', 'name': 'down'}],
          'types': {'count': '5',
                    'happy': true,
                    'id': '5',
                    'know_it': 'false'}},
 'version': '1.0'}
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
