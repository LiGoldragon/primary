# 415 — Context maintenance sweep, designer reports

*Kind: Review · Topics: discipline, workspace, context-maintenance · 2026-05-28*

*Designer-lane context-maintenance subagent sweep. Triages the
`reports/designer/` backlog (42 entries, far over the 12 soft cap)
against the drop / forward / migrate / keep discipline in
`skills/context-maintenance.md` §2-3. Primary target: the older
`341`-`404` reports, mostly superseded by this session's `405`-`414`
schema-stack work and by the now-rich workspace `INTENT.md`. The live
`405`-`414` SchemaX-audit surface (four agents reading it in parallel)
was left untouched by directive. This report IS the handover: it
records the inventory, per-report decisions, what migrated where, and
the borderline items for the next pass.*

## Count summary

| | Reports + meta-dirs |
|---|---|
| Before | **42** (32 numbered files + 5 standalone older + ... ; effectively 42 entries) |
| Dropped this pass | **27** (25 superseded/migrated + 2 absorbed sweep-ledgers) |
| Migrated to permanent doc | **1** (`/367` CapnProto-superset framing → `INTENT.md`) |
| After | **15** (4 older standalone + 1 older meta-dir + 10 protected `405`-`414`) |

The 15 survivors: `341`, `351`, `352`, `363`, `386/` (older KEEPs) +
`405`-`414` (live SchemaX-audit surface, untouched). The "after" count
sits near cap only because 10 of the 15 are the protected current
surface; the older backlog is trimmed from ~31 entries to 5.

## Continuing from prior maintenance

Two prior passes set the baseline; this sweep continues from them
rather than redoing them:

- **`/377`** (designer-only sweep, 2026-05-27 morning) landed at 11
  entries. Its drops were executed.
- **`/386/`** (cross-lane meta-dir, 2026-05-27 afternoon) ranked all
  lanes and handed per-lane punch-lists to 11 lanes.
- **`/394`** (designer-side report audit, 2026-05-27 evening) executed
  the `/386` designer punch-list — dropped 18 reports + 1 meta-dir
  (101/102/105/106/107 RETRACTED; 349/354/356/358/368/370/372/375/378/
  379/380/381/384/385 absorbed-or-superseded), leaving a 21-entry
  surface. That 21-entry surface plus this session's new `393`-`414`
  is what this pass inherited.

