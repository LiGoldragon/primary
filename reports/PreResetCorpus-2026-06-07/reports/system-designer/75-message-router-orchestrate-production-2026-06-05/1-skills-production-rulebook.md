# 1 — Skills production rulebook: what makes a component production-ready as a triad-engine daemon

Refresh report for the 75 session. Distilled from the full governing skill
set (read in full, not skimmed) and ground-checked against the spirit /
triad-runtime / schema-rust-next reference sources and the three target
components' actual source. Companion reports: `2-intent-agglomeration.md`
(Spirit sweep), `3-triad-base-state.md` (how a triad daemon is built today),
`4/5/6-*-production.md` (per-component port maps).

This report answers one question: **what rules determine whether `message`,
`router`, or `orchestrate` is production-ready on the schema/triad-engine
base?** It is a rulebook plus a checklist a porter ticks off. The skills are
the substance; this is the load-bearing extract with source citations.

## Part A — The production-readiness rulebook (the invariants)

A component is production-ready as a triad-engine daemon when it satisfies
every rule below. Each rule names its source skill and, where it has one, its
witness-test shape. Rules are grouped by layer: schema shape, engine traits,
runtime mechanism, authority/sockets, bootstrap/state, wire discipline, Rust
discipline, contract repos.

### A1. Schema shape — three plane schemas, not one concept schema

Rule 1 (R1). **The daemon carries THREE plane schema files inside its own
crate**: `schema/signal.schema`, `schema/nexus.schema`, `schema/sema.schema`
— emitted to `src/schema/signal.rs`, `nexus.rs`, `sema.rs`. This is the
worked shape in `spirit` (verified: `spirit/schema/{signal,nexus,sema}.schema`
→ `spirit/src/schema/{signal,nexus,sema}.rs`). The old all-in-one
`*.concept.schema` and `ComponentRuntime` target are dropped.
Source: `skills/component-triad.md` §"'Signal' names two different schema
files" + §"The shape". A single `.concept.schema` is the pre-triad form
(this is exactly what all three targets still carry — see Part D).

R2. **The three planes split by runtime ownership**: Signal owns
communication (wire framing, dispatch, identity-stamping, triage); Nexus owns
execution + in-flight mail + Signal↔SEMA translation; SEMA owns durable
single-writer state. Source: `skills/component-triad.md` §"Runtime triad —
Signal / Nexus / SEMA". Intent anchor (description-first): [SEMA owns DB /
Nexus owns decisions / Signal owns communication].

R3. **Interface roots are enums with MORE THAN ONE variant.** A single-variant
root is a newtype wearing enum clothing — replace it with the struct/scalar it
is. When sketching a plane root, ask "can I name two operations on this
root?"; if not, the design is not done. Source: `skills/component-triad.md`
§"Interface roots are enums with more than one variant" (Spirit 1401). Worked
example: `SemaReadInput [(Observe Query)]` fails; the real interface is
`[(Observe Query) (Lookup RecordIdentifier) (Count Query) (Summarize Query)]`.

R4. **The daemon-local `signal.schema` is what emits `SignalEngine`** (via the
`SignalRuntime` emission target) — NOT the public `signal-<component>`
contract, which emits `WireContract` (engine-free, wire vocabulary + codecs
only). Conflating these two "signal schemas" hides where `SignalEngine` comes
from. Source: `skills/component-triad.md` §"'Signal' names two different
schema files". Verified against the emitter:
`schema-rust-next/src/lib.rs` `RustEmissionTarget` =
{`WireContract`, `ComponentRuntime`, `SignalRuntime`, `NexusRuntime`,
`SemaRuntime`}, with `runtime_planes()` mapping
WireContract→none, ComponentRuntime→all, SignalRuntime→signal-only,
NexusRuntime→nexus-only, SemaRuntime→sema-only.

### A2. The Nexus-feature-catalog rule (the load-bearing visibility rule)

R5. **Every internal engine feature MUST be a declared Nexus verb+object in
`nexus.schema` — never inline hand-written logic hidden from the schema.**
Any computation, any filter/condition on results, any conditional write, any
internal logic feature is declared first as a Nexus interface verb+object;
the hand-written Rust then implements that declared interface. The
consequence is load-bearing: *the complete surface of everything the engine
can do internally is readable in one place — the nexus schema*. A feature
that is not a Nexus verb/object is invisible, and that invisibility is the
failure mode this rule forbids. So when adding a capability (a new filter, a
derived computation, a conditional-write rule), the FIRST move is to declare
its Nexus verb+object, THEN implement. Source: `skills/component-triad.md`
§"Nexus (execution …)" + the strong-form statement there. Intent anchor
(description-first): [the Nexus schema IS the engine's visible internal
feature catalog — every internal feature is a declared Nexus verb+object,
VeryHigh].

