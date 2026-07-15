# Vision evidence ledger v1 — classified reconstruction before the proof-of-concept epic

A read-only evidence reconstruction for Codex and the psyche, ahead of a
multi-component proof-of-concept epic. It classifies every material claim in the
`nextgen-recrystallization` session under Codex's binding evidence rules,
separating explicit psyche rulings from agent proposals, interpretations,
implementations, and unanswered suggestions. The framing that governs the whole
document is the psyche's: "My vision has evolved, so recency alone does not
establish authority."

Written 2026-07-15, session `NextgenRecrystallization`, lane
`VisionEvidenceLedger`, generalist evidence auditor, Opus 4.8 (1M). Read-only on
all code repositories; this one file is the lane's only artifact. The auditor was
not present for the chat; the Manager-witnessed session ledger supplied in the
brief is treated as the witness record for chat events, and every manifested
trace was verified in artifacts, tracker, and code. No classification was
upgraded on the strength of the witness record alone.

## Evidence classes (Codex's, binding)

`EXPLICIT-PSYCHE` directly stated or explicitly accepted by the psyche ·
`ACCEPTED-PROPOSAL` agent-proposed then explicitly accepted · `AGENT-PROPOSAL`
proposed, not accepted · `IMPLEMENTED-FACT` verified in code/artifacts (accepted
or not) · `SUPERSEDED` previously authoritative, explicitly replaced ·
`CONTRADICTION` incompatible surviving evidence without a ruling · `UNKNOWN`
unavailable, corrupted, or only inferred. Silence, continued discussion,
"not obviously bad," implementation, or appearance in a summary is NOT
acceptance. The psyche's graded "non-rejection (not acceptance) — must be
reviewed later" is its own recorded state under `AGENT-PROPOSAL` (beads
primary-56d1.8/.9/.10).

## Headline findings (read this first)

**Commonly believed settled that is NOT settled.**

1. **The three implemented next-gen readings are NOT accepted.** Right-associative
   dot, floats-reconstructed-from-dotted-text, and period-strings-take-`(| |)` are
   `IMPLEMENTED-FACT` (green and tested on the nota next-gen worktree) but their
   ruling status is `AGENT-PROPOSAL` — explicit **non-rejection**, bead
   primary-56d1.8. Implementation is not acceptance. They gate the nota merge
   (primary-z4s9) and remain un-blessed.
2. **The syntax slate (a–g) and the storage proposals are NOT accepted** — same
   non-rejected state, beads primary-56d1.9 and .10. Includes converting
   `StructuralMacroNode` to dotted, the `$` sigil, meta-type sharing, and the
   format-upgrade / co-versioned-NameTable proposals.
3. **The two accepted library/lowering slates are gated, not green-lit.** The
   psyche accepted the *direction* of the four-crate library ("1. Yes") and the
   lowering slate A–H ("3. that all sounds right") but **both are explicitly gated
   on up-close review before implementation** ("I want to see the design up close
   first"). The gate is unmet: he has not reviewed `up-close-design-v1.md` (he
   does not read reports — L9.2).
4. **The Codex recrystallized pipeline is entirely `AGENT-PROPOSAL`.** The psyche
   forwarded it "didnt read what he said in detail." Nothing in it — expectation
   table, declarative programs + trusted evaluator + generated codecs +
   conformance, profile/typed split, sidecar recommendation, branch reorder, the
   five rulings-needed — has a psyche ruling. The manager's alignment assessment
   and the up-close design's integration of it are agent work.
5. **`True*` → `Textual*` IS now settled (L13), superseding the L10 "maybe."** But
   the follow-on terminology ("structural form" vs "structural macro"; a name for
   the Core side) is NOT settled — it is mid-conversation, confirmation-seeking.

**CONTRADICTIONs / discrepancies found and resolved by measurement.**

6. **Golden line-count: BOTH circulating numbers are wrong.** The session brief's
   ~9,000 and the up-close/lowering reports' ~11,700 both miss. Measured:
   **10,779 lines across 8 `*generated.rs` files** (8,110 across the 6 flat-glob
   files). `CONTRADICTION` between the two reports, resolved to 10,779.
7. **`split_at_first_dot` naming: a cross-branch citation split, not a fact
   conflict.** On next-gen (where the design lands) only `split_text_at_first_dot`
   exists (parser.rs:572, `pub(crate)`); the psyche's remembered
   `split_at_first_dot` is a stale doc name there — the shared-codec report is
   right. On the `repos/nota` **main** clone, `split_at_first_dot` IS a real public
   method — the up-close report cited that one while describing next-gen. Both
   real, different branches.
8. **`Block` "Application variant" disagreement is also cross-branch.** core-first
   and shared-codec cite `Block` with an `Application` variant (parser.rs:57–80) —
   TRUE on the next-gen worktree (`Application { span, head, payload }` at
   parser.rs:72). The up-close report cites "parser.rs:70, exactly three variants,
   application NOT a variant" — TRUE on the main clone. No factual contradiction;
   the up-close report inconsistently cited the main clone for `Block` while citing
   next-gen for `macros.rs`.
9. **"13 schema compilation errors" (Codex) — FALSIFIED**, independently, twice.
   `schema`, `schema-language`, `schema-rust` all `cargo check` clean on their
   checked-out state. If Codex means an unmerged branch, that is a
   dependency-portability flag, not a present fact.

**The single most load-bearing inventory fact.**

10. **The next-gen nota work is NOT in the base checkout.** `repos/nota` is on
    **main `f8de7a5`, v0.7.0** (3-variant `Block`, `split_at_first_dot` present).
    All the reports' next-gen `IMPLEMENTED-FACT`s live on the **remote
    `origin/next-gen` (`08ce05c`, v0.8.0)** and its worktree
    `/home/li/agent-worktrees/SchemaCodex/NotaNextGen/nota`, **unmerged**, merge
    gated on psyche acceptance (primary-z4s9). A reader grounding in `repos/nota`
    sees v0.7.0, not the design's ground truth.

