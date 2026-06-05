---
title: 73.6 — Overview — the improved NOTA/schema mechanism, situated
role: system-designer
variant: Psyche
date: 2026-06-05
topics: [nota, schema, schema-next, schema-rust-next, structural-macro-node, asschema-removal, schema-pipeline, spirit, record-shape, situate, implications]
description: |
  Orchestrator synthesis (incorporates the completeness + accuracy critiques, which
  corrected the situate draft's central error). The improved mechanism: schema is a
  NOTA dialect of structural macro nodes; authored .schema deserializes to
  schema-in-rust then lowers to Rust; Asschema is being removed (landed in nota-next;
  removal deferred + multi-repo). Situated against our Spirit-record-redesign: report
  72's migration MECHANISM is confirmed-wrong (asschema-based), but the record SHAPE
  (flat vs per-kind) is NOT decided — it is the gating open question. Plus a live
  finding: the hash migration re-minted ids mid-session, so earlier short-code
  citations are stale. Full touch-list + the clarifications the psyche must resolve.
---

# 73.6 — Overview: the improved NOTA/schema mechanism, situated

Kind: psyche (orchestrator synthesis). Date: 2026-06-05.

This overview supersedes the contradiction in `5-situate-and-implications.md` that
both critics caught: that report asserted the flat record was DECIDED in Part B
while flagging it as OPEN in Part C. The honest position is below: flat-vs-per-kind
is **not decided** — it gates our thread.

## 1. What the improved mechanism is (landed vs deferred)

`(Spirit Decision vez8, Maximum)` [Schema is a specialized NOTA dialect built on
structural macro nodes — NOT a separate language; a schema file IS full NOTA. The
pipeline: authored .schema (NOTA) DESERIALIZES via the structural-macro-node codec
into schema-in-rust (typed Rust, rkyv, a canonical round-trip image), which LOWERS
into Rust interface code. No separate assemble step — Asschema is removed; the
resolution it did (inline hoisting, visibility, ordering, symbol paths) becomes
methods on schema-in-rust used during lowering.]

`(Spirit Principle xai7)` [The structural macro node — a NOTA enum decoded by SHAPE
in declaration order, type-directed, bidirectional, `#[derive(StructuralMacroNode)]`.]

Landed vs deferred (source-grounded, gather report 4):

- **Structural macro node: LANDED** in nota-next.
- **Asschema removal: DEFERRED.** Asschema is still the live compat intermediate;
  its removal is designed (`522`) but not executed, and it is **multi-repo** —
  the deletion touches spirit, cloud, domain-criome, upgrade, signal-cloud.
- **The spirit pilot is already off `.asschema` materialization** — it builds
  `schema/*.schema → src/schema/*.rs` directly via the shared driver; the
  `*.asschema` files remain only as committed test fixtures. (Note: spirit's own
  `INTENT.md` and `protocols/active-repositories.md` still describe the OLD
  asschema pipeline — both stale.)

## 2. Situate against our Spirit-record-redesign (the corrections)

**2a. Report 72's migration MECHANISM is wrong — confirmed by both critics + source.**
Report 72 said "bump the asschema version literal in `build.rs`, propagating into
`*.asschema` headers." Spirit no longer materializes `.asschema`; there is no such
version literal; `build.rs` watches `.schema` + `src/schema/*.rs`. The correct path:
edit `schema/signal.schema`, regenerate `src/schema/signal.rs` via
`SPIRIT_UPDATE_SCHEMA_ARTIFACTS`. And because the pilot is clean-break (`o7lx`),
**no `UpgradeFrom` runs at all** — the whole report-72 migration section is moot.

**2b. Report 72's record SHAPE is NOT decided — this is the gating question.**
The corpus holds, all at High, none superseded:
- `20jk` [record fields vary by kind; a private-bearing record carries a privacy
  field while a public record omits it; tighter per-kind shape] — this is the
  record I earlier cited as `3awz` (see §3 on the re-mint).
- `f0wm` [intent records shaped as specific VARIANTS whose fields match their
  semantic needs; private variants carry privacy, public variants should not carry
  unused privacy fields].
- `m27p` [privacy is an Optional field — NOTA None public, (Some Magnitude)
  elevated — available to ANY kind; this is how the per-kind "public omits privacy"
  intent is realized in NOTA].

`m27p` is the most recent (the psyche's direct answer) and frames itself as
*realizing* the per-kind intent via Optional. But `20jk`/`f0wm` explicitly say
per-kind **variants** with public variants structurally lacking privacy. Optional-
on-a-flat-record and per-kind-variants are different structures. I inferred "flat"
from `m27p` and ran with it; the critics correctly flag that as an unconfirmed
resolution of psyche-gated intent. **The psyche must choose** (clarification A).

**2c. The flat/positional record is UNAFFECTED by decode-by-shape.** Whichever
shape wins, `Kind` is a data-tag enum, not a structural-shape enum; the record is a
fixed positional shape; privacy-as-Optional and relations-as-Vec ride existing NOTA
`Option`/vector decode. The structural-macro-node mechanism does not change record
authoring here. The one real exposure: the P1 dual-lowering bare-header bug
(`primary-vllc`) sits under our payload-less `Kind` unit-enum headers — so we must
not blind-regenerate, and that bug is **operator-owned main work** (we coordinate,
we don't fix it).

**2d. relations is coupled to hash identity.** relations (`a3l4`, was `50qy`) is a
vector of stable hashes; the pilot's `RecordIdentifier` is still a reusable `u64`
(report 72 Blocker 4). relations-of-`u64` is a silent-corruption bug, so the pilot
must move to the frozen-hash identity (report 64) before relations is correct — the
same coupling §3 just demonstrated live.

**2e. lojix/horizon.** lojix adoption (`4sff`) is unblocked-downstream: copy
spirit's CURRENT (asschema-free) build, and wait on `primary-vllc` before relying on
payload-less variant lowering. horizon-rs (`4v45`) is untouched by this mechanism.

## 3. Live finding — the hash migration re-minted ids mid-session

Operator's "migrate ALL records to random hashes" + the min-4 short-code deploy ran
DURING this session. Records I captured early returned 19-char hashes and now render
as different short codes: `3awz`→`20jk`, `50qy`→`a3l4`, `audg3`→`cw5t`,
`515t`→`g8ln`, `6vsl`→`vbx6`. Records captured after the deploy (`m27p`, `o7lx`,
`tw81`) are stable. So: a **one-time re-mint**, now settled — but it means **every
short-code citation in reports 71/72 and this report's frame is stale**. Two
consequences: (1) those citations degrade to their bracket-descriptions (which is
why the workspace rule is description-first, code-secondary — the descriptions still
resolve); a refresh pass should update the codes. (2) It is a live proof that
relations-by-hash only works once hashes are frozen-at-creation (report 64) — exactly
§2d's coupling.

## 4. Everything this touches (the enumeration you asked for)

Reports:
1. `reports/system-designer/72-...` — re-ground: delete the asschema migration
   mechanism (§2a); mark the record SHAPE as gated on clarification A, not decided;
   keep the relations↔hash coupling (Blocker 4).
2. `reports/system-designer/71-.../` §3 (stack-rewrite) — the schema/triad framing
   should note the asschema-removal + structural-macro-node direction.
3. This report (73) — the situate of record.

Skills (all currently describe the pre-improvement world):
4. `skills/spirit-cli.md` — deployed version is **v0.5.2** (not 0.5.0), 5-field
   shape; will change with the record redesign.
5. `skills/intent-log.md`, `skills/intent-maintenance.md` — record shape + the
   relations/refresh behavior (the agglomeration skill we owe).
6. `skills/nota-design.md` — the structural-macro-node concept + schema-is-NOTA.
7. `skills/nota-schema-docs.md` — EXISTS already (don't create a duplicate
   "schema-design" skill); extend it / cross-reference for the new pipeline. Query
   `skills/skills.nota` before authoring any new schema skill.

Workspace surfaces (stale, will misdirect future sweeps):
8. `protocols/active-repositories.md` — lines ~37-38 still say schema-next "emits
   ordered macro-free Asschema" / schema-rust-next "consumes Asschema." Update to
   the schema-in-rust pipeline.
9. `spirit/INTENT.md` — still claims `.asschema` materialization.

Repos (the asschema-removal blast radius, when it lands):
10. spirit, cloud, domain-criome, upgrade, signal-cloud — all schema-derived
    consumers that the Asschema deletion touches (designer 2's migration step 5).

Our thread / cross-lane:
11. The pilot implementation approach: new pipeline (edit `.schema` + regenerate),
    clean break, hash-identity-first, wait on `primary-vllc` (operator).
12. `primary-vllc` is operator-owned — sequencing dependency, not ours to fix.

## 5. Clarifications the psyche must resolve (gating first)

**A [GATES THE RECORD REDESIGN] — flat vs per-kind.** `m27p` (privacy Optional on a
flat record, any kind) vs `20jk`/`f0wm` (per-kind variants, public variants omit
privacy). `m27p` is latest and frames itself as realizing the per-kind intent, but
`20jk`/`f0wm` literally say variants. Which is the target: (a) one flat record with
Optional privacy + weight + relations, or (b) per-kind variant records where public
variants structurally omit privacy? Everything downstream in report 72 depends on
this. I will not resolve it by inference.

**B — production/pilot divergence during the pilot period.** Production Spirit
(v0.5.2) carries the 5-field shape and is capturing your live intent *today*; the
pilot will carry flat/variant + weight + relations + Optional privacy. During the
pilot, do agents capture against the production shape (status quo) or the new shape?
And when/how does production absorb weight + relations — operator cutover only?

**C [confirm] — clean break under the new mechanism.** Edit `schema/signal.schema` +
regenerate `src/schema/signal.rs`, fresh `.sema`, no `UpgradeFrom` in the pilot.
Confirm this is the intended path.

**D [FYI + sequencing] — `primary-vllc`.** The dual-lowering bare-header bug under
our `Kind` headers is operator-owned; our regeneration waits on or coordinates with
operator's fix. We do not regenerate blind.

## See also

- `1-latest-intent.md`, `2-designer-thread.md`, `3-operator-thread.md`,
  `4-source-grounding.md` — the gather.
- `5-situate-and-implications.md` — the situate draft (its central flat-vs-per-kind
  contradiction is corrected here in §2b).
- `reports/system-designer/72-...`, `71-.../` — our prior record-redesign thread.
