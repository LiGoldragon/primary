# Codex Catch-Up and Continuation — 2026-08-02

You are the ProtosEngine implementation agent, resuming after the overnight
package. Read this file and the surfaces in section 1, then execute the
work items in section 3 in order. The boot contract is
`/home/li/primary/AGENTS.md`; Rust work follows the Rust doctrine named by
your role packet and the standards repository
(`/git/github.com/LiGoldragon/standards`): traits are always the first
pass, implementations fall under named traits with site-noted exceptions,
multi-field tuples forbidden.

## 1. Read first

- `reports/ProtosEngineHighLevelUnderstanding-2026-08-02.md` — the new
  dedicated high-level orientation report, psyche-reviewed today.
- `design/ProtosEngine/databaseEvolutionEngine-2026-08-02.md` — newly
  seated: the schema-edit operation produces the migration code (two
  compilation vehicles: next version, or standalone migration executable);
  two routes into a schema edit (native operation, or textual edit whose
  operation is derived by diffing encoded forms, LLM-aided on ambiguity).
- `design/ProtosEngine/dotosSyntaxCorrections-2026-08-02.md` — newly
  seated: struct bodies are `{}`; type tags and field labels are illegal
  restatement; `protocols/repos-manifest.dotos` ruled systemically wrong;
  pipe-text also serves multiline text with indentation-aware parsing,
  dedent baseline = minimal common indent of the block's lines.

## 2. Audit outcome — no rework

Your overnight account was independently audited today and every claim
confirmed: all component heads, versions, pins, assumption labels
(A1-A18, pjm-A1..3, zjo-A1..11 exactly), stop gates, tuple-register
closure, bead and worktree states, and every test gate re-executed at the
exact claimed heads (core-nomos 107+1 with ScopeOf 9/9, core-logos 40,
signal-domain 10+3, byte-compare hash exact). One phrasing nit only: the
signal-domain doc-test target passes but contains zero tests — do not
claim "doc tests" where none exist. No corrective action on the overnight
work is needed.

## 3. Work items

### 3.1 Dotos pipe-text indentation — verify, then implement if absent

Ruling: pipe-text (`(|...|)`, `[|...|]`) carries literal content for
escaping AND multiline text under indentation-aware parsing. A multiline
block is dedented at parse time by the minimal common indent of the
block's lines; the pretty-printer re-indents to structural depth; the
encoded value holds the dedented true text. Re-formatting at a different
depth must never change the value.

In `/git/github.com/LiGoldragon/dotos`: establish what parse and pretty
currently do with multiline pipe-text (`tests/pretty.rs`, codec tests).
If the behavior is absent, implement it with a canonical test in
`tests/design_examples.rs` plus round-trip witnesses (text -> encoded ->
text at two different nesting depths, same encoded bytes). If existing
behavior diverges (e.g. a different baseline, or archived values carrying
indent), stop and report the divergence with evidence before changing
anything archive-visible. Version bump per the versioning discipline.

### 3.2 tree-sitter-dotos catch-up — implement

The tree-sitter grammar lags the language: it still carries the removed
structural pipe forms `(| ... |)` / `{| ... |}`, and its fixtures
(`test/fixtures/basic.dotos`) show retired syntax. Bring `grammar.js` and
the fixtures to current dotos: structural pipes gone, `(|...|)` as
pipe-text only, dotted variant forms (`Tick.7`, `Range.{3 9}`, nested
paths), brace struct bodies, pipe-text indentation from 3.1.

### 3.3 Working-copy hygiene — small

Five of the six component repos have on-disk working copies checked out
behind their `main` bookmarks (this caused a false audit alarm today).
Where no Orchestrate claim or active worktree owns the checkout, advance
the working copy to `main`. Do not touch `language-engine-witness` — its
`TypesOnlyEthos20260802` worktree is still Active.

### 3.4 Tuple continuation under `primary-wgd` — bounded implementation

The audit found four unregistered multi-field tuple enum variants in
`core-nomos/src/manifest.rs` (`NomosManifestLoadError`). Convert them to
named fields with archive witnesses per the established remediation
pattern. Then continue current-universe ad-hoc tuple cleanup ONLY where no
historical or compatibility source is touched — the historical-witness
question (morning-report question 7) is still with the psyche.

### 3.5 repos-manifest remediation — review and propose only, do not land

`protocols/repos-manifest.dotos` is ruled systemically wrong: paren record
bodies (struct is `{}`), a `Repo` type tag restating the known element
type, `(Family X)` field labels where position implies the field, a
remote derivable from the name, retired `(Variant payload)` spellings.
The file self-documents a convention mirrored by
`repos/skills/manifests/*.dotos`, and coverage/doctrine runs consume it.
Survey every consumer and mirrored manifest, then write a proposal report
(corrected file shape, consumer changes, migration order). Psyche approval
is required before any of it lands.

## 4. Hard stops — unchanged

- No six-slot/types-only compatibility bridge; the canonical-source ruling
  (morning-report question 1) is pending; `primary-pjm` stays blocked.
- No output-identity allocation anywhere but the translator (question 2
  pending); the boundary tests enforcing this stay in force.
- No recursion traversal beyond the `RecursiveDescent` gate (question 3
  pending).
- Do not cross the language-witness / ProtosEngine-root integration
  boundary (question 8 pending).
- No fixpoint machinery, ever (DAG law).
- Do not delete or rewrite historical/compatibility witnesses (question 7
  pending).

## 5. Reporting

One report in `reports/` on completion, morning-report style: landed work
with heads and versions, gates run with counts, assumption labels at their
sites, failures and corrections honestly, and ranked psyche questions only
where a new gate was actually hit. Track the work with beads; claim shared
paths through Orchestrate and conclude worktrees when done.
