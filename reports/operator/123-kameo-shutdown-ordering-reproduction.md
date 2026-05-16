# 123 — Kameo shutdown-ordering reproduction

Date: 2026-05-16
Role: operator
Scope: recover the lost operator-assistant report, isolate the Kameo
shutdown-ordering issue in a dedicated repo, and state the implementation
consequence for Persona.

## 1. Recovery

The "lost" report was real. It lived on side change
`lsuzwnyvovps / c29cbae9309c` as:

`reports/operator-assistant/139-kameo-spawn-in-thread-supervised-shutdown-bug-2026-05-16.md`

The current main line had the broader summaries:

- `reports/operator-assistant/138-persona-mind-gap-close-2026-05-16.md`
- `reports/operator-assistant/140-phase3-actor-supervision-audit-2026-05-16.md`

but not the focused bug report. I restored the exact focused report
under its original path and pushed it in primary commit `399683f3`.
That leaves two operator-assistant reports numbered 139. I left the
duplicate number intact because the recovery goal was preserving the
side-commit artifact, not rewriting OA history.

## 2. Reproduction repo

Repository:

`/git/github.com/LiGoldragon/kameo-supervised-shutdown-repro`

Remote:

`https://github.com/LiGoldragon/kameo-supervised-shutdown-repro`

Commit:

`063e3ccf reproduce kameo shutdown ordering`

The repo pins Kameo `0.20.0`, uses a tiny state-bearing actor, and
exposes both Cargo and Nix entry points. The Nix witness is:

```sh
nix --option max-jobs 1 --option cores 1 --option builders '' run .#test-shutdown-order
```

The pure flake check also passes:

```sh
nix --option max-jobs 1 --option cores 1 --option builders '' flake check -L
```

Both commands ran successfully. The four Rust witnesses all pass.

## 3. The witness shape

The actor owns a `std::net::TcpListener`. That listener is the resource
witness: while the actor is alive, a second bind to the same address
must fail; after the actor drops, rebinding must succeed.

Core actor shape:

```rust
pub struct ResourceActor {
    listener: TcpListener,
    stop_delay: Duration,
    lifecycle: LifecycleWitness,
}
```

The actor deliberately delays inside `on_stop`:

```rust
async fn on_stop(
    &mut self,
    _actor_reference: WeakActorRef<Self>,
    _reason: ActorStopReason,
) -> Result<(), Self::Error> {
    tokio::time::sleep(self.stop_delay).await;
    if let Some(sender) = self.lifecycle.stop_sender.take() {
        let _ = sender.send(());
    }
    Ok(())
}
```

`Drop` sends a second witness signal. This separates three moments:

1. `wait_for_shutdown()` returns;
2. `on_stop` completes;
3. `Self` drops and the listener is released.

## 4. What reproduced

The original OA finding is correct in its important operational
consequence: **Kameo can report shutdown before a state-bearing actor
has released its resources.**

The reproduction sharpened it:

| Witness | Result |
|---|---|
| `threaded_actor_wait_for_shutdown_returns_before_on_stop_completes` | `spawn_in_thread` `wait_for_shutdown()` returns before `on_stop` finishes. |
| `threaded_actor_wait_for_shutdown_returns_before_socket_is_released` | after `spawn_in_thread` `wait_for_shutdown()`, the actor still holds the TCP listener. |
| `threaded_actor_wait_for_shutdown_result_waits_for_on_stop` | `wait_for_shutdown_result()` waits for `on_stop`. |
| `tokio_actor_wait_for_shutdown_also_returns_before_on_stop_completes` | plain `.spawn()` has the same `wait_for_shutdown()` semantic. |

That last row matters. The bug is not only "supervised
`spawn_in_thread`". The more precise statement is:

> Kameo `ActorRef::wait_for_shutdown()` waits for mailbox closure, not
> for `on_stop` completion or actor state drop. `spawn_in_thread`
> makes the bug more dangerous because the actor state is released on a
> dedicated OS thread, but the early observation point exists in the
> regular Tokio-task spawn path too.

## 5. Upstream source read

Kameo 0.20's own docs say `wait_for_shutdown()` waits until the actor
has stopped and describes this as useful when cleanup must finish first.
The implementation does this instead:

```rust
pub async fn wait_for_shutdown(&self) {
    self.mailbox_sender.closed().await
}
```

The actor lifecycle closes/notifies links before `on_stop`:

```rust
actor_ref
    .links
    .lock()
    .await
    .notify_links(id, reason.clone(), mailbox_rx);

log_actor_stop_reason(id, name, &reason);
let on_stop_res = actor.on_stop(actor_ref.clone(), reason.clone()).await;
```

Only after `on_stop` does Kameo set `shutdown_result`, which is why
`wait_for_shutdown_result()` is a stronger API:

```rust
self.mailbox_sender.closed().await;
match self.shutdown_result.wait().await {
    Ok(reason) => Ok(reason.clone()),
    ...
}
```

`spawn_in_thread` runs the actor lifecycle through a thread using the
current Tokio runtime handle:

```rust
std::thread::Builder::new()
    .name(A::name().to_string())
    .spawn({
        let actor_ref = self.actor_ref.clone();
        move || handle.block_on(CURRENT_ACTOR_ID.scope(actor_ref.id(), self.run(args)))
    })
    .unwrap()
```

So the implementation evidence matches the reproduction: mailbox
closure is the early signal; hook completion is later; actor drop is
later still.

## 6. Implementation consequence

For Persona and other state-bearing components:

- Do not use `wait_for_shutdown()` as a resource-release witness.
- Do not use child-link "closed" observation as proof that the child
  has released redb databases, sockets, file locks, or PTYs.
- Use `wait_for_shutdown_result()` when the contract only needs
  `on_stop` completion.
- If resource release matters, release the resource inside `on_stop`
  through an explicit `Option<T>::take()` or implement an actor-owned
  close-then-confirm message and wait for that reply before restart.
- For `spawn_in_thread`, treat a post-drop hook or join-aware actor
  handle as the proper upstream fix. Without that, restart code must
  not race on `wait_for_shutdown()`.

The current workspace warning in `skills/kameo.md` is directionally
right but slightly too narrow. It should be sharpened from "supervised
`spawn_in_thread` releases before drop" to:

> `wait_for_shutdown()` and link-notification closure are mailbox
> closure observations. They are not lifecycle-completion or
> resource-release observations. The bug is most dangerous with
> supervised `spawn_in_thread`, but the early observation point exists
> for ordinary `.spawn()` too.

I have not edited the skill yet because the user asked first for
reproduction and research. That skill edit is the next clean change.

## 7. Sources

- Kameo ActorRef docs:
  `https://docs.rs/kameo/latest/kameo/actor/struct.ActorRef.html`
- Kameo 0.20 `actor_ref.rs` source:
  `https://docs.rs/crate/kameo/latest/source/src/actor/actor_ref.rs`
- Kameo 0.20 `spawn.rs` source:
  `https://docs.rs/crate/kameo/latest/source/src/actor/spawn.rs`
- Reproduction repo:
  `https://github.com/LiGoldragon/kameo-supervised-shutdown-repro`
