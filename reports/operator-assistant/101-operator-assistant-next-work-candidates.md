# 101 - Operator-assistant next work candidates

Role: `operator-assistant`

Purpose: handoff to designer after a hunt across recent reports, active
beads, contract repos, Persona runtime repos, and Nix-backed testing
surfaces.

---

## Short answer

I found two categories of useful work.

First, there are ready operator-assistant implementation slices that
follow directly from recent designer/operator decisions:

1. Apply the data-type-shadowing actor rule across persona-*.
2. Remove or redesign `MindRuntime` as a non-actor runtime facade.
3. Add missing architectural-truth witnesses around commit-before-delivery,
   no-polling, and durable terminal/PTY state.
4. Continue normalizing contract-crate Nix check surfaces.

Second, there are design-dependent items that should not be grabbed by
operator-assistant until designer decides the shape:

1. The `signal` vs `signal-core` kernel overlap.
2. Whether `signal-persona-message` should own text projection tests or
   narrow its architecture wording.
3. The Nexus body shape for terminal/harness delivery contracts.
4. The post-commit subscription contract for `signal-persona-mind`, which
   should wait for durable `mind.redb` and the committed event model.

During the hunt I already landed two safe fixes:

| Repo | Commit | What |
|---|---|---|
| `/git/github.com/LiGoldragon/persona-mind` | `769649c8` | `IngressSupervisor`, `DispatchSupervisor`, `DomainSupervisor`, and `ViewSupervisor` renamed to `*Phase`; topology, traces, manifest, and architecture updated. |
| `/git/github.com/LiGoldragon/signal-persona` | `dfad8b48` | Flake upgraded to named build/test/doc/fmt/clippy checks; `test-frame` and `test-version` exposed; lint priority fixed after Clippy surfaced it. |

Both repos pass `nix flake check`.

---

## What the recent pattern looks like

Recent operator/designer work has converged on a consistent loop:

1. Architecture names constraints.
2. Constraints become witness tests.
3. Long-lived runtime concerns become direct Kameo actors.
4. Nix is the test entry point, not an afterthought.
5. Contract crates stay payload-only; runtime crates own behavior.

The high-signal work is therefore not "add more code". It is:

- remove actor-shaped wrappers that do not own real actor responsibilities;
- add witnesses that prove the intended path was used;
- make Nix expose every relevant test surface;
- stop contract crates from claiming behavior or text syntax they do not own.

---

## Ready implementation candidates

### 1. Data-type-shadowing rule across persona-*

Current bead: `primary-3ro`

This is ready operator-assistant work. The design rule is settled in
`skills/actor-systems.md`: if an actor wraps exactly one data type and
only forwards to that type's methods, the data type is probably the actor.

Known cases from the bead:

| Repo/path | Current shape | Likely change |
|---|---|---|
| `/git/github.com/LiGoldragon/persona-mind/src/actors/store.rs` | `StoreSupervisor` wraps `MemoryState` | Collapse to `impl Actor for MemoryState`, preserving trace/write witnesses. |
| `/git/github.com/LiGoldragon/persona-message/src/actors/ledger.rs` | `Ledger` wraps `MessageStore` | Collapse to `impl Actor for MessageStore`. |
| `/git/github.com/LiGoldragon/persona-system/src/niri_focus.rs` | `NiriFocus` wraps `FocusTracker` | Collapse to `impl Actor for FocusTracker`. |
| `/git/github.com/LiGoldragon/persona-mind/src/actors/config.rs` | `Config` only has dead-code store-location read | Delete unless designer wants a real config actor. |
| `/git/github.com/LiGoldragon/persona-wezterm/src/terminal.rs` | `TerminalDelivery` is not spawned in production | Delete unless a consumer is added. |

Designer decision needed before implementation:

- The bead says counter-only state policy was still being clarified in
  `skills/actor-systems.md`. If designer has now settled the counter-only
  carve-out, operator-assistant can implement this in repo-sized chunks.

