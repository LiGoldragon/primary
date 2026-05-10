# 99. Kameo adoption and code-quality audit

## 1. Bottom line

Kameo is active, gaining attention quickly for a Rust actor runtime, and
has a coherent local actor core. It is not abandoned, not obscure in the
"nobody noticed it" sense, and not a toy from the visible source shape.

It is also younger and less broadly adopted than `ractor`, with a
single-maintainer center of gravity and several code-quality risks that
matter to PersonaMind. I would not call it a conservative
production-ready replacement for the central PersonaMind runtime today.
I would call it good enough for a deliberate local-runtime spike.

The distinction matters:

- **Local in-process actors:** plausible candidate. The actor-as-state
  model fits our no-ZST actor rule better than `ractor`.
- **Remote/distributed actors:** not ready for PersonaMind's core path
  without a separate hardening pass.
- **`kameo_actors` helper crate:** do not start there. Its public value
  shapes are looser than the core crate and weaker than our Rust
  discipline.

No intermediate `persona-actor`, `workspace-actor`, or other imagined
actor library is involved in this report. The comparison is direct
`ractor` versus direct Kameo.

## 2. Fresh adoption snapshot

Date checked: 2026-05-10.

Kameo source:

- Repository: `tqwewe/kameo`
- Local clone: `/git/github.com/tqwewe/kameo`
- Checked commit: `1d498c0 chore(deps): update hotpath requirement
  from 0.11 to 0.15 (#324)`
- Repository created: 2024-03-29
- Last GitHub push observed: 2026-04-27
- Stars: 1,296
- Forks: 69
- Watchers: 14
- crates.io downloads: 247,952
- crates.io recent downloads: 109,144
- crates.io versions: 33
- Current crate version: 0.20.0, published 2026-04-07
- crates.io reverse dependency entries: 20
- Open issues: 7
- Open PRs: 2

For scale, `ractor` at the same check:

- Repository: `slawlor/ractor`
- Repository created: 2023-01-03
- Last GitHub push observed: 2026-05-07
- Stars: 2,011
- Forks: 125
- Watchers: 31
- crates.io downloads: 655,842
- crates.io recent downloads: 199,443
- crates.io versions: 75
- Current crate version: 0.15.13, published 2026-05-05
- crates.io reverse dependency entries: 31

Conclusion: Kameo is popular enough to take seriously and appears to be
gaining attention quickly, especially given that it is about a year
younger than `ractor`. It is not yet as established as `ractor`.

The contributor graph is concentrated. `git shortlog -sn --all` shows
Ari Seyhun with 399 commits, Dependabot with 13, and the next human
contributors at 5, 3, and 3 commits. That is normal for a young Rust
crate, but it is a real dependency risk for foundational infrastructure.

## 3. Release and maintenance signal

Recent release cadence is healthy:

- `v0.20.0`: 2026-04-07
- `v0.19.2`: 2025-11-17
- `v0.19.0`: 2025-11-10
- `v0.18.0`: 2025-09-11
- `v0.17.2`: 2025-06-26
- `v0.17.1`: 2025-06-24
- `v0.17.0`: 2025-06-22
- `v0.16.0`: 2025-03-28
- `v0.15.0`: 2025-03-13
- `v0.14.0`: 2025-01-16

The project is still moving quickly. That is good for attention and bad
for API stability. The current `Cargo.toml` uses edition 2024 and
`rust-version = "1.88.0"`, so it assumes a modern toolchain.

Open issues are not numerous, but the shape of the open bugs matters:

- #306: forwarded reply downcast panic through multi-hop forwarding.
- #307: forwarding to a stopped actor can panic due to signal downcast.
- #213: remote lookup results inconsistent between peers.

Those are not cosmetic issues. They sit near typed reply safety and
remote/distributed behavior.

## 4. What looks strong in the code

The core actor model is conceptually good for PersonaMind:

- `Actor` is implemented by the data-bearing actor type itself.
- `Actor::on_start` returns `Self`, not a separate framework `State`.
- `Message<T> for ActorType` handlers take `&mut self`.
- `ActorRef<ActorType>` is typed by actor, not by an untyped mailbox.
- `AskRequest` / `TellRequest` are `#[must_use]`.
- Bounded mailbox sends apply async backpressure.
- Supervision has named restart policies and strategies.

That gives Kameo a real semantic advantage over `ractor` for the hard
no-ZST actor rule. With `ractor`, the framework naturally splits a ZST
actor marker from its `State`. With Kameo, the runtime actor can be the
state-bearing noun directly.

