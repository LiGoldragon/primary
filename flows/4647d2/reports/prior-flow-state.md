# Prior Listener/Wispr flow state

Carried account for flow `4647d2`, reconstructed on 2026-09-02 from the
retained flow logs, the bounded 01a05588 transcript, current Listener
workspaces, current Orchestrate locks, and the Listener bead file. No Wispr
session or credential contents were opened.

## Bottom line

The streaming-port effort stopped after private-protocol transport and
authorization reverse engineering, at the latest identity-correction witness.
It did not reach a successful transcript, production integration, deployment,
or live Listener partial-stream verification.

The accepted feature line is isolated at Listener commit
`71a194df8dc6dfb232049473481e67b405153e49` (0.17.0), with later witness-only
commits ending at `b97090f3cd7b04a5c73d3dde16adca18dc95b2c8`. The production
checkout and service remain Listener 0.14.0, batch-on-stop, with PID 976964.
No streaming operation or partial-transcript protocol has landed on main.

## What each relevant flow settled

### 01a0439e: existing Listener behavior

The deployed Listener retained completed recordings in durable history and
joined independent 600-second upstream requests locally. The long-capture
anomaly was already present in stored upstream text; no local insertion path
was witnessed, and per-chunk responses/audio were not retained. This is useful
durability evidence, not Wispr streaming evidence.

### 01a04e75: isolated provider architecture

This flow created the isolated 0.17.0 feature line: a provider boundary,
Wispr-first/OpenAI fallback policy, durable attempts/results/history/delivery
state, request-time named `gopass` lookup, pause-aware raw-PCM segmentation
with overlap and a 5:50 hard cap, and actor-owned finalization. Remote full
tests and package build passed; bead `listener-a9b` was closed. Main
integration, downstream activation, gopass provisioning, and a real Wispr
call were explicitly not done.

The feature's concrete credential contract names `wispr-flow/session` and
`wispr-flow/user-id` (and `openai/api-key` for fallback). The values never
entered code, logs, arguments, environment, or durable job state.

### 01a05209 and 01a052bb: desktop packaging, not Listener integration

The unofficial, user-supplied-installer `wispr-flow-linux` Electron package
was repaired and integrated separately: Home owns the desktop package and
CriomOS owns narrow input capability. Ouranos deployments 89–91 and later
keyboard/window repairs were witnessed. The authenticated profile was only
inspected by metadata; its contents were not read. The canonical proposal
correction is `goldragon/proposal.datom`; any `.datomic`/`.dotos` wording is
superseded and must not be revived as a compatibility path.

These flows prove the desktop client can be installed and authenticated, not
that it exposes a supported transcription proxy or that Listener can use its
cloud session.

### 01a0539e: sandbox and typed-operation direction

The isolated sandbox began from 0.17.0 at `04c5ba2aba60b5e2c49de86e740f33c88161b0b4`.
It used inherited descriptors, sandbox-only sockets/stores, Wispr-only
routing, direct TLS, no daemon/audio device/OpenAI/fallback/retry/system
clipboard, and opaque diagnostics. Two non-private synthetic requests failed
with redacted protocol errors and returned no transcript. No third request was
authorized in that phase.

Static evidence then established that Desktop 1.6.7 uses a real bidirectional
gRPC stream and can emit progress/raw/formatted/candidate-beam states before
final output. The living separately ruled that streaming capture and ordinary
capture are different typed operations, with a third typed operation for an
already-recorded audio file. The file-result durable-history/delivery rule and
partial-visual ownership/persistence remain open design details.

The Noctalia `criomos/listener-level` visual was packaged and live-tested only
with synthetic partial/final events. It is not evidence of a production
Listener partial stream. Existing-file transcription should continue to
clipboard plus durable history, without automatic focused-application
injection.

### 01a05588: private API witness, current stop point

Read-only inspection first found no supported Desktop local proxy: no TCP/UDP
transcription listener, DBus service, CLI, native-messaging host, HTTP API, or
transcript-returning deeplink. The living then explicitly opened private API
reverse engineering.

The faithful h2/TLS witness progressed as follows:

