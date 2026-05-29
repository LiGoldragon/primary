# Frame — horizon/lojix schema-next port feasibility

*Meta-report orchestrator's frame. Psyche directive 2026-05-28 (Spirit record 1024, High): audit the current state of the new-logic horizon/lojix rewrite and assess whether schema-next + nota-next can be ported to be the MAIN driver of datatypes, signal behavior, and sema behavior across the rewrite — is it possible at all, what is the port path, what gaps must close first. Grounded in the schema-at-heart direction (record 1000, Maximum) and the schema-deep pilots that already proved lojix can be schema-driven.*

## The question, decomposed

"Port schema-next + nota-next to be the main datatype + signal + sema behavior driver" decomposes into three sub-questions, mapping to the Signal/Nexus/SEMA runtime triad (`/392`, records 963-970):

1. **Datatype driver** — can every horizon/lojix datatype (ClusterProposal, NodeProposal, the Horizon view, deploy records, generation records) come FROM schema (schema-next emits them) instead of hand-authored Rust on the legacy nota-codec?
2. **Signal driver** — can the wire protocol (signal-lojix deploy operations, replies, events) be schema-derived (Signal schemas) instead of hand-authored?
3. **Sema driver** — can durable state (deploy ledger, generation records, observations) go through sema-engine with schema-emitted SEMA commands/responses?

The workspace has ALREADY decided schema-at-heart (record 1000, Maximum: "schema-emitted Rust types are the canonical truth source for every type that appears in the system; everything else is methods written by agents on those nouns"). So the feasibility question is really: **is anything about the horizon/lojix rewrite specifically that makes reaching schema-at-heart hard or impossible — and what is the staged port path?**

## What's already proven (this session's accumulated evidence)

- **Lojix CAN be schema-driven** — `/35` schema-deep pilot (28 schema-emitted nouns, 9-actor topology, 10 tests) + `/37` iteration 2 (Nexus mail keeper + sema-engine durable + Communicate + DatabaseMarker, 16 tests, 6.7/8.0 component fullness). Datatype + signal + sema all schema-driven at pilot scale.
- **Cross-crate schema import works in Nix** — `/39` proved shared schema types resolve across crates via `links` + `DEP_*`. This means horizon datatypes shared across lojix + CriomOS consumers can live in one schema home.
- **The full runtime triad works at a process boundary** — spirit-next (the designer-lane schema-at-heart pilot, records 1018/1019) realizes Nexus-mail typestate + durable redb SEMA + real Nix integration tests (record 1006).
- **The substrate-direction reading** — `/36` + `/163` already argued the lean stack should migrate onto nota-next/schema-next rather than walk the legacy nota-codec forward; this audit elevates that to a full feasibility assessment.

So the datatype/signal/sema driving is PROVEN possible for lojix. The open questions are (a) the horizon-specific projection logic, (b) the production-track vs pilot-track gap, (c) the schema-next capability gaps that must close for a FULL (not pilot) port.

## The crux — horizon projection logic

Lojix is a daemon (datatypes + signal + sema — the schema-deep pilots cover it). **Horizon is different: horizon-rs PROJECTS a ClusterProposal into per-node configuration.** That projection is substantial LOGIC (derive node domains, router SSID, LAN CIDR, resolver addresses, tailnet base from cluster facts), not just datatypes. The crux feasibility question:

