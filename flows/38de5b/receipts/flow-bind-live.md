# Flow bind of live flows — 38de5b, 2026-09-25

Subflow of 38de5b (Opus). Flow 0.10.5 (`LiGoldragon/flow` 5e1382f) on ouranos, with the `flow` and `flow-meta` CLIs from the same closure (`/nix/store/0awmdvi0l15i1k65p00grycxwjkxr984-flow-0.10.5`). Nothing was Started, Stopped, Replaced or Sent. The unit and the pin were not touched.

## Notice to Field Sol
`FLOW_ID=38de5b hm-send b7da5d '…'` returned `Transported.{ b7da5d working }`. No Held was returned and no objection arrived during the window.

## Query type (meta-signal-flow 29ec97d, `ethos/signal.ethos`; pinned by flow 5e1382f Cargo.toml)
The ordinary contract, signal-flow 83171f3, has no bind or import query. The meta contract has one:
```
queries:   MetaBindExisting.MetaBindExisting
responses: BoundExisting.BoundExisting  BindExistingRejected.BindExistingRejection
ProcessIdentity.{ ProcessId ProcessUserId ProcessStartToken }
FlowContainer.{ HerdrSessionName HerdrServerSocketPath HerdrServerProcessIdentity MetaFlowOwnerId }
FlowBinding.{ FlowId FlowAspect PowerLevel ModelName HarnessKind NativeSessionId HerdrWorkspaceId HerdrPaneId HerdrTabId HerdrTerminalId HerdrAgentName ProcessIdentity WorkingDirectory }
MetaBindExisting.{ FlowContainer Vector<FlowBinding> }
FlowLifecycle.[ RegisteredUnconfirmed ]
BoundFlowBinding.{ FlowId FlowLifecycle }
FlowBindingRefusalReason.[ AmbiguousPane DeadProcess DuplicateFlowId AnatomyMismatch ]
RefusedFlowBinding.{ FlowId FlowBindingRefusalReason }
FlowBindingResult.[ Bound.BoundFlowBinding Refused.RefusedFlowBinding ]
BoundExisting.{ FlowContainer Vector<FlowBindingResult> }
BindExistingRejection.[ ContainerUnavailable ContainerIdentityMismatch StoreRefused ]
```
How the Nexus handles it (`crates/flow-nexus/src/lib.rs`, the `Query::MetaBindExisting` arm):
- The container socket must be a live socket, and the container's process identity must match `/proc/<pid>` (uid, plus stat field 22, the start time).
- For each binding, in order, the Nexus refuses with:
  - `DuplicateFlowId` when the id is repeated in the request, or is already in the store.
  - `AnatomyMismatch` when a field is empty, or the process cwd is not the given `WorkingDirectory`.
  - `AmbiguousPane` when the (workspace, pane, tab, terminal, agent) tuple is repeated.
  - `DeadProcess` when the process identity does not match.
- A binding that passes is stored as a `FlowNode` with `EndpointSelection Unavailable`, its Herdr route `Available`, the origin `{ <owner> <herdr-session> meta-bind-existing }`, and lifecycle `Pending`. The reply reports it as `RegisteredUnconfirmed`. Per UPGRADES.md 0.4.0, no binding becomes `Active` through this request. Only an ordinary `Send` whose marker is Presented can promote it.

## Binding list
The 12 live rows of `reports/route-manifest.md` were checked against `herdr agent list` (session `messaging-build`) and `herdr pane process-info`. All 12 panes are live, and their pane and terminal ids match. **5f38bc was left out** because Flow already holds it as `Active`, so a bind would only return `DuplicateFlowId`.
- Container: the Herdr server `pid 3219203` (the `ss -xlp` listener on `/home/li/.config/herdr/sessions/messaging-build/herdr.sock`). The owner is `38de5b`.
- Process: the pane's `codex` or `claude` foreground process, not the intercom helper. The start token is `/proc/<pid>/stat` field 22.
- Native session: from each process's argv (`resume <thread>` or `--session-id`). For d8df70, `d8df703d-…` came from argv. Herdr's `agent_session` shows a different id (`97d78b53-…`), as the manifest noted.
- Power:
  - From receipts `canonicalRole.power`: 26c50c, f5a74e, a676b3, b7da5d, e71dab, 98eb43 and 504461.
  - From the log header: d8df70 and e51411.
  - From profile `role`: 38de5b.
  - Inferred from the title tier (Sol = Medium, which a676b3/b7da5d receipts corroborate): 00f95a.
