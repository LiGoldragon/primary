# 272 - Audit of operator-side activity vs. designer reports 260-271

*Designer audit, 2026-05-21. Surveys operator-side activity that
responds to the designer reports filed today (260-271 plus
`pi-api-surface-notes.md`) and reports findings the prime designer
will use to drive parallel reversion work. Focus: which designs need
a `-v2` bump, which to leave, which to supersede.*

## 1. Survey method and scope

The audit window is "everything filed after designer/260 hit disk at
2026-05-21 12:49". Specifically:

- All `reports/<role>/` subdirectories under `/home/li/primary/reports`,
  filtered by modification time newer than `designer/259-session-handover-2026-05-21.md`
  (the immediate predecessor of the design thread).
- `.beads/` short-tracked-item store (open issues only; nothing
  matched the 260-271 thread).
- ghq checkouts under `/git/github.com/LiGoldragon`: `persona-spirit`,
  `signal-persona-spirit`, `owner-signal-persona-spirit`,
  `signal-sema`, `signal-persona-mind`, `persona-mind`,
  `forge`, `signal-forge`, plus a fresh `ls` of the org
  to detect new triad repositories.

Each operator-side report newer than `designer/259` was read briefly
to determine its relation to a designer/260-271 design. The git log
of the listed crates was filtered to commits dated 2026-05-21T15:00+
(after /260 was filed) to find code-side responses.

Scope excludes pre-thread material the designs build on (e.g.,
`reports/system-specialist/154`, `reports/operator/150`,
`reports/second-system-assistant/7`) except where they constitute
direct antecedents the design cites.

## 2. Operator-side activity inventory

### 2a. Newer-than-`/259` reports across operator-side directories

Listed by modification time:

| Time | Path | Lane | Relation to /260-/271 |
|---|---|---|---|
| 2026-05-21 10:35 | `operator-assistant/162-persona-orchestrate-signal-executor-migration-vision.md` | operator-assistant | Predates `/260`; unrelated to this thread. |
| 2026-05-21 11:27 | `second-system-assistant/7-persona-spirit-production-user-session.md` | second-system-assistant | Predates `/260`. Establishes the deployed spirit baseline that `/260` and `/265` then test against. Not a response. |
| 2026-05-21 15:13 | `operator/151-spirit-deployed-version-and-schema-migration.md` | operator | **Direct response to `/260` + `/261`.** Cites `/261` by path; positions storage wrappers separately from signal types; proposes copy-migrate-verify-switch with sequence high-water mark. |
| 2026-05-21 16:03 | `operator/152-bird-zeus-local-update-authority-design.md` | operator | Unrelated. Bird-on-Zeus local update authority through criomos / horizon. No overlap with the schema / pi / magnitude / forge thread. |
| 2026-05-21 15:20 | `designer-assistant/143-designer-state-digest-2026-05-21.md` | designer-assistant | Designer-lane digest, not operator activity. Notes `/262` is partially superseded. |
| 2026-05-21 15:26 | `second-designer/1-real-time-intent-recording-system-2026-05-21.md` | second-designer | Designer-lane (different thread): `persona-listen` voice capture. Not operator activity; orthogonal. |
| 2026-05-21 16:07 | `nota-designer/1-protocol-adoption-and-lane-gap.md` | nota-designer | Designer-lane variant. Not operator activity. |
| 2026-05-21 16:30 | `second-designer/2-persona-orchestrate-lane-management-2026-05-21.md` | second-designer | Designer-lane. Touches persona-orchestrate; not a response to /260-/271. |
| 2026-05-21 17:39 | `nota-designer/2-bracket-string-vision-production-audit.md` | nota-designer | Designer-lane. NOTA bracket-string discipline; not operator activity. |

### 2b. Code-side activity (ghq checkouts) since /260 filed