This is the single rule most likely to be violated by a port that mechanically
moves a hand-written `match` into a `NexusEngine::execute` body without first
declaring each branch as a Nexus verb. Porting message/router/orchestrate
means **enumerating their internal features and declaring each as a Nexus
verb+object** before writing the engine body.

### A3. The three engine traits — Signal triage / Nexus heavy / SEMA durable

R6. **The runtime is a composition of three trait impls attached to
data-bearing nouns**: `SignalEngine` (triage only — admission, dispatch,
identity-stamping, validation, wire-frame handling; no heavy logic),
`NexusEngine` (heavy logic — algorithms, decisions, the Signal↔SEMA
translation; `&mut self` is the single-flight guard), `SemaEngine` (durable
single-writer with parallel reads — `apply(&mut self, …)` writes serialize,
`observe(&self, …)` reads run concurrent). Source: `skills/component-triad.md`
§"Runtime triad engine traits" (Spirit 1326-1336). Verified in `spirit`:
`impl SignalEngine for SignalActor` (engine.rs), `impl NexusEngine for Nexus`
(nexus.rs), `impl SemaEngine for Store` (store.rs).

R7. **Engine traits carry minimal lifecycle hooks** — `on_start` /
`on_stop` with typed start/stop failure types, default bodies `Ok(())`.
Components that bind sockets, open databases, or hold start-time resources
override `on_start`; the typed failure (port-bound, database-missing,
dependency-unreachable) is the minimum surface persona supervision reads to
decide retry/escalate/fail. Source: `skills/component-triad.md` §"Lifecycle
hooks on the engine traits" (Spirit 1487). Intent anchor (description-first):
[engine traits carry minimal on_start/on_stop lifecycle hooks — the minimum
surface persona supervision uses]. Verified: all three spirit engine impls
carry `on_start`/`on_stop`, and the emitter emits them
(`schema-rust-next/src/lib.rs` emits `fn on_start(&mut self) -> Result<(),
ActorStartFailure>` and `fn on_stop`).

R8. **The engine impl lives on a REAL data-bearing type — never a ZST
namespace, never a fieldless "helper" struct, never a free function dressed
through a trait-alias macro.** The engine impl owns the actor's state (redb
handles, typed configuration, in-memory caches, trace log, child actor refs).
The test: erase the type's name from the type system; if its job vanishes, it
was a namespace and the verbs need a real noun. Source:
`skills/actor-systems.md` §"Engine traits live on real data-bearing types" +
`skills/rust/methods.md` §"No ZST method holders". Verified in spirit:
`SignalActor`, `Nexus`, `Store`, `Engine` are all data-bearing structs.

### A4. The Nexus mechanism substrate — NexusWork / NexusAction / runner loop

R9. **The Nexus engine returns a `NexusAction` from a 5-variant action set**:
`ReplyToSignal(Output)`, `CommandSemaWrite(SemaWriteInput)`,
`CommandSemaRead(SemaReadInput)`, `CommandEffect(Effect)`, `Continue(NexusWork)`.
The runner loop (schema-emitted) dispatches: ReplyToSignal→wire egress;
CommandSemaWrite/Read→SEMA apply/observe whose result is the next NexusWork;
CommandEffect→component-declared effect handler; Continue→re-enter
`Nexus.execute` in-process on the same call stack. Source:
`skills/component-triad.md` §"Nexus mechanism substrate" (Spirit 1486).
Verified in the emitter: `schema-rust-next/src/lib.rs` emits the action→step
mapping `Self::CommandSemaWrite(input) => triad_runtime::NextStep::SemaWrite`,
`Self::ReplyToSignal(output) => …NextStep::Reply`,
`Self::CommandEffect(effect) => …NextStep::RunEffect`.
Intent anchor (description-first): [the runner adapter is generated glue;
authors implement the three plane engines + effect handler + budget reply].

R10. **Effects are per-component declared in schema; `Stash` is the first
universal candidate.** Each component declares its effect vocabulary; the
runner dispatches via the schema-emitted effect handler. A component that
needs no effects declares none. Source: `skills/component-triad.md` §"Nexus
mechanism substrate".

R11 (LANDED-VS-PROPOSED). **`triad_main!` as a named macro is NOT yet
landed.** The frame and the skill describe a macro-generated `triad_main!`
runner loop; in source, the emitter (`schema-rust-next`) emits the
NexusAction→NextStep dispatch and `triad-runtime` carries the runner
(`runner.rs`) + daemon shells, but there is **no `triad_main!` literal
anywhere in `schema-rust-next`** (verified: `grep -rn triad_main` returns only
the emitted `triad_runtime::NextStep::*` mapping references, no macro
definition). A porter must treat "one-line `main` via `triad_main!`" as a
near-future convenience, not an existing API — wire the runner explicitly via
`triad-runtime` until the macro lands.

