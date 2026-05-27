# 222 — Schema-at-heart test truth audit

## Frame

Psyche asked whether the current prototype tests are actually proving the
schema-at-heart concept, or only proving a hand-written Rust story that looks
schema-shaped. I captured that as Spirit record 1005.

This audit checks two current surfaces:

- Operator main: `/git/github.com/LiGoldragon/spirit-next` at `f12d11e2`
  (`spirit: drive tests through schema plane traits`).
- Designer cycle-2 prototype: `/home/li/wt/github.com/LiGoldragon/spirit-next/designer-prototype-schema-driven-cycle-2-2026-05-27`
  at `cf17e67c` (`designer: regenerate src/schema/lib.rs against latest
  schema-stack mains`), reported in `/reports/designer/403`.

My opinion: the direction is right. The tests should prove the whole chain:
schema files lower into generated Rust; generated Rust owns Signal, Nexus, and
SEMA data types and traits; the CLI and daemon communicate over the real binary
Signal boundary; Nexus processes schema messages in the middle; SEMA takes and
returns SEMA schema objects for database work. Per Spirit record 1007, full
SEMA proof means a durable database write, not just an in-memory store call. We are partly there. Operator main proves the
kernel more honestly than `/403`; `/403` adds useful scenario coverage but
also regresses two important constraints.

## Current Situation

Operator main passes the local-stack Nix check with real local dependency
overrides:

```sh
cd /git/github.com/LiGoldragon/spirit-next
scripts/check-local-schema-stack --print-build-logs
```

That command builds `spirit-next` while overriding:

- `nota-next-source` to `/git/github.com/LiGoldragon/nota-next`
- `schema-next-source` to `/git/github.com/LiGoldragon/schema-next`
- `schema-rust-next-source` to `/git/github.com/LiGoldragon/schema-rust-next`

The Nix run executed 13 flake checks and ran 16 Rust tests under the Nix build:
6 generated signal-plane tests, 1 process-boundary test, and 9 runtime-triad
tests.

Designer cycle-2 also passes its local-stack check and reports 28 tests. That
is valuable, but its branch is not a clean extension of operator main's
strongest constraints. It removes the generated `Output::Rejected` surface from
`schema/lib.schema`, routes validation rejection through `Output::Error`, and
uses inherent `Store::apply` instead of the generated `SemaEngine` trait.

## Strong Proof Already Present On Operator Main

### 1. Nix Really Builds The Local Stack

`spirit-next/scripts/check-local-schema-stack` is a real local override runner.
It does not rely on ambient Cargo paths. It asks Nix to build `spirit-next`
against the actual local checkouts for `nota-next`, `schema-next`, and
`schema-rust-next`.

The flake also patches those local sources into Cargo inside the Nix source
tree, then strips git source lines from `Cargo.lock`. That is the right shape:
the stack is built together as packages, not tested by ad hoc local commands.

### 2. Schema Emission Is In The Build Path

Operator main's flake check `generated-schema-source-checked-in` requires
`build.rs` to call the schema lowering and Rust emission path, including:

- `SchemaEngine::default`
- `lower_source_with_context`
- `RustEmitter::default().emit_file`
- `assert_checked_in_schema_is_fresh`

It also forbids build-time hidden source writes and `include!(OUT_DIR)` for the
generated schema module. That proves the checked-in `src/schema/lib.rs` is the
artifact the runtime uses.

This is not a full semantic proof of every generated line, but it is a good
structural witness that the runtime is not bypassing schema emission.

### 3. Main Uses Generated Plane Traits

Operator main now has the schema emitter generate:

```rust
pub trait NexusEngine {
    fn execute(&self, input: NexusInput) -> NexusOutput;
}

pub trait SemaEngine {
    fn apply(&mut self, input: SemaInput) -> SemaOutput;
}
```

`spirit-next` implements those generated traits on runtime objects:

- `Engine` implements `NexusEngine`.
- `Store` implements `SemaEngine`.

The strongest test on main is
`schema_emitted_traits_drive_the_full_plane_chain` in
`/git/github.com/LiGoldragon/spirit-next/tests/runtime_triad.rs`. It explicitly
walks:

```rust
Input
  -> SignalAccepted
  -> NexusOutput
  -> SemaInput
  -> SemaOutput
  -> Output
```

