# Spirit redesign — live deployment audit (0.9.0)

Independent audit of the deployed Spirit `0.9.0`, run against the **running daemon** (not
operator's report alone), per audit-precision: what the production path *does*. Operator
deployed spirit `ea92ecf` + CriOMOS-home `9ad4e2f`; migration ran on activation.

## Verdict

**The redesign is live and the deployment is faithful and correct.** Every design behavior
verified against the running daemon. Two follow-up findings — **neither blocks**, both are
quality/correctness improvements; finding 1 is the more urgent (it degrades guardian
judgment, not just output size).

## Verified live

| Check | Evidence (live) | Verdict |
|---|---|---|
| Version | `spirit Version` → `(VersionReported (0.9.0 ...))` | ✓ |
| No data loss | `Count` (cert≥Min) = **1407**; migration `(Upgraded (1452))` | ✓ |
| Migration faithful | `kasm` (was `Craft(Architecture)`) → `(Technology (Software (Engineering SoftwareArchitecture)))`; `mn3k` (was `Craft(Schema)`) → `(Technology (Software (Data SchemaEvolution)))`; `Knowledge(Taxonomy)` preserved | ✓ |
| Nested schema deployed | `domain.schema`: `Technology = Hardware + Software`; the two equivalences (`Networking`, `DatabaseSystems`) | ✓ |
| Scope prefix-matching | `(Technology)`→7, `(Technology Software)`→7, `(Technology Software Engineering)`→5 (incl. `kasm`) | ✓ |
| Guardian gate (reject) | a deliberately non-durable `Propose` → `GuardianRejected NonIntent` via live DeepSeek; count held at 1407 | ✓ |
| Guardian gate (accept) | a genuine `Record` accepted (`34hu`) under a nested domain | ✓ |
| Services | `agent-daemon` + `spirit-daemon` active, `NRestarts=0`; old `persona-spirit-*` gone (operator-reported) | ✓ |

The migration is the standout — the whole 1407-record store re-encoded through the new
nested vocabulary with the former-Craft software records correctly re-tagged, zero loss.

## Finding 1 — guardian retrieval bundle is unbounded and over-inclusive (urgent)

Operator flagged this; the audit confirms and diagnoses it precisely, and it is **worse than
"output too big" — it degrades verdict reliability.**

**Root cause (code):**
- `guardian_relevance_score` (`store.rs:1333`) gives **`+1` for merely sharing the same
  `Kind`** (`store.rs:1355`), and `GuardianRecordCandidate::new` (`store.rs:1138`) admits any
  record scoring **`> 0`**. So **every record of the same Kind enters the bundle** — and Kind
  has only 5 values, so that's a large fraction of the store.
- `guardian_records_for_entry` (`store.rs:~627`) sorts by score but **applies no cap**.
  `GUARDIAN_RECORD_LIMIT = 64` exists (`store.rs:51`) but is used **only** in the
  `CollectRemovalCandidates` branch (`store.rs:615`) — never on the entry/propose path.
- Net: the bundle ≈ all same-kind records (+ domain/keyword/text matches), uncapped → hundreds
  of records, dominated by the `(Information Documentation)` catch-all (~1100 records, the
  deferred re-tag).

**Live evidence of the consequence:**
- A `(Selfhood Emotion)` smoke-test `Propose` pulled a pile of unrelated
  `(Information Documentation)` schema records into the rejection — enormous output.
- A genuine `Correction` record was rejected `Duplicate` citing an **unrelated**
  beads-coordination record (`09do`, +1 same-Kind only) instead of the actual near-duplicate
  (`34hu`, exact domain+Kind match). The verdict direction was defensible, but the citation is
  unsound — the noisy bundle made the model reason over and cite the wrong record. In other
  cases that noise can flip the verdict, not just the citation.

**Fix (addressed by operator `365`; one reframe).** The real fix is **relevance-scoping**:
drop the same-`Kind` floor (`+1 if kind == kind` admitted a fifth of the store on no real
relevance) so only genuinely-related records — same/equivalent domain, shared keyword/text —
enter. Operator did this in `365`. Plus the **corpus cleanup** (594) to shrink the
`(Information Documentation)` catch-all that makes any retrieval there huge.

The **fixed-count cap (`GUARDIAN_RECORD_LIMIT = 64`) is a backstop, not the mechanism** — and
a smell. A record *count* can silently drop a genuine duplicate that ranks 65th → a wrong
accept, the exact failure the guardian exists to prevent. It rarely bites (a true duplicate
scores high and lands in the top 64), but that is luck, not design. Recommendation: keep the
residual backstop bound by a **relevance threshold** (drop below score X), not top-N count; and
once relevance-scoping + cleanup land, the bundle is naturally small and the cap should never
bind. (This corrects report 585's "cap/rank the bundle": rank/scope by relevance, do not cap by
count.)

## Finding 2 — `DomainScope` is untyped strings; should be recursive enums

The deployed `DomainScope = DomainPath = (Vec String)` (`domain.schema:47-48`) — a flat list
of **free strings** (`[Technology Software]`). Untyped: a misspelled segment parses fine.
**Resolved design** (psyche + operator thread; records `k4zc`, `oqwb`, `izib`):

- **`Domain` is a typed recursive enum tree with mandatory subdomains all the way to a leaf** —
  a domain value is always complete: `Technology(Software(Security(AdmissionControl)))`.
- **`DomainScope` is NOT `Domain` with optional payloads.** That deadend renders ugly
  `(Technology None)` / `Some` (`oqwb`: a NOTA variant with an optional payload encodes as a
  record, not a bare atom). Instead `DomainScope` is a **separate generated prefix language over
  the same tree** — declared `DomainScope (ScopeOf Domain)`. Stopping early is the prefix
  *semantics*, not optional subdomain data.
- **Clean, fully-typed NOTA surface, no `Some`/`None`:** `Technology`, `(Technology Hardware)`,
  `(Technology (Software Security))`, `(Technology (Software (Security AdmissionControl)))`.
  Every segment a typed variant — a typo fails to parse.
- **Implementation order (operator, in progress per `365`):** schema-next gains a
  `ScopeOf`/prefix construct + recursive-enum support; schema-rust-next does recursive-reference
  boxing (`gh29`) and emits the prefix type with a clean NOTA codec; Spirit then replaces
  `DomainPath`, regenerates, and migrates.

Consistent with typed-domain-values (`skills/abstractions.md`, `rust-discipline`): no free
strings where a typed sum belongs.

## Operator-actionable

1. **Guardian bundle (finding 1):** cap `guardian_records_for_entry` at `GUARDIAN_RECORD_LIMIT`;
   drop/raise the same-Kind score floor. Small, high-leverage, fixes both output size and
   citation reliability. *Verify with the live DeepSeek suite (363).*
2. **Recursive-enum `Domain`/`DomainScope` (finding 2):** retype from `(Vec String)` to a typed
   recursive enum; a scope is an early-terminating prefix. Round-trip test the nested paren form.

## Net

The deploy is a clean success — full redesign live, migration faithful, guardian gating real
DeepSeek end-to-end. The two findings are refinements on top of a working system: tighten the
guardian's retrieval so its judgment is trustworthy (1), and make domain scopes typed recursive
enums rather than string paths (2). Neither is a regression; both raise the floor.
