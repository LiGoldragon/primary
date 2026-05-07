# Rust documentation audit — what's there, what's missing, what to lift

Date: 2026-05-07
Author: Claude (designer)

The user asked: reinforce the Rust programming discipline; the
ractor doc might be thin; check old workspace versions for
anything we don't have. This report answers all three.

---

## TL;DR

**Rust discipline (`skills/rust-discipline.md`) is solid.** The
audit on the persona scaffold and the persona-message scaffold
both used it cleanly to identify naming and shape issues. No
strengthening needed *to the discipline itself*. What's missing
is breadth on a few neighboring topics (async patterns,
default-derives, generics) — discussed in §5 below; minor.

**The ractor doc (`lore/rust/ractor.md`, 239 lines) is
comprehensive on the patterns currently practiced**, distilled
from criome's working daemon. A wide search found **four
small additions worth lifting** from live repos (criome, hexis):

1. ZST actor + `*Handle` wrapper that owns the spawn result.
2. Sync-façade-on-State paired with the actor for direct
   testing — full working example.
3. Concrete `handle_supervisor_evt` override for accept-loops.
4. `pre_start` pool initialization (open store, read count,
   spawn N).

**Five other ractor patterns are not documented because they
are not yet practiced** in live code: registry / named-actor
lookup, actor-group pubsub (`pg` module), hot-reload with
state preservation, bridging sync threads, error propagation
through `pre_start` panics. These are *gaps in practice*, not
gaps in documentation. Surfacing them so the boundary is
explicit.

**The archives (`/home/li/git-archive/criome-rt`, `criome-rt`,
`criome-stored`, `criome-store-contract`, `Mentci-v0/v1`,
`mentci-fractal`, `aski-rs`) had no ractor patterns to lift.**
Most pre-date the ractor adoption or are non-actor systems.
Skip them for migration.

---

## 1. Audit scope

Searched:

- **Live repos**: criome (canonical actor source), hexis
  (Reconciler/Supervisor pair), forge + arca (skeleton-only,
  no actor code yet).
- **Archive candidates**: criome-rt, criome-stored,
  criome-store-contract, Mentci-v0/v1, mentci-fractal,
  mentci-archive, aski-rs.
- **Current docs**: `lore/rust/ractor.md`,
  `lore/rust/style.md`, `lore/rust/rkyv.md`,
  `lore/rust/nix-packaging.md`,
  `~/primary/skills/rust-discipline.md`.

Search method: subagent comb-through targeting actor patterns
(ractor / Actor::spawn / RpcReplyPort / pre_start / post_start
/ post_stop / supervisor / pg / registry), tests, and
documentation files.

---

## 2. Current state of Rust documentation

```
lore/rust/
├── style.md           749 lines · toolchain reference + discipline
│                      (the discipline content overlaps with
│                       skills/rust-discipline.md; trim still pending)
├── ractor.md          239 lines · actor framework usage
├── rkyv.md            141 lines · binary serialization
└── nix-packaging.md   214 lines · crane + fenix flake layout

~/primary/skills/
└── rust-discipline.md ~600 lines · the discipline (methods on
                       types, domain newtypes, error enums, no anyhow,
                       ractor-as-default, naming, tests-in-separate-files)
```

Coverage today:

| Topic | Where | Notes |
|---|---|---|
| Methods on types | rust-discipline | full |
| Domain newtypes | rust-discipline | full |
| Error enums (thiserror) | rust-discipline | full |
| One object in / out | rust-discipline | full |
| Naming | skills/naming + rust-discipline | full |
| Cargo.toml shape | lore/rust/style | reference |
| Cross-crate deps | lore/rust/style | reference |
| Pin strategy | lore/rust/style | reference |
| Module layout | both | OK |
| Tests in separate files | rust-discipline | full |
| Crane + fenix | lore/rust/nix-packaging | full |
| rkyv usage | lore/rust/rkyv | full |
| Ractor four-piece | lore/rust/ractor | full |
| Ractor messages | lore/rust/ractor | full |
| Ractor supervision | lore/rust/ractor | partial — see §3.3 |
| Ractor mailbox | lore/rust/ractor | full |
| Ractor pools | lore/rust/ractor | partial — see §3.4 |
| Ractor sync façade | lore/rust/ractor | mentioned, no example |
| Ractor daemon entry | lore/rust/ractor | full |
| Ractor registry / pg | nowhere | not practiced — see §4 |
| Ractor testing | nowhere | partial — see §3.2 |