## 1. Chronological ledger

Chat events are from the Manager-witnessed session ledger (no absolute chat
timestamps exist — ordering + date bound given; session ran 2026-07-14 →
2026-07-15). Artifact/commit rows carry real jj/git commit timestamps.

| Order / time-bound | Source / agent | Event or statement | Class | Supersedes / depends on | Current consequence |
| --- | --- | --- | --- | --- | --- |
| L0 · 07-14 start | Psyche (handover) | Prior-session baseline: stack NOTA→schema→Nomos→Logos→Rust; logos 1-to-1 with Rust; Core/True mirror; macros define lowering (named+structural kinds); headless Nomos; next-gen grammar; delimiter principle; nexus repos were agent fabrications, deleted | EXPLICIT-PSYCHE (curated baseline) | — | Standing frame; individual claims verified below |
| L0 · 07-14 | Psyche (handover, verbatim) | "Rust is our assembly language."; Core-first statement (Core = strictly-typed true binary rkyv, the essential representation; text is a bridge until in-daemon editing/versioning/format-upgrade mature; sema is the original name for the core true/logical/strict-binary part); "Do a deep audit and recrystalization… no matter the code re-writing magnitude." | EXPLICIT-PSYCHE | — | Governs the whole recrystallization; names **sema** as the historical Core name |
| L0 · 07-14 | Psyche (handover) | Management directive: "DO NOT make elaborate responses until you are completly done launching and/or waiting for agents (also harden that in the management skill)." | EXPLICIT-PSYCHE | — | Manifested → skills commit `8e1451a1`, primary `a469e2fe` (07-14 22:27) |
| L1 · 07-14 | Psyche | "1. all Core* have no strings, they use the corresponding NameTable" + "i now seeing a pattern; this could go in a library" | EXPLICIT-PSYCHE | — | Stringless-Core rule; library *direction* (not a specific design) |
| L2 · 07-14 | Psyche "yes" to manager slate | Identity = blake3 over stringless Core rkyv bytes, NameTable excluded, layout-version-tagged, rename hash-stable | ACCEPTED-PROPOSAL (origin: core-first worker, decision 2) | depends L1 | Target identity model; NOT yet implemented (§3.2) |
| L3 · 07-14 | Psyche "5. Yes" | Nomos stateful at rest; CoreNomos macro-package store; symmetric with schema/logos | ACCEPTED-PROPOSAL (origin: core-first worker, decision 1) | — | Nomos is a stateful daemon by ruling |
| L4 · 07-14 | Psyche directive | "put a fable researcher on making the logos to rust lowering more structural, object-method based on… rust as a form of data" | EXPLICIT-PSYCHE | — | Spawned `logos-rust-lowering-v1.md` |
| L5 · 07-14 | Psyche (question form) | "what if we agglomerate all the `split_at_first_dot` types of abstraction into a shared library/design surface for all the encoding/decoding…" | EXPLICIT-PSYCHE (direction) | — | Spawned `shared-codec-library-v1.md` |
| L6 · 07-14 | Psyche clarification | Any parsing aspect the family does — delimiters, "query to a table of different structural-expectations-macro" | EXPLICIT-PSYCHE | refines L5 | Widened agglomeration to the expectation-table mechanism |
| L7 · 07-14 | Psyche (from Codex exchange) | Complex `*Core` types associated with their structural-parsing table for the next block; the table is used for **both** encode and decode | EXPLICIT-PSYCHE | refines L6 | Table is Core-associated + bidirectional |
| L8 · 07-14 | Psyche (hedged) | "possibly two-way decode-encode rust… crazy idea, but fairly simple even if it only works for a subset" | EXPLICIT-PSYCHE (exploratory) | — | Two-way Rust codec is explored, not committed |
| L9.1 · 07-14 | Psyche reply | "1. Yes, and I want to see the design of all that up close first" | ACCEPTED-PROPOSAL, **gated** (origin: shared-codec worker) | depends L1/L5/L6 | Four-crate library accepted in direction; gated on up-close review (unmet) |
| L9.2 · 07-14 | Psyche | "2. what report? I dont really read reports… make sure we dont grow a pile of stale design" | EXPLICIT-PSYCHE (process) | — | Reports are UNREVIEWED surface; drove report-hygiene bead .14 |
| L9.3 · 07-14 | Psyche | "3. that all sounds right. Id like to see the design up clos" | ACCEPTED-PROPOSAL, **gated** (origin: lowering worker) | depends L4 | Lowering slate A–H accepted in direction; same unmet gate |
| L9.4 · 07-14 | Psyche | "8. no, that would be too implementation specific to record to spirit… train agents better (principle over substance of spirit)" | EXPLICIT-PSYCHE (Spirit doctrine) | — | Manifested → skills `77280a2d`, primary `e74f51de` (07-15 11:47) |
| L9.5 · 07-14 | Psyche | "non-rejection (not acceptance) which means must be reviewed later, and find a place where this way of communicating… could live" | EXPLICIT-PSYCHE creating a graded state | — | The three readings + syntax slate + storage → `AGENT-PROPOSAL` beads .8/.9/.10; slate-protocol manifested in skills |
| L10 · 07-14 | Psyche fork ruling | Textualization is an extension of the text-side (true) — "maybe true is renamed to Textual" — the `Textual*` view extended with structural data (`DelimitedBlock`, `ObjectSymbolPrefixedBlock`, …) | EXPLICIT-PSYCHE (rename hedged "maybe") | — | SUPERSEDED at L13 on the rename |
| L11 · 07-14 | Psyche | "we extend the textual to have many forms, so corelogos has both the logos and rust textual form data-trees… this even opens us emitting other languages than rust from logos" | EXPLICIT-PSYCHE (many-forms) | builds on L10 | Textual is a per-language family over one Core |
| L12 · 07-15 | Psyche forwards Codex | "codex has been looking at pushing the implementation with me. I didnt read what he said in detail. consider it and tell me what sticks out…" | Forwarding is EXPLICIT-PSYCHE; **the entire Codex pipeline is AGENT-PROPOSAL (Codex)** | — | Codex triad unread-in-detail; needs rulings |
| L13 · 07-15 (latest) | Psyche monologue | "true made no sense for any of them. It's just textual… The textual schema and the textual logos." | EXPLICIT-PSYCHE | **supersedes L10 "maybe"** | `Textual*` adopted |
| L13 · 07-15 | Psyche (confirmation-seeking, "Is that what you mean?") | "instead of saying structural macro, we say structural form" | EXPLICIT-PSYCHE-**leaning**, pending his ack of the manager's two-concept split (TextualForm vs StructuralForm) | — | Terminology not final (questionnaire Q2) |
| L13 · 07-15 | Psyche (unruled musing) | "You could even say the symbolic form… but it's more general" | AGENT-adjacent musing, UNRULED | — | Not a ruling |
| L13 · 07-15 | Psyche (open question) | "so what do we call the core? Just the core? … maybe there's an even better word" | EXPLICIT-PSYCHE **open question** | — | Questionnaire Q3 |
| A1 · 07-13 22:01/22:05 | generalist (schema-codex) | `nomos-macro-model-v1.md` (commits `4be37999a`, `a1dc7b351`) — headless declarations, inline-struct input `{ Name Type }`, capitalized macros, named/structural kinds | Report = AGENT work; its rulings cite prior-session psyche | prior session | Kept-as-is by up-close supersedence map |
| A2 · 07-14 22:32:06 | generalist | `syntax-recrystallization-audit-v1.md` **and** `core-first-architecture-v1.md` both land in whole-working-copy commit `827eb2c3` | IMPLEMENTED-FACT (artifacts) | — | Confirms the trace note that core-first was swept into the peer commit |
| A3 · 07-14 23:40 | generalist | `shared-codec-library-v1.md` + `logos-rust-lowering-v1.md` first appear in `28601d88e`; lowering titled commit `791a0c13` (23:40:55) | IMPLEMENTED-FACT (artifacts) | — | — |
| A4 · 07-15 11:47:29 | skill-editor | Spirit principle-over-substance + decision-slate doctrine (primary `e74f51de`, skills `77280a2d`) | IMPLEMENTED-FACT (manifests L9.4/L9.5) | depends L9 | Slate protocol now in skills |
| A5 · 07-15 11:51:20 | generalist | `up-close-design-v1.md` lands (`7f2782ac3`), with supersedence map | AGENT work, UNREVIEWED | depends L9/L10/L11/L12 | Consolidation surface; psyche has not read it |

