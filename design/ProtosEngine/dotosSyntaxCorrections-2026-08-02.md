# Dotos Syntax Corrections — 2026-08-02

> **Supersession notice (2026-08-06).** Later rulings supersede parts of this file; the text below is preserved unedited as the record. No longer in force:
> - The survival of `(|...|)` as pipe-text — superseded: all piped delimiters were dropped and curly quotes “ ” (U+201C/U+201D) became the string carrier, inheriting pipe-text's common-indentation semantics (`llmTokenOptimizationRulings-2026-08-04.md`).
> - Multi-segment dotted name chains (`Technology.Software.Programming.CodeGeneration`) — scrapped (`redesignAuditRulings-2026-08-06.md`).
> The design log reads by recency; consult the named files for the current form.

Rulings from the psyche-interaction session, correcting the Dotos exhibit
in `reports/ProtosEngineHighLevelUnderstanding-2026-08-02.md`, which had
been lifted from the agent-written `protocols/repos-manifest.dotos`.

## Ruling 1: the manifest exhibit is wrong syntax

Agent text answered: the report's exhibit
`(Repo dotos github:LiGoldragon/dotos (Family Dotos) Code Active
Architecture [])` presented as canonical Dotos.

Psyche ruling [psyche-verbatim]: "this syntax is wrong" — and, on the
manager reading the manifest file to diagnose it: "your reading the wrong
syntax file? to get inspired with more bad syntax?"

Seated: `protocols/repos-manifest.dotos` is not a syntax authority; it is
agent-written and systemically wrong (every record). Canonical Dotos
evidence lives in the dotos repository itself (`tests/design_examples.rs`
declares itself the canonical example surface; `tests/next_gen_grammar.rs`,
`tests/derive.rs`, `tests/codec.rs`, `tests/instance_schema.rs`,
`ARCHITECTURE.md`).

## Ruling 2: struct delimiter is `{}`

Agent text answered: the manager's corrected exhibit using brace-delimited
headless record bodies, asking whether the obvious wrongness was the
restated `Repo.` head.

Psyche ruling [psyche-verbatim]: "yes, the delimiters of structs were
wrong; struct is {}"

Seated: struct bodies are brace-delimited. The manifest's
parenthesis-delimited records are wrong at a glance. Corroborated
independently by the dotos repository ("`{}` = structs",
`tests/next_gen_grammar.rs`; a derived struct encodes as
`{(commit sequence) 4}`).

## Manager diagnosis accepted in session [manager-stated, psyche-reviewed]

- A type tag on a record at a known-typed position (`Repo` heading every
  element of a homogeneous list) restates what the position supplies —
  illegal restatement, same disease as field labels.
- `(Family Dotos)` is a field label; field names are illegal; the position
  carries the meaning — bare atom `Dotos`.
- The remote `github:LiGoldragon/<name>` is derivable from the name; a
  position whose value is a function of another position should not exist.
- Corrected form of a manifest record:
  `{dotos Dotos Code Active Architecture []}`.

## Repository-evidence corrections [agent-verified, not psyche-ruled]

- Dotted variant forms replaced the old `(Variant payload)` spelling:
  `Tick.7`, `Range.{3 9}`, nested paths
  `Technology.Software.Programming.CodeGeneration`.
- The structural pipe forms `(| ... |)` and `{| ... |}` are removed from
  the current grammar; `(|...|)` survives only as pipe-text, alongside
  `[|...|]`, reserved for content that genuinely needs escaping.
- Explicit empty collections (`[]`) at known positions are canonical:
  every field is always present.
- `tree-sitter-dotos` lags the current grammar (still carries the removed
  structural pipe forms); its fixtures are not current-syntax authority.

## Appended 2026-08-02, later same session: pipe-text indentation baseline

Agent text answered: the report's pipe-text table row ("only when content
genuinely needs escaping") and, after the psyche's addition, the manager's
restatement of indentation-aware parsing ending with the baseline
sub-choice: opening-delimiter column vs minimal common indent.

Psyche ruling [psyche-verbatim]: "and for indented whitespace parsing (for
beautifully indented formatting). do you understand what I mean?" then,
ruling the baseline: "the minimal common indent of the block's lines"

Seated:

- Pipe-text serves two purposes: literal carriage of content that needs
  escaping, AND multiline text under **indentation-aware parsing** so
  documents can be beautifully indented.
- Parsing dedents a multiline pipe-text block by the **minimal common
  indent of the block's lines**; the pretty-printer re-indents to the
  structural depth; the encoded value carries the dedented true text.
- Indentation belongs entirely to the textual projection, never to the
  value: re-formatting at a different nesting depth never changes what the
  string is. This supersedes the "reserved for content that genuinely
  needs escaping" phrasing above.

## Appended 2026-08-02: vector-payload variant spelling confirmed

Agent text answered: the manager's expected form for a dotted variant whose
single field is a vector — the vector carried directly as the payload,
`Batch.[3 9 27]`.

Psyche ruling [psyche-verbatim]: "you have it right"

Seated: a single-field variant takes its payload block directly, whatever
its delimiter — `Tick.7`, `Deprecated.(remote archived + local deleted)`,
`Batch.[3 9 27]`; the brace wrapper appears only for multi-field products
(`Range.{3 9}`).

## Open: remediation of the manifest convention

`protocols/repos-manifest.dotos` self-documents its convention as mirroring
`repos/skills/manifests/*.dotos`. Correcting it therefore touches a shared
convention and its consumers (coverage and doctrine runs read the file).
Remediation not yet commissioned; pending psyche direction.
