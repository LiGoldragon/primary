# 79.1 — The terminal-layer decomposition

Variant: Psyche. Source-grounded via workflow `w2qcp5qxh`. Answers: who owns the terminal
control/session surface, given terminal-cell is an abduco wrapper process (`bcca`) and
orchestrate does instance management.

## Resolved by psyche (2026-06-06)

The Option-D decomposition below is **adopted**; the two open calls are settled (Spirit
`ckhx`, `5fd6`):

- **Name = `terminal-control`** (the psyche's choice — supersedes the `termctl`
  recommendation written below). Contracts: **`signal-terminal-control`** (working) +
  **`meta-signal-terminal-control`** (policy, born meta-signal per `hnpo`).
  `signal-orchestrate` `DownstreamComponent::Terminal` → **`TerminalControl`**.
  `terminal-cell` unchanged.
- **Cell fork = systemd, logged in sema.** The cell must **survive a `terminal-control`
  restart**, so it is NOT a child of terminal-control — it is forked as a **systemd-managed
  process**, and each instance is **durably logged in sema**. On restart, terminal-control
  rediscovers the still-running cells from sema and **reattaches** to their control/data
  sockets. This realizes abduco's survive-detach property through **systemd as the OS
  process supervisor** + **sema as the durable instance registry**. It refines `bcca`:
  orchestrate owns lifecycle *policy/orders*, **systemd** owns OS process supervision +
  restart-survival, **terminal-control** owns the durable sema record used to reattach. The
  systemd unit wiring is system-operator deploy work.

Everything else in the report (not-harness, not-orchestrate, the responsibility map, the
cell absorbing the gate-writer + matcher) stands as adopted. Where the text below says
`termctl`/`signal-termctl`/`owner-signal-termctl`, read `terminal-control`/
`signal-terminal-control`/`meta-signal-terminal-control`.

## The answer

**Keep a dedicated session-control component — but rename it and trim it.** Don't fold it
into harness; don't dissolve it into orchestrate. The source resolves your uncertainty
more cleanly than the question implied: the surface is **generic** (any program), the
residue is **real and homeless elsewhere**, and the trim costs **near-zero working code**
because the colliding pieces are unbuilt. Recommended shape (Option D):

```
router → agent → harness ──(client: supplies AI prompt patterns, drives delivery)──┐
                                                                                     ▼
orchestrate ──(issues create/retire/launch ORDERS, tracks instances)──►  [ session-control daemon ]
   (lifecycle policy, never forks)                                         registry + signal control
                                                                          plane + per-session pattern
                                                                          registry + session Sema
                                                                                     │ drives
                                                                                     ▼
                                                                          terminal-cell (library)
                                                                          fork + PTY + transcript +
                                                                          input-gate WRITER + matcher
```

## Why not the other two options

- **Fold into harness — REJECTED (fatal coverage gap).** A terminal-cell wraps **any**
  program — a shell, an editor, a build — not only an AI harness. harness models *only* AI
  harnesses (closed `HarnessKind {Codex,Claude,Pi,Fixture}`; intent forbids a generic
  variant), and in source it is a *client* of terminal (`HarnessTerminalEndpoint::PtySocket`),
  not its owner — its INTENT/ARCHITECTURE explicitly **disclaim** terminal transport. Folding
  the surface into harness would leave every non-harness terminal **ownerless**. And harness
  is being subsumed from above by the new `agent` front door — exactly the wrong moment to
  hand it a cross-cutting plane.
- **Dissolve into orchestrate — REJECTED (category error).** orchestrate's identity
  vocabulary is roles/lanes/scopes (coordination identity), and it **explicitly disclaims
  terminal byte paths** (`orchestrate/ARCHITECTURE.md §6`). Folding a name→socket registry +
  a byte/control relay into a coordination-state engine conflates coordination identity with
  delivery identity and makes orchestrate forward `Input`/`Resize`/`Capture` frames — a
  category mismatch. (orchestrate has **zero** process machinery today — no spawn/PID/argv/
  kill; its only `spawn` is `thread::spawn` for its own listeners.)

