# Cloud component — schema-triad port: the full 2026-06-04 arc

*cloud-designer. Agglomeration of reports 18 (concept + derivation showcase), 19
(first `next` prototype results), 20 (contract/daemon boundary audit), 21
(open-threads register + late-day refresh), and 22 (accuracy audit of
cloud-operator/14). This one report carries every un-superseded point of that
arc. The final state of the arc is recorded in the §"Where this landed" section
at the end: the designer hand-scaffold prototype was DEMOTED as authority by
Spirit `7jcpracf6q8v5nhbred` (Maximum) — [for the cloud component, ignore the
earlier prototype as the implementation authority and write the system fresh
from the current desired shape] — and the operator's generated path is the
authority, now landed actor-native in `cloud/ARCHITECTURE.md`. The durable value
below is the derivation-chain showcase, the wire-only contract correction, the
proven shapes, and the design findings.*

## 1. What the port was and the dual-track workflow

The psyche asked both cloud-designer and cloud-operator to port the cloud
component onto the schema-derived triad-engine stack — designer proving the
forward shape on a `next` branch, operator re-implementing/integrating on `main`
— and specifically wanted to **see the schema and what it produces** (Spirit
2565: seeing what schema produces what code is a design-review technique).

The designer/operator split (Spirit 2556): designers work on a `next` branch by
default per repo; operators own `main` and integrate at discretion (rebase,
cherry-pick, re-implement, or merge a clean designer branch as-is — designer code
is not second-class). Worktree rotation for `next` is deferred (Spirit 2557);
designers use the existing worktree location. Per repo in the cloud triad
(`cloud`, `signal-cloud`, `owner-signal-cloud`→`meta-signal-cloud`), designer
works at `~/wt/github.com/LiGoldragon/<repo>/next/`; the two tracks are compared
(double-implementation strategy) — convergence signals the design is settling.

## 2. The derivation chain — what schema produces (the showcase)

