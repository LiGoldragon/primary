# Kameo upstream

As of 2026-08-22, the latest upstream tagged release is `v0.22.2` (GitHub tag/release 2026-07-18; changelog date 2026-07-17), while `main` is 2026-07-21 commit `b4aaee7`. The downstream fork’s `main` is an unreleased `0.20.0`-manifest branch at `3486e4f`; its common ancestor with upstream is `4d2e2d0` on 2026-06-19. The fork is therefore behind three released core minor lines (`0.21.0`, `0.21.1`, `0.22.0`), two patches (`0.22.1`, `0.22.2`), and the companion actors/console/macro releases. This is a repository/release fact, not a recommendation to rebase: the fork’s lifecycle work needs an explicit design decision.

## Release chronology after the divergence point

The release boundary is clear in upstream `CHANGELOG.md` and tags:

- `0.21.0`, 2026-06-21: breaking `SendError` error-chain support; live actor-system console TUI; lifecycle deadlock fixes and panic-safe shutdown; preservation of pending mailbox messages through stop/restart; and parent-supervision documentation.
- `0.21.1`, 2026-07-01: per-actor default async ask reply timeout through `PreparedActor`; a revised drain implementation; release-plz automation; and mailbox-test/CI reliability fixes.
- `0.22.0`, 2026-07-05: breaking `Context::pipe`/`pipe_with`; terminal `on_undelivered` hook; rejection of new messages after `stop_gracefully`; breaking pending-ask results during drain (`ActorRestarting` or `ActorNotRunning`); breaking single-`Arc` `ActorRef` clone representation; and delivery of leftover tells to `on_undelivered` when restart intensity is exhausted.
- `0.22.1`, 2026-07-07: hotpath dependency update.
- `0.22.2`, 2026-07-17: root/link correction for `actor.handle_message` tracing spans and documentation/API clarification that `ActorStopReason::Panicked` includes hook errors, with `PanicError::is_panic`.

Companion packages released in the same period are `kameo_actors` 0.6.0, 0.6.1, 0.7.0, 0.8.0, and 0.8.1; `kameo_console` 0.1.0 through 0.1.4; and `kameo_macros` 0.21.0 and 0.21.1. `kameo_actors` 0.8.0 is breaking because pool worker dispatch errors now expose `SendError<M, E>`, and 0.8.1 adds `FutureActor`, which runs one future in actor state, stops normally on successful output, and exposes an error output as supervised actor failure.

## Current actor lifecycle and supervision

The current 0.22.2 API still has one actor task per actor and a bounded mailbox by default. `Actor` is `Sized + Send + 'static`; `Args: Send`; and `Error: ReplyError`. Lifecycle hooks are `on_start`, `on_message`, `on_panic`, `on_link_died`, `on_stop`, `on_undelivered`, and `next`. The defaults stop on panic and on fatal link death, while a normal or supervisor-initiated linked stop continues.

Supervision is explicit parent/child linking through `Spawn::supervise`/`supervise_with`. `RestartPolicy` is `Permanent`, `Transient`, or `Never`; the default is permanent. `SupervisionStrategy` is `OneForOne`, `OneForAll`, or `RestForOne`; the default is `OneForOne`. The builder default restart budget is five restarts in five seconds.

The material lifecycle shape now visible in source is:

1. During child/sibling shutdown drain, tell messages are preserved for a restart; asks are returned to their callers with the original message wrapped as `ActorRestarting` if a restart is predicted, otherwise `ActorNotRunning`.
2. On terminal stop, leftover tell messages are drained into `Actor::on_undelivered`; asks are returned as `ActorNotRunning`. The hook runs before `on_stop` and is not called for restart-preserved messages or startup failure.
3. The child shares restart-intensity state with its supervisor so the child’s drain-time prediction tracks the supervisor’s terminal/restart decision. There is a narrow restart-window boundary race documented in the implementation: the prediction can conservatively send tells to `on_undelivered` even if the supervisor then restarts, but the opposite message-loss case is not expected.
4. `PreparedActor::reply_timeout` supplies a default only for async asks; a call-site `reply_timeout` overrides it, and blocking asks ignore the prepared default.

These semantics supersede the older 0.20-era “drain and drop” behavior. They are exactly the area where a downstream lifecycle fork can conflict, so no merge/rebase choice follows from upstream progress alone.

## Messaging and request/reply

