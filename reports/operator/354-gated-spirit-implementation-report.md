# Gated Spirit Implementation Report

## Summary

This operator run took Spirit from "schema-derived daemon with local duplicate
guarding" to a deployed, locally active Spirit stack with an LLM-backed
guardian available through the `agent` component.

The production deployment now has two user services:

- `agent-daemon.service`: local OpenAI-compatible LLM-call component, configured
  against the CriOMOS local provider on Prometheus.
- `spirit-daemon.service`: Spirit `0.8.0`, started from a prebuilt binary
  startup archive, with guardian configuration pointing at the agent socket.

The gate is on the `Propose` path. Direct `Record` remains the raw write path.
`Propose` lowers to a Nexus effect, retrieves relevant existing records, asks
the guardian for a typed verdict, and either records the entry or returns
`GuardianRejected`.

## Landed Commits

| Repo | Commit | Meaning |
|---|---:|---|
| `signal-spirit` | `a458c026` | Added daemon guardian-agent configuration to the Spirit contract. |
| `signal-agent` | `d29fd78e` | Refreshed generated artifacts for current schema/NOTA syntax. |
| `meta-signal-agent` | `00b2302b` | Refreshed generated artifacts for current schema/NOTA syntax. |
| `spirit` | `c621f090` | Added the `signal-agent` guardian path and `Version` signal. |
| `spirit` | `8fe88d66` | Removed the separate `Weight` axis, bumped the store to schema v6, and made `RecordAccepted` / `Proposed` return only the created record UID. |
| `agent` | `758df952` | Added `agent-write-configuration` and Nix package surface. |
| `CriOMOS-home` | `dfba8741` | Added deployed agent service and wired Spirit guardian deployment. |
| `CriOMOS-home` | `d5227b7f` | Fixed guardian config archive encoding to field-only payload form. |
| `CriOMOS-home` | `8e909a40` | Pinned the UID-only Spirit build. |
| `CriOMOS` | `78cd8113` | Pinned the fixed Home build into the FullOS deployment. |
| `CriOMOS` | `df05927f` | Pinned the UID-only Spirit deployment and activated it locally. |

## Contract Work

`signal-spirit` now carries the daemon-level guardian configuration. The shape
is deliberately in the contract, not local Spirit-only config, because daemon
startup configuration belongs to the component contract and is encoded into the
binary startup archive before the daemon starts.

The added guardian configuration carries:

- agent socket path
- optional provider name
- optional model name
- timeout in milliseconds
- maximum output tokens

`signal-agent` and `meta-signal-agent` were refreshed against the current
schema/NOTA stack. The notable syntax consequence is that canonical strings now
prefer bare tokens when legal, for example `(User hello)` instead of bracketed
strings where brackets are not needed.

## Spirit Runtime Work

Spirit gained the `agent-guardian` feature:

```toml
agent-guardian = ["nota-text", "dep:signal-agent"]
```

That feature adds the `signal-agent` contract and enables the LLM guardian
path. The feature implies `nota-text` because the guardian asks the model to
return a NOTA `GuardianVerdict`, and Spirit must parse that text into the
generated verdict type.

The Nexus schema gained a private guardian verdict type:

```nota
GuardianVerdict [Accept (Reject)]
Reject { GuardianRejectionReason * Explanation * }
```

This is the model-facing verdict shape. It is not the public Spirit output. If
the model returns `Accept`, the proposal continues. If it returns `Reject`, or
if the guardian path fails, Spirit maps the result to the public
`GuardianRejected` output.

The runtime path is:

1. CLI/client sends `Propose Entry`.
2. Signal admission validates the entry.
3. Nexus lowers `Propose` into a Nexus effect.
4. Spirit retrieves relevant existing records with `guardian_records_for`.
5. Spirit sends a `signal-agent::Call(Prompt)` over the agent Unix socket.
6. Agent calls the configured OpenAI-compatible provider.
7. Agent returns `Completed(Completion)`.
8. Spirit parses the completion text as `GuardianVerdict`.
9. `Accept` records the proposal; `Reject` returns `GuardianRejected`.
10. The deterministic duplicate guard still runs after the LLM guardian.

