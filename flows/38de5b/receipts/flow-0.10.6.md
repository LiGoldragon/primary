# Flow 0.10.6 — 38de5b, 2026-09-25

Subflow of 38de5b (Opus). This patch followed the live bind (`receipts/flow-bind-live.md`): Flow 0.10.5 resolved every bound Codex flow's Herdr route as `Unavailable`. Nothing was reactivated, and the unit and the pin were not touched. Reactivating is b7da5d's decision.

## Notice
`FLOW_ID=38de5b hm-send b7da5d '…one more Flow patch…'` returned `Transported.{ b7da5d done }`.

## Witness: Herdr 0.8.2 `--session messaging-build api snapshot`, live
- **Codex panes at rest report `agent_status` `done`:** 26c50c, f5a74e, a676b3, b7da5d, e71dab, 98eb43, 504461 and 5f38bc.
  - Of these, 26c50c, b7da5d, e71dab and 5f38bc have **no `interactive_ready` key**.
  - The rest report `true`.
- **00f95a** is `working` with no key.
- **Claude panes:**
  - `idle` or `working` with `interactive_ready: true`: d8df70, e51411, 38de5b.
  - `done`, with the flag or without it: 88475f, 9c7514.
  - `working` with no key: b87854.
- No pane in the snapshot reported `interactive_ready: false`.

## Rule (0.10.6)
A binding matches an agent when its name, pane, terminal and harness match, as before. Given a match:
- **Routable** (`snapshot_has_route`): `agent_status` is `idle`, `done` or `working`.
- **Presentable** (`snapshot_has_idle_route`, for a Send that waits for its marker): `agent_status` is `idle` or `done`.
- **`interactive_ready`**, for both of the above: when Herdr leaves the flag out or sets it to null, it does not block. `true` is accepted. Any other value refuses.
- **Still `Unavailable`:** a missing agent, and any other status, such as `waiting`.
- **Unchanged:** the launch-time readiness checks in `herdr/launch.rs`, which are for new panes.

One case changed that no Codex fixture covers: a Claude pane that is `idle` and has no flag was refused in 0.10.5 and is now routable. The existing fixture was changed from "idle, no flag" to "idle, `interactive_ready: false`" so that it still witnesses a refusal. This follows the brief's rule that the flag is required only when Herdr reports it.

## Repo `LiGoldragon/flow`
- **Base:** 5e1382f (0.10.5), cloned fresh into a scratch dir under Orchestrate lock 6577. The lock was released.
- **a1a5175:** the fix in `crates/flow-nexus/src/herdr.rs`, a new helper `agent_readiness_permits_prompt`, the version bump in `Cargo.toml` and `Cargo.lock`, and an `UPGRADES.md` entry.
- **5b59761:** `flake.nix` package version 0.10.6. This is the current `main`, and `git ls-remote` shows it on the remote.
- **New fixtures:**
  - A done Codex pane with no flag is Available, both routable and presentable.
  - A done Codex pane with a reported flag follows the flag.
  - A missing Codex agent is Unavailable, whether the roster holds another agent or is empty.
  - A working pane is routable but not presentable.
  - The Claude idle-ready snapshot is unchanged.
- **Checks:**
  - `cargo test`: 105 passed before and 110 after, none failed.
  - `cargo clippy --all-targets -- -D warnings` is clean, and `cargo fmt --check` is clean.
  - `nix build --option builders '' --option substituters https://cache.nixos.org --option max-jobs auto` at 5b59761 gave `/nix/store/gi42aic5s1kw8papfaais61lqwaw41by-flow-0.10.6`, which holds `flow`, `flow-meta` and `flow-nexus`.