| Crate | Commit | Date | Subject | Relevance |
|---|---|---|---|---|
| `signal-sema` | `22b036a` | 17:10 | `signal-sema: add magnitude vocabulary` | **Direct landing of `/269` design.** `Magnitude` enum with seven variants Minimum..Maximum lives in `src/magnitude.rs`, with NotaEnum + Archive + Ord derives, `as_record_head` / `from_record_head` helpers, full round-trip tests in `tests/magnitude.rs`, ARCHITECTURE.md updated, and seven magnitude record-heads added to `examples/canonical.nota`. Matches `/269` §3 exactly. |
| `signal-persona-spirit` | `8586f59` | 17:10 | `make record acknowledgements identifier-only` | Post-/260 chronologically but addresses unrelated record-acknowledgement compaction. `Certainty` enum still present in `src/lib.rs`; downstream Magnitude consumption has not landed. |
| `persona-spirit` | `0590920`, `e5c624f`, `7c2d902` | 17:14-17:26 | acknowledgement / owner-contract / client-split changes | Tracks `signal-persona-spirit` upstream changes; no schema-migration, sema-upgrade, or Magnitude work. |
| `signal-persona-mind` | — | — | (no commits since `/260`) | `ItemPriority` still lives here per `/269` finding; no migration to Magnitude has landed. |
| `forge` / `signal-forge` | — | — | (no commits since `/260`) | Both crates exist on disk with pre-thread history; the latest commits are from 2026-04-29 ("forge tooling", "forge edit", etc.). No response to `/271`'s family redesign. |
| `sema-upgrade` / `signal-sema-upgrade` / `owner-signal-sema-upgrade` | — | — | (do not exist) | `/270`'s component family is unimplemented; no crates have been created. |
| `persona-pi` / `signal-persona-pi` / `owner-signal-persona-pi` | — | — | (do not exist) | `/266`'s triad is unimplemented; no crates have been created. A `pi-delegate` repo exists in the org, but predates this thread and is unrelated. |

### 2c. Beads (`bd list`)

Fifty open issues. None match the 260-271 thread on quick scan — the
open beads are existing migration tasks (`Migrate persona-terminal
triad`, `Migrate lojix triad`, `Migrate criome triad`,
`Migrate persona-system triad`), unrelated bug reports
(Whisrs audio drops, Whisrs Opus encoding), or pre-existing design
intentions. No `magnitude`, `sema-upgrade`, `persona-pi`,
`forge-core`, or `schema-address` bead has been filed for the
new thread's work.

## 3. Per-designer-report audit rows

### 3a. `/260` - Schema migration discipline

- **Operator response found:** Yes. `operator/151-spirit-deployed-version-and-schema-migration.md` (15:13). Cites `/260` and `/261`. Tags deployed `v0.1.0` across persona-spirit + signal-persona-spirit + owner-signal-persona-spirit + nota-codec / sema / signal-frame / signal-sema / signal-executor / signal-core. Reads the deployed-vs-current diff: storage layout unchanged, wire contract gained `Topics` / `TopicCount` / `TopicsObserved`. Proposes per-component schema-version constants plus a `persona-spirit/src/schema/{current,version_1}.rs` + `migration/version_1_to_2.rs` layout, with a one-shot `spirit-migrate` maintenance binary using the same library the daemon uses. Identifies that **stored wrappers (`StoredRecord`, `StampedEntry`, table keys/names) need a separate historical record set from public signal types** — a refinement `/260` foreshadowed but did not pin down.
- **State:** Implementation proposal in prose; no schema/migration modules have landed in code yet. `/265` (master upgrade smoke test) demonstrates that the deployed redb is currently readable by the master daemon, so no urgent migration is pending — the proposal is forward-looking.
- **Implication:** `/260` remains the canonical kickoff. Operator/151 adds two facts `/260` could now absorb cleanly:
  - The split between public-signal historical types (signal crate) vs. private-storage historical wrappers (runtime crate).
  - The need for a durable commit-sequence high-water mark (sema-engine pressure point) for live-copy cutover.
