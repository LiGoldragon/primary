# 113 — Actor blocking-handler audit (post-Kameo migration)

*Designer report. Audit of actor handlers in components touched during
the 2026-05-10 Kameo migration wave. Looks for blocking work inside
`async fn handle()` per the discipline in `~/primary/skills/actor-systems.md:177-202`
and `~/primary/skills/kameo.md:837-841`. Read-only audit — no code
changes. Sourced from four parallel sub-agent sweeps (one timed out;
that territory audited directly afterward).*

---

## 0 · TL;DR

| Repo | Status | Notes |
|---|---|---|
| **persona-mind** | clean (1 borderline) | `StoreSupervisor::on_start` opens redb itself instead of asking `StoreKernel` — runs at spawn only |
| **persona-router** | clean-by-design | `HarnessDelivery` is the textbook blocking-plane template (`spawn_blocking` + `context.spawn` + `DelegatedReply`) |
| **persona-harness** | clean | all handlers are pure state mutations / reads |
| **persona-message** | clean-by-design | `Ledger` actor IS the named writer mailbox; sync `std::fs` writes are clean-by-design at today's payload size; flag for `spawn_blocking` upgrade if writes grow |
| **persona-system** | clean | sync niri-CLI driver lives outside any handler |
| **persona-wezterm** | **1 violation** | `TerminalDelivery::handle(DeliverTerminalPrompt)` runs `Command::output()` × 2 + `thread::sleep(500ms)` inline |
| **chroma** | clean | every handler non-blocking; `StateStore` runs on a dedicated OS thread; `ConfigWatcher` owns notify; theme appliers use `tokio::process` + bounded `timeout` |
| **terminal-cell** | clean (architectural-issue tracked elsewhere) | actor handlers clean; daemon-loop `block_on` calls live in a sync `spawn_blocking` driver, not in handlers; broader relay shape rejected by DA/13 (separate concern) |

**One hard violation. One borderline. Two clean-by-design patterns worth canonizing.**

---

## 1 · The one violation — `persona-wezterm::TerminalDelivery`

**File:** `/git/github.com/LiGoldragon/persona-wezterm/src/terminal.rs:150-157`

```rust
impl Message<DeliverTerminalPrompt> for TerminalDelivery {
    async fn handle(&mut self, message: DeliverTerminalPrompt, _ctx: …) -> … {
        self.backend.pane(message.pane_id).deliver(&message.prompt)
        // expands to:
        //   self.send_text(prompt)?;          -> Command::new("wezterm").output()  (sync)
        //   thread::sleep(Duration::from_millis(500));
        //   self.send_enter()?;               -> Command::new("wezterm").output()  (sync)
    }
}
```

Three forbidden patterns in one handler, on the same Tokio worker:

1. **`Command::output()` × 2** — synchronous blocking process execution
2. **`std::thread::sleep(500ms)`** — blocks the mailbox for half a second per delivery
3. No `spawn_blocking`, no `DelegatedReply` — `?` propagates inline

`TerminalDelivery` is not declared as a dedicated blocking plane in the
ARCH. It's a one-shot wrapper that was migrated to Kameo by adding
`impl Message<>` over an existing sync helper without the matching
detach pattern.

**Suggested fix (mechanical, ~10 lines):** mirror
`persona-router::HarnessDelivery`'s template — `tokio::task::spawn_blocking(...)`
inside `context.spawn(async move { ... })`, return
`DelegatedReply<Result<DeliveryReceipt>>`. Or — cleaner if the
`wezterm cli` invocations don't take long — replace `Command::output()`
with `tokio::process::Command::output().await` and `thread::sleep` with
`tokio::time::sleep(...).await`, making the whole handler properly
async without a detach.

---

## 2 · The one borderline — `persona-mind::StoreSupervisor::on_start`

**File:** `/git/github.com/LiGoldragon/persona-mind/src/actors/store/mod.rs:173`

```rust
async fn on_start(arguments: Self::Args, _ref: ActorRef<Self>)
    -> Result<Self, Self::Error>
{
    let graph = MindTables::open(&arguments.store)?.memory_graph()?;
    …
}
```

Pattern: synchronous redb open + read inside the supervisor's
`on_start`, **outside** the kernel boundary. ARCHITECTURE.md §4 says
"`StoreKernel` is the only long-lived store actor that owns the
`MindTables` handle"; this opens a second handle to bootstrap.

**Verdict: borderline.** `on_start` runs once during spawn, not in a
hot handler — no mailbox-starvation risk in steady state. The harm is
architectural, not runtime: duplicates the redb-owner invariant.

**Suggested fix:** spawn `StoreKernel` first, then
`kernel.ask(LoadBootstrapGraph)` and pass the resulting `MemoryGraph`
into `MemoryStore::Arguments`. Removes the duplicate `MindTables::open`
and keeps the redb-owner invariant tight. Not urgent.

---

## 3 · Clean-by-design patterns worth canonizing

These three actors get the discipline right and should be referenced
when designing new blocking planes:

### 3.1 — `persona-router::HarnessDelivery` (template)

**File:** `/git/github.com/LiGoldragon/persona-router/src/harness_delivery.rs:88-120`

The reference shape for "actor whose job IS blocking work":

```rust
impl Message<DeliverToHarness> for HarnessDelivery {
    type Reply = DelegatedReply<…>;

    async fn handle(&mut self, msg: …, context: &mut Context<…>) -> Self::Reply {
        let (delegated, sender) = context.reply_sender();
        context.spawn(async move {
            let result = tokio::task::spawn_blocking(move || {
                HarnessDelivery::deliver(…)  // sync work
            }).await;
            if let Some(sender) = sender { sender.send(result); }
        });
        delegated
    }
}
```

The handler returns *immediately* (`delegated` is returned synchronously);
the blocking work runs on a Tokio blocking thread; the reply is sent
back when it finishes. The mailbox doesn't stall.

ARCH §1 explicitly names `HarnessDelivery` as "the dedicated blocking
plane." Pattern + ARCH-naming is the discipline complete.

### 3.2 — `chroma::StateStore` (dedicated OS thread)

**File:** `/git/github.com/LiGoldragon/chroma/src/state.rs:61`

```rust
fn spawn_in_thread(store: StateStore) -> ActorRef<StateStore> {
    // spawn on a dedicated OS thread, NOT a Tokio worker
}
```

Synchronous redb (`begin_write`, `commit`, `begin_read`) on an actor
that runs on a dedicated thread, off the Tokio worker pool entirely.
For state-bearing components with frequent sync DB calls, this is
arguably *cleaner* than `spawn_blocking` per call — one thread, one
mailbox, one writer.

### 3.3 — `chroma` theme appliers (`tokio::process` + `timeout`)

**File:** `/git/github.com/LiGoldragon/chroma/src/theme.rs:493-510`

```rust
tokio::time::timeout(Duration::from_secs(1), async {
    let mut child = tokio::process::Command::new(…)
        .kill_on_drop(true)
        .spawn()?;
    child.wait().await
}).await
```

When the blocking work IS async-capable (process exec via
`tokio::process`), wrap it in `timeout` with `kill_on_drop`. Bounded,
cancellable, non-blocking. This is the right shape when porting away
from `std::process::Command::output()`.

---

## 4 · Two notes on terminal-cell

The actor (`TerminalCell` in `session.rs`) is **clean**. All handlers
are in-memory state mutations / projections, or use `DelegatedReply`
for waiters (`WaitForTranscriptText`, `WaitForTerminalExit`).

`terminal-cell-daemon.rs` uses `runtime.block_on(self.terminal.ask(...))`
several times (lines 308, 316, 331, 339, 347), but this is a **sync
daemon driver** wrapped in `tokio::task::spawn_blocking` at the
top-level (line 96). The sync driver bridges to the async actor via
`block_on` — that's the textbook sync↔async bridge, not a
blocking-handler violation.

DA/13 (`reports/designer-assistant/13-terminal-cell-relay-architecture-failure.md`)
already rejected this relay architecture on different grounds (live
human use). Whatever replaces it should keep the actor clean and pick
a different bridge shape (raw byte pump + transcript side channel per
DA/13).

---

## 5 · What this audit didn't cover

- **kameo-testing**: not in scope (test scaffolding, not production
  actors).
- **persona-sema**: retired (no live code).
- **signal-* contract crates**: type-only crates, no actors.
- **CriomOS / nix modules**: no Rust actor code.
- **`Arc<Mutex<…>>` shared-state usage in non-actor sites**: a few
  exist (e.g., `persona-wezterm/src/pty.rs` driver threads) — outside
  the audit's scope (not actor handlers), but worth a separate sweep
  per `actor-systems.md:206-` ("No shared locks").

---

## 6 · Recommendations

1. **File a bead** to fix `persona-wezterm::TerminalDelivery`. Small
   mechanical change; either pattern (`HarnessDelivery` template, or
   port to `tokio::process` + `tokio::time::sleep`) works. Suggested
   role label: `role:operator-assistant`. Priority P2 (works today
   under low load; mailbox starvation appears at scale).
2. **Optionally file a bead** to tighten
   `persona-mind::StoreSupervisor::on_start` (route bootstrap through
   `StoreKernel`). Low priority; architectural-hygiene only.
3. **Consider documenting** the three clean-by-design patterns
   (§3.1–3.3) in `~/primary/skills/kameo.md` or
   `~/primary/skills/actor-systems.md` as the canonical "named
   blocking plane" templates. Currently the discipline says "use a
   dedicated actor" but doesn't show the three concrete shapes side
   by side.

---

## See Also

- `~/primary/skills/actor-systems.md` §"No blocking" (L177-202)
- `~/primary/skills/kameo.md` §"Operating notes" (L837-841)
- `~/primary/reports/designer-assistant/13-terminal-cell-relay-architecture-failure.md`
