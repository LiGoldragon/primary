# Harness failure forensics — 2026-07-28

## Scope and confidence boundary

This is a read-only forensic pass over primary reports, agent outputs, Beads,
local configuration, and relevant LiGoldragon repositories. It did not inspect
private material, send requests to live harness daemons, restart anything, or
run a state-changing harness command.

The reported loss is not identifiable from the available artifacts. No record
ties a named session, terminal error, no-output event, or token/accounting
measurement to “roughly ten days” and “about half the tokens.” Those quantities
are therefore not repeated as measured facts below.

The most likely candidate is the **Orchestrate coordination/control-plane
failure** (medium confidence, about 0.70), not necessarily the Rust `harness`
component. “Harness” may have been used broadly for the agent-running and
coordination machinery. Two narrower candidates are documented separately and
must not be merged into that conclusion.

## Observed timeline

| Date | Observation | What it establishes | What it does not establish |
| --- | --- | --- | --- |
| 2026-07-05 onward | `reports/OrchestrateContinuation/ContextHandover.md` records that the documented `Register` example had been invalid since 2026-07-05. | The guidance agents relied on was stale for an extended period. | That every failed session used that example. |
| 2026-07-18 to 07-26 | Primary history is dominated by regenerated role/skill packets and Orchestrate worktree/lane repair work; Orchestrate main received ownership/liveness fixes on 07-23 and further changes through 07-26. | The period overlaps a substantial coordination-system repair effort. | A causal token-loss total. |
| 2026-07-23 | Orchestrate commits `029a93e2` and `b74a7963` changed lane-reclamation/liveness behavior to preserve active ownership across silence and close related proof gaps. | A real stale/idle ownership failure mode had enough evidence to require a code repair. | That the repair was deployed before the reported loss. |
| 2026-07-25 | The continuation handover says the deployed build still contained a 24-hour lane reaper that could remove an idle lane, its claims, and mark worktrees abandoned; it also says the newer code had not been redeployed. | Source/deployment drift was observed, and observation itself could affect durable state in that deployed version. | That this reaper deleted the particular work at issue. |
| 2026-07-25 | The same handover records no registered agents (`AgentDirectory []`), missing runnable lane-registration instructions for writers, invalid/help-poor CLI behavior, and roughly 1,100 recorded failures from agents brute-forcing command names. | The operative path was undiscoverable and repeatedly induced nonproductive retries. | The exact distribution of those failures or their token cost. |
| 2026-07-27 | Bead `primary-xpw` records a live Rust edit hook injecting nonexistent/deleted doctrine and a fabricated authority citation. | A separate harness-adjacent instruction-injection defect existed and could make an agent stall or follow false constraints. | A ten-day incident; only two firings were recorded. |

## Candidate A — Orchestrate control plane and its deployed/documented contract

### Evidence

- `reports/OrchestrateContinuation/ContextHandover.md:44-58` records the
  psyche’s assessment that Orchestrate was costing more than it gave, and the
  instruction to push through broken orchestration machinery.
- The same report at `:164-166` records that the Register example was invalid
  since 2026-07-05; at `:207-271` it records that writing agents had no runnable
  registration instruction, the CLI gave poor discovery errors, semantic
  refusals exited zero, and command-name brute forcing produced roughly 1,100
  failures.
- At `:139-151`, it records a deployed 24-hour reaper that could remove lanes
  and claims while newer source had removed that behavior but was not deployed.
- `orchestrate` commits `029a93e2` and `b74a7963` on 2026-07-23 are direct
  evidence that active-ownership/liveness semantics were being repaired, not
  merely discussed.

### Proven mechanism vs. inference

**Proven:** stale documentation plus a weak discovery/error interface caused
repeated malformed or semantically refused control-plane requests. A false
success exit code makes shell-status-only handling unreliable. The deployed and
source states differed during the period described in the handover.

**Supported inference:** agents spent substantial effort trying to satisfy a
coordination prerequisite they could not reliably invoke, instead of moving to
the underlying task. This is the best fit for a multi-day, broad cost event.

**Not proven:** the reaper deleted the reported work; that all or even most of
the claimed token loss came from Orchestrate; or that this is what the psyche
called “the broken harness.”

