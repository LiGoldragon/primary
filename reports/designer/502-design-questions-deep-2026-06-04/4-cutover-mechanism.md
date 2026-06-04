---
title: 502.4 — The cutover mechanism — gate, migration, rollback
role: designer
variant: Design
date: 2026-06-04
topics: [cutover, spirit, persona-spirit, schema-derived, contract-equivalence, redb-sema-migration, rollback, fd-handoff, criomos-home, deploy-chain]
description: |
  The biggest undesigned gap (report 499): there is no contract-equivalence
  gate, no redb-to-sema data-migration path, and no rollback story for
  replacing production persona-spirit (hand-written) with the schema-derived
  spirit pilot. Today the cutover is a manual one-line CriomOS-home edit
  (currentDefault). This entry shows that verbatim, then proposes the three
  missing mechanisms as real/proposed Rust + Nix: an equivalence GATE
  (both daemons answer the same probe set identically), a redb-to-sema
  DATA-MIGRATION (the From-chain pattern), and a ROLLBACK (keep the old slot
  live, flip back on health-check failure). Future view: persona owns the
  atomic FD-handoff cutover with no downtime.
---

# 502.4 — The cutover mechanism

## What exists today — a manual one-line edit, nothing else

The deploy chain is real and good at *coexistence*; it has no notion of
*switching safely*. Three facts establish that.

### Fact 1 — the version slots are side-by-side packages, selected by one option

`CriomOS-home/modules/home/profiles/min/spirit.nix:23` enumerates every slot,
and `:33` maps each to a flake input:

```nix
# CriomOS-home/modules/home/profiles/min/spirit.nix:23
availableVersions = [
  "v0.1.0" "v0.1.1" "v0.2.0" "v0.3.0" "v0.4.0" "v0.4.1" "next"
];

packageInputsByVersion = {
  "v0.1.0" = inputs."persona-spirit-v0-1-0";
  # ...
  "v0.4.1" = inputs."persona-spirit-v0-4-1";
  "next"   = inputs.persona-spirit-next;        # the schema-derived pilot
};
```

The `next` slot points at the pilot — `flake.nix:150`:

```nix
# CriomOS-home/flake.nix:150
persona-spirit-next.url = "github:LiGoldragon/persona-spirit?ref=main";
```

Each slot gets its own systemd user service, its own state directory, its own
redb database, its own socket — fully isolated. `makeService`
(`spirit.nix:162`) gives every version a `persona-spirit-daemon-${version}`
unit. So *all* versions can run at once; they never share state.

### Fact 2 — the cutover IS the `currentDefault` selector, a manual edit

The unsuffixed `spirit` command is a symlink built by `defaultCommandLine`
(`spirit.nix:157`) pointing at whichever version `currentDefault` names:

```nix
# CriomOS-home/modules/home/profiles/min/spirit.nix:151
selectedDeployment =
  if builtins.elem currentDefault deployedVersions then
    deployments.${currentDefault}
  else
    throw "...currentDefault must be listed in deployedVersions";

defaultCommandLine = pkgs.runCommand "spirit-current-${sanitizeVersion currentDefault}" { } ''
  mkdir -p "$out/bin"
  ln -s "${selectedDeployment.commandLineWrapper}/bin/${selectedDeployment.wrapperName}" "$out/bin/spirit"
'';
```

And `currentDefault` is a plain enum option with a hardcoded default
(`spirit.nix:189`):

```nix
# CriomOS-home/modules/home/profiles/min/spirit.nix:189
currentDefault = mkOption {
  type = enum availableVersions;
  default = "v0.4.1";       # <-- the cutover. Editing this string IS the flip.
  description = "Persona-spirit version reached by the unsuffixed spirit command.";
};
```

**The entire cutover is changing `"v0.4.1"` to `"next"` and rebuilding home.**
There is no proof the two agree, no data carried across, no automatic flip-back.

### Fact 3 — there IS a data-migration precedent, but only redb-to-redb same-stack

The chain already does *one* migration — `v0.3.0 → v0.4.1` privacy widening —
and it shows the shape the cutover lacks. `spirit.nix:99`:

```nix
# CriomOS-home/modules/home/profiles/min/spirit.nix:99
${lib.optionalString (version == "v0.4.1") ''
  previous_privacy_database_path=${lib.escapeShellArg previousPrivacyDatabasePath}
  if [ ! -e "$database_path" ] && [ -e "$previous_privacy_database_path" ]; then
    ${privacyMigration}/bin/spirit-migrate-0-3-to-0-4 "([$previous_privacy_database_path] [$database_path])"
  fi
''}
```

