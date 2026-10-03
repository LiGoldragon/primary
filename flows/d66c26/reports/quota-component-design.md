# One-shot subscription-usage snapshot: native component boundary

## Decision

Put the one-shot subscription-usage snapshot on the ordinary Harness working
surface. It is a new read-only request/reply on `signal-harness`, served by
the existing `harness-daemon` implementation and invoked by the existing
`harness` CLI. This is an extension of two existing repositories, not a new
Nexus repository and not a Mind operation.

`nexus` is the universal lifecycle library, not a domain-command home:
[`/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md`](/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md)
leaves domain configuration, contracts, and effects to component repositories.
Mind owns durable cognitive/work state; its CLI is deliberately a client of a
long-running Mind daemon, so it is not the home for a no-storage, one-shot
provider observation.

Harness already owns Claude/Codex/Pi adapter-facing runtime behavior and has
the relevant ordinary client/daemon route:

```text
harness CLI → signal-harness request → harness-daemon → typed reply → stdout
```

The current implementation of that route is in
[`harness/src/client.rs`](/git/github.com/LiGoldragon/harness/src/client.rs)
and [`harness/src/daemon.rs`](/git/github.com/LiGoldragon/harness/src/daemon.rs).
This records code ownership only. It does not claim that a Harness daemon is
currently deployed or running.

## Required slice

The new ordinary contract operation must mean one fresh, read-only snapshot of
all known Claude and Codex subscriptions and live-session context observations.
The contract needs a corresponding typed reply that can carry observed data,
freshness/provenance, and typed unavailability without exposing credential
material or raw provider responses. Its final authored names and field shapes
remain for the contract implementation; no existing `SnapshotUsage` operation
or response exists to reuse.

This is a daemon-level operation. It must be handled before the existing
per-instance dispatch that selects a configured interactive Harness by name.
That makes the snapshot independent of configured Harness instances and of
launching Claude or Codex sessions. It reads the live local provider sources
already identified by the quota-source handoff, with bounded I/O and timeouts:

- Claude: read the local credential file only inside the program; check token
  expiry; call the fixed OAuth usage endpoint only with a still-valid token;
  normalize `limits[]` first and retain non-null unrecognized top-level
  windows as unknown-present rather than discarding them.
- Codex: discover local app-server control sockets; use the existing
  initialize/initialized WebSocket exchange; query every returned limit ID and
  each server-declared window rather than assuming a primary weekly limit.
- Context: enumerate only live sessions/loaded threads, use existing bounded
  transcript/rollout-tail readers, and preserve their exact/proxy/superseded
  freshness states. Claude context percentage remains unknown without a live
  status-line snapshot.

No absolute quota limit is invented when the providers expose only a used
percentage. A token refresh is not performed. A failure response is a stable
typed category, never an error echo. Tokens, credential paths, raw response
bodies, process arguments, and environment contents must not be emitted.

The command is paced by invocation: one request produces one snapshot and
returns. It adds no Watch operation, subscription, polling loop, persistent
store, scheduler, or new daemon. The existing daemon implementation is reused
when deployed; its deployment status is a separate fact.

## Acceptance boundary

The installed command is accepted only when one invocation returns both
provider accounts, deduplicates the known same-account Codex homes, enumerates
every provider-reported quota limit and window, and includes the live-session
context observations it can bind. Every quota window reports used percentage,
remaining percentage when derivable, its provider-supplied reset/window basis,
and its absolute limit as unknown when unavailable. A remaining-per-day or
variance figure is permitted only with its operands and basis in the typed
reply: remaining percentage, time until the named reset, and the window
duration or observation interval used. It must be unknown when any operand is
unknown or stale.

Each provider/session result carries its observation time and freshness state.
Unavailable credentials, absent sockets, expired Claude access tokens,
unbound threads, transcript supersession, and bounded transport failures stay
explicitly unavailable, stale, proxy, or superseded as applicable. A provider
failure cannot suppress the other provider's result. These are semantic
acceptance conditions for the new typed request/reply; they do not prescribe
Datom syntax or a wire ABI.

## Bounded implementation surface

1. In `/git/github.com/LiGoldragon/signal-harness`, author the request/reply
   vocabulary in `ethos/signal.ethos`, regenerate `src/generated/signal.rs`,
   and extend `examples/canonical.datom` and `tests/contract.rs` with the
   generated contract witnesses.
2. In `/git/github.com/LiGoldragon/harness`, add the daemon-level dispatch in
   `src/daemon.rs` and a narrowly scoped provider-observation module under
   `src/` that owns normalization, redaction, bounded local reads, and the
   two provider transports. Add recorded-input/provider fixture tests and an
   end-to-end CLI contract fixture in `tests/component_cli.rs`.
3. `src/client.rs` and `src/command.rs` already parse one ordinary
   `HarnessRequest`, submit it, and render one `HarnessEvent`; they should not
   need a second command language or a separate executable.

The confirmed test homes are `signal-harness/tests/contract.rs` and
`harness/tests/component_cli.rs` plus new Harness-local fixtures. No third
repository is required for this slice.

## Delivery condition

Because the contract changes, regenerate the contract projection, update
Harness to the new immutable `signal-harness` revision, rebuild both the
`harness` CLI and `harness-daemon`, and deploy them through the existing native
component deployment path before treating the command as usable. Any currently
running daemon built against the old contract must be replaced together with
its client. The deployment configuration/path was not inspected here, so this
report does not prescribe it.

## Existing protocol reference

[`tools/field-census/codex-context.mjs`](/home/li/primary/tools/field-census/codex-context.mjs)
and [`tools/field-census/claude-context.mjs`](/home/li/primary/tools/field-census/claude-context.mjs)
already provide the Codex app-server protocol and bounded per-session context
algorithms. They are implementation references for the new Harness module,
not a finished component or an alternate command surface.

## Sources

- [`flows/28d847/reports/quota-sources.md`](/home/li/primary/flows/28d847/reports/quota-sources.md)
- [`flows/28d847/vision/quotas.md`](/home/li/primary/flows/28d847/vision/quotas.md)
- [`harness/ARCHITECTURE.md`](/git/github.com/LiGoldragon/harness/ARCHITECTURE.md)
- [`signal-harness/ARCHITECTURE.md`](/git/github.com/LiGoldragon/signal-harness/ARCHITECTURE.md)
- [`mind/ARCHITECTURE.md`](/git/github.com/LiGoldragon/mind/ARCHITECTURE.md)
- [`nexus/ARCHITECTURE.md`](/git/github.com/LiGoldragon/nexus/ARCHITECTURE.md)