- **Reversion recommendation:** **Leave `/260` v1.** It is the kickoff and properly framed the question. Update the running picture through `/270` (sema-upgrade) which already absorbs the orchestration layer, and through a fresh designer report (post-/272) that pulls in operator/151's two refinements. The thread should not bump /260 itself; it should bump the *applicable* successor.

### 3b. `/261` - Schema version surface research

- **Operator response found:** Yes, indirectly via operator/151's §"Reading designer/261" section. Operator accepts the layered recommendation (coarse component label + per-record-type machinery) and supplies the missing detail: storage wrappers need their own per-record-type machinery alongside signal types.
- **State:** Acceptance of recommendation + refinement; no code.
- **Implication:** `/261`'s layered recommendation stands. The "what does the number actually range over" question is now answered for the specific case (per-record-type at the read path; coarse per-component for talkability) and operator/151 extends this to "per-record-type across two type families - public signal types AND private storage wrappers".
- **Reversion recommendation:** **Leave `/261` v1.** The research-and-recommend shape is intact. The refinement is downstream, not corrective.

### 3c. `/262` - Content-addressable schema-layout schema

- **Operator response found:** None.
- **State:** `/262` already carries its own in-flight banner correction (lines 11-22): aski stack is past experience, not foundation. The successor is `/263`.
- **Implication:** The aski-stack-as-foundation framing is wrong per intent records 33+42. The successor `/263` does the fresh design work. The exploratory body of `/262` is largely superseded by `/263`'s framing; the residual value of `/262` is the three-layer table (user-facing NOTA / schema-layout DSL / rkyv bytes) and the schema-change classes (zero-cost / append-only / structural).
- **Reversion recommendation:** **Bump `/262` to `-v2` OR supersede entirely via `/263`.** Two options:
  - **Preferred:** Supersede via `/263` and delete `/262` outright. `/263` already declares itself the supersession in its banner. Delete `262-content-addressable-schema-layout-schema.md` in the same commit that lands the post-audit consolidation.
  - **Alternative:** Bump to `262-v2-...` that retains only the schema-change classes table and the three-layer split, and points at `/263` for the language itself. Heavier, less clean.
  - **Recommended action:** Supersede entirely. The retained content is small enough to absorb into `/263` directly.

### 3d. `/263` - Schema specification language design

- **Operator response found:** None.
- **State:** Fresh fork after `/262`'s correction. Specifies the workspace Rust subset constraints (no tuples; no in-schema generics; NOTA-flavoured positional records; content-addressable canonical encoding; layout-bound annotations first-class).
- **Implication:** Implementation has not started. The schema generator, diff classifier, and daemon-side address comparator are all unimplemented.
- **Reversion recommendation:** **Leave `/263` v1.** No new evidence has accumulated to revise it. The downstream consumers (`/270` sema-upgrade) reference it as the layer they consume; no contradiction yet.

### 3e. `/264` - Designing protocol and role spaces

- **Operator response found:** None directly. `second-designer/2-persona-orchestrate-lane-management-2026-05-21.md` (16:30) and `second-designer/1-real-time-intent-recording-system-2026-05-21.md` (15:26) operate within the "second-designer" lane that `/264`'s section on parallel-main lanes implicitly authorises, but neither cites `/264`.
- **State:** Settled material (per-role protocols, designer-as-bridge workflow, role-label-driven interpretation) is acted on. Speculative material (Git-isolated role-spaces, Criome-backed identities, short ID prefixes, LLM-call fallback chains) is untouched.
- **Implication:** Settled sections are functioning as intended. Speculative sections were properly flagged; no agent has acted on them as if settled.
- **Reversion recommendation:** **Leave `/264` v1.** The settled-vs-speculative line is doing its job.

### 3f. `/265` - Spirit master-upgrade test result

