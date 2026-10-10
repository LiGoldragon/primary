# Flow 0.12.2: the Codex endpoint is not a gate, and a matching rebind gives a held flow its role

An Opus subflow of 38de5b did this on 2026-09-25. The work ran in a fresh clone in the scratchpad dir `codexep-0122-38de5b`, under Orchestrate lock 6671, which was released before return. Against the live Nexus I ran only `flow 'ResolveRecipient.…'` queries and read-only system inspection. There was no Start, Stop, Send, Replace, Configure or bind.

## Diagnosis (live Flow 0.12.1, pid 3403852)

- **Live answers:**
  - `flow 'ResolveRecipient.26c50c'` → `RecipientResolved.{ 26c50c 01a0d579-… Codex Unavailable Available.{ messaging-build mind-astra-26c50c wM:pC term_65c41e8c721447a } { 38de5b messaging-build meta-bind-existing } Pending }`.
  - For comparison, 5f38bc → `Codex Available.{ /home/li/.codex-next/app-server-control/app-server-control.sock Ready } Available.{ … } … Active`.
- **No Codex endpoint check exists on the resolve or Send path**, at fe709c7 or at 7fdd833.
  - The `Query::ResolveRecipient` arm (`lib.rs`) calls `store.resolve_recipient` and then applies `claude::refresh_readiness` and `herdr.refresh_route`. The first touches only Claude endpoints. The second touches only the Herdr route, and sets an Available endpoint to Parked when the route is gone.
  - `codex.rs` (`CodexEndpoints`, `CodexAdapter`) is used only by Start/launch, ConsumeReset and transcript location.
  - `Send` checks only three things: not Stopped, not a held successor, and the Herdr route (`refresh_route`, `identity_is_claimed`, snapshot). It never reads `endpoint_selection`.
- **Where `Unavailable` comes from:** it is a stored fact. The `MetaBindExisting` arm writes every imported flow as `endpoint_selection: EndpointSelection::Unavailable` with lifecycle `Pending`, which is the Flow 0.4.0 rule. Nothing re-evaluates the endpoint afterwards. 5f38bc shows `Available` only because its meta `RegisterFlow` row carried that value.
- **Why `Pending`:** by design. A flow becomes Active only after a Presented `Send` (0.4.0 / 0.11.0). No Send has been made to 26c50c since the bind.
- **Candidate causes tested:**
  - **(a) Empty configuration: no.** The unit's drop-in and `/proc/3403852/environ` carry `FLOW_CODEX_{STABLE,NEXT}_{CLIENT,SOCKET,HOME,MODELS}` with real values (next = `/home/li/.codex-next/app-server-control/app-server-control.sock`, `gpt-6-sol,gpt-6-luna,gpt-6-astra`). `adopt_overrides` persists them at open. There is no read-only meta query for configuration: `Configure` is the only configuration request, and it writes. The resolve path does not read the configuration anyway. **No Configure datom is needed.**
  - **(b) Imported threads not owned by the app-server: no.** 26c50c's process (pid 2669153) runs `codex resume --remote unix:///home/li/.codex-next/app-server-control/app-server-control.sock -m gpt-6-astra … 01a0d579-…`. Its thread is served by the configured next app-server. Flow never asks the app-server about it.
  - **(c) Socket path or model mismatch: no.** The socket and model list match the live install. They are not consulted either.
- **The actual cause:** the brief's reading, that `Unavailable` gates the flow, does not hold. The reply already shows the Herdr route `Available` and the endpoint `Unavailable` as separate facts. A Send to 26c50c today types into the pane, and a Presented Send promotes it. ResolveRecipient has no top-level Available/Unavailable. Once deployed, "ResolveRecipient.26c50c → Available" means the route field, and it already reads that way.

## Change (LiGoldragon/flow 34aaf7875af11cb539218c61cf2fc51996db271b, 0.12.1 → 0.12.2)

- **Rule for the version: a patch.** It changes Nexus behaviour and has no wire, contract or storage-shape change: signal-flow and meta-signal-flow are untouched and no table is new. `git ls-remote origin main` = 34aaf78.
- **Coordinator's mid-task ruling:** a matching MetaBindExisting of a held flow asserts its role. It is implemented in `store.rs` `assert_role_of_matching_binding`, and the `lib.rs` pre-check that refused every held FlowId was removed.
  - **Matching** means all of these:
    - the stored flow is not Stopped;
    - it has the same native thread and harness;
    - its stored route is on the same Herdr session, pane and terminal. The agent name may differ.
  - **Recording the role:** it is written only when the flow has none. Nothing else is written, and a repeat is idempotent.
  - **Refusals:** any other binding, or a role different from the one recorded, stays `DuplicateFlowId` and writes nothing.
  - **Reply:** `Bound.{ <flow> RegisteredUnconfirmed }`. The meta contract has no other bound form. For an already-Active flow that word confirms nothing new. This is a wording gap in meta-signal-flow, not fixed here.
- **Imported-Codex rule:** stated and pinned with fixtures. The code is unchanged, because it already behaved this way.
- **UPGRADES.md and DESIGN.md** state both.

## Fixtures (cargo test 124 before → 128 after, 0 failed; clippy `--all-targets -D warnings` clean; `cargo fmt --check` clean)

- `an_imported_codex_flow_is_sent_through_its_pane_without_an_endpoint`:
  - Setup: MetaBindExisting of a Codex flow; its Herdr pane is `done` with no `interactive_ready`, as 26c50c is live; the fixture's Codex endpoint sockets do not exist.
  - Resolve: route Available, endpoint Unavailable, Pending.
  - Send: Presented, exactly `bare prompt` typed, one observed prompt.
  - After: Active, with the endpoint still Unavailable.
- `an_imported_codex_flow_whose_pane_is_gone_is_refused_before_typing`: the route is Unavailable and Send answers `RouteUnavailable`. Nothing is typed, there is no prompt, and the flow stays Pending.
- `a_matching_binding_of_a_flow_already_held_asserts_only_its_role`:
  - Setup: a RegisterFlow row, Active and roleless, shaped like 5f38bc, rebound twice under a new agent name.
  - Each time: Bound, the role is stored, and List is byte-equal to before.
- `a_differing_binding_of_a_flow_already_held_is_refused_and_writes_nothing`:
  - A different terminal, pane, thread or harness → DuplicateFlowId, with no role and the node unchanged.
  - A different role after one is recorded → DuplicateFlowId, and the role is kept.
- The two imported-Codex fixtures pass on 0.12.1 as well, since they are witnesses of the rule. The two rebind fixtures fail on 0.12.1 by construction, because its pre-check refused every held FlowId. I reasoned this and did not run it.

## Build

`nix build --option builders '' --option substituters https://cache.nixos.org --option max-jobs auto` at 34aaf78 → `/nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2` (flow, flow-meta, flow-nexus). Its check phase ran 6+3+117+1+1 tests with 0 failed, and `flow-nexus --version` prints `flow-nexus 0.12.2`. It is not deployed. Deploying is b7da5d's step.

## For Field

- There is no Configure datom to apply.
- After deploy, 5f38bc can take a role with `flow-meta 'MetaBindExisting.{ <container> [ { 5f38bc <aspect> <power> <model> Codex 01a0d4f6-6bc6-7530-94d6-1515f38bcb84 <ws> wQ:pN <tab> term_65c3ff14cafb070 <agent> <process identity> /home/li/primary } ] }'`. The role must be verified first: 00f95a's M1 gate holds 5f38bc's model as unverified, so this receipt names no role.
- The 11 imported Pending flows become Active on their first Presented Send. No Send was made here.