### A5. Two authority tiers, two sockets, bootstrap policy

R12. **Two typed authority surfaces, both part of the triad**:
`signal-<component>` (ordinary peer-callable) and
`meta-signal-<component>` (owner-only policy/configuration). Each gets its
own typed listener actor and its own permission-separated socket. **A daemon
with only the ordinary surface is not yet triad-shaped.** Contracts split by
WHO-CAN-CALL, not by what-state-they-touch — both contracts can carry
`Mutate` against any state. Source: `skills/component-triad.md` §"Two
authority tiers". Witness tests: `*-owner-socket-rejects-ordinary-frame`,
`*-ordinary-socket-rejects-owner-frame`,
`*-owner-socket-mode-matches-spawn-envelope`.

R13 (LANDED-VS-PROPOSED). **The two-listener wiring is only PARTLY landed in
the base.** `triad-runtime` now ships `MultiListenerDaemon` (committed —
`triad-runtime/src/daemon.rs` carries `MultiListenerRuntime`,
`MultiListenerDaemon`, `BoundMultiListenerDaemon`; recent commit `28d03c3`
"add multi-listener daemon shell"). BUT the canonical reference daemon
`spirit` still uses **`SingleListenerDaemon` only** (verified:
`spirit/src/daemon.rs` `SingleListenerDaemon::new(...)`, no MultiListener, no
owner socket). So there is **no worked two-socket triad-engine daemon yet** —
a porter wiring meta-signal sockets onto the runner is doing it for the first
time against `MultiListenerDaemon`, with `orchestrate`'s existing
thread-based two-socket daemon as the only same-component precedent (but that
is the OLD hand-daemon shape, not the runner shape).

R14. **`meta-signal` is the canonical policy-contract prefix;
`owner-signal-*` is a migration leftover to retire.** New repos, ARCH, skills,
code, schema identities use `meta-signal-<component>`. Source:
`skills/component-triad.md` §4 + §"Why the contract is a separate repo". Intent
anchor (description-first): [`meta-signal-*` is the canonical policy-contract
prefix; `owner-signal-*` is a migration leftover to retire]. Verified that the
prefix is real and adopted elsewhere: `meta-signal-cloud`,
`meta-signal-domain-criome`, `meta-signal-upgrade` exist; but NONE of the three
targets has one (router/orchestrate still carry `owner-signal-*`, message has
no policy contract at all — see Part D).

R15. **`meta-signal` is OPTIONAL** — a component with no owner relationship
ships two repos (daemon + working signal), not three. Source:
`skills/component-triad.md` §"Why the contract is a separate repo" item 3.
This matters for `message`: if message has no owner issuing policy, it
legitimately ships without a meta-signal repo (but then R12's "two surfaces"
is satisfied by the absence being deliberate, not by the surface being unbuilt).

R16. **Policy state bootstraps once from `bootstrap-policy.nota`; thereafter
meta-signal `Mutate` is the only path.** The daemon reads the file exactly
once on first start when policy tables are empty, writes the records as if
Mutated, records bootstrap-complete in a one-shot table, never reads the file
again. Working state never bootstraps from file. Source:
`skills/component-triad.md` §5. Witness tests:
`*-policy-tables-empty-on-first-start-trigger-bootstrap`,
`*-bootstrap-runs-exactly-once`,
`*-policy-changes-after-bootstrap-only-via-meta-signal`,
`*-working-tables-never-read-bootstrap-file`.

R17 (LANDED-VS-PROPOSED). **`bootstrap-policy.nota` is documented but NOT
present in the reference.** The skill's shape diagram puts
`bootstrap-policy.nota` in the daemon repo root; verified `spirit` has **no
`bootstrap-policy.nota`** at its root. So bootstrap-once is an
invariant-on-paper for the base; a porter introducing policy state is the one
establishing the pattern in code.

R18. **Both policy and working state live in ONE `<component>.redb` opened
through `sema-engine`**, split by table category (name prefixes or a sema
table-set declaration), not by storage backend. One sema-engine DB per
component. Source: `skills/component-triad.md` §5 +
`skills/rust/storage-and-wire.md` §"The sema-engine pattern". **Default for
new state-bearing components: depend on `sema-engine`, not `sema` directly.**

### A6. Single-argument NOTA + no NOTA between components