So exactly one cohesive home remains for the residue: a dedicated, **program-agnostic**
session-control component.

## Responsibility map — each duty to its best owner

| Responsibility | Today | Best owner | Why |
|---|---|---|---|
| Session naming + durable registry (`TerminalName → sockets/state`); List/Resolve | terminal | **session-control daemon** | Generic, opaque name; cell refuses Sema; orchestrate disclaims; every caller (harness, agent, viewer, CLI) hits it — the load-bearing residue |
| Create / Retire of the logical session | terminal (stub `NotBuiltYet`) | **orchestrate ISSUES the order; session-control RECORDS; cell FORKS** | Resolves the `bcca` collision by altitude; nothing built is lost |
| `signal-terminal` control-plane relay (Connect/Input/Resize/Detach/Capture) | terminal | **session-control daemon** | Generic byte/control relay; inseparable from the registry (resolve-then-forward) |
| Input-gate leasing + injection policy | DUPLICATED: terminal **and** terminal-cell | **terminal-cell library** (matcher/writer) surfaced via the daemon's signal plane | Must live next to the single PTY writer = the cell; collapse the duplication downward |
| Prompt-pattern lifecycle | DUPLICATED: terminal **and** terminal-cell | **matcher → cell; registry → daemon; meaning → harness/agent** | Three altitudes: match-a-suffix (cell), durable pattern registry (daemon), what-clean-means (AI policy) |
| Viewer-adapter launch policy | terminal (claimed, **unimplemented vapor**) | **orchestrate** (launch as an instance order) + cell exposes the attach point | Launching a viewer process is instance lifecycle (`bcca`); don't leave a vapor claim in the daemon |
| Durable session metadata + observation Sema (6 tables + worker-lifecycle stream) | terminal | **session-control daemon** | Generic per-session durable truth; cell refuses Sema; not orchestrate's coordination state |
| PTY fork + child group + transcript + one-viewer raw pump | terminal-cell | **terminal-cell (unchanged)** | The abduco primitive; not a triad component (`bcca`) |

## Naming — the ambiguity you flagged

Post the `persona-terminal → terminal` rename there are three `terminal-*` repos at three
layers (`terminal-cell` primitive, `signal-terminal` contract, `terminal` daemon) and the
bare word names none of their distinct jobs. The daemon's actual job is *named-session
registry + control plane + injection/pattern registry* — a control-plane noun.

**Recommendation: rename the daemon `termctl`** (terminal control plane) — short, clearly
the controller above the cell, reads cleanly in the triad. Contract repos rename in
lockstep, and — applying the `MetaSignal`-canonical decision (`hnpo`, OwnerSignal
deprecated) — the policy contract is **`meta-signal-termctl`**, not `owner-signal-termctl`:

- daemon: `terminal` → **`termctl`**
- working contract: `signal-terminal` → **`signal-termctl`**
- policy contract: `owner-signal-terminal` → **`meta-signal-termctl`** (born meta-signal)
- `signal-orchestrate` `DownstreamComponent::Terminal` → **`TerminalControl`**
- **keep `terminal-cell`** as-is (unambiguously the primitive) and keep the data type names
  (`TerminalName`/`TerminalSession`/…) — they describe sessions generically.

Strong alternative: `terminal-session` (most literal, but longer three-word contract
names). Reject `session` (collides with agent/harness session vocabulary).

## How orchestrate manages cell instances (the order plane)

orchestrate is a policy/order plane, **never** a forker (zero process machinery in source):

