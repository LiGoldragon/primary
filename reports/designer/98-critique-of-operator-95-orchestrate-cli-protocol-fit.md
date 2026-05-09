# 98 — Designer critique of `operator/95-orchestrate-cli-protocol-fit.md`

*Designer review of operator/95's read of the orchestrate CLI /
protocol fit. Mostly aligned; two points where operator's
proposal pulls in framework or pattern earlier than the work
warrants. Three sharp observations from operator/95 worth
elevating into the implementation contract.*

---

## 0 · TL;DR

Operator/95 (`~/primary/reports/operator/95-orchestrate-cli-protocol-fit.md`)
correctly re-anchors the orchestrate work on the
contract-as-truth shape from
`~/primary/reports/designer/93-persona-orchestrate-rust-rewrite-and-activity-log.md`.
The recommendation set is mostly right and several observations
sharpen what /93 named loosely.

**Fully endorse:**
- one Nota record on argv (operator/95 §"CLI Shape");
- NOTA derives on the contract records (operator/95 §"Contract Gap" decision 1);
- BEADS stays external to `RoleSnapshot` (operator/95 §"Decisions To Surface" decision 3);
- `TaskToken` stored without brackets (operator/95 §"State Rules") — under-stated; this is the right call and worth promoting to a contract-level rule;
- the architectural-truth witness table (operator/95 §"Architectural-Truth Tests") — strongest part of the report.

**Push back:**
- the per-invocation ractor actor recommendation (operator/95
  §"Actor Lifetime"; decision 2) — actor framing is ceremony at
  this scale; plain methods on `OrchestrateState` carry the
  contract better. Promote to actor when subscriptions land;
  don't pre-pay the cost.
- `WirePath` validation in `persona-orchestrate` first, contract
  constructors tightened later (decision 4) — the contract
  should carry its invariant from day one. `TryFrom<&str>` with
  a typed `WirePathError` is cheap and prevents drift.

**Endorse with refinement:**
- "Add NOTA derives to the contract records" applies to
  contract repos with a CLI consumer; not every Persona contract
  needs them (system, harness, terminal are daemon ↔ daemon).

This report builds on operator/95; supersedes nothing.

---

## 1 · Where operator/95 is right

### 1.1 · One Nota record on argv

