# mentci-lib — repository history and re-founding decision

Psyche question: *"what is the history of this repo?"* — and, given that
history, whether to re-found mentci-lib on the live contracts, adopt its
existing model, or leave it.

## Direct answer

mentci-lib is the **original Mentci design, built ~50 days before the
daemon and contract existed, on a protocol stack that has since been
replaced**. It was never forked or abandoned in the usual sense — it was
*overtaken*. The daemon (`mentci`) and the contract (`signal-mentci`)
were both founded on 2026-06-18 and built differently, on `signal-frame`
streaming frames and a daemon-owned `signal-mentci` typed vocabulary,
while mentci-lib still sits on the old generic `signal` crate's
`Graph`/`Node`/`Edge` graph-signal vocabulary and a hand-rolled
`Body::Request(Request::Handshake)` / `DaemonRole::Criome|Nexus` wire
that no live daemon speaks.

The recent operator commits (Jun 18-19: approval flow model, approval
state subscriptions, edited-answers-as-proposals, component-triad
boundary) are real development — but they grew a **second, duplicate
approval vocabulary inside the dead skeleton**, in parallel with the
`signal-mentci` contract the daemon already ships. So the tension
"developed but not consumed" resolves cleanly: it is being developed *on
the wrong foundation*, and its one consumer (mentci-egui) has explicitly
walked away from it.

**Recommendation: re-found mentci-lib on the live contracts.** Keep the
design ideas (the MVU shape, the proposal model, the approval state
machine); discard the entire `signal`-crate transport, graph vocabulary,
and the duplicate approval *types*. This is the right call precisely
*because* of the history: mentci-lib was the design lab where the Mentci
shape was invented, and that shape won — it is now reified in
`signal-mentci`. The library should be rebuilt to drive that contract,
not to keep maintaining a private fork of it.

## The arc of evolution

The whole timeline fits in one frame:

| Date | Event |
|---|---|
| 2026-04-29 | mentci-lib created — full typed skeleton (initial scaffold, `5c1c7fa`) |
| 2026-04-29 (same day) | runnable workbench, tokio UDS driver, handshake exchange against a live **criome** daemon, auto-query, auto-subscribe, first constructor flow, records-on-canvas — 10 commits in ~5 hours |
| 2026-04-30 | `Slot<T>` phantom-type migration tracking the `signal` crate upstream |
| 2026-05-01 → 06-05 | docs-only churn (AGENTS/ARCH cleanup, INTENT.md added) |
| **2026-06-18** | **`mentci` daemon AND `signal-mentci` contract both created — the real component triad, on a different stack** |
| 2026-06-18 → 06-19 | operator adds approval flow / subscriptions / proposals / triad-boundary docs **to mentci-lib** — but still on the old `signal` stack |
| 2026-06-19 | flake repins (build infra only) |

mentci-lib's substantive code is essentially frozen at the 2026-04-30
`Slot<T>` migration; everything after is docs until the June approval
work, which bolted a new module onto the frozen body.

### What mentci-lib embodied originally

The 2026-04-29 scaffold commit is an unusually complete design
statement. It declared the **MVU contract** — five typed shapes
`WorkbenchState` / `WorkbenchView` / `UserEvent` / `EngineEvent` / `Cmd`
with `update(state,event)→(state, Vec<Cmd>)` and `view(state)→View` —
plus a per-kind canvas renderer system, a constructor-flow state machine
(new-node / new-edge / rename / retract / batch), a schema-source
abstraction, and a **dual-daemon model: criome for state + a
"nexus-daemon" for rendering**, hidden from widget code behind one engine
surface. This is the design that the current `signal-mentci` +
`mentci` + `mentci-egui` triad is a *realization of* — minus the
nexus-daemon, which the live stack dropped entirely (it survives only as
a *daemon-local schema name* in `mentci/INTENT.md`, never as a second
socket).

### When and why it diverged

The divergence is not a single bad commit — it is the **founding of the
daemon and contract on 2026-06-18 on a different transport**, leaving
mentci-lib stranded on the old one. Concretely:

- **Transport.** mentci-lib's driver
  (`src/connection/driver.rs`) imports from the generic `signal` crate
  and speaks `Frame { body: Body::Request(Request::Handshake(
  HandshakeRequest{...})) }`, awaiting `Reply::HandshakeAccepted`, with a
  `DaemonRole::Criome | Nexus` switch. The daemon
  (`mentci/src/client.rs`) speaks `signal_frame::StreamingFrame<Input,
  Output, MentciEvent>` with `ExchangeIdentifier` / `ExchangeLane` /
  `LaneSequence` / `SessionEpoch`. **No live daemon answers the handshake
  mentci-lib sends.**

- **Vocabulary.** mentci-lib's model (`src/state.rs`) is built on
  `signal::{Graph, Node, Edge, GraphQuery, NodeQuery, EdgeQuery,
  QueryOperation, ...}` — a generic graph-signal data model. The live
  contract (`signal-mentci/src/schema/lib.rs`) has no graph vocabulary at
  all; its nouns are `ApprovalQuestion`, `QuestionProposal`,
  `AnswerProposal`, `InterfaceState`, `PaneContent`,
  `InterfaceProjection`, etc. — a programmable-UI / approval vocabulary.

