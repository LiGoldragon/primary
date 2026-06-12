# Guardian-effect simulation — merge-with-importance + split

What the guardian would have done to the corpus if it had gated every record: merge same-arrow
restatements into one canonical with importance raised by repetition, and split compound records
into clean single arrows. Run over the **live rebuilt corpus** (1328), read-only, proposes only.
Workflow `wf_0a5648fa-98c`, 24 domain agents. Full proposal: `wdzqp0tiy.output`.

## The effect

| | |
|---|---|
| Start (rebuilt corpus) | 1328 |
| Merge groups | **113** (48 of size ≥3, 65 pairs) |
| Records merged away | **215** |
| Compound records split | **45** → **134** clean parts |
| **After** | **1202** |

Canonical importance after the bump: VeryHigh 25, High 48, Medium 37, Maximum 1, Low 1. The
repeated arrows *are* the important ones — restatement count and importance line up almost
perfectly, which is the whole point.

## The conviction ranking — your load-bearing principles, surfaced by repetition

These are the arrows you restated the most, across months and in different words. The guardian
would have collapsed each into one high-importance record. This ranking is something the raw
corpus never exposed — it *is*, almost exactly, the AGENTS.md hard-override list, recovered
statistically:

| Restated | Importance | The arrow |
|---|---|---|
| **15×** | VeryHigh | Schema macros are structural matching over NOTA node shape (delimiter/object-count/child-shape/symbol/position), dispatched most-specific-first — not a separate text syntax. |
| 7× | VeryHigh | Schema emits the data nouns; hand-written Rust writes only methods/logic on them, never free functions. |
| 6× | VeryHigh | Everything (macros most of all) is serializable data — pre-assembled objects read by one tiny generic interpreter, no per-macro bespoke parsing. |
| 6× | VeryHigh | Every root message carries an auto-minted origin-route return-address threading Signal→Nexus→SEMA→back so async replies correlate. |
| 6× | VeryHigh | Records carry graduated per-record privacy (a Magnitude, Zero=public default, Maximum=sealed); elevated levels need an explicit higher-clearance call — never a public/private boolean. |
| 5× | **Maximum** | A daemon never parses NOTA: it consumes a pre-encoded rkyv config, stands by when virgin, self-resumes from its store. |
| 5× | VeryHigh | Each code repo keeps main + a long-lived next branch: designers work on next/feature, operators own main and integrate. |
| 5× | VeryHigh | Nexus is the in-between mail keeper/translator: Signal-ingress → SEMA query → reply → Signal output, emitting lifecycle events. |
| 5× | VeryHigh | Model-heavy work runs on the node that owns the model cache (Prometheus), never on the workstation; the deploy pipeline must allow it. |
| 5× | VeryHigh | The lojix/Horizon rewrite charter: port lojix onto the triad-engine + schema-core stack, reach parity, cut over per node, retire the dual stack. |
| 5× | High | The @-sigil binder surface is abandoned; the authored surface is positional bracket/brace. |
| 4× | VeryHigh | Strict triad separation: SEMA owns durable state, Nexus owns decisions, Signal owns communication. |
| 4× | VeryHigh | Every agent commits and pushes at the end of every pass; uncommitted work blocks the psyche's review loop. |
| 4× | VeryHigh | An optional testing build installs actor/interface trace hooks proving Signal, Nexus, and SEMA actually fired. |
| 4× | High | Components share a universal async mail substrate: a Communicate trait over binary signal-frame with request-reply correlation + a database-marker on replies. |
| 4× | High | Component upgrades are Nix-flake-input versions: pin running-production + unstable/testing, expose the previous version, run upgrade tests as flake pipelines. |

## The splits — compounds broken into clean arrows

45 records bundled multiple arrows; the guardian would have rejected them `Compound` and asked
for the parts. Examples: `3do3` (the Rust methods rule) → Principle + Constraint + Decision;
`qmm4` → 4 (3 Decisions + a Constraint); `d42z` → 4; `vez8` → 3 Decisions. 134 clean single-arrow
records in place of 45 epics.

## The noise (excluded on apply)

A few agents emitted placeholders rather than real merges — flagged, **not for application**:
`1kfk` (×5, "REPLACE — do not apply"), `di1r` (×2, same), and a `07pn-unused-placeholder`
(ignore). ~3 of 113 groups. The apply step drops any merge whose canonical id isn't a real record
or is flagged, and I'd hand you those for a manual look rather than guess.

## What applying would do, and the reversible path

Applying = retire the 215 merged-away records (their arrows preserved in the canonical), set each
canonical's raised importance, replace the 45 compounds with their 134 split parts (new records).
Net **1328 → 1202**, via the same `meta-spirit` re-import that did the rebuild — current corpus
exported, transformed, re-imported into a fresh store, old store kept as the undo. Fully
reversible.

## Net

This is the guardian's shaping made visible: a corpus a third smaller than the original 1410,
where every record is one arrow, duplicates are collapsed, and **importance is earned by
conviction** — the things you kept coming back to float to the top by themselves. It's a proposal;
nothing is applied. The merges are the lossy part (a wrong merge buries a distinct arrow), so this
is the pass worth your eyes before it lands.