- **Spawn:** orchestrate decides when/whether a cell exists (capacity, scheduling, drain)
  and emits a meta-Mutate **CreateCell** order carrying the launch params
  (`TerminalCommand{executable,arguments,environment,working_directory}`, target session)
  toward `DownstreamComponent::TerminalControl` (the enum slot already exists as `Terminal`).
  `termctl` receives it, allocates `control.sock`/`data.sock`, writes the session row, and
  performs (or delegates to a program-agnostic process executor) the actual
  `terminal-cell::spawn_session`. **Routing the fork through harness is a category mismatch**
  (AI-only) — the spawner must be program-agnostic.
- **Track:** orchestrate records the cell in one **generic wrapped-program instance table**
  (the "missing" `agent_runs`/`spawn_plans` slot in its ARCHITECTURE §5, generalized beyond
  AI runs). PID/socket/transcript truth lives downstream (termctl/cell), not in
  orchestrate.redb — orchestrate tracks lifecycle *state* and order outcome.
- **Retire:** a meta-Retract **RetireCell** order (drain: stop new viewers, let the child
  exit); termctl removes the row and the cell tears down its child + PTY; orchestrate marks
  it retired. (Mirrors orchestrate's existing "retire = delete a record," extended to a
  remote process via an order.)

This resolves the `bcca` collision by altitude: **orchestrate orders, termctl records, the
cell forks.** `owner-signal`/`meta-signal-termctl`'s `CreateSession`/`RetireSession` (today
`NotBuiltYet`) become the orders termctl *executes on receipt*, not ops a client calls.

## Net: do you want the component? Yes — here's what it is

A thin, program-agnostic **`termctl`** daemon: the durable name→socket registry, the
`signal-termctl` control-plane relay, the per-session prompt-pattern registry, and the
session observation Sema. It is a coherent **delivery-identity** boundary — distinct from
orchestrate's coordination identity, from harness's AI-only meaning, and from the cell's
per-app mechanics. It IS a triad component (it gains the engine it never had — `bcca`'s
"predates the engine" applied to the *cell*, but `termctl` is the genuine triad daemon the
layer was missing). The change is mostly a **rename + reassigning unbuilt responsibilities**
(create/retire are stubs, viewer-launch is vapor) — near-zero working code lost.

## Residual decisions for the psyche

1. **Naming — RESOLVED:** `terminal-control` + `signal-terminal-control` +
   `meta-signal-terminal-control` + `DownstreamComponent::TerminalControl` (`ckhx`).
2. **Who forks the cell — RESOLVED:** **systemd** forks the cell so it survives a
   terminal-control restart, and the instance is logged in **sema** for reattach (`5fd6`).
   Not a child of terminal-control. systemd unit wiring is system-operator work.
3. **Instance table shape:** one generic wrapped-program instance table (covers AI runs +
   plain shell/editor/build cells), or separate `agent_runs` + `terminal_cell_instances`?
   *(Recommend one generic table.)*
4. **Injection/prompt collapse direction:** confirm gate-writer + matcher collapse **down**
   into terminal-cell (next to the writer/transcript), termctl owning only the pattern
   registry. *(Recommend collapse-down.)*
5. **Sequencing vs agent/harness:** termctl is below the agent/harness layer and
   program-agnostic, so the agent decision doesn't gate it — ship termctl independently.
   *(Recommend proceed.)*
6. **Viewer-launch:** confirm it moves OUT of the daemon's intent to an orchestrate
   instance order (or a human-run abduco-style CLI), termctl/cell owning only the attach point.
7. **Stale-rename cleanup (mechanical, same pass):** `terminal/INTENT.md` still says
   `persona-harness`; `harness/src/terminal.rs` still imports crate `persona_terminal` — fix
   to post-rename names.

## See also
- `0-frame-and-method.md` — the question + method.
- Spirit `bcca` (abduco cell + orchestrate instance management), `hnpo` (meta-signal canonical).
- `reports/system-designer/78-...` — the carve-out study (now corrected: terminal-cell is a
  library/binary, not a triad daemon; this report places the actual triad daemon = `termctl`).
