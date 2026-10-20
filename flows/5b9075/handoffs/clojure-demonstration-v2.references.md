# Clojure demonstration v2 references

This companion record preserves attributed evidence without merging it into
the unexecuted JVM handoff.

## Source-observed scratchpad evidence

The source record is
`flows/d68c82/books/references/15-clojure-translation.refs.md`, Edition 2,
with corroborating attribution in `flows/d68c82/log.md` at the reported
scratchpad entry. The scratchpad directory is:

`/tmp/claude-1001/-home-li-primary/d68c8272-6db0-47dd-9c8e-538d95ff12a6/scratchpad/clj-example/`

The supplied exact file identities are:

- `src/translation_example.clj`, SHA256
  `39e167387aee0097ce2a097d65bcf095b0f32fade0e8fb02264bb2dd4db4825b`
- `bb.edn`, SHA256
  `3726c4b9775abf87d612ad1fc03c6d7780d5ffff4283d83c563c79842b8d83c`
- The supplied `bb.edn` contents are
  `{:paths ["src"] :deps {metosin/malli {:mvn/version "0.18.0"}}}`.

Five results were attributed to that scratchpad: `true`, `false`, `true`,
`true`, `false`. They cover the recorded Person/Accepted checks, nested
`#none []` and `#some #none []`, and equality/inequality. They are schema/EDN
observations only; no forward or inverse Datom adapter was tested.

The exact executed command, Babashka version, and execution-environment
identity were not recorded. The reference says the code was reformatted for
width and that the reformatted reader form was not rerun separately. A later
attributed message says the formatted form was rerun. Those accounts are
unresolved; this record does not assert either outcome beyond the five
reported results.

## Separation from v2

`clojure-demonstration-v2.md` is a separate, unexecuted JVM Clojure 1.12.6 /
Malli 0.18.0 artifact. The Babashka scratchpad is evidence about its own
source and configuration only; its hashes and five results do not witness v2.