## 2. Subagent / worker trace

"Reviewed by psyche" counts **only** slate-answered items; reports themselves are
UNREVIEWED ("I dont really read reports," L9.2). All commits on primary `main`
unless noted; nota work on `origin/next-gen`, unmerged.

| Worker (agent) | Task | Timing | Output artifact | Psyche-reviewed conclusions? | Commits | Superseded-by |
| --- | --- | --- | --- | --- | --- | --- |
| Syntax recrystallization auditor (generalist) | Text-syntax audit + recrystallization | 07-14, done 22:32 | `syntax-recrystallization-audit-v1.md` | Its slate (a–g) is **non-rejected only** (bead .9); readings non-rejected (.8) | `827eb2c3` (whole-copy) | up-close §0 (partial) |
| Core-first architecture auditor (generalist) | Core-first stack audit | 07-14, done 22:32 | `core-first-architecture-v1.md` | Decisions 1,2 accepted (L3,L2); 5–7 parked; storage props non-rejected (.10) | swept into `827eb2c3` | up-close keeps §2.6 |
| Management-skill hardening (skill-editor) | Harden reply-pacing (L0) | 07-14 22:27 | skills `8e1451a1`, primary `a469e2fe` | Manifests an EXPLICIT-PSYCHE directive | `a469e2fe` | — |
| Shared-codec library designer (generalist) | Repetition survey + 4-crate library (L5/L6) | 07-14, done 23:40 | `shared-codec-library-v1.md` | Direction accepted **gated** (L9.1); design UNREVIEWED | `28601d88e` | up-close §0 (§2.2–2.5, decisions 7,8) |
| Logos→Rust lowering researcher (generalist) | Rust-as-data lowering (L4) | 07-14, done 23:40 | `logos-rust-lowering-v1.md` | Direction accepted **gated** (L9.3); design UNREVIEWED | `791a0c13` | up-close §0 (§1,§2,§6) |
| Spirit principle + slate doctrine (skill-editor) | Manifest L9.4/L9.5 | 07-15 11:47 | skills `77280a2d`, primary `e74f51de` | Manifests EXPLICIT-PSYCHE | `e74f51de` | — |
| Tracker weaver | Record non-rejection + psyche-only questions | 07-15 | beads .8/.9/.10 (non-rejected), .11/.12/.13 (psyche-only), .14 (hygiene) | n/a (records state) | beads | — |
| Up-close designer (1st launch) | — | 07-15 | none (died on harness glitch, zero tool uses) | n/a | none | relaunched |
| Up-close designer (relaunch, generalist) | Code-level reconciliation + Codex fold | 07-15, done 11:51 | `up-close-design-v1.md` | UNREVIEWED (report) | `7f2782ac3` | — (latest) |
| Prior session | epic primary-56d1 (+7 children); nota next-gen pushed unmerged; pretty-printing landed | ≤07-13 | design-v0.md etc. | baseline | `39b34dc9d`+ | partially by up-close map |