- Model: from argv, receipts or log header. d8df70 is `claude-opus-5` (argv and log header).

## Validation
The datom was checked in a scratch worktree of meta-signal-flow at 29ec97d with `cargo test --features datom`. It actualizes as `Query::MetaBindExisting` with 11 bindings, and the text round-trips byte-identical (`test live_bind_datom_is_a_meta_query ... ok`). It was regenerated from live state just before sending and matched byte-for-byte (`cmp` UNCHANGED).

## Datom sent (`flow-meta '<datom>'`)
```
MetaBindExisting.{ { messaging-build /home/li/.config/herdr/sessions/messaging-build/herdr.sock { 3219203 1001 61814493 } 38de5b } [ { 00f95a Mind Medium gpt-6-sol Codex 01a0d4ec-9746-7340-b60c-84300f95aa7c wM wM:pB wM:tF term_65c3ff8204dc373 mind-sol-00f95a { 2027935 1001 121109544 } /home/li/primary } { 26c50c Mind High gpt-6-astra Codex 01a0d579-f7e3-72e3-8444-65826c50c59f wM wM:pC wM:tG term_65c41e8c721447a mind-astra-26c50c { 2669153 1001 121943394 } /home/li/primary } { f5a74e Mind High gpt-6-astra Codex 01a0d997-a21c-7903-b997-b34f5a74e208 wM wM:pD wM:tH term_65c52095db80f82 mind-astra-f5a74e { 807681 1001 128869853 } /home/li/primary } { a676b3 Mind Medium gpt-6-sol Codex 01a0da22-1cab-7aa1-89d7-9b4a676b3fc7 wM wM:pF wM:tK term_65c5414e9aa9884 mind-sol-a676b3 { 1176701 1001 129791488 } /home/li/primary } { b7da5d Field Medium gpt-6-sol Codex 01a0d54c-9013-73f3-8ab2-c55b7da5da58 wQ wQ:pT wQ:tP term_65c41aac961f978 field-sol-b7da5d { 2584918 1001 121845063 } /home/li/primary } { e71dab Field Low gpt-6-luna Codex 01a0d572-6ba1-7b20-bdcf-f29e71dabb46 wQ wQ:pV wQ:tQ term_65c41cd7bd31479 field-luna-e71dab { 2631788 1001 121897550 } /home/li/primary } { 98eb43 Field Low gpt-6-luna Codex 01a0d956-86a5-7600-9283-c8f98eb43815 wQ wQ:pW wQ:tR term_65c5100e5cf517e field-monitor-01a0d9 { 487785 1001 128426203 } /home/li/primary } { 504461 Field High gpt-6-astra Codex 01a0da2a-fdbb-7262-a93b-226504461843 wQ wQ:pX wQ:tS term_65c543d588df185 field-astra-504461 { 1194653 1001 129837689 } /home/li/primary } { d8df70 Psyche Medium claude-opus-5 Claude d8df703d-d083-4c29-9597-6b32e7411b75 wD wD:pD wD:tC term_65c2be0c1adcd62 psyche-opus-5 { 520394 1001 112480426 } /home/li/primary } { e51411 Psyche Medium claude-opus-5-5 Claude e5141130-9a4a-4b8f-b405-67d941a7b320 wD wD:pF wD:tE term_65c3d2d430e6265 psyche-opus-of-d8df70-r2 { 1716162 1001 119917948 } /home/li/primary } { 38de5b Psyche High claude-fable-5-1 Claude 38de5bbb-be48-4bae-883e-2d622fb79c9e wD wD:pR wD:tG term_65c500aa730757c psyche-fable-refresh-5f38bc { 157498 1001 128017785 } /home/li/primary } ] }
```

