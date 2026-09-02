# Listener Wispr current code state

Inspection date: 2026-09-02. This is a read-only source and worktree audit. No
secret value was read and no product file was changed.

## Bottom line

The deployed/current stack is not on the Wispr port. Listener `main` is
`6905a4f1` (package version `0.14.0`) and has the original direct OpenAI
batch-transcription path. CriomOS-home `main` (`097a9bde`) locks its Listener
input to `6905a4f115092f0a7c1489aa4ad171785dcb7ec1`, so its dictation service
builds that OpenAI-only package. The current `signal-listener` and
`meta-signal-listener` main heads likewise have no Wispr/provider-policy
contract.

The Wispr implementation is real source on a separate Listener head,
`listener-wispr-01a04e75` at `71a194df`, with matching unmerged contract heads
`signal-listener:b44a9e7a` and `meta-signal-listener:03306429`. That Listener
head is internally wired when built from the branch, but it is not merged into
Listener main and is not the revision locked by Home. Later local heads add an
isolated desktop/edge witness; they remain branch-only. The true incremental
HTTP/2 sender is confined to that witness. The production provider on
`71a194df` materializes all gRPC-framed request messages and sends one blocking
Reqwest POST body, despite the RPC being named `TranscribeStream`.

## Directly witnessed repository and worktree state

| Area | Observed revision/state | What is present |
| --- | --- | --- |
| Listener main checkout | bookmark `main` `6905a4f1`; root working copy `fc37927f` has only an added `.beads/issues.jsonl` over parent `dcc8f1b4` | OpenAI-only Listener baseline; no Wispr/provider modules in `src/lib.rs` |
| Listener Wispr branch | `listener-wispr-01a04e75` `71a194df`; dedicated path has no working copy | 0.17 provider router, durable jobs/policy, Wispr wire adapter, daemon/runtime wiring |
| Listener edge branch | `listener-wispr-edge-proxy-01a05588` `b97090f3`; dedicated worktree clean (empty `@`) | 0.17 branch plus 3,329-line Wispr module and sandbox/edge witness |
| Listener auth branch | `listener-wispr-auth-discriminator-01a05588` `302aa698`; dedicated worktree clean (empty `@` at `b61082ea`) | 0.17 branch plus isolated auth-discriminator witness |
| Listener sandbox branch | divergent `listener-wispr-sandbox-01a0539e` `cd8d7e81` (parent `e4631269`); dedicated worktree dirty | Four uncommitted files: `Cargo.toml`, sandbox binary, `src/lib.rs`, `src/wispr.rs`; prototype diagnostics/checkpoint changes, not integrated |
| signal-listener | main `01fc1fd2` clean; branch `listener-wispr-01a04e75` `b44a9e7a` clean | Ordinary capture lifecycle contract is the same on both heads; no streaming-provider operation was added |
| meta-signal-listener | main `6112fd45` clean; branch `listener-wispr-01a04e75` `03306429` clean | Branch-only owner policy operation and provider identities |
| CriomOS-home | main `097a9bde` clean | Listener lock is `6905a4f1`; dictation service has no Wispr policy configuration |
| Wispr Home worktrees | overlay `6201c493`, integration `ac54e3af`, both clean | Desktop Wispr package overlay/private installer input only; both still lock Listener `6905a4f1` |
| wispr-flow-linux | main `003ccc28` clean | Unofficial packaged Wispr desktop app/helper; no Listener provider integration |

The Listener Wispr branch is a substantial branch-only change: `jj diff
--from main --to listener-wispr-01a04e75 --stat` reports 27 files changed,
5,001 insertions, and 371 deletions. Its branch history is a sequence of
provider-contract, observed-wire-codec, durable-policy/job/finalization,
segmentation, production-provider, secret-boundary, and actor-routing commits,
ending at `71a194df`. The edge branch grows the diff to 28 files, 7,957
insertions, and 370 deletions; this growth is not on main.

