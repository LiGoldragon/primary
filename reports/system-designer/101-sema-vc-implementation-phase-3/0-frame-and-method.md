# 101 — Sema version control, implementation phase 3 + fix round: frame and method

Phase 3 completed the build the psyche commissioned: spirit as the
version-control pilot, the mirror triad as the remote, and the fold's
tamper-detection story made behavioral. One build workflow
(`wf_7d6062d4-e2b`, 6 agents) and one fix-round workflow
(`wf_8b2831ee-e40`, 6 agents), each task adversarially reviewed; the fix
round's re-reviewers reproduced the original failure scenarios against the
fixed code before approving.

| Chapter | Subject | Final verdict |
|---|---|---|
| `1-spirit-pilot.md` | spirit `versioned-store-pilot`: schema-declared families, generation-only opt-in, v8→v9 logged-fold bootstrap (`t0tu`) | needs-fixes → closed in fix round + orchestrator nix work |
| `2-mirror-triad.md` | `mirror` / `signal-mirror` / `meta-signal-mirror` (new repos, `0yx5`): payload-blind daemon, TCP ingress, end-to-end arc witness | needs-fixes (two empirically-proven wedges) → closed, self-heal proven |
| `3-fold-tamper-witnesses.md` | sema-engine `versioned-fold`: nine doctored-store witnesses + two surface fixes | needs-fixes (two unwitnessed paths) → closed |
| `4-recovery-and-remaining.md` | the recovery dossier (written under cutoff risk) + remaining integration/deploy items | superseded in part by chapter 5; integration list current |
| `5-fix-round.md` | the fix round: every must-fix closed, re-reviewed, approved | approve ×3 |

Final branch heads after the fix round: spirit `versioned-store-pilot` @
`9c8c44b1` (+ the orchestrator's nota-next→main unification commit on top,
closing the nix-build duplicate-lockfile failure diagnosed in chapter 4);
sema-engine `versioned-fold` @ `dbe29427`; mirror @ `4724ac01`,
signal-mirror @ `4fa767d7`, meta-signal-mirror @ `674f24d2` (mains,
greenfield). All other branches as in chapter 4's table.

The arc's acceptance witness — a component store shipping its outbox over
real TCP frames to the running mirror daemon, durability flipping to
`ServerCommitted`, and a fresh store restoring identical records via the
engine-owned import — passes (`mirror/tests/end_to_end_arc.rs`), alongside
spirit's own migrated-store checkpoint-restore witness. `29pb`'s first cut
(data-loss protection with a remote) exists end to end at the daemon level;
what remains is operator integration of the branch stack and
system-operator deployment of `mirror-daemon` on ouranos (beads filed —
chapter 4 §Remaining lists the full set with the integration order).