`/377` and `/394` are themselves retired this pass (see below): a
deletion-ledger Review report retires once a successor review
supersedes it (`skills/context-maintenance.md` §"What context
maintenance is NOT" — *"not a deletion ledger"*). This report (415) is
that successor.

## Inventory + topic-recency ranking (the `341`-`404` target set)

The dominant topic is the **schema-derived stack** (NOTA → schema →
emission → runtime), which threads through almost every report. The
recency arc, newest-canonical at top:

1. **`405`-`414`** (2026-05-28) — current. The SchemaX audit (`414/`),
   the engine-in-reality walk-through (`413`), the bottom-up
   presentation (`407`), the gap audit (`405/`), the Nexus/SEMA
   fix-prototype (`406/`), macro-by-example (`410`), collections
   (`411/`), plane envelopes (`409`), three-engines (`408/`),
   `/167`-divergence review (`412`). **Protected — not touched.**
2. **`392`** (2026-05-27) — the prior "canonical vision" landing page.
   Superseded: its rules migrated into `INTENT.md` §"The schema-driven
   stack" → §"Recurring architectural patterns A-F"; its live-
   presentation role is now `/407`; its 5 open questions are resolved
   by records 1029-1054 (plane envelopes, auto origin route, plane
   enum, collections).
3. **`389`/`390`/`391`** (2026-05-27) — the three chapters OF `/392`.
   Superseded by the same `INTENT.md` sections + `/407` + `/413`.
4. **`387`/`388`** (2026-05-27) — schema-design representation + macro
   exploration. Superseded by `/413` (engine in reality) + `/410`
   (macro by example).
5. **`393`/`395`/`396`/`398`/`399`** (2026-05-27) — manifestation /
   synthesis passes. By construction their substance landed in
   permanent docs (verified — see Migrations below).
6. **`397`/`400`/`401`/`402`/`403`/`404`** (2026-05-27) — the
   prototype-development cycle. Superseded by `/405` (audit that
   explicitly builds on `/404`) + `/406` (fix-prototype) + `/407`.
7. **`382`** (2026-05-27) — pair-style namespace sweep. Substance in
   `INTENT.md` §"The schema-driven stack" + `skills/nota-design.md`.
8. **`361`/`366`/`367`/`371`/`374`/`376`** (2026-05-26) — the
   prior-wave vision arc. Two waves behind: superseded by `/392`
   (already noted by `/394`) and now by `/407` + `INTENT.md`.
9. **`341`/`351`/`352`/`363`** (2026-05-25/26) — the standalone
   non-schema-arc reports (design-rationale guards + intent-file
   audits). Kept (see below).

## Per-report decision

### Dropped — superseded by `405`-`414` + `INTENT.md` (25)

| Report | Rationale (one line) |
|---|---|
| `361` latest-vision | Vision arc; superseded by `/392` then `/407` + `INTENT.md`. |
| `366` component truth-verification | Point-in-time empirical tables; superseded by `/405` audit + `/407` §8 honest-status. |
| `367` NOTA-as-spec / CapnProto-superset | **Migrated** (see below) then dropped. |
| `371` Signal/Executor/SEMA triad | `Executor` naming superseded by record 964; framing in `INTENT.md` §"Three schema types" + `skills/component-triad.md` per its banner. |
| `374` deep spirit parallel impl | v0.3-target prototype; superseded by `/406` fix-prototype + `/405` audit on the `-next` stack. |
| `376` bottom-up tour Layer 1 (NOTA) | Tour never reached Layers 3-7; `/407` is the bottom-up presentation that replaces it. |
| `382` pair-style sweep | Substance in `INTENT.md` §schema-driven-stack + `skills/nota-design.md` §"Map keys". |
| `383` next-version schema study/implement | Superseded by `/413` engine-in-reality + `/410` macro-by-example. |
| `387` nota-schema design representation | Superseded by `/413` + `/407`. |
| `388` macro system + brace-enum sugar | Superseded by `/410` macro-by-example + `/413`. |
| `389` schema+macros chapter | Chapter of `/392`; superseded by `INTENT.md` + `/413`. |
| `390` wire+runtime chapter | Chapter of `/392`; superseded by `INTENT.md` §"Three schema types"/§"Signal protocol"/§"REST-shaped" + `/407`. |
| `391` emission+discipline chapter | Chapter of `/392`; the src/schema + Nix-enforced-methods substance is in `skills/rust/methods.md` + `INTENT.md` Pattern C. |
| `392` canonical vision | Migrated to `INTENT.md` §schema-driven-stack..§Recurring-patterns; live presentation now `/407`; open questions resolved by records 1029-1054. |
| `393` continuous manifestation | Substance in `skills/repo-intent.md` §"Continuous manifestation" + `AGENTS.md` (record 944). |
| `395` Signal/Nexus/SEMA manifestation | Substance in `INTENT.md` §"Three schema types, three runtime planes". |
| `396` Nexus mail-keeper consolidation | Substance in `INTENT.md` §"Nexus is the MAIL KEEPER". |
| `397` prototype audit cycle 1 | Superseded by `/405` audit + `/406`. |
| `398` intent-spread completeness audit | Manifestation/audit pass; gaps closed, substance landed in per-repo + workspace docs. |
| `399` discipline pattern manifestation | Substance verbatim in `INTENT.md` §"Recurring architectural patterns" (Patterns A-F) + skills. |
| `400` async-mail on_sent pilot | Superseded by `/402`/`/406`; Pattern A in `INTENT.md`. |
| `401` async-mail Pattern A walkthrough | Superseded by `/406`; Pattern A in `INTENT.md` + `skills/push-not-pull.md`. |
| `402` typed tests per-plane | Superseded by `/403`/`/404`/`/405` (prove-not-pretend test discipline). |
| `403` prototype cycle 2 | Superseded by `/405` audit + `/406`/`/407`. |
| `404` state + prove-not-pretend + Nix integration | `/405` audit explicitly builds on it and confirms its open bead `primary-lrgj`. |

### Dropped — absorbed sweep-ledgers (2)

| Report | Rationale |
|---|---|
| `377` designer-only sweep | Fully absorbed by `/394` then this pass; deletion-ledger retires on successor review. |
| `394` designer report audit | Deletion ledger for the 2026-05-27 evening sweep; absorbed by this report (415). |

### Migrated then dropped (1)

| Report | Migrated to | What |
|---|---|---|
| `367` NOTA-as-spec / CapnProto-superset | `INTENT.md` §"The schema-driven stack" (new paragraph) | The durable identity framing: `.schema`/NOTA is a **specification language more specific than Rust** (data-shape-only; Rust emits from it), a **CapnProto-superset** with three additions (module system / macro system / shape-driven matching), and NOTA is the **text view of the portable rkyv format's specification** appearing in two contexts (SEMA at rest, signal in transit). Records 839-844. The report's other substance (single-colon, module/macro mechanics) was already in `INTENT.md` + `schema-next/INTENT.md` + `/413`. |

### Kept (4 standalone + 1 meta-dir)

| Report | Why kept |
|---|---|
| `341` schema-crystallizes-architecture | **Design-rationale guard** (`skills/context-maintenance.md` §3a): enumerates retracted alternatives (P5 InteractTrait retracted record 666; effect-table/fan-out retracted 713-715). Status banner names permanent-doc landings. |
| `351` intent-file tour | Carries **5 psyche-review flags** still pending (Reading-actor + auto-tap; auto-migration detail level; signal-frame INTENT.md unmerged-branch; missing owner-signal-persona-spirit/INTENT.md; auditor substrate compression). Load-bearing until psyche acts. (See-also dead pointers cleaned this pass.) |
| `352` intent-log audit | Comprehensive **flagged-for-psyche** audit (D1-D18 duplicates, M1-M5 misalignments, H1-H12 suspected hallucinations). Per record 719 agents FLAG, never supersede; pending psyche supersession decisions. |
| `363` design: nota from schema | **Design-rationale guard** §3a: WIDER vs NARROWER recursion-floor cut comparison. Banner **refreshed this pass** — the dead `/361` landing pointer now points at `INTENT.md` + `/407` (the WIDER cut shipped). |
| `386/` cross-lane maintenance meta-dir | Carries **per-lane handoffs to 11 lanes** (operator, second-designer, system-operator, cluster-operator, cloud-*, nota-designer, etc.). No evidence those handoffs are applied; dropping would lose other-lane context. Keep until those lanes consume their punch-lists. |

## What I migrated

One migration, into the workspace `INTENT.md` (the only permanent
surface in scope — repos under `repos/`/`/git` were off-limits):

- **`INTENT.md` §"The schema-driven stack"** gained one paragraph
  carrying `/367`'s CapnProto-superset / specification-language-more-
  specific-than-Rust framing (records 839-844). Inserted right after
  the "schema specifies, signal moves, sema holds" paragraph.

No skill edits were needed — the manifestation reports (`393`/`395`/
`396`/`398`/`399`) had already landed their substance into
`INTENT.md` and the skills during the 2026-05-27 session, which is
exactly why they were droppable. I verified `/399`'s six patterns
appear verbatim as `INTENT.md` §"Recurring architectural patterns"
A-F before dropping it.

## What I dropped and where its substance now lives

The 27 dropped reports' substance lives in (by cluster):

- **Schema-stack vision/chapters** (`361`/`366`/`367`/`371`/`376`/
  `382`/`387`/`388`/`389`/`390`/`391`/`392`) → `INTENT.md`
  §"The schema-driven stack", §"Three schema types, three runtime
  planes", §"Nexus is the MAIL KEEPER", §"Signal protocol",
  §"The wire architecture is REST-shaped", §"Schema-emitted Rust
  mirrors the schema namespace", §"Recurring architectural patterns"
  + the live presentation `/407` + engine-in-reality `/413`.
- **Manifestation passes** (`393`/`395`/`396`/`398`/`399`) → the
  `INTENT.md` sections above + `skills/repo-intent.md`,
  `skills/component-triad.md`, `skills/actor-systems.md`,
  `skills/rust/methods.md`, `skills/push-not-pull.md` (landed during
  2026-05-27 session).
- **Prototype cycle** (`374`/`397`/`400`/`401`/`402`/`403`/`404`) →
  the current audit `/405/`, the fix-prototype `/406/`, and the
  presentation `/407`.
- **Sweep ledgers** (`377`/`394`) → this report (415) + the commit
  tree.

All dropped reports remain one `jj show <change-id>:reports/designer/<N>-…md`
away per `skills/reporting.md` §"Deleted reports live in the commit tree".

## Borderline — needs human / next-pass review

1. **Cross-lane dead pointers to dropped designer reports.** Several
   other-lane reports cite designer reports retired this pass —
   `operator/201` (cites designer/361), `operator/202`, `operator/219`,
   `operator/222`, `operator/218/`, `operator/216/`,
   `system-designer/37/`, `system-designer/38`, `cloud-operator/7/`.
   Per the cross-lane discipline I did NOT edit out-of-lane reports;
   each lane cleans its own surface on its next maintenance, and the
   commit tree preserves the targets. Flagging so the next cross-lane
   sweep knows.

2. **The live `405`-`414` set cites dropped reports too** (`/407` §9
   names `/392` as "vision landing page"; `/405/6-overview` cites
   `/404`; `/408`/`/409` cite predecessors). Left untouched by
   directive (parallel SchemaX audit is reading them). When that audit
   lands its synthesis (`414/5-overview.md`), whoever integrates it
   should repoint `/407` §9's "vision landing page" reference from the
   retired `/392` to `INTENT.md` §"The schema-driven stack".

3. **`386/` cross-lane handoffs may be stale.** The meta-dir's per-lane
   punch-lists are from 2026-05-27; some lanes may have since acted.
   A future cross-lane sweep should verify which handoffs were
   consumed and retire `386/` when they all are.

4. **`351`/`352` psyche-review flags are aging.** Both reports have
   been pending psyche review since 2026-05-26 across three sweeps
   now. Worth surfacing to the psyche: either action the flags
   (intent-log duplicates/hallucinations in `/352`; the 5 intent-file
   flags in `/351`) or explicitly defer, so they stop riding every
   maintenance pass as forced KEEPs.

5. **`341`/`363` design-rationale guards are durable KEEPs.** Per §3a
   they persist as long as their rejected-alternative rationale is
   worth preserving. No action — noting they are intentional permanent
   residents, not backlog.

## Cross-references

- `skills/context-maintenance.md` §2-3 (drop/forward/migrate/keep) +
  §3a (design-rationale guard, protects `341`/`363`).
- `skills/reporting.md` §"Hygiene" (soft cap, supersession,
  deleted-reports-in-commit-tree).
- `INTENT.md` §"The schema-driven stack" — the migration target for
  `/367`.
- The live surface this pass protected:
  `reports/designer/414-schemax-design-audit/0-frame-and-method.md`
  §3 (which names this context-maintenance pass as the parallel
  scoped-to-older-reports sweep).