## Current main: actual transcription and credential path

Current Listener main has no `provider`, `provider_job`, `provider_policy`,
`provider_finalization`, `segmentation`, or `wispr` module. Runtime construction
in `src/runtime.rs` calls `OpenAiBatchTranscriptionActor::from_environment()`
and keeps that actor as its transcription dependency. Stop/retry therefore
transcribes through the direct OpenAI REST implementation.

`src/transcription.rs` establishes the current credential boundary:

* `OpenAiRestTranscriber::from_environment()` and its customization-archive
  constructor both set `OpenAiCredentialSource::gopass("openai/api-key")`.
* Each upload calls `OpenAiCredentialSource::resolve()`, which executes
  `gopass show -o openai/api-key`, trims the output, and rejects failure or an
  empty result. The value is then used as the HTTP bearer token.
* The production default endpoint is OpenAI's audio transcription endpoint and
  model `gpt-4o-transcribe`; `OpenAiCredentialSource::literal` is an explicit
  construction/test seam, not the default runtime path.
* No `OPENAI_API_KEY` environment lookup exists in this production path.

The current Listener Nix wrapper adds FFmpeg to the daemon `PATH`; the Home
dictation wrapper supplies capture, clipboard, and customization-archive
variables. The current Listener wrapper does not itself add `gopass` (the 0.17
branch does). Whether the running Home profile happens to obtain `gopass` from
another profile is not established here.

Home's `modules/home/profiles/min/dictation.nix` runs the locked Listener
package as `listener-daemon`, sets `LISTENER_CAPTURE_PROGRAM`,
`LISTENER_CLIPBOARD_PROGRAM`, and
`LISTENER_TRANSCRIPTION_CUSTOMIZATION_ARCHIVE`, and documents that production
transcription reads OpenAI credentials from gopass. It does not configure a
provider policy or any Wispr secret. The Home checks assert Listener version at
least `0.14.0` and reject legacy external transcriber variables, but do not
assert the 0.17 Wispr heads.

## 0.17 Wispr branch: implemented architecture, not integrated deployment

The branch changes `Cargo.toml` to `0.17.0`, pins
`meta-signal-listener` to its matching branch, pins `signal-listener` to
`b44a9e7a`, and adds the actor/runtime and Sema dependencies required by the
provider path. Its `flake.nix` daemon wrapper adds both FFmpeg and `gopass` to
`PATH`.

The provider layer in `src/provider.rs` is credential-free and typed:

* `ProviderIdentifier` is the closed pair `WisprFlow` / `OpenAi`, rendered as
  `wispr-flow` / `openai`.
* `ProviderPolicy::wispr_then_openai()` is the built-in order. Policies carry a
  generation and reject empty or duplicate provider identities.
* `TranscriptProvider` receives a `ProviderTranscriptRequest` naming the
  durable Listener artifact and optional sample range, context tail, and
  vocabulary. The router records typed redacted attempt states and falls back
  in policy order except for cancellation/local-artifact failures.
* Provider health is a local typed circuit-breaker/fanout projection; it does
  not carry response text, request IDs, artifact paths, or credentials.

`provider_job.rs` persists only session, artifact path, policy generation and
provider codes, redacted attempt state/sample ranges, segment transcripts,
assembled result, and history/delivery progress. It has no secret, request ID,
provider media, or credential field. `provider_policy.rs` owns the durable
`listener_transcription_provider_policy` Sema table and exposes the owner/meta
policy service. `provider_finalization.rs` stores segment attempts before the
assembled result and result before history/delivery projections.

`ListenerDaemon::run()` on this branch constructs the status/health fanout,
creates the runtime, explicitly calls
`runtime.use_wispr_then_openai_provider(production_wispr_provider(), ...)`,
opens the policy store, and serves the policy meta socket. Direct construction
of `ListenerRuntime` still starts with the OpenAI actor; the daemon's explicit
injection is what installs Wispr first and OpenAI second. The normal ordinary
`signal-listener` socket remains the capture lifecycle surface; provider policy
is owner-only meta traffic.

