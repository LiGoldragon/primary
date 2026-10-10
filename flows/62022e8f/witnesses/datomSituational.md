# Datom situational reading

Method: code read /git/github.com/LiGoldragon/datomic/src/lib.rs, tests/bare_strings.rs, tests/d2_structs_and_enums.rs, tests/d3_orchestrate_anatomy.rs, tests/d3_string_payloads.rs; /git/github.com/LiGoldragon/protos/src/lib.rs:526-567 (via subflow, 2026-08-30).

Fixed by the text's delimiters alone: braces are a struct, brackets a
vector, guillemets a map, curly quotes or parentheses a string, a head
a variant; Headed/Bare/Enclosed and the separator are decided by
Protos before any type is consulted; no datomic type accepts another
enclosure (Vec: lib.rs:275 Bracketed only; BTreeMap: lib.rs:291
Guillemets only; every struct Braced); no single-field unwrapping
(Release.{-42}, d3_orchestrate_anatomy.rs:269-275). Textualize never
varies by position (every `portion()` is context-free; lib.rs:40-42).

Decided by the expected type: a Bare symbol reads as String, i64
(protos lib.rs:527-537), bool True/False (lib.rs:129-135), or a unit
variant; a Headed reads as FiniteDecimal (Period separator, protos
lib.rs:540-567) or, where a String is expected, as the string it came
from (`canonical_text()` fallback, lib.rs:264; test
bare_strings.rs:4-11 for a.b a!b a:b). DatomicString accepts any
Portion shape. Option: absence is the bare `None`, presence
`Some.body` (lib.rs:319-337).