---

## 3. Four ractor.md additions worth lifting

Each is a small extension to a section that already exists in
`lore/rust/ractor.md`. The substance is taken from live code
in `criome/src/` and `hexis/src/` where the patterns are
running today. None proposes new architecture.

### 3.1 ZST actor + `*Handle` wrapper

The four-piece (`Actor`, `State`, `Arguments`, `Message`) is
documented. What isn't named: the **`*Handle` companion** that
holds the spawn result (`ActorRef + JoinHandle`) and exposes a
`start(Arguments)` constructor. It's the consumer surface for
the actor.

From `hexis/src/supervisor.rs` lines 117–149:

```rust
pub struct SupervisorHandle {
    actor_ref: ActorRef<supervisor::Message>,
    join_handle: tokio::task::JoinHandle<()>,
}

impl SupervisorHandle {
    pub async fn start(arguments: supervisor::Arguments)
        -> Result<Self>
    {
        let (actor_ref, join_handle) = Actor::spawn(
            Some("supervisor".to_string()),
            supervisor::Supervisor,
            arguments,
        )
        .await
        .map_err(|error| Error::ActorSpawn(error.to_string()))?;

        Ok(Self { actor_ref, join_handle })
    }

    pub fn actor_ref(&self) -> &ActorRef<supervisor::Message> {
        &self.actor_ref
    }

    pub async fn wait(self) -> std::result::Result<(), tokio::task::JoinError> {
        self.join_handle.await
    }
}
```

**Why lift it**: the lore doc shows `Daemon::start` returning
the `(ActorRef, JoinHandle)` tuple but doesn't name the
`*Handle` pattern. This makes the pattern teachable —
"every spawned actor has a `*Handle` that owns its
spawn result; consumers of the actor reach for `*Handle`,
never bare `Actor::spawn`."

**Where it goes**: a new short subsection in
`lore/rust/ractor.md` after "Daemon entry point", named
"Handle wrappers".

### 3.2 Sync façade + direct-state testing

The lore doc says: *"When the crate ships a one-shot CLI
binary or wants tests without a tokio runtime, expose the
dispatch as inherent methods on `State`."* No example.

From `hexis/src/reconciler.rs` + `hexis/tests/reconciler.rs`:

```rust
// reconciler.rs — the actor side
async fn handle(&self, _myself: ActorRef<Self::Msg>, message: Message,
                state: &mut State)
    -> std::result::Result<(), ActorProcessingErr>
{
    match message {
        Message::Run => {
            let _ = state.apply();
        }
    }
    Ok(())
}

// State has the real method:
impl State {
    pub fn apply(&mut self) -> Result<(), Error> {
        let result = self.apply_inner();
        self.phase = match &result {
            Ok(()) => Phase::Settled,
            Err(_) => Phase::Failed,
        };
        result
    }

    fn apply_inner(&mut self) -> Result<(), Error> { … }
}
```

```rust
// tests/reconciler.rs — direct, no tokio runtime
struct Fixture { arguments: reconciler::Arguments }

impl Fixture {
    fn apply(&self) -> Result<(), hexis_cli::Error> {
        State::new(self.arguments.clone()).apply()
    }
}

#[test]
fn applies_a_proposal_to_a_target_file() {
    let fixture = Fixture { arguments: … };
    fixture.apply().unwrap();
    // assert the side effect on disk
}
```

**Why lift it**: shows the discipline as a complete pattern.
The actor's `handle` is a thin shell around `state.apply()`;
the real logic is in `State`, which is sync, total, and
testable directly. Tests don't need a tokio runtime, an
ActorRef, or a mock supervisor.

**Where it goes**: replace the current "Sync façade" paragraph
in `lore/rust/ractor.md` with this concrete example.

### 3.3 Concrete `handle_supervisor_evt` override

The lore doc says (line 137): *"Wrong for the per-connection-
spawning Listener — override to log and continue:"* and then
shows a hand-typed snippet. Live code in `criome/src/listener.rs`
lines 89–99 has the working version that's slightly cleaner
and includes the actor name in the error:

```rust
async fn handle_supervisor_evt(
    &self,
    _myself: ActorRef<Self::Msg>,
    event: SupervisionEvent,
    _state: &mut State,
) -> std::result::Result<(), ActorProcessingErr> {
    if let SupervisionEvent::ActorFailed(actor, reason) = event {
        let label = actor
            .get_name()
            .unwrap_or_else(|| format!("{:?}", actor.get_id()));
        eprintln!("criome-daemon: connection {label} failed: {reason}");
    }
    Ok(())
}
```

**Why lift it**: the `actor.get_name()` extraction is a small
but useful trick. Drop-in replacement.

**Where it goes**: replace the existing snippet in the
"Supervision" section.

### 3.4 `pre_start` pool initialization

The lore doc shows worker pools as `Vec<ActorRef<…>> +
Arc<AtomicUsize>` cursor (line 194-205). What's not shown:
how to *populate* the pool at boot.

From `criome/src/daemon.rs` lines 45–86:

```rust
async fn pre_start(
    &self,
    _myself: ActorRef<Self::Msg>,
    arguments: Arguments,
) -> std::result::Result<Self::State, ActorProcessingErr> {
    // open the resource the pool will share
    let sema = Arc::new(Sema::open(&arguments.sema_path)?);
    let reader_count = sema.config().reader_count();

    // spawn the engine (1, exclusive writer)
    let (engine, _engine_handle) = Actor::spawn_linked(
        Some("engine".into()),
        engine::Engine,
        engine::Arguments { sema: Arc::clone(&sema) },
        _myself.get_cell(),
    ).await?;

    // spawn N readers
    let mut readers = Vec::with_capacity(reader_count);
    for index in 0..reader_count {
        let (reader, _handle) = Actor::spawn_linked(
            Some(format!("reader-{index}")),
            reader::Reader,
            reader::Arguments { sema: Arc::clone(&sema) },
            _myself.get_cell(),
        ).await?;
        readers.push(reader);
    }

    // spawn the listener that hands out reader refs to connections
    let reader_cursor = Arc::new(AtomicUsize::new(0));
    let (_listener, _) = Actor::spawn_linked(
        Some("listener".into()),
        listener::Listener,
        listener::Arguments {
            socket_path: arguments.socket_path,
            engine: engine.clone(),
            readers: readers.clone(),
            reader_cursor: Arc::clone(&reader_cursor),
        },
        _myself.get_cell(),
    ).await?;

    Ok(State { sema, engine, readers, reader_cursor })
}
```

**Why lift it**: shows the *full daemon-bootstrap pattern* —
open shared resource, derive count from it, spawn singletons
and the pool together, return State that carries everything
the rest of the system needs. The lore doc has the worker-pool
*shape* but not the bootstrap.

**Where it goes**: a new subsection in `lore/rust/ractor.md`
after "Worker pools", named "Pool initialization in
`pre_start`".

---

## 4. Five gaps (not documented because not yet practiced)

These are patterns the lore doc and the live code both lack.
Documenting them would be premature; flagging them so the
boundary of "what's actually known" is explicit. When one
becomes load-bearing in real code, the doc grows then.

| Gap | What's missing | When it'll matter |
|---|---|---|
| **Actor registry** | `ractor::registry` for named-actor lookup. Today every actor is passed by parent via `ActorRef`. | When a daemon needs cross-tree lookup ("ask the registry for the engine, not my parent for it"). |
| **Actor groups / `pg`** | `pg::join` / `pg::cast` for fan-out subscribe + broadcast. Today subscriptions are hand-wired. | When the persona reducer's subscription hub lands and needs efficient many-subscriber dispatch. |
| **Hot-reload with state preservation** | Restart an actor without losing State. ractor doesn't support directly; pattern would involve serialising State to disk + replaying log. | When the workspace wants live config reload without dropping in-flight work. |
| **Bridging sync threads** | `std::thread::spawn` ↔ ractor actor. Today everything is pure-async. | When integrating non-async libraries (e.g. blocking FFI, blocking compute). |
| **`pre_start` panics** | Lore says they bubble as `SpawnErr` but no example of handling that in calling code. | First time a `pre_start` panics in production. |

If any becomes load-bearing soon, write the section then.
Don't pre-write speculatively.

---

## 5. Reinforcement to `rust-discipline` itself