1. The initial faithful stream reached the service: HTTP 200, gRPC status 7
   (`PERMISSION_DENIED`), zero response frames. DNS, TCP, TLS, ALPN, HTTP/2,
   RPC path, request submission, and half-close were thereby witnessed; no
   inference result was obtained.
2. The first model mismatch (`q049l843` versus packaged default `v31pl413`)
   was corrected, but the default still returned status 7.
3. A scoped extractor corrected the wrong bundled opaque key. The corrected
   key changed the response to status 5 (`NOT_FOUND`), proving the earlier
   key was wrong and the corrected authorization reached model resolution.
4. Known Desktop model variants were added. The Qwen route remained open
   through the safety cap, then returned HTTP 200, gRPC status 3
   (`INVALID_ARGUMENT`), one empty frame. This proves deployment/key/stream
   closure passed farther, but protobuf semantics were still rejected.
5. The recorder audit corrected the earlier four-request assumption: one-shot
   Desktop capture coalesces init, context, 13 raw PCM16LE 40-ms packets, and
   commit into one protobuf request, then half-closes. Commit `d3a942cb` records
   this one-shot contract; it is not ongoing partial-result streaming.
6. Exact default preference/context wrappers were added at `a603e4bb`; the
   result remained status 3. The latest identity audit found the canonical
   sources: Supabase nested `user.id`, WorkOS JWT claim
   `urn:wispr:user_external_id` (not `sub`), a separate persisted UUID-shaped
   Desktop session ID, and UUID-shaped request ID. Commit `b97090f3` added
   provider-specific UUID validation.

The transcript ends while the corrected UUID mapping is being tested against
the private endpoint. No outcome, transcript text, partial event, billing
result, or successful live request is recorded after `b97090f3`.

## Current implementation and collision map

Current Orchestrate locks are:

- Lock 440, `WisprAuthWitness`, `run_wispr_live_witness`,
  `/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-auth-witness`.
  Its empty post-commit child is at `b61082ea`, parent source
  `b97090f3`; preserve this ownership while continuing the canonical-identity
  witness.
- Lock 441, `WisprEdgeProxy`, `implement_wispr_edge_proxy`,
  `/home/li/wt/github.com/LiGoldragon/listener/listener-wispr-edge-proxy-01a05588`.
  Its empty post-commit child is at `250b32ac`, parent/source bookmark
  `b97090f3`; an active Rust build was observed under this worktree, so do not
  reuse or alter it.

Other Listener workspaces:

- `listener-wispr-sandbox` at divergent `cd8d7e81` is dirty in
  `Cargo.toml`, `src/bin/listener_wispr_sandbox.rs`, `src/lib.rs`, and
  `src/wispr.rs`; it is the continuing feature/sandbox workspace and must not
  be overwritten or merged implicitly.
- The old temporary `listener-wispr-auth-01a0539e` workspace is clean at
  `32f96622`, descended from `302aa698`, with no current lock.
- The default checkout is on production-era 0.14.0 and has an unrelated
  added `.beads/issues.jsonl` change; preserve it. The
  `parallel-transcription-healing` workspace is unrelated and should remain
  untouched.

The current Listener bead file contains closed `listener-a9b` only; it records
the 0.17.0 synthetic feature and explicitly says no real credential/provider
call occurred. The protocol spike `wispr-flow-linux-5v0` is recorded as
`in_progress` in the 01a05588 transcript, but no matching current Listener
bead is present. The locks above, rather than a visible open bead, are the
active ownership evidence.

## Current versus superseded evidence

- Current production is 0.14.0 batch-only. The 0.17.0 feature is isolated;
  its package/test success does not imply integration or activation.
- The four separate-request model was superseded by the evidence-backed
  one-shot combined request for final captures. True Desktop streaming still
  exists statically, but the current witness does not yet implement an
  ongoing production partial-result path.
- The global bundled-key lookup was superseded by the module-47708 scoped
  extractor; status 7 before that correction is not current authorization
  evidence.
- `v31pl413` is the packaged default and `q049l843` is the Qwen HTTP variant;
  status 5 for the corrected key means the default deployment was not found,
  not that the credential failed.