## 3. The 24-item ruling-status audit

Format: **status** — evidence. "Accepted" = psyche ruling; "non-rejected" =
`AGENT-PROPOSAL` explicitly not accepted; "implemented" = `IMPLEMENTED-FACT`;
"proposed" = `AGENT-PROPOSAL`.

1. **Every Core* stringless via NameTable** — **Accepted (EXPLICIT-PSYCHE, L1)**;
   **NOT implemented**: schema repo is `Name(String)` string-bearing
   (schema.rs:15), no `NameTable` (absent); schema-language has `CoreType`
   (core.rs:452) but still stringful. `IMPLEMENTED-FACT`: unbuilt.
2. **Identity = domain-separated, layout-tagged BLAKE3 over Core rkyv, excluding
   NameTables** — **Accepted (ACCEPTED-PROPOSAL, L2)**; **NOT implemented as
   specified**: current `TrueSchema::content_hash` is blake3-over-rkyv,
   domain-separated (identity.rs:71–75,158–165) but pre-image **includes** names
   ("Any edit… moves this address," identity.rs:161). Rename-stable target unbuilt.
3. **Rename is Core-hash-stable** — **Accepted (implied by L2)**; **contradicted by
   current code** (rename moves the hash today). Target, not fact.
4. **CoreNomos durable at rest** — **Accepted (ACCEPTED-PROPOSAL, L3)**; unbuilt
   (Nomos component not yet created).
5. **Complex Core types associated by stable identity with structural
   parsing/formatting tables** — **Accepted in principle (EXPLICIT-PSYCHE, L7)**.
   Partial substrate exists: nota `StructuralMacroNode::structural_variants()`
   (macros.rs:1261/1266) is a per-type variant table, but keyed by trait method,
   not external stable identity. Sidecar-by-`CoreTypeId` is `AGENT-PROPOSAL`
   (up-close §4.3).