Grounded in the live `spirit` reference. The three lowering stages:
`schema source (NOTA)` → `Asschema` (macro-free typed data: Alias / Struct /
Enum / Newtype + visibility tags; both schema-next's output AND
schema-rust-next's input, so the two emission layers are independently testable)
→ emitted Rust (enums + 3 engine traits + trace hooks + plane envelopes) →
hand-written impls (the component author writes only the inner methods).

Four concrete derivations:

- **Alias** — `Topic String` → `(Public Topic (Alias String))` →
  `pub type Topic = String;`
- **Header variant resolution** — a bare PascalCase variant in the Input/Output
  root resolves its payload by namespace lookup (multi-pass
  `SourceTypeResolver` pre-collects namespace type names):
  `[(Lookup RecordIdentifier) Count]` + namespace → `pub enum Input { Lookup(RecordIdentifier), Count(Query) }`.
- **Newtype vs struct** — single-field bodies become tuple newtypes with
  `new`/`payload`/`into_payload`/`From<Payload>`; multi-field bodies stay
  structs. `Summary { Description * }` → `pub struct Summary(pub Description);`.
- **Cross-crate import** — preserves type identity via `pub use ... as` (the
  Spirit 1557-1562 alias pattern): `{ Local dependency-crate:module:Type }` →
  `pub use dependency_crate::schema::module::Type as Local;`.

**How traits are derived:** the presence of `Input`+`Output` roots plus
`NexusWork`/`NexusAction` plus `SemaWriteInput`/`SemaReadInput` in the Asschema
triggers the emitter to write the three engine traits (`SignalEngine` with
`triage_inner`/`reply_inner` + a typed trace hook; `NexusEngine` with
`decide`/`execute`; `SemaEngine` with `apply_inner`/`observe_inner`). The
surface is uniform across components; only the method bodies differ. Trace
identity is typed (`SignalObjectName`/`NexusObjectName`/`SemaObjectName` enums
projected from plane variants, carried as `TraceEvent(ObjectName)` — no stringly
trace names, Spirit 1365).

**How implementations are derived:** the author writes only the inner methods on
data-bearing nouns — in the spirit reference, exactly three impls carry all
hand-written logic: `SignalEngine for SignalActor`, `NexusEngine for Nexus`,
`SemaEngine for Store`. The REST-shaped wire (Spirit 951) falls out: Input/Output
roots are typed resource operations, SEMA is the single-writer canonical state,
the short-header + rkyv framing is generated, NOTA touches only the CLI/argv
boundary.

The freshness round-trip works: `build.rs` lowers the schema, compares the
checked-in `.asschema`, re-emits Rust from both NOTA and rkyv artifacts and
asserts they match — a stale schema fails the build loudly.

## 3. The two-schema decision and the proven shape

Per Spirit 2568 the port authors **two schemas**, one per contract repo, each
emitting its own engines and sharing record types; `cloud` imports both and runs
two listeners (the triad's two authority surfaces). The split is clean: the
working contract (`signal-cloud`) is read-only (Observe/Validate, no
`SemaWriteInput`); the policy contract (`meta-signal-cloud`) owns every mutation
(RegisterAccount/RotateCredential/SetPolicy/PreparePlan/PrepareProjection/
ApprovePlan/ApplyPlan/RetireAccount).

**The single most important shape decision (proven end-to-end):** the provider
API call (Cloudflare DNS mutation) is a Nexus `CommandEffect`, never inline in a
handler (Spirit 1486: the 5-variant NexusAction set ReplyToSignal /
CommandSemaWrite / CommandSemaRead / CommandEffect / Continue; effects
per-component declared in schema). The owner `decide` loop (hand-written, modeled
on spirit) drives read→effect→write→reply via `Continue` under a
`ContinuationBudget`; `run_provider_effect` is the SOLE site the Cloudflare
client is touched. `ApplyPlan` recurses: a SEMA write that emits
`CommandEffect(CloudflareApplyPlan(plan))` rather than replying. The two-listener
daemon (working socket + owner socket over one in-memory `Store`) is preserved.

The prototype proved the derivation chain is real and runnable: two
schema-derived contract crates authored from scratch, generated through
schema-next → schema-rust-next, **both compile**; the cloud daemon's three engine
impls scaffolded for both contracts.

## 4. The boundary correction — contracts are WIRE-ONLY (report 20)

The psyche caught that the prototype embedded Nexus/SEMA in the contract
schemas. A four-angle audit (canon, macro, reference, prototype) converged,
high-confidence: **a component contract is wire-only.** The contract schema
(`signal-<component>` / `meta-signal-<component>`) carries only the Signal
messaging vocabulary — Input/Output roots, their record types, the wire codec.
Nexus and SEMA are daemon-internal runtime planes and must NOT appear in a
contract; a client sends/receives only Signal messages.

Why it happened: the prototype was modeled on `spirit`, an all-in-one single-repo
pilot that deliberately defers the split (its own ARCHITECTURE.md admits it). The
canon (`component-triad.md`) was clear; an incomplete reference was followed. The
error was workspace-wide — `signal-upgrade` carried the same Nexus/SEMA-in-
contract error (Spirit 2594 cleanup).

**The correct three-way layout** (settled by Spirit 2597/2598/2601/2604/2605):
- `signal-cloud.schema` (wire-only): Input `[Observe Validate]`, Output, records,
  codec. No Nexus/SEMA.
- `meta-signal-cloud.schema` (wire-only): the 8 policy ops + replies + records.
  No Nexus/SEMA.
- The daemon's plane schemas — **separate files inside the one daemon crate**,
  NOT per-plane crates, NOT one all-in-one daemon schema:
  `cloud/schema/nexus.schema` + `cloud/schema/sema.schema`. Each imports the wire
  contracts' Signal Input/Output; the generator emits per-plane (the Nexus
  schema emits the Nexus engine, the Sema schema the Sema engine). This requires
  schema-next to read multiple plane-schemas per crate (2604) and to import a
  contract's wire roots. The separate `signal-*`/`meta-signal-*` repos exist for
  rebuild-churn isolation and security-edit visibility (2605/2602).

A wire-only contract already emits no engine traits today (SignalEngine is gated
on NexusWork/NexusAction presence), so stripping Nexus/SEMA fixed the contracts
with no macro change — and that strip was confirmed DONE on `next` (report 21
thread 3). The prototype's engine logic (decide loops, effect handler) is sound
and only needed to move from the contract repos into the daemon schema.

## 5. Design findings the prototype surfaced (durable)

1. **Read-only contract had no SEMA engine hook** — the emitter gated
   `SemaEngine` emission on `SemaWriteInput`; a read-only contract got the typed
   read path with no trait method to implement the observe. (Resolved into the
   wire-only correction above: reads belong to the daemon's sema.schema, not the
   contract.)
2. **Old and new contract surfaces cannot coexist in one crate** — `[patch]`-ing
   `signal-cloud` to the schema-derived crate poisons every pre-schema dependent.
   This is the expected staged-cutover shape (build replacement to parity, run
   parallel, switch consumers, retire old), not a defect.
3. **`ObservationResult::Zones`/`Records` were query-shaped, not listing-shaped**
   — the Observed reply carried request types, not result types, so an observe-
   effect result had nowhere to ride home. Fix: listing-shaped arms mirroring
   `SemaReadOutput::Observed`.
4. **Cross-contract Plan/record drift** — the working `Plan` and owner `Plan`
   differed in field names; shared record types should be authored once and
   imported via the schema language's Import/Export (Spirit 1557-1562), not
   re-declared per contract.
5. **Single-field records lower to tuple newtypes** — `Approval { plan }` →
   `Approval(pub PlanIdentifier)`; callers shift from `.plan` to `.0`/`.payload()`.
6. **Output variants must be bare, not self-aliased** — self-aliasing collides
   with the same-named struct (`DuplicateSourceDeclaration`); bare variants
   auto-resolve via `SourceTypeResolver`. Worth a schema-authoring-skill note.
7. **`cloudflare.rs` is typed against the old contracts** — must be re-typed
   against the generated contracts before the effect handler does real IO.

## 6. Where this landed — the final state of the arc (the supersession)

A late-2026-06-04 five-agent re-verification (plus a Spirit sweep, daemon up at
0.4.2) found the state moved hard the same afternoon; most of the open-threads
register resolved or superseded:

- **Prototype DEMOTED as authority.** Spirit `7jcpracf6q8v5nhbred` (Maximum) —
  ignore the earlier prototype as the implementation authority and write the
  cloud system fresh from the current desired shape — killed the
  compare-two-equal-candidates framing. The operator's generated path landed a
  real `build.rs` generation driver on cloud `main` (bead `primary-qhi6`,
  per-crate generation driver, CLOSED); the designer hand-scaffold stays a
  feature-gated prototype on `next`. The generated path is the authority; the
  scaffold's only residual value is its proven shapes (provider IO as a Nexus
  `CommandEffect`; in-memory `Store` SemaEngine) — captured in §3 above.