Direct `Record Entry` does not use this gate. It still writes through the SEMA
write path. That distinction matters: operational callers that want guardian
admission must use `Propose`, not `Record`.

## Guardian Prompt

The guardian prompt tells the model to judge whether the proposed forward
intent arrow can enter a mutually consistent intent store.

The prompt includes:

- the candidate `Entry` rendered as NOTA
- relevant existing records rendered as NOTA
- the exact accepted form: `Accept`
- an exact rejected form example
- rejection criteria: contradiction, compound intent, non-intent, unclear
  privacy, unclear category, or retrieval insufficiency

The agent call requests `OutputMode::Nota`, so the agent adds its own
NOTA-output instruction and validates model output as parseable NOTA before
returning it.

## Error Mapping

Guardian failures fail closed. Spirit maps guardian errors into
`GuardianRejected` rather than admitting the proposal.

| Guardian failure | Public rejection reason |
|---|---|
| socket unavailable | `HarnessUnavailable` |
| frame read/write/decode failure | `HarnessUnavailable` |
| agent returned a non-completion output | `HarnessMalformed` |
| model completion was not a parseable verdict | `HarnessMalformed` |
| model returned `Reject` | model-specified `GuardianRejectionReason` |
| duplicate proposal | `Duplicate` from deterministic store guard |

This is intentionally conservative. If the guardian cannot be reached or cannot
produce a typed verdict, `Propose` does not silently become `Record`.

## Agent Work

The existing `agent` component was used as the LLM-call substrate. It remains an
LLM API caller, not a full agent harness.

The added `agent-write-configuration` binary is the deploy/bootstrap text edge.
It accepts one NOTA request, builds a typed `AgentDaemonConfiguration`, and
writes a binary rkyv archive for `agent-daemon`.

The daemon itself still takes exactly one binary startup archive. It does not
parse NOTA at startup.

The startup request carries provider seeds:

- provider name
- endpoint
- default model
- API key handle

The API key handle is an environment variable name. Secret bytes are not placed
in Nix, the rkyv archive, the lock file, or the report. The deployed service
reads the real local LLM token from gopass at runtime and exports it only into
the agent daemon process environment.

## CriOMOS Deployment Work

`CriOMOS-home` now owns the local deployment shape for this stack.

It builds the agent startup archive in Nix with `agent-write-configuration`.
It builds the Spirit startup archive in Nix with `spirit-write-configuration`.
Service startup therefore does not generate either archive.

The deployed local provider values are:

- provider: `criomos-local`
- model: `gemma-4-26b-a4b`
- endpoint: the large-AI endpoint projected from Horizon / CriOMOS-lib
- key handle: `LOCAL_LLM_API_KEY`
- gopass entry read at runtime: `goldragon.criome/local-llm-api-token`

`agent-daemon.service` is enabled when the projected cluster has a large-AI
endpoint. `spirit-daemon.service` is still deployed even if there is no endpoint;
in that case the guardian configuration is `None`.

When the guardian exists, `spirit-daemon.service` has `Wants` and `After` on
`agent-daemon.service`.

The old persona-spirit services are explicitly conflicted by the Spirit unit
and absent from the generated Home profile.

## The NOTA Encoding Bug Found During Deploy

The first FullOS switch caught a real archive-generation bug that the fake Home
check missed.

I initially encoded the optional guardian payload as:

```nota
(Some (ConfigurationWriterGuardianAgent ...))
```

The derived `NotaDecode` for `ConfigurationWriterGuardianAgent` expects the
field payload in the typed `Option` context, not a second headed record. The
correct encoding is field-only:

```nota
(Some (...))
```

Fixes landed:

- Home module emits the field-only payload.
- The fake deployment check now rejects the incorrect headed guardian form, so
  this class of mistake is caught before FullOS activation.

## Verification Run

Component tests/builds completed before deployment:

- `signal-spirit`: tests green.
- `signal-agent`: `cargo test --all-targets` and `cargo test --features nota-text --all-targets`.
- `meta-signal-agent`: `cargo test --all-targets` and `cargo test --features nota-text --all-targets`.
- `spirit`: default tests, `nota-text` tests, `agent-guardian` tests, and Nix default package build.
- `agent`: default tests, `nota-text` tests, `live-provider` tests, and Nix default package build.
- `CriOMOS-home`: `checks.x86_64-linux.spirit-deployment` green.

Production deployment:

- FullOS switch through `lojix-run` succeeded for `goldragon / ouranos`.
- `agent-daemon.service` is active.
- `spirit-daemon.service` is active.
- old `persona-spirit*` user units are not found / inactive.
- `spirit Version` returns `0.8.0`.
- production record count query returns `1418`.

Live provider checks:

- direct deployed `agent` call reached Prometheus/Gemma and returned typed
  `Completed`.
- guardian-shaped NOTA call returned `Accept` when given enough output tokens.
- a temporary Spirit daemon with a temporary database was configured against
  the production agent socket; `Propose` accepted a temp record and counted it
  in that temp store.

## Production State

Current observed production state after deploy:

```nota
(VersionReported (0.8.0 (1420 3566863645473464308)))
(RecordsCounted (1418 (1420 3566863645473464308)))
```

Both user services are active:

```text
agent-daemon.service active
spirit-daemon.service active
```

The old persona-spirit unit names are absent/inactive.

## Incident During Verification

During the first temporary-daemon test, I accidentally used the deployed Home
`spirit` wrapper. That wrapper intentionally overwrites `SPIRIT_SOCKET`, so the
test command hit the production daemon and created one test record:

```nota
ug3t
```

I immediately removed it and verified lookup returns `record not found`.

The production database marker advanced because the accidental record and its
removal were real writes.

During the UID-only correction deployment, I made one deliberate temporary live
record to verify the public reply shape:

```nota
(RecordAccepted q2pp)
```

I immediately removed it and verified lookup returns `record not found`. The
live record count returned to `1418`; the marker advanced because the temporary
record and removal were real writes.

The corrected temp test used the deployed Spirit binary directly, bypassed the
wrapper, and wrote only to the temporary database.

## What Is Production-Ready

Production-ready now:

- binary-only daemon startup for both Spirit and agent
- Nix-built startup archives
- local user services enabled and active
- local Prometheus/Gemma provider reachable through `agent`
- Spirit `Propose` guarded by agent-backed typed verdicts
- fail-closed guardian error handling
- deterministic duplicate guard still present
- no separate `Weight` axis; reaffirmation now raises `Importance`
- `RecordAccepted` and `Proposed` public replies return only the created UID
- old persona-spirit services removed from the active profile
- `Version` signal for version reporting

## What Is Not Done

This did not implement a full general agent harness. The deployed `agent`
component is the LLM-call substrate: `Call(Prompt)` to provider completion. That
is enough for Spirit's guardian path but not a full multi-step harness backend.

The gate is not on `Record`. Callers must use `Propose` for guarded admission.
If the intended product shape is "all user-facing captures are gated," then the
CLI or workflow convention must route durable captures through `Propose`, or the
raw `Record` path must be restricted/renamed.

The guardian is model-prompted, not a formal verifier. The typed verdict parse
and fail-closed mapping make the boundary safe operationally, but the quality of
semantic judgment is still model-dependent.

The guardian prompt and retrieval strategy are first production shape, not final
research-complete shape. `guardian_records_for` retrieves related records by
category with default certainty behavior; it does not yet implement a deep
semantic search or multi-step investigation loop.

## Operational Notes

For a guarded write, use `Propose`, for example:

```nota
spirit "(Propose ([Meaning] Constraint [schema creates the interface] High Minimum Zero))"
```

For an immediate raw write, use `Record`:

```nota
spirit "(Record ([Meaning] Constraint [schema creates the interface] High Minimum Zero))"
```

For version:

```nota
spirit Version
```

For count:

```nota
spirit "(Count (Any Any Any None Any Any Any))"
```

The last number in `VersionReported` or `RecordsCounted` is the state digest
inside the `DatabaseMarker`. The first number in the marker is the commit
sequence.