- **Operator response found:** None — `/265` IS the test artifact. Antecedent is `second-system-assistant/7` (the deployment that the test ran against).
- **State:** Test passed. Master daemon decodes the deployed redb's 42 records cleanly; the additive-but-position-inserting Observation enum change is wire-compatible for the unaffected variants. Tests for the position-shifted variants and structural payload changes (the harder cases) are not in scope.
- **Implication:** `/265` validates `/260`'s intent record 30 (the rkyv-headroom Principle) for the easy case and explicitly defers the hard case to `/260` / `/262` / `/263` / `/270`. No drift between report and current state.
- **Reversion recommendation:** **Leave `/265` v1.** It is a test result with a known scope. No revision is warranted; if a future test exercises the hard case, that becomes a separate report.

### 3g. `/266` - Persona-pi triad design

- **Operator response found:** None. No `persona-pi`, `signal-persona-pi`, or `owner-signal-persona-pi` repo exists. `pi-delegate` exists in the org but predates this thread.
- **State:** Sketch only. Settled material: triad shape, dual-path communication (terminal-cell + harness API both first-class), namespace adaptation (flat snake_case verbs to typed-noun records), composite-designer-role substrate. Speculative material: select-or-merge policy, composite roles beyond designer, authority graph placement, persona-terminal interaction, observability shape.
- **Implication:** Implementation has not begun. `/266` correctly defers to `/268` (operator-input brief) which itself asks the operator to take a position on the open forks. No further substance has accumulated.
- **Reversion recommendation:** **Leave `/266` v1.** Awaiting operator's implementation proposal per `/268`'s framing. The settled/speculative split is doing its job.

### 3h. `pi-api-surface-notes.md` - Pi API research

