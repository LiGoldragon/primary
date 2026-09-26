# Flow L1: ResolveCaller, Flow knows the caller

An Opus subflow of 38de5b did this on 2026-09-25, for landing L1 of `reports/message-in-flow.md`. The living's words it serves: "It knows which pane the call came from so we can use the database to know the aspect and the model." (e51411, 2026-09-25, STT, `flows/e51411/vision/messaging.md`).

## Revisions landed

- signal-flow 5.1.0: `74a47edc39a94e39cfbe7f4619340f257b11cecd`, on 5.0.0 (cf3648f), which the concurrent L2 subflow landed while I worked. The next minor was taken.
- meta-signal-flow 6.0.4: `fbfe8970247d57e9299e496e89d1845df991c73d`. This repins signal-flow only; its own wire is unchanged. The repin is needed because Flow and meta-signal-flow must share one signal-flow.
- flow 0.12.0: `7fdd83333d260051b7ab078c2d1c18c3cb4b5128`, rebased onto L2's 0.11.0 (1d7a0e3), which itself sits on 0.10.7 (8df890b).
- `git ls-remote origin main` printed each of these revisions after its push.

## The new ethos lines (signal-flow `ethos/signal.ethos`)

```
; ResolveCaller names the flow bound to the process that called: the
; Nexus reads the caller from its own socket, never from the payload.
; The optional FlowId is the caller's claim, checked against the
; binding: CallerMismatch carries the Caller the binding names.
```

Appended to queries: `ResolveCaller.Option<FlowId>`

Appended to responses: `CallerResolved.Caller  CallerResolutionRejected.CallerResolutionRejection`

Appended to types: `Caller.{ FlowId FlowAspect PowerLevel ModelName }  CallerResolutionRejection.[ CallerUnknown CallerMismatch.Caller ]`

These lines reuse the existing FlowId, FlowAspect, PowerLevel and ModelName; no type is repeated. The query and both replies are appended, so every 5.0 variant keeps its archived bytes. A test checks this against bytes read from cf3648f, which makes the change additive and the bump a minor one. Datom examples: `ResolveCaller.None`, `ResolveCaller.Some.fac697`, `CallerResolved.{ fac697 Psyche High claude-opus-5-5 }`, `CallerResolutionRejected.CallerMismatch.{ fac697 Mind Medium gpt-6-sol }`.

## How the Nexus identifies the caller

The Nexus uses peer credentials. It does not read the environment the client passes.

1. `SO_PEERCRED` on the accepted ordinary connection gives the peer pid, through rustix `socket_peercred`. The crate forbids unsafe code.
2. Herdr's snapshot carries no pids, so the pid cannot be matched to a pane in the roster. Herdr does mark every process it starts in a pane with `HERDR_SESSION` and `HERDR_PANE_ID`. The Nexus runs as the same uid, so it reads them from `/proc/<pid>/environ`. If the peer's environment is scrubbed, it reads the nearest marked ancestor, walking up through `/proc/<pid>/stat` ppid.
3. The registry must hold exactly one routable flow on that session and pane: not Stopped, and not a held successor. `pane_presence` against the live snapshot must also still show that flow's binding (pane, terminal, harness). A pane id that Herdr reused for a new terminal therefore names no one.
4. The answer comes from the registry's role record.

Why not the client-passed environment: the peer pid comes from the kernel. The pane marks are read from that process's own `/proc` entry, not from anything the caller chose to send. A same-uid process could still exec itself with forged marks, so this is not authentication against the same user. The socket is 0600, which closes the door to anyone else.

## Registry change (storage)

- There is a new `flow_nexus_roles` table. Its row is `StoredRole { Caller }`, keyed by FlowId.
- MetaBindExisting writes the row from the binding's aspect, power and model, atomically with the flow and route rows. Start writes it from the launch profile (`register_flow_in_role`). A flow registered through meta `RegisterFlow` has no role, and ResolveCaller answers `CallerUnknown` for it.
- On open, a store written without roles adopts them. The source is the launch profile of the launch that bound the flow. Failing that, it is the `<aspect>:<power>:<model>` flow type that MetaBindExisting already wrote. Text is parsed only in this migration, and the site says so.