Recommended execution:

1. Do `persona-message` and `persona-system` first. They are narrower.
2. Do `persona-mind` `StoreSupervisor` after designer confirms how to treat
   counters and after reviewing `primary-m8x`.
3. Delete `TerminalDelivery` only after a quick consumer scan confirms no
   new spawn path appeared after the last report.

### 2. `MindRuntime` public facade cleanup

Current bead visible in status: `primary-m8x`

The title says: "delete MindRuntime; expose ActorRef<MindRoot> as
persona-mind public surface."

Evidence:

- `persona-mind` architecture says the production shape is daemon-owned
  `MindRoot` plus thin CLI clients.
- `skills/actor-systems.md` says runtime roots are actors and a struct that
  merely owns `ActorRef<_>` values is a hidden non-actor owner.
- `persona-mind/src/service.rs` still exposes `MindRuntime` as a facade
  around `ActorRef<MindRoot>`.

This is probably ready, but I would ask designer to order it relative to
durable store work. If tests currently use `MindRuntime` heavily, deleting
it may be a larger cascade than the name suggests.

Suggested acceptance:

- public tests talk to `ActorRef<MindRoot>` or a clearly justified domain
  facade;
- no `MindRuntime` convenience owner remains;
- topology tests still prove the root actor owns child lifecycle;
- `nix flake check` passes.

### 3. `persona-router` commit-before-delivery witness

No current lock seen.

Evidence from survey:

- `/git/github.com/LiGoldragon/persona-router/ARCHITECTURE.md` claims
  commit-before-emit / commit-before-delivery ordering.
- The missing witness is a test that proves delivery cannot be emitted before
  durable commit.

Likely test:

- `router_cannot_emit_delivery_before_commit`

Nix surface:

- Ideally `nix run .#test-router-commit-before-delivery` if it needs a
  stateful transcript/store artifact.
- If it can be pure actor-trace only, expose it through `nix flake check`.

Why high signal:

- It is exactly the new `skills/testing.md` + `skills/architectural-truth-tests.md`
  pattern: split visible delivery from the commit witness so an in-memory
  shortcut cannot pass.

Designer input:

- Decide whether the first witness should be pure actor trace or stateful
  artifact chain. I lean stateful if router durable state is already real;
  otherwise actor trace is the correct first witness.

### 4. `persona-message` tail polling removal

Current open bead: `primary-2w6`

Evidence from survey:

- `/git/github.com/LiGoldragon/persona-message/src/store.rs` has a `Tail`
  loop with sleep/poll behavior.
- Workspace `skills/push-not-pull.md` forbids polling.
- `persona-message` is transitional and already has several Nix test apps.

Likely tests:

- `message_tail_cannot_poll_message_log`
- `message_tail_receives_pushed_ledger_event`

Nix surface:

- Pure source/architecture guard in `nix flake check` for "no sleep/polling
  tail".
- Later stateful `nix run .#test-tail-push` when router-owned Sema state is
  available.

Designer input:

- This likely belongs inside the larger `primary-2w6` migration rather than
  as a separate cleanup, because the replacement is router-owned Sema state.

### 5. `persona-system` push witness for Niri focus

No current lock seen.

Evidence from survey:

- `persona-system` architecture says system observations are pushed.
- Implementation reads `niri event-stream`.
- We should prove subscription events enter through the `NiriFocus` mailbox
  and do not fall back to snapshot polling.

Likely test:

- `niri_subscription_cannot_poll_focus_snapshots`

Nix surface:

- `nix flake check` with a fake event-stream fixture; no live Niri should be
  required.

Designer input:

- Probably low design risk. This is a strong operator-assistant test-backfill
  candidate after `primary-3ro`.

### 6. `persona-harness` terminal delivery sleep

No current lock seen.

Evidence from survey:

- `persona-harness` architecture has a pushed-observation invariant.
- `/git/github.com/LiGoldragon/persona-harness/src/terminal.rs` waits a fixed
  one second before capture.
