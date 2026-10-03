# Home deployment 79 evidence

## Recorded terminal result

The flow log recorded on 2026-10-03 that Lojix deployment 79 advanced the
Home profile and then failed at `Activate` with `ActivationFailed`. The
recorded activation command was the resulting Home Manager generation's
`activate` entrypoint and its exit status was `1`. The captured operational
cause was refusal to replace the non-legacy `~/.local/bin/messenger-clj`
binding. This is a partial profile advance, not a successful switch.

The source record is [the deployment log](../log.md), entries dated
2026-10-03, and the retained deployment-execution transcript in this flow.

## Guard mismatch and correction state

The failing managed-file predecessor differed from the source guard. The
accepted Home correction changes the predecessor handling without weakening
the foreign-file, link, wrong-root, or alias refusal guards. The corrected
Home source was published; the corresponding CriomOS consumer repin remained
local when its GitHub SSH publication had no route. No immutable retry was
submitted from that unpublished consumer source.

## Current local profile and runtime

The current `home-manager` profile resolves to a Home Manager generation
distinct from protected rollback generation 1039. Generation 1039 still has
its profile link and activation entrypoint.

The running service set is split: stable `flow-nexus` is active at Flow
0.12.2, next `flow-nexus` is active at Flow 0.17.4, stable Message is
inactive, next Message is active, and the Orchestrate user unit is inactive
while its ordinary and meta sockets remain listening. Stable and next Flow
and Message socket pairs are present. This is not rollout success and does
not establish the fresh-launch or first-turn witness.

## Current source boundary

The canonical CriomOS-home and CriomOS directories are present, but both are
detached at unrelated source revisions; CriomOS also contains an untracked
USB-observer build tree. The expected prior worktree locations are no longer
Git worktrees. No source build, consumer publication, Lojix retry, or
activation was attempted from this state.
