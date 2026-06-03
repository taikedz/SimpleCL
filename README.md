# SimpleCL : a minimal structured config notation

A minimal, well-defined, human-readable/writable config notation with easy-to-implement parsing rules.

This came about because

* ENV is too restrictive, with no support for complex types
* INI is not well-defined and doesn't typically support complex types and deep-nesting ; different parsers for different flavours abound
* JSON is tedious for hand-editing ; it doesn't support comments so is prone to being loaded through `eval()` - yuck !
* YAML is usually not supported in standard libraries, complex to fully implement, and usually requires an unaudited third-party library

You may want a self-implemented parser for any reason including

* the structure of json/yaml , but the simplicity of env/ini
* security/auditability - self-implementing can be better than SOUP from an auditing perspective
    * with supply-chain attacks on the rise, a complex parser in your SOUP dependencies should not be one of them
    * (SOUP = "Software Of Unknown Provenance")
* A restricted environment means you have access to no parsers (e.g. in-game scripting environments)

amongst others.

## Supported features

* Line-based definitions - each definition is on a single line
* Comments, multiline comments
* Nested map and list structures
* Multiline data

See the [example file](example/data.example)

## Specification

TBD. I started the implementation to get a feel for the ergonomics and was done beore I knew it...

## Reference implementation

This repository provies a reference implementation in python to demonstrate how easy it is to parse the language. It is a single self-contained file with barely 200 lines to perform the parsing, and also provides line number feedback on syntax errors.

## Licensing and identity

The specification is licensed CC-BY 4.0 . The reference code is licensed LGPL v3.0 .

For purposes of clarity:

* The name of the format specified here is `SimpleCL`.
* The specific subname of the specification as implemented in this copy of the repo is `Reference`
* Its full name is `SimpleCL.Reference`

If forked, the full name MUST be different. It is recommended you change the subname to suit your project if you modify the specification.