- **Operator response found:** None.
- **State:** Identifies Pi as `pi-mono` (Mario Zechner's `@mariozechner/pi-coding-agent`), documents the four built-in tools, the flat `pi.*` ExtensionAPI, the event surface, and the six load-bearing divergences from workspace discipline (flat tool namespace vs. typed-noun records; flat method bag vs. typed record API; TypeScript closure state vs. typed signal types; free-form args vs. single-NOTA-argument rule; npm distribution vs. Nix flake; user-editable system prompt vs. designer-owned protocol).
- **Implication:** Research feed; no design commitments; no implementation status to track. The Pi-API-specifics speculative sections of `/266` depend on this research.
- **Reversion recommendation:** **Leave `pi-api-surface-notes.md` as-is.** Research material; not a design subject to reversion. If the team renames it to fit the numbered scheme later (`reports/designer/N-pi-api-surface-notes.md`), that is a rename, not a revision.

### 3i. `/267-v2` - Intent substrate certainty drift

- **Operator response found:** None directly. **`/269` (designer-self) supersedes /267-v2's mapping proposal** by widening the vocabulary instead of narrowing it. `/269` lands the Magnitude type in `signal-sema` (commit `22b036a`); once Spirit consumes Magnitude, the seven `High` records become valid as-is.
- **State:** Seven `High` records still live in `intent/*.nota` (4 in `persona.nota`, 2 in `workspace.nota`, 1 in `reports.nota` per workspace scan). Deployed Spirit still rejects them. The mapping plan `/267-v2` proposed (High to Maximum) has not been executed.
- **Implication:** `/267-v2` was the diagnostic that surfaced the wider problem; the **solution shifted** between `/267-v2` and `/269`. `/269` correctly calls itself the supersession of `/267-v2`'s mapping proposal.
- **Reversion recommendation:** **Supersede `/267-v2` entirely.** Two options:
  - **Preferred:** Delete `/267-v2` and absorb its diagnostic value (the count of seven High records, the cluster locations, the broader substrate-migration discipline in §5) into either `/269` or a successor report. The diagnostic is what survives; the mapping proposal is wrong.
  - **Alternative:** Bump to `267-v2-...` retaining the diagnostic and §5 discipline, deleting §4 (the mapping proposal). Then point at `/269` for the actual solution.
  - **Recommended action:** Bump to `-v2`. The §5 substrate-migration discipline (enumerate enums on both sides; strict substrate is ground truth; surface mismatches before bulk relog; even a dumb tool needs the mapping table) is general principle that survives the specific mapping shift. The simplest move is to keep that and rewrite §4 to point at `/269`.

### 3j. `/268` - Persona-pi operator-input brief

- **Operator response found:** None. No implementation proposal yet.
- **State:** Brief is fresh (16:27). No operator turn has begun.
- **Implication:** Awaiting operator engagement. The brief properly bounds the forks the operator must close.
- **Reversion recommendation:** **Leave `/268` v1.** Operator-input briefs are explicitly transitional artifacts. Once the operator's proposal lands, the brief may be retired; until then, leave it.

### 3k. `/269` - Universal Magnitude type design

- **Operator response found:** **Yes — Magnitude landed in code as `signal-sema` commit `22b036a` ("signal-sema: add magnitude vocabulary"), 2026-05-21T17:10:17+02:00.** This is ~40 minutes after `/269` was filed at 16:29. The implementation:
  - `src/magnitude.rs` with the seven-variant enum (Minimum, VeryLow, Low, Medium, High, VeryHigh, Maximum) in the order /269 §3 specified.
  - NotaEnum + Archive + RkyvSerialize + RkyvDeserialize derives, plus Ord / PartialOrd / Hash / Copy / Eq.
  - `as_record_head` / `from_record_head` helpers matching /269 §3's documented surface.
  - `tests/magnitude.rs` with 106 lines of round-trip + ordering + unknown-head rejection witnesses.
  - `examples/canonical.nota` lists all seven heads.
  - `ARCHITECTURE.md` and `README.md` updated.
- **State:** Type lives in `signal-sema`. **Downstream consumers have not migrated.** `signal-persona-spirit` still owns `Certainty` (three-variant). `signal-persona-mind` still owns `ItemPriority`. The migration to retire the per-component enums and pull them through `signal-sema::Magnitude` is unimplemented.
- **Implication:** /269's design landed cleanly. The next operator slice is consumer migration (Spirit + Mind), which `/269` §"Migration plan" sketches but does not commit code for.
- **Reversion recommendation:** **Leave `/269` v1.** Implementation matches design; the followup work (consumer migration) is normal downstream propagation, not design revision.

### 3l. `/270` - sema-upgrade component design

- **Operator response found:** None. No `sema-upgrade` triad repos exist.
- **State:** Sketch only. Triad shape declared (sema-upgrade-daemon + signal-sema-upgrade + owner-signal-sema-upgrade with `upgrade` CLI). Wire surface (Inspect / Plan / Approve / Run / Observe / Subscribe) declared as designer proposals pending psyche confirmation. Consumes the `/262` / `/263` schema-layout machinery and orchestrates the migrations `/260` motivated.
- **Implication:** Implementation has not begun. Operator/151 proposed a one-shot `spirit-migrate` binary per-component, which `/270` reframes as a universal triad. The two proposals are not yet reconciled in writing.
- **Reversion recommendation:** **Leave `/270` v1.** The reconciliation with operator/151 is straightforward (the universal triad is the home; per-component migration libraries are its consumers) and can happen in implementation arc or in a future designer report. /270 itself does not need bumping today.

### 3m. `/271` - Forge component family design

- **Operator response found:** None new. `forge` and `signal-forge` crates exist in the org with prior history (latest commits 2026-04-29, well before this thread). The existing skeletons cover an earlier framing — forge as the workspace's lojix-deploy-daemon-successor build-system — and the latest commit message in the `forge` repo (`8c1ef63 docs: framing — future work, not the lojix deploy daemon`) explicitly distances from being the immediate lojix replacement. None of /271's family members (forge-nix-builder, workspace-content-store) exist; forge-core's role in the new design is undeclared in code.
- **State:** Exploratory sketch. Settled: forge is a family; forge-core is the standardisation point; forge-nix-builder is the first concrete leg; the workspace-content-store is the eventual reach; "the first concrete forge wraps Nix straight up". Speculative: per-component forges, the forge-core triad vs. pure-library question, the trajectory of replacing Nix's store + substitution.
- **Implication:** `/271`'s relationship to the existing `forge` / `signal-forge` skeletons is unspecified. Specifically: does `/271`'s "forge-core" map to the existing `forge` skeleton, or is it a new crate? Does the existing `signal-forge` become `signal-forge-core`, or stay flat? The existing crates' ARCHITECTURE docs (criome-mediated arca deposit, capability tokens, blake3-via-arca-daemon) are not visible in `/271`'s sketch.
- **Reversion recommendation:** **Leave `/271` v1, but flag the gap.** The exploratory framing was correct; no falsifying evidence has landed. The reconciliation with the existing `forge` / `signal-forge` skeletons is a real gap and belongs in a designer follow-up (post-/272) that either:
  - reframes the existing `forge` / `signal-forge` as the first family members under the new `/271` plan, or
  - explicitly retires the existing skeletons in favour of a fresh family.
  - The follow-up is new substance, not a revision of /271.

## 4. Cross-thread observations

### 4a. The Magnitude landing is the only material code response

Within the audit window, exactly one design from the 260-271 thread
has landed in code: `/269` Magnitude in `signal-sema`. Operator/151
is a proposal, not implementation. All other designs (persona-pi,
sema-upgrade, forge family, schema-language) are sketch-only. The
Magnitude landing is fast (40 minutes from design to commit) and
matches the design precisely.

### 4b. The two thread halves are concurrent, not sequential

Two design clusters formed today:

- **Schema-migration cluster:** `/260` → `/261` → `/262` → `/263` →
  (operator/151 lands here) → `/265` validates → `/267-v2` (drift
  diagnostic) → `/269` (Magnitude as response) → `/270` (sema-upgrade
  as orchestration layer).
- **Composite-designer cluster:** `/264` (role spaces) → `/266`
  (persona-pi triad) + `pi-api-surface-notes.md` → `/268` (operator
  brief).
- **Forge family:** `/271` is a separate exploratory thread.

The clusters are weakly coupled. Reversion can proceed per-cluster
without forcing global sequencing.

### 4c. `/267-v2` superseded inside the thread, not by operator

`/267-v2`'s certainty mapping proposal was reframed by the **designer**
in `/269`, not by an operator response. This is the designer-thread
working as intended: the diagnostic surfaced the wider problem, the
next design widened the vocabulary instead of narrowing the writer.
The reversion for `/267-v2` is therefore intra-thread, not in response
to external evidence.

### 4d. Operator-side migration backlog is unrelated to this thread

The fifty open beads in `.beads/` are mostly migration tasks
(`Migrate persona-terminal triad`, `Migrate lojix triad`,
`Migrate criome triad`, etc.) tracking pre-existing migration
arcs. None reference the new `/260-/271` thread. The thread has not
yet generated bead entries; if the designer wants the implementation
work tracked, beads should be filed.

### 4e. The existing `forge` / `signal-forge` skeletons are an unresolved gap

`/271` should not have been filed without naming the existing
`forge` / `signal-forge` skeletons in the org. Their existence is
load-bearing context the sketch missed. This is the single
substantive gap the audit finds in `/271`.

## 5. Recommended reversion actions

### 5a. Per-report action table

| Report | Action | Rationale |
|---|---|---|
| `/260` Schema migration discipline | **Keep v1** | Kickoff; properly framed. Refinements live in successors. |
| `/261` Schema version surface research | **Keep v1** | Research-and-recommend shape intact. Operator extension is downstream. |
| `/262` Content-addressable schema-layout schema | **Supersede entirely; delete in same commit as the post-audit consolidation** | Already self-banner-corrected; `/263` is the fresh design. Retained content (schema-change classes, three-layer table) absorbs into `/263` cleanly. |
| `/263` Schema specification language design | **Keep v1** | No falsifying evidence; downstream consumers reference it. |
| `/264` Designing protocol and role spaces | **Keep v1** | Settled/speculative split is functioning. |
| `/265` Spirit master-upgrade test result | **Keep v1** | Test result with bounded scope. |
| `/266` Persona-pi triad design | **Keep v1** | Awaiting operator's implementation proposal per `/268`. |
| `pi-api-surface-notes.md` | **Keep as-is** | Research material; not a design subject to reversion. |
| `/267-v2` Intent substrate certainty drift | **Bump to `-v2`** | §4 mapping proposal superseded by `/269`; §5 substrate-migration discipline survives. Rewrite §4 to point at `/269`. |
| `/268` Persona-pi operator-input brief | **Keep v1** | Transitional brief; retire when operator's proposal lands. |
| `/269` Universal Magnitude type design | **Keep v1** | Implementation matches design; consumer migration is normal downstream propagation. |
| `/270` sema-upgrade component design | **Keep v1** | Reconciliation with operator/151's per-component migration library can happen in implementation arc. |
| `/271` Forge component family design | **Keep v1, flag the gap** | Existing `forge` / `signal-forge` skeletons in the org are unresolved context; belongs in a follow-up designer report, not a /271 revision. |

### 5b. Punch list of designs needing reversion

Two reversions only:

1. **Supersede `/262`** (content-addressable schema-layout schema) entirely. Already self-banner-corrected. Absorb the schema-change classes table and the three-layer table into `/263` (which already declares itself the supersession). Delete `262-content-addressable-schema-layout-schema.md` in the same commit that lands the consolidation.
2. **Bump `/267-v2` to `-v2`** (intent substrate certainty drift). Rewrite §4 to point at `/269`'s Magnitude widening instead of the old High-to-Maximum mapping. Retain §1-§3 (the diagnostic) and §5 (the broader substrate-migration discipline).

### 5c. Two follow-up reports recommended (not reversions)

Beyond the above, two new designer reports would close real gaps:

1. **Schema-migration synthesis report** absorbing operator/151's two refinements:
   - The split between public-signal historical types and private-storage historical wrappers.
   - The durable commit-sequence high-water mark requirement for live-copy cutover (sema-engine pressure point).
2. **Forge-existing-skeletons report** that reconciles `/271`'s family plan with the on-disk `forge` and `signal-forge` crates. Either reframe the existing skeletons as family members or explicitly retire them.

Both are new substance, not reversions of existing reports.

## 6. Implementation state summary

What has actually landed in code, with crate commits cited:

| Design | Landed? | Where | Commit |
|---|---|---|---|
| `/269` Magnitude | **Yes** | `signal-sema` | `22b036a` "signal-sema: add magnitude vocabulary" (2026-05-21T17:10:17+02:00) |
| `/260`-`/263` schema-migration / schema-language | No | — | (no code; operator/151 is a proposal, not implementation) |
| `/265` Spirit master-upgrade test | Tested only; deployment unchanged | `persona-spirit` deployed at `694452a`, master at `7c2d902` (4 commits ahead; unrelated to schema-migration design) | — |
| `/266` persona-pi triad | No | — | (no crates exist) |
| `/267-v2` certainty drift | No | — | (7 High records still in `intent/*.nota`; Spirit still rejects them) |
| `/268` operator brief | n/a (brief, not design) | — | — |
| `/270` sema-upgrade triad | No | — | (no crates exist) |
| `/271` forge family | No | — | (existing `forge` / `signal-forge` crates predate this thread; latest commits 2026-04-29) |

Downstream consumer migration for Magnitude (Spirit's `Certainty` →
`signal_sema::Magnitude`, Mind's `ItemPriority` → `signal_sema::Magnitude`)
is the obvious next operator slice and has not begun. The seven
`High` records in `intent/*.nota` remain rejected by the deployed
Spirit and become valid only after Spirit consumes Magnitude.
