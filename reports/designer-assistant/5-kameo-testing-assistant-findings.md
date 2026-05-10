# 5 - Kameo testing assistant findings

*Designer-assistant report. This supplements the designer-owned Kameo
skill work. I did not edit `skills/autonomous-agent.md`, did not write
`skills/kameo.md`, and did not touch the designer-owned
`kameo-testing` repository.*

---

## 0. Test Surface

I created and pushed a separate public repository:

- `/git/github.com/LiGoldragon/kameo-testing-assistant`
- `https://github.com/LiGoldragon/kameo-testing-assistant`
- latest tested commit: `a0fd6f25`

Verification passed:

```sh
nix develop -c cargo fmt
nix develop -c cargo test
nix develop -c cargo clippy --all-targets -- -D warnings
nix flake check -L
```

The repo currently has **15 passing Kameo tests**.

| Test file | What it probes |
|---|---|
| `tests/data_bearing_patterns.rs` | actor-as-state, `Args = Self`, prepared actors, typed handles, `Recipient`, `ReplyRecipient`, delegated replies |
| `tests/creative_state_models.rs` | one actor type with many equipment/state variations, `Context::forward` routing |
| `tests/failure_and_mailbox.rs` | bounded mailbox backpressure, transient restart, restart-from-args state reset, default link-death fatality |
| `tests/lifecycle_registry_and_threads.rs` | startup failure, `on_panic` recovery, `on_link_died` survival, local registry, `spawn_in_thread` runtime requirement |

---

## 1. Adoption And Stability Signal

As of 2026-05-10, Kameo looks active and growing, not yet boring or
deeply mature.

Crates.io reports:

- crate created: 2024-03-29;
- latest/default/max stable version: `0.20.0`;
- latest publish: 2026-04-07;
- 33 published versions;
- 247,952 total downloads;
- 109,144 recent downloads;
- 20 crates.io reverse dependencies.

GitHub reports:

- `tqwewe/kameo`;
- 1,296 stars;
- 69 forks;
- last pushed: 2026-04-27;
- 9 open issues;
- not archived.

GitHub code search found 79 public repositories with a `Cargo.toml`
match for Kameo. That is not proof of production use, but it is enough
to reject the "unused toy" framing.

Public production-shaped users I found:

- `CapSoftware/Cap` uses `kameo = "0.17.2"` in `crates/recording`.
  Cap describes itself as the open source Loom alternative, has public
  desktop/web releases, and had release `cap-v0.4.84` on 2026-04-15.
- `ethui/ethui` uses workspace Kameo in `crates/types`. Ethui describes
  itself as an Ethereum toolkit, publishes releases, and had release
  `v1.27.0` on 2026-01-29.
- `volga-project/volga` uses `kameo = "0.16.0"`. Volga describes itself
  as real-time data processing / feature engineering for AI and ML
  systems.
- `microsoft/dactor` publishes `dactor-kameo`, a Kameo adapter for its
  distributed actor framework. This is low-adoption today, but it is a
  useful signal that Kameo is being treated as an integration target.

My read: Kameo is not Ractor-scale established infrastructure yet. It is
pre-1.0, moving fast, and made a toolchain jump to Rust `1.88.0` in the
0.19/0.20 line. That means we should expect API churn and pin versions
intentionally. But the project is active, the download curve is real, and
there are credible public application repos using it.

---

## 2. Main Fit

Kameo fits the workspace's actor philosophy well.

The biggest win is not syntax. It is that the actor noun carries the
actor body:

```rust
struct MemoryLedgerActor {
    actor_name: String,
    opened_items: Vec<String>,
    notes: Vec<String>,
    mutation_count: usize,
}
```

The implementation then says:

```rust
impl Actor for MemoryLedgerActor {
    type Args = Self;
    type Error = Infallible;

    async fn on_start(state: Self::Args, _: ActorRef<Self>) -> Result<Self, Self::Error> {
        Ok(state)
    }
}
```

That shape is exactly what the no-ZST actor rule wants. The type that
receives messages is the type that owns the mutable data.

The hunter experiment makes the point more vividly:

- one `HunterActor` type;
- different carried `Camouflage`;
- different `HuntingTool`;
- different ammunition, material, and age;
- behavior changes by actor state, not by inventing more actor marker
  types.

This is the clean answer to "a hunter has a bow, arrows, clothes, and
equipment." In Kameo, those are fields on the actor.

---

## 3. Useful Patterns

### Local Handles

A repo-local handle around `ActorRef<MyActor>` works cleanly:

```rust
struct LedgerHandle {
    actor_reference: ActorRef<MemoryLedgerActor>,
}
```

That is not an actor abstraction layer. It is a consumer surface for one
repo's actor. This should be the default public shape for Persona
components: public handles hide runtime mechanics, while implementation
code still uses direct Kameo.

### Recipient Types

`Recipient<M>` and `ReplyRecipient<M, Ok, Error>` are useful when a
caller should know only one message capability, not the whole actor type.
They let us narrow a surface without inventing a wrapper trait.

### PreparedActor

`PreparedActor` is excellent for tests:

- create mailbox and `ActorRef`;
- enqueue messages before the actor runs;
- run the actor in the test task;
- get the final actor value and `ActorStopReason` back.

This is the best Kameo-native test shape I found for state assertions.

### Context::forward

`Context::forward` lets a dispatch actor route a message to a child and
preserve the reply path. This maps naturally to Persona's ingress →
dispatch → domain actor shape and avoids a separate routing abstraction.