R19. **Every component binary (CLI and daemon) takes exactly ONE argv
argument**: inline NOTA, a path to a NOTA file, or a path to a signal-encoded
(rkyv) file. **No flags — ever.** No `--verbose`, `--format`, `--config=path`,
no positional second argument. New configuration is a field of the NOTA
payload, not a flag. Source: `skills/component-triad.md` §"The single argument
rule". Witness test: `*-binary-rejects-flag-style-arguments`. The CLI's arg is
a NOTA request record; the daemon's arg is a NOTA config record naming
identity, socket paths, redb path, and bootstrap-policy path.

R20. **No NOTA between live components — binary protocol is the wire.** The
daemon's external surface is exclusively signal-frame (length-prefix + rkyv).
NOTA exists at three named projection edges only — CLI argv/stdin, daemon↔harness
terminal, audit/debug dumps — never inter-component. Source:
`skills/component-triad.md` Invariant 2 + §"No NOTA between components" (Spirit
1373). Witness test: `*-daemon-rejects-non-signal-traffic-on-its-socket`.
Intent anchor (description-first): [no NOTA between live components — binary
wire only; inter-component messaging uses unique agent+message identifiers for
async correlation].

R21. **The CLI has exactly one Signal peer — its own daemon — and opens no
database or peer socket.** "Any database" includes the component's own
redb/sema store. A "temporary direct-store CLI" is a triad violation; if the
daemon socket is not implemented yet, the CLI fails closed or stays unshipped.
Source: `skills/component-triad.md` Invariant 1. Witness tests:
`*-cli-accepts-one-argument-and-prints-one-nota-reply`,
`*-cli-has-exactly-one-signal-peer`,
`*-cli-cannot-open-any-database-or-peer-socket`.

R22. **Help is a NOTA operation, not a flag.** Every component supports
`(Help Main)` and `(Help (Verb <name>))` in its ordinary contract;
auto-injected via the `signal_channel!` macro; help text comes from the
schema's mirror description namespace, not Rust doc comments. Source:
`skills/component-triad.md` §"Help operations" (Spirit 263, 1493).

### A7. Verb layers and reply discipline

R23. **Verbs come in three layers**: Contract Operations (external wire verbs
— domain-named verb form: `Submit`, `Query`, `Observe`, `Configure`,
`State`), Component Commands (internal per-daemon typed executable records),
Sema Operations (the six payloadless classification classes: `Assert`,
`Mutate`, `Retract`, `Match`, `Subscribe`, `Validate` — for observation only,
never on the public wire). Source: `skills/component-triad.md` Invariant 3 +
`skills/contract-repo.md` §"Public contracts use contract-local operation
verbs". Witness test: `*-signal-verb-mapping-covers-every-request-variant`.

R24. **Sema classification vocabulary is FORBIDDEN on the public contract
wire.** The six words must not appear as request-root tags; a contract must
not mirror them as an `AuthorizedSignalVerb` enum; an event must not carry the
payloadless `SemaObservation` label. Contract roots are domain verbs; the Sema
class is derived internally. Source: `skills/contract-repo.md` §"What moved
below the public contract" (record 2612). The six legacy contracts that still
carry the pattern — including **signal-router and signal-orchestrate** — are a
cleanup track, not a tolerated convention. This is a direct hit on two of the
three targets.

R25. **Reply success variants are verb-past-tense matching the root**
(`Submit`→`Submitted`, `Register`→`Registered`); **rejection variants are
verb-past-tense + `Rejected`** with typed reason payloads. Replies are
causally tied to the request; independent events are modeled as event/stream
records, not hidden in a reply enum. Source: `skills/contract-repo.md` §"Reply
discipline". Intent anchor (description-first): [component feedback/status/
errors are typed self-descriptive NOTA enums, no string messages].

### A8. Rust discipline (applies to every line of the port)

R26. **Every function is a method/associated-function on a NON-zero-sized
data-bearing type, or a trait impl.** Free functions forbidden except
`fn main()` and `#[cfg(test)]`. Methods on ZST namespace holders equally
forbidden (free function in disguise). Module-level `fn`/`const fn`/`async fn`
all forbidden. Source: `skills/rust/methods.md` + `skills/abstractions.md`
(AGENTS.md hard override). This directly flags `orchestrate`'s daemon, which
uses free functions `accept_ordinary`/`accept_owner`/`bind_socket` (verified
in `orchestrate/src/daemon.rs`).

R27. **Domain values are typed; the wrapped field is private.** A content
hash is not a `String`; a node name is not a `String`. Construction with
validation via `TryFrom`. Don't recover typed information via
`starts_with`/`contains`/`match s.as_str()`. The system mints identity, time,
and sender — the agent supplies only content. Source: `skills/rust/methods.md`
§"Domain values are types" + §"Don't hide typification in strings".

