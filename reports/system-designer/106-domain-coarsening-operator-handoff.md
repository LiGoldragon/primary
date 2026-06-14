# 106 — Implementation hand-off: coarsen + curate the Spirit Domain taxonomy

*System-operator hand-off for the domain-taxonomy fix the psyche approved
("I agree with everything with medium conviction. So that's good to proceed").
Design is reports 104 (naming audit) + 105 (coarsening curation); intent is
Spirit `qr5o` (Principle). This report is the buildable spec: the target schema,
the value/scope enum change, the `From`-chain store migration, the guardian
retrieval extension, the test plan, the deploy bar, and the sequencing against
the in-flight SEMA-VC tower. Goal: a known-to-function fixed-domain spirit,
verified on a staging copy of the live store, then deployed.*

## What this is, in one paragraph

The closed `Domain` enum over-specified `Technology>Software` into ~200 fine
leaves (54% with zero records) doing work that belongs to the open referent layer
and free-text keywords (Spirit `qr5o`). The fix: keep the 12 Software sub-domains
as **terminal-able** branches, keep only the **42 curated broad-field leaves**,
cut the other 169 to keywords, and rewrite every affected live record's domain
vector. This also **satisfies `primary-gm78`** (stored scope-level `All` buckets):
the value side gains the terminal-ability the query `*Scope` side already has.

## Deliverable 1 — the curated taxonomy (target schema)

Replace the `Technology` subtree in `signal-spirit/schema/domain.schema` with this
(ancestry-stripped names; `Languages`→`Programming`; term-of-art compounds whole):

```
(Technology
  (Hardware [Networking])
  (Software
    (Programming   [TypeSystems Compilation Parsing Grammars CodeGeneration Metaprogramming Macros DomainSpecificLanguages])
    (Theory)                          ;; terminal-only: no curated leaves
    (Systems       [SystemsProgramming Concurrency])
    (Distributed   [ProtocolDesign EventDrivenArchitecture])
    (Data          [Persistence Serialization Formats Modeling SchemaEvolution Migration])
    (Intelligence  [AgentSystems])
    (Security      [Cryptography Authentication Authorization SecretsManagement Privacy])
    (Quality       [Testing])
    (Operations    [BuildSystem ReleaseEngineering DependencyManagement Deployment ConfigurationManagement])
    (Observability [Tracing])
    (Surfaces      [Visualization CommandLineInterfaces])
    (Engineering   [Architecture Design ApplicationProgrammingInterfaces Documentation VersionControl DevelopmentProcess Management Modularity])))
```

The 23 non-Technology domains are **unchanged** (the psyche scoped this to
Technology). The borderline calls in 105 are resolved by the psyche's "agree with
everything" — build the set above as-is. Two implementation-time sanity checks (not
new decisions): before finalizing the re-homes, glance at the live records behind
the three high-usage cuts to confirm the fold target — `AdmissionControl` (15,
expected daemon/actor peer-cred admission → keyword near the IPC/actor area, NOT
Security), `InterprocessCommunication` (9 → `ProtocolDesign`), `Virtualization`
(6 → `Systems` terminal).

## Deliverable 2 — the value/scope enum change (satisfies `primary-gm78`)

The taxonomy is a dual family in `signal-spirit/src/schema/domain.rs`: **39 value
enums** (stored in `Entry.Domains`) + **39 `*Scope` enums** (queries). The `*Scope`
side already has `All` on 38/39; the **value side gains the equivalent terminal**.
Each sub-domain carries an `Optional` curated-leaf payload — bare atom = terminal
(`(Technology Software Security)`), `(Sub Leaf)` = curated
(`(Technology Software Security Cryptography)`):

```
enum Technology { Hardware(Option<HardwareLeaf>), Software(SoftwareScope) }
enum SoftwareScope {
    Programming(Option<ProgrammingLeaf>),
    Theory,                                  // unit variant — pure terminal
    Systems(Option<SystemsLeaf>),
    Data(Option<DataLeaf>),
    // … one Option<…Leaf> per curated sub-domain
}
enum ProgrammingLeaf { TypeSystems Compilation Parsing Grammars CodeGeneration Metaprogramming Macros DomainSpecificLanguages }
```

Rules: each value sub-enum shrinks from ~16 to 0–8 variants; `Theory` emits no leaf
enum; single-leaf sub-domains (`Quality`/`Intelligence`/`Observability`) keep an
`Option`-wrapped one-variant enum so the terminal case stays expressible; leaf-enum
variants are ancestry-stripped; the schema-emit macro emits each leaf enum + its
`From`/`Display`/SEMA impls into `impl` blocks (method-only rule). Apply the same
to the mirror `*Scope` family. Decide whether `Technology` and `Software`
themselves also become terminal-able (mirrors the existing `TechnologyScope::All`/
`SoftwareScope::All`) — recommended yes, for the ancestor-`All` retrieval chain.

## Deliverable 3 — the `From`-chain store migration (precious data)

`Entry.Domains` is stored inline (rkyv + NOTA) across **1248 live records**. Build
a faithful domain-vector rewrite as a `From`-chain step (same pattern as the v8→v9
fold), driven by a mechanical map so no record is missed:

- **42 survivors** — rename in place to the ancestry-stripped leaf
  (`SoftwareArchitecture`→`Architecture`, `DataModeling`→`Modeling`,
  `DataFormats`→`Formats`, `SoftwareDevelopmentProcess`→`DevelopmentProcess`,
  `SoftwareEngineeringManagement`→`Management`; `Languages`→`Programming` layer).
