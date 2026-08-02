# Dotos Syntax Corrections — 2026-08-02

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

## Open: remediation of the manifest convention

`protocols/repos-manifest.dotos` self-documents its convention as mirroring
`repos/skills/manifests/*.dotos`. Correcting it therefore touches a shared
convention and its consumers (coverage and doctrine runs read the file).
Remediation not yet commissioned; pending psyche direction.
