# 2 - Bracket string vision production audit

## Load-bearing claim

The best current implementation of the bracket-string vision is:

- keep `[ ... ]` as the sequence delimiter at `Vec<T>` / set
  positions;
- also accept `[ ... ]` as an ordinary string delimiter at `String`,
  `Path`, and map-key positions;
- make the encoder canonicalize non-bare string-like values to bracket
  strings instead of double-quoted strings;
- keep legacy double-quoted decode support for now, but stop emitting
  it from the canonical encoder;
- use `[| ... |]` as the multiline block-string delimiter, with the
  existing common-indent stripping behavior when the content begins
  with a newline.

This is intentionally schema-positioned. The position tells the
decoder whether the same square-bracket surface is a sequence or a
string. That would be ugly if strings were unrelated to vectors. It is
acceptable here because the design premise is that a string is the
compact character-vector case, and NOTA is already positional.

## What this fixes

The prior canonical quoted-string form makes inline NOTA fight the
shell:

```sh
spirit "(Record nota Principle "bad shell edge" ...)"
```

Putting NOTA itself inside shell double quotes is the ergonomic goal.
Normal string content therefore needs a canonical form that does not
emit `"`:

```nota
[he said 'yes']
```

The correction is not cosmetic. If the ordinary human-authored string
surface teaches agents to write `"..."`, the CLI surface stays fragile.

## Skeptical audit

### Ugly pattern: delimiter overload

`[ ... ]` already means sequence. Making it also mean string can look
like the same special-case mistake the map redesign just removed.

The distinction is that map-as-vector-of-entry-records lied about the
data structure. A map is not a vector; it is key/value. It deserved
`{ ... }`.

A string as compact character sequence does not lie about the data
structure. The ugly part is not conceptual; it is implementation
pressure. A lexer that insists on classifying `[` without schema
context cannot support the design cleanly.

Resolution: leave the raw `Lexer` token stream sequence-oriented, and
teach the schema-aware `Decoder` string protocol method to consume a
bracket string when the schema position expects string-like text. The
schema-aware layer already owns the distinction between `String`,
`Path`, map key, record field, enum variant, and vector element.

### Ugly pattern: canonical output still contains double quotes

If decode accepts bracket strings but encode keeps writing `"..."`, the
design fails in production. Agents and component CLIs mostly learn from
encoder output, examples, and tests. Canonical emit must move first.

Resolution: `Encoder::write_string`, `Encoder::write_path`, and
`Encoder::write_map_key` emit bracket strings whenever a bare token is
not valid. Double-quoted strings remain parseable as legacy input, not
as the normal output form.

### Ugly pattern: block string delimiter collision

`[| ... |]` needs a collision rule. If the content contains `|]`, the
block delimiter cannot preserve it without more syntax.

Resolution: use block strings only when the value contains a newline,
does not start with a newline, and does not contain `|]`. Otherwise
emit the inline bracket string with escaped newline/control characters.
This mirrors the old triple-string encoder rule and keeps round-trip
canonicality simple.

### Ugly pattern: whitespace-sensitive maps

Map keys remain a flat alternating token stream. Allowing whitespace
inside keys would require grouping inside the key slot and reopen the
same "map has interior exception syntax" problem.

Resolution: map keys may decode through bracket strings for non-bare
single-token key text, but keys containing whitespace stay invalid on
encode and decode.

### Ugly pattern: old quote syntax becomes permanent by accident

Keeping `"..."` decode support is a practical compatibility choice, but
it can become a silent second canonical syntax.

Resolution: tests should assert that encoder output contains bracket
strings for non-bare string-like values. Documentation should describe
double quotes, if mentioned at all, as legacy accepted input rather
than the normal authored form.

## Production witnesses

The implementation should prove these constraints:

- A string field with spaces encodes as `[with spaces]` and decodes
  back.
- A string containing an apostrophe encodes without shell-hostile
  double quotes: `[we're ready]`.
- A string containing double quotes is preserved inside bracket
  strings, but examples should not prefer that prose style.
- A `Vec<String>` still encodes as `[alpha beta]`; the same delimiter
  remains a sequence at vector positions.
- A `String` field can decode `[alpha beta]` as one string, while
  `Vec<String>` decodes `[alpha beta]` as two strings.
- A multiline string encodes as `[|...|]` when safe and decodes through
  the same dedent behavior as the old human-layout block.
- A multiline string containing `|]` falls back to inline bracket
  escapes and still round-trips.
- A `Path` with spaces and a map key requiring delimiters no longer
  emit double quotes.
- Map keys with whitespace remain rejected.

## Implementation boundary

The implementation belongs in `nota-codec`; the language spec examples
belong in `nota`. `nota-derive` should not need a code change because
derive output already calls `Decoder` / `Encoder` protocol methods for
strings, paths, maps, and vectors.