- **Multi-provider lives in the wire contract.** `signal-cloud` `lib.schema`
  carries `Provider [Cloudflare GoogleCloud Hetzner]` + Capability vocabulary;
  "Cloudflare-only" is an engine-impl detail (one `CommandEffect` per provider),
  not a schema fork (the old open fork F4 — closed).
- **The parked 12/16/17 concepts are write-offs** — double-verified zero
  material trace (no report, no bookmark, no branch artifact).
- **Type-name reconciliation is operator-owned on `main`** (bead `primary-1eqv`,
  held under `orchestrate/operator.lock`): align the daemon schemas to the
  contract names; the `owner-signal-cloud`→`meta-signal-cloud` rename is
  half-done (imports/commit titles use the new name; the repo dir/crate/remote
  still old). Part of the 13-repo `owner-signal-*`→`meta-signal-*` fleet rename.

The cloud port itself subsequently went actor-native — `cloud/ARCHITECTURE.md`
now describes `main` running "the production-shaped runtime through the emitted
actor-native daemon spine" (`ActorMultiListenerDaemon` bind for working+meta
tiers), with the provider `Store` behavior behind a schema bridge and the schema
placement split by plane (nexus.schema / sema.schema). So the durable design of
this arc has fully landed in code + ARCHITECTURE.md.

## 7. The accuracy audit of cloud-operator/14 (report 22 — preserved verdict)