- Synthetic Noctalia rendering is current visual-client test evidence only;
  it does not prove live production partial text.
- Desktop packaging and Zeus/Bird rollout in 01a05cd5 (CriomOS
  `2929538c…`, Home `cf21965b…`, Lojix deployment 128) and the helper v0.1.3
  rollout in 01a05e03 (Ouranos generation 178) are separate desktop/input
  outcomes, not Listener streaming integration. Its remembered 01a05833 and
  01a05c80 descendants concern broad Codex/Claude deployment and startup, not
  Wispr streaming. 01a05d17 left its UI witness open.

## Unresolved work for the new realization

The living has now authorized migrating the existing Wispr credential into a
stable, setup-independent secure-store entry and continuing isolated tests,
integration, deployment, and live verification. That authority supersedes the
earlier “no provisioning/no real call” hold. The migration itself and its
stable entry status were not witnessed here; preserve the existing request-time
secret boundary, do not expose values, and coordinate the target entry name
with the feature's established names before wiring it.

Remaining technical work is:

- finish the locked canonical-identity/Qwen witness and obtain a structural
  success or a narrowly classified remaining error, with no transcript or
  credential text leaving the process;
- reconcile the dirty sandbox with the locked witness line before any product
  integration, then decide the one authoritative Listener workspace/bookmark;
- integrate the typed streaming operation, provider partial/final event
  contract, durable finalization, and shell visual ownership; ordinary and
  file-transcription semantics still need the recorded design rulings;
- run real isolated verification, then integrate the accepted line into main,
  activate downstream packages, deploy, and perform live verification. None of
  these steps is evidenced by the prior flows.

Until those steps succeed, do not claim that Listener streams Wispr audio,
receives partial text, preserves partials, or falls back correctly in a live
deployment. Keep the production 0.14.0 daemon and its existing sockets/stores
isolated from the witness.

## Sources

- `/home/li/primary/flows/01a0439e/log.md`, lines 3–17: Listener durability and anomaly boundary.
- `/home/li/primary/flows/01a04e75/log.md`, lines 5–33: provider design, feature head, tests, and explicit non-completion of integration/live calls.
- `/home/li/primary/flows/01a05209/log.md`, lines 11–37: desktop package, credential metadata-only inspection, and deployment/canonical-proposal corrections.
- `/home/li/primary/flows/01a052bb/log.md`, lines 1–23: canonical proposal migration and later desktop activation boundary.
- `/home/li/primary/flows/01a0539e/log.md`, lines 43–91: Listener destination, sandbox, streaming/typed-operation rulings, synthetic visual, and worktree history.
- `/home/li/primary/flows/01a05588/log.md`, lines 1–11: absence of a supported local proxy and opening of private reverse engineering.
- `/home/li/.codex/sessions/2026/08/31/rollout-2026-08-31T03-57-07-01a05588-db47-7091-af64-914a7c01fa1f.jsonl`, bounded assistant-message records through ordinal 3637: gRPC statuses, key/model corrections, one-shot packet contract, exact defaults, identity audit, and the last unrecorded-outcome witness.
- `/home/li/primary/flows/01a05cd5/log.md`, lines 5–41: separate Zeus/Bird packaging and deployment outcome.
- `/home/li/primary/flows/01a05833/log.md`, lines 1–44, and `/home/li/primary/flows/01a05c80/log.md`, lines 1–25: remembered descendant deployment/startup work with no Listener streaming result.
- `/home/li/primary/flows/01a05d17/log.md`, lines 7–17: setup UI witness remains open.
- `/home/li/primary/flows/01a05e03/log.md`, lines 13–21: helper v0.1.3 deployment; no Listener integration.
- Current read-only observations on 2026-09-02: `orchestrate 'Observe.Locks'`, `jj workspace list` and `jj status` in `/git/github.com/LiGoldragon/listener`, Listener source/worktree inspection, current `.beads/issues.jsonl`, and process listing showing only production `listener-daemon` PID 976964 among Listener/Wispr processes.