This is the template — a dedicated migration binary, taking one NOTA argument
`([source] [destination])`, run from `ExecStartPre` exactly once. But it
migrates *old-redb → new-redb within the same hand-written stack*. The
hand-written `persona-spirit` redb and the schema-derived `spirit` `.sema`
redb are **different storage shapes**; there is no `persona-spirit.redb →
spirit.sema` migration binary. That is gap #2.

### The FD-handoff already exists in persona — but the selector never uses it

The atomic, no-downtime primitive the future cutover wants is already built in
`persona/src/transport.rs`. The router accepts a public client, finds the
receiver registered for the active version, and passes the live connection FD
across via `SCM_RIGHTS` (`unix-ancillary = "0.2"`, `persona/Cargo.toml:44`):

```rust
// persona/src/transport.rs:294
pub async fn handoff_one(&mut self, active_version: &Version) -> Result<()> {
    let (stream, _address) = self.public_listener.accept().await?;
    let stream = stream.into_std()?;
    stream.set_nonblocking(false)?;
    let receiver = self
        .registry
        .receiver_for(self.endpoint.component_name(), active_version)?;
    receiver.send_fds(b"persona-public-client", &[&stream])?;   // SCM_RIGHTS
    Ok(())
}
```

The receiving side (`persona/tests/handoff.rs:32`) reconstructs the client
stream from the passed FD:

```rust
// persona/tests/handoff.rs:32
let file_descriptor = control.recv_fds::<1>()?.fds[/* 0 */]..;
let mut stream = UnixStream::from(file_descriptor);
```

So persona can already route a client connection to *whichever version is
active* by reading an `active_version` value. **The selector flip and the
FD-handoff are two unconnected mechanisms** — the cutover today is the static
Nix symlink, not the live `active_version` the router reads. Wiring them is the
future view.

## What is missing — the three mechanisms, in order

### Mechanism 1 — the contract-equivalence GATE

**What it proves.** Before the selector names `next`, prove old and new answer
the *same signal contract identically*. The probe surface already exists:
`Engine::handle(&self, input: Input) -> Signal<Output>` (spirit
`src/engine.rs:114`). The gate drives a fixed probe set through *both* daemons'
sockets and asserts byte-identical replies (after canonical normalisation of
known-divergent fields like timestamps).

**Shape.** A standalone `spirit-equivalence-gate` binary, single NOTA argument
`([old-socket] [new-socket] [probe-set-path])`, exit 0 only on full agreement.
It owns a `ProbeSet` and an `EquivalenceVerdict`; each verb is a method on a
real data-bearing noun (no free functions, no ZST namespace).

```rust
// PROPOSED — spirit/src/bin/equivalence_gate.rs (or a sibling crate)
use triad_runtime::{ComponentArgument, ComponentCommand};

/// One probe: a contract input plus the canonical normalisation applied to
/// both replies before comparison. Normalisation strips fields the contract
/// permits to differ (mint identifiers, wall-clock stamps).
#[derive(Debug, Clone)]
pub struct ContractProbe {
    name: ProbeName,
    input: Input,
}

impl ContractProbe {
    /// Drive this probe through one daemon socket and return the canonical
    /// reply bytes (rkyv, with non-deterministic fields zeroed).
    pub fn ask(&self, socket: &SocketAddress) -> Result<CanonicalReply, GateError> {
        let mut transport = SignalTransport::connect(socket)?;
        transport.write_input(&self.input)?;
        let output = transport.read_output()?;
        Ok(CanonicalReply::from(output))   // From<Output> erases mint/stamp
    }
}

/// The full set of probes the two daemons must agree on. Authored as NOTA,
/// loaded as a typed artifact — never a flag list.
#[derive(Debug, Clone)]
pub struct ProbeSet {
    probes: Vec<ContractProbe>,
}

impl ProbeSet {
    /// Run every probe against both daemons; one disagreement fails the gate.
    pub fn judge(
        &self,
        old: &SocketAddress,
        new: &SocketAddress,
    ) -> Result<EquivalenceVerdict, GateError> {
        let mut divergences = Vec::new();
        for probe in &self.probes {
            let old_reply = probe.ask(old)?;
            let new_reply = probe.ask(new)?;
            if old_reply != new_reply {
                divergences.push(ProbeDivergence::new(
                    probe.name.clone(),
                    old_reply,
                    new_reply,
                ));
            }
        }
        Ok(EquivalenceVerdict::from_divergences(divergences))
    }
}

/// The gate's outcome — either both agree, or a list of named divergences.
#[derive(Debug)]
pub enum EquivalenceVerdict {
    Agree,
    Diverge(Vec<ProbeDivergence>),
}

impl EquivalenceVerdict {
    fn from_divergences(divergences: Vec<ProbeDivergence>) -> Self {
        if divergences.is_empty() {
            Self::Agree
        } else {
            Self::Diverge(divergences)
        }
    }

    /// Map the verdict onto a process exit; non-zero blocks the selector flip.
    pub fn into_exit_code(self) -> i32 {
        match self {
            Self::Agree => 0,
            Self::Diverge(divergences) => {
                for divergence in &divergences {
                    eprintln!("equivalence: probe {} diverged", divergence.name());
                }
                1
            }
        }
    }
}
```