Raw recording logs are recovered as 16 kHz mono signed-16-bit PCM. The branch
plans roughly 330–350 second ranges, prefers a stable pause, retains one second
of seam overlap, and uses the same durable source for fallback. The Wispr
adapter enforces a 350-second maximum and builds a PCM16 WAV per range.

### Wispr credential boundary and stable names

The branch's `src/wispr.rs` has exactly these stable gopass entry identifiers:

* `openai/api-key` — existing OpenAI fallback, also used by the existing
  OpenAI actor;
* `wispr-flow/session` — opaque request-time Wispr session value;
* `wispr-flow/user-id` — non-public Wispr identity used in the observed Init
  message.

`GopassWisprSessionSource` and `GopassWisprWireIdentity` run
`gopass show -o <entry>` at request time. The session is kept only in an
in-memory boundary, cached for five minutes, and refreshed once after an
authentication-expired response. User/session values are not returned by
public provider APIs, serialized, logged, or placed in durable jobs. Request
and session IDs are generated per submission and likewise excluded from durable
state. These are source-level expectations; this audit intentionally did not
query the entries, so their existence and validity are unknown.

The matching meta consumer interface is branch-only:

* `meta-signal-listener/schema/lib.schema` adds
  `ConfigureTranscriptionProviders.TranscriptionProviderPolicy`;
* provider identities are `TranscriptionProviderId.[WisprFlow OpenAi]`;
* generated API accepts
  `Input::configure_transcription_providers(TranscriptionProviderIds::new(...))`;
* replies are `TranscriptionProvidersConfigured` with a monotonic generation,
  or typed rejection for `Empty`/`Duplicate`.

The ordinary `signal-listener` schema remains capture-oriented (`Start`,
`Stop`, `Cancel`, `Status`, `Retry`, etc.); there is no public streaming-audio
or transcript-stream operation. `meta-listener` accepts one typed policy input
and connects to `LISTENER_META_SOCKET` (defaulting beside the ordinary runtime
socket); the branch's daemon binds that socket mode from Listener
configuration.

### What “streaming” means in each head

On `71a194df`, the private wire codec targets
`/flow_api.v1.TranscriptionService/TranscribeStream` at
`inference.wisprflow.com`, builds gRPC-framed Init/context/audio messages, and
decodes response frames while discarding heartbeat frames. However,
`ReqwestWisprGrpcStreamingBoundary` uses a blocking `reqwest::Client`, first
concatenates all messages with `grpc_encode_messages`, sends one `.body(...).send()`
call, then reads the complete response bytes. There is no source-level
incremental request-frame send in this production constructor. Tests inject a
synthetic boundary and therefore do not prove live provider connectivity.

The later edge branch (`b97090f3`) adds
`NativeWisprGrpcStreamingBoundary`, Tokio TLS/ALPN/h2 setup, per-message body
sends, and half-close after Commit. Its source explicitly scopes this native
transport to the isolated sandbox witness. The witness binary consumes
inherited session/bundle descriptors and writes structural redacted diagnostics;
it does not create a Listener runtime, capture audio, route fallback, or return
a transcript. The edge/auth/sandbox heads are not in Home or Listener main.

## Verification performed

Using the repository-prescribed Nix entry point:

* Current Listener main: `nix develop -c cargo test --all-targets` exited 0.
  The observed run passed 10 library unit tests and all capture, command,
  configuration, history, recall, recording-log, runtime, and transcription
  integration tests (including 34 runtime tests and 9 transcription tests).
* Exact 0.17 branch source at the dedicated no-working-copy path:
  `nix develop -c cargo test --all-targets` exited 0. It passed the expanded
  provider, provider-health, provider-job, provider-notification,
  provider-policy, segmentation, runtime, and Wispr synthetic-wire tests in
  addition to the existing lifecycle suites.
