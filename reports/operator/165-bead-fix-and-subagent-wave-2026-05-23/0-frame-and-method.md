# 165 — Bead dependency repair and authorized subagent wave — frame

*Kind: Meta-report frame · Topic: /310 bead repair + implementation fanout · Date: 2026-05-23 · Lane: operator*

## Psyche instruction

Psyche: "fix the beads - then work the ones that you can with subagents".

Captured in Spirit as record 361 (`operator`, Decision, Maximum): fix the `/310` bead dependency graph first, then use subagents for work that can proceed safely.

## Parent method

1. Claimed the operator lane for the `/310` dependency repair and the first safe implementation roots.
2. Repaired the inverted BEADS dependencies for the golden-ratio chain, pre-typed-frame/tap chain, and persona-agent epic.
3. Verified `bd dep cycles` reports no dependency cycles and `bd ready` now surfaces the true roots: `primary-li0p`, `primary-2cjv`, `primary-gvgj.1`, and `primary-gvgj.2`.
4. Subagent fanout is limited to non-overlapping or carefully scoped work. No child may launch its own subagents. Every child is briefed on headless `jj` usage.

## Dependency repair performed

Golden-ratio chain now reads:

- `primary-li0p` root.
- `primary-v5n2` depends on `primary-li0p`.
- `primary-avog` depends on `primary-li0p`.
- `primary-muu2` depends on `primary-v5n2` and `primary-avog`.
- `primary-g21y` depends on `primary-muu2`.

Pre-typed-frame/tap chain now reads:

- `primary-2cjv` root.
- `primary-3cl1` depends on `primary-2cjv`.
- `primary-bann` depends on `primary-2cjv` and `primary-3cl1`.
- `primary-145a` depends on `primary-bann`.

Persona-agent epic now reads:

- `primary-gvgj.1` and `primary-gvgj.2` are root contract beads.
- `primary-gvgj.3` depends on `.1` and `.2`.
- `primary-gvgj.4` through `.9` depend on `.3`.
- `primary-gvgj.10` depends on `.4` through `.9`.

Comments were added to `primary-li0p`, `primary-2cjv`, and `primary-gvgj` noting the repair and Spirit record 361.

## Child work planned

- Child 1: `primary-li0p` and, if naturally adjacent, `primary-avog` in `signal-frame`; avoid concurrent conflict with the existing `signal-frame/ARCHITECTURE.md` working-copy change.
- Child 2: `primary-gvgj.1` — scaffold/implement `signal-persona-agent` ordinary contract.
- Child 3: `primary-gvgj.2` — scaffold/implement `owner-signal-persona-agent` owner contract.

`primary-2cjv` is deliberately not launched in parallel with Child 1 because both touch `signal-frame`; it remains ready after Child 1 completes or can be assigned to a separate isolated worktree later.