Local refs expose typed `ask` (reply-bearing) and `tell` (fire-and-forget), plus `try_send`, mailbox timeouts, blocking forms, `enqueue`/pending replies, forwarding, delayed tells (`send_after`), and type-erased `Recipient`/`ReplyRecipient` forms. `Context` provides actor-ref access, reply channels, spawning, stop, forward, and `pipe`/`pipe_with`.

`SendError` now carries the original message in the drain/terminal cases, enabling a caller to retry `ActorRestarting` asks and to account for `ActorNotRunning` asks. The exact error type is a compatibility surface: 0.21.0’s `SendError` error-chain change and 0.22.0’s pending-ask drain change are marked breaking upstream.

Macros currently include `#[derive(Actor)]`, `#[derive(RemoteActor)]`, `#[derive(Reply)]`, `#[messages]`/`#[message]`, and `#[remote_message]`. The message macro creates message structs and `Message` impls from actor methods, preserves selected docs/derives, supports a context parameter, and rejects references, inferred types, and `impl Trait` in message fields. Upstream `main` has merged the `syn` 3.0.2 macro dependency update after v0.22.2, but the macro package is still version 0.21.1; there is no released macro 0.21.2 tag.

## Distributed actors: released shape versus open redesign

Released `0.22.2` keeps distributed actors inside the core crate behind the `remote` feature. The core remote module uses libp2p transports and a composable `remote::Behaviour`; mDNS convenience bootstrap is aimed at local development, while custom swarms can compose Kameo’s behavior with other libp2p behaviors. Actor registration/discovery uses Kademlia providers and metadata; `RemoteActorRef` supports `lookup`, `lookup_all`, `ask`, `tell`, and remote link/unlink. Wire-level remote messages are registered by `RemoteActor`/`RemoteMessage` traits and macros. Current request-response config defaults include ten-second request timeout, 100 concurrent streams, 1 MiB request limit, and 10 MiB response limit.

The open redesign is not part of any release or `main` ancestor:

- PR #373 (`feat/kameo-remote`) adds a separate `kameo_remote` 0.1.0 crate. It uses chitchat gossip for cluster membership/registry and plain TCP + MessagePack for messaging; registration is set-per-name; node-incarnation generation IDs prevent stale actor refs from reaching reused sequence IDs; pooled connections and per-sender/per-target workers provide FIFO ordering; tells are acknowledged on mailbox delivery with `send_unacked` as an escape hatch; and same-node dispatch bypasses TCP.
- PR #376 (`chore/remove-core-remote`) removes libp2p remote actors from the core crate and is explicitly breaking. This would turn the current core `remote` feature into a separate integration choice.
- PR #380 (`feat/kameo-remote-tls-auth`) adds optional rustls mutual TLS and a pre-shared cluster key, covering both gossip and messaging authentication/encryption. The proposed config warns that TLS without a cluster key leaves gossip unauthenticated. Its security choices are proposal-only and must not be treated as upstream guarantees.

The upstream maintainer’s own distributed-actors discussion says there is no built-in centralized broker or failover takeover model, and that the existing libp2p swarm model leaves application-specific fault tolerance and discovery choices open. That is a useful open-direction signal, not a release contract.

## Toolchain and maintenance state

The released/current core package is edition 2024 with MSRV 1.88.0; macros declare MSRV 1.85.1. Current source has four workspace packages (`kameo`, `kameo_actors`, `kameo_console`, `kameo_macros`), default `macros` + `tracing`, and optional `remote`, `otel`, `metrics`, and `hotpath` features. The `main` branch has release-plz automation and a release candidate branch, but no release tag beyond v0.22.2.

As of the review date, GitHub shows active open work rather than abandonment: PR #396 relaxes `Send + 'static` bounds on messages to permit reference-bearing messages; #394 releases terminal child ownership; #387 serializes supervised restarts; #386 is the pending 0.22.3/companion-package release; #395/#389/#388 are dependency updates; and #373/#376/#380 are the remote redesign/security sequence. These are open proposals, not compatible upstream behavior. In particular, #396 would challenge the current `Actor: Send + 'static`/message-send assumptions and needs explicit compatibility review before downstream adoption.

## Downstream decision surface

What is established:

- The fork is materially behind released upstream and has an unreleased lifecycle branch against the 0.20-era API.
- Upstream has invested in lifecycle result correctness, drain accounting, supervision strategies, actor observability, and request/reply timeout ergonomics.
- Core remote actors are still the released libp2p/Kademlia/request-response design; the chitchat/TCP/generation-ID/mTLS design is open work.

What remains unresolved and should be returned to the caller before any material change:

- Whether the fork’s lifecycle semantics are intended to replace upstream’s 0.21/0.22 drain, restart-budget, `on_undelivered`, and ask-error contracts, or should be redesigned around them.
- Whether the downstream architecture wants released libp2p remote actors, the open `kameo_remote` direction, or a distinct design; neither the open branch nor its TLS posture is authority.
- Whether the downstream message model can accept the current `Send + 'static` bounds, or wants to evaluate open PR #396 separately; removing those bounds is a compatibility/security design decision, not a routine update.
- Whether adoption targets released v0.22.2, unreleased `main` (with `syn` 3.0.2), or the unmerged 0.22.3 release candidate.

## Sources

Primary repository and release sources:

- https://github.com/tqwewe/kameo
- https://github.com/tqwewe/kameo/blob/main/CHANGELOG.md
- https://github.com/tqwewe/kameo/releases
- https://github.com/tqwewe/kameo/releases/tag/v0.22.2
- https://github.com/tqwewe/kameo/blob/main/Cargo.toml
- https://github.com/tqwewe/kameo/blob/main/src/actor.rs
- https://github.com/tqwewe/kameo/blob/main/src/actor/spawn.rs
- https://github.com/tqwewe/kameo/blob/main/src/actor/actor_ref.rs
- https://github.com/tqwewe/kameo/blob/main/src/links.rs
- https://github.com/tqwewe/kameo/blob/main/src/request/ask.rs
- https://github.com/tqwewe/kameo/blob/main/src/request/tell.rs
- https://github.com/tqwewe/kameo/blob/main/src/supervision.rs
- https://github.com/tqwewe/kameo/blob/main/src/remote.rs
- https://github.com/tqwewe/kameo/blob/main/src/remote/messaging.rs
- https://github.com/tqwewe/kameo/blob/main/src/remote/registry.rs
- https://github.com/tqwewe/kameo/blob/main/macros/src/lib.rs
- https://github.com/tqwewe/kameo/blob/main/actors/src/future.rs
- https://github.com/tqwewe/kameo/blob/main/actors/CHANGELOG.md
- https://github.com/tqwewe/kameo/blob/main/console/CHANGELOG.md

Current and proposed upstream history:

- https://github.com/tqwewe/kameo/commit/4d2e2d02cc1ba59f05123d79f73eb47dd819ef92
- https://github.com/tqwewe/kameo/commit/b4aaee797cc3fd12e8194db406d9d73a6bc021ce
- https://github.com/tqwewe/kameo/commit/ae17f01270c5d578ebc404749a91792d774da42a
- https://github.com/tqwewe/kameo/commit/bddbbf015eec2392947778cceed216cb5889c2f6
- https://github.com/tqwewe/kameo/commit/0750d5a731669f6d473c441afc79fc7835f7a954
- https://github.com/tqwewe/kameo/commit/4d897f2c5418fd0b297bd3fbfe49f174c382b3d
- https://github.com/tqwewe/kameo/commit/4e0594abbb550ccb679e9c696d2393a4907184fb
- https://github.com/tqwewe/kameo/commit/e8a0bce041af295eb3c013be08b5282fda4d9b7b
- https://github.com/tqwewe/kameo/commit/c1c14b95f0efe41c532345438802c19cc9d8d19c
- https://github.com/tqwewe/kameo/commit/77feb7a5e5c1ab2cfde9ab20242af5c0ea71d0c3
- https://github.com/tqwewe/kameo/commit/39018860114723a86c705b37c62ae3d3c0511426
- https://github.com/tqwewe/kameo/commit/ceb672e2bb076fb32fbe7212d1d9b2d9ae327ea2
- https://github.com/tqwewe/kameo/commit/1c66bf9d16f80cd374283616fdbbebd49a4df61b
- https://github.com/tqwewe/kameo/commit/90138758779d2260798c41cfaa47598db84f05b8
- https://github.com/tqwewe/kameo/pull/373
- https://github.com/tqwewe/kameo/pull/376
- https://github.com/tqwewe/kameo/pull/380
- https://github.com/tqwewe/kameo/pull/387
- https://github.com/tqwewe/kameo/pull/394
- https://github.com/tqwewe/kameo/pull/396
- https://github.com/tqwewe/kameo/pull/386
- https://github.com/tqwewe/kameo/commits/feat/kameo-remote
- https://github.com/tqwewe/kameo/commits/feat/kameo-remote-tls-auth
- https://github.com/tqwewe/kameo/discussions/262

Witness for local ref comparison and own inference: `flows/cc4105a6/witnesses/upstreamState.md`.