R28. **One object in, one object out; no anonymous tuples at type
boundaries.** When inputs/outputs need more, define a struct. Source:
`skills/rust/methods.md` §"One object in, one object out".

R29. **Schema-generated objects are the method surface** — attach methods to
emitted nouns; don't hand-write a parallel mirror of a generated type; don't
add free functions around generated types. The async mail flow
(`Input`/`Output`/`MessageSent`/`NexusMail<Payload>`/`MessageProcessed<Reply>`)
is object flow, not free procedural glue. Source: `skills/rust/methods.md`
§"Schema-generated objects are the method surface" + §"Async mail flow is
object flow" + `skills/abstractions.md` §"Schema-emitted nouns". Corollary:
**don't hand-edit generated data-type mirrors** — edit the `.schema` and
regenerate.

R30. **Each crate defines its own typed `Error` enum via `thiserror`;
structured variants; foreign errors via `#[from]`.** Never `anyhow`/`eyre`/
`Box<dyn Error>` at component boundaries. Source: `skills/rust/errors.md`.

R31. **redb holds durable state; rkyv is the binary contract** — both for redb
values and inter-component wire. No flat-file logs, no JSON between Rust
components, no ad-hoc binary, no NOTA on the inter-component wire. One redb
file per component. Validate on receive (`rkyv::access`). Append-only fields;
treat any rkyv layout change as a coordinated upgrade; version-skew guard at
boot. Source: `skills/rust/storage-and-wire.md`.

R32. **No hand-rolled parsers** for any named format. Source:
`skills/rust/parsers.md`. (Low risk for these three, but the rule stands for
any external-byte ingestion.)

R33. **CLIs are daemon clients; one Rust crate per repo (lib+CLI may share);
tests in separate `tests/` files; one concern per file.** Cross-crate
`Cargo.toml` deps use `git =` named refs, never `path = "../"`. Source:
`skills/rust/crate-layout.md` + `skills/micro-components.md` §"Cargo.toml
dependencies".

R34. **Actors all the way down; the daemon root is an actor; no
`Arc<Mutex<T>>` between actors; handlers do not block; supervision is part of
the design; release-before-notify on resource-owning actors.** A ZST one-shot
forwarder is a method, not an actor; a real actor's `State` field names the
noun it is. Durable state goes through sema. Source: `skills/actor-systems.md`.
Note the framework is **Kameo 0.20** — but the engine-trait substrate (R6) is
the workspace-canonical runtime shape; actors realize the planes.

### A9. Architectural-truth tests (the witnesses that prove the port is real)

R35. **Every architectural constraint gets at least one witness test: a
positive test proving the intended path is used, and a negative test proving
the tempting shortcut fails.** Positive proof must compile/execute/round-trip/
observe the real boundary — **a positive grep is NOT proof of usage.** Grep
proves absence (negative guards only), never live use. Pick the cheapest
sufficient layer: Layer 1 STATIC (compile-time type reference,
`assert_impl_all!`, compile-fail), Layer 2 RUNTIME (unit/integration test,
actor-trace recorder, process-boundary spawn — the default), Layer 3
BEHAVIORAL (removal breaks observable behavior). Source:
`skills/architectural-truth-tests.md`.

R36. **Schema-chain witnesses use schema objects flowing through the engine
traits**, not test-only enums. The strongest in-process witness drives
Signal→Nexus→SEMA through `SignalEngine`/`NexusEngine`/`SemaEngine` taking and
returning generated root types. **The testing-trace socket is the canonical
Layer-2 witness for engine-trait usage** (Spirit 1349): trace records flowing
on the trace socket prove the engine-trait method was actually called; a
bypass that re-implements the engine outside the trait loses the trace surface
as a consequence. Source: `skills/architectural-truth-tests.md` §"Schema-chain
witnesses" + §"Testing-trace as the workspace canonical Layer 2 witness".
Trace hooks are trait methods (default no-op), not a side enum (Spirit 1365);
trace identity is schema-emitted, not stringly (Spirit 1400).

R37. **Push, not pull** — producers push, consumers subscribe; no
`sleep`/`interval`/"check every K seconds". Subscribe-receive-current-state-
then-deltas is the contract. Actor mailboxes are push channels; a blocking
handler violates push. Source: `skills/push-not-pull.md`. Relevant to router's
delivery/observation paths and orchestrate's lifecycle observation.

## Part B — The production-readiness checklist (tick per component)

A porter runs this list per component (`message`, `router`, `orchestrate`).
Each item references the rule above. "Done" means **verified in source**, not
asserted.

Schema shape:
1. [ ] `schema/signal.schema`, `schema/nexus.schema`, `schema/sema.schema`
   exist inside the daemon crate; the `*.concept.schema` is deleted. (R1)