## Reply (verbatim)
```
BoundExisting.{ { messaging-build /home/li/.config/herdr/sessions/messaging-build/herdr.sock { 3219203 1001 61814493 } 38de5b } [ Bound.{ 00f95a RegisteredUnconfirmed } Bound.{ 26c50c RegisteredUnconfirmed } Bound.{ f5a74e RegisteredUnconfirmed } Bound.{ a676b3 RegisteredUnconfirmed } Bound.{ b7da5d RegisteredUnconfirmed } Bound.{ e71dab RegisteredUnconfirmed } Bound.{ 98eb43 RegisteredUnconfirmed } Bound.{ 504461 RegisteredUnconfirmed } Bound.{ d8df70 RegisteredUnconfirmed } Bound.{ e51411 RegisteredUnconfirmed } Bound.{ 38de5b RegisteredUnconfirmed } ] }
```

## `flow 'List.{}'` after (verbatim)
```
Listed.[ { 00f95a 01a0d4ec-9746-7340-b60c-84300f95aa7c Codex Unavailable Available.{ messaging-build mind-sol-00f95a wM:pB term_65c3ff8204dc373 } { 38de5b messaging-build meta-bind-existing } Pending } { 26c50c 01a0d579-f7e3-72e3-8444-65826c50c59f Codex Unavailable Available.{ messaging-build mind-astra-26c50c wM:pC term_65c41e8c721447a } { 38de5b messaging-build meta-bind-existing } Pending } { 38de5b 38de5bbb-be48-4bae-883e-2d622fb79c9e Claude Unavailable Available.{ messaging-build psyche-fable-refresh-5f38bc wD:pR term_65c500aa730757c } { 38de5b messaging-build meta-bind-existing } Pending } { 504461 01a0da2a-fdbb-7262-a93b-226504461843 Codex Unavailable Available.{ messaging-build field-astra-504461 wQ:pX term_65c543d588df185 } { 38de5b messaging-build meta-bind-existing } Pending } { 5f38bc 01a0d4f6-6bc6-7530-94d6-1515f38bcb84 Codex Available.{ /home/li/.codex-next/app-server-control/app-server-control.sock Ready } Available.{ messaging-build field-astra-5f38bc wQ:pN term_65c3ff14cafb070 } { 5f38bc 01a0d4f6-6bc6-7530-94d6-1515f38bcb84 unavailable } Active } { 88475f 88475fd7-e328-4e11-9094-db2139a08fe0 Claude Unavailable Available.{ messaging-build claude-86b6e54cb9618d95d6d8ceaa w17:p1 term_65c5883e612c88a } { e51411 e5141130-9a4a-4b8f-b405-67d941a7b320 handover-successor } Pending } { 98eb43 01a0d956-86a5-7600-9283-c8f98eb43815 Codex Unavailable Available.{ messaging-build field-monitor-01a0d9 wQ:pW term_65c5100e5cf517e } { 38de5b messaging-build meta-bind-existing } Pending } { a676b3 01a0da22-1cab-7aa1-89d7-9b4a676b3fc7 Codex Unavailable Available.{ messaging-build mind-sol-a676b3 wM:pF term_65c5414e9aa9884 } { 38de5b messaging-build meta-bind-existing } Pending } { b7da5d 01a0d54c-9013-73f3-8ab2-c55b7da5da58 Codex Unavailable Available.{ messaging-build field-sol-b7da5d wQ:pT term_65c41aac961f978 } { 38de5b messaging-build meta-bind-existing } Pending } { d8df70 d8df703d-d083-4c29-9597-6b32e7411b75 Claude Unavailable Available.{ messaging-build psyche-opus-5 wD:pD term_65c2be0c1adcd62 } { 38de5b messaging-build meta-bind-existing } Pending } { e51411 e5141130-9a4a-4b8f-b405-67d941a7b320 Claude Unavailable Available.{ messaging-build psyche-opus-of-d8df70-r2 wD:pF term_65c3d2d430e6265 } { 38de5b messaging-build meta-bind-existing } Pending } { e71dab 01a0d572-6ba1-7b20-bdcf-f29e71dabb46 Codex Unavailable Available.{ messaging-build field-luna-e71dab wQ:pV term_65c41cd7bd31479 } { 38de5b messaging-build meta-bind-existing } Pending } { f5a74e 01a0d997-a21c-7903-b997-b34f5a74e208 Codex Unavailable Available.{ messaging-build mind-astra-f5a74e wM:pD term_65c52095db80f82 } { 38de5b messaging-build meta-bind-existing } Pending } ]
```