The repository also has a serious CI/test/doc skeleton:

- Rustdoc warnings are denied from `src/lib.rs`.
- Core tests cover request, reply, actor id, and supervision paths.
- CI runs format, clippy, tests, and docs.
- Dependencies are modular: defaults are `macros` and `tracing`; the
  large `remote`, `metrics`, `otel`, and `hotpath` surfaces are optional.

Local verification:

- `cargo test --workspace --all-features` compiled the workspace and
  core unit tests passed: 50 passed, 0 failed.
- `cargo test --workspace --all-features --doc` passed: core doctests
  77 passed and 5 ignored, `kameo_actors` doctests 9 passed, and
  `kameo_macros` doctests 6 ignored.

## 5. Code-quality concerns

### 5.1 Typed surface leaks dynamic machinery

Kameo presents a typed API, but lower-level dynamic pieces are public
enough to bypass the intended path:

- `MailboxSender::send` and `MailboxReceiver::recv` expose public
  `Signal<A>` values.
- `Signal::Message` carries `BoxMessage`, `ActorRef`,
  `Option<BoxReplySender>`, and a `sent_within_actor` flag.
- `Actor::on_message` is an overridable public hook that accepts raw
  `BoxMessage`, `Option<BoxReplySender>`, and `&mut bool`.

This does not mean ordinary Kameo code is bad. It means the type safety
story depends on users staying on the high-level `ActorRef::ask` /
`ActorRef::tell` path. For PersonaMind, our architecture tests should
forbid direct mailbox/signal use in component code.

### 5.2 Reply delivery relies on downcast conventions

The reply system uses type erasure internally. There are several
unchecked `downcast(...).unwrap()` paths in reply and error conversion
code. Two open Kameo bugs are already about forwarding/downcast panics.

This is manageable for ordinary local ask/tell usage, but it is a
reason not to treat advanced forwarding as a free primitive in
PersonaMind until we have weird tests around it.

### 5.3 Detached work is first-class

`Context::spawn` uses `tokio::spawn` and documents that the task can
outlive the actor and does not trigger the actor's `on_panic`.
`ActorRef::attach_stream` also starts independent work. The
`kameo_actors` crate has spawned delivery modes.

That conflicts with our actor-heavy discipline unless we ban those
surface areas in application code. PersonaMind wants failure ownership
and lifecycle ownership to remain visible in the actor tree.

### 5.4 Remote/distributed path has sharper edges

The remote feature is where I would draw the strongest line:

- Remote registry parsing can slice malformed network bytes before
  validating length.
- Remote send failure can be logged and discarded or escalate to panic.
- Remote behavior command polling can leave queued control commands
  waiting for an unrelated wake.
- Remote helpers contain bootstrap/registration panics.
- Open issue #213 reports inconsistent peer lookup behavior.

This is not a blocker for a local actor spike. It is a blocker for using
Kameo remote actors as PersonaMind's distributed substrate today.

### 5.5 Supervision and shutdown semantics need care

The source audit found lifecycle edge cases:

- Coordinated `OneForAll` / `RestForOne` restart paths can call sibling
  factories directly, apparently bypassing `RestartPolicy::Never`.
- `wait_for_shutdown()` waits for mailbox closure, while
  `wait_for_shutdown_result()` is the stronger barrier after cleanup.
- The documented startup message ordering guarantee can break when a
  bounded mailbox is full and `StartupFinished` is sent with `try_send`.

PersonaMind should use the stronger shutdown barrier and test restart
policy behavior explicitly if we spike Kameo.

### 5.6 CI and docs are good, but not complete

One audit lane found that the CI feature matrix likely does not exercise
the intended cross-product: `toolchain` is the real axis, while
package/features entries are listed through `include`. Workspace
all-features checks still run, but isolated feature coverage is weaker
than it looks.

There is no `tests/` integration suite, no tests in `actors/`, and no
proc-macro UI/trybuild tests despite exported macros. The docs are
broad, but MDX examples are not validated by CI and at least one remote
configuration page appears to mention method names that no longer match
the source.

The release scripts are manual and use `--allow-dirty`; the changelog
has small hygiene issues. These are maturity signals, not immediate
technical blockers.

## 6. Fit against our Rust discipline

Kameo is closer to our desired actor shape than `ractor` in one
important way: behavior belongs to a data-bearing noun. A
`StoreSupervisorActor { memory: MemoryState }` with
`impl Message<ApplyMemory> for StoreSupervisorActor` is more aligned
with our naming and actor discipline than a `StoreSupervisor` marker plus
separate `State`.

