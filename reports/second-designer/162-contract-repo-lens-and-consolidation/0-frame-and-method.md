*Kind: Frame · Topic: contract-repo audit + aggressive report consolidation · Date: 2026-05-23*

# 0 — Frame and method

## What this directory is

Meta-report per intent record 231. Six sub-agents in parallel.
Final synthesis in `7-overview.md`.

Per psyche 2026-05-23: "reread intent and new architecture
decisions. do a parallel audit and @skills/contract-repo.md - move
all old reports into re-contextualized new reports, leaving out
stale context in the deleted old versions."

Intent **362** (captured by orchestrator) supersedes /161/3's
conservative-default discipline when psyche explicitly directs
consolidation. The sweep this session is aggressive: re-contextualize
into fewer, current reports + delete stale originals.

## The contract-repo lens

`skills/contract-repo.md` is the primary audit lens. Key rules to
check against:

- **Operation roots are verbs in verb form** (Submit, Query,
  Observe, Configure, Register, Retire, Start, Stop) — not noun
  forms (Submission, Configuration, Registration)
- **Reply success variants are verb-past-tense** (Submit →
  Submitted; Register → Registered)
- **Reply rejection variants are verb-past-tense + Rejected**
  (Submit → SubmitRejected); rejection reasons are payload variants
  of a typed enum
- **Names don't repeat namespace** already supplied by crate /
  module / channel / relation / owning component / enclosing enum
- **Closed enums** — no Unknown variant; no string-typed kinds for
  lifecycle uncertainty
- **Per-relation root enums** in multi-relation contract crates
- **Contract owns both wire (rkyv) AND text (NOTA) form** of typed
  records; consumers don't carry shadow types
- **Layered effect crate pattern** for narrow-audience operations
  (signal-<consumer>) atop signal base contract
- **Kernel extraction trigger** when two domains share kernel
- **Round-trip discipline**: text → typed → text + rkyv archive
  round-trip per record kind, with canonical text examples
- **Domain-noun payloads, verb-form operation roots** (Submit
  carries Message, Configure carries Configuration)
- **Contract repos do not own daemon code, runtime, validation,
  routing, configuration, or serde** (rkyv-on-wire)

## Sub-reports + sub-agent assignments

| # | Slice | Author |
|---|---|---|
| 0 | Frame + method (this file) | second-designer (orchestrator) |
| 1 | Intent records audit through contract-repo lens | sub-agent A |
| 2 | Recent ARCH commits audit through contract-repo lens | sub-agent B |
| 3 | Consolidate /152 meta-directory | sub-agent C |
| 4 | Consolidate standalone /153-/158 reports | sub-agent D |
| 5 | Consolidate older /145, /150, /151 + /131-/144 triad audits | sub-agent E |
| 6 | Bead reference sweep + operator audit (deletion follow-on) | sub-agent F |
| 7 | Overview synthesis with visuals | second-designer (orchestrator) |

## Sub-agent contract

1. Second-designer-window sub-agent (designer discipline).
2. Stick to your slice. Don't expand scope.
3. **No sub-sub-agents** (intent 5).
4. Observe Spirit with `spirit '(Observe (Records (None None WithProvenance)))'`.
   Do NOT capture new intent (orchestrator handles).
5. `jj` HEADLESS `-m '<msg>'` form (intent 237). Never let jj open
   an editor.
6. All `nix` invocations: `--max-jobs 0`.
7. Full English names per `skills/naming.md`.
8. NOTA positional per `skills/nota-design.md`.
9. No `---` horizontal-rule lines.
10. Opaque identifiers carry inline descriptions on first chat mention.
11. Per `skills/mermaid.md`: NO `;` in sequenceDiagram Notes/messages,
    NO Unicode arrows in sequenceDiagram body, NO pipe-delimited
    labels `-->|"label"|` in sequenceDiagram.
12. Sub-report at `/home/li/primary/reports/second-designer/162-contract-repo-lens-and-consolidation/<N>-<slug>.md`.
13. Chat response per intent 232: 3-7 items balanced across (a)
    intent questions/clarifications, (b) observations/explanations,
    (c) examples/evolving picture.

## Consolidation discipline (for sub-agents C, D, E)

Per intent 362:

- **Re-contextualize** — read the old reports, extract the
  substance that is still load-bearing in 2026-05-23 context, write
  ONE consolidated report (per cluster) capturing only the
  still-relevant substance with updated cross-references
- **Drop stale** — substance that has migrated to ARCH/skills/intent
  is omitted from the new report (it lives in its permanent home)
- **Delete originals** — use `jj` to remove the old report files;
  commit per-deletion with inline -m citing intent 362
- **Verify references** — grep for the report path in other reports,
  skills, ARCH files, bead bodies. Update or note references that
  need follow-on (sub-agent F handles bead body updates)
- **Preserve competing-design alternatives per intent 229** — if a
  consolidated report contains a designer-recommended path AND a
  competing alternative, keep BOTH in the consolidated version. The
  competing-design preservation rule survives the consolidation.

## Garbage collection

Per intent 231 this directory is one session unit. When substance
migrates to permanent homes, the directory retires together.
