# 102 - Situation after MindRoot surface

Role: `operator-assistant`

Purpose: short status after checking new reports, open beads, current locks, and
the work I just landed.

---

## Short read

My situation is good but bounded by current ownership:

- `primary-m8x` is done. `/git/github.com/LiGoldragon/persona-mind` commit
  `cacd8eb5` deletes `MindRuntime`, exposes the direct `ActorRef<MindRoot>`
  surface, updates tests and architecture, and passes `nix flake check -L`.
- The designer wisdom from `reports/designer/108-review-of-operator-assistant-101.md`
  is now in skills. `/home/li/primary` commit `4ad5b70b` updates
  `skills/actor-systems.md`, `skills/architectural-truth-tests.md`, and
  `skills/contract-repo.md`.
- Operator now holds `/git/github.com/LiGoldragon/persona-mind` for a
  daemon-backed mind prototype. I should avoid further `persona-mind` edits
  until that work lands or we coordinate.
- The best next operator-assistant work is therefore outside `persona-mind`:
  `primary-o3m` in `persona-router`, `primary-46j` in `persona-system`, or
  `primary-aww` in `signal`.

## New report

The new report since my last pass is:

- `reports/designer-assistant/12-terminal-cell-owner-spike.md`

The report says the terminal target should be a backend-neutral terminal cell:
a durable PTY owner, append-only transcript, derived screen projection, and
disposable viewers. The prototype in `/git/github.com/LiGoldragon/terminal-cell-lab`
already proves detached replay, programmatic input through the same PTY input
port, and screen projection derived from transcript bytes.

My read: this is important, but it is not my next lane unless asked. It points
toward a later `persona-terminal` split and is currently owned by
designer-assistant/system-specialist lanes.

## Open beads relevant to me

Open operator-assistant beads:

| Bead | Repo | Current read |
|---|---|---|
| `primary-o3m` | `persona-router` | Best next small implementation: add `router_cannot_emit_delivery_before_commit` actor-trace witness. |
| `primary-46j` | `persona-system` | Good next test-backfill: fake Niri event-stream fixture proving push path, no polling snapshots. |
| `primary-aww` | `signal` / `signal-core` | Important but wider: complete kernel extraction and update consumer imports. |
| `primary-3ro` | persona-* | Still valuable, but split it. Avoid the `persona-mind` part while operator owns that repo. |

Related but not cleanly mine:

- `primary-2w6`: P1 persona-message migration off text-files/polling. This is
  larger than a quick witness and should be taken only with a proper claim.

Closed:

- `primary-m8x`: closed with the `persona-mind` commit above.

## Review of my recent work

The work is aligned with the latest skills:

- `MindRuntime` removal matches `skills/actor-systems.md`: runtime roots are
  actors; tests should not keep a non-actor facade alive.
- The direct test fixtures now ask `ActorRef<MindRoot>` through
  `SubmitEnvelope`, which keeps Kameo visible instead of laundering it through
  a wrapper.
- The weird tests caught two useful cleanup edges: dead manifest-message code
  and a public ZST `ReadManifest` marker. Both are gone.
- The skill extraction preserves the durable parts of the designer answer
  without copying the report into the skills.

One workspace hygiene issue remains: `reports/operator-assistant/100-kameo-persona-actor-migration.md`
is still an uncommitted added file in `/home/li/primary`. It looks stale now:
it talks about earlier Kameo migration commits and names such as
`MindRootActor` that have since been corrected. I would retire or rewrite it
rather than commit it as current truth.

## What I can do next

My preferred next move is `primary-o3m`:

- it is outside the operator's current `persona-mind` lock;
- designer already answered that actor trace is the right first witness;
- it exercises the new `skills/architectural-truth-tests.md` rule directly;
- the expected change is bounded to `persona-router` tests and maybe trace
  fixtures.

Second choice is `primary-46j` in `persona-system`, because it is also a
bounded witness and aligns with push-not-poll.

Third choice is `primary-aww`, because it is important but broader. It may
force a consumer import cascade across the `signal-*` family.

## What I would like to know

1. Should I retire/rewrite the stale uncommitted
   `reports/operator-assistant/100-kameo-persona-actor-migration.md`, or leave
   it untouched for now?

2. Should my next bead be the small router witness (`primary-o3m`), or do you
   want me to prioritize `primary-46j` / `primary-aww` despite the larger
   surface?

3. Should operator-assistant stay out of the terminal-cell lane until
   system-specialist/designer-assistant finish the split decision?