The psyche asked whether cloud-operator report 14 accurately identified the cloud
schema-triad-engine blockers. A five-agent workflow (four investigation angles +
an adversarial judge, all high-confidence, reproductions against committed
canonical checkouts then cleaned up) verdict: **partially accurate —
directionally right, but misidentifies the primary blocker and gets the bead
state materially wrong.**

The report named one blocker (the schema-next nested-import resolver loss). The
audit found a **stack** of them; the resolver bug is item 4, not item 1:

1. **Type-name content drift (deepest).** `cloud/schema/sema.schema` and
   `nexus.schema` import `signal-cloud:lib:` names the next-worktree
   `signal-cloud` `lib.schema` does NOT define — so even with the resolver fixed,
   resolution hits `ImportedTypeNotFound`. The cloud daemon schemas and the
   contract schemas were mutually inconsistent; the report named it nowhere.
2. **Canonical-vs-next schema split.** The resolvable `lib.schema` /
   `meta-signal-cloud.schema` exist only in the `~/wt/.../next` worktrees; the
   `/git` canonical checkouts carry only `*.concept.schema`. Yet
   `cloud/schema/{nexus,sema}.schema` (on `/git` main) reference contract modules
   that only exist on next.
3. **Missing module schema files on canonical** — a canonical build fails first
   with `Io "No such file: signal-cloud/schema/lib.schema"` (the loader expects
   `<schema_dir>/<module>.schema`; `concept.schema` is not a loadable module).
4. **schema-next nested-resolver bug (the report's named blocker).** Real at
   `resolution.rs:206`: a directly-imported module is lowered with a fresh empty
   resolver, so its nested imports resolve against nothing →
   `UnresolvedImportCrate`. One-line fix (`lower_with_resolver(engine, self)`,
   already provided at `module.rs:203-213`), but it only matters once 1-3 clear.
5. **No cloud `build.rs` / no auto-discovery wiring** — no `links` key, no
   `DEP_<LINKS>_SCHEMA_DIR`, so schema-rust-next's auto-discovery returns `None`.
6. **`meta-signal-cloud` repo not created** — carried by a local path dep into
   `owner-signal-cloud/next`; a real deployment gate.

**The materially-false claim (C9):** report 14 said bead `primary-1tsw` was
"claimed by the operator with uncommitted in-progress edits". The audit: that
bead is **CLOSED**, assignee **designer**, work **committed on `schema-next`
main `3f7813cf`**; the only uncommitted cloud work is the hand-written
`cloud/next` engine scaffold. The "finish/commit primary-1tsw" framing should be
dropped entirely.

**Root cause the resolver bug survived:** the only multi-module test
(`tests/lowering.rs:229`) uses a fixture whose nested module imports nothing
further, so the resolver-loss path is never exercised. Any fix should add a
`nexus → sema → third-crate` regression test.

**The meta-signal-cloud subtlety, resolved precisely:** NOT a resolver-name
blocker — resolution matches by registered Cargo crate-name string, and
`owner-signal-cloud/next`'s package name IS `meta-signal-cloud`. The concern was
directionally right but located in deployment + canonical-vs-next, not in the
resolver's name matching.

The operator subsequently wrote the correction
(`reports/cloud-operator/15-correction-to-cloud-schema-blocker-report-2026-06-04.md`,
cited the five-agent audit, fixed the false bead-state claim and the
misidentified blocker), so this audit's loop closed itself.

## 8. Branch locators (historical)

- `cloud` → `next` (`073dcf60`) — daemon engine scaffold (both contracts),
  provider-IO-as-effect.
- `signal-cloud` → `next` (`ab456c41`) — working contract, wire-only, compiles.
- `owner-signal-cloud` → `next` (`65b21e81`) — policy contract as package
  `meta-signal-cloud`, wire-only, compiles. (Repo rename a separate slice.)

All were on `next`, pushed-or-local awaiting operator integration. With the
prototype demoted by `7jcprac…`, these branches are low-value record-keeping; the
authority is the operator's generated path on `main` (now actor-native per
`cloud/ARCHITECTURE.md`).