2. [ ] Each plane root enum has ≥2 meaningful variants. (R3)
3. [ ] Emission targets wired: signal.schema→SignalRuntime,
   nexus.schema→NexusRuntime, sema.schema→SemaRuntime; ComponentRuntime
   dropped. (R4)
4. [ ] Every internal feature (every filter, computation, conditional write)
   is declared as a Nexus verb+object in `nexus.schema` BEFORE its Rust body
   exists. (R5)

Engine traits + mechanism:
5. [ ] `impl SignalEngine for <DataBearingType>` — triage only, no heavy
   logic. (R6, R8)
6. [ ] `impl NexusEngine for <DataBearingType>` — heavy logic; returns
   `NexusAction` from the 5-variant set. (R6, R9)
7. [ ] `impl SemaEngine for <DataBearingType>` — `apply(&mut self)` writes,
   `observe(&self)` parallel reads. (R6)
8. [ ] All three engines override `on_start`/`on_stop` where they hold
   start-time resources; typed failure reasons. (R7)
9. [ ] No engine impl on a ZST / fieldless struct / via trait-alias macro
   masking a free function. (R8, R26)
10. [ ] Effects (if any) declared in schema; runner dispatches via the
    schema-emitted effect handler. (R10)
11. [ ] Runner loop wired via `triad-runtime` (explicitly until `triad_main!`
    lands). (R11)

Authority + state:
12. [ ] Ordinary surface `signal-<component>` present AND policy surface
    `meta-signal-<component>` present (or its absence is a deliberate
    no-owner decision, R15). Two listener actors, two permission-separated
    sockets via `MultiListenerDaemon`. (R12, R13)
13. [ ] Contract repo named `meta-signal-<component>`, not `owner-signal-*`.
    (R14)
14. [ ] One `<component>.redb` through `sema-engine`; policy tables vs working
    tables split by category. (R18)
15. [ ] `bootstrap-policy.nota` in the repo root; bootstrap-once logic;
    one-shot bootstrap-complete table; working tables never read the file.
    (R16, R17)

Wire + argv:
16. [ ] CLI and daemon each take exactly one NOTA/file argv argument; zero
    flags. (R19)
17. [ ] Daemon socket is signal-frame binary only; rejects NOTA/JSON traffic.
    (R20)
18. [ ] CLI has exactly one Signal peer (its daemon); opens no database/peer
    socket. (R21)
19. [ ] `(Help Main)` + `(Help (Verb …))` present (auto-injected). (R22)

Verbs + replies:
20. [ ] Contract operation roots are domain verbs in verb form; NO Sema
    classification words (`Assert`/`Mutate`/`Retract`/`Match`/`Subscribe`/
    `Validate`) on the public wire; no `AuthorizedSignalVerb` mirror. (R23,
    R24)
21. [ ] Reply success = verb-past-tense; rejection = verb-past-tense +
    `Rejected` with typed reason; typed enums, no string messages. (R25)

Rust discipline:
22. [ ] Zero free functions outside `fn main()`/`#[cfg(test)]`; zero ZST
    namespace method holders. (R26)
23. [ ] Domain values typed, fields private; no string-prefix typification;
    infrastructure mints identity/time/sender. (R27)
24. [ ] One object in / one out; no anonymous tuples at boundaries. (R28)
25. [ ] Methods on schema-emitted nouns; no hand-edited generated mirrors; no
    free helpers around generated types. (R29)
26. [ ] Typed `thiserror` `Error` enum per crate; no `anyhow`/`eyre` at
    boundaries. (R30)
27. [ ] redb+rkyv for durable/wire; no flat files, no JSON between Rust
    components, no NOTA on the inter-component wire. (R31)
28. [ ] Daemon root is an actor; no `Arc<Mutex<T>>` between actors;
    no blocking handlers; supervision + release-before-notify. (R34)

Witness tests:
29. [ ] Each constraint above has a positive witness (compile/execute/
    round-trip/observe) AND a negative guard; no positive grep stands as
    proof. (R35)
30. [ ] A Signal→Nexus→SEMA chain witness drives the real engine traits with
    generated root types; testing-trace socket records prove engine-trait
    usage. (R36)
31. [ ] No-polling witnesses where the component has producer/consumer paths.
    (R37)

A component passes when items 1-31 are verified-in-source. Items 11, 12-15
carry the base-not-yet-landed caveats (R11/R13/R17) — a porter who ticks them
is establishing the pattern, not following a worked example.

## Part C — Code-repo workflow discipline (how the port branches and lands)

These three repos are **code repos under `/git/github.com/LiGoldragon/`** — so
the main-and-next / `~/wt` worktree discipline applies (NOT primary's
always-on-main flow).