and the load-bearing calls include:

```rust
let sema_output: SemaOutput = SemaEngine::apply(&mut sema_engine, sema_input);
let signal_output: Output =
    NexusEngine::execute(&nexus_engine, NexusInput::Sema(sema_output)).into_signal_output();
```

That is a real concept proof: the test would fail to compile if the generated
traits disappeared or if the runtime only exposed primitive helper methods.

### 4. The CLI/Daemon Boundary Is Real

Operator main's process-boundary test launches the real daemon binary and talks
to it with the real CLI binary:

```rust
Command::new(env!("CARGO_BIN_EXE_spirit-next-daemon"))
Command::new(env!("CARGO_BIN_EXE_spirit-next"))
```

The test uses a real Unix socket under a temporary directory and sends NOTA
through the CLI. The daemon returns:

```text
(RecordAccepted (1 (1 39)))
(RecordsObserved (([schema] Constraint [schema creates the interface] Maximum) (1 39)))
(Rejected (EmptyTopic (1 39)))
```

That proves more than an in-process runtime story. It proves the actual CLI,
daemon, NOTA parser, Signal frame transport, runtime engine, and output renderer
work together inside the Nix test build.

## Weak Or Pretend-Prone Areas

### 1. Some Nix Checks Are Grep Witnesses

The flake's `generated-signal-plane-used` and `runtime-triad-visible` checks
grep for important strings. That is useful as a tripwire, but it can be fooled:
a stale string in a comment or dead file could pass the check.

The real compile-and-run tests currently carry the proof. The grep checks
should increasingly become supplements, not primary proof.

Better next witness: a compile-time API test or `trybuild`-style negative test
that fails if `Store` does not implement generated `SemaEngine`, if `Engine`
does not implement generated `NexusEngine`, or if `Output::Rejected` is not a
generated variant.

### 2. The Runtime Is Still Mostly In One Process

Main has a real CLI/daemon boundary, but the Nexus executor and SEMA store are
inside one daemon process. That is acceptable for this prototype, but it means
we are not yet proving a multi-component system where Signal, Nexus, and SEMA
are separately observable actors.

The current test proves the data-plane shape more than the actor/process
topology.

Better next witness: make the daemon emit a typed trace artifact for:

```text
SignalAccepted -> MessageSent -> NexusInput -> SemaInput -> SemaOutput -> MessageProcessed -> Output
```

and assert that artifact in a second Nix check.

### 3. SEMA Is Still In-Memory, So It Is Only A Language Prototype

`Store` is an in-memory vector. The tests prove SEMA takes `SemaInput` and emits
`SemaOutput`, but they do not prove SEMA in the strict sense from record 1007:
database work that writes durable state to the component database file. They do
not prove durable SEMA storage, database reopening, or state transfer across
derivation boundaries.

The current physical substrate is redb. Renaming the component database from a
`.redb` extension to `.sema` is a plausible clarity move, because it makes the
file's architectural role visible instead of naming the implementation library.

Better next witness: a chained Nix test:

1. Start daemon and record data.
2. Persist `state.sema` (or `state.redb` until the extension changes) as the first derivation's
   output.
3. Read it in a second derivation using the authoritative Spirit reader.
4. Assert typed `SemaOutput` / Signal `Output`.

Until that exists, claims that the prototype has proved SEMA itself should stay
qualified. It proves the SEMA schema language and generated trait boundary; it
does not yet prove durable SEMA database work.

### 4. One Schema File Still Contains Three Planes

The current `schema/lib.schema` declares Signal, Nexus, and SEMA types in one
file. That does prove the generated type chain, but not the newer three-schema
shape where `.signal.schema`, `.nexus.schema`, and `.sema.schema` share the same
import/export protocol.

Better next witness: split the schema files and make the flake fail if one plane
imports a type not exported by the other.

## Audit Of `/403`

`/403` has useful tests. The scenario coverage around multi-observer fanout,
RAII subscriptions, typed `MailLedgerEvent` vectors, and step-by-step per-plane
chain tests is worth harvesting.

But `/403` is not safe to merge as-is.

### Finding 1 — It Regesses The Generated SEMA Trait Surface

The report says `Store::apply` is a trait surface, but the branch implements it
as an inherent method:

```rust
impl Store {
    pub fn apply(&mut self, command: SemaInput) -> SemaOutput { ... }
}
```

The branch's flake check also greps for `pub fn apply`, not
`impl SemaEngine for Store`. That means the test can pass while bypassing the
schema-emitted `SemaEngine` trait. Operator main is stronger here: it requires
`impl SemaEngine for Store` and tests `SemaEngine::apply`.

### Finding 2 — It Does Not Use Generated `NexusEngine`

The branch contains generated `pub trait NexusEngine`, but no `impl NexusEngine`
and no test calling `NexusEngine::execute`. The scenario tests call
`InputNexus::record` and direct conversion methods. That proves some Nexus data
typing, but not the newer generated Nexus engine trait.

Operator main is stronger here: `Engine` implements generated `NexusEngine`,
and tests call `NexusEngine::execute`.

### Finding 3 — It Removes The Explicit Rejection Variant

Operator main has:

```nota
Output ((RecordAccepted SemaReceipt) (RecordsObserved ObservedRecords) (Error ErrorReport) (Rejected SignalRejection))
SignalRejection [ValidationError DatabaseMarker]
```

The designer branch has `ValidationError`, but routes rejection through
`Output::Error(ErrorReport)` and lacks `SignalRejection` / `Output::Rejected`.
That loses a useful schema distinction: ordinary SEMA/query errors and Signal
admission rejections are no longer different output variants.

For the current intent, main's `Output::Rejected(SignalRejection)` is the better
shape.

### Finding 4 — Its Process Boundary Is Weaker Than Main

The branch process-boundary test still launches CLI and daemon, but it only
records and observes. It does not test invalid input over the real socket. Main
does test invalid input through the CLI/daemon boundary and expects the
generated rejection output.

### Finding 5 — The 28 Tests Are Useful But Not Decisive

The 16 added tests are useful design examples, especially:

- typed fanout to multiple observers;
- RAII observer unregistration;
- lifecycle event vectors as `Vec<MailLedgerEvent>`;
- explicit per-plane local variables.

But several tests assert the typed shape while still entering through weaker
surfaces (`store.apply`, `engine.record`, conversion methods). They should be
ported onto main's stronger generated-trait spine before being treated as
architectural truth tests.

## What Should Happen Next

### Immediate Integration

Do not merge `/403` mechanically. Rebase its useful scenario tests onto
operator main and preserve these main constraints:

- `Store` implements generated `SemaEngine`.
- `Engine` implements generated `NexusEngine`.
- tests call `SemaEngine::apply` and `NexusEngine::execute` where they claim
  plane-engine proof;
- validation rejection stays `Output::Rejected(SignalRejection)`;
- process-boundary still tests rejection through the real CLI/daemon socket.

### Stronger Nix Witness

Add a named Nix check that is more than grep and more than in-process Cargo
tests. The best next shape is a chained or scripted check that:

1. Builds `nota-next`, `schema-next`, `schema-rust-next`, and `spirit-next`
   through local path overrides.
2. Starts `spirit-next-daemon` from the built package.
3. Drives `spirit-next` CLI through NOTA input.
4. Captures a typed trace or artifact proving the chain:
   Signal input -> Nexus input/output -> SEMA input/output -> Signal output.
5. Validates the artifact using schema-emitted types, not string greps.

The current process-boundary test already does steps 1-3 and part of 5. The gap
is the explicit middle trace through Nexus and SEMA at the daemon boundary.

### Durable SEMA Later

After the in-memory language prototype is tighter, promote SEMA to a durable
database artifact.
That is when a Nix-chained database proof becomes the stronger test:

```text
writer derivation emits state.sema / state.redb artifact
reader derivation consumes only that artifact
authoritative schema reader asserts typed records and marker
```

## Bottom Line

The tests are not just pretending on operator main: the main stack now has real
schema-generated types, generated engine traits, Nix local dependency
overrides, and a real CLI/daemon socket test. It proves the core idea better
than the previous prototype.

It is not yet a full architectural proof of the final system. The biggest
missing proof is a daemon-boundary trace or artifact showing the actual Nexus
and SEMA plane crossings, not only in-process Rust locals. `/403` gives useful
scenario tests, but it must be reworked onto main's stronger trait and rejection
surfaces before it counts as the next truth layer.