- Its flake check shape appears weaker than the newer contract/runtime repos.

Likely test:

- `harness_terminal_delivery_cannot_sleep_before_capture`

Nix surface:

- First step: make `nix flake check` run real tests if it does not.
- Later: `nix run .#test-terminal-delivery-witness` with transcript/capture
  artifacts.

Designer input:

- This may overlap system-specialist terminal work. Designer should decide
  whether `persona-harness` or the emerging terminal component owns the first
  capture witness.

### 7. `persona-wezterm` durable PTY witness

No current lock seen.

Evidence from survey:

- Reports now say the repo is really evolving toward a durable terminal/PTy
  component, not only WezTerm.
- `/git/github.com/LiGoldragon/persona-wezterm/src/pty.rs` has PTY/session
  machinery and some sleep/polling points.
- Architecture claims terminal durability and viewer detachment.

Likely tests:

- `wezterm_pty_survives_viewer_close`
- `wezterm_resize_is_event_driven`

Nix surface:

- `nix run .#test-pty-survives-viewer-close`, emitting socket/transcript
  artifacts.

Designer input:

- Name/ownership question first: if the repo is becoming `persona-terminal`,
  decide whether to write tests before or after rename/split.

---

## Contract repo candidates

### 1. `signal-persona` check surface - landed

Survey initially said `nix flake check` only built the package. The old
`buildRustPackage` check did run Cargo's `checkPhase`, so it did execute the
existing tests. The real gap was that the flake exposed only one conflated
`checks.default` and lacked the named check surface used by the newer
contract crates.

Landed in `/git/github.com/LiGoldragon/signal-persona` commit `dfad8b48`:

- Crane/Fenix flake layout.
- named `build`, `test`, `test-frame`, `test-version`, `test-doc`, `doc`,
  `fmt`, and `clippy` checks.
- lint priority fix required by newer Clippy.

This is the pattern I can repeat for older contract repos if any remain.

### 2. `signal` vs `signal-core` kernel overlap

No current lock seen.

Evidence from contract survey:

- `/git/github.com/LiGoldragon/signal/ARCHITECTURE.md` says `signal-core`
  owns the frame/kernel.
- `/git/github.com/LiGoldragon/signal/src/frame.rs`,
  `/git/github.com/LiGoldragon/signal/src/request.rs`, and
  `/git/github.com/LiGoldragon/signal/src/reply.rs` still declare local
  frame/request/reply shapes.
- `reports/designer/107-contract-enum-naming-pass-mind.md` flags this as
  architectural ambiguity.

This needs designer direction before implementation.

Options:

1. Collapse `signal` to aliases/payloads over `signal-core`.
2. Document a deliberate exception: `signal` is a higher-level vocabulary
   with local request/reply wrappers.
3. Add a source/dependency witness that prevents kernel drift, whatever
   shape designer chooses.

I should not pick option 1 or 2 as operator-assistant without a designer
decision.

### 3. `signal-persona-message` text round-trip wording

No current lock seen.

Evidence from contract survey:

- `signal-persona-message/ARCHITECTURE.md` says the contract covers
  `text -> typed -> frame`.
- Existing tests construct typed `MessageRequest` / `MessageReply` directly
  and round-trip frames.
- Human-facing NOTA belongs in boundary crates, not contract crates.

Designer question:

- Should the architecture be narrowed to typed frame round trips, or should
  the text projection witness be placed in `persona-message`?

My recommendation:

- Narrow the contract repo wording.
- Put the NOTA text witness in `persona-message`, because CLI syntax is a
  boundary behavior.

### 4. `signal-persona-harness` body type

No current lock seen, but design-dependent.

Evidence from contract survey:

- `signal-persona-harness` still has an opaque `MessageBody(String)` for
  terminal delivery.
- Architecture wants typed Nexus-in-NOTA body eventually.

Designer question:

- Is the body shape ready, or should this stay provisional until Nexus body
  record shape is settled?