- **Duplicate approval types.** The June work added `src/approval.rs`
  (`ApprovalQuestion`, `ApprovalSource`, `AnswerProposal`,
  `ApprovalDecision`, `ApprovalSubscription`, `ApprovalUpdate`, ...).
  Every one of these **already exists in `signal-mentci`** as a
  schema-emitted type (`ApprovalQuestion`, `ApprovalSource`,
  `AnswerProposal`, `ApprovalDecision`, `ApprovalVerdict`,
  `QuestionProposal`, `InterfaceInterest`, ...) and is what the daemon's
  `state.rs` actually uses. mentci-lib's are a hand-rolled, structurally
  parallel re-implementation — the "DUPLICATE hand-rolled approval
  vocabulary" wave-1 flagged.

## The decisive fact: the consumer left

mentci-lib exists to be consumed by shells, chiefly mentci-egui. As of
2026-06-20, **mentci-egui depends on `signal-mentci` directly and does
not depend on mentci-lib at all** (its `Cargo.toml` lists `signal-mentci`
+ `signal-frame` + `nota-next`, no mentci-lib). Commit `293a228`
(2026-06-20) is literally titled *"mentci-egui: remove old direct-driver
workbench"* — egui tore out its mentci-lib-shaped workbench and rebuilt
on the contract. A grep of `mentci-egui/src` for `mentci-lib`,
`DaemonRole`, `HandshakeRequest`, or `WorkbenchState` returns nothing.

So mentci-lib is, today, a library with **zero consumers**, being
developed against a transport **no daemon speaks**, carrying a model
**no contract shares**.

## Valuable ideas vs dead skeleton

**Worth preserving (the design, not the code):**

- The **MVU five-shape contract** — `update`/`view` purity,
  `Vec<Cmd>` side-effect return, time-travel-debuggable shape. This is
  the actual intellectual contribution and it is what the whole triad
  realizes.
- The **proposal model** — "edits are proposals, not open verdict
  bodies": a closed verdict set (approve / reject / defer), and an edited
  answer becomes a new typed object through the normal authorization
  path. This idea is now *also* in `signal-mentci` (`AnswerProposal`,
  `ProposeEditedAnswer`, `AnswerProposalAdmitted`) and the daemon, but
  mentci-lib is where it was first stated cleanly (`approval.rs`
  `AnswerProposal` doc-comment).
- The **approval state machine** (`ApprovalState`: receive / select /
  answer / subscribe with interest-filtered deliveries). The *logic* is
  sound client-side projection logic; it should be rebuilt over the
  contract's `InterfaceState` / `PendingQuestionsView` /
  `InterfaceProjection` rather than over its own private types.
- The **per-kind canvas renderer + constructor-flow** abstractions, if
  a graph-editing surface is still wanted — but note the live contract
  has no graph vocabulary, so this is speculative until the daemon grows
  a graph surface.

**Dead skeleton (discard outright):**

- The entire `signal`-crate transport: `connection/driver.rs`'s
  `Body::Request(Request::Handshake)` handshake, `DaemonRole::Criome |
  Nexus`, the length-prefixed `signal::Frame` codec.
- The `Graph` / `Node` / `Edge` / `*Query` / `QueryOperation` model in
  `state.rs` and the `ModelCache` built on it.
- The **`nexus-daemon` second connection** — the live stack has one
  daemon, not two; the dual-daemon `ConnectionState`, the `Nexus*`
  `EngineEvent` variants, and the as-nexus rendering round-trips are all
  for a daemon that was never built.
- The duplicate `approval.rs` *types* (keep the state-machine *shape*,
  drop the type definitions in favor of `signal-mentci`'s).

## Why re-found, not adopt-existing or leave

- **Not "leave it":** it has no consumers and a wire no daemon speaks;
  leaving it means a permanently dead repo accreting more duplicate
  vocabulary on each operator pass (exactly the Jun 18-19 pattern).
- **Not "adopt its existing model":** its model *is* the duplicate. The
  contract already won — `signal-mentci` is the canonical typed
  vocabulary, the daemon and egui both use it, and the no-backward-compat
  / single-best-shape discipline says the consumer-side library must
  consume the one contract, not maintain a private fork of it.
- **Re-found** keeps the genuinely valuable layer (the MVU shape and the
  proposal/approval *logic*, which the design pioneered) and rebuilds it
  as a thin shared client over `signal-mentci` + `signal-frame` — the
  same dependencies mentci-egui already adopted — so that future shells
  (TUI, CLI, status bars) get the shared library mentci-lib's INTENT.md
  promises, instead of each re-implementing the contract the way egui was
  forced to.

The history *is* the argument: mentci-lib was the prototype that proved
the Mentci shape; the shape graduated into the live triad on a new stack;
the prototype must now be rebuilt to ride that stack, carrying its ideas
forward and shedding its obsolete transport and its accidental fork of
the contract's vocabulary.
