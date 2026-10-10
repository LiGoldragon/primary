# Codex-half pair bootstrap preparation

Status: prepared for review; no `turn/start` has been sent.

## Live API witness

Endpoint: `/home/li/.codex/app-server-control/app-server-control.sock`, WebSocket JSON-RPC after HTTP Upgrade.

The live server is Codex `0.153.4`. `skills/list` with `cwds: ["/home/li/primary"]` returned the requested skills as enabled repo skills:

```json
[
  {"name":"spirit","path":"/home/li/primary/.agents/skills/spirit/SKILL.md"},
  {"name":"psyche","path":"/home/li/primary/.agents/skills/psyche/SKILL.md"},
  {"name":"behavior","path":"/home/li/primary/.agents/skills/behavior/SKILL.md"},
  {"name":"correction","path":"/home/li/primary/.agents/skills/correction/SKILL.md"},
  {"name":"vocabulary","path":"/home/li/primary/.agents/skills/vocabulary/SKILL.md"},
  {"name":"testing","path":"/home/li/primary/.agents/skills/testing/SKILL.md"},
  {"name":"psyche-interraction","path":"/home/li/primary/.agents/skills/psyche-interraction/SKILL.md"},
  {"name":"main-flow","path":"/home/li/primary/.agents/skills/main-flow/SKILL.md"},
  {"name":"edit-coordination","path":"/home/li/primary/.agents/skills/edit-coordination/SKILL.md"}
]
```

The generated live protocol schema establishes that skill injection belongs in `turn/start.params.input`, as `UserInput` entries of this shape:

```json
{"type":"skill","name":"spirit","path":"/home/li/primary/.agents/skills/spirit/SKILL.md"}
```

`thread/start.params` accepts `model`, `cwd`, `approvalPolicy`, `sandbox`, `reasoningEffort` is returned from the selected model configuration, and optional `developerInstructions`; it has no skill list. Therefore the first model turn must carry the nine `type: skill` input entries alongside one `type: text` entry. This is the structured skill interface; do not paste skill files into the prompt.

## Fresh thread and attach plan

After review, create exactly one fresh thread with:

```json
{
  "model":"gpt-6-astra",
  "cwd":"/home/li/primary",
  "approvalPolicy":"never",
  "sandbox":"danger-full-access"
}
```

Then issue one `turn/start` for that returned `thread.id`, with `input` ordered as the nine skill entries above followed by the text prompt below. No old thread is resumed or forked. The supported TUI attach command is:

```sh
codex resume '<THREAD_ID>' --remote 'unix:///home/li/.codex/app-server-control/app-server-control.sock' -C '/home/li/primary'
```

The command attaches the interactive TUI to the fresh thread through the existing remote app server. The thread ID is copied from the `thread/start` response; no canonical flow alias is invented.

## Proposed first prompt

```text
You are the fresh Codex half of the bcd02a pair. This is a machine-authored handoff from the main flow, with explicit provenance: FLOW_ID=bcd02a; prior paired flow=024bc7 at remembered depth 1. Preserve the identity and work of the main Astra/Fable pair; do not impersonate either existing root. The current pair is a scoped proof of concept only: no production configuration, deployment, credentials, or existing roots may be changed.

Claim your own actual flow ID after startup if the harness gives you one. Do not mint a fake canonical alias. If the main flow settles a shared pair lane, follow that witnessed decision and record the membership; otherwise remain the Codex member of the bcd02a pair.

Reacquire and apply the nine injected skills through the skill interface. Respect their authored instructions and the repository's ordinary-agent rules. The pair policy is: main Astra/Fable remains primary; cheap Luna/Haiku is medium effort for supporting witnesses; council is 2 for this POC and 3 for production; raw records remain in the middle stratum and only approved distilled material belongs in the top stratum. Do not edit unapproved skills or Vision files. Do not treat this handoff as authorization for production work.

First report that you received this handoff, identify your actual thread and flow provenance from available evidence, and state the exact pair membership and lane you will use. Then wait for the main flow's next scoped instruction. Use the medium stratum for pair messages and preserve provenance on every relay.
```

## Review gate

The first prompt and structured skill input are ready for main-flow review. No paid model turn has been started from this preparation artifact.

## Probe incident

During schema probing, two idle fresh Astra threads were accidentally created by sending `thread/start` twice while testing accepted parameter shapes. Neither has a turn. Their IDs were `01a09c90-c82c-7621-b7b3-c9734d94eb22` and `01a09c90-c8ee-7ad0-a270-05ff58f4f418`; neither is used by this plan. No further thread creation or model turn should occur until the main flow decides how to handle this deviation.

Cleanup attempt (2026-09-13): the supported `thread/archive` request was sent separately to each of those exact IDs. Both returned JSON-RPC `-32600` / `no rollout found for thread id ...`; therefore neither could be archived through the live server. A subsequent `thread/loaded/list` still listed both IDs. No delete or other cleanup operation was attempted, and the protected root thread `01a09c47-6fae-7a52-8879-1d5bcd02ab4e` was not touched. Both remain confirmed idle with zero turns.

Authorized launch witness (2026-09-13): the first probe thread was re-read before use and matched `gpt-6-astra`, `medium`, `/home/li/primary`, idle, and zero turns. Exactly one `turn/start` was accepted with explicit `model: "gpt-6-astra"`, `effort: "medium"`, the nine skill inputs above, and the reviewed handoff. The returned turn is `01a09c99-9d3f-77c1-bc28-ed33d3d87c83`; `thread/items/list` confirms all nine native skill items and the handoff text. The fresh MAIN executed `flow-id codex --flows-root /home/li/primary/flows`, returning canonical flow ID `34d94e`, and `intercom_whoami` witnessed `codex-3809808-f7566c95`; it sent readiness checkpoints to `codex-3752558-f7566c95` and `claude-2843909-f7566c95`. At last observation the turn remained `inProgress`, with no further launch or input. The appserver remains running for attachment.
