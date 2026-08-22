# Upstream state

Observed 2026-08-22 from the local authoritative clones after a read-only fetch.

Method: probe `git -C /git/github.com/tqwewe/kameo fetch --tags --prune origin`

- `origin/main` is `b4aaee797cc3fd12e8194db406d9d73a6bc021ce`, committed 2026-07-21, `chore(deps): update syn requirement from 2.0.52 to 3.0.2 (#383)`.
- Latest fetched release tags are `v0.22.2` (main crate), `actors-v0.8.1`, `console-v0.1.4`, and `macros-v0.21.1`, all pointing to the 2026-07-17 release commit `9013875` or the corresponding package release commits.
- Active upstream branches include `dependabot/cargo/hotpath-0.23` (2026-08-10), `dependabot/cargo/opentelemetry-0.32` and `dependabot/cargo/tracing-opentelemetry-0.33` (2026-07-27), `release-plz-2026-07-21T06-17-56Z` (release candidate), `feat/kameo-remote-tls-auth`, and `chore/remove-core-remote`.

Method: probe `git -C /git/github.com/LiGoldragon/kameo merge-base main upstream/main; git log; git diff`

- Fork `main` is `3486e4f63ea4e87123476cfbdefeb12403540306`, committed 2026-06-19, `docs: mark Protos estate status`.
- The fork/upstream merge base is `4d2e2d02cc1ba59f05123d79f73eb47dd819ef92`, committed 2026-06-19, `chore: use libp2p::identity instead of libp2p_identity directly (#339)`.
- Fork `main` has six commits after that base, including four lifecycle commits from 2026-05-16 (`publish terminal lifecycle outcomes`, `split lifecycle control mailbox`, `cover lifecycle control edge cases`, `gate weak shutdown result helpers`) and a 2026-06-19 rebase fix. The fork package manifest remains `kameo` 0.20.0 with `kameo_macros` 0.20.0 and no `console` workspace member.
- Upstream `main` has 49 commits after the base; `git diff --stat` reports 65 files, 8,015 insertions, and 718 deletions. This includes the released 0.21/0.22 work plus console, CI/release automation, and post-release dependency changes.

Method: code read `/git/github.com/tqwewe/kameo:origin/main:Cargo.toml`, `actors/Cargo.toml`, `macros/Cargo.toml`, `src/actor.rs`, `src/actor/actor_ref.rs`, `src/actor/spawn.rs`, `src/links.rs`, `src/mailbox.rs`, `src/request/ask.rs`, `src/request/tell.rs`, `src/supervision.rs`, `src/remote.rs`, `src/remote/messaging.rs`, `src/remote/registry.rs`, `macros/src/lib.rs`, and `actors/src/future.rs`

- Core `kameo` is 0.22.2, edition 2024, MSRV `rust-version = "1.88.0"`; default features are `macros` and `tracing`. Its current workspace members are `.`, `actors`, `console`, and `macros`. `kameo_macros` is 0.21.1 and declares MSRV 1.85.1. The current main source already requires `syn = "3.0.2"` in the macro crate, but the 0.22.2 release tag used the prior macro version.
- Core features remain `macros`, `remote`, `tracing`, `otel`, `metrics`, and `hotpath`; released remote support is still a core feature using libp2p transports, Kademlia registry, and request-response messaging.
- `Actor` remains `Sized + Send + 'static`, with `Args: Send`, `Error: ReplyError`, lifecycle hooks `on_start`, `on_message`, `on_panic`, `on_link_died`, `on_stop`, `on_undelivered`, and `next`; default `on_panic` breaks with `ActorStopReason::Panicked` and default `on_link_died` breaks for killed/panicked/link-dead reasons.
- Current supervision exports `RestartPolicy::{Permanent,Transient,Never}` and `SupervisionStrategy::{OneForOne,OneForAll,RestForOne}`. The builder default is five restarts per five seconds. Child restart intensity is shared with the child so drain-time classification can distinguish a real restart from terminal stop.
- Current lifecycle drain preserves tell signals for a restart, returns pending asks with `SendError::ActorRestarting` when a restart is expected and `ActorNotRunning` on terminal stop, and calls `Actor::on_undelivered` for leftover tells only on terminal stop. `stop_gracefully` rejects new messages after shutdown begins. `PreparedActor::reply_timeout` supplies a per-actor async ask default; a call-site timeout overrides it, while blocking asks ignore it.
- Current `ActorRef` exposes strong/weak refs, startup/shutdown result accessors and waiters, link/unlink, typed and erased recipients, delayed tells (`TellRequest::send_after`), `Context::pipe`/`pipe_with`, and remote refs. `RemoteActorRef` supports `lookup`, `lookup_all`, `ask`, `tell`, and remote linking.
- Current macros provide `#[derive(Actor)]`, `#[derive(RemoteActor)]`, `#[derive(Reply)]`, `#[messages]` with `#[message]` methods, and `#[remote_message]` registration. The `#[messages]` parser rejects references, inferred types, and `impl Trait` message parameters and generates message structs plus `Message` impls.
- `kameo_actors` 0.8.1 adds `FutureActor`; a future runs on the actor task, normal output stops normally, and an error output becomes an actor panic visible to supervision. Pool worker dispatch errors now expose `SendError` (a breaking change in actors 0.8.0).

