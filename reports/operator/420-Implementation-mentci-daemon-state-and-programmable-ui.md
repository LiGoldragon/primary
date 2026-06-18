# 420 — Mentci daemon state and programmable UI

## Frame

The psyche corrected the component name and expanded the design: **Mentci** is spelled `M-E-N-T-C-I`, and it is not just an egui panel. It is a state-bearing daemon whose clients are renderers and subscribers.

Spirit record `7x5z` now reflects that directly: Mentci is the psyche-facing criome approval component and a programmable user-interface daemon. The daemon owns canonical interface state; TUI, CLI, editor panes, status bars, popups, email surfaces, and agentic flows subscribe to that state and push responses back through it. Criome owns the key store and decrypt/sign path; Mentci presents and coordinates the user approval surface.

This implementation landed the shared state/subscription model in `mentci-lib` and repinned `mentci-egui` to consume it. It does not create the long-lived daemon binary yet.

## What Landed

### mentci-lib

Commit: `81e852b1` — `mentci-lib: add approval state subscriptions`

Files:

- `/git/github.com/LiGoldragon/mentci-lib/src/approval.rs`
- `/git/github.com/LiGoldragon/mentci-lib/src/cmd.rs`
- `/git/github.com/LiGoldragon/mentci-lib/src/event.rs`
- `/git/github.com/LiGoldragon/mentci-lib/src/state.rs`
- `/git/github.com/LiGoldragon/mentci-lib/tests/approval.rs`
- `/git/github.com/LiGoldragon/mentci-lib/INTENT.md`
- `/git/github.com/LiGoldragon/mentci-lib/ARCHITECTURE.md`

The approval model now has explicit daemon-style subscription nouns:

- `ApprovalClientIdentifier`
- `ApprovalSubscriptionIdentifier`
- `ApprovalInterest`
- `ApprovalSubscription`
- `ApprovalSubscriptionReceipt`
- `ApprovalUpdate`
- `ApprovalDelivery`
- `ApprovalAnswerOutcome`

`ApprovalState` now keeps subscription state and publishes updates when questions arrive, get selected, or are answered. The workbench emits commands that a future daemon can send to subscribed clients:

- `PublishApprovalUpdates`
- `ConfirmApprovalSubscription`
- `ConfirmApprovalUnsubscription`

The important shift is ownership: `mentci-lib` is now shaped as the reusable state machine a daemon hosts, not as a UI-local model that every client privately owns.

### mentci-egui

Commit: `b7c17fbb` — `mentci-egui: accept approval subscription commands`

Files:

- `/git/github.com/LiGoldragon/mentci-egui/src/app.rs`
- `/git/github.com/LiGoldragon/mentci-egui/INTENT.md`
- `/git/github.com/LiGoldragon/mentci-egui/Cargo.lock`

`mentci-egui` now consumes `mentci-lib` at `81e852b1` and is exhaustive over the new approval subscription commands. It currently treats daemon-facing publish/confirm commands as accepted no-ops, because the actual daemon/socket client is the next slice.

The repo intent now says the egui surface is one thin shell over the daemon-owned programmable UI model, not the owner of approval semantics.

## Tests

`mentci-lib`:

- `cargo fmt`
- `cargo test` — 8 approval tests passed.
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check --print-build-logs 'git+ssh://git@github.com/LiGoldragon/mentci-lib?ref=main'` — passed against the pushed remote main.

`mentci-egui`:

- `cargo fmt`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `nix flake check --print-build-logs 'git+ssh://git@github.com/LiGoldragon/mentci-egui?ref=main'` — passed against the pushed remote main.

I intentionally did not use local `path:/git/...` Nix inputs. `github:` refs hit the unauthenticated GitHub API rate limit, so the Nix checks use remote SSH Git refs instead.

## What This Enables

Mentci can now be implemented as a normal daemon around `mentci-lib`:

```text
criome escalation
  -> mentci-daemon receives approval question
  -> mentci-lib updates canonical daemon state
  -> subscribed clients receive pushed state updates
  -> psyche responds through TUI/CLI/editor/status surface
  -> mentci-daemon sends approval result back toward criome
```

The subscription model is deliberately push-shaped. A status bar client does not poll the approval queue; it subscribes and receives updates when the daemon state changes.

## Not Landed Yet

The next implementation slices are:

- create the actual `mentci` daemon/runtime crate, or decide whether `mentci-lib` grows the daemon binary before a separate runtime repo exists;
- define the daemon/client protocol, likely through `signal-mentci` and `meta-signal-mentci`;
- connect Mentci to criome's local socket for pending approval ingress and signed approval egress;
- add the login/decrypt-key test path, with criome owning key storage and Mentci presenting the user interaction;
- decide where canonical local socket locations live. The psyche floated `signal-standard`, but that was exploratory, so I did not capture or implement it as settled design.

One older maintenance gap remains outside this slice: the Spirit referent vocabulary still needs a proper canonical rename pass so old `Menchie` / `Menchi` references do not survive as active identifiers. The STT skill already maps those variants to `Mentci`.