The gate is wired into `CriomOS-home` as a Nix *check* — the same place the
existing `persona-spirit-versioned-deployment` check
(`CriomOS-home/checks/persona-spirit-versioned-deployment/default.nix`) lives.
The flip-to-`next` derivation gains an assertion that the gate passed against
the live `v0.4.1` socket. The gate is the precondition expressed as
`currentDefault = "next"` failing to build unless the probe set agrees.

### Mechanism 2 — the redb-to-sema DATA-MIGRATION

**What it carries.** The deployed `persona-spirit.redb` (hand-written stack)
into the schema-derived `spirit.sema` redb. **Precondition: the pilot adopts
sema-engine** so a `.sema` destination exists to write into (report 499's
"sema-engine adoption being the precondition"). Then the migration follows the
canonical two-submodule From-chain pattern from
`skills/spirit-cli.md` §"Substrate migration discipline" — the same shape the
`spirit-migrate-0-3-to-0-4` binary already uses, but crossing stacks:

```rust
// PROPOSED — spirit-migrate-persona-to-schema/src/lib.rs
//
// Follows skills/spirit-cli.md: `mod historical` reproduces the deployed
// hand-written redb leaf types locally (no dependency on persona-spirit's
// crate); `mod current_shape` borrows the schema-derived `Entry` leaves;
// a From-chain composes the conversion. One direction of typed flow.

mod historical {
    //! Local rkyv reproduction of persona-spirit's stored record. Pinned to
    //! the source bytes, NOT to the persona-spirit crate version.
    #[derive(rkyv::Archive, rkyv::Deserialize)]
    pub struct StoredRecord {
        pub topics: Vec<String>,
        pub kind: HistoricalKind,
        pub description: String,
        pub certainty: HistoricalCertainty,   // narrow legacy enum
        pub privacy: HistoricalPrivacy,
    }
    #[derive(rkyv::Archive, rkyv::Deserialize)]
    pub enum HistoricalCertainty { Low, Medium, High, Maximum }
}

mod current_shape {
    //! Binds the schema-derived `spirit` leaves unchanged from the live crate,
    //! overriding only what differs.
    pub use spirit::schema::{Entry, Magnitude, Privacy, Topic, Kind};
}

// The From-chain — leaf maps plus the record map. No per-field handwiring
// at the call site (the discipline's rule 4).
impl From<historical::HistoricalCertainty> for current_shape::Magnitude {
    fn from(certainty: historical::HistoricalCertainty) -> Self {
        // record 70: Certainty widened to the universal Magnitude.
        match certainty {
            historical::HistoricalCertainty::Low => Self::Low,
            historical::HistoricalCertainty::Medium => Self::Medium,
            historical::HistoricalCertainty::High => Self::High,
            historical::HistoricalCertainty::Maximum => Self::Maximum,
        }
    }
}

impl From<historical::StoredRecord> for current_shape::Entry {
    fn from(record: historical::StoredRecord) -> Self {
        current_shape::Entry {
            topics: record.topics.into_iter().map(current_shape::Topic::from).collect(),
            kind: record.kind.into(),
            description: record.description,
            magnitude: record.certainty.into(),   // narrow -> universal
            privacy: record.privacy.into(),
        }
    }
}

/// The migration binary's owning noun: reads source redb, writes sema redb.
pub struct PersonaToSchemaMigration {
    source: SourceDatabasePath,
    destination: SemaDatabasePath,
}

impl PersonaToSchemaMigration {
    /// Read every historical record, run the From-chain, append into the
    /// schema-derived `.sema` store. Idempotent: skips if destination exists.
    pub fn run(&self) -> Result<MigrationReceipt, MigrationError> {
        let source = HistoricalStore::open(&self.source)?;
        let mut destination = SemaStore::create(&self.destination)?;
        let mut carried = 0_usize;
        for stored in source.records()? {
            let entry = current_shape::Entry::from(stored?);   // typed flow
            destination.append(entry)?;
            carried += 1;
        }
        Ok(MigrationReceipt::new(carried))
    }
}
```

Nix wiring mirrors the existing privacy migration — an `ExecStartPre` that runs
the binary once when the `next` slot's `.sema` does not yet exist:

```nix
# PROPOSED addition to makeDeployment in spirit.nix (next slot)
${lib.optionalString (version == "next") ''
  legacy_persona_database_path=${lib.escapeShellArg legacyDatabasePath}
  if [ ! -e "$sema_database_path" ] && [ -e "$legacy_persona_database_path" ]; then
    ${schemaMigration}/bin/spirit-migrate-persona-to-schema \
      "([$legacy_persona_database_path] [$sema_database_path])"
  fi
''}
```

### Mechanism 3 — the ROLLBACK

**What it does.** Keep the old slot live (the chain already does this — every
version has its own service and state). On a post-flip health-check failure,
flip `currentDefault` back to `v0.4.1` *automatically*, without losing the
intent written to `next`'s `.sema` during the trial window.

Because slots are isolated, rollback is cheap structurally — the old daemon
never stopped. What is missing is (a) a health probe that fails fast, and (b)
the automatic flip-back. The health probe reuses the gate's `ContractProbe`
machinery against the *new* socket alone:

```rust
// PROPOSED — spirit/src/bin/cutover_health.rs
/// A post-flip liveness + correctness probe on the newly-active daemon.
/// Distinct from the equivalence gate: the gate compares two daemons
/// pre-flip; this confirms the one live daemon stays healthy post-flip.
pub struct CutoverHealthCheck {
    socket: SocketAddress,
    probes: ProbeSet,
    deadline: HealthDeadline,
}

impl CutoverHealthCheck {
    /// Returns Healthy only if every probe answers within the deadline and
    /// the daemon's own (Health) signal reports Ready. Any failure -> Degraded.
    pub fn assess(&self) -> Result<HealthState, HealthError> {
        for probe in self.probes.liveness_subset() {
            match probe.ask(&self.socket) {
                Ok(reply) if reply.is_ok() => continue,
                _ => return Ok(HealthState::Degraded),
            }
        }
        Ok(HealthState::Healthy)
    }
}
```

The flip-back is owned by persona once persona is the upgrade orchestrator
(report 499 cutover A — persona first). Until then, a systemd timer or the
`upgrade.sock` already provisioned in every slot (`spirit.nix:68`,
`upgradeSocketPath`) carries the health verdict and rewrites the *runtime*
selector. The rollback intent: **never stop the old slot; the new slot must
earn the connection.**

## Suggestion — the cutover as a typed orchestrator decision, not a Nix edit

Today the cutover is static Nix. The three mechanisms above are the missing
*runtime* layer. The clean end state collapses them into a single persona
Nexus decision:

- The selector stops being `currentDefault` baked into a derivation and
  becomes a `RecordActiveVersion` write into persona's own SEMA — the
  `active_version` value the FD-handoff router (`transport.rs:309`,
  `handoff_one_from_manager_store`) already reads.
- The gate, migration, and health check become the three steps of a persona
  Nexus `PromoteVersion` operation: run gate → if Agree, run migration → flip
  `active_version` → run health check → if Degraded, flip back. Each step is a
  typed `NexusAction`; the recursion (`Continue(NexusWork)`) sequences them
  with no round-trip, exactly the landed Nexus shape.
- No daemon ever stops. The FD-handoff means in-flight clients are routed to
  whichever version `active_version` names *at connect time*; flipping the
  value flips the destination atomically, with zero downtime — the SCM_RIGHTS
  primitive is already built and tested.

The work decomposes cleanly: build the gate binary (independent, testable
now), build the redb-to-sema migration (blocked on pilot sema-engine
adoption), and wire `active_version` from a Nix string into a persona SEMA
value (blocked on persona-as-orchestrator, cutover A).

## Future view — persona-owned atomic FD-handoff, no downtime

One year out, the production cutover is not an event a human performs; it is a
persona Nexus decision the orchestrator makes and can reverse. A new
schema-derived component version is published; persona spawns it in its own
slot with its own `.sema`; the equivalence gate runs automatically and gates
promotion; the redb-to-sema (or sema-version-N to sema-version-N+1) migration
carries state once; persona flips `active_version`; the FD-handoff router
sends every new client connection to the new daemon via SCM_RIGHTS with the old
daemon still warm; the health check watches; a degraded verdict flips
`active_version` back and the next connection lands on the old daemon again —
all with no socket ever closing under a client. The `currentDefault` Nix string
becomes the *initial* value persona reads at boot, not the live selector. The
manual one-line edit shown at the top of this entry is replaced by a typed,
gated, reversible, downtime-free orchestrator operation — the same operation
for spirit's first cutover and for every component cutover after it.

## One-glance cutover flow

```mermaid
flowchart LR
  G[Equivalence gate] -->|agree| M[Migrate state]
  M --> F[Flip active version]
  F --> H[Health check]
  H -->|degraded| R[Flip back]
```
