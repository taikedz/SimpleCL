# StruConf : a minimual structured config notation

A minimal, well-defined, human-readable config notation with easy-to-implement parsing rules.

* INI is not well-defined and doesn't typically support deep-nesting
* JSON is tedious for hand-editing
* YAML is complex to implement fully

You may want a self-implemented parser for any reason including

* security/auditability - with supply-chain attacks on the rise, a complex parser in your SOUP dependencies should not be one of them
* minimality - if your system is resource-constrained, a bespoke parser for your needs may make sense
* language support - your language may not have the parser you need

amongst others.

## Supported features

* Line-based definitions - each definition is on a single line
* Comments, multiline comments
* Nested map and list structures
* Multiline data

See the [example file](example/data.example)

## Licensing and identity

The specification is licensed CC-BY 4.0 . The reference code is licensed LGPL v3.0 .

For purposes of clarity:

* The name of the format specified here is "StruConf".
* The specific subname of the specification as implemented in this copy of the repo is "Reference"
* Its full name is "StruConf.Reference"

If forked, the full name MUST be different. It is recommended you change the subname to suit your project if you modify the specification.