### DelegatedReply

`Context::spawn` with `DelegatedReply<T>` keeps the actor mailbox
available while a reply is completed elsewhere. This is useful for waits
that should not pin the actor handler.

But it is not supervised actor work. Kameo's docs say the detached task's
errors do not call the actor's `on_panic`. Use it for small reply
delegation, not as the default answer to long work.

---

## 4. Kinks

### Toolchain

Kameo 0.20.0 declares:

```toml
edition = "2024"
rust-version = "1.88.0"
```

That is a real workspace consequence. Existing Persona crates pinned at
Rust `1.85` need a toolchain bump before a Kameo switch lands.

### Restart Reconstructs State

Kameo's actor value is the mutable state, but a supervised restart does
not preserve the crashed in-memory state. It reconstructs from the spawn
arguments or the `supervise_with` factory.

The test mutates a worker from `10` to `12`, crashes it, and verifies the
restarted actor reads `10` again.

Design implication: any actor that must survive restart needs durable
state or an explicit reconstruction source. Kameo makes restart policy
easy to express; it does not make restart semantics automatically safe.

### Default Link Death Is Fatal

A linked actor stops when its link dies abnormally unless
`on_link_died` overrides the behavior. This is good for fail-fast
supervision, but too strong for observational links.

Skill rule should distinguish:

- supervision links: death should usually propagate;
- observational links: override `on_link_died` and record the event.

### spawn_in_thread Needs Multi-Thread Tokio

`spawn_in_thread` panics under Tokio's default single-thread test runtime.
The passing test needs:

```rust
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
```

Blocking-plane actors can use `spawn_in_thread`, but the host runtime must
be multi-threaded.

### Registry Is Global

The local registry works:

- `register(name)` succeeds once;
- duplicate registration returns an error;
- shutdown unregisters the actor.

But it is global. Parallel tests should use unique names, usually derived
from `ActorId`, and production topology should not depend on registry
names when owned `ActorRef` fields are available.

### on_panic Can Continue

`on_panic` gets `&mut self`, so an actor can record panic state and return
`ControlFlow::Continue(())`. The test proves the actor remains alive after
a handler panic.

This is powerful and dangerous. It should be used only when the actor's
state is still known-good after the panic. Default stop/restart remains
the safer policy.

### Nix Source Filtering

One repo-local packaging kink appeared: `craneLib.cleanCargoSource` did
not include a README used by `include_str!("../README.md")`. The fix was
to keep crate docs in `src/lib.rs`. This is not a Kameo issue, but it is
worth remembering for new experiment repos.

---

## 5. Skill Guidance To Steal

Recommended Kameo skill rules:

1. Use direct Kameo, not a wrapper actor trait.
2. Make runtime actor types data-bearing structs.
3. Prefer `type Args = Self` for simple actors; use a separate `Args`
   only when startup input is not the actor body.
4. Put public consumer APIs in repo-local handle types.
5. Use `Recipient` / `ReplyRecipient` to narrow capability surfaces.
6. Use `PreparedActor` for actor tests that need final state.
7. Use `watch` or `oneshot` channels as test witnesses instead of sleep
   loops.
8. Treat restart as reconstruction, not memory preservation.
9. Give each child an explicit `RestartPolicy`.
10. Use `Context::forward` for dispatch actors.
11. Use `DelegatedReply` sparingly; prefer supervised actors for real
    long work.
12. Use `spawn_in_thread` only under a multi-thread Tokio runtime.
13. Keep registry use narrow; prefer owned `ActorRef` fields for topology.
14. Override `on_link_died` only when link death is observational.
15. Before switching a crate to Kameo 0.20, bump Rust to `1.88.0`.

---

## 6. Sources Checked

- Kameo crate metadata: `https://crates.io/api/v1/crates/kameo`
- Kameo reverse dependencies: `https://crates.io/api/v1/crates/kameo/reverse_dependencies`
- Kameo repository metadata: `https://api.github.com/repos/tqwewe/kameo`
- Kameo docs: `https://docs.page/tqwewe/kameo`
- Kameo API docs: `https://docs.rs/kameo/latest/kameo/`
- Cap repository: `https://github.com/CapSoftware/Cap`
- Ethui repository: `https://github.com/ethui/ethui`
- Volga repository: `https://github.com/volga-project/volga`
- Dactor repository: `https://github.com/microsoft/dactor`

---

## 7. Bottom Line

Kameo passed the shape test.

It makes the beautiful path the normal path: actors carry their state,
handlers mutate `&mut self`, replies are typed per message, and dispatch
can forward without a custom runtime layer.

The main hazards are not blockers. They are design rules:

- restart reconstructs from args/factory;
- default link death propagates;
- detached delegated work is not supervised actor work;
- `spawn_in_thread` needs multi-thread Tokio;
- Rust `1.88.0` is required.

Those belong in the designer's Kameo skill.

---

## Sources

- `/git/github.com/LiGoldragon/kameo-testing-assistant`
- `https://github.com/LiGoldragon/kameo-testing-assistant`
- `https://docs.rs/kameo/latest/kameo/actor/trait.Actor.html`
- `https://docs.rs/kameo/latest/kameo/message/trait.Message.html`
- `https://docs.rs/kameo/latest/kameo/actor/trait.Spawn.html`
- `https://docs.rs/kameo/latest/kameo/supervision/index.html`
