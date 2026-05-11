# 18 - Current Persona handoff after editorial pass

*Designer-assistant report. Date: 2026-05-11. This replaces the
superseded back-and-forth reports `18-deferred-persona-decisions-
response.md`, `19-response-to-designer-127-and-contract-skill.md`,
and `20-operator-report-feedback-after-127.md`. Those reports were
useful while the designer plans were being corrected; this report is
the current consolidated read after the designer editorial pass.*

---

## 0 - Reading Order

The active reading order is now clear:

1. `reports/designer/127-decisions-resolved-2026-05-11.md`
   for the settled D1-D7 decisions.
2. `reports/designer/125-channel-choreography-and-trust-model.md`
   for the trust and channel model.
3. `reports/designer/126-implementation-tracks-operator-handoff.md`
   for operator tracks and bead suggestions.
4. Component plans `reports/designer/116-123`, but only after reading
   their status banners.
5. `skills/contract-repo.md` for the updated contract-repo rule:
   a contract crate owns one component's wire surface, and each relation
   inside it is named explicitly.

`reports/designer-assistant/16-new-designer-documents-analysis.md`
remains a historical diagnosis because designer files still cite it.
It is not the active implementation guide.

`reports/designer-assistant/17-pre-today-report-cleanup-agglomeration.md`
is also historical where it conflicts with 127. In particular, its
typed-Nexus-body concern is superseded by 127 D2: `MessageBody(String)`
is acceptable as the freeform body, and specificity grows through
`MessageKind` variants.

## 1 - Settled Architecture

The current architecture is simpler than the earlier plan set.

Local trust comes from the kernel filesystem ACL on Unix sockets. The
persona daemon creates sockets with the correct owner and mode at spawn
time. Internal component sockets are privileged. The user-writable
persona-message socket is the boundary where untrusted user input
enters. `MessageOrigin` / `ConnectionClass` are audit and provenance
records, not runtime proof objects that every component verifies. There
is no Persona-local `AuthProof` record in the current design.

Router owns authorized-channel state. It does not run the old
class-aware delivery tree. If a channel is already authorized, router
can deliver without asking mind again. If a message attempts a channel
that is not authorized, router parks or forwards it to mind for
adjudication. Mind can grant one-shot, permanent, or time-bound
channels, and it owns owner-approval or suggestion structures.

Terminal injection safety is terminal-owned. Persona-terminal
coordinates the transaction; terminal-cell provides the low-level
writer-side gate. The current flow is:

1. Acquire the input gate.
2. Cache human bytes while the gate is held.
3. Check prompt state using a registered `PromptPattern`.
4. Inject only if clean.
5. Release the gate and replay cached human bytes in order.

Persona-system is paused for this wave. Focus is not a current injection
safety dependency. The existing focus tracker can stay in code, but T8
is not an active implementation track.

Terminal-cell stays its own repo. Its control plane moves to
`signal-persona-terminal`; its data plane stays raw. Keystrokes and PTY
output must not be Signal-encoded per byte, routed through a Kameo
mailbox, or delayed behind transcript subscription machinery.

Harness publishes prompt-pattern records for the terminal flow. It also
owns harness identity, lifecycle, adapter capabilities, and transcript
pointers. Transcript fanout defaults to typed observations plus sequence
pointers; raw transcript bytes remain in terminal-owned storage and are
read only through explicit inspection/query paths.

`MessageBody(String)` is acceptable as the freeform text part of a
message. More specificity grows through closed, data-carrying
`MessageKind` variants. There is no current typed-Nexus-body migration
block.

Enums stay closed. `HarnessKind::Other { name }` is gone; `Fixture` is
the named integration/test case, and real new harness kinds require
schema evolution.

## 2 - Operator Tracks

The operator-facing handoff is `reports/designer/126-implementation-
tracks-operator-handoff.md`.

Active tracks:

- T1: create `signal-persona-auth`, with `MessageOrigin`,
  `ConnectionClass`, engine ids, channel ids, and no Persona-local
  `AuthProof`.
- T2: retire stale `persona-message` paths. The target is a stateless
  one-shot message ingress surface, not a delivery daemon or local
  ledger.