## `flow 'ResolveRecipient.<id>'` after (verbatim, read-only)
```
RecipientResolved.{ 00f95a 01a0d4ec-9746-7340-b60c-84300f95aa7c Codex Unavailable Unavailable { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ 26c50c 01a0d579-f7e3-72e3-8444-65826c50c59f Codex Unavailable Unavailable { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ f5a74e 01a0d997-a21c-7903-b997-b34f5a74e208 Codex Unavailable Unavailable { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ a676b3 01a0da22-1cab-7aa1-89d7-9b4a676b3fc7 Codex Unavailable Unavailable { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ b7da5d 01a0d54c-9013-73f3-8ab2-c55b7da5da58 Codex Unavailable Unavailable { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ e71dab 01a0d572-6ba1-7b20-bdcf-f29e71dabb46 Codex Unavailable Unavailable { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ 98eb43 01a0d956-86a5-7600-9283-c8f98eb43815 Codex Unavailable Unavailable { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ 504461 01a0da2a-fdbb-7262-a93b-226504461843 Codex Unavailable Unavailable { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ d8df70 d8df703d-d083-4c29-9597-6b32e7411b75 Claude Unavailable Available.{ messaging-build psyche-opus-5 wD:pD term_65c2be0c1adcd62 } { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ e51411 e5141130-9a4a-4b8f-b405-67d941a7b320 Claude Unavailable Available.{ messaging-build psyche-opus-of-d8df70-r2 wD:pF term_65c3d2d430e6265 } { 38de5b messaging-build meta-bind-existing } Pending }
RecipientResolved.{ 38de5b 38de5bbb-be48-4bae-883e-2d622fb79c9e Claude Unavailable Available.{ messaging-build psyche-fable-refresh-5f38bc wD:pR term_65c500aa730757c } { 38de5b messaging-build meta-bind-existing } Pending }
```

## Outcome
- **Bound, 11 of 11:** 00f95a, 26c50c, f5a74e, a676b3, b7da5d, e71dab, 98eb43, 504461, d8df70, e51411, 38de5b. Each is stored as `Pending` / `RegisteredUnconfirmed`. None refused. Flow now lists 13 flows.
- **Active:** only 5f38bc, which was already there. 88475f was also already there, launched by e51411 as a successor, and is `Pending`.
- **Live route at resolve time:**
  - The 3 Claude bindings (d8df70, e51411, 38de5b) resolve `Available`.
  - All 8 Codex bindings resolve their Herdr route `Unavailable`, as does the Active 5f38bc. `HerdrCli::snapshot_has_route` needs `agent_status` to be `idle` or `working` and `interactive_ready == true`. Herdr reports rested Codex panes as `done`, and several have no `interactive_ready`.
  - 88475f resolves `Unavailable` because its Herdr agent name changed after launch, from `claude-86b6e54cb9618d95d6d8ceaa` to `psyche-opus-88475f`.
- **Promotion to Active:** needs an ordinary `Send` per flow, which types a marker into each pane. This subflow was not authorised for that.

## Sources
- `LiGoldragon/meta-signal-flow` 29ec97d: `ethos/signal.ethos`, `tests/contract.rs`
- `LiGoldragon/signal-flow` 83171f3: `ethos/signal.ethos`
- `LiGoldragon/flow` 5e1382f: `crates/flow-nexus/src/lib.rs`, `crates/flow-nexus/src/store.rs`, `crates/flow-nexus/src/herdr.rs`, `crates/flow-meta/src/main.rs`, `UPGRADES.md`, `DESIGN.md`
- `/home/li/primary/flows/38de5b/reports/route-manifest.md`, and the receipts it cites
- Live on 2026-09-25: `herdr agent list`, `herdr pane process-info --pane <id>`, `/proc/<pid>/{stat,cwd}`, and `ss -xlp`
