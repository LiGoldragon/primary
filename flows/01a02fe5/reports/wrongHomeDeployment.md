# Wrong Home deployment attribution

## Result

An agent did deploy the Zeus user environment onto Ouranos. The concrete cause
was a mismatched Lojix request, not target substitution inside Lojix.

Deployment 49 named `goldragon zeus li` as its logical node and user, while its
copy and activation transport was `ssh-ng://li@ouranos` / `li@ouranos`. Lojix
keeps logical node and transport independent. It therefore materialized Horizon
for Zeus, built a Home environment selecting Zeus's `li` keygrip, and activated
that closure through SSH on Ouranos.

## Attribution

The request was submitted at `2026-08-23T20:21:08.176Z` by the
`lojix_daemon_deploy_plan` subflow. Lojix accepted it as deployment 49 and
recorded it completed and succeeded. The resulting local Home generation 973
was created on Ouranos at approximately `2026-08-23 22:23:28 +0200` and its
managed `.gnupg/sshcontrol` contained Zeus's declared keygrip.

The submitting transcript establishes who constructed the mismatched request.
It does not establish whether the logical Zeus target was intentionally approved
or accidentally carried over from prior Zeus work because the parent approval
content is unavailable. A stale logical target is therefore a hypothesis, not
a verified explanation.

## Mechanism

The deployed Lojix implementation copies the request's logical node and
transport independently into evaluation, copy, and activation. The pinned Home
module selects `user.pubKeys.${node.name}.keygrip`. Generated inputs for
deployment 49 named the node `zeus`, so the Zeus keygrip was the deterministic
result of the request.

This request shape had no invariant requiring a user-environment activation
transporting to Ouranos to also evaluate the Ouranos logical node. The mismatch
was consequently valid to the engine and reached successful activation.

## Disconfirming evidence

Deployment 27 did not introduce the foreign identity. Its request named Ouranos,
its materialized Horizon node was Ouranos, and its generated payload was
identical to the already-active profile. Earlier accepted user-environment
requests found in the August 19–22 transcript sweep also named Ouranos.

## Sources

- `/home/li/.codex/sessions/2026/08/23/rollout-2026-08-23T21-12-06-01a03009-87e6-7231-8d15-58a80bcbc94f.jsonl`, ordinal 789.
- `/home/li/.codex/sessions/2026/08/22/rollout-2026-08-22T14-20-14-01a0296a-18fa-7143-97fa-8c76f48bc898.jsonl`, ordinal 827.
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs`, deployed revision `782805bf07a4bcbb0c23e222b8916a3ceaf2e8af2`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`, pinned revision `756ce723ea7f1a58d20e2b6f153f15e30aa9b885`.
- `/git/github.com/LiGoldragon/goldragon/datom.dotos`.
- `flows/01a02fe5/witnesses/sshRecovery.md`.
- Flow `01a02fe5`.