## Tests

- signal-flow: 9 before (on 5.0.0) and 12 after. The three new ones are the datom examples, the Caller textualization, and the 5.0 byte stability check.
- meta-signal-flow: 5 before and 5 after.
- flow, before: 6+3+103+1+1 on 1d7a0e3. The earlier bases were 6+3+99+1+1 on 5b59761 and 6+3+102+1+1 on 8df890b.
- flow, after: 6+3+110+1+1, with 0 failed. The seven new tests:
  - `a_caller_bound_in_the_registry_resolves_with_its_role`
  - `a_process_in_a_pane_is_found_by_its_own_marks_or_its_ancestors`: a real child process, and a grandchild whose marks are scrubbed.
  - `an_unbound_peer_is_caller_unknown`: an unbound pane, no pane, a dispatch without a connection, and a terminal reused by Herdr.
  - `a_claimed_flow_id_that_differs_is_caller_mismatch`
  - `the_kernel_names_the_peer_of_a_connection`: SO_PEERCRED on a socket pair.
  - `a_store_written_before_roles_adopts_them_when_it_reopens`
  - `a_role_is_kept_with_its_binding_and_a_different_one_conflicts`
- `cargo fmt --check` is clean in all three repos.
- `cargo clippy --all-targets` shows 0 warnings in flow and meta-signal-flow. In signal-flow it shows 2 `large_enum_variant` warnings on the generated Query/Response, and 4.0.1 already had them.
- Local `nix build` of flow: `/nix/store/vs59mbgi61bglh2rksvdlpf2w75mk8rf-flow-0.12.0`. Its check phase ran 110 flow-nexus tests with 0 failed, and `flow-nexus --version` prints `flow-nexus 0.12.0`.

## Live witness, on a copy of the store (not deployed)

I copied `~/.local/state/flow/flow.sema` into the scratchpad and opened it with 0.12.0 through a throwaway test, which I did not commit. The live Nexus, its sockets and its store were never touched.

- 11 of 13 flows adopted a role from their MetaBindExisting flow type. For example, 38de5b is Psyche High claude-fable-5-1, e51411 is Psyche Medium claude-opus-5-5, and b7da5d is Field Medium gpt-6-sol.
- 5f38bc and 88475f have no role.
- From this pane, the peer walk gave `messaging-build wD:pR`. `resolve_caller` answered `CallerResolved.{ 38de5b Psyche High claude-fable-5-1 }`, and with claim `ffffff` it answered `CallerMismatch` carrying the same Caller.

## Found while doing it

- **The live store's launch attempts do not decode.** The live store's `flow_nexus_launch_attempts` rows fail rkyv validation (`InvalidSubtreePointer` in `ArchivedLaunchProfile.launch_source_vector`) under 0.11.0 as well as under 0.12.0. My adoption first failed the open on this, and it now reads attempts leniently.
- **Consequence for launched flows.** The two flows launched by Start, 5f38bc and 88475f, therefore get no role and resolve `CallerUnknown` until they are bound again.
- **Check before deploy.** Whether 0.10.7's startup scan of ambiguous launches trips on the same rows was not tested. It should be checked before deploying 0.11 or 0.12.

## Hook for Send (not in this landing)

`Connection::serve_ordinary` already holds the peer. Send's arm should call the same `peer_process().and_then(caller_pane)` and `resolve_caller`, then carry the resulting Caller as the message's sender (Flow ID, aspect, power, model) in place of any claimed `FLOW_ID`.

## Locks

Orchestrate lock 6600 was held over the scratchpad dir `l1-caller-38de5b` and this receipt, and released before return.