But the Kameo examples and affordances are not our discipline by
default. Kameo still permits:

- ZST actors in examples.
- abbreviated names such as `ctx` and `msg`;
- direct mailbox/signal access;
- `blocking_send`;
- unbounded mailboxes;
- detached tasks through `Context::spawn`;
- public DTO-style generated message structs through `#[messages]`;
- broad primitive public fields in `kameo_actors`.

If PersonaMind spikes Kameo, the local rules should be strict:

- use `kameo` core only, not `kameo_actors` initially;
- keep `remote` disabled;
- require long-lived actors to have fields;
- ban direct `Signal`, `MailboxSender`, and `MailboxReceiver` usage in
  component code;
- ban `Context::spawn`, `ActorRef::attach_stream`, `blocking_send`, and
  unbounded mailboxes unless a report grants an exception;
- avoid `#[messages]` for public component APIs until macro output has
  trybuild coverage;
- use full names: `context`, `message`, `actor_reference`, not `ctx`,
  `msg`, or `myself`;
- test ask/tell reply behavior, shutdown barriers, and supervision
  restart policies under pressure.

## 7. Production-readiness judgment

My answer to the user's questions:

- **How actively used is it?** Active enough to care about. It has
  regular releases, recent commits, real crates.io traffic, and some
  reverse dependencies.
- **Is it production-ready?** For local actors, it is plausible but not
  conservative. For remote/distributed actors, no, not for PersonaMind's
  core without hardening.
- **Is it popular?** It is popular for a young Rust actor crate, but
  less popular than `ractor` on stars, downloads, reverse dependencies,
  and breadth of contributors.
- **Is it gaining attention quickly?** Yes. The ratio of recent downloads
  to total downloads is high, and the repository has 1,296 stars less
  than twenty-six months after creation.

The best next move is not a full runtime switch. The best next move is a
small Kameo branch or test component inside `persona-mind` that rewrites
one real actor path, probably the store path, with these constraints:

1. local `kameo` only;
2. no remote feature;
3. no `kameo_actors`;
4. no direct mailbox/signal APIs;
5. no detached tasks;
6. no ZST runtime actors;
7. weird tests for backpressure, shutdown, restart, and reply typing.

If that spike feels cleaner and the tests expose no fatal runtime
friction, then Kameo becomes a serious candidate. Until then, direct
`ractor` remains the lower-risk implemented baseline.

## 8. Sources

Workspace reports:

- `reports/designer/102-kameo-deep-dive.md` - Kameo API survey.
- `reports/designer-assistant/4-kameo-ractor-no-zst-switch-assessment.md`
  - no-ZST switch assessment.
- `reports/operator/103-actor-abstraction-drift-correction.md` -
  correction against imagined actor abstraction names.
- `reports/operator-assistant/98-kameo-persona-mind-code-shape.md` -
  code-shaped PersonaMind Kameo sketch.

Primary project sources:

- `https://github.com/tqwewe/kameo`
- `https://crates.io/crates/kameo`
- `https://github.com/slawlor/ractor`
- `https://crates.io/crates/ractor`
- `/git/github.com/tqwewe/kameo/Cargo.toml`
- `/git/github.com/tqwewe/kameo/src/actor.rs`
- `/git/github.com/tqwewe/kameo/src/message.rs`
- `/git/github.com/tqwewe/kameo/src/mailbox.rs`
- `/git/github.com/tqwewe/kameo/src/reply.rs`
- `/git/github.com/tqwewe/kameo/src/error.rs`
- `/git/github.com/tqwewe/kameo/src/request/ask.rs`
- `/git/github.com/tqwewe/kameo/src/request/tell.rs`
- `/git/github.com/tqwewe/kameo/src/supervision.rs`
- `/git/github.com/tqwewe/kameo/src/remote/`
- `/git/github.com/tqwewe/kameo/actors/`
- `/git/github.com/tqwewe/kameo/macros/`
- `/git/github.com/tqwewe/kameo/.github/workflows/ci.yml`

Queries used:

- `gh repo view tqwewe/kameo`
- `gh api repos/tqwewe/kameo/releases`
- `gh api repos/tqwewe/kameo/issues`
- `gh api repos/tqwewe/kameo/pulls`
- `curl https://crates.io/api/v1/crates/kameo`
- `curl https://crates.io/api/v1/crates/kameo/reverse_dependencies`
- equivalent `gh` and crates.io queries for `slawlor/ractor`.