- T3: persona daemon socket setup, privileged-user mode, manager redb,
  engine catalog, `EngineId`-scoped paths, and spawn envelope.
- T4: persona-router channel state and adjudication.
- T5: persona-mind channel choreography, subscription primitive, and
  suggestion/adoption policy.
- T9: terminal-cell signal integration. Control plane speaks
  `signal-persona-terminal`; data plane stays raw; worker lifecycle
  push is required.
- T6: persona-terminal supervisor socket, delivery state, and
  gate-and-cache transaction. T6 depends on T9's contract surface.
- T7: persona-harness daemon, identity, lifecycle, prompt patterns, and
  transcript-pointer fanout.

Deferred:

- T8: persona-system. Do not file the T8 bead in this wave.
- Engine-level upgrade. This is a later track after T1-T9, not T9.

## 3 - Status Of The Old Plan Bodies

The status banners added by designer are now the safety rail:

- `reports/designer/118` keeps actor topology and sema schema framing,
  but old class-aware delivery, `OwnerApprovalInbox`,
  `EngineRoute` / `OtherPersona`, and class gates are superseded.
- `reports/designer/119` is deferred entirely for this wave.
- `reports/designer/120` keeps harness daemon, redb, lifecycle,
  adapter capabilities, prompt patterns, and transcript pointers. Its
  old `Other` harness kind and raw transcript fanout are superseded.
- `reports/designer/121` keeps supervisor socket, sema tables,
  terminal events, session GC, and control CLI. Its old class-aware
  input gate and system-owned input-buffer path are superseded.
- `reports/designer/123` keeps the raw data-plane design, terminal-cell
  input gate, worker observability, and maturity framing. Its old
  recommendation to keep the control socket bespoke is superseded.

`reports/designer/124-synthesis-drift-audit-plus-development-plans.md`
is historical synthesis. It already has a banner pointing to 125/126.
Do not use its body as the implementation source when it conflicts with
125, 126, or 127.

## 4 - Operator Feedback Folded Forward

The useful feedback to operator now fits in one place:

- Add 127 context to any operator report that still cites only 125/126.
- Do not implement persona-system focus/prompt observations as the
  current injection safety model.
- Do not implement persona-message as a delivery relay. Delivery flows
  router -> harness -> persona-terminal -> terminal-cell.
- Do not let T9 mean engine upgrade. T9 is terminal-cell signal
  integration.
- Keep the rejection of Persona-local `AuthProof`, but distinguish it
  from the existing base `signal-core::AuthProof` frame carrier if that
  remains for compatibility.
- Split dev witnesses from deployment witnesses for privileged-user
  mode. Socket mode and owner behavior can have temp-runtime tests;
  the actual `persona` system user belongs to host/NixOS deployment
  witnesses.

## 5 - Questions Still Worth Answering

These are implementation-shaping questions, not blockers for the
current handoff:

- What is the final well-known manager socket for the persona daemon
  itself, separate from `EngineId`-scoped component sockets?
- Where does the bootstrap component catalog live before the full
  manager redb path is complete: Nix-generated config, static config,
  or seeded manager tables?
- What is the exact relation between base `signal-core::AuthProof` and
  Persona-local `MessageOrigin` during the migration? The local Persona
  contract should not create a new proof type.
- What is the exact `PromptPattern` contract shape that harness
  publishes and persona-terminal registers with terminal-cell?
- Which T9 witness proves attached viewer bytes do not pass through
  Signal encoding, a Kameo mailbox, or transcript subscription before
  reaching the PTY writer?

## 6 - Net Position

The designer pass did the important cleanup. The architecture now tells
operators one coherent story:

- persona daemon owns engine substrate;
- router owns authorized-channel state;
- mind owns adjudication and policy;
- terminal owns injection safety;
- terminal-cell owns the low-level PTY and raw byte path;
- harness owns adapter semantics and prompt patterns;
- persona-message is ingress convenience only;
- persona-system is paused until a real OS-level consumer appears.

The remaining risk is stale plan body text below the new banners. Agents
should treat the banners, 125, 126, and 127 as authoritative.
