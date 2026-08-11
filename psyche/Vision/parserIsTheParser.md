# The parser is the parser

> "assembly.rs reimplements its own parser, which is forbidden.
> the parser is the parser, nothing implements its own parsing logic."

— psyche, 2026-08-11, steward session

Context: the skills generator's assembly.rs contains custom parsing
logic for DOTOS and frontmatter instead of using the project's actual
parser.