### Missed disconfirming checks / behavior failures

- Agents were instructed to register but were not given a valid executable
  invocation or a verified deployed reply shape.
- Documentation was repeatedly treated as sufficient when the handover says to
  trust the binary; no early, bounded contract probe was made the prerequisite.
- A zero exit code was not enough to distinguish acceptance from refusal, yet
  agents could mistake it for success or continue guessing after rejection.
- Work continued around a coordination block without a durable, compact failure
  receipt naming the deployed version, command, reply, and safe fallback.
- The presence of newer source changes was not disconfirmation of an old live
  daemon; deployment state was a separate witness and remained unproven or
  stale.

## Candidate B — Pi subagents “silent no output” defects

This is a real, narrower failure family, but its timing is earlier and it is not
linked to the reported loss.

### Evidence

- In `LiGoldragon/pi-subagents`, commit `409da8ad` (2026-07-12) fixes output
  file streaming after session compaction and adds a compaction end-to-end
  witness.
- Commit `441dd4c3` (2026-07-13) reports failed final turns as errors with
  bounded partial output.
- Commit `f8116eed` (2026-07-14) states the residual precisely: an empty
  length-stopped final previously resolved as `completed` with silent “No
  output.”
- The 2026-07-10 recovery snapshot contains an active lane named
  `PiHarnessNoOutputFailureAudit`, but no durable output from that lane was
  found in the searched primary artifacts.

### Assessment

The root cause for these extension-specific shapes is proven by the fixes and
tests: output tracking could lose its anchor after compaction, and selected
failed/empty terminal states were classified as completed. The local evidence
does **not** show that the affected release was installed at the time of the
reported loss, that a relevant session compacted or length-stopped, or that its
output was the work lost. It is therefore a competing candidate, not the lead.

## Candidate C — incomplete production session-launch path

`LiGoldragon/harness` commit `498cb031` (2026-07-18) added `LaunchSession`.
Its source declares Codex launch deferred/refused, continuation unsupported,
and the Claude command’s cooperative-channel flag effectiveness unverified.
The production Pi/Claude launch path is built from a golden NOTA composition and
terminal-cell directory inspection; its included launch test proves only a
fixture direct spawn. The real Pi steer test is explicitly environment/model
gated, and the message-router end-to-end path was separately recorded as failing
on a wire-deserialization error in July audit artifacts.

This establishes an incomplete, insufficiently witnessed production launcher.
It does not establish that any failed user work went through it, so it ranks
below Candidate A.

## Recurrent failure pattern

Across all three candidates, the recurring operational mistake is treating a
plausible boundary as a working one after a narrow or static witness:

1. A prompt, generated packet, or source-level/golden test asserts a workflow.
2. The live boundary either refuses it, classifies a failure as success, or is a
   different deployed revision.
3. Agents retry, reinterpret, or build adjacent machinery instead of recording
   the first discriminating runtime observation and taking the safe fallback.

The evidence supports this pattern. It does not prove that every affected agent
made every one of these mistakes.

## Best-supported single prevention control

Adopt a **fail-open, one-attempt harness preflight** for any task whose progress
depends on coordination, session launch, or agent delivery:

> Before a second harness/control-plane attempt, capture one actual deployed
> request/reply witness. If it is unavailable, malformed, refused, stale, or
> lacks the required observable, record that exact boundary failure and continue
> the independently safe underlying work without further harness guessing.

The preflight receipt must contain only: component/version or executable path,
the exact request, typed reply/error, and the next safe fallback. It must treat a
semantic refusal as failure even when the process exits zero. This single control
would have stopped the documented brute-force command loop, exposed source/live
drift before relying on it, and prevented a silent/empty result from being
accepted as completed.

## Smallest clarification needed to identify the exact incident

Provide one non-sensitive anchor from an affected session: the harness/client
name and approximate timestamp, plus **one** of (a) the visible error/no-output
text, (b) the command or request shape, or (c) the session/log directory name.
No transcript content, credentials, or personal material is needed. With that
anchor, the candidate can be matched against the correct runtime and a causal
timeline can be tested rather than inferred.
