# 105 - Kameo context maintenance

Date: 2026-05-17
Role: designer-assistant
Scope: context-maintenance pass over the current Kameo lifecycle and
Persona component migration arc.

## 0. Current Load-Bearing State

The Kameo lifecycle work is no longer in the exploratory research
phase. The current working state is:

```text
Kameo fork named refs:
origin/main == origin/kameo-push-only-lifecycle

Current migration head:
22514f7c actor: gate weak shutdown result helpers
```

The clean stack is:

```text
ddab7733 actor: publish terminal lifecycle outcomes
565ff25e actor: split lifecycle control mailbox
04f6e2ab actor: cover lifecycle control edge cases
22514f7c actor: gate weak shutdown result helpers
```

The branch is ready for Persona component migration with one caveat:
component-level resource witnesses still decide whether the migration
has actually made Persona correct. Kameo now gives the right actor
runtime contract; it does not prove that a component did not clone,
leak, or delegate its exclusive resource elsewhere.

## 1. Decisions Forwarded From The Conversation

### 1.1 Kameo public lifecycle contract

The current public contract is terminal-outcome shaped:

```rust
pub struct ActorTerminalOutcome {
    pub state: ActorStateAbsence,
    pub reason: ActorTerminalReason,
}
```

Callers use `wait_for_shutdown().await` and inspect the outcome when
the shutdown result matters. The old public phase/fact stream is not
part of the contract.

### 1.2 Release-before-notify is internal framework discipline

Kameo's job is to ensure actor state release happens before terminal
shutdown becomes observable. Parent and watcher notifications are sent
through the control plane and awaited until the target control lane
accepts them. Kameo does not wait for the target actor to process
`on_link_died`; that would risk deadlock.

### 1.3 Shutdown is not drain

Stopping a Kameo actor closes ordinary message admission and may discard
queued ordinary messages. Components that require pending domain work to
finish must implement their own domain-level quiesce/drain protocol
before calling stop. Kameo shutdown is lifecycle cleanup, not a hidden
work-completion protocol.

### 1.4 Named dependency references only

Persona components should depend on the fork through a named Git
reference, not a raw commit revision. `branch = "main"` is a valid named
reference for immediate migration, with `Cargo.lock` witnessing the
resolved commit. A stable named branch or tag for this runtime contract
would be cleaner before a broad multi-repo sweep.

### 1.5 `persona-message` naming correction

There is no separate `MessageProxy` component and no
`persona-message-proxy-daemon`. The supervised first-stack component is
`persona-message`; its long-lived binary is `persona-message-daemon`;
that daemon binds `message.sock` and forwards stamped message
submissions to `persona-router`.

Any migration report that says "no proxy daemon" must not be read as
"no message daemon." It means "do not name a separate component
MessageProxy."

## 2. Current Implementation Handoff

Use `reports/operator/132-kameo-component-migration-plan.md` as the
operator implementation plan, with these corrections:

1. In `persona-message`, make the daemon mandatory: migrate
   `MessageDaemonRoot` and any listener/connection actors to the
   terminal-outcome contract; add a `message.sock` release witness.
2. In lifecycle diagrams and prose, say parent/watchers' control lanes
   accept terminal signals. Do not imply target actors have processed
   those signals before `wait_for_shutdown()` returns.
3. Prefer minting a stable named branch or tag from `22514f7c` before
   pinning every component, although `branch = "main"` remains an
   acceptable named reference.
4. Adopt the explicit mechanical sweep from the earlier DA execution
   notes:

```sh
rg "fn on_link_died|wait_for_shutdown\\(|shutdown_result|is_alive\\(|is_accepting_messages\\(|is_terminated\\(" \
  /git/github.com/LiGoldragon/<repo>/src \
  /git/github.com/LiGoldragon/<repo>/tests
```

The first implementation slice remains:

```text
persona-mind:
  pin Kameo named ref
  move StoreKernel to supervised spawn_in_thread
  add redb reopen-after-shutdown witness
  update ARCH constraints
  run checks

then:
  terminal-cell
  persona-terminal
  persona-harness
  persona-router
  persona-message
  persona-introspect
  persona-system
  persona meta-repository last
```

## 3. Still Open

### 3.1 StoreKernel component witness

Kameo's `supervised_spawn_in_thread_releases_resource_before_restart`
test closes the framework-level blocker. `persona-mind` still must prove
the real component fact:

```text
StoreKernel drops the real mind.redb/sema-engine handle before
supervisor replacement or daemon restart can reopen it.
```

Do not remove the `StoreKernel` deferral comment merely because the
Kameo fork test passes. Remove it after the component-level redb witness
passes.

### 3.2 Source-shape checks

Each migrated component should gain source-shape tests or equivalent
Nix checks that prove:

```text
component_uses_workspace_kameo_fork_reference
component_does_not_depend_on_crates_io_kameo
component_does_not_call_get_shutdown_result_for_resource_truth
component_does_not_use_actor_liveness_as_shutdown_proof
```

Process `is_alive` helpers are not a violation. The violation is using
Kameo actor liveness as terminal shutdown truth.

### 3.3 Deferred Kameo framework items

These are not migration blockers:

- `run_to_state_ejection` enum-shaped public API;
- `Shutdown::Brutal` / kill semantics split;
- `#[deprecated]` attribute on `is_alive()`;
- mailbox helper docs polish;
- remote `PeerDisconnected` state truth.

They should not block Persona migration unless a component actually
needs one of them.

## 4. Retired Designer-Assistant Reports

This report forwards the current load-bearing substance from the
following designer-assistant reports:

```text
96-kameo-lifecycle-independent-pov-2026-05-16.md
97-flaws-in-designer-204-kameo-lifecycle.md
98-review-operator-130-kameo-lifecycle-implementation.md
99-review-current-designer-204-kameo-lifecycle.md
101-kameo-lifecycle-implementation-impact-2026-05-16.md
102-audit-operator-131-kameo-control-plane.md
103-kameo-lifecycle-component-migration-plan.md
104-review-operator-132-kameo-component-migration-plan.md
```

Those reports were useful during the design turn, but the branch and the
implementation plan have moved past them. Their still-current
substance is captured here; their detailed history remains in version
control.

## 5. Next-Session Targets

1. Confirm whether operators minted a stable Kameo named ref or used
   `branch = "main"` for the first migration pass.
2. Review the `persona-mind` migration once it lands, especially the
   real redb/sema-engine reopen-after-shutdown witness.
3. After `StoreKernel` lands as a worked example, update
   `skills/kameo.md` with the concrete Persona pattern rather than
   theory-only guidance.
4. Re-run report hygiene after the component migration lands; this
   Kameo handoff should retire once its substance is absorbed into
   component architecture docs and `skills/kameo.md`.