C1. **Designers work on `next` / feature branches in `~/wt`; operators own
main + integrate.** Each code repo keeps two long-lived lines: `main` (the
integrated line the operator owns) and `next` (the development line the
designer works on). The designer's home is `next`; when `main` is locked the
designer never blocks on it. Designers do NOT push to main in code repos;
operators do. Source: `skills/main-next.md` + AGENTS.md hard override
([in the CODE repos under /git, designers work on next/feature branches in
~/wt; operators own main + rebase]). Per-component port work lands on a
`next` (or a named feature branch like `triad-engine-port`) in
`~/wt/github.com/LiGoldragon/<component>/<branch>/`, not in the canonical ghq
checkout.

C2. **Worktree mechanics**: `jj workspace add` from the canonical checkout to
`~/wt/github.com/LiGoldragon/<repo>/<branch>/`; the canonical checkout stays
on `main` so peers read it freely; claim the worktree path via
`tools/orchestrate claim`. The same branch name is used across every repo a
multi-repo feature touches (so a port touching `message` +
`meta-signal-message` + `signal-message` uses one branch name across all
three). Source: `skills/feature-development.md`.

C3. **Subagents always create feature branches when touching repos** (the
parent assigns branch name + report path before launch; the dispatch prompt
states the feature-branch requirement so the subagent does not commit to
main). Source: `skills/feature-development.md` §"Subagent feature work".
(This 75 session's map/verify agents are READ-ONLY — they touch no repo
worktree.)

C4. **Per-repo `INTENT.md` and `ARCHITECTURE.md` are updated on the SAME
branch as the work — continuous manifestation, not a deferred pass.** When the
port lands the three-plane schema shape, the engine-trait runtime, and the
meta-signal rename, each repo's `INTENT.md`/`ARCHITECTURE.md` is edited on the
port branch alongside the code. Every repo needs an `INTENT.md`; its absence
is a gap to fill. The repo's `INTENT.md` is read FIRST on entry, before code
or `ARCHITECTURE.md`. Source: `skills/repo-intent.md` §"Continuous
manifestation discipline" (spirit 944) + AGENTS.md required-reading. All three
targets already have `INTENT.md` + `ARCHITECTURE.md` at root (verified) — so
the obligation is to UPDATE them on the port branch, not to create them.

C5. **`jj` inline messages only; commit the whole working copy.** Every
description-taking `jj` invocation passes `-m` inline (never falls back to
`$EDITOR`); `jj commit` takes no path arguments. Source: `skills/jj.md` (AGENTS
hard overrides). On the code-repo worktrees, push the feature branch via
`jj bookmark set <branch> -r @-` + `jj git push --bookmark <branch>`.

## Part D — Where the three components violate the rulebook TODAY

All three are PRE-triad-engine. Verified against source 2026-06-05. This
section is the concrete violation map keyed to the rules above; the per-component
port maps (`4/5/6-*-production.md`) carry the full plans.

### D1. Schema: concept.schema vs the three-plane split (R1, R2, R4 — all three)

Every target carries a single `*.concept.schema`, not the three-plane
`schema/{signal,nexus,sema}.schema`:

- `message/schema/message.concept.schema` — verified its head is the OLD
  concept form: a flat operation list `[(Submit …) (Query …) (Validate …)]`
  with a single trailing namespace, no plane split, no Nexus feature catalog,
  no SemaEngine apply/observe surface. Payloads are `Text(String)` stubs.
- `router/schema/router.concept.schema` — single concept schema.
- `orchestrate/schema/orchestrate.concept.schema` PLUS the pre-`schema-next`
  versioned files `orchestrate-v0-1.schema`, `orchestrate-v0-1-1.schema`,
  `orchestrate-types-v0-1.schema`, `orchestrate-storage-v0-1.schema` (verified
  present). Orchestrate carries the most schema debt — both the concept form
  AND a legacy versioned-schema generation to retire.

Consequence: none of the three has a Nexus feature catalog (R5), so none has
the "every internal feature is a declared Nexus verb" property. Their internal
logic is hand-written and invisible to schema today. The port's FIRST design
move per component is enumerating internal features into nexus.schema verbs.

### D2. Runtime: Kameo / thread hand-daemon vs the engine-trait runner (R6-R11)

None of the three implements `SignalEngine`/`NexusEngine`/`SemaEngine` or uses
`triad-runtime`. None depends on `triad-runtime` in Cargo.toml (verified).

