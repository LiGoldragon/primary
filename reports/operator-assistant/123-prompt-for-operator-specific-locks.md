## 123 — Prompt for operator: use file-specific locks so OA can run a parallel lane

*Operator-assistant note, 2026-05-15. The user (`ligoldragon@gmail.com`)
asked OA to write this for the operator to read; the user will pass it
to operator.*

## TL;DR for operator

Your current `operator.lock` for `primary-a18` ("persona-engine sandbox
two-component harness tests") claims **six whole repository roots**:

```
[primary-a18] # persona-engine sandbox two-component harness tests
/git/github.com/LiGoldragon/persona
/git/github.com/LiGoldragon/persona-message
/git/github.com/LiGoldragon/persona-router
/git/github.com/LiGoldragon/persona-terminal
/git/github.com/LiGoldragon/persona-harness
/git/github.com/LiGoldragon/terminal-cell
```

The orchestrate helper's overlap rule is "nested or equal paths," so any
operator-assistant claim inside any of these six roots is rejected — the
whole persona runtime side is now serialized on one role.

The user wants this to be specific-lock-shaped so operator-assistant can
run a parallel lane on the same bead. Please **release the whole-repo
claims and re-claim only the files you'll actually edit in your current
commit batch**.

## Why this matters

The user has explicitly directed OA to do "elaborate sandbox tests with
midway witnesses and signal-catching negatives" inside the same bead
(`primary-a18`). That work touches the same six repos but **different
files** than what you're focused on for credential/auth/harness wiring:

| OA's planned scope | Operator's likely scope |
|---|---|
| `persona/src/bin/wire_*.rs` (new files) | `persona/src/manager.rs`, `harness.rs`, supervisor wiring |
| `persona/Cargo.toml` `[[bin]]` additions | Same `Cargo.toml` for harness deps |
| `persona/flake.nix` new `wire-*` checks | Same `flake.nix` for harness checks |
| `persona/TESTS.md` additive entries | Same `TESTS.md` for harness entries |

OA's new shim files don't overlap with operator's source-code edits at
all. The three hotspot files (`Cargo.toml`, `flake.nix`, `TESTS.md`) are
additive on both sides, so a short-hold "claim, edit, commit, release"
window handles them cleanly.

## The discipline

**Claim only the paths your current edits will touch. Release as soon as
you commit.** Hotspot files (Cargo.toml, flake.nix, TESTS.md, README.md,
ARCHITECTURE.md) are usually additive — both agents can append/edit
different sections in quick alternation rather than blocking on
whole-repo holds.

For new files, claiming the full path is fine (no conflict possible —
the file doesn't exist on the other agent's branch yet). For existing
shared files, hold them only during the edit-and-commit window.

## Refinement for your current `primary-a18` claim

Here's what your refined claim could look like (replace with whatever
you're actually editing — these are guesses from the bead title and
recent activity):

```sh
tools/orchestrate release operator
tools/orchestrate claim operator '[primary-a18]' \
  /git/github.com/LiGoldragon/persona/src/manager.rs \
  /git/github.com/LiGoldragon/persona/src/manager_store.rs \
  /git/github.com/LiGoldragon/persona/tests/manager.rs \
  /git/github.com/LiGoldragon/persona-harness/src \
  -- "persona-engine sandbox two-component harness tests"
```

If you're editing `Cargo.toml` or `flake.nix` right now, add those
paths to the claim; release them as soon as your commit lands so OA
can take its turn.

## What OA will claim in parallel

OA plans to claim these paths (all in `persona`, no overlap with the
above example):

```sh
tools/orchestrate claim operator-assistant '[primary-a18]' \
  /git/github.com/LiGoldragon/persona/src/bin/wire_emit_message_reply.rs \
  /git/github.com/LiGoldragon/persona/src/bin/wire_decode_message_reply.rs \
  /git/github.com/LiGoldragon/persona/src/bin/wire_router_client.rs \
  /git/github.com/LiGoldragon/persona/src/bin/wire_tap_router.rs \
  /git/github.com/LiGoldragon/persona/src/bin/wire_decode_message.rs \
  -- "elaborate tests: wire-capture witnesses + signal-catching negatives"
```

(The five `wire_*.rs` files include one existing file — `wire_decode_message.rs`
— that needs a `--expect-origin` extension. The other four are new.)

For `Cargo.toml`, `flake.nix`, and `TESTS.md` edits, OA will batch them
into single short-hold claim-edit-commit-release windows and coordinate
with you via lock-file inspection (`cat operator.lock` before claiming a
hotspot file).

## The general principle, for future beads

| Scope shape | When to use |
|---|---|
| Whole-repo path | Only when you're doing a wide sweep across most of the repo and other roles can't safely interleave. |
| Directory path (`/repo/src/`) | When you own a subsystem and an assistant or peer agent should stay out of that subsystem entirely. |
| File path | Default for most edits. Claim the files you'll touch. |
| Glob-style intent (informal, in the `# reason`) | Express what you're doing semantically when the file list would be long; rely on commit logs + reports to communicate finer-grained intent. |

For this workspace specifically: persona's `Cargo.toml`, `flake.nix`,
`TESTS.md`, and per-repo `ARCHITECTURE.md` are hotspots. Short holds on
these are the norm; long holds block parallel work.

## See also

- `protocols/orchestration.md` §"Lock-file format" — describes path
  locks, task locks, and the overlap rule.
- `skills/operator.md` §"Working with operator-assistant" — the
  operator-assistant is "extra capacity, not hidden edits under the
  operator lock"; the user is asking operator-assistant to be that extra
  capacity now.
- `reports/operator-assistant/122-persona-dev-stack-smoke-2026-05-15.md` —
  the predecessor work this builds on.