6. **A structural entry bidirectionally expands raw→Core and collapses Core→canonical
   text** — **Accepted in principle (EXPLICIT-PSYCHE, L7 "both encoding and
   decoding")**. Today decode/encode are two hand-kept bodies
   (`NotaDecode`/`NotaEncode`, codec.rs:119–125); one-entry-both-directions is
   `AGENT-PROPOSAL` (shared-codec decision 7).
7. **Expected type chooses the entry; input never chooses its own type** —
   **Accepted (EXPLICIT-PSYCHE ruling 5, handover; L7)**; **implemented** in nota
   (raw parser discovers structure, codec dispatches by expected type;
   next_gen_grammar tests). Solid.
8. **Structural entries are declarative data, not arbitrary parsing code** —
   **`AGENT-PROPOSAL` (Codex, L12; up-close §4.1)**. Nota's `Pattern`/`AtomShape`/
   `DelimitedShape` (macros.rs:525/623/804) are already data-shaped, but "no
   arbitrary code" as a design law is unruled.
9. **Interpreted evaluation + generated codecs explicitly accepted?** — **NO.**
   `AGENT-PROPOSAL` (Codex triad, L12; up-close §4.4/§4.5, fork C). Unread-in-detail.
10. **Structural programs vs Nomos transformations: two kinds of one macro concept,
    or separate?** — **UNRULED / open.** Codex wants "macro" reserved for Nomos;
    psyche's own words unified them ("structural-expectations-macro," L6). L13
    "structural form" leans toward separating the *name*, but is confirmation-seeking.
    Questionnaire Q2.
11. **Structural tables independently versioned/hash-addressed sidecars, excluded
    from Core identity?** — **`AGENT-PROPOSAL` (up-close §4.3, "resolved by
    derivation")**. Follows *from* accepted L2 but the sidecar mechanism itself is
    unruled.
12. **Accepted crate split (content identity vs NameTable ownership)** — **Direction
    accepted, gated (ACCEPTED-PROPOSAL L9.1)**; the concrete four crates are
    `AGENT-PROPOSAL`: `content-identity` (rkyv+blake3, `ContentHash<Domain>`) ←
    `name-table` (`Identifier`+`NameTable`) ← `raw-discovery` (nota `Block`) ←
    `structural-codec` (Textual vocabulary + evaluator + sidecar). Names are proposals.
13. **Raw grammar profiles / document-kind selection / new glyphs need explicit
    profile revisions** — **`AGENT-PROPOSAL` (Codex + up-close §4.2/§5,
    `RawProfile`/`GlyphSet`/`ProfileRevision`)**. Unruled.
14. **`$` ownership and current Nomos escape ruling** — **non-rejected
    (`AGENT-PROPOSAL`, bead .9 items c/f)**: `$` sigil, Nomos = NOTA delimiters + one
    `$` token. `IMPLEMENTED-FACT`: nota lexer still treats `$`/`<`/`>` as bare-safe
    (D7); escapes do not yet bind. Not accepted.
15. **Right-assoc dot / dotted-float reconstruction / period-string escaping** —
    **`IMPLEMENTED-FACT` on next-gen** (parser.rs right-assoc; codec.rs float rejoin;
    `(| |)` strings) **but non-rejected, NOT accepted** (bead .8). The delimiter
    *reshuffle* itself is covered by handover ruling 24 (EXPLICIT-PSYCHE), but the
    three specific readings are held for review.
16. **`StructuralMacroNode` canonical form + compatibility** — **`IMPLEMENTED-FACT`:
    still the headed `(Head body)` parenthesis form** (derive emits
    `headed_parenthesis`/`pascal_headed_parenthesis`, derive/src/lib.rs:1084–1120;
    D8), the lone construct not migrated to dotted. Converting it to dotted is
    **non-rejected `AGENT-PROPOSAL`** (slate a, bead .9). Full machinery present
    (`StructuralVariantSet`:436, `validate_no_silent_conflicts`:486/1029).
17. **Delimiter semantics across NOTA/Schema/Nomos/Logos** — **Accepted in
    principle (handover "delimiter principle" ruling 24, EXPLICIT-PSYCHE)** and
    **implemented on next-gen** (`{}` struct, `[]` vector, `Map.( … )`, `Some.payload`).
    Docs are stale ([LEANING]); nota `ARCHITECTURE.md` still mis-describes maps (D10).
18. **"Many forms" ruling (Textual, TextualRust, foreign forms, custom leaves,
    `syn`)** — **Accepted (EXPLICIT-PSYCHE, L11)** for the many-forms *principle* and
    (L13) the `Textual*` name. The concrete `TextualForm` trait, `TextualRust` via
    `syn`/prettyplease, and custom-leaf codecs are `AGENT-PROPOSAL` (up-close §6,
    lowering §6).
19. **Logos 1-to-1 with Rust; binds Core not literal text** — **Accepted
    (EXPLICIT-PSYCHE, handover + design-v0 §1.2)**. The "binds Core, text is a
    projection/codec" reading is accepted (L10/L11). Emitter today is `TrueSchema`-in,
    `IMPLEMENTED-FACT` shows compute-at-projection (derives, visibility) which the
    1-to-1 ruling forbids — a gap, not a ruling conflict.
20. **Visibility representation + field-name elision/derivation** — **Accepted:
    visibility is a modifier field, no type proliferation (EXPLICIT-PSYCHE ruling 2)**;
    field name stored in Core, elided in text only (`IMPLEMENTED-FACT` gap: emitter
    computes visibility via `references_private_type`, lib.rs:1640–1691). Text-side
    snake_case elision is `AGENT-PROPOSAL` detail (D2 resolution), consistent with rulings.
21. **Schema unit, split/merge identity, allocation-domain semantics** — **OPEN /
    blocked-on-psyche** (bead primary-56d1.11, type `decision`). No ruling exists.
    Questionnaire Q5.
22. **Bootstrap / self-hosting trust boundaries** — **Partially accepted**: staged
    Phase A–D bootstrap with goldens-as-oracle is design-v0 §4 (EXPLICIT-PSYCHE
    oracle ruling). Phase D self-hosting (dialects = CoreNomos packages) is accepted
    in principle; the trust boundary of an in-runtime evaluator is `AGENT-PROPOSAL`
    (fork C). Bootstrap **question 2 is LOST** (bead .12, unrecoverable).
23. **Accepted implementation ordering (content-identity vs structural front-end
    first)** — **`AGENT-PROPOSAL`, unresolved**: the library "Phase L: identity
    first" vs Codex "structural front end first." The up-close §8.3 reconciliation
    (L1 identity → L2 name-table → L3/L4 front end → B/C/D) is agent-derived, unruled.
24. **Spirit's role in the PoC + isolated deploy/rollback posture** — **No session
    ruling.** Spirit appears only via the L9.4 principle-over-substance doctrine and
    the `o2cd` epic (separate Spirit-consolidation work). No evidence Spirit is a
    PoC component; isolated-deploy posture is unaddressed. Questionnaire Q6 (only if
    he intends Spirit in the PoC).

## 4. Source and work inventory

**Authoritative vs stale reports.**

- **Latest consolidation:** `up-close-design-v1.md` (07-15) carries the supersedence
  map and is the current agent pickup point — but UNREVIEWED by psyche.
- **Superseded-in-part** (per up-close §0): `shared-codec-library-v1.md` §2.2–2.5 &
  decisions 7/8; `logos-rust-lowering-v1.md` §1/§2/§6 (True→Textual, RustShape→
  TextualRust). Their *evidence* sections (surveys, worked examples) are kept.
- **Partially superseded baseline:** `design-v0.md` (07-11) and earlier
  (`architecture-v0.md`, `nota-grammar-revision-v0.md`, `syntax-mockup-v0/1/2.md`).
  The reshuffle they mark `[LEANING]` has LANDED — treat code as ground truth.
- **Contradictory, NOT authority:** `reports/logos/samples/` holds **three
  coexisting Nomos syntaxes** — `types-section.nomos` / `v2-nomos-macros.nomos` (v0
  strawmen) vs `v1-nomos-bracket.nomos` / `v1-nomos-sigil.nomos`. Bead .14 tracks
  the hygiene pass (blocked on psyche review). Do not cite samples as settled.
- **Kept as-is:** `nomos-macro-model-v1.md` (inline-struct input, capitalized macros).

**Recent Claude-authored edits (this session, primary `main`):** `827eb2c3`
(syntax + core-first reports), `28601d88e`/`791a0c13` (shared-codec + lowering),
`7f2782ac3` (up-close), `a469e2fe`/`e74f51de` (skills manifests). Prior:
`4be37999a`/`a1dc7b351` (nomos model), `39b34dc9d` (design-v0).

**Repos and branches (all untracked under `repos/`, detached/no-branch HEADs).**

| Repo | HEAD | Ver | State relevant to PoC |
| --- | --- | --- | --- |
| nota (`repos/nota`) | `f8de7a5` (main) | 0.7.0 | **Base clone is pre-reshuffle.** 3-variant `Block`; `split_at_first_dot` present |
| nota worktree (`agent-worktrees/…/NotaNextGen`) | next-gen (~`08ce05c`) | 0.8.0 | **Design ground truth.** 4-variant `Block` (`Application`:72); reshuffle+right-assoc dot+`(||)` landed & tested; only `split_text_at_first_dot`. **Unmerged** (primary-z4s9) |
| schema | `36a79b7` | 0.2.0 | `TrueSchema` string-bearing (schema.rs:464); `Name(String)` (~137 sites, not 123); no `CoreSchema`/`NameTable`; blake3-name-bearing hash. cargo check clean |
| schema-language | `59d59ac` | 0.2.0 | **`CoreType`/`CoreSchema`/`CoreReference` DO exist** (core.rs:452/119/718) with projection-by-kind (schema.rs:2372 "never on a head string"). Still stringful. cargo check clean |
| schema-rust | `87de872` | 0.8.0 | Token emitter (`TrueSchema`→`RustModule`→prettyplease); compute-at-projection (lib.rs:1596–1691). **Goldens = 10,779 lines / 8 files.** cargo check clean |
| sema-engine | `fa3a822` | 0.7.0 | **Already Core-first.** rkyv portable, blake3-over-rkyv, storage layout v5 staged upgrade (engine.rs:61), ≥6 `[u8;32]` digest newtypes (five named + `ViewDigest` fold.rs:42). Successor stored-record identity basis **explicitly pending** the sema.schema design (ARCHITECTURE.md:654) |
| signal-schema | `e8f06cf` | 0.1.0 | Text payloads: `LoadPackage` carries `SchemaModuleSource{ schema_text: SchemaText }` (nested); `EmitRust` req + `RustEmitted{ rust_text }` reply. No Core/NameTable exposure |
| signal-frame | `519b4c0` | 0.3.0 | The single shared frame codec (`signal_channel!` macro); consumed by 89 Cargo.toml refs. The "17 generated copies" are in the signal-* *consumers*, not here |

**Pushed vs local-only:** all primary report/skill commits pushed to `main`. nota
next-gen **pushed to `origin/next-gen`, unmerged**. Schema-family repos are at
older pushed HEADs (07-07 → 07-11), untouched this session.

**Tracker (epic primary-56d1, 0/14 complete).** Non-rejected review pile: **.8**
(three readings, blocks z4s9), **.9** (syntax slate), **.10** (storage props).
Blocked-on-psyche: **.11** (schema unit — decision), **.12** (lost bootstrap Q2 —
decision), **.13** (sema.schema doc-kind + record-identity, blocked by .11/.12),
**.14** (reports hygiene, blocked on up-close review). Merge gate **primary-z4s9**
depends on .8. Seven prior children (.1–.7) still open.

**Compilation/test evidence.** nota next-gen: full test suite + clippy + fmt green
locally (per z4s9 notes); `nix flake check` blocked by the down substituter
`nix.prometheus.goldragon.criome` — so byte-exact `cargo test` is inner-loop
evidence only, durable flake-check evidence is gated (do not fix the substituter).
schema/schema-language/schema-rust `cargo check` clean this session.

**Unfinished / unreviewed:** every design report (psyche reads none); the nota
merge; the entire four-crate library and the Nomos/Logos components (unbuilt); the
Codex triad rulings; the two blocked psyche-only questions.

## 5. Vision reconstruction

### A. Settled current psyche vision (EXPLICIT-PSYCHE + ACCEPTED-PROPOSAL only)

- **The Core is the substance; text is a bridge.** The strictly-typed true-binary
  (rkyv-portable) in-memory/in-database representation — historically **sema** — is
  "the most essential way to think of and handle/edit this language-system." Text
  serves viewing, LLM interaction, and bootstrap compiling until in-daemon Core
  editing, snapshotting, version-control, and predictable programmatic
  format-upgrading mature. *(L0, verbatim.)*
- **"Rust is our assembly language."** Logos is 1-to-1 with Rust; the fixed
  lowering is the small kernel every dialect reduces into. *(L0 + handover.)*
- **The stack is NOTA → schema → Nomos → Logos → generated Rust → rustc**, with
  macros defining lowering in two kinds (named + structural) and Nomos headless.
  *(Handover.)*
- **All `Core*` are stringless and use the corresponding NameTable.** "In fact i
  now seeing a pattern; this could go in a library." *(L1.)*
- **Core identity is blake3 over the stringless Core rkyv bytes, NameTable
  excluded, layout-version-tagged, so rename is hash-stable.** *(L2, accepted.)*
- **Nomos is stateful at rest — a CoreNomos macro-package store, symmetric with
  schema and logos.** *(L3, accepted.)*
- **One shared encode/decode surface.** Agglomerate the `split_at_first_dot`-family
  and every parsing aspect (delimiters, structural-expectation queries) into a
  shared library/design surface. *(L5/L6.)*
- **Complex Core types are associated with their structural-parsing table for the
  next block, and that one table drives BOTH encode and decode.** *(L7.)*
- **The text side is renamed `Textual` and has many forms.** "true made no sense
  for any of them. It's just textual." CoreLogos is viewed through both a Textual
  Logos and a Textual Rust form-tree; this "opens us emitting other languages than
  rust from logos." *(L10 → L13 rename settled; L11 many-forms.)*
- **Visibility and field names are data, not proliferated types or
  projection-time computation** — one modifier field; nothing materializes at
  projection. *(Handover ruling 2; design-v0 §1.2.)*
- **Expected type at every boundary; the parser never classifies** — floats,
  variants, generics resolved by expected type, not lookahead. *(Handover ruling
  5; implemented and tested.)*
- **The delimiter reshuffle and the goldens-as-oracle bootstrap are authorized.**
  Wave-one includes the reshuffle (ruling 24); macro-produced Logos must lower to
  the Rust schema-rust already emits (design-v0 §4). *(Note: the *specific* landed
  readings still sit in the non-rejected pile — §B.)*
- **Process/Spirit doctrine:** reports are not his surface ("I dont really read
  reports"; don't grow stale design); Spirit records principle, never
  implementation substance. *(L9.2, L9.4.)*
- **The recrystallization is authorized at any rewrite magnitude.** *(L0.)*

### B. Strong but unaccepted candidates (the awaiting-ruling pile)

- **The three implemented next-gen readings** (right-assoc dot; floats-from-dotted;
  `(| |)` period-strings) — landed and green, **non-rejected** (bead .8).
- **The syntax slate a–g** — `StructuralMacroNode`→dotted; no fourth escape (name
  synthesis via derived-name rule); `$` sigil; meta-types shared with schema;
  visibility outer as right-assoc application; Nomos = NOTA delimiters + `$`;
  `Literal.( rustfmt.skip )` as dotted path — **non-rejected** (bead .9).
- **The storage proposals** — format-upgrade modeled on sema-engine's layout
  upgrade; NameTables as co-versioned stored siblings — **non-rejected** (bead .10).
- **The four-crate library design** (content-identity / name-table / raw-discovery
  / structural-codec) — direction accepted, concrete design gated & UNREVIEWED.
- **The lowering slate A–H** — `ProjectRust` domain trait; prettyplease sole
  formatter; stored visibility/derives; two-way `syn` codec; goldens as two-way
  harness — direction accepted, concrete design gated & UNREVIEWED.
- **The Codex recrystallized pipeline (triad)** — declarative structural programs +
  one trusted evaluator + generated codecs + conformance; versioned raw profiles;
  external sidecar keyed by `CoreTypeId`; profile-vs-typed split; branch reorder —
  **all `AGENT-PROPOSAL` (Codex), unread-in-detail.**
- **Evaluator-in-runtime** (fork C) — ship the interpreter in production so dialects
  add forms with zero codegen — `AGENT-PROPOSAL`, a standing architecture commitment.
- **The reconciled phase order** (identity-first then structural front end) —
  `AGENT-PROPOSAL` reconciling the two accepted-in-direction slates with Codex.

### C. Conflicts, losses, unknowns

- **CONTRADICTION (resolved): golden line count.** ~9,000 (brief) vs ~11,700
  (reports) — measured **10,779 / 8 files**. Both prior numbers wrong.
- **Cross-branch citation discrepancies (resolved):** `split_at_first_dot` (main
  clone) vs `split_text_at_first_dot` (next-gen) — both real; `Block` 3-variant
  (main) vs 4-variant with `Application` (next-gen) — both real. The reports
  silently cite different checkouts as "current."
- **FALSIFIED premise:** Codex's "13 schema compilation errors" — no such errors on
  the checked-out state (twice verified). May reference an unmerged branch (a
  dependency-portability flag) — `UNKNOWN` which branch.
- **PARTIAL count:** `Name(String)` sites ~137, not the reported 123 (same order).
- **Digest newtypes:** "five duplicate" is real but non-exhaustive — a sixth
  (`ViewDigest`) exists.
- **LOST (UNKNOWN, unrecoverable): bootstrap question 2** — only its opening
  survives ("how do text edits become daemon edits…"); must be restated by the
  psyche from memory (bead .12). Blocks .13.
- **OPEN (blocked-on-psyche): the unit of "one schema" + split/merge identity**
  (bead .11), and the **sema-engine successor stored-record identity basis**
  (bead .13, pending .11/.12 and the sema.schema doc-kind).
- **UNRULED terminology:** "structural form" vs "structural macro" (confirmation-
  seeking, L13); "symbolic form" (musing); and the **Core-side name** ("what do we
  call the core?", open question).
- **The Core scaffolding is split across two schema repos** — `schema-language` has
  `CoreType`/`CoreReference` (projection-by-kind), while the deployed `schema` repo
  is `TrueSchema`/string-bearing. The core-first report checked `schema` and
  reported "CoreSchema does not exist"; the up-close report found `CoreType` in
  `schema-language`. Both true, different repos — worth naming so the PoC does not
  "invent CoreSchema" that half-exists.

## 6. Proof-of-concept proposal (compressed; NO implementation)

**Smallest coherent component set** proving the settled vision end-to-end on the
narrowest slice (`CommitSequence`/`DatabaseMarker`, already the shared worked
example across every report):

1. `content-identity` — portable rkyv bound + `ContentHash<Domain>` (layout-tagged,
   NameTable-excluded), extracted from sema-engine (its locked-byte tests prove the
   lift). Proves ruling 2/3.
2. `name-table` — `Identifier(u32)` + append-only `NameTable` with continuous
   schema→logos extension. Proves ruling 1.
3. `raw-discovery` — nota's `Block` + recognizer lifted, structure-only. Proves
   ruling 7 (parser never classifies) reusable.
4. `structural-codec` (thin slice) — one `StructuralForm` vocabulary + a single
   trusted evaluator running one entry **both directions**, over the two worked
   types only. Proves rulings 5/6.
5. CoreSchema slice — stringless-ify the *existing* `schema-language` `CoreType`
   for the two types (do not invent it).
6. TextualLogos + TextualRust slices — the two-form family over one CoreLogos,
   TextualRust via `syn`/prettyplease. Proves L11 many-forms + L4/L19 lowering.

**Epic / branch dependency graph** (all as feature worktrees off clean `main`,
disposition-tracked; nothing merged until psyche acceptance):

```
[ (nota-next-gen-merge            proves reshuffle+dot rulings green   gate: primary-z4s9 / bead .8 blessing)
  (content-identity  ← sema-engine  proves layout-tagged NameTable-excluded hash on locked bytes)
  (name-table        ← content-identity  proves continuous stringless identifier space)
  (raw-discovery     ← nota           proves structure-only recognizer reused)
  (structural-codec  ← raw-discovery + name-table  proves one bidirectional entry, evaluator==intent)
  (coreschema-slice  ← schema-language + name-table  proves stringless CoreSchema for 2 types)
  (textual-forms     ← structural-codec + coreschema-slice  proves TextualLogos + TextualRust one Core)) ]
```

**What each branch proves** and **acceptance gates:**

- Identity branch: byte-stable hash unchanged under rename; layout-tag re-fold
  deterministic. Gate: sema-engine locked-byte tests stay green.
- structural-codec branch: **conformance interpreter == codegen** on the two types;
  **byte-exact round-trip** decode→Core→encode.
- textual-forms branch: **byte-exact goldens** — TextualRust encode of the two Core
  values equals the verbatim schema-rust goldens; **two-way `syn` harness** decodes
  those goldens back to the same Core.
- Global gate: every phase reproduces the schema-rust goldens byte-for-byte
  (design-v0 §4, EXPLICIT-PSYCHE oracle). Durable evidence gated on the substituter
  (inner-loop `cargo test` meanwhile).

**Reuse vs rewrite.** Reuse: sema-engine (already Core-first — the template),
signal-frame (shared codec), nota raw parser, schema-language `CoreType`,
schema-rust goldens (as oracle, unchanged), prettyplease. Rewrite: nota codec
center-of-gravity (rkyv-primary), schema Core-ification, signal-schema payloads.
Build new: the four crates, Nomos/Logos components, format-upgrade for language
Cores. **No implementation is proposed here — this is the shape only.**

## 7. Final prioritized questionnaire

Only decisions genuinely needing psyche authority. Each recommendation is a
**recommendation, not a ruling.**

**Q1 — Bless or reject the three implemented next-gen readings (right-assoc dot,
floats-from-dotted, `(| |)` strings), clearing the nota merge gate (z4s9).**
*Recommendation:* bless all three — landed, tested, mutually reinforcing, and the
keystone (right-assoc dot makes visibility a modifier for free). But this is your
explicit non-rejection to convert to a ruling; nothing merges until you do.

**Q2 — Macro vs "structural form": final terminology.** Do we (a) reserve "macro"
for Nomos and name the parser-side data `StructuralForm`, splitting into two
concepts (TextualForm = per-language view tree; StructuralForm = the sidecar
conversion-pattern), or (b) keep your earlier unification
("structural-expectations-macro," "a dialect is a macro package")?
*Recommendation:* adopt the two-concept split with the name **structural form** —
it matches your L13 lean and separates "how a form looks" from "how expectation
lands on the next block." Confirmation only; you said "Is that what you mean?" and
the term is not yet ruled.

**Q3 — The Core-side name.** You asked "what do we call the core?" Candidates, all
**proposals**: **`sema`** — your own original name for "the core true/logical/
strict-binary part" (the engine is already named for it); **`Core`** (plain);
**`Code`** (you floated it); **`semantic form`** — the natural pair to a
"symbolic form" text side if you adopt that; **`symbolic`/`semantic`** paired.
*Recommendation:* **`sema`** for the Core substance, pairing with **`Textual`** for
the text side (sema ↔ textual), since it revives your own coinage and the database
engine already carries the name. Mark as proposal — this is yours to name.

**Q4 — Does the trusted evaluator ship in the runtime, or only as the conformance
oracle (fork C)?** *Recommendation:* ship it in the runtime — it is the difference
between "dialects are data" (add a form, zero codegen) and "dialects need a codegen
step," and the concrete form of your "infinitely programmable" instinct. Genuine
because it is a standing performance/architecture commitment (an interpreter on the
hot path for un-codegen'd types).

**Q5 — Disposition of the non-rejected pile (beads .8/.9/.10).** These will decay
into silent acceptance if left. Do you want to (a) rule them item-by-item now, (b)
defer explicitly with a review date, or (c) fold them into the PoC branch reviews
as each is exercised? *Recommendation:* (c) — rule each reading/slate item at the
point its PoC branch proves it, so acceptance rides on working evidence, not on a
report you won't read.

**Q6 — Restate lost bootstrap question 2, and define the schema unit.** Bead .12's
question is unrecoverable from artifacts ("how do text edits become daemon
edits…") and must come from your memory; bead .11 needs the unit of "one schema"
plus split/merge identity semantics. Both block the sema.schema doc-kind and
sema-engine's successor record-identity basis (.13). *No recommendation* — these
require your intent, not an agent's guess.

**Q7 — Spirit's role in the PoC and its deploy/rollback posture (item 24).** No
session evidence places Spirit inside this PoC. *Recommendation:* keep Spirit out
of the language-PoC scope (it is a separate consolidation epic, primary-o2cd);
raise this only if you intend the PoC to exercise Spirit — in which case an
isolated deploy/rollback posture would need defining. Flagged, not assumed.

## 8. Sources

Design corpus (this workspace, read this session):
`reports/logos/up-close-design-v1.md`, `core-first-architecture-v1.md`,
`logos-rust-lowering-v1.md`, `shared-codec-library-v1.md`,
`syntax-recrystallization-audit-v1.md`, `nomos-macro-model-v1.md`, `design-v0.md`;
`reports/logos/samples/`. Tracker: epic primary-56d1 (.1–.14), primary-z4s9.
Manager-witnessed session ledger (brief) for chat events L0–L13.

Code ground truth (read-only, this session; no edits, no branch switches):
nota `repos/nota` main `f8de7a5` (0.7.0) and worktree next-gen `08ce05c` (0.8.0,
`Block`:57, `StructuralMacroNode`:1261, `split_text_at_first_dot`:572); schema
`36a79b7` (0.2.0, `TrueSchema`:464, `Name`:15, identity.rs:71–165); schema-language
`59d59ac` (0.2.0, `CoreType`:452, `CoreReference`:718, schema.rs:2372);
schema-rust `87de872` (0.8.0, goldens 10,779 lines/8 files, emitter
lib.rs:1596–1691); sema-engine `fa3a822` (0.7.0, layout v5 engine.rs:61,
ARCHITECTURE.md:654); signal-schema `e8f06cf`; signal-frame `519b4c0`. Commit
timestamps from jj/git. Repositories under `repos/` are untracked.