Method: code read `/git/github.com/tqwewe/kameo:origin/feat/kameo-remote:remote/{Cargo.toml,src/lib.rs,src/node.rs,src/remote_actor.rs,src/remote_ref.rs,src/registry.rs,src/messaging/protocol.rs,src/messaging/transport.rs}`

- The unmerged `kameo_remote` proposal is a separate 0.1.0 crate (`rust-version = "1.88.0"`) built on chitchat gossip and plain TCP/MessagePack, with `RemoteNode`, `RemoteNodeConfig`, `RemoteActor`, `RemoteMessage`, `RemoteMessages`, and typed `RemoteActorRef`.
- The proposal uses generation-checked node/actor IDs, gossip-backed set-per-name registration, `lookup_all`/watch, pooled connections, per-sender/per-target FIFO workers, acked tells plus `send_unacked`, and local dispatch fast paths.
- The TLS branch adds optional rustls mutual TLS and a pre-shared cluster key for gossip and messaging authentication/encryption. It explicitly warns that TLS without a cluster key leaves gossip unauthenticated. Neither branch is an upstream `main` ancestor.

Method: probe `git -C /git/github.com/tqwewe/kameo log --reverse --format='%h %ad %s' --date=short 4d2e2d0..origin/main` and code read `origin/main:CHANGELOG.md`

Released chronology after fork base:

- 0.21.0 (2026-06-21): `SendError` chains (breaking), live console TUI, lifecycle deadlock/panic fixes, preservation of pending mailbox messages across stop/restart, and parent-supervision documentation.
- 0.21.1 (2026-07-01): per-actor default reply timeout, revised drain handling, release-plz automation, and test/CI robustness fixes.
- 0.22.0 (2026-07-05): `ctx.pipe`/`pipe_with` (breaking), `on_undelivered`, reject messages after `stop_gracefully`, pending ask errors during drain (breaking), single-`Arc` `ActorRef` cloning (breaking), and leftover-tell delivery when restart budget is exhausted.
- 0.22.1 (2026-07-07): hotpath update.
- 0.22.2 (2026-07-17): tracing span root/link fix and panic-hook documentation/API clarification (`PanicError::is_panic`).
- Companion releases: `kameo_actors` 0.6.0/0.6.1/0.7.0/0.8.0/0.8.1; `kameo_console` 0.1.0 through 0.1.4; `kameo_macros` 0.21.0 and 0.21.1.

Merged to `origin/main` but not released:

- 2026-07-20 commits are titled dependency updates for `opentelemetry` 0.32 and `tracing-opentelemetry` 0.33, but both have the same tree as their parent; the current declared source requirements remain `opentelemetry = "0.31"` and `tracing-opentelemetry = "0.32"`. Treat their effective dependency change as unknown, not as an observed source update.
- 2026-07-21 `syn` 3.0.2 update in the macro crate is an observed source change; `macros/Cargo.toml` is still version 0.21.1.

Proposed or open, not merged as of 2026-08-22:

- PR #386 release-plz candidate proposes 0.22.3, actors 0.8.2, console 0.1.5, and macros 0.21.2; no release tag was fetched beyond v0.22.2.
- PR #373/#376/#380 are the distributed-actor redesign and security sequence; their branch tips are not ancestors of `origin/main`.
- PR #387 serializes supervised restarts; PR #394 releases terminal child ownership; PR #396 removes `Send + 'static` bounds from `Message` to permit reference-bearing messages. These remain open; no compatibility decision should be inferred from them.