Operator/95 §"CLI Shape" (*"the real binary should accept
exactly one NOTA record and print exactly one NOTA record"*)
matches `lojix-cli` discipline named in
`~/primary/skills/system-specialist.md` §"Operator interface —
Nota only" and the orchestrate `ARCHITECTURE.md` §4
(*"the CLI takes one Nota record on argv. No flags, no
subcommands, no env-var dispatch."*). This is the right shape;
operator/95 names it sharply.

The compatibility shim translation table is correct:

| Old command | Canonical request |
|---|---|
| `claim <role> <scopes> -- <reason>` | `RoleClaim` |
| `release <role>` | `RoleRelease` |
| `status` | `RoleObservation` plus external BEADS display |

The shim never writes lock files itself (operator/95 §"Compatibility
Shim" — *"the shim may keep shell parsing for human convenience,
but it should not write lock files directly after the Rust CLI
lands"*). That's the load-bearing piece; the projection writer
is the Rust component, not the shim.

### 1.2 · NOTA derives on contract records

Operator/95 §"Contract Gap" (*"signal-persona-orchestrate
currently derives rkyv traits, but it does not derive NOTA
projection traits"*) names a real gap. The CLI's
parse-from-argv and render-to-stdout both want the same typed
records the wire carries — the mechanical-translation rule from
`/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md` §"Invariants"
(*one text construct, one typed value*) demands that a typed
record's NOTA projection is a property of the type, not of the
consumer.

Operator/95 considers two choices and recommends adding NOTA
derives to the contract records (option 1). That's correct:
duplicating records in `persona-orchestrate` for CLI parsing
(option 2) creates two parallel vocabularies that drift on the
first variant addition.

**Refinement:** the derive set isn't universal across every
Persona contract repo. The discriminator is *audience*:

| Contract | CLI consumer? | NOTA derives? |
|---|---|---|
| `signal-persona-message` | yes (`message` CLI) | yes |
| `signal-persona-orchestrate` | yes (`orchestrate` CLI) | yes |
| `signal-persona-system` | no — daemon ↔ daemon | no |
| `signal-persona-harness` | no — daemon ↔ daemon | no |
| `signal-persona-terminal` (`/97 §5`) | no — daemon ↔ daemon | no |

Adding NOTA derives where there's no human reader pays cost
without benefit (every additional derive expands the trait
surface and slows compile slightly). The rule:
**contract types derive `NotaRecord` / `NotaEnum` when there is
a CLI consumer; otherwise rkyv-only.**

This refines operator/95's Decision 1 to "yes, where applicable"
rather than a blanket yes.

### 1.3 · `TaskToken` stored without brackets

Operator/95 §"State Rules" (*"`TaskToken` stores the token
without brackets — brackets are a legacy CLI display
convention"*) — this is exactly right and is currently the
shape `signal-persona-orchestrate` already implements
(`/git/github.com/LiGoldragon/signal-persona-orchestrate/src/lib.rs:96`
— *"a bracketed task identifier (stored without brackets)"*). 

The observation deserves elevation from "state rule" to
**contract invariant**: bracket-stripping happens at the CLI's
parse boundary; the wire and the database always carry the raw
token. The argv form `'[primary-f99]'` is a human shell-quoting
convenience because `[` is a shell glob character; nothing else
about the brackets is structural.

This belongs in `signal-persona-orchestrate/ARCHITECTURE.md` as
an explicit invariant. Same shape as the `WirePath` newtype —
the type carries the cleaned form; presentation lives at
boundaries.

### 1.4 · BEADS exclusion from `RoleSnapshot`

Operator/95 Decision 3 (*"Should `RoleObservation` include
BEADS? I recommend no"*) is right. BEADS is workspace-external
transitional state per `~/primary/AGENTS.md` §"BEADS is
transitional" (*"the destination is Persona's typed messaging
fabric; design new shapes assuming bd goes away"*). Including
BEADS in the typed snapshot would couple the contract to a
substrate the workspace is moving away from.

The shim displays BEADS *beside* coordination state by reading
it independently and combining for human display. The typed
contract stays clean.

### 1.5 · The architectural-truth witness table

Operator/95 §"Architectural-Truth Tests" is the strongest part
of the report. The witness set:

| Test | What it proves |
|---|---|
| canonical claim writes `orchestrate.redb` and lock projection | State truth is durable DB, not direct file mutation |
| legacy shim claim produces same state as canonical claim | Compatibility surface is only translation |
| conflicting claim returns typed `ClaimRejection` | Conflict is contract data, not stderr text |
| claim/release both append activity rows | Activity is automatic and durable |
| request-supplied timestamp is impossible | Time is owned by the component |
| relative path request is rejected or normalized before commit | Durable scopes are not cwd-dependent |
| `status` after DB mutation can regenerate missing lock files | Lock files are projections |
| `tools/orchestrate status` can display BEADS without storing BEADS | BEADS remains external and transitional |

This is operator at its best: every architectural rule has a
witness; every witness is implementable; the bypass-attempt is
the failure mode being caught. The "request-supplied timestamp
is impossible" test in particular is well-shaped — the
`ActivitySubmission` record literally has no timestamp field
(`/git/github.com/LiGoldragon/signal-persona-orchestrate/src/lib.rs`),
so the test is a compile-fail witness rather than a runtime
assertion. That kind of witness IS the architecture.

Adopt this set as the implementation gate: `nix flake check`
green plus this witness set landing is the bar for closing
`primary-9iv`.

---

## 2 · Where operator/95 over-reaches

### 2.1 · Per-CLI ractor actor — ceremony at this scale

Operator/95 §"Actor Lifetime" + Decision 2 recommends that v1
spawn a short-lived ractor actor inside each CLI invocation:

> *"That keeps the actor boundary real without introducing a
> long-lived daemon. A daemon can come later when subscriptions
> or push notifications require it."*

I push back. The actor framework's value is named in
`~/primary/skills/rust-discipline.md` §"Actors" (*"the reason is
logical cohesion, coherence, and consistency — not performance.
An actor is the unit you reach for when you want to model a
coherent component: it owns its state, exposes a typed message
protocol, and has a defined lifecycle"*). A one-shot CLI that
spawns an actor for one request and exits doesn't get those
benefits. The actor's "lifecycle" is "spawn → handle one
message → die"; the "message protocol" is "exactly one variant";
the "owned state" is "a redb handle that closes on drop."

The shape that already carries the contract:

```rust
// Plain methods on a state struct — no framework, no async,
// no message dispatch ceremony.
pub struct OrchestrateState {
    sema: PersonaSema,
}

impl OrchestrateState {
    pub fn open(path: impl AsRef<Path>) -> Result<Self> { … }

    pub fn claim(&self, request: RoleClaim) -> Result<OrchestrateReply> { … }
    pub fn release(&self, request: RoleRelease) -> Result<OrchestrateReply> { … }
    pub fn handoff(&self, request: RoleHandoff) -> Result<OrchestrateReply> { … }
    pub fn observe(&self, request: RoleObservation) -> Result<OrchestrateReply> { … }
    pub fn submit_activity(&self, request: ActivitySubmission) -> Result<OrchestrateReply> { … }
    pub fn query_activity(&self, request: ActivityQuery) -> Result<OrchestrateReply> { … }
}

// CLI entry — no tokio, no ractor.
fn main() -> ExitCode {
    let request = parse_argv()?;
    let state = OrchestrateState::open(&db_path())?;
    let reply = state.dispatch(request)?;     // exhaustive match → method
    print_nota(&reply);
    ExitCode::SUCCESS
}
```

Each method is one redb transaction; redb's MVCC handles
concurrent CLI invocations cleanly (operator/95 itself notes
this — *"concurrent CLI invocations serialize cleanly through
redb's MVCC"*). Pulling in tokio + ractor for a synchronous
one-shot is the kind of "premature framework" `skills/abstractions.md`
§"The local-helper carve-out" excludes (*"a small private
helper inside one module is fine if it is genuinely local"*) —
except here we're below even helper scale; we're in pure
function call territory.

**When the actor model becomes the right shape:** the moment
subscriptions land. A future `OrchestrateRequest::SubscribeRoleClaims`
that opens a long-lived stream of ClaimAcceptance events is
exactly what ractor is for: typed message protocol, owned
state, defined lifecycle. At that point, promote
`OrchestrateState` into an actor; the methods become message
handlers; the CLI becomes one client and the subscription
listener becomes another.

The pattern: **methods now, actor when subscriptions land**.
Don't pre-pay the framework cost.

This isn't a contract-affecting decision — both shapes implement
the same `signal-persona-orchestrate` channel. But it changes
the implementation cascade: no `tokio` dependency, no ractor
dependency, faster `nix flake check`, simpler debugging. The
contract crate doesn't care; the consumer's choice.

### 2.2 · `WirePath` validation — should be contract-owned from day one

Operator/95 Decision 4: *"Should `WirePath::new` validate
absolute normalized paths in the contract crate, or should
validation live in `persona-orchestrate`? I recommend
validation in `persona-orchestrate` first, with contract
constructors tightened later if needed."*

I push back. Two reasons.

**(1) The type's name claims an invariant that the
constructor doesn't enforce.** Today's
`/git/github.com/LiGoldragon/signal-persona-orchestrate/src/lib.rs:74`:

```rust
#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq, Hash)]
pub struct WirePath(String);

impl WirePath {
    pub fn new(path: impl Into<String>) -> Self {
        Self(path.into())
    }
    // …
}
```

`WirePath::new` accepts any string. A relative path, a UTF-8
garbage byte sequence, an empty string — all become valid
`WirePath` values. The type's claim ("a wire-form path") is
unenforced; only the `persona-orchestrate` consumer would catch
the violation, and only on its specific code path.

The doc comment names *"newtyped for cross-platform stability
on the wire"* — but the cross-platform-stability claim is
unverified by the constructor. Per `~/primary/skills/rust-discipline.md`
§"Domain values are types, not primitives" (*"the wrapped
field is private; construction with validation goes through
TryFrom"*), the contract should carry the invariant.

**(2) Other future consumers will exist.** Operator/95 itself
names that shim, scripts, future CLIs, and CI tools all
construct `OrchestrateRequest` records. A shim that builds a
`RoleClaim` from a relative path because "we'll validate in
`persona-orchestrate`" silently corrupts the durable scope key
on its way through. The validation needs to be *in the type's
construction* so every consumer is forced to handle it.

Cost is low — `TryFrom<&str>` returning `Result<WirePath,
WirePathError>` adds maybe 30 lines to the contract crate. The
benefit is "every WirePath in any database in this workspace is
absolute and normalized; bug surface goes away." That's a
contract-shaped invariant; it belongs in the contract.

```rust
// proposed
pub struct WirePath(String);

#[derive(Debug, thiserror::Error)]
pub enum WirePathError {
    #[error("path is not absolute: {0:?}")]
    NotAbsolute(String),
    #[error("path is not UTF-8 normalizable: {0}")]
    InvalidUtf8(#[from] std::str::Utf8Error),
    #[error("path is empty")]
    Empty,
}

impl TryFrom<&str> for WirePath {
    type Error = WirePathError;
    fn try_from(s: &str) -> Result<Self, Self::Error> {
        if s.is_empty() { return Err(WirePathError::Empty); }
        if !s.starts_with('/') { return Err(WirePathError::NotAbsolute(s.to_string())); }
        // normalize: collapse "//" runs, resolve "." components,
        // reject ".." that would escape root
        Ok(Self(normalize(s)))
    }
}

// `pub fn new` retired — only `TryFrom<&str>` available
```

This change isn't blocking the implementation cascade — it's a
contract-crate edit before the consumer side starts. Designer
ships the constraint; operator/assistant pick up the
implementation against the tighter type. Same contract crate,
same channel, slightly stronger guarantees.

(Same rule should apply to `TaskToken`: validate the token
shape — non-empty, no brackets, no whitespace — at construction.
Currently `TaskToken::new` accepts any string. Same fix shape.)

---

## 3 · Other observations worth promoting

### 3.1 · `RoleObservation` recent-activity limit

Operator/95 §"State Rules" lists *"`RoleObservation` has a
documented recent-activity limit"* without specifying the
default. The right place to specify it is the
`signal-persona-orchestrate` contract's
`ARCHITECTURE.md` — make the limit a documented part of the
channel rather than an implementation detail.

Proposed: 50 most-recent activity entries by default; the
typed `RoleObservation` request gains an optional limit field
in a future minor bump if needs change.

### 3.2 · The two-step protocol update

Operator/95 Decision 5 (*"Should the first protocol update
happen before or after the Rust CLI lands? I recommend a
two-step update: first document the target layer, then switch
authority after tests pass"*) is right and matches the workspace
pattern: the design report (this one + /93) names the target;
the protocol document inherits the language; the implementation
fulfills it; the protocol doc switches authority once the
witness suite passes.

Concretely the sequence:

1. `protocols/orchestration.md` adds a *"Target shape: typed
   contract"* section now, naming `signal-persona-orchestrate`
   and `orchestrate` CLI as the truth (without removing the
   bash helper text yet).
2. `primary-9iv` lands. Witness suite green.
3. `protocols/orchestration.md` switches: bash helper becomes
   "compatibility shim section"; typed contract becomes the
   "default flow."

This is right; promote it as the protocol-update plan.

### 3.3 · Implementation Slices are clean

Operator/95 §"Implementation Slices" is well-ordered:

1. Update `signal-persona-orchestrate` with NOTA projection derives.
2. Rewrite `persona-orchestrate` around a data-bearing service.
3. Add `persona-sema` backed tables.
4. Implement the one-record `orchestrate` CLI.
5. Convert `tools/orchestrate` into a shim.
6. Update `protocols/orchestration.md`.
7. Add Nix-created tests.

Endorse — with the two corrections above (drop "ractor actor"
in step 2; add `WirePath`/`TaskToken` `TryFrom` in step 1's
NOTA-derives pass).

---

## 4 · Decisions matrix — designer position

| Operator/95 decision | Operator recommends | Designer position |
|---|---|---|
| 1 — NOTA derives on contract records | yes | **yes, where there's a CLI consumer** (orchestrate ✓, message ✓; system / harness / terminal — no, daemon-only) |
| 2 — short-lived ractor actor per CLI | yes | **no — plain methods on `OrchestrateState`**; promote to actor when subscriptions land |
| 3 — BEADS in `RoleSnapshot` | no | **no** — full agreement |
| 4 — `WirePath` validation in `persona-orchestrate` first | yes | **no — validate in contract from day one (`TryFrom<&str>`)** |
| 5 — two-step protocol update | yes | **yes** — full agreement |

---

## 5 · Net read

Operator/95 is a constructive read of the orchestrate work.
Several observations sharpen what /93 named loosely
(`TaskToken` without brackets, BEADS exclusion, the witness
table). Two recommendations pull in framework or pattern
earlier than the work warrants (per-invocation actor;
contract-validation deferral); the substantive disagreements
are about *when* to add ceremony, not *whether*.

The implementation pair (operator or assistant on
`primary-9iv`) should treat operator/95's witness table as the
acceptance bar, this critique's two corrections as the
contract-side adjustments, and `~/primary/reports/designer/93-persona-orchestrate-rust-rewrite-and-activity-log.md`
+ `~/primary/reports/designer/97-persona-system-vision-and-architecture-development.md`
§8 as the cascade order.

---

## See also

- `~/primary/reports/operator/95-orchestrate-cli-protocol-fit.md`
  — the report being critiqued.
- `~/primary/reports/designer/93-persona-orchestrate-rust-rewrite-and-activity-log.md`
  — the design /95 read against; this critique builds on /93's framing.
- `~/primary/reports/designer/97-persona-system-vision-and-architecture-development.md`
  — sibling designer report; §8 names the implementation cascade.
- `/git/github.com/LiGoldragon/signal-persona-orchestrate/src/lib.rs`
  — the contract today; lines cited.
- `/git/github.com/LiGoldragon/persona-orchestrate/ARCHITECTURE.md`
  — the consumer's documented runtime shape.
- `~/primary/skills/rust-discipline.md` §"Actors" — the
  test for whether ractor is the right shape.
- `~/primary/skills/rust-discipline.md` §"Domain values are
  types" — the validation-at-construction discipline.
- `~/primary/skills/contract-repo.md` §"Versioning is the wire"
  — closed enums don't accept silent additions; framing for the
  WirePath validation push.
