# Design vision summary: criome/router/spirit recovery

Evidence source: aggregator transcript-block search/read over a temporary Claude transcript root containing a symlink to `/home/li/.claude/projects/-home-li-primary/a2018f45-014c-45ef-9483-b9e5c9c0f086.jsonl`. This summary separates psyche-authored or psyche-quoted constraints from agent interpretation. No direct transcript scraping was used.

## Settled psyche/design constraints visible through aggregator

### Authorization gates acceptance everywhere

Aggregator block `transcript-block:v1:3b89c61df8ad960a`, `AgentResponse`, timestamp `2026-07-07T13:41:29.318Z`, records the orchestrator acknowledging the corrected semantic: authorization gates acceptance everywhere, including locally; with authorization enabled, spirit does not record a change anywhere until quorum grants it.

Aggregator block `transcript-block:v1:80a29d5ba916e0e9`, `ToolCall`, timestamp `2026-07-07T14:06:03.424Z`, dispatches implementation with the psyche constraint quoted in the prompt: `The whole point of the authorization is to gate the operation from being accepted, and by that I mean being accepted everywhere, including locally. The quorum gates the acceptance everywhere.`

### Spirit does not own quorum logic

The same implementation dispatch points at the amended design and frames the implementation as spirit consulting criome before acceptance. In this transcript evidence, criome/quorum authorization is the gate; spirit is not the quorum authority.

### Criome state governance uses one state-change primitive

Aggregator block `transcript-block:v1:a1dc86af74ed8868`, `ToolCall`, timestamp `2026-07-07T15:13:06.623Z`, quotes the psyche's governance correction: `Any new contract needs to be proposed through a parent quorum. A new contract is a state change.` The prompt states that the same quorum-authorized state-change mechanism gates criome's own state, including contract issuance and contract-associated data such as the mirror-target list.

Aggregator block `transcript-block:v1:bc6d6a214027ee97`, `ToolCall`, timestamp `2026-07-07T15:19:05.344Z`, quotes the naming correction: `rename Contract to Criome, the account is the criome.` It also records sequencing: rename slice after in-flight everywhere-gate implementation.

### Silo and root-anchor decisions

Aggregator block `transcript-block:v1:fd26fb880bedb430`, `ToolCall`, timestamp `2026-07-07T15:57:15.481Z`, quotes two settled answers:

- Silo set: `just make it a single silo for now. that gradient will be replaced by a privacy-silo name, but that isn't on your plate.`
- Root-anchor re-pinning: `we can rotate. i'm not an idealist, i'm a realist.`

Aggregator block `transcript-block:v1:a67c0fdced9bce19`, `AgentResponse`, timestamp `2026-07-07T15:57:26.733Z`, restates the operational consequence: one silo now; named privacy silos later; per-silo governance and public-only mirroring defer until named silos exist; mirror-list stays its own log; re-pinning after root succession is allowed.

## Probably implemented or tested

Aggregator-visible agent-authored evidence says:

- `transcript-block:v1:4dbc61f6c5427349`, `SessionEvent`, timestamp `2026-07-07T14:27:24.856Z`: criome dead-round supersession complete and pushed at criome commit `0a96a23aefb9`, version `0.8.0`.
- `transcript-block:v1:26e00c2abff792f7`, `SessionEvent`, timestamp `2026-07-07T15:19:11.496Z`: verification worker reported current mains with criome `0a96a23`, signal-criome `7436072`, spirit `1698cba`, signal-spirit `eba2afe`, sema-engine `7cfcece`; mentions `AdvanceRefused` and staging seam.
- `transcript-block:v1:ee37487c120b3e43`, `SessionEvent`, timestamp `2026-07-07T15:38:57.125Z`: design worker says code facts were verified and `the everywhere-gate has already landed: criome 0.8.0, spirit staging seam, AdvanceRefused`.

These are agent-authored evidence, not authority. A fresh agent should verify repository heads and tests before relying on them.

## Uncertain or not proven by aggregator evidence

- The interrupted everywhere-gate implementation worker did not produce a normal final report through aggregator; its notification result is only the session-limit message.
- The scratch mirror typecheck worker has no detailed aggregator-visible handoff.
- The contract-crate schema toolchain migration agent named in the orchestration brief was not recovered through the attempted searches; no conclusion is made here.
- Exact test commands and pass/fail evidence for the final implementation are not recoverable from the aggregator blocks used here.

## Recommended design pickup posture

Proceed as if the semantic direction is settled: criome/quorum authorization gates acceptance everywhere; criome state changes are governed by the same parent-quorum primitive; `Contract` is becoming `Criome`; one silo exists for now; root-anchor re-pinning is allowed. Treat implementation state as probable but requiring direct repo/test verification.