My recommendation:

- Do not change this until Nexus body shape is settled. Once settled, this is
  a clean contract + consumer migration.

### 5. `signal-persona-mind` subscriptions

Design-dependent and blocked by runtime foundation.

Evidence:

- `signal-persona-mind/src/lib.rs` says subscription mode is future.
- `reports/designer-assistant/9-persona-mind-implementation-pins-prepass.md`
  says subscription contract should wait for durable `mind.redb`,
  `EventSeq`, and post-commit append.

Recommendation:

- Do not start with the contract. First land durable mind store and event
  append. Then add subscription request/reply/event types plus no-polling
  witnesses.

---

## Testing architecture candidates

These are especially aligned with the new `skills/testing.md`.

| Repo | Constraint | Test name | Nix shape |
|---|---|---|---|
| `persona-mind` | durable store survives restart and is not in-memory | `mind_store_survives_process_restart` | chained artifact test: writer emits `mind.redb`, reader/restart consumes it |
| `persona-mind` | CLI accepts one NOTA record and talks Signal to daemon | `mind_cli_accepts_one_nota_record_and_prints_one_nota_reply` | stateful `nix run .#test-mind-cli-daemon-boundary` |
| `persona-mind` | role claims stop being unsupported and append activity after commit | `role_claim_reaches_claim_flow`, `claim_commit_appends_activity` | pure actor path first, chained store artifact later |
| `persona-router` | visible delivery cannot happen before commit | `router_cannot_emit_delivery_before_commit` | actor trace now; stateful store/transcript artifact later |
| `persona-message` | tail cannot poll old message log | `message_tail_cannot_poll_message_log` | pure source guard now; push-stateful app later |
| `persona-system` | Niri focus events are pushed through mailbox | `niri_subscription_cannot_poll_focus_snapshots` | pure fake event-stream fixture |
| `persona-harness` | capture cannot depend on fixed sleep | `harness_terminal_delivery_cannot_sleep_before_capture` | source/actor guard now; terminal artifact later |
| `persona-wezterm` | PTY survives viewer close | `wezterm_pty_survives_viewer_close` | stateful Nix app with socket/transcript artifacts |

Best next unblocked test candidate:

- `persona-router` `router_cannot_emit_delivery_before_commit`.

Best overall strategic test:

- `persona-mind` `mind_store_survives_process_restart`, once durable store
  foundation exists.

---

## Suggested ordering

If designer agrees, I would take work in this order:

1. `primary-3ro`: data-type-shadowing pass, starting with the smaller
   `persona-message` and `persona-system` collapses.
2. `primary-m8x`: `MindRuntime` deletion only after confirming the public
   surface cascade.
3. `persona-router`: commit-before-delivery witness.
4. `persona-system`: pushed Niri focus witness.
5. `persona-message`: tail polling removal inside or after `primary-2w6`.
6. `signal` kernel rationalization after designer chooses the direction.
7. Terminal/harness stateful Nix witnesses after designer/system-specialist
   settle whether the durable component remains `persona-wezterm` or becomes
   `persona-terminal`.

---

## Decision points for designer

1. For `primary-3ro`, is counter-only state enough to keep a wrapper actor,
   or should counters be folded into the data-bearing actor / deleted unless
   they are a tested domain witness?

2. Should `MindRuntime` be deleted before durable store work, or should it
   survive briefly as a test facade until the daemon boundary exists?

3. Should `persona-router` commit-before-delivery be proven first by actor
   trace, or should we wait until a stateful Nix artifact can prove the store
   write across process boundaries?

4. Should `signal` collapse to `signal-core` types, or is it intentionally a
   higher-level vocabulary layer with local frame/request/reply wrappers?

5. Should `signal-persona-message` narrow its architecture wording away from
   text projection, leaving NOTA text tests to `persona-message`?

6. Should terminal durability tests land in `persona-wezterm` now, or wait
   for a rename/split to `persona-terminal`?

