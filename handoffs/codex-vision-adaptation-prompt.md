# First prompt: Codex implementer — acquire psyche vision, then adapt protos-engine

You are the implementer on the protos engine, starting with clear, fresh
context. Do not start coding. Your first task is to acquire enough psyche
vision, from the primary sources below, with your own eyes and your own
inference — nothing in this prompt is imposed as doctrine, and summaries by
other agents (including this prompt) are pointers, not authority. Grade the
provenance of everything you absorb. When you judge your vision acquisition
sufficient, say so, answer the question at the end, and only then begin
work.

## Session transcripts, most current first

- `~/.claude/projects/-home-li-primary/0f9d1436-0f9a-4cb0-9c08-60027d8cbc6e.jsonl`
  — 2026-07-31 through 2026-08-01, the current management session. The most
  current authority. Contains the psyche's verbatim flows behind every
  design entry dated 2026-07-31/08-01: the review-agenda rulings (Q1
  common-mechanism, Q2 file-kinds law), three-layer naming, capsule-as-
  program, sugar doctrine (main/generics/attributes), FFI-in-Logos, the
  self-hosting mirror-type loop, the trait standard, the syntax conciseness
  gradient, the Dotos rename, and the intent-to-spirit rename.
- `~/.claude/projects/-home-li-primary/df3857a3-2c92-4545-9659-d43727d969cb.jsonl`
  — 2026-07-30/31 management session. The foundational structural-parsing
  re-explanation: the Ethos source file as a pre-known typed struct, per-
  position structural possibilities, same surface forms meaning different
  things at different positions, the six-slot layout demoted to old design,
  and the doubt-everything directive.
- `~/.claude/projects/-home-li-primary/e659bbc8-10bc-4a4b-81c8-0ff7a7b5d882.jsonl`
  — prior vision session. The three-language separation rationale (ethos /
  nomos / logos, NOTA-now-Dotos as the fourth), "this means my design was
  lost", the All-matches-all reversal, and the long po2.19 Fold/
  RecursiveInvoke negotiation ending at delegated-assent, not ruling.
- `~/.codex/sessions/2026/07/30/rollout-2026-07-30T11-12-27-019fb24b-ea61-7440-88d3-9679e407131a.jsonl`
  — your own prior thread. The same re-explanation was broadcast here
  (index ~2487); also the tuples ruling, po2.19 left explicitly unruled
  (index ~2456: "do not build recursion surface until it is"), and the
  closing directive "expect having to rewrite significant portions of many
  parts" (bead protos-engine-po2.25, blocks po2.7).
- `~/.codex/sessions/2026/07/28/rollout-2026-07-28T12-54-09-019fa85c-4f71-7512-85a4-e40941519405.jsonl`
  — older implementer thread: naming/rename model, module-owned nametables,
  encodedID chains. Pre-dates the re-explanation; treat as older evidence,
  not current doctrine.
- Older still: many original sessions were deleted by the psyche. Old
  material is discussed as "schema"; schema-rust is the old generation.
  Everything written before 2026-07-31 is evidence, not doctrine.

## Design log entries (condensed authority; the transcripts are primary)

- `design/ProtosEngine/sameFormAndFileKinds-2026-08-01.md` — "same
  textual/encoded form" = common-mechanism reading; file kinds differ ONLY
  by root type, one shared expected-type-at-position machinery; per-kind
  parsing code means the implementation failed.
- `design/ProtosEngine/threeLayerNamingAndNomosBootstrap-2026-08-01.md` —
  three-layer naming (true/encoded/visible) adopted; capsule is a program,
  not a file; files are balanced renderings; imports/exports are derived
  views; main is sugar (trait on the main-thread object); generics and
  attributes are Nomos objects; FFI belongs in Logos; the self-hosting
  loop: a Nomos object eventually emits both the final Logos type and its
  promise-variant mirror from Ethos declarations.
- `design/ProtosEngine/traitStandardAndSpiritRename-2026-08-01.md` —
  impls-under-traits standard; syntax conciseness gradient (Ethos concise,
  Nomos as concise as emission allows, Logos fully explicit); tuple ban
  reaffirmed; handwritten mirror pairs sanctioned as bootstrap.
- `design/ProtosEngine/dotosRename-2026-07-31.md` — NOTA renamed Dotos,
  landing with your train (bead primary-83s).
- `design/Nomos/` — reuse==correctness, tuples-forbidden law scope,
  All-matches-all.

## Reports (evidence and research, graded, never doctrine)

- `reports/protosVisionReacquisition/` — your own prior research pair and
  experiments; its review agenda is being answered in order (Q1, Q2 ruled).
- `reports/PsycheVisionFirstPrinciples-2026-07-31.md` — the manager-side
  tentative vision reconstruction, with live-thoughts section.
- `reports/NomosLogosMirrorTypesResearch-2026-07-31.md` — mirror-type
  options; read its provenance caveat.
- `reports/MacroTimeEvaluationPriorArt-2026-07-31.md` — with appended
  retraction of the universality claim (your correction was accepted).
- `NON_IDEAL_AGENTS.md`, section "Handwritten Nomos/Logos mirror types
  until self-hosting" — the sanctioned bootstrap hack you will live under.

## Bead

primary-36y — adapt protos-engine to the reacquired vision, contracts and
traits first.

## Standing constraints (verify each against its source yourself)

po2.19 recursion surface unruled — do not build recursion surface. No
syn/quote/prettyplease. Tuples forbidden, newtype exception. No string
manipulation in transformation. Translator-only allocation. Impls under
named traits except where trivial or the trait genuinely cannot be
determined. Mirror pairs handwritten, kept in step, treated as future test
fixtures for the self-hosting generator.

## After vision acquisition: first deliverable

Answer this before writing code: under the common-mechanism ruling and the
file-kinds law, which existing components do you judge salvageable as-is,
salvageable with rework, or dead — specifically raw-discovery,
structural-codec's seal-time disjointness, the TemplateValue substrate, and
the six-slot root in core-ethos? Give a provenance-graded assessment and
your proposed ScopeOf trait signatures (your report's section 14.1 truth
tables are the right skeleton; state every [U] cell you fill as an explicit
assumption for psyche ruling). The manager routes disagreements to the
psyche before you commit to a direction.
