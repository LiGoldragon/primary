# Primary Workspace Handoff

Date: 2026-05-06

## Current Goal

Li wants `~/primary` to become the primary workspace. The immediate project is
to build our own better version of Gas City, starting by isolating the durable
primitives from Gas City's current implementation:

- city directory;
- harness definitions;
- work records;
- routes from work to executors;
- prompt templates;
- event emission and subscription;
- observable process lifecycle.

The replacement should not clone Gas City's hidden state-machine shape.

## Workspace State

Created:

- `/home/li/primary`
- `/home/li/primary/repos`
- `/home/li/primary/reports`
- `/home/li/primary/GOALS.md`
- `/home/li/primary/RECENT-REPOSITORIES.md`
- `/home/li/primary/reports/1-gas-city-fiasco.md`

`~/primary/repos` is a symlink index only. Repository state remains under
`ghq` root `/git`, mostly `/git/github.com/LiGoldragon/...`.

Current link count: 35.

Cutoff rule applied: keep only linked repositories whose latest commit is on or
after 2026-04-22. Removed old symlinks only:

- `atom` (latest commit 2024-12-22)
- `annas-mcp` (latest commit 2026-02-22)
- `maisiliym` (latest commit 2026-04-18)

The ghq clones were not deleted.

## Report Written

Main report:

- `/home/li/primary/reports/1-gas-city-fiasco.md`

It summarizes the multi-day Gas City/Criopolis failure: Dolt CPU burn, no-op
metadata commits, setup failures, start-lock failures, wake-loss, pool/dog
demand surprises, config-drift loops, polling, hidden lifecycle metadata, and
tmux as an unsuitable runtime substrate.

Local source material read for that report:

- `/git/github.com/LiGoldragon/test-city/REPORT-2026-05-05-dolt-amp-investigation.md`
- `/git/github.com/LiGoldragon/test-city/REPORT-2026-05-05-test-city-testing-log.md`
- `/home/li/Criopolis/_intake/findings/2026-05-05-dolt-amp-live-trace.md`
- `/home/li/Criopolis/_intake/reports/2026-05-05-city-investigation-status.md`
- `/home/li/Criopolis/research/answers/dolt-write-amplification.md`
- `/home/li/Criopolis/research/answers/gascity-fork-stability.md`
- `/home/li/Criopolis/gascity-manual/runbook/dolt-high-cpu-when-idle.md`

## Important Context From Before This Workspace Setup

The prior Gas City fixing attempt was abandoned as a direction. We had patched
some surfaces in the fork, but new tight loops kept appearing. The active
opinion at handoff:

- Gas City has useful primitives.
- The current implementation has too many coupled reconcilers and hidden
  metadata truths.
- Polling and repeated no-op writes are core failure modes.
- Dolt/bd subprocess persistence is too expensive for the hot path.
- tmux should not be the runtime/process API for the replacement.

There are still uncommitted local changes in `/git/github.com/LiGoldragon/gascity`
from the prior fork debugging session. Do not assume they should be kept or
discarded without inspecting them. The new direction is to design a replacement,
not continue patching Gas City by default.

## Suggested Next Step

Create the first primitive inventory in `~/primary/reports`, probably named:

```text
/home/li/primary/reports/2026-05-06-gas-city-primitive-inventory.md
```

Recommended structure:

1. Define the primitive nouns: city, harness, executor, work, route, session,
   event, subscription, prompt, durable state, live process state.
2. For each primitive, record what Gas City did that was useful.
3. For each primitive, record what must be rejected from Gas City's
   implementation.
4. Sketch the smallest working replacement core: one city, one harness, one
   work item, one executor, one route, one append-only event log, one
   subscription.

Do not start implementation until that primitive inventory is clear.

## Restore Command

Start a new session in:

```sh
cd /home/li/primary
```

Then read, in order:

```sh
sed -n '1,220p' GOALS.md
sed -n '1,260p' reports/1-gas-city-fiasco.md
sed -n '1,220p' reports/2-primary-handoff.md
```

