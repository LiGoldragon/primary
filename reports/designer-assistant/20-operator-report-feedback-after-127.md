# 20 - Operator report feedback after designer 127

*Designer-assistant report. Date: 2026-05-11. Scope: feedback on the
current operator reports after the trust/channel/input-gate decisions in
`reports/designer/125-channel-choreography-and-trust-model.md` and
`reports/designer/127-decisions-resolved-2026-05-11.md`. Files read:
`reports/operator/108-persona-mind-system-overview.md`,
`reports/operator/109-beads-audit-and-session-discipline.md`,
`reports/operator/110-persona-meta-integration-start.md`, and
`reports/operator/111-persona-daemon-implementation-review.md`.*

---

## 0 - Short Read

The operator reports are strongest where they describe implementation
truth without pretending the scaffolds are final. `reports/operator/111-
persona-daemon-implementation-review.md` is especially useful: it names
the daemon-client slice, calls out the in-memory catalog, rejects
environment-derived identity, and correctly says the persona daemon
creates sockets at spawn time instead of becoming a runtime acceptor for
every component stream.

The feedback is mostly propagation from 127:

- add 127 to the operator reading model, not just 125/126;
- stop treating persona-system focus/prompt observation as a current
  injection dependency;
- stop describing persona-message as a delivery daemon or router-to-
  terminal proxy;
- make terminal-cell signal integration (T9) explicit in meta-stack
  and terminal plans;
- treat any Persona-local `AuthProof` name as a design smell, while not
  confusing that with the existing base `signal-core::AuthProof` carrier;
- mark older mind/system overview language as historical where it still
  teaches the old focus/input-buffer model.

## 1 - Feedback On Operator 111

`reports/operator/111-persona-daemon-implementation-review.md` is the
best aligned of the operator reports. The bottom line is right: the
current `persona` repo has a real daemon-client proof slice, not yet the
real engine manager.

High-signal parts to keep:

- thin CLI → daemon over Unix socket;
- data-bearing nouns (`PersonaEndpoint`, `PersonaClient`,
  `PersonaDaemon`, `EngineManager`);
- Kameo actor owns current in-memory state;
- tests named after constraints;
- explicit rejection of a runtime `ConnectionAcceptor`;
- explicit warning that `AuthProof::LocalOperator` should be retired,
  not hardened;
- T3 focus on socket setup, privileged-user mode, manager redb,
  `EngineId`-scoped paths, and spawn envelope.

Corrections I would make:

- The update banner should cite `reports/designer/127-decisions-resolved-
  2026-05-11.md` as well as 125/126. 127 changes the active wave by
  pausing persona-system, adding T9, and defining terminal-cell's
  control/data split.
- The sentence "no route table" / "no route table yet" should be
  precise. The persona daemon may need an engine catalog and maybe
  upgrade/migration metadata later, but router/mind channel state is not
  a persona-daemon route table. Avoid reintroducing old `EngineRoute`
  machinery through the daemon.
- T3 says engine-level upgrade lands in follow-up T9 if it mirrors the
  stale lower half of 126. T9 now means terminal-cell signal integration.
  Engine-level upgrade is a later engine-upgrade track with no current
  track number.
- Socket paths need two levels named: the manager/control socket for
  the persona daemon itself may be global, while component sockets are
  `EngineId`-scoped. "Replace `/tmp/persona.sock` with
  `/var/run/persona/<engine-id>/...`" is right for component sockets,
  but the persona manager CLI still needs a well-known manager endpoint.
- The concurrent-client fix should not be named in a way that recreates
  `ConnectionAcceptor`. Per-stream tasks or a small listener object are
  fine. The thing to avoid is a central security actor that accepts
  every component stream and mints in-band proofs.
- Privileged-user tests should split dev and production witnesses:
  mode/owner behavior can be tested in a temp runtime directory where
  possible; the actual `persona` system user belongs to NixOS/systemd
  deployment witnesses. Do not make ordinary repo tests require host
  user setup.

The `IngressContext` recommendation is good. I would sharpen it:
`IngressContext` / `AcceptedPeer` is local socket provenance; future
cross-host signed assertions should get a different type name. Do not
let a slim `AuthProof` tag become a fake proof.

## 2 - Feedback On Operator 110

`reports/operator/110-persona-meta-integration-start.md` has a good
systemd read. The staged decision is pragmatic:

1. Nix app/scripts for dev and stateful tests first.
2. NixOS module/systemd unit for the privileged persona daemon next.
3. Rust systemd D-Bus control only if Persona later needs dynamic
   transient units.

The part that needs updating is the current stack/missing-seam model.
After 127, the next visible terminal dependency is:

```text
T1 signal-persona-auth
  -> T9 terminal-cell control plane speaks signal-persona-terminal
  -> T6 persona-terminal supervisor uses that contract
  -> T7 persona-harness maps delivery into terminal action
  -> T4/T5 router+mind channel choreography authorizes delivery
```

The report should stop implying persona-system participates in the
current message-to-terminal injection path. Focus may return later, but
injection safety is terminal-owned: acquire input gate, cache human
bytes, read prompt state, inject only if clean, release and replay.

The "smallest honest stack" can stay, but add a warning that current
terminal Signal input/capture witnesses are not the final T9/T6 split
until terminal-cell's control plane is actually `signal-persona-terminal`
and the raw data plane is protected by witnesses.

## 3 - Feedback On Operator 109

`reports/operator/109-beads-audit-and-session-discipline.md` needs the
most queue refresh.

Rows I would update:

- `primary-2w6`: still real, but the description is stale. Persona-
  message should be a stateless one-shot message proxy / CLI surface
  that sends to router. It should not be a proxy daemon that receives
  router delivery work and talks to terminal. Delivery path is router →
  harness → persona-terminal → terminal-cell.
- `primary-b7i`: after 127, the typed-Nexus-body migration is no longer
  the target. If this bead remains open, reframe it as "grow specificity
  through `MessageKind` data-carrying variants and prevent freeform
  body from swallowing modeled semantics." Otherwise close it as
  superseded by 127 D2.
- `primary-3fa`: focus/input observation ownership is mostly resolved
  for the current wave. Prompt state is terminal-owned; persona-system
  focus is paused. Refresh or close this if no other competing types
  remain.
- `primary-rhh`: if this is the old `ActorKind` decision bead, it is
  obsolete after the user's decision. Verify the code, then close or
  replace with a concrete removal task if `ActorKind` still exists.
- `primary-kxb`: any remaining terminal-adapter protocol question should
  now point at T9's control/data split, not at a generic "terminal
  adapter protocol" uncertainty.

The BEADS discipline itself is good: if the work can survive context
compaction, it needs a bead; a claimed bead must be closed or updated
before release. Keep that.

## 4 - Feedback On Operator 108

`reports/operator/108-persona-mind-system-overview.md` is useful as an
implementation snapshot, but several paragraphs should be marked
historical after 127.

The stale part is this framing:

> injecting text into an interactive prompt is unsafe unless the router
> can prove the prompt buffer and focus state are acceptable. That is why
> persona-system and the router-side input gate remain first-class.

The updated framing is:

- injection safety is terminal-owned;
- router requests delivery and consumes terminal delivery results;
- persona-terminal acquires the input gate and checks prompt state while
  human bytes are cached;
- persona-system focus is not a current safety dependency;
- there is no router-side input gate for terminal bytes.

The mind overview should also avoid calling `persona-mind` "the
executable center" in a way that suggests all messages pass through
mind. Mind is the policy/choreography and durable work-graph center.
Router can deliver messages over authorized channels without asking mind
every time.

The suspicious-code section remains valuable. The `StoreSupervisor`,
whole-graph snapshot, trace phases, and prototype daemon loop are still
real implementation debt. None of that is invalidated by 127.

## 5 - Priority Feedback To Operator

If I were sending the operator only five changes, they would be:

1. Add a short 127 update banner to 108, 110, and 111.
2. Rewrite the `primary-2w6` / persona-message language so it is not a
   daemon or delivery relay.
3. Remove current-wave persona-system focus/input-buffer wording from
   108 and 110.
4. Update 111 so T9 is terminal-cell signal integration, not engine
   upgrade, and so persona daemon does not own router/mind channel
   state.
5. Keep the `AuthProof` rejection, but distinguish base
   `signal-core::AuthProof` compatibility from new Persona-local
   provenance types.

## 6 - Open Questions

Questions I would send back to the operator before implementation:

- What is the final well-known manager socket for the persona daemon
  itself, separate from `EngineId`-scoped component sockets?
- Is `AuthProof::LocalOperator` being removed only from Persona-local
  provenance, or is there a plan to change the base `signal-core` frame
  carrier too? Those are different blast radii.
- Where will the bootstrap component catalog live before full manager
  redb exists: static config file, Nix-generated config, or manager
  table seeded on first run?
- Which T9 witness will prove the raw terminal data plane does not pass
  through Signal encoding or a Kameo mailbox?

## 7 - Net Position

The operator's implementation instincts are good: build real slices,
name scaffolding honestly, and add constraint witnesses. The main risk
is stale architecture language leaking back into implementation through
old report diagrams and bead descriptions. The 127 decisions are simple
enough to enforce: terminal owns injection safety, router owns channel
state, mind owns adjudication/policy, persona daemon owns engine
substrate, and persona-message is only an ingress convenience surface.