- Can projection be expressed as **methods on schema-emitted nouns** (the `skills/abstractions.md §"Schema-emitted nouns"` pattern — schema emits the ClusterProposal/NodeConfig types, agents write the projection as methods)?
- Or is there something about projection that RESISTS schema-driving (e.g. it needs computation the schema language can't express, forcing it to stay hand-written logic that merely consumes schema-emitted types)?

The likely answer (per the schema-at-heart frame): projection stays hand-written LOGIC, but operates on schema-emitted NOUNS — which IS schema-at-heart (schema drives the datatypes; agents write the methods). But the audit must confirm the current horizon-rs projection can be re-grounded this way without a blocker.

## Method

Two research waves (research-only subagents — read + write their wave report; no worktree per `skills/feature-development.md`), then orchestrator synthesis:

- **Wave A — horizon datatype + projection layer** (`1-horizon-datatype-and-projection-state.md`): current state of lean horizon-rs (horizon-leaner-shape) — datatypes, NOTA parsing, the projection logic. What porting the datatype layer to schema-next/nota-next-emitted entails. THE CRUX: can projection be logic-on-schema-emitted-nouns, or does it resist?
- **Wave B — lojix signal + sema reconciliation** (`2-lojix-signal-sema-state.md`): current state of lean lojix — production-track (horizon-leaner-shape) vs schema-deep pilot (`/35`, `/37`). What's already schema-driven vs hand-authored. The signal-lojix wire contract state. The gap between the pilot and a real production lojix-on-schema-next.

Then `N-overview.md` — orchestrator synthesis: feasibility verdict (possible / partial / blocked, per sub-question) + staged port path + schema-next capability gaps that must close first (types-only module per `/39`, vectors per `/37/3`, schema upgrade traits per record 950, projection-logic-on-nouns) + risks + recommendation.

## Wave A dispatch brief (research-only)

You are a research-only designer subagent (system-designer lane, inherited per record 920). Read + write ONE report; no code changes, no worktree. Audit the lean horizon-rs datatype + projection layer for schema-next/nota-next port feasibility.

Read: `/git/github.com/LiGoldragon/horizon-rs` (the lean stack is on the `horizon-leaner-shape` branch — check the worktree at `~/wt/github.com/LiGoldragon/horizon-rs/horizon-leaner-shape/` if it exists, else the branch). Focus: (a) the datatype layer — ClusterProposal, NodeProposal, the Horizon view types, the role/capability enums; how are they declared (hand-authored Rust + nota-codec derive)? (b) the NOTA parsing — how does horizon-rs read `datom.nota` / cluster proposals; which nota crate (legacy `nota`/`nota-codec` vs nota-next)? (c) THE PROJECTION LOGIC — where cluster facts become per-node config (domains, SSID, CIDR, resolver, tailnet); how much is it, what shape (free functions? methods? match-heavy?).

Also read for grounding: `/home/li/primary/reports/system-designer/35-schema-deep-new-logics/2-schema-deep-lojix-next-pilot.md` (how lojix was schema-driven — the pattern to mirror), `/home/li/primary/reports/designer/392-vision-schema-driven-stack-canonical-2026-05-27.md` (the schema-at-heart vision), `/git/github.com/LiGoldragon/schema-core/` (the cross-crate import proof from `/39`), `skills/abstractions.md §"Schema-emitted nouns"`.

Answer in your report (`reports/system-designer/40-horizon-lojix-schema-next-port-feasibility/1-horizon-datatype-and-projection-state.md`):
1. Current datatype inventory — what types exist, how declared, how big.
2. Which nota crate horizon-rs uses today + what porting to nota-next/schema-next-emitted datatypes entails.
3. THE CRUX: can the projection logic be re-grounded as methods on schema-emitted nouns (schema-at-heart)? Walk the actual projection code. Is it expressible that way, or is there a genuine blocker (computation the schema can't express, a pattern that resists)? Be concrete — cite the projection functions/methods you find.
4. A feasibility verdict for the horizon datatype + projection layer: POSSIBLE / PARTIAL / BLOCKED, with evidence.
5. Schema-next capability gaps the horizon datatypes specifically need (vectors? nested enums-with-data? recursive types? the cluster proposal is a big nested structure — does schema-next express it today?).

Be honest: if projection genuinely can't be schema-at-heart, that's a real finding, not something to paper over. Do NOT capture Spirit records (record 1024 is the directive). Report under 400 lines.

## Wave B dispatch brief (research-only)

You are a research-only designer subagent (system-designer lane, inherited per record 920). Read + write ONE report; no code changes, no worktree. Reconcile the lean lojix production-track vs the schema-deep pilot-track for the schema-next/nota-next port.

Read: the lean lojix on `horizon-leaner-shape` (worktree `~/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape/` if it exists, else the branch) — the PRODUCTION-track lean lojix that `/34` audited. Compare against the schema-deep pilot tracks: `~/wt/github.com/LiGoldragon/lojix/schema-deep/` (`/35` + `/165` source staging) and `~/wt/github.com/LiGoldragon/lojix/schema-deep-iteration-2/` (`/37` Nexus + sema-engine). Read `signal-lojix` (the wire contract repo). 

Read for grounding: `/home/li/primary/reports/system-designer/34-mvp-and-sandbox-audit/5-overview.md` (the production-track lean state as of earlier), `/home/li/primary/reports/system-designer/37-prototype-schema-deep-iteration-2-nexus-mail-sema-engine-2026-05-27/3-overview.md` (the pilot at 6.7/8.0), `/home/li/primary/reports/system-designer/38-source-staging-prototype-audit.md`.

Answer in your report (`reports/system-designer/40-horizon-lojix-schema-next-port-feasibility/2-lojix-signal-sema-state.md`):
1. Production-track lean lojix (horizon-leaner-shape) — what's its datatype/signal/sema shape TODAY? Hand-authored types + legacy signal-core/signal-lojix wire + which storage?
2. The schema-deep pilot tracks — what they proved is schema-drivable (cite `/35`+`/37`'s 6.7/8.0). Which of the 8 components are pilot-proven schema-driven.
3. The signal-lojix wire contract — hand-authored or schema-derivable? What porting it to schema-emitted Signal schemas entails.
4. The GAP between the pilot and a real production lojix-on-schema-next: what's pilot-only (in-memory shortcuts, sandbox markers) that production needs real (durable sema-engine — partly done in `/37`; real nspawn; criome auth; owner-signal triad leg).
5. A feasibility verdict for the lojix signal + sema layer: POSSIBLE / PARTIAL / BLOCKED, with evidence. (Expectation: POSSIBLE, largely pilot-proven — confirm + quantify the remaining gap.)

Do NOT capture Spirit records. Report under 400 lines.

## Risks + open questions (orchestrator-level, for the synthesis)

- **Projection-logic-on-schema-nouns** — the crux (Wave A). If projection resists schema-at-heart, that bounds the feasibility.
- **Production-track vs pilot-track divergence** — there are now multiple lojix branches (horizon-leaner-shape production-track + schema-deep + schema-deep-iteration-2 pilots + the system-operator source-staging). The port path must reconcile them (the `/37/3` Decision C branch-convergence question).
- **Schema-next capability gaps** — types-only module (`/39`), vectors (`/37/3`), schema upgrade traits (record 950), big-nested-structure expression (the cluster proposal). The synthesis ranks which gaps GATE the port vs which are incremental.
- **Cluster data as schema** — `goldragon/datom.nota` is hand-authored NOTA at a stale shape (`/36`). Porting it to schema-emitted-types-conforming data is part of the datatype-driver question.
- **The substrate-direction decision is the psyche's** — this audit assesses feasibility + path; the GO/NO-GO on actually porting (vs continuing the legacy lean stack to cutover) is a psyche decision the synthesis surfaces.