The skill is solid; two minor topics could land later as the
codebase has working examples to draw from:

- **Default `#[derive(...)]` set.** The discipline doesn't say
  what to derive by default. Looking at criome / hexis /
  persona-message: `#[derive(Debug, Clone, PartialEq, Eq)]`
  for records; `#[derive(Debug, Clone, Copy, PartialEq, Eq)]`
  for closed enums. Plus `Hash` when used as map key, `Ord +
  PartialOrd` when used in BTreeMap key positions, `NotaRecord`
  / `NotaEnum` / `NotaTransparent` for wire records. Worth a
  short table.
- **Generics / type parameters.** Discipline says the standard
  carve-out (T, U, V) but doesn't extend to "use `$Value` /
  `$Output` / `$Failure` style names when the parameter has
  semantic content." This was strong in aski's design and
  worth carrying forward when generic-heavy code lands.
- **Async patterns**. The discipline says "ractor is the
  default for any service with concurrent state; plain sync is
  fine for one-shot CLIs." That's enough for now. A deeper
  treatment of `async fn` hygiene, `Send` bounds, `Pin`,
  cancellation safety can wait for code that demands it.

Don't edit the skill yet. Note these as expansion candidates;
land when the practice supports them.

---

## 6. Recommendations

**Do now (4 small lifts to `lore/rust/ractor.md`):**

| # | Title | Source | Effect |
|---|---|---|---|
| 3.1 | `*Handle` wrapper pattern | hexis | Names the consumer-side surface |
| 3.2 | Sync façade with full test example | hexis | Replaces vague mention with code |
| 3.3 | Concrete `handle_supervisor_evt` with `get_name()` | criome | Drop-in replacement, slightly nicer |
| 3.4 | `pre_start` pool initialization | criome | Completes the worker-pool teaching |

Net: ractor.md grows by ~80 lines. Existing structure stays.
Each section already exists; these are *fills*, not new
sections, except 3.4 which is a new subsection under "Worker
pools".

**Defer:**

- The five gaps in §4. Wait until practice exists.
- The three rust-discipline expansions in §5. Wait until
  pattern density supports them.

**Skip entirely:**

- Archive contents. Pre-rewrite implementations are not
  authoritative; live code is.

---

## 7. Open questions for the user

1. **Want me to do the four ractor.md additions in this
   session?** They're surgical and concrete. The operator is
   currently focused on persona-message; the lore work is
   parallelisable from my side.
2. **The `*Handle` pattern** — it has a name in the lore doc
   already (mentioned implicitly in "Daemon entry point" for
   `Daemon::start` returning the spawn result). Should we
   formalize as `*Handle` or keep loose? I'd lean
   formalize: `EngineHandle`, `SupervisorHandle`,
   `ReaderHandle` — every actor's consumer surface.
3. **Cross-cutting question**: do we want a separate
   `lore/rust/testing.md` for testing patterns (sync façade
   tests, integration tests, the `tempfile` pattern, the
   `cargo_test` flake-check pattern)? Today testing is split
   between rust-discipline.md and rust/style.md. A focused
   testing reference would absorb both. Worth a separate
   conversation.
4. **The five gaps in §4** — does any of them feel like a
   near-term need (e.g. is the persona daemon planning to
   need actor registry or pg-pubsub)? If yes, lifting now (vs
   waiting for first use) becomes worth the effort.
5. **Old aski docs** — `aski/spec/design.md` (read in an
   earlier session) had rich language-design substance with
   relevance to the persona/nota typed-records direction.
   Should I mine it for any patterns that should land in the
   workspace's docs (likely as a *language-design* skill), or
   leave aski as the historical record it currently is?

---

## See also

- `lore/rust/ractor.md` — current canonical ractor doc.
- `~/primary/skills/rust-discipline.md` — the discipline.
- `criome/src/daemon.rs`, `criome/src/listener.rs`,
  `criome/src/connection.rs` — live actor patterns the lore
  was distilled from.
- `hexis/src/supervisor.rs`, `hexis/src/reconciler.rs`,
  `hexis/tests/reconciler.rs` — the *Handle and sync-façade
  patterns this report proposes lifting.
- `~/primary/reports/designer/2026-05-06-persona-audit.md` —
  earlier audit using the rust-discipline skill on real code.
