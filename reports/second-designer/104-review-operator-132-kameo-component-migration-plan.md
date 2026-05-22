# 104 - Review of operator/132 Kameo component migration plan

Date: 2026-05-17
Role: designer-assistant
Scope: review `reports/operator/132-kameo-component-migration-plan.md`
against the current Kameo fork, `reports/designer/205-kameo-lifecycle-migration-impact-2026-05-16.md`,
and current Persona component architecture.

## 0. Verdict

`operator/132` is broadly good to implement. It correctly picks up
the current Kameo stack, including the weak-reference shutdown-result
fix at `22514f7c`, and it preserves the workspace rule that component
manifests use named Git references rather than raw commit revisions.

The main correction needed before an operator follows it literally is
the `persona-message` section: it still reads as if the message daemon
might be optional. Current architecture says the opposite. There is no
separate `MessageProxy` component, but there is a supervised
`persona-message` component with a long-lived
`persona-message-daemon` binary.

## 1. Findings

### 1.1 `persona-message` daemon is under-specified

`operator/132` says:

```text
The current direction after designer report 142 is no separate message proxy
daemon. `persona-message` remains the user/CLI text surface and should talk to
the router using Signal contracts.
```

and then:

```text
Any message daemon/client actor that exists stops with a terminal outcome.
```

The first sentence is only half right. The correct current architecture is:

- no `MessageProxy` component;
- no `persona-message-proxy-daemon`;
- yes `persona-message` as the supervised first-stack message-ingress
  component;
- yes `persona-message-daemon` as the long-lived binary;
- yes `message.sock` owned by that daemon;
- the `message` CLI is a client of `message.sock`.

Current `persona-message/ARCHITECTURE.md` is explicit: the repo owns
both the `message` CLI and `persona-message-daemon`; the daemon binds
`message.sock`, stamps origin/provenance, and forwards
`StampedMessageSubmission` to `persona-router`.

Required correction to `operator/132`: section 6.6 should stop using
optional language. It should require:

- pin `persona-message` to the Kameo fork;
- migrate `MessageDaemonRoot` and any listener/connection actors to
  the terminal-outcome contract;
- add a witness that daemon shutdown releases `message.sock`;
- add a witness that ingress after daemon stop is rejected or reports
  actor stopped;
- keep "no proxy" only as a naming correction, not as a daemon-removal
  claim.

### 1.2 The lifecycle graph slightly overstates notification semantics

`operator/132`'s graph says:

```text
actor Self drops -> parent and watchers receive terminal signal -> wait_for_shutdown returns
```

The implementation guarantee is narrower and should be worded that way:
link/parent notifications are awaited until the target control lane
accepts the signal. Kameo does not wait for the target actor to process
`on_link_died`. That distinction matters because waiting for processing
would create deadlock opportunities.

Suggested wording:

```text
actor Self drops -> parent/watchers' control lanes accept terminal signal -> wait_for_shutdown returns
```

This is not a migration blocker; it is a precision fix.

### 1.3 `main` is acceptable as a named reference, but a stable bookmark is cleaner

`operator/132` correctly rejects raw `rev = ...` pins and says the
lockfile witnesses the resolved commit. It currently proposes
`branch = "main"` as the implementation-ready named reference.

That is allowed by the workspace rule, but the migration would be
cleaner if the Kameo fork minted a stable named branch or tag for this
runtime contract before the multi-repo sweep. The purpose is not
backward compatibility; it is to make the interface name say what the
components depend on. A name like `persona-lifecycle-terminal-outcome`
would make the dependency intent clearer than a moving `main`.

This is a recommendation, not a blocker.

### 1.4 Designer/205 is partially stale after Kameo `22514f7c`

`reports/designer/205-kameo-lifecycle-migration-impact-2026-05-16.md`
is still useful for the migration checklist, but its high blockers were
written against operator/130 at `1329a646`. The later Kameo stack now
covers the control-lane split, generation guard, weak shutdown-result
helper gate, queued ask stop semantics, and supervised
`spawn_in_thread` exclusive-resource witness.

Operators should use designer/205 for migration patterns, not for its
"wait before pinning" conclusion. `operator/132` is the fresher handoff.

## 2. Implementation stance

After the `persona-message` wording is corrected, the plan is good to
execute in the order it gives:

1. pin the Kameo fork by named reference;
2. migrate `persona-mind::StoreKernel` first with a real redb reopen
   witness;
3. migrate terminal/session owners with real PTY/socket/process
   release witnesses;
4. migrate fanout components;
5. update `persona` last so the sandbox can prove a single resolved
   Kameo graph across the first-stack binaries.

The report's best point is that Kameo terminal outcomes do not remove
the need for component-level resource witnesses. `ActorStateAbsence::Dropped`
means the actor state dropped; it does not prove the component did not
clone, leak, or delegate the resource elsewhere. Each component still
has to prove the resource it owns is actually gone.

