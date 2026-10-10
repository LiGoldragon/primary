# Counselor role registration — 2026-06-02

## What changed

The workspace now has a `counselor` role for personal-affairs advisory, paired with the `assistant` lane. Where `assistant` (default agent Pi) is the user-facing support that clarifies the request and keeps the work legible, `counselor` (default agent Claude) sits upstream — surfacing options, weighing tradeoffs, naming what is at stake, and offering advice the psyche can accept or decline. The two roles share `personal affairs` as scope; they divide labor by disposition.

This is the sixth main role, alongside `operator`, `designer`, `system-operator`, `poet`, and `assistant`.

## Surfaces updated

- `orchestrate/roles.list` — appended `counselor` after `assistant`, so `tools/orchestrate` can claim, release, and show `orchestrate/counselor.lock`.
- `skills/counselor.md` — new role discipline file modeled on `skills/assistant.md`.
- `skills/skills.nota` — `Role counselor skills/counselor.md Apex` entry under the Apex-tier role block.
- `AGENTS.md` — counselor named in the "Roles" section; the leading sentence changed from "Five main roles" to "Six main roles".
- `orchestrate/AGENTS.md` — counselor row added to the role table; counselor added to the `<role>` enumeration after `assistant` in the claim flow; counselor added to the per-role reports list. Opening "five main roles" updated to "six main roles".
- `skills/role-lanes.md` — counselor named in the mirror-model role enumeration, the lane-shape table examples, the main-role reading-list paragraph, and the "see also" main-role skill list (count updated from five to six).
- `orchestrate-cli/tests/registry.rs` — `SAMPLE_REGISTRY` constant, `parses_all_lanes_in_order` expected vec, and `peer_lanes_exclude_self` peer count (13 → 14) updated.
- `orchestrate-cli/tests/claim_release.rs` — `REGISTRY` constant and `status_lists_every_lane_in_registry_order` expected vec updated.
- `reports/counselor/` — created as the role's report lane.

## Intent captured

Spirit record `1426` captures the psyche's decision: counselor is a workspace role/lane for advising in personal affairs and working with the assistant lane. Topics `workspace orchestrate`, kind `Decision`, magnitude `Medium`.

## Verification

```sh
cd orchestrate-cli && cargo fmt && cargo test --quiet     # all suites pass
cd orchestrate-cli && cargo build --release --bin orchestrate --quiet
tools/orchestrate status                                   # counselor.lock listed (idle)
tools/orchestrate claim counselor /home/li/primary/reports/counselor \
  -- counselor report-lane smoke test                      # accepted
tools/orchestrate release counselor                        # lock cleared
```

The Rust unit + integration suites (registry, lock_file, overlap, scope, argv_decode, claim_release) all pass with the counselor fixture added. The `tools/orchestrate status` listing now shows `counselor.lock` between `assistant.lock` and the open-beads block. The smoke-test claim and release both round-tripped cleanly, leaving `orchestrate/counselor.lock` empty.

## Open follow-ups

- **No tests yet for assistant/counselor as a paired-role unit.** The `claim_release.rs` and `registry.rs` suites verify each lane appears and the lane count is correct, but there is no test that asserts counselor's discipline pairing with assistant. That pairing lives in `skills/counselor.md` prose for now; if the pairing becomes a structural mechanism (shared lock semantics, joint scope checks), a structural-truth test belongs in `architectural-truth-tests`.
- **The Pi-bound `assistant` and Claude-bound `counselor` are working hypotheses.** Default agents are convenience labels per `orchestrate/AGENTS.md`; the workspace allows any agent on any lane. If the psyche prefers a different default pairing, the role table is the single edit site.
- **Whether the counselor advises *only* on personal affairs, or also on workspace-shape questions where the psyche wants a thinking partner separate from designer.** Today the skill file scopes counselor to personal-affairs advisory; that is the conservative read of the psyche's wording. If counselor should also be a general advisory surface — adjacent to designer the way assistant is adjacent to operator-implementation — that widens the skill prose.