* Clean edge branch worktree at `b97090f3`: the same command exited 0,
  including the native h2 loopback and sandbox witness tests. These are
  synthetic/offline tests; no live Wispr or OpenAI credential was used.

Passing tests establish build and fixture behavior for these source heads. They
do not establish that the current Home lock builds 0.17, that any gopass entry
exists, that a live Wispr session is authorized, or that the production
Reqwest path has been exercised against Wispr.

## Historical claims and unresolved questions

The branch's `README.md` describes the 0.17 provider policy as production
behavior, while `ARCHITECTURE.md` still describes the older internal OpenAI
actor as the first vertical slice. The latter is historical/stale relative to
the branch source; the current Listener `AGENTS.md` explicitly labels the
checkout legacy-wired and says it is not proof of correct-new adoption. Source
heads, lockfiles, and daemon wiring—not those prose claims—are the basis of the
integration conclusion above.

Unresolved without an explicit integration decision or live authorized
verification:

* whether `listener-wispr-01a04e75` and its two contract heads should be merged
  or merely used as a witness;
* whether Home should move its Listener lock from `6905a4f1` to the 0.17 head;
* whether Wispr gopass entries are provisioned and what their lifecycle/owner
  policy is (entry names are known; values were not read);
* whether “streaming” means the branch's gRPC-framed one-shot POST or the later
  native h2 sandbox path, and whether a live provider call is authorized;
* whether any external consumer needs a new ordinary Signal operation. The
  inspected source currently provides only lifecycle operations plus the
  owner-only provider policy operation.

## Sources

All source observations above were read from these local repositories/heads:

* `/git/github.com/LiGoldragon/listener`: `main` `6905a4f1` and
  `listener-wispr-01a04e75` `71a194df`; especially `src/transcription.rs`,
  `src/runtime.rs`, `src/daemon.rs`, `src/provider.rs`,
  `src/provider_policy.rs`, `src/provider_job.rs`,
  `src/provider_finalization.rs`, `src/wispr.rs`, `src/lib.rs`, `README.md`,
  `AGENTS.md`, `Cargo.toml`, `Cargo.lock`, and `flake.nix`.
* `/git/github.com/LiGoldragon/listener`: branch heads
  `listener-wispr-edge-proxy-01a05588` `b97090f3`,
  `listener-wispr-auth-discriminator-01a05588` `302aa698`, and divergent
  `listener-wispr-sandbox-01a0539e` `cd8d7e81`; corresponding dedicated
  worktrees under `/home/li/wt/github.com/LiGoldragon/listener/`.
* `/git/github.com/LiGoldragon/signal-listener`: `main` `01fc1fd2`, branch
  `listener-wispr-01a04e75` `b44a9e7a`, `schema/lib.schema`, `Cargo.toml`.
* `/git/github.com/LiGoldragon/meta-signal-listener`: `main` `6112fd45`,
  branch `listener-wispr-01a04e75` `03306429`, `schema/lib.schema`, generated
  `src/schema/lib.rs`, and `tests/round_trip.rs`.
* `/git/github.com/LiGoldragon/CriomOS-home`: `main` `097a9bde`,
  `flake.lock`, `flake.nix`, `modules/home/profiles/min/dictation.nix`,
  `modules/home/profiles/min/wispr-flow.nix`, and
  `checks/listener-dictation-bindings/default.nix`; dedicated Wispr worktrees
  at `6201c493` and `ac54e3af`.
* `/git/github.com/LiGoldragon/wispr-flow-linux`: `main` `003ccc28`, README
  and Nix packaging files.
* Read-only commands: `jj status`, `jj bookmark list`, `jj log`,
  `jj diff --stat`, targeted `rg`/file reads, and
  `nix develop -c cargo test --all-targets` in the current, exact-feature, and
  clean edge Listener worktrees.