- **169 cuts** — rewrite to the surviving fold target (the sub-domain terminal or a
  sibling curated leaf) and append the specificity as a description keyword. The
  high-usage folds (the migration's real work):

| Cut leaf (usage) | New domain | Append keyword |
|---|---|---|
| `Quality>IntegrationTesting` (10) | `Quality>Testing` | integration testing |
| `Quality>EndToEndTesting` (7) | `Quality>Testing` | e2e |
| `Data>QueryProcessing` (10) | `Data` (terminal) | query processing |
| `Data>Encoding` (9) | `Data>Serialization` | encoding |
| `Data>DataValidation` (9) | `Data` (terminal) | validation |
| `Distributed>InterprocessCommunication` (9) | `Distributed>ProtocolDesign` | IPC |
| `Engineering>SoftwareMaintenance` (6) | `Engineering>DevelopmentProcess` | maintenance |
| `Engineering>DesignPatterns` (4) | `Engineering>Design` | design pattern |
| `Security>AdmissionControl` (15) | re-home (IPC/actor area) | admission control |
| `Security>AccessControl` (4) | `Security>Authorization` | access control |
| `Operations>PackageManagement` (5) | `Operations>DependencyManagement` | packaging |
| `Operations>Orchestration` (5) | `Operations>Deployment` | orchestration |
| `Systems>Virtualization` (6) | `Systems` (terminal) | virtualization |

The 113 zero-usage cuts have no records to rewrite — pure schema deletion. Full
fold map: report 105 "Migration consequence."

**Hard dependency:** cutting `Data>DatabaseSystems` requires editing the
`Information>Database` ≡ `…Data DatabaseSystems` `Equivalence` entry in
`domain.schema` (104) in the same change. The `Hardware>Networking` ≡
`Distributed>Networking` bridge: Hardware keeps `Networking`, Distributed cuts it
to keyword — update or retire that bridge accordingly.

## Deliverable 4 — guardian retrieval (closes `primary-gm78`)

Extend guardian retrieval so a candidate pulls its typed **ancestor-`All` chain**
(global → `Technology` → `Software` → sub-domain terminal) plus exact leaf +
referent neighbors, **without descending into sibling subtrees** (a coarse scope
candidate must not pull all descendant leaves). Tests must prove the ancestor-`All`
path and a bounded bundle size (gm78 acceptance criteria).

## Test plan (the bar for "known-to-function")

1. **Schema/codegen** — regenerate `domain.rs` (both mirror families) via
   schema-rust-next; `cargo build` + `cargo fmt --check` + no new clippy.
2. **Round-trip** — NOTA and rkyv round-trip witnesses for: a terminal sub-domain
   tag, a curated-leaf tag, and `Theory` (pure terminal). Assert cut leaves
   (`ServiceMesh`, `UnitTesting`, `SoftwareArchitecture` old form) **fail** to
   parse.
3. **Migration faithfulness on a staging copy of the LIVE store** — copy the
   deployed `~/.local/state/spirit/` SEMA store, run the `From`-chain, then assert:
   record count preserved (1248); every renamed survivor reachable at its new path
   with the same identifier; every high-usage cut's records reachable at the fold
   target with the keyword appended; no record left tagged with a deleted variant.
   This is the load-bearing test — it is over precious data.
4. **Guardian retrieval** — the ancestor-`All` path test + bounded-bundle test.
5. **Skills/consumers** (same change): `skills/spirit-cli.md` + `skills/intent-log.md`
   worked examples (`SoftwareArchitecture`→`Architecture`; the `(Quality Testing)`
   example is now a terminal-able leaf — reword); `spirit/src/guardian-prompts/record-shape.md`;
   `signal-spirit/src/lib.rs`; `spirit/tests/process_boundary.rs`,
   `tests/operator_271_closed_claims.rs`; `production_migration.rs`. Manifest Spirit
   `qr5o` into the spirit/signal-spirit `INTENT.md` on the implementation branch.
6. **Full suite** — `cargo test --all-features` green; `nix build` green.

## Deploy bar

Report back ready-to-deploy when: codegen + full suite green; the staging-copy
migration is proven faithful (test 3); guardian retrieval tests pass; the deployed
daemon, restarted against the migrated store, self-resumes and `Observe`/`Count`
return the expected records at the new paths. Then deploy (the daemon self-resumes
from persisted SEMA state after the migration runs as the `ExecStartPre`
migrate-store step). Bump the spirit component version and update
`skills/spirit-cli.md`'s stated deployed version.

## Sequencing against the in-flight SEMA-VC tower

This is **not the only spirit change pending production.** The SEMA-VC hardening
tower (`primary-qu28`) is built + adversarially reviewed on branches (0.13.x) but
**not yet integrated or deployed** — the live daemon is **0.12.1**. Both this
coarsening and that tower migrate the store and require a redeploy. **Do not run
two separate migrations of the precious intent store.** Recommended: land/deploy
the VC tower first (it self-heals layout 4→5 via rebuild-from-log, `primary-lmf3`),
then this domain migration as the next staged step — or bundle both `From`-chain
steps into one migration pass. The system-operator owns the sequencing call;
flag it before deploying so the two don't collide. (Full tower state: `primary-qu28`
and its sub-beads — see the "anything else pending" summary in chat.)

## Lane note

`primary-gm78` is currently assigned `operator`; this hand-off is to
`system-operator` per the psyche's instruction. One lane should own the whole
change (schema + migration + deploy). Reconcile gm78's assignee with the new
implementation bead so the All-bucket half and the curation half don't fork.
