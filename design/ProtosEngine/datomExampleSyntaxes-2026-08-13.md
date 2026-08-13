# Datom example syntaxes to design against — 2026-08-13, re-cut 2026-08-14

Status: proposed by the Designer (session 06196cc7), unreviewed by
the psyche. Re-cut 2026-08-14 under the rulings in
psyche/Vision/datomSyntax.md: a string that doesn't need quotes
must not be quoted; parenthesis is the default string delimiter,
balance-based (interior balanced pairs are content, an unbalanced
parenthesis is escaped); string blocks ignore other delimiters
until they close; the dotted prefix is officially the Head and is
part of the block's type; variants always re-emit their head,
types with special shapes might not ("It depends"). Curly quotes
remain the legacy carrier. `“ ”` are U+201C/U+201D.

## Example 1 — the deep fixture under the ruled surface

```
Report.{
  Q3
  Map.[
    north.[
      Note.(quick note)
      Group.{
        Ops
        [ Note.(sub note)
          Group.{
            (Deep } ] “quote)
            [ Note.tail ]
            Map.[ remark.(child sees } ] and (nested markup) only as text) ] }
          Map.[ kind.core ] }
      Tags.[ alpha beta ] ] ]
  Some.(inside } ] “current context) }
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

Head placement, corrected 2026-08-14: a variant always emits its
head, and its payload follows in its own shape, headless —
`Note.(quick note)`, `Group.{…}`, `Tags.[…]`, `Some.(…)` are all
uniformly variant-head + payload-shape; no doubling ever arises
because a payload type inside a variant never adds a second head.
A struct standing alone (as at the document root, `Report.{…}`)
emits its own head — "a struct called X" — understood in the right
context when printed alone. Strings go bare whenever the bare form
carries them (`Q3`, `Ops`, `core`, `alpha`, `Note.tail`); raw `}`
`]` `“` and interior *balanced* parentheses are plain content
inside paren strings.

## Example 2 — paren-string balance rules

```
InterimNote.{
  (a plain string)
  (nested (balanced) parentheses are content — the seed of markup)
  (a lone unbalanced one is escaped \( like this)
  “legacy carrier still accepted”
}
```

```rust
struct InterimNote { a: String, b: String, c: String, d: String }
```

At the discrimination site:

```rust
// String, for now: ParenthesisDelimited and CurlyQuoteDelimited
// both select String. Implement the complex-string type here later
// (structuredStringType.md, bead primary-xqb.8.5).
```

## Example 3 — psyche-component shaped (illustrative only)

Component anatomy stays open under bead primary-xqb.8.4; Layer enum
{Spirit, Intent, Vision} is ruled; the rest is illustrative.

```
VisionEntry.{
  Vision
  traitsAsCapabilities
  [ Ruling.{ (2026-08-13T17:17) (all traits will be qualifiers) }
    Ruling.{ (2026-08-14) (verbs accepted for traits) } ]
  Map.[ supersedes.encodedFormIsTheCode status.Open ]
}
```

Bare `Vision` and `Open` announce their enum variants by name, as
`None`/`True`/`False` already work in the estate.

## Surface truths the examples rest on

- Records are positional; field names never appear.
- Strings: bare when possible; parens default when delimited,
  balance-based; curly quotes legacy.
- Variants always re-emit their Head; special-shape payloads may
  absorb it (see the "It depends" application above).
- Bare `{…}` is an unprefixed struct; `X.(…)` is a string-carrying
  variant.
- Scalars bare: `42`, `-7`, `1.0`, `True`, `False`, `None`.
- Comments: `;;` to end of line.
- String blocks ignore other delimiters until they close, so a
  first-pass block scan stays lexical.

## Open questions for the psyche

1. Bare-symbol boundaries: may bare strings carry `-`, `:`, `.`
   (dates, timestamps), or do such values take the paren carrier?
