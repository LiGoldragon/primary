# Datom example syntaxes to design against — 2026-08-13

Status: proposed by the Designer (session 06196cc7), unreviewed by
the psyche. Surface grounded in the verified estate at datom
10c61336 (tests/round_trip.rs, tests/parser.rs). Example 1 is the
estate's own deep fixture reassembled from its encoding rules
(fragments asserted in tests; the full line is not a test literal).
Examples 2–3 are Designer proposals under the 2026-08-13 interim
string ruling (psyche/Vision/datomSyntax.md). All `“ ”` are
U+201C/U+201D; `\”` is a backslash escaping a closing curly quote.

## Example 1 — the verified deep fixture (nine context levels)

```
Report.{
  “Q3”
  Map.[
    north.[
      “quick note”
      Group.{
        “Ops”
        [ “sub note”
          Group.{
            “Deep } ] \”quote”
            [ “tail” ]
            Map.[ remark.“child sees } ] only as text” ] }
          Map.[ kind.“core” ] }
      Tags.[ “alpha” “beta” ] ] ]
  Some.“inside } ] \”current context” }
```

Lands in:

```rust
struct Report {
    heading: Text,
    groups: BTreeMap<String, Vec<Entry>>,
    latest: Option<Text>,
}
enum Entry { Note(Text), Group(Group), Tags(TagList) }
struct Group {
    title: Text,
    children: Vec<Entry>,
    annotations: BTreeMap<String, Text>,
}
struct TagList(Vec<Text>);
struct Text(String);
```

Exercises: positional records (no field names — ruled density);
variants discriminated by shape alone — `Entry::Note` needs no
head because CurlyQuoteDelimited announces it, `Group.{` and
`Tags.[` announce theirs by head+shape; `Some.` keeps its head
because an Option payload can be any shape; maps as `Map.[key.val
…]` with dotted keys; raw `}` and `]` legal inside legacy strings
(only the closing curly quote is escaped); nine levels of context
with pair-by-pair parent resumption, witnessed in the estate.

## Example 2 — interim string carriers (proposed surface)

Under the 2026-08-13 ruling: `()` and curly quotes both select
plain `String`; the Meaning type replaces this later.

```
InterimNote.{
  “legacy carrier”
  (structured carrier, for now a plain string)
  (nested (balanced) parentheses stay inside the block)
  (a lone closer is escaped \) like this)
}
```

```rust
struct InterimNote { a: String, b: String, c: String }
```

At the discrimination site:

```rust
// String, for now: CurlyQuoteDelimited and ParenthesisDelimited
// both select String. Implement the Meaning type here later — the
// super-string (structuredStringType.md, bead primary-xqb.8.5).
```

Proposed interim interior rules for `(…)`, needing psyche approval:
mirror the legacy-string rules — nesting by balance (as curly
quotes nest by depth), backslash escapes `\)` and `\\`, raw `}` `]`
`“` legal inside. Keeps every carrier lexically skippable, which
the first-pass block scan requires.

## Example 3 — psyche-component shaped (illustrative only)

The component anatomy is open under bead primary-xqb.8.4; this
example only shows the notation carrying that domain. Layer enum
{Spirit, Intent, Vision} is ruled; everything else here is
illustrative.

```
VisionEntry.{
  Vision
  “traitsAsCapabilities”
  [ Ruling.{ “2026-08-13T17:17” (all traits will be qualifiers) }
    Ruling.{ “2026-08-13” (transcodable falls with the drop) } ]
  Map.[ supersedes.“encodedFormIsTheCode” status.Open ]
}
```

Bare `Vision` suffices for the layer field: the expected type is
the Layer enum and BareSymbol announces the variant by name, as
`None`/`True`/`False` already work in the estate.

## Surface truths the examples rest on (verified in the estate)

- Records are positional; field names never appear.
- Heads appear only where shape alone cannot discriminate.
- Scalars are bare: `42`, `-7`, `1.0`, `True`, `False`, `None`.
- Comments: `;;` to end of line.
- Multiline legacy strings strip common indentation.
- Unruled surface, refused with ShapeNotYetRuled: bare `{…}`
  (BraceDelimited) and `X.(…)` (DotParenthesized). `(…)` was
  refused too until the 2026-08-13 interim ruling.

## Open questions for the psyche

1. Interim `(…)` interior rules — approve the mirror-legacy
   proposal above, or rule otherwise.
2. Bare `{…}` and `X.(…)`: keep refusing as unruled, or assign.
3. Confirm heads-only-where-shape-cannot-discriminate as the ruled
   principle (it follows from "no self-describing tags" plus
   shape discrimination, but has not been stated as a rule).