- `message` — Kameo hand-daemon: `message/src/daemon.rs` uses
  `kameo::actor::{Actor, ActorRef, …}`, `kameo::message::{Context, Message}`,
  a `tokio::runtime::Runtime`, and a raw `std::os::unix::net::UnixListener`.
  Cargo deps: `kameo` (a `persona-lifecycle-terminal-outcome` branch),
  `signal-core`, `signal-frame`, `signal-persona`, `signal-message`. **No
  `sema`/`sema-engine` dependency at all** — message is described as a
  stateless boundary, so its port likely carries a thin or stateless SEMA
  plane (a design decision for the map: whether message needs durable state).
- `router` — Kameo hand-daemon (`kameo 0.20`, `tokio`). Daemon binary is
  `router-daemon` at `src/main.rs` (verified `[[bin]] name = "router-daemon"
  path = "src/main.rs"`; `src/bin/` is empty). Hand-written modules:
  `channel.rs`, `delivery.rs`, `adjudication.rs`, `harness_delivery.rs`,
  `harness_registry.rs`, `observation.rs`, `tables.rs`. Depends on `sema`
  **directly** (not `sema-engine`) — R18 wants `sema-engine` as the default.
- `orchestrate` — the most advanced and the furthest from the runner shape in
  one specific way: it is a **`std::thread`-based hand-daemon with FREE
  FUNCTIONS**. `orchestrate/src/daemon.rs` carries
  `thread::spawn(... accept_ordinary ...)`, `accept_owner`, an upgrade thread,
  and `fn bind_socket(path: &Path)` — all module-level free functions, a
  direct R26 violation. It depends on `sema-engine` (good, matches R18) and
  has the richest domain (claims, activities, lanes, divergence, handover,
  lowering). It already has TWO sockets (ordinary + owner) — but via threads
  and free functions, not via `MultiListenerDaemon` + two listener engine
  impls.

### D3. Authority/contracts: owner-signal vs meta-signal, missing policy (R12-R15)

- `message` — has `signal-message` only. **No `owner-signal-message` and no
  `meta-signal-message`** (verified). So message has NO policy contract today.
  Whether this is an R15 legitimate no-owner case or an R12 gap is a design
  question for the map: does mind/orchestrate issue policy to message?
- `router` — has `signal-router` + `owner-signal-router` (verified both exist;
  `owner-signal-router/schema/owner-signal-router.concept.schema`). The
  policy contract exists but is named `owner-signal-*` — an R14 rename to
  `meta-signal-router` is required, and it is still a `.concept.schema` stub.
- `orchestrate` — has `signal-orchestrate` + `owner-signal-orchestrate`
  (verified; daemon depends on both). Same R14 rename required to
  `meta-signal-orchestrate`; both are `.concept.schema` stubs.

All policy contracts that exist are `owner-signal-*` concept stubs. The
`meta-signal-*` prefix is real and adopted for OTHER components
(`meta-signal-cloud`, `-domain-criome`, `-upgrade` exist) — so the rename has
precedent but has not reached these three.

### D4. Public-wire Sema vocabulary (R24 — router + orchestrate named directly)

`skills/contract-repo.md` names **signal-router and signal-orchestrate** among
the six legacy contracts still carrying Sema classification vocabulary on the
public wire (`Assert`/`Match`/`Mutate` roots or an `AuthorizedSignalVerb`
mirror). Their port must move those to domain verbs (R23/R24). (signal-message
is not on that named list; its concept schema already uses domain verbs
`Submit`/`Query`/`Validate` — verified — so message is cleaner on R24.)

### D5. The base-not-yet-landed dependencies a porter must NOT assume away

Honesty markers for any "the port is unblocked" claim downstream:
- `triad_main!` macro does NOT exist yet (R11) — wire the runner explicitly.
- No worked two-socket triad-engine daemon exists yet (R13) — `spirit` is
  single-listener; `MultiListenerDaemon` is committed but unexercised by a
  reference daemon. orchestrate's two-socket precedent is the OLD thread shape.
- `bootstrap-policy.nota` is not present in the reference (R17) — bootstrap is
  invariant-on-paper for components introducing policy state.
- These three port-blocking items are independent of the also-named-in-frame
  blockers (sema-engine emit, primary-vllc dual-lowering, the meta-signal
  rename slices) which the per-component maps and `7-verification.md` track.

## Sources (read in full)

`skills/component-triad.md`, `skills/nota-design.md`, `skills/rust-discipline.md`
+ `skills/rust/{methods,errors,storage-and-wire,parsers,crate-layout}.md`,
`skills/abstractions.md`, `skills/actor-systems.md`,
`skills/micro-components.md`, `skills/contract-repo.md`,
`skills/push-not-pull.md`, `skills/architectural-truth-tests.md`,
`skills/feature-development.md`, `skills/main-next.md`, `skills/repo-intent.md`,
`skills/skills.nota`. Ground-checked against `spirit/`, `triad-runtime/`,
`schema-rust-next/` and the three target repos' source.
