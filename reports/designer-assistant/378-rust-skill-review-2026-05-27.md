# Rust skills review — consistency with the strengthened no-free-functions rule

## Verdict

Skill IS strong, with four small tightenings landed. The canonical
discipline in `skills/rust/methods.md` already had the §"No ZST
method holders" + §"Legitimate ZST uses — narrow, named" sections
that carry the strengthened rule cleanly. Surface drift was small:
one example file showed a free function in a "Right" example, one
sub-file comment was stale, one cross-reference needed sharpening,
and the index file's one-sentence summary did not name the rule.

No structural rewrites are required. The hard override in AGENTS.md
and the canonical `methods.md` discipline are aligned; everything
else is downstream cross-reference work that has now been done.

## Edited (executed)

| File | Change | jj id |
|---|---|---|
| `skills/rust/methods.md` | Strengthened opening §"Methods on types, not free functions": now states `impl` block must be on a non-zero-sized data-bearing type, names `fn main()` and `#[cfg(test)]` as the only exemptions, calls out `const fn` and `async fn` at module level as forbidden (per record 882), points forward to §"No ZST method holders". | see commit below |
| `skills/rust/methods.md` | Added explicit "the local-helper carve-out from `abstractions.md` does not apply for Rust" — methods.md already disagreed with abstractions.md's carve-out in spirit; now stated. | same |
| `skills/rust/parsers.md` | The "Right" example previously showed `fn extract_private_key` as a free function. Re-cast both Wrong and Right as `impl KeyMaterial { pub fn from_external_json(...) }` so the parser-substitution lesson lands inside a method, removing the implicit free-function endorsement. | same |
| `skills/rust/crate-layout.md` | Module-layout block: `# only free fn lives here` (stale) -> `# contains only fn main() (the one exempt free function per skills/rust/methods.md)`. | same |
| `skills/rust-discipline.md` | §"The rules in one sentence" now leads with the methods-on-types-or-trait-impls rule (was "Behavior lives on types" — true but vague). Sub-files table row for methods.md now spells out "non-zero-sized data-bearing types only; no free functions outside `fn main()` / `#[cfg(test)]`; no ZST namespace holders". | same |

All five edits landed in a single jj commit: short id documented in final chat reply.

## Proposed for designer review

1. **`skills/abstractions.md` §"The local-helper carve-out"** —
   this is the cross-language skill, so the carve-out can stand for
   languages where small private free helpers are idiomatic (Python,
   Go); but the section currently reads as if the carve-out applies
   universally, and a Rust reader following the See-also chain from
   abstractions.md may take the carve-out home. Proposal: add a
   one-line note ("Note: the Rust enforcement in
   `skills/rust/methods.md` removes this carve-out; private helpers
   in Rust go inside `impl` blocks.") at the bottom of that
   subsection. Did not execute — restructuring a §-header's content
   exceeds my tightening authority.

2. **`skills/abstractions.md` §"Schema-emitted nouns" worked example
   (lines 322-330)** — shows `fn dispatch(engine: &Engine, input: Input)
   -> Output { ... }` labelled "Wrong". That's correct, but the
   labelling could be made stronger now that the rule is Maximum.
   Currently reads "Wrong — free function with schema-emitted types
   as arguments"; tightening idea: "Wrong — free function (now
   absolutely forbidden in Rust per `skills/rust/methods.md`)".
   Minor; left for the designer.

3. **`skills/skills.nota` index description for `rust-methods`** —
   currently "Methods on types. One-object-in/one-object-out." Could
   add "no ZST namespace holders" to surface the strengthened rule
   at the index layer. Description-only entries are short by
   discipline, so I left this alone; flagging for designer judgment.

4. **No new skill file proposed.** The strengthened rule is fully
   carried by the existing `skills/rust/methods.md` §"No ZST method
   holders" + §"Legitimate ZST uses — narrow, named" pair.

## Verified consistent

| Skill | Confirmation |
|---|---|
| `skills/rust/methods.md` | Canonical discipline. Already has §"No ZST method holders" + §"Legitimate ZST uses — narrow, named". All `pub fn` examples appear inside `impl` blocks. Opening now matches AGENTS.md wording closely. |
| `skills/rust/errors.md` | Clean. Shows only `pub enum Error` definitions and references `methods.md` in See-also. No free functions, no ZSTs as namespaces. |
| `skills/rust/storage-and-wire.md` | Strong. Already lists "Storage actor as namespace" and "Public ZST actor noun" as anti-patterns in the anti-pattern table. All `pub fn` examples land in `impl` blocks. No drift. |
| `skills/rust/crate-layout.md` | Now consistent (after tightening the main.rs comment). The `pub fn issue_server` example is inside `impl Cert`. Test-files-separate discipline aligns with the `#[cfg(test)]` exemption. |
| `skills/rust/parsers.md` | Now consistent (after re-casting the example). |
| `skills/rust-discipline.md` | Now leads with the rule in its one-sentence summary. |
| `skills/abstractions.md` | Cross-language form. Carve-outs are correctly narrower than AGENTS.md says (because cross-language); Rust enforcement is correctly delegated to `methods.md`. Shows the Wrong / Right schema-emitted example. |
| `skills/naming.md` | No code samples that violate. The "framework-category suffixes" section reinforces the discipline by removing `*Actor` / `*Message` framework tagging — which complements the methods-on-data-bearing-types rule. |
| `skills/beauty.md` | Lists "A free function that should be a method" among the ugliness signals; consistent. |

## Cross-reference graph

Files that reference `skills/rust/methods.md`:

- `skills/abstractions.md` line 355 — §"Domain values are types".
- `skills/enum-contact-points.md` lines 423, 456, 528 — three deep cross-references (Same constraint type-checked; "Use existing trait domains"; "Don't hide typification in strings"). Strong.
- `skills/rust/errors.md` lines 10, 55 — pair-with reference + See-also.
- `skills/rust/storage-and-wire.md` lines 13, 398 — pair-with reference + See-also.
- `skills/rust/crate-layout.md` line 187 — See-also.
- `skills/rust-discipline.md` lines 51, 131 — sub-files table + See-also.
- `skills/operator.md` lines 130, 173, 585, 597 — required reading + deep `§"No ZST method holders"` reference + `§"One object in, one object out"` reference.
- `skills/system-operator.md` line 83 — required reading list.
- `skills/designer.md` line 127 — required reading list.
- `skills/skills.nota` line 65 — index entry.

Gaps: none material. `operator.md` already deep-links to the §"No ZST method holders" subsection — that's the surface where the strengthened rule lands for the role doing the work. Designer and system-operator role files point at `methods.md` at the file level, which is sufficient.

No new cross-references needed.
