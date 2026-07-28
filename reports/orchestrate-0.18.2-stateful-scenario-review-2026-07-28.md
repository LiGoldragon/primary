# Orchestrate 0.18.2 stateful-scenario review — 2026-07-28

## Verdict

The first scenario is a real packaged Nix integration witness, but it does not
yet satisfy the requested all-feature scenario. Downstream pinning remains
paused.

## Verified

- `main@origin` is `8d80eed914b0`, version `0.18.2`.
- The stateful scenario and separate state-purity Nix checks pass.
- Substantial scenario logic is outside `flake.nix`.
- It uses the packaged daemon plus ordinary and meta NOTA clients.
- Declared worktree paths remain absent; production source contains no VCS or
  process probe.
- Human age presentation uses the shared `relative-age-display` package.

## Missing coverage

- Lane unregister, lane retirement, and session clearing.
- All workflow operations and upgrade/handover.
- Four observation variants.
- Handoff, ambiguous/missing worktree conclusion, agent registration, and
  detailed launch-refusal cases.
- Restart proof for archived/merged worktree status and agent/topic state.
- Upgrade-socket binding and behavior.

The shell checks use substring matching rather than structural NOTA
assertions. The age assertion depends on wall-clock presentation.

## State-semantics discrepancy

The source still enforces count-bounded retention on writes:

- activities: 256 rows;
- divergences: 128 rows;
- triage records: 256 rows.

This is not filesystem/worktree management, but it contradicts claims that
those tables are append-only or that no automatic table reclamation exists.
The behavior must be tested and documented accurately unless the psyche
separately changes retention policy.

## Stale documentation

Repository documentation still describes worktree scaffolding, `jj workspace
add`, missing-checkout reaping, and deleted VCS/path-probe files. Runtime
correctly refuses scaffolding and performs state-only transitions, so the
documentation must be corrected before the final release is pinned.

## Required correction

Expand the packaged scenario to cover every supported operation and key
refusal, use structural NOTA assertions, prove restart state comprehensively,
test bounded retention explicitly, and correct stale documentation. Keep the
related-work notification as a deferred acceptance case until the psyche
chooses branch/bookmark versus logical work-line identity.
