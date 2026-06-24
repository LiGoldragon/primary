# 1 · Idea-disposition ledger — designer lane

Read `0-frame-and-method.md` first. This is the walkable ledger: every
distinct idea extracted from the 129 `reports/designer/` entries, deduped
across reports, each with a **recommended fate** — but the decision is
yours. We walk the live ones (intent + work); abandons are listed compactly
for bulk confirmation.

**312 raw ideas → 195 distinct.** Recommended split: **9 intent · 70 work · 116 abandon.**

Fate legend: **intent** = durable direction, needs your blessing → Spirit
capture. **work** = concrete buildable thing not yet tracked → new bead.
**abandon** = stale / superseded / already-landed → report retires.

## Summary by cluster

| Cluster | distinct | intent | work | abandon |
|---|--:|--:|--:|--:|
| Intent layer & Spirit | 22 | 0 | 8 | 14 |
| Schema & codegen | 30 | 4 | 9 | 17 |
| Criome (auth / cluster / quorum) | 43 | 1 | 17 | 25 |
| Mentci | 18 | 1 | 12 | 5 |
| Signal-standard & router | 10 | 1 | 5 | 4 |
| Trace / introspect / e2e | 7 | 1 | 3 | 3 |
| Mirror | 4 | 0 | 3 | 1 |
| Orchestrate & worktree | 18 | 0 | 6 | 12 |
| Guardian & guard substrate | 15 | 0 | 4 | 11 |
| Discipline & skills | 18 | 1 | 1 | 16 |
| Other (telos / persona-runtime / cloud) | 10 | 0 | 2 | 8 |
| **Total** | **195** | **9** | **70** | **116** |

## Section A — Intent candidates (need your blessing)

These nine express durable direction not yet in `INTENT.md` or Spirit.
Each becomes a Spirit record only if you confirm it. Draft statements are
my proposal, not captured.

### I-001 · Generic-impl-header emission is NEW codegen, not a free consequence of generics-as-data  — **INTENT**

A guardrail principle: emitting generic impl headers (impl<P..> Type<P..> where P: Bound) is genuinely new codegen requiring a parameter-bound vocabulary as prerequisite; parameterized-decl impls stay suppressed until both land. Recurs across the whole 654-666 arc but is not a discrete record.

- origins: 654-generics-traits-as-data-review.md
- why: Not in the intent digest; t5wx (capability set closed) and zjmc (declare-once frames) do not state this overclaim-guardrail, which gates whether generic impl emission is in scope.
- draft: Principle: Emitting generic impl headers is genuinely new codegen capability (needs a parameter-bound vocabulary first), never a free consequence of treating generics as data; parameterized-declaration impls stay suppressed until both land.

### I-002 · A component's generated output is a concrete owned interface, never a persisted generic alias  — **INTENT**

Reaction-frame codegen via expansion (binder->argument substitution into a concrete owned enum) over generic-alias: the frame's genericity is a schema-authoring convenience that must not persist into a component's generated output; true generics live only in hand-written polymorphic runtime code.

- origins: 656-reaction-frame-codegen-design.md, 657-concrete-interface-vs-persisted-generic.md
- why: Not captured in the digest; zjmc says declare-once frames but does not rule that generated output is concrete-owned, never a persisted generic alias. The expansion mechanism itself is built (tracked by primary-9gkn/8dcn) but the principle is uncaptured.
- draft: Principle: A component's generated output gets a concrete owned interface (own enum + constructors/From/codecs), wire-byte-identical to a generic alias; genericity is schema-authoring convenience plus hand-written runtime polymorphism, never stamped into component output.

### I-003 · Soft Absent-marker omission over a single maximal reaction frame  — **INTENT**

Because hard type-level leg omission via enum Never is impossible under the wire derives, unused reaction-frame legs bind to a derivable Absent marker (constructible but never constructed) on one maximal frame, rather than per-component bespoke frames. A single repetition-vs-hard-type-safety tradeoff awaiting psyche ratification.

- origins: 621-schema-generics-impl-plan-and-open-decisions-2026-06-13.md
- why: Not in the digest; no record names the soft-omission tradeoff. Genuine durable design decision flagged for psyche ratification, distinct from zjmc/n6fz (declare-once-apply-per-component).
- draft: Decision: Use one maximal reaction frame with unused legs bound to a derivable Absent marker (soft omission), accepting that hard type-level omission is impossible under the wire derives.

### I-004 · Name the paradigm 'Structural Forms'  — **INTENT**

A terminology decision proposing 'Structural Forms' (alias 'Shape Grammar') as the name for the language-is-data paradigm where the grammar IS a type matched by shape recursively, the type IS the parser, and node-types being data makes the language open.

- origins: 627-structural-forms-the-concept.md
- why: The underlying concept is already intent (7c71/2zed/ospz) but the paradigm NAME is not a recorded term anywhere; the report explicitly asks the psyche to confirm or coin it.
- draft: Decision: Adopt 'Structural Forms' as the name for the schema language-is-data paradigm (the grammar is a type matched by shape; the type is the parser; node-types are data so the language is open).

### I-005 · Fork D: generic agreement primitive with closed claim vocabulary  — **INTENT**

The agreement machine agrees on facts/state generally (stamped-quorum-over-a-proposition already spans auth, time, admission, reconciliation); authorization is the first/most-used application, not a privileged core; keep the primitive generic but the claim vocabulary closed.

- origins: 678-criome-agreement-machine-visual.md
- why: a durable framing (generic stamped-quorum agreement primitive, authorization as first application, closed claim vocabulary) proposed as a Clarify of m0p2's 'for authorization' wording but not yet applied per the 682 audit; recommendation only, needs psyche blessing.
- draft: Clarification: criome's quorum is a generic stamped-agreement-over-a-proposition primitive (auth/time/admission/reconciliation are all applications); authorization is the first application, not the core, and the claim vocabulary stays closed (deliberate schema additions only).

### I-006 · MCP is a thin per-component CLI-edge wrapper, never inter-component transport  — **INTENT**

If MCP is ever adopted for this stack it must remain a thin per-component wrapper around the existing one-NOTA-string CLI edge (an MCP tool mentci(nota)->nota forwarding to the local daemon socket), never component-to-component transport — that role stays owned by signal-frame and the daemon-binary-only-startup rule.

- origins: 712-criome-mentci-overview-and-io.md
- why: a durable boundary constraint not covered by existing transport intent (4oev/b1vi/o2xk/ur16 address NOTA-free inter-component wire but not MCP specifically); would guide any future MCP adoption.
- draft: Constraint: MCP, if adopted, is only a thin per-component wrapper around the one-NOTA-string CLI edge — never component-to-component transport, which stays owned by signal-frame binary wire and the daemon-binary-only-startup rule.

### I-007 · Home of the per-frame BLS attestation envelope (peer-lane type placement)  — **INTENT**

Peer-frame mechanics reuse signal-frame, AttestedMoment and the (signer,nonce) replay family lift to signal-standard, and only the agreement verbs live in signal-criome — but the home of the per-frame BLS signature envelope (PeerAttestation/RouterPeerAttestation), transport-property (signal-frame) vs cross-component-standard (signal-standard), is an explicitly open seam needing an explicit decision.

- origins: 683-design-review-and-networking
- why: a durable cross-library boundary decision shaping the contract architecture; eeeo defines signal-standard's charter but not this specific placement, and it is not captured or beaded.
- draft: Decision: The per-frame BLS attestation envelope (PeerAttestation/RouterPeerAttestation) lives in <signal-frame as a transport property | signal-standard as a cross-component standard> — peer-frame mechanics reuse signal-frame, AttestedMoment + the (signer,nonce) replay family live in signal-standard, agreement verbs live in signal-criome.

### I-008 · VM-proof runNixOSTest as staged release gate for live multi-daemon integration  — **INTENT**

Make a criome+mentci runNixOSTest on Prometheus a release gate for landing live multi-daemon behavior (approval loop, peer transport, registry liveness), but NOT for pure contract/lib work — i.e. gate integration, not every change.

- origins: 709-mentci-criome-orchestrate-problems-and-decisions.md
- why: durable directive about release-process shape not in the intent digest (closest are test-cluster cpip and tests-prove-real-behavior aipc, neither names a VM-proof gate); flagged by designer for psyche ratification.
- draft: Constraint: live multi-daemon behavior (approval loop, peer transport, registry liveness) is gated on a passing criome+mentci runNixOSTest on Prometheus; pure contract/lib changes are exempt.

### I-009 · Sequence durable-write before externally-visible pulse; never swallow a fallible ask  — **INTENT**

A Principle against commit-before-confirm plus swallowed Results: never `let _ =` a fallible actor/socket ask, and sequence the durable write before the externally-visible pulse. The footgun recurs structurally in spirit, criome, mentci, introspect, and mentci-egui.

- origins: 722-Audit-recent-criome-mentci-work.md
- why: genuinely-new durable Principle closing a confirmed gap: existing typed-Error discipline catches untyped errors but not typed-error-swallowed; not in the intent digest and not a bead (psyche leaned yes in report 722).
- draft: Principle: Sequence the durable write before the externally-visible pulse, and never `let _ =` a fallible actor or socket ask — a typed Result swallowed into success is as wrong as an untyped error.

## Section B — Work candidates (proposed beads)

70 concrete buildable things not yet tracked as beads. Grouped by cluster;
each carries a proposed bead title + lane. We can approve per-cluster.

### B · Intent layer & Spirit (8)

- **I-010** Reconcile ~10 INTENT.md/ARCHITECTURE.md files presenting scaffold as live
  - Across criome/mentci/introspect/spirit and others, per-repo intent/arch docs present inert scaffold as shipped fact; mark scaffold as scaffold.
  - bead: Reconcile per-repo INTENT.md/ARCHITECTURE.md to mark inert scaffold as scaffold (criome/mentci/introspect/spirit et al), including spirit guard against becoming its own mirror peer and stale criome/INTENT.md ESSENCE cross-ref | lane: designer
  - why-now / origins: Concrete confirmed doc-reconciliation across named repos; not a tracked bead. (Folds in the spirit self-mirror guard-note and the spirit-meta and criome cross-ref fixes as part of the same doc sweep.)  ·  722-Audit-recent-criome-mentci-work.md, 685-cross-machine-self-mentci-criome-tiers, 675-system-with-perspective
- **I-011** Spirit live in-place Store::adopt_head
  - A peer adopts an announced head into its running store rather than reconstructing via a fresh import.
  - bead: spirit: implement live in-place Store::adopt_head (adopt announced head into running store, not fresh import) | lane: operator
  - why-now / origins: Concrete spirit Store capability (live in-place adoption) distinct from the promoted import_from_bundle method and not in the open bead digest.  ·  694-cluster-propagation-poc
- **I-012** Spirit single-source meta types from meta-signal-spirit
  - Spirit keeps a local schema/meta-signal.schema with no dependency on meta-signal-spirit, violating the meta single-source rule.
  - bead: spirit: single-source meta types from meta-signal-spirit, remove local schema/meta-signal.schema | lane: schema-operator
  - why-now / origins: Concrete discipline-violation fix (point spirit at meta-signal-spirit, drop local meta schema) not built and not a bead; intent rule exists (cgd8/pb1g) but the fix is unbuilt residue.  ·  675-system-with-perspective
- **I-013** Agent-proposes/psyche-blesses corpus-agglomeration Supersede pipeline
  - Cluster records by domain+similarity and emit ready-to-confirm multi-target Supersede records showing quoted sources beside merged text; run three pilot clusters.
  - bead: spirit: build agent-proposes/psyche-blesses corpus-agglomeration Supersede pipeline (cluster by domain+similarity, emit ready-to-confirm multi-target Supersede) and run three pilot clusters | lane: schema-operator
  - why-now / origins: Concrete buildable agglomeration tool not yet a bead, distinct from the standing auditor-lane intent (2gj4/ek8w) and refresh-as-skill (tf2o).  ·  617-spirit-guardian-corpus-health-and-referent-activation-2026-06-13.md
- **I-014** Interim off-host backup of spirit.sema
  - The authoritative log is one local spirit.sema with no off-host mirror in the running daemon; add an interim periodic off-host push until the production shipper lands.
  - bead: Add interim off-host backup of spirit.sema (periodic restic/rclone push of the rebuildable file) until production shipper wiring lands | lane: system-operator
  - why-now / origins: Interim safety-net is concrete buildable residue NOT covered by the proper-fix beads primary-85hv (production mirror shipper) or primary-x3l7 (mirror ingress hardening).  ·  615-sema-vc-system-and-spirit-pilot-opus-review-2026-06-13.md
- **I-015** Decouple every-boot migration from daemon liveness
  - Every-boot migration couples migration failure to daemon liveness and the closed detection range wedges boot on a forward-skewed store; treat a forward/unknown generation as already-newer instead of a hard ExecStartPre failure.
  - bead: spirit: decouple every-boot migration from daemon liveness, treat forward/unknown store generation as already-newer (let daemon open) not a hard ExecStartPre failure | lane: system-operator
  - why-now / origins: Likely overnight-outage cause; concrete buildable residue not found as a bead (closest bead primary-4civ only adds failure escalation around ExecStartPre, not forward-skew degrade).  ·  615-sema-vc-system-and-spirit-pilot-opus-review-2026-06-13.md
- **I-016** Crash-injection tests + delete v1-v6 migration readers
  - The hard-link+rename crash-safety swap has no crash-injection test and v1-v6 migration conversions have zero coverage; psyche confirmed old stores disposable, so delete readers and add crash tests.
  - bead: sema-engine/spirit: delete untested v1-v6 migration readers (psyche-confirmed old stores disposable) + add crash-injection tests for the hard-link+rename migration swap | lane: schema-operator
  - why-now / origins: Concrete buildable residue with a psyche ruling (report 616 Q3: delete v1-v6 readers, reject pre-current loudly) but no tracked bead.  ·  615-sema-vc-system-and-spirit-pilot-opus-review-2026-06-13.md
- **I-017** Seal kernel write surface + single SchemaHash construction path
  - The exclusive-DB invariant (fosp) is a doc-comment not a type proof (Sema::write pub, kernel table re-exported); seal it and drop the SchemaHash::for_label stringly back-door.
  - bead: sema-engine: seal the kernel write surface to type-enforce the exclusive-DB invariant (fosp) and give SchemaHash one schema-derived construction path (drop the for_label back-door) | lane: schema-operator
  - why-now / origins: Concrete buildable discipline fixes not clearly tracked; the RecordKey-as-string sibling finding already landed (bead primary-s22j, sema-engine 909eaa0b) but seal+for_label remain.  ·  615-sema-vc-system-and-spirit-pilot-opus-review-2026-06-13.md

### B · Schema & codegen (9)

- **I-018** Finish the schema-rust-next emission stack (663-arc back half + narrow-stack finish)
  - The unbuilt back half of the codegen plan: flip standard newtype/scalar impls to default-on (gated on scalar_like / transitive-scalar leaf-following), emit struct field accessors + enum is_/as_ predicates, add VariantMatch for the enum-rewrap class, and convert the residual ~8 emitter panic!/assert! to typed SchemaError; shape-derived Capability resolution behind it.
  - bead: Finish schema-rust-next emission stack: flip standard newtype/scalar impls default-on (scalar_like + transitive-scalar leaf-following), emit struct/enum accessors, add VariantMatch for enum-rewrap, convert ~8 emitter panic!/assert! to typed SchemaError | lane: schema-operator
  - why-now / origins: Distinct from the integration/migration beads primary-9gkn (integrate generics+reaction branches) and primary-8dcn (14-component migration); these are concrete unbuilt emitter slices not covered by any open bead. Some scalar-impl scope decisions (Q2/Q3/Q4) gate on quick psyche confirms.  ·  666-have-what-we-need-and-the-port-plan.md, 692-schema-and-schema-rust-gaps.md
- **I-019** Choose the neutral importable home for reaction.schema
  - Where reaction.schema physically lives (own crate vs alongside signal-frame vs self-registered per daemon) is deliberately open and must resolve before the 14-component fan-out, since it sets the import-target string and the emission boundary.
  - bead: Decide and create the neutral importable home repo/crate for reaction.schema (sets import-target + emission boundary for the 14-component fan-out) | lane: system-operator
  - why-now / origins: Concrete undecided prerequisite blocking the primary-8dcn fan-out; reaction.schema currently lives only as a schema-next fixture and no bead names this neutral-home decision.  ·  621-schema-generics-impl-plan-and-open-decisions-2026-06-13.md
- **I-020** nota-next derive: reconcile and re-land named-field/struct-body/sum-head structural derive
  - The nota-next StructuralMacroNode derive needs named-field pascal_head/body variants and sum-typed heads to shrink the hand-written TypeReference top-level seed; the structural-forms tracker (#411/#416) says these landed but nota-next HEAD rejects both, so the owner must re-land or close the tasks to match code.
  - bead: nota-next derive: re-land or close #411/#416 (named-field pascal_head/body + sum-typed head variants) to match HEAD, shrinking the hand-written TypeReference seed | lane: schema-operator
  - why-now / origins: Concrete nota-next derive extension + a tracker-vs-code reconciliation, neither covered by an open bead (closest, primary-cxyf, is the structural-forms integration, not the derive re-land/reconcile).  ·  631-typeref-reconciliation-outcome.md, 691-gaps-and-drifts-fixed.md
- **I-021** schema-next: route Family-body parsing through a typed structural-macro node (retire hand-parse)
  - schema-next's Family-body parsing still uses a hand-written chunks_exact(2) + field-name match, a live v0n6 (no-hand-rolled-parsers) violation; route it through a typed structural-macro node instead.
  - bead: schema-next: route Family-body parsing through a typed structural-macro node, retiring the chunks_exact(2) hand-parse (v0n6) | lane: schema-operator
  - why-now / origins: Concrete v0n6-violation cleanup on a live code path, not covered by any open bead.  ·  692-schema-and-schema-rust-gaps.md
- **I-022** Build the real RustSurface crate-parse populator + impl-reference method-call resolver
  - The impl-reference grammar/round-trip/enumerable-catalog/out-of-band-verification prototype is real and pushed, but the real RustSurface populator (parse an actual Rust crate's impls to feed verify_catalog) and the method-call resolver (resolve a schema-authored call against shape-capabilities union the extern catalog) are the deferred capstone.
  - bead: schema-next: build the real RustSurface crate-parse populator + the method-call resolver consuming the impl catalog (fold next/schema-capability-resolution 3709fc1; bring macro/document lowering path to parity) | lane: schema-operator
  - why-now / origins: The capstone consuming the impl catalog is explicitly deferred and unbuilt beyond the green prototype; no open bead tracks it (integration-bar fixes from 699 are separate and done).  ·  696-impl-reference-prototype.md
- **I-023** schema-rust-next: emit the guardian verdict-type triad as a schema macro
  - Schema-macro extraction of the verdict-type triad (binary verdict over a closed reason enum + its NOTA grammar + harness-fallback constructors), emitted from schema-rust-next, replacing the repetition that recurs per guardian, per referent-guardian, and for any future admission gate.
  - bead: schema-rust-next: emit the guardian verdict-type triad (binary verdict over closed reason enum + NOTA grammar + harness-fallback constructors) as a reusable schema macro | lane: schema-designer
  - why-now / origins: The correctness half (render grammar from enum in-repo) shipped; the emitter extraction is explicitly the next step and aligns with standing intent xprx but is not a tracked bead.  ·  609-guardian-justice-built.md
- **I-024** Fix orchestrate contract-fidelity bugs + add wire round-trip tests to every contract delta
  - Generated wire-layer correctness bugs on main: signal-orchestrate's generated mirror and canonical struct disagree on the Worktree status field name (root cause schema/lib.schema:45); meta-signal-orchestrate carries a hand-rolled WorktreeIndexRefreshed NOTA codec that violates no-hand-rolled-parsers and disagrees with its own schema; and the contract deltas this wave shipped with zero round-trip test coverage.
  - bead: Fix orchestrate contract-fidelity bugs (Worktree status field-name skew at schema/lib.schema:45, hand-rolled WorktreeIndexRefreshed NOTA codec) + add wire round-trip tests to every contract delta (signal-orchestrate/meta-signal-orchestrate/signal-mentci/signal-criome) | lane: operator
  - why-now / origins: Concrete correctness bugs on main plus a real test gap, not yet fixed and not a tracked bead; no-hand-rolled-parsers and wire-round-trip discipline are intent (rust/parsers.md, aipc/b2jg) so these are violations.  ·  708-yesterday-designer-work-audit
- **I-025** Reconcile signal-agent artifact-freshness against current schema-rust-next pin
  - Live pin-skew: a fresh resolve bumped schema-rust-next so signal-agent main fails its artifact-freshness check (RetiredStructFieldSyntax 'Model.'); resolved locally only by seeding Cargo.lock from main. Operator/system should regenerate signal-agent artifacts against current schema-rust-next.
  - bead: signal-agent: regenerate artifacts against current schema-rust-next to clear the RetiredStructFieldSyntax 'Model.' freshness failure (replace the local Cargo.lock-from-main workaround) | lane: schema-operator
  - why-now / origins: Concrete operator/system reconciliation of a live pin-skew, not a tracked bead.  ·  727-Thin-end-to-end-proof-and-parallel-lane-finding.md
- **I-026** router: live authorized-object fan-out (Attend/Withdraw + durable attendance table)
  - The Differentiator (ComponentKind, AuthorizedObjectKind) cross-product coordinate and interest-bearing subscription token landed; the remaining unbuilt piece is the router-side live fan-out: Attend/Withdraw verbs and a durable attendance table keyed by the standard interest coordinate so publish becomes a one-line filter instead of fan-to-everyone.
  - bead: router: live authorized-object fan-out — Attend/Withdraw verbs + durable attendance table keyed by the standard differentiator/interest coordinate | lane: operator
  - why-now / origins: The decision is captured (Spirit l2ha) and the token landed (criome/signal-criome main), but the router live fan-out is designed-not-built (reports 682/683) and not a bead. (Edge of cluster but the schema-coordinate is the load-bearing part.)  ·  680-telos-integrated-poc

### B · Criome (auth / cluster / quorum) (17)

- **I-027** criome-auth watch rides the tracing surface (criome-auth trace event)
  - Spirit emits a criome-authorization trace event in its testing-trace vocabulary so the watch rides trace->introspect->mentci, reusing the introspect query path; later evolves into the gate.
  - bead: spirit: add a criome-authorization trace event to the testing-trace vocabulary so the criome-auth watch rides trace->introspect->mentci | lane: operator
  - why-now / origins: a concrete buildable increment (one new trace event type), confirmed Duplicate as intent (covered by m5jl/xqkv/80bl/7x5z/2st7) but not yet a tracked bead.  ·  721-Status-production-watch-and-cleanup.md, 722-Audit-recent-criome-mentci-work.md
- **I-028** Arm the criome gate in the shipped spirit daemon (production watch GATE half)
  - Wire spirit daemon startup / meta-signal config to build a real SpiritAttestor from an admitted contract digest + signer keypair, call arm_criome_gate in Observing mode, and deploy a launchable production mentci pointed at the local criome meta socket.
  - bead: spirit-production: arm the criome gate from authenticated meta-signal config (SpiritAttestor from contract digest + signer keypair) + deploy a launchable production mentci in Observing mode | lane: operator
  - why-now / origins: arm_criome_gate is cfg(mirror-shipper) and called only by tests; SpiritAttestor is a test fixture (reports 721/722 confirm the gate is compiled out and never armed in the shipped daemon); no matching bead.  ·  721-Status-production-watch-and-cleanup.md
- **I-029** Make criome SubmitAuthorizationApproval idempotent + honest replies + TTL
  - Status-guard the approval (return early when status != Parked), store-before-pulse and stop discarding the store Result, add honest AlreadyDecided/SlotNotFound/store-failure reply variants, and add a parked-request TTL/auto-expiry.
  - bead: criome: make SubmitAuthorizationApproval idempotent (terminal-state guard, store-before-pulse, honest AlreadyDecided/SlotNotFound/store-failure replies) + parked ClientApproval TTL/auto-expiry | lane: operator
  - why-now / origins: replay-unsafe/non-idempotent authorization bug still open from 714 (root.rs:406-482) plus missing honest-reply contract variant and unbounded parked-request accumulation; not a tracked bead.  ·  722-Audit-recent-criome-mentci-work.md, 714-Audit-operator-bootstrap.md
- **I-030** Deploy a second criome on Prometheus (multi-node quorum plane)
  - Build the second criome on Prometheus with double-sign + missing-co-signature watcher as part of the first general-substrate build, coordinated with the landed ObjectCoSignature/CoSignatureExpectation contracts.
  - bead: system-operator: deploy a second criome on Prometheus with double-signature + missing-co-signature watcher (multi-node quorum plane) | lane: system-operator
  - why-now / origins: concrete multi-node deploy realizing pviw/7let/ic4o; co-signature contracts already landed on main (report 725) but the 2nd-criome deploy is not covered by any bead.  ·  724-Design-guard-substrate-contracts.md
- **I-031** BLS12-381 aggregate verification (FastAggregateVerify + PoP-on-admission)
  - Implement BLS aggregate verification replacing the per-signature pairing loop so the direct-lane latency win does not collapse, with proof-of-possession folded into cluster-root admission.
  - bead: criome: BLS12-381 aggregate verification (FastAggregateVerify same-message path + PoP-on-admission) replacing the per-signature quorum loop | lane: schema-operator
  - why-now / origins: psyche leaned ship-it-in-v1 (684/4); still the per-signature loop in use; not covered by any bead (kr40 is real Sign/Verify + master-key lifecycle, not aggregate verification).  ·  684-design-woes
- **I-032** Cluster-root provisioning ceremony / AdmitRegistration minting CLI
  - Build the out-of-band cluster-root provisioning ceremony: an offline Criome CLI (AdmitRegistration) that mints cluster-root-signed admission envelopes, or a pre-bootstrap registration API; the admission gate is built and tested but nothing mints envelopes outside tests.
  - bead: criome: cluster-root AdmitRegistration ceremony CLI that mints cluster-root-signed admission envelopes (offline / pre-bootstrap API) | lane: schema-operator
  - why-now / origins: repeatedly-named nearest live-e2e unblock (684 Woe 6, 669/675/677/678/682, 701 E2); not built; adjacent beads (kr40, 5zur, at7x) do not cover cluster-root admission minting.  ·  684-design-woes, 669-first-e2e-offline-build, 701-multi-machine-criome-cluster-roadmap.md
- **I-033** Peer-responder enforces three-layer auth boundary with distinct reasons
  - Keep transport reachability, cluster-root peer admission, and BLS quorum membership syntactically distinct in signal-criome and the peer-responder handler, with distinct rejection reasons, so transport-fact is never conflated with membership-fact.
  - bead: criome: peer-responder handler enforces the three-layer auth boundary (transport vs peer-admission vs quorum-membership) with distinct rejection reasons + tests | lane: schema-operator
  - why-now / origins: concrete handler clarity + test task on the not-yet-written peer-responder (684 Woe 7); lt44 covers the two transport lanes but not the three-check non-implication; not a bead.  ·  684-design-woes
- **I-034** Collapse decline reasons to coarse PolicyRefused + document coauthority trust
  - Mitigate the irreducible k-of-n metadata leak by collapsing fine-grained decline reasons to a coarse PolicyRefused for untrusted callers (peer-trust table + conditional reason-hiding) and documenting coauthority trust discipline in criome ARCHITECTURE.md.
  - bead: criome: collapse decline reasons to coarse PolicyRefused for untrusted peers + document coauthority trust discipline | lane: schema-operator
  - why-now / origins: concrete low-severity mitigation (684 Woe 8); not built, not tracked.  ·  684-design-woes
- **I-035** Encrypted multi-key KeyStore replacing the bare MasterKey
  - Replace criome's single 0600 plaintext MasterKey with an encrypted multi-key KeyStore: mlock'd zero-on-drop self-start home key sealed under a KEK, per-KeyPurpose sub-keys via labeled HKDF-blake3, a RotateKey meta op with KeyGeneration-stamped attestations, and a SigningKey trait for later TPM/HSM.
  - bead: criome: build the encrypted multi-key KeyStore (self-start home key + per-KeyPurpose HKDF-blake3 sub-keys, sealed-at-rest, SigningKey trait, RotateKey meta op) replacing MasterKey | lane: schema-operator
  - why-now / origins: intent captured (q1le) but the build is absent (criome still has bare MasterKey) and it gates real verdict signing; not covered by kr40 (which is Sign/Verify + master-key lifecycle, not the sealed multi-key store + sub-keys + rotation).  ·  685-cross-machine-self-mentci-criome-tiers
- **I-036** Consumer-build sweep across the ~12 unaudited consumer daemons
  - Confirm the ~12 unaudited consumer daemons (message, lojix, terminal, introspect, mind, persona, cloud, domain-criome, upgrade, orchestrate, repository-ledger, triad-runtime) build after strict-positional port + sema-5 migration, Nix included, before the stack is green.
  - bead: Stack: consumer-build sweep — confirm the ~12 strict-ported + sema-5-migrated consumer daemons build under Nix before declaring the stack green | lane: operator
  - why-now / origins: the broad ~12-consumer build/migration sweep is live and untracked; only the spirit/mirror subset closed (697); not a bead.  ·  691-gaps-and-drifts-fixed.md
- **I-037** Wire the single-host criome-gated typed propagation loop to LoopProvenGreen
  - Wire the criome-gated propagation loop into the real in-repo path per the report-700 7-slice brief: add a criome client to spirit + capture the shipped head and derive D, insert the criome authorize gate, read the typed AuthorizedObjectReference back by type, replace MirrorObjectNotice with the typed reference into the router, acquire exactly D (verify-after-restore), upgrade the e2e test to assert the falsifiable C7, and retire criome's operational matcher (m0p2).
  - bead: spirit/criome/router: implement the single-host criome-gated typed propagation loop to LoopProvenGreen (700 Slices 1-7: criome gate, typed AuthorizedObjectReference, acquire-by-D verify, e2e C7, m0p2 retire) | lane: operator
  - why-now / origins: PoC proven as logic (694) but the in-repo causal loop is still PartialGreen per 697/700; Spirit jk1w makes it step 1 prerequisite; not a tracked bead. (Note: the 1-of-1 local gate landed on spirit main 90875f26, but the full typed-reference loop + acquire-by-D + m0p2 retire remain.)  ·  694-cluster-propagation-poc, 697-propagation-loop-state-blockers.md, 700-propagation-operator-brief.md
- **I-038** Adjudicator/escalation ladder beyond EscalateToPsyche
  - Build the named adjudicator rungs above criome's mechanical verify: L1 quorum, L2 named adjudicator signing a content-addressed verdict that criome verifies, L3 terminal honest fork, with EscalateToPsyche the highest rung — so EscalateToPsyche is no longer a dead-letter.
  - bead: criome: build the adjudicator ladder beyond EscalateToPsyche — named adjudicator rungs + signed-verdict-verification surface | lane: schema-operator
  - why-now / origins: framing already intent (gc0n) and three-valued EvaluationDecision landed (683), but the named rungs + signed-verdict-verification surface are unbuilt and EscalateToPsyche is a dead-letter; not a bead.  ·  674-criome-internal-engine
- **I-039** Verb-scoped quorums + meta-plane amend-contract verb + full replay quad
  - Complete the policy-language integration: verb-scoped quorums (Use/ReKey/Admit/Revoke/Amend each with its own quorum), a meta-plane define/amend-contract verb, and a full (digest,branch,version,moment) replay anchor bound into every proof.
  - bead: criome: verb-scoped quorums (Use/ReKey/Admit/Revoke/Amend) + meta-plane amend-contract verb + full (digest,branch,version,moment) replay quad | lane: schema-operator
  - why-now / origins: core integration landed (content-addressed contracts + real BLS + StoredContract SEMA family, criome main 3c051223), but verb-scoped quorums + amend-contract verb + full replay quad remain unbuilt and unbeaded.  ·  674-criome-internal-engine
- **I-040** Migrate signal-criome/signal-persona/signal-message to positional schema syntax
  - Migrate the signal-criome, signal-persona, and signal-message contract bodies to the positional dot-differentiator struct syntax now required on schema-next main and regenerate; their name-value bodies no longer parse.
  - bead: Migrate signal-criome/signal-persona/signal-message contract bodies to positional schema-next syntax + regenerate (prerequisite for signal-standard) | lane: schema-operator
  - why-now / origins: forced consumer-side migration blocking signal-standard and criome peer verbs; not covered by primary-cxyf (engine-side landing) or any other bead.  ·  682-overview-and-context-maintenance
- **I-041** Build the direct criome peer lane (peer verbs + codec + coordinator + replay)
  - Build the direct criome peer lane: a signal-criome peer verb family (Solicit/Contribution/PeerHello/PeerWelcome) over a CriomePeerFrameCodec carrying a PeerAttestation envelope, RemoteCriomeRegistry admission via CRIOME-PEER-ADMISSION-V1, a peer_coordinator that fans solicitations and assembles k contributions into the verifier, and a durable (signer,nonce) replay SEMA family.
  - bead: criome E1 peer lane: wire peer transport into the daemon serve loop (timed-out TCP listener) + nonce-bound quorum tally + 2-of-2 two-node nixosTest (increments 4-5, atop landed peer verbs/codec/registry) | lane: operator
  - why-now / origins: detailed cross-host quorum-assembly protocol; increments 1-3 built+verified on designer branches (signal-criome-peers, criome-peer-transport) per 706 but increments 4-5 (daemon serve-loop integration + nonce-bound quorum tally + 2-of-2 two-node nixosTest) are genuinely unbuilt; primary-ymww is the deploy, not this code slice.  ·  683-design-review-and-networking, 705-criome-cluster-reassessment, 706-criome-e1-peer-transport.md
- **I-042** SO_PEERCRED owner-auth on the criome meta socket / distinct Unix users
  - Implement SO_PEERCRED owner-auth (and/or run criome and mentci as distinct Unix users with the meta socket owner-restricted) so the meta-vs-working authority boundary is kernel-enforced, not path-secrecy-only.
  - bead: criome: implement SO_PEERCRED owner-auth on the meta socket (and/or distinct Unix users for criome vs mentci) to make the meta-vs-working boundary kernel-enforced | lane: operator
  - why-now / origins: intent exists (9v7h/alom name SO_PEERCRED) but the criome implementation is a confirmed gap repeated in 705 q3 and 714 q4 (criome daemon.rs:135); not a bead.  ·  705-criome-cluster-reassessment, 714-Audit-operator-bootstrap.md
- **I-043** Decide and encode where the AuthorizationGrant lives
  - The AuthorizationGrant is produced by neither end of the seam (criome stores grant:None and replies AuthorizationApprovalRecorded; mentci discards it); decide and encode in the contract + ARCHITECTURE where the grant lives — persisted in criome and observable via ObserveAuthorization, or carried back through the verdict reply into mentci's InterfaceState.
  - bead: criome/mentci: decide and encode where the AuthorizationGrant lives (persist in criome + observable via ObserveAuthorization, or carry back through the verdict reply) | lane: operator
  - why-now / origins: a design+code hole on main (root.rs:433-436); the grant is a documented concept with no home in code; no intent record names where it lives and no bead covers it.  ·  714-Audit-operator-bootstrap.md

### B · Mentci (12)

- **I-044** Create signal-mentci-egui + meta-signal-mentci-egui triad and rework mentci-egui off hand-rolled control.rs
  - Per the psyche's report-720 ruling, mentci-egui becomes a real component with its own schema-generated triad (Drive/ObserveView/SubscribeView working signal + RemoteControlMode/Configure meta signal), replacing the hand-rolled control.rs NOTA enums and folding in the dead-meta-roster cleanup (NOTA-reachable Configure, dropped config fields, dead rejection roster).
  - bead: Create signal-mentci-egui + meta-signal-mentci-egui triad and rework mentci-egui off hand-rolled control.rs (UserEvent schema-emitted, single Drive path, meta Configure binary-only, apply all config fields, wire the rejection/authority roster + ResetRemoteControl) | lane: operator
  - why-now / origins: concrete buildable repo-creation + rework; report 722 confirms the runtime is contract-complete-but-runtime-incomplete with hand-rolled remnants and a NOTA-reachable Configure, not a tracked bead (no mentci beads exist).  ·  720-Design-mentci-egui-triad.md, 722-Audit-recent-criome-mentci-work.md
- **I-045** mentci-egui: per-client view-state + DriveOrigin double-write attribution
  - Each client owns its own ObservationModel (projection/cursor/subscription tokens + remote-control mode) instead of one shared model, and each driven UserEvent carries a DriveOrigin (Local|Remote(label)) latching a DoubleWriteIndicator (Single|Contended) surfaced as a banner.
  - bead: mentci-egui/mentci-lib: model per-client view/subscription state + implement DriveOrigin attribution + DoubleWriteIndicator so DualWrite is distinct from RemoteEnabled | lane: operator
  - why-now / origins: report 722 findings (medium) confirm multi-client view-state is unmodeled (one shared remote_control_mode) and DriveOrigin/DualWrite attribution is built nowhere; not a tracked bead.  ·  719-Design-driveable-mentci-client.md
- **I-046** Build the real mentci daemon over mentci-lib (kameo, durable SEMA, verdict egress)
  - The mentci repo is a schema-only skeleton with no Cargo.toml; build the actual daemon (kameo actor over mentci-lib's state machine, schema-emitted SEMA with durable self-resume, Nexus ops, eaf7 socket, one binary rkyv config via meta-signal-mentci, verdict egress to home criome).
  - bead: mentci: build the daemon over mentci-lib's state machine (kameo actor, durable schema-emitted SEMA, Nexus ops, eaf7 socket, binary rkyv config, verdict egress to home criome) | lane: operator
  - why-now / origins: the daemon binary is unbuilt (689 confirms schema skeleton, no Cargo.toml) and untracked; realizes existing ur16/kzk5 self-resume override but is the unmet mentci side.  ·  687-mentci-full-component
- **I-047** Resolve LiGoldragon/mentci remote-name collision + push the four component repos
  - The LiGoldragon/mentci GitHub remote currently resolves to a repo named 'workspace'; resolve that namespace collision (psyche call) and push signal-standard/signal-mentci/meta-signal-mentci/mentci to real remotes so the daemon depends via git rather than forbidden local-path deps.
  - bead: mentci: resolve LiGoldragon/mentci remote-name collision (psyche call) + push the four component repos to real remotes | lane: operator
  - why-now / origins: operational push/namespace task gating the running daemon (689 names it the one open item), untracked; carries a psyche-decision sub-item on the GitHub namespace.  ·  687-mentci-full-component
- **I-048** mentci daemon: persist SEMA state / reconcile from criome on restart
  - mentci daemon state is in-memory while criome persists, yielding orphaned parked authorizations and duplicate-grant-after-restart (empty dedup set re-mints question ids); give mentci a persisted SEMA store or criome-snapshot reconciliation on startup and write the restart contract into INTENT/ARCHITECTURE.
  - bead: mentci daemon: persist SEMA state (or reconcile from criome snapshot on startup) + write the restart contract into mentci INTENT/ARCHITECTURE | lane: operator
  - why-now / origins: high/missing-design confirmed on main in report 714 (state.rs); the self-resume-from-SEMA override (kzk5/ur16) is unmet on mentci; not a tracked bead.  ·  702-deep-engine-analysis, 714-Audit-operator-bootstrap.md
- **I-049** mentci daemon: surface criome rejection instead of unconditional VerdictAccepted
  - The daemon-to-criome verdict seam silently succeeds under failure ('let _ = bridge.submit_criome_verdict(&verdict)?' discards the Output discriminant), so clients are told VerdictAccepted even on unknown-slot/DependencyNotReady or a recorded Reject; inspect the criome Output and return a Rejection on mismatch.
  - bead: mentci daemon: inspect criome SubmitAuthorizationApproval Output and return Rejection on unknown-slot/Reject instead of unconditional VerdictAccepted | lane: operator
  - why-now / origins: high live bug on main (report 714, daemon.rs:137 + criome root.rs:425), pending a psyche decision on intended behavior; not a tracked bead.  ·  714-Audit-operator-bootstrap.md
- **I-050** mentci correctness/security cluster: rollback, Defer delivery, remote-answer guard, subscription consumer
  - On main: mentci commits local state before criome confirms with no rollback, Defer is structurally undeliverable, remote AnswerQuestion bypasses the criome-write-access guard the local UI enforces, and client shells run the synchronous one-shot path INTENT forbids with no subscription consumer.
  - bead: mentci+mentci-egui: rollback on criome rejection, deliver Defer, enforce criome-write-access on remote AnswerQuestion, add the subscription consumer (drop the synchronous one-shot path) | lane: operator
  - why-now / origins: report 722 high root causes D/F/G/H confirmed with file:line on current main; no matching bead.  ·  722-Audit-recent-criome-mentci-work.md
- **I-051** mentci-lib: make the Error surface load-bearing + clear slot on RetractObservation
  - mentci-lib swallows errors behind a decorative Error module (unknown-question/unknown-token/unheld-token paths return empty Vec indistinguishable from success), and RetractObservation emits the Cmd without clearing the local slot, leaving a retracted token that still passes the fold guard.
  - bead: mentci-lib: return typed errors on unknown-question/token/unheld-token paths, clear slot on RetractObservation, add distinguishing tests | lane: operator
  - why-now / origins: correctness hazard on the approval control surface (708-5 finding 3), distinct from the 714 Defer bug, not a tracked bead.  ·  708-yesterday-designer-work-audit
- **I-052** mentci post-answer refresh (Observe-on-VerdictAccepted now; daemon-pushed deltas later)
  - After a client answers, the GUI/model does not refresh (question moves pending->answered and grant is recorded but view stays stale until manual observe); cheap MVU fix now is to emit an Observe Cmd on the VerdictAccepted event, durable fix is daemon-pushed InterfaceState deltas on the observation token signal-mentci already returns.
  - bead: mentci: emit an Observe Cmd on VerdictAccepted (post-answer refresh) now + design daemon-pushed InterfaceState deltas on the observation token as the durable follow-on | lane: operator
  - why-now / origins: live-confirmed high in report 714; realizes existing push-not-poll intent (brgo/c5nq) but unmet; not a tracked bead.  ·  714-Audit-operator-bootstrap.md
- **I-053** criome+mentci two-daemon nixosTest keystone on Prometheus
  - The end-to-end proof: one guest runs both daemons under the same criome system user (0600 meta-socket as a real OS boundary), criome flipped to ClientApproval, parks an authorization, mentci surfaces it as CriomeEscalation(slot) with criome_access=ReadWrite, the test answers, mentci routes the verdict by slot, criome records the grant; needs mentci/flake.nix + mentci.nix module + an observe-answer witness bin + criome-mentci-node.nix.
  - bead: criome+mentci nixosTest keystone: add mentci/flake.nix + mentci.nix module + observe-answer witness bin + criome-mentci-node.nix and run on Prometheus, one end-to-end owner | lane: operator + system-designer
  - why-now / origins: fully designed (713) but structurally unbuildable today (714 gaps a-e: mentci has no flake, no NixOS modules, encoder bin-name mismatch); repeatedly named the highest-leverage task; not a tracked bead.  ·  711-mentci-bootstrap-phase2-mode-card-and-handoffs.md, 713-criome-mentci-nixostest-draft-and-cli-status.md, 714-Audit-operator-bootstrap.md
- **I-054** mentci CLI all-paths completeness (render generic path, retract:/propose: atoms)
  - Route the generic inline-NOTA/.nota/binary fallback through ClientReplyRender so it prints readable reply NOTA like the atoms (factoring the socket exchange onto FrameCodec::exchange), add the cheap write atoms retract:<token> and propose:<id>:<text>, and add a read-only rejection test.
  - bead: mentci CLI: render the generic NOTA reply path via ClientReplyRender (FrameCodec::exchange), add retract:/propose: write atoms, add a read-only rejection test | lane: operator
  - why-now / origins: report 714 re-confirms the gaps (generic path emits raw binary, hand-rolled atom parsing, missing atoms); realizes intent isia (CLIs are complete typed text edges); operator's in-flight surface but not a tracked bead.  ·  713-criome-mentci-nixostest-draft-and-cli-status.md
- **I-055** mentci README.md stale criome:* CLI atoms
  - mentci/README.md lines 15-18 still document removed criome:* CLI atoms (criome:parked / criome:approve|reject|defer:<slot>) the current CLI no longer recognizes; update to the observe-only roster to match the CLI and ARCHITECTURE.md.
  - bead: mentci: update README.md to remove stale criome:* CLI atoms and match the current observe-only roster + ARCHITECTURE.md | lane: operator
  - why-now / origins: concrete small doc-correctness fix (criome:* atoms removed in cab247b/25acda3), not captured as a bead.  ·  712-criome-mentci-overview-and-io.md

### B · Signal-standard & router (5)

- **I-056** signal-orchestrate drop mirror decision/outcome types
  - signal-orchestrate hand-maintains its own StepOutcome/EvaluationDecision that mirror signal-criome nouns, making typed step outcomes lossy to route; the orchestrate nexus effect schema should reference signal-criome nouns directly so one decision type world spans the guard chain.
  - bead: signal-orchestrate: drop duplicate mirror EvaluationDecision/StepOutcome, cross-import signal-criome nouns (one decision type world) | lane: schema-operator
  - why-now / origins: concrete cross-import cleanup (drop the mirror types), aligned with the 'source of truth remains signal-criome' principle; no matching open bead.  ·  727-Thin-end-to-end-proof-and-parallel-lane-finding.md
- **I-057** Router closure lock convergence
  - Router main and its newest transitive signal-router/signal-message/signal-persona/schema-rust-next are not one freely-updatable closure; converge the pinned lock so a future cargo update doesn't re-break router types.
  - bead: router: verify-and-converge the closure lock (signal-router/signal-message/signal-persona/schema-rust-next ahead-of-lock) so cargo update doesn't re-break router types | lane: operator
  - why-now / origins: concrete verify-then-converge lock task for four ahead-of-lock crates; not tracked by any open bead.  ·  697-propagation-loop-state-blockers.md
- **I-058** Router m3: real criome forward-attestation + off-mailbox replay + Nix modules
  - Build-ready router m3 design: a CriomeForwardAttestation verifier delegating to local criome, a router-owned seen-(signer,nonce) replay window off-mailbox with a sixth router.sema replay family (schema 2->3), async verifier trait, plus criome.nix/message-router.nix NixOS modules and a MessageFabric capability.
  - bead: router m3: real criome forward-attestation + off-mailbox replay/freshness window (router.sema schema 2->3) + async verifier + criome.nix/message-router.nix modules + MessageFabric capability | lane: cloud-operator
  - why-now / origins: concrete build-ready logic and deploy modules that exceed the deploy-only bead primary-ymww and have no implementation bead; deferred by the 'no key encryption for now' steer but still live buildable residue.  ·  669-first-e2e-offline-build
- **I-059** Create signal-standard shared library + migrate consumers
  - Create signal-standard (second non-component shared signal- library) owning domain-free cross-component standards: a closed-but-partitioned 14-variant ComponentKind roster plus Differentiator, AuthorizedObjectKind/Interest lattice/Reference, ComponentClassification; migrate signal-criome/signal-persona/signal-message and retire ComponentPrincipal/ComponentName.
  - bead: Create signal-standard shared library (14-variant ComponentKind + Differentiator/interest lattice) and migrate signal-criome/signal-persona/signal-message consumers | lane: schema-operator
  - why-now / origins: the decision is captured as Spirit eeeo but the buildable deliverable (create the crate + migrate three consumers) is designed/validated and not yet beaded.  ·  681-signal-standard
- **I-060** Retire local ComponentKind forks by importing signal-standard
  - signal-criome carries a genuinely divergent 7-variant ComponentKind (vs signal-standard's 14) and meta-signal-mentci a matching local copy; import signal-standard to retire both forks (signal-mentci has no local copy).
  - bead: signal-standard: import ComponentKind/SocketPath/StandardSocket into signal-criome (retire 7-variant fork) and retire meta-signal-mentci's local copy | lane: operator
  - why-now / origins: a concrete collapse-the-duplicate-contract-type task repeatedly surfaced (702/703/708/709), handed to operator but not landed and not a tracked bead.  ·  702-deep-engine-analysis

### B · Trace / introspect / e2e (3)

- **I-061** introspect CLI ComponentTrace query + config-encode binary
  - The introspect CLI cannot issue a ComponentTrace query (single-variant PrototypeWitness input) and introspect ships no config-encode binary, forcing witness-binary workarounds in the runbook. Add ComponentTrace to the CLI surface and ship an introspect config-encode binary.
  - bead: introspect: add ComponentTrace to CLI surface input + ship a config-encode binary | lane: operator
  - why-now / origins: concrete buildable gaps flagged in report 717 (surface.rs:24 single-variant input; no encode binary in Cargo.toml); no matching open bead.  ·  717-Runbook-mentci-introspect-live.md
- **I-062** Fix the dead trace plane (producer/consumer mismatch + record key + sequence + faults)
  - The trace plane is inert end-to-end on main: producer stamps engine=socket-path while consumer queries engine='prototype' (zero matches), the record key omits layer/event_name, per-process sequence resets to 0 on restart (silent overwrite), component is mislabeled Signal, and the drain loop swallows all faults. Open question: EngineIdentifier source-of-truth and whether spirit/criome get dedicated IntrospectionTarget variants.
  - bead: Fix the dead trace plane: align producer/consumer EngineIdentifier, add layer+event_name to record key, persist trace sequence across restart, stop mislabeling component as Signal, surface drain faults | lane: operator
  - why-now / origins: confirmed high-severity bugs on current main (spirit trace.rs:44,54; introspect store.rs:534-535) making the trace plane non-functional; no matching open bead.  ·  722-Audit-recent-criome-mentci-work.md
- **I-063** mentci+criome durable SEMA self-resume
  - Both criome and mentci must self-resume from SEMA per the daemon hard override: mentci is wholly in-memory poll-only and re-mints duplicate questions for criome's durable parked slots on restart, and criome's configuration_generation resets. Persist mentci's slot->question map (or re-derive from the canonical criome slot), commit before client-visible removal, and add a push/subscription surface.
  - bead: mentci+criome: durable SEMA self-resume — persist mentci slot->question map (canonical criome slot), commit before client-visible removal, add push/subscription surface | lane: operator
  - why-now / origins: confirmed violation of the SEMA self-resume hard override in both daemons on main (mentci src/state.rs in-memory; INTENT claims durable); concrete durability+correlation work, no matching open bead.  ·  722-Audit-recent-criome-mentci-work.md

### B · Mirror (3)

- **I-064** Mirror chain-endpoint audit (build + routed-object-notice integration)
  - Assign an owner to verify the mirror builds after the schema-chain split and that its routed-object-notice handling matches real router delivery and spirit outbox-drain. Mirror is the cross-component causal-loop endpoint nobody has audited.
  - bead: Mirror chain-endpoint audit: verify build + routed-object-notice handling matches router delivery and spirit outbox-drain | lane: operator
  - why-now / origins: Chain-endpoint ownership/verification remains unowned and untracked even though the schema-chain split closed on main; no bead covers the routed-object-notice-into-real-loop integration (700 C2).  ·  691-gaps-and-drifts-fixed.md
- **I-065** Mirror fetch-by-digest restore (E5: target HeadMark + HeadNotHeld + locate-by-digest)
  - Extend signal-mirror RestoreQuery to carry an optional target HeadMark, add a HeadNotHeld rejection reason, and make Store::load_restore locate the entry whose digest equals the target, so machines acquire exactly head D rather than latest. Content-addressed locate-by-digest at the mirror, replacing the verify-after-restore interim.
  - bead: Mirror E5 fetch-by-digest: target HeadMark on RestoreQuery + HeadNotHeld rejection + locate-by-digest in Store::load_restore | lane: operator
  - why-now / origins: Concrete signal-mirror contract+code change repeatedly specified across 700/701/702/703 (RestoreQuery is store-name-only today) but never landed and not a tracked bead.  ·  700-propagation-operator-brief.md, 701-multi-machine-criome-cluster-roadmap.md, 703-engine-fixes
- **I-066** Production MirrorObjectNotify contract (router EndpointKind::Mirror + mirror auto-fetch reactor)
  - Promote the harness-local MirrorObjectNotice into the production signal-router/signal-mirror MirrorObjectNotify shape: a real router EndpointKind::Mirror, a mirror-side reactor that auto-fetches on the delivered notice, and server-to-server mirror<->mirror fetch. Realizes Spirit 5osd (router triggers the mirror's own fetch).
  - bead: Production MirrorObjectNotify: router EndpointKind::Mirror + mirror-side auto-fetch reactor + server-to-server fetch (realize Spirit 5osd) | lane: designer
  - why-now / origins: Concrete buildable production contract grounded in Spirit 5osd, distinct from the offline harness (primary-xj51) and live-deploy beads; not yet built and not a bead.  ·  672-first-e2e-full-chain-harness.md

### B · Orchestrate & worktree (6)

- **I-067** Cross-lane 'recently landed' push feed
  - A shared per-lane status feed pushing what each lane just landed so cross-lane state is subscribed, not polled.
  - bead: orchestrate: shared cross-lane 'recently landed' status feed (push, not poll) | lane: operator
  - why-now / origins: Concrete unbuilt coordination capability; the digest/intent-summary parts overlap intent (tf2o/INTENT.md/auditor) but this push feed is distinct and not a tracked bead.  ·  632-architecture-and-agent-friction.md
- **I-068** Full orchestrate workflow-execution engine
  - Build orchestrate's effect plane and DAG runner to production depth: durable SEMA WorkflowRunRecord with self-resume, multi-step parallel/series dispatch, CombinationRule, and workflow/agent/psyche escalation.
  - bead: orchestrate: build the workflow-execution engine to production depth (durable SEMA WorkflowRunRecord self-resume, multi-step DAG parallel/series, CombinationRule, escalation workflow/agent/psyche) | lane: operator
  - why-now / origins: Large greenfield piece only thin-sliced so far (report 727 built one-step proof green); full durable-SEMA run record, multi-step DAG, and escalation remain unbuilt and untracked.  ·  726-Design-orchestrate-workflow-engine.md, 725-Compare-operator-guard-substrate-build.md
- **I-069** Guard substrate downstream daemon behavior (mind + criome)
  - mind stores/resolves WorkflowDefinition and criome consumes WorkflowReceipt in its real evaluation path (not the fixture proof).
  - bead: Guard-substrate daemon behavior: mind WorkflowDefinition storage+resolve and criome WorkflowReceipt consumption in real evaluation | lane: operator
  - why-now / origins: Concrete buildable downstream pieces of the guard substrate; the orchestrate engine and thin criome proof are tracked above, but mind WorkflowDefinition resolution and criome real receipt-consumption are distinct, unbuilt, and not a bead.  ·  725-Compare-operator-guard-substrate-build.md
- **I-070** Integrate real workflow engine to main, replacing the stub
  - Operator integrates the proven real agent-effect engine + criome proof to main, replacing the synchronous fixture stub that fabricates Authorized.
  - bead: operator: integrate the real orchestrate workflow engine + criome proof to main, replacing the synchronous fixture stub | lane: operator
  - why-now / origins: Concrete operator integration action on a designer feature branch (stub bfe4f6d on main never calls agent); not a tracked bead.  ·  727-Thin-end-to-end-proof-and-parallel-lane-finding.md
- **I-071** Implement orchestrate worktree lifecycle + GC reader + refresh INTENT.md
  - Land at least one Archive/Recycle lifecycle transition order, a GC reader that consumes worktrees.nota, and refresh orchestrate/INTENT.md for the registry work.
  - bead: orchestrate: implement at least one worktree lifecycle order (Archive/Recycle) + a GC reader of worktrees.nota + refresh orchestrate/INTENT.md | lane: operator
  - why-now / origins: WorktreeStatus exists in the wire but every path sets Active and worktrees.nota is inert; realizes intent eh5a but the lifecycle order + GC reader + INTENT.md refresh are unbuilt and not a tracked bead.  ·  708-yesterday-designer-work-audit
- **I-072** Migrate live orchestrate redb store 2->3 and restart daemon
  - The running orchestrate daemon is the schema-2 binary while source is at version 3, so the registry is on main but dead in production; migrate the store and rebuild/restart.
  - bead: Migrate the live orchestrate redb store 2->3 + rebuild/restart the orchestrate daemon | lane: maintainer
  - why-now / origins: Concrete highest-leverage deploy task converting merged-but-inert source into a live registry; schema migration is intent c9fv but this specific live migration+restart is not a tracked bead.  ·  708-yesterday-designer-work-audit

### B · Guardian & guard substrate (4)

- **I-073** Activate referents: register recurring instances + model-tag aboutness at write-time
  - The +30 referent signal is dead (2 of 1236 records carry a referent); fix by registering recurring named instances via RegisterReferent and repairing the mis-named implied-referent path to derive aboutness from description text with a model at write-time.
  - bead: spirit: activate referents — register recurring named instances via RegisterReferent and fix the implied-referent path to model-tag aboutness at write time (report 617 Fix 2) | lane: schema-operator
  - why-now / origins: Concrete buildable residue explicitly excluded from the only related bead (tqe3 says seeding/population is separate backfill work); no population/implied-referent-fix bead exists in the digest.  ·  617-spirit-guardian-corpus-health-and-referent-activation-2026-06-13.md
- **I-074** Guardian cache telemetry + verdict cache
  - Capture DeepSeek's dropped prompt-cache telemetry into the journal as a free measurement win, then add a verdict cache keyed on digest(operation+candidate+bundle+prompt-version) to skip the model call on exact repeats, now unblocked by the stable referent-scoped bundle.
  - bead: agent/spirit: capture DeepSeek prompt-cache telemetry into the guardian journal, then add a verdict cache keyed on digest(operation+candidate+bundle+prompt-version) | lane: schema-operator
  - why-now / origins: Concrete unbuilt items with no matching bead in the digest; bundle stabilization (tqe3) already landed so the verdict cache is unblocked.  ·  617-spirit-guardian-corpus-health-and-referent-activation-2026-06-13.md
- **I-075** Rewrite guardian rejection-reason glosses to lead with the operable test
  - Rewrite the NonIntent gloss and three neighbors (UnclearPrivacy/ImportanceUnsupported/RetrievalInsufficient) to lead with the durability test, demote examples, and draw the boundaries that collide, as XS edits to admission_gloss() since the catalogue renders from the enum.
  - bead: spirit: rewrite the NonIntent / UnclearPrivacy / ImportanceUnsupported / RetrievalInsufficient guardian glosses to lead with the operable test (admission_gloss) | lane: schema-operator
  - why-now / origins: Concrete XS edits with no matching gloss-rewrite bead in the digest; operator flagged the NonIntent wording.  ·  617-spirit-guardian-corpus-health-and-referent-activation-2026-06-13.md
- **I-076** Verbatim authentication + idiolect-aware modality learned from the journal
  - Two deferred foundations: retain the source utterance so the guardian can check quotes against the real conversation (the door is currently open), and an idiolect-aware modality pass that learns the psyche's hedging style from the decision journal.
  - bead: spirit: verbatim authentication for the guardian (retain source utterance so quotes can be checked) plus an idiolect-aware modality pass learned from the decision journal | lane: schema-operator
  - why-now / origins: Genuine live residue: authentication is explicitly deferred-pending-full-stack-rewrite (607) and idiolect-aware modality is neither captured nor beaded; the other doubts resolved to intent/closed beads.  ·  606-design-doubts-and-load-bearing-parts.md

### B · Discipline & skills (1)

- **I-077** Visuals-as-data: emit architecture/flow/dependency diagrams from the schema
  - Build a schema-rust-next-style emitter that derives mermaid architecture/engine-flow/dependency diagrams from the typed contract graph, the way Rust and help text are emitted, so diagrams cannot drift.
  - bead: schema-rust-next: emit architecture/flow/dependency mermaid diagrams from the typed schema (visuals-as-data) | lane: schema-operator
  - why-now / origins: concrete buildable capability proposed as a candidate slice, recurring across reports 632/634/635; not intent (only n097 'visuals = mermaid in reports' exists) and no matching bead in the digest.  ·  632-architecture-and-agent-friction.md, 634-new-moon-2026-06-14

### B · Other (telos / persona-runtime / cloud) (2)

- **I-078** Kameo fork split-brain across the daemon fleet
  - criome/router/mentci use the LiGoldragon kameo fork while spirit/mirror run stock kameo 0.20 (real split located to lojix per report 703); pick one runtime fleet-wide, bump every triad-runtime pin, and add a Nix flake-check witness so deployed binary equals audited source.
  - bead: Resolve kameo fork split-brain: unify lojix + fleet onto one runtime via triad-runtime pin, add Nix flake-check witness | lane: system-operator
  - why-now / origins: Concrete, decided cross-stack fix (unify actor runtime + Nix witness) firmed in report 703 as witness-then-fork; not landed (no unification commit) and not in the bead digest.  ·  702-deep-engine-analysis
- **I-079** DigitalOcean nixos-anywhere bring-up + mandatory teardown safety guard
  - Bring DigitalOcean droplets up to NixOS via nixos-anywhere (kexec-install over SSH) with one DesiredHostState bring-up field, and wire idempotent teardown plus a Drop guard and a hard max-N droplet cap so a failed run cannot leak money.
  - bead: cloud: DigitalOcean nixos-anywhere bring-up + DesiredHostState field + mandatory live-substrate teardown Drop guard and max-N droplet cap | lane: cloud-operator
  - why-now / origins: The teardown Drop-guard + max-N cap is a concrete cloud-code safety mechanism not landed and not a dedicated bead; the nixos-anywhere bring-up overlaps primary-hpkj but the cost-safety guard is genuinely distinct live residue.  ·  704-criome-test-cluster

## Section C — Abandon (bulk-confirm)

116 ideas already-landed, superseded, or dead. Each names its
superseder / bead / landed surface. Skim per cluster; flag any you want
to rescue into work or intent.

### C · Intent layer & Spirit (14)

- **I-080** Tag empty referent vectors on l3k4/17ss — Trivial one-time passing record-tagging chore, not durable direction nor lane-sized work.
- **I-081** Pipe-delimiter Spirit cleanup reconciliation — Already done: cleanup executed/verified live, n1px landed in intent digest; guardian lessons restate existing intent (Clarify is wording-refinement, 5g5h).
- **I-082** Operator structural-forms integration regressions — Already tracked: bead primary-3rj9 (operator integration fixes: schema-next reconciliation fold-ins + spirit testing-trace regression) covers both action items.
- **I-083** Intent-digest synthesis layer over raw Spirit corpus — Already intent: refresh-as-agent-skill (tf2o/ne92) and Spirit-as-single-source (8rpu) cover the synthesized-digest loop.
- **I-084** Spirit positional-syntax production cascade — Already built/pushed; remaining main-landing tracked by bead primary-cxyf (integrate structural-forms epic) and agent-pin breakage by primary-opzy.
- **I-085** Guardian-gated intent record-maintenance edits — Recommend-only low-stakes guardian-gated record maintenance applied by the orchestrator; not durable new direction nor lane work.
- **I-086** Per-repo INTENT.md drafting program — Superseded by intent record 8rpu (static INTENT.md/ESSENCE.md deprecated, all intent driven from Spirit); the static-authoring premise is dead.
- **I-087** Guardian-effect agglomeration simulation (1328->1202) — Stale: report 617 reframes the mechanism and the corpus has since changed (628 records); nothing applied. Superseded by the agglomeration-pipeline idea below.
- **I-088** Spirit redesign landing-witness refresh — Already intent and deployed: domain-as-unit (42rh), referent runtime registry, binary guardian (woku/7xnx), two-layer state/stream (icpa/otel); a landing recap with no live residue.
- **I-089** Intent-maintenance + report-GC arc refresh — Report declares no actionable residue; work executed or mooted by corpus rebuild, discipline lives in skills and intent (q4l0, conservative-capture, intent-maintenance).
- **I-090** Sema-engine O(n) head-scan and single-writer TOCTOU — Already done: bead primary-7hro closed the single-writer gap and primary-s22j range-scan slice landed (sema-engine 05f77a78) replacing whole-log reads.
- **I-091** Sema-VC audit reconciliation (cross-table torn writes) — Already done: multi-table atomic commit is closed bead primary-im74; remaining findings covered by 615 entries and beads 7hro/85hv/x3l7.
- **I-092** Grand-DVCS scope question for the psyche — Open question for the psyche to rule on, not a captured decision or buildable item; the DVCS direction is already loosely intent (i4ak/2uhh) pending the psyche's scope call.
- **I-093** Verdict-by-slot retires cross-import-deferred note — Resolved in report 710: the note was a comment, no durable intent record to supersede; procedural Spirit-gate housekeeping.

### C · Schema & codegen (17)

- **I-094** schema-cc compiler-compiler (datafy the compiler definition, generate the resolver) — Already intent: vpbx (schema-cc) + 549v (precedence as generative data) + 9rjq (build-time only); built and integrated into schema-next per report 653 (operator owns code-repo merge).
- **I-095** Generics/traits/impls as schema data (delimiter family, pipe syntax, type-kind explicitness) — Already intent: 3742 (type-kind explicit), hh3z (generics (| |)), bpyu ({| |} traits/impls); plus the no-keywords-in-records hard override. Settled and recorded.
- **I-096** Reaction-frame declare-once-bind-expand (generics in schema-next, Absent-leg maximal frame) — Already intent zjmc/n6fz (declare-once frames) and built across branches; integration/migration tracked by beads primary-9gkn (integrate generics+reaction branches) and primary-8dcn (migrate 14 components + delete into_next_step shim + runner re-point). The 619 Plane-trait shape was superseded by direct-generics (621).
- **I-097** Code-is-data method bodies + capability resolution (composition closure, shape-derived resolver) — Captured via the d3r2 Clarify and then explicitly re-scoped/parked as a future tool by report 666 (Spirit t5wx); not live required residue. The Deref-by-default refinement is an explicit open psyche question deferred to the psyche.
- **I-098** schema-codegen capability set is closed; finish-and-port the narrow stack — Already intent: t5wx (capability set closed; finish-and-port) plus the d3r2 re-scope; the port/integration is tracked by beads primary-9gkn and primary-8dcn. (The discrete finish-slices residue is captured as a separate work item above.)
- **I-099** Language-as-data / macros-as-data / self-host thesis and corrections — Already intent: 7c71/2zed/t85k/j9du/wfdt (language/macro-as-data, self-host the macro-table). The headline self-host item is bead primary-bojw; remaining gaps are fenced out-of-scope. The template fork was dissolved by 2zed (kinds-as-macros).
- **I-100** Structural Forms derive deepening + self-host boundary — Struct-level derive landed (641); SchemaMacro retirement tracked by bead primary-bojw; the thesis is intent (7c71/2zed/my86). The remaining nota-next derive extension is captured as the nota-next work item above; the rest are explanatory recaps.
- **I-101** Positional/dimensional struct syntax (role-is-type, bare-types body, dot-differentiator) — Already intent: ov30 (role-is-type/newtype-per-role), adnn (positional struct syntax), 6wwf/mcuk/vr32 (positional never labeled). Built and landed (643); integration tracked by bead primary-cxyf.
- **I-102** Streams and families are closed typed records, not open type-field structs — Framing settled across 645/646/649 and the migration is already a bead: primary-hhp0 (migrate streams/families to positional typed-body structs).
- **I-103** Universal positional syntax + family-identity SchemaHash + symbol-atom derive (consolidated) — Tracked by beads: primary-hhp0 (universal-positional migration), primary-6eog (family-identity SchemaHash named-newtype emission); intent ov30/adnn underpins. Integration is operator's lane.
- **I-104** TypeReference reconciliation / structural-forms epic integration — Status/handoff; integration tracked by beads primary-cxyf (integrate structural-forms epic) and primary-3rj9 (operator reconciliation fold-ins); mandated by intent v0n6.
- **I-105** impl-reference syntax: grammar, catalog, out-of-band verification, placement — Prototype + integration fixes built and pushed on next/impl-reference-syntax; the only unbuilt live residue (real crate-parse RustSurface populator + method-call resolver) is captured as a separate work item above.
- **I-106** Design assessment: gains/costs/strangeness of structural forms + no-backward-compat — Pure assessment/recap; the design decisions it weighs are already intent (3742/hh3z/bpyu/zjmc) and the no-backward-compat stance is the ESSENCE/lrfa hard override. No new live residue.
- **I-107** Self-host the macro-table type from core.schema — Already a tracked bead: primary-bojw (self-host the macro-table type: generate the pattern family from core.schema); intent wfdt.
- **I-108** Schema-chain migration / cluster-propagation PoC — PoC/validation snapshot; schema migration as a workspace-wide prerequisite is already intent (c9fv/29pb) and the vertical-slice/regen path is tracked by beads primary-lwc6/primary-ing7. No distinct live residue.
- **I-109** Schema triad runtime / grammar-engine-actor refresh — Situation/refresh report; engine-mechanism-workspace-canonical and the triad runtime are intent (czw0/zjmc/7tqc) and integration is tracked by primary-9gkn/8dcn. No new residue.
- **I-110** Deep engine analysis + engine fixes (snapshot) — Analysis snapshot + applied fixes; the actionable contract-fidelity residue is captured in the orchestrate-bugs work item (708) above, and the rest is already-intent engine discipline. No separable new direction.

### C · Criome (auth / cluster / quorum) (25)

- **I-111** Spirit ungated-request monitoring (non-blocking emit + mentci watch) — already done: spirit emit_authorization (criome_gate.rs:237) + AuthorizationMode wired (engine.rs:168-172) and mentci monitor proven per report 721; the watch was re-framed onto the tracing surface.
- **I-112** Attested-moment a-priori window (optional CrystallizationMoment extension) — already intent: ay3y captures the a-priori-window decision (operator 418 confirmed); the extension is speculative, not live residue.
- **I-113** k>n/2 quorum-majority invariant in the criome verifier — already done: operator 426 landed is_valid_majority (criome 22801af, language.rs:623-626); reports 694/697 call Woe 3 RESOLVED.
- **I-114** criome tiers are deployment profiles, not a contract split — superseded/already intent: 9s52 (per-Unix-user criome) settled the tier question (687 Q1 RESOLVED); the no-typed-tier lean is non-additive, nothing to capture.
- **I-115** AuthorizedObjectKind::Head + cross-machine self loop — framing already intent (nfvm) + Head kind already landed (operator 426, criome 9194c795/475075fa); the unbuilt adoption/loop residue is captured by the propagation-loop work item below.
- **I-116** No embeddable criome engine library (one daemon per component) — a do-not-build lean consistent with existing intent (many criome daemons, one per Unix user; two contracts per component); no live residue.
- **I-117** Retire telos-poc + content-addressed-bls branch — housekeeping disposition already acted on by landed main work (4250cbb, 0cf326c); no live residue.
- **I-118** criome's internal limited typed policy language — already intent: Spirit vhs2 (digest carries the limited policy language); substantially landed on criome main (reports 675/682).
- **I-119** Attested-clock crystallized-past time — already intent: Spirit ay3y; landed on criome main as Evidence.stamp + TimeNotProven (reports 675/682).
- **I-120** criome contract-machinery genus thesis — comparative research grounding already-captured intent (vhs2/wckt/z9d6/p3td); no new live idea; the referenced SEMA family already landed (3c051223).
- **I-121** criome is the universal agreement machine; quorum is the universal primitive — already intent: Spirit p3td/m0p2/pviw, confirmed coherent by the 682 audit.
- **I-122** Propagation forks A/B (compute-set-vs-subscribe; event-vs-heartbeat) — both resolved into Spirit l2ha (Fork A: subscribe + router fan-out) and m0p2 (Fork B: contract-scheduled freshness floor, not ambient heartbeat) per reports 680/682; no open residue.
- **I-123** Fork C: one-daemon-per-user authority unit + logical self-quorum object — the daemon-per-user half is already intent (9s52 per-Unix-user criome; p3td self-quorum 'self-quorum for reliability'); the self-quorum-as-logical-object reading restates p3td and adds no durable direction not already in the digest.
- **I-124** Direct criome-to-criome peer lane (lt44) — already intent: Spirit lt44 (which superseded wckt); the report's duplicate Record was guardian-rejected because lt44 already covers it.
- **I-125** E1 wire crypto / increment-4 hazards — increments 1-3 already built+verified on branches (signal-criome-peers f4b64fc5, criome-peer-transport 081f6f7c); the design is realized code and the remaining slice plus its hazards fold into the E1 increment-4/5 work item already captured; no-blocking-in-actor-handlers is already intent.
- **I-126** Multi-machine criome cluster roadmap (E1-E6 + deploy) — a roadmap whose live enablers are captured individually (cluster-root ceremony, BLS aggregate, peer lane, propagation loop work items above); E1 overlaps primary-ymww/9x9f; the roadmap itself is not a distinct buildable unit beyond its enablers.
- **I-127** Which three machines form the first 2-of-3 cluster — a blocking psyche question resolved via chat, not durable intent nor a buildable item; 9s52 already captures the per-user model.
- **I-128** Spirit gates on criome in the commit path (1-of-1 local gate) — already done + already intent: spirit main 90875f26 carries the production 1-of-1 fail-closed gate (703); xhwa captures the near-term 1-of-1 local auth; residual cross-process daemon e2e folds into the propagation-loop work item.
- **I-129** Reusable networked criome test-cluster interface (mkCriomeClusterTest) — durable intent already captured (Spirit cpip) and the remaining de-branch integration is already tracked by bead primary-exzf (de-branch criome cluster test to CriomOS-test-cluster main).
- **I-130** criome AuthorizationMode (Quorum/AutoApprove/ClientApproval) — already done: operator landed AuthorizationMode contracts (signal-criome aa5498a, meta-signal-criome 2a2f7d9) and criome main subsumed the runtime (245f0441); the three-mode model is intent t00s/p43g.
- **I-131** Criome owns key custody + is the authorization decider (custody disambiguation) — already intent: Spirit p43g (folding 9s52/t00s/2st7), in the digest.
- **I-132** Verdict from meta-socket approver or auto-approve policy — already intent: Spirit t00s, in the digest.
- **I-133** ClientApproval park-flow VM proof — process-level proof already built (criome-client-approval-witness branch, green); the VM-level proof folds into the recurring criome+mentci nixosTest item and de-branch is tracked by primary-exzf.
- **I-134** Track A authorization defects on criome main — already done: operator landed the fixes in criome 6a5e797 (reject-gate, unknown-slot->RequestUnimplemented, malformed-Configure->ConfigurationRejected, numeric slot sort, dead-fn removal); residual items are minor polish.
- **I-135** Bump p43g certainty Medium->High — p43g is already intent; a certainty bump is a psyche-driven in-place edit (ChangeCertainty), not a new intent record or bead.

### C · Mentci (5)

- **I-136** mentci component = human-adjudication triad over criome (state-bearing UI daemon) — already intent: 7x5z/gc0n/9s52/mu0o; component design already built+verified (operator 422, report 689 PASS — four schemas + mentci-lib landed).
- **I-137** mentci-lib re-founded as the client-side observability+control library — already done: mentci-lib re-founded and integrated to main (707-9/708); role question settled by psyche in report 710, consistent with intent 7x5z.
- **I-138** criome verdict-by-slot seam + daemon-routing + criome-access mode + egui approval card — already done: seam, daemon-routing, criome-access mode, and egui card all built and integrated to main (signal-mentci 951c9c2a, mentci-egui befd358e) and audited clean in report 714; guardian ruled daemon-routing/access-mode repo-doc design-detail.
- **I-139** Embeddable-daemon vs universal-typed-client forks for mentci-lib — superseded by the report 719/720 driveable-client/egui-triad direction the psyche acted on; the recurring direct-client-vs-daemon-bridge fork is carried as an unresolved psyche-call in reports 721, not durable residue here.
- **I-140** Driveable-client contract (UserEvent in / ObservationView out) landed — already done: signal-mentci-client + meta-signal-mentci-client landed on main per report 722 (d8a6064); the design also realizes existing no-parallel-vocabulary/single-colon-import intent (isia, 1sa2/lk22).

### C · Signal-standard & router (4)

- **I-141** Message fast-path X/Y already beaded — already tracked: primary-ydfh (message owns existence-fact, l3k4 clause 1) and primary-xslx (direct-delivery fast path, supersedes l3k4 clause 2 + 17ss); the conditional supersession is part of xslx execution.
- **I-142** Registry-owner fork resolved router-sole — already intent: m0p2 clarified router-sole, consistent with l2ha and lt44 in the intent digest (router payload-blind, two-lane model).
- **I-143** signal-standard typed StandardSocket connection point — already intent (eaf7 signal-standard socket type) and already built (signal-standard crate landed with the StandardSocket sum vocabulary, operator 422 aa672cc).
- **I-144** Router cross-socket/remote delivery push — already tracked: the router forwarding contract + daemon transport (the in-process-delivery-to-wire and remote-push surface) is bead primary-9x9f, with cross-host deploy under primary-ymww.

### C · Trace / introspect / e2e (3)

- **I-145** Trace introspect plane: shared contract record + dependency direction — already done: landed on main per report 722 (introspect store.rs/runtime.rs, signal-introspect a926995) and branches retired (721); realizes existing intent so0p/cd76/m5jl, not new direction.
- **I-146** First e2e production milestone: spirit->vcs->criome->router->mirror chain — already intent: captured as Spirit Decision d6he (per report 668) with the vcs=mirror clarification (D1, report 669) already resolved and acted on across 669-673.
- **I-147** Offline in-process full-chain e2e harness — already done + tracked: built and passing on branch (end_to_end_offline_full_chain.rs @ 75d0e8d4, reports 672/673); main integration including signal-router regen is bead primary-xj51.

### C · Mirror (1)

- **I-148** Spirit->mirror MirrorShipper reland + shared-engine seam (5-branch e2e stack) — Already built and pushed green on branches (mirror-shipper-reland @75d0e8d4, mirror-target-reland @5d61ae8c, arc-shipper-mainline @6bcefa4f); main integration tracked by bead primary-xj51 (Integrate offline first-e2e stack to main), with production driver under primary-85hv; the restart-persistence slice is a known follow-up inside that integration.

### C · Orchestrate & worktree (12)

- **I-149** Top-down re-grounding teaching artifact — Serves existing intent obo5 (re-ground psyche top-down); inner claims retracted by report 624.
- **I-150** Ground every report claim in real source — Already intent: aipc/gni3 (tests prove real behavior; agent-authored content not psyche-authorized; cite-or-retract drift).
- **I-151** Worktree cleanup/hygiene snapshots — Transient cleanup already executed; worktree lifecycle/registration is intent eh5a/cb0j.
- **I-152** Cross-lane review + TypeReference reconciliation — Coordination status; the reconciliation was completed in report 631 and wire shape is grounded in intent wqdi; integration tracked by beads primary-9gkn (reaction-frame integration) and primary-cxyf (structural-forms integration).
- **I-153** Auditor role restatement — Already intent (2gj4/ek8w/wgii); report only restates it.
- **I-154** Unpushed reconciled-branch coordination gap — Session-specific, resolved in report 641 (epic branch pushed); standing rule already intent 6xzu (designer next-branches, operator owns main).
- **I-155** Maintainer standing audit duty — Guardian ruled it InsufficientWarrant per report 715; covered by intent 6u6o (specialized lanes) + 2gj4 (auditor coming).
- **I-156** Guard step as typed agent::Call — Built green in report 727 and realizes existing intent l0w8 (agent contract) + 7mvx (guardian runs strong model); folds into the engine work above.
- **I-157** Worktree registry as daemon-owned typed orchestrate state — Already intent eh5a and built+operator-integrated to main (reports 707-9/708); residual items carried in the live-migration and lifecycle work beads below.
- **I-158** Worktree GC contract (refuse unpushed) — Governed by intent eh5a; the gated destructive GC pass is an operational follow-up in report 708, folded into the lifecycle/GC-reader work bead below.
- **I-159** Document register-worktree-at-creation in skills — A docs realization of intent eh5a/cb0j, blocked behind the still-unbuilt orchestrate worktree CLI adapter; folds into the lifecycle/CLI work, not a standalone idea.
- **I-160** criome-mentci-bootstrap epic-branch protocol note — Operational bookkeeping governed by intent 6xzu (designer next-branches/operator owns main) and eh5a (worktree registry); not a new durable idea.

### C · Guardian & guard substrate (11)

- **I-161** Referent-guardian admits identifier names for abstract records — Already done: spirit/src/guardian-prompts/referent.md fix built, deployed (daemon 0.12.1 on ouranos), and principle re-recorded via Supersede as Spirit zjmc; report 406 COMPLETE.
- **I-162** Criome as universal LLM-workflow guard substrate — Already intent (m3ms/ic4o/pviw/p43g) and built: contract families landed on main (signal-criome 9d7a785, signal-orchestrate 4f1e3ff, criome cd9791db) per reports 724/725/727.
- **I-163** Two-plane guard trust model — Already intent ic4o ('Two-plane guard trust: local execution chamber vs remote'), captured by operator and cited in report 724.
- **I-164** Guard-substrate contract shapes and composition algebra — Already done: shapes and the de-duplicated content-addressed composition landed on main per reports 725/727 (signal-criome 9d7a785/a7b2f3d/7b3d5b2, signal-orchestrate 4f1e3ff).
- **I-165** Open-weight reasoning-model selection for the guardian — Already done: guardian shipped on deepseek-v4-pro (609); durable principle is intent (qoku, hosted inference not a privacy violation); numbers are stale by design.
- **I-166** Importance earned by restatement; orthogonal to certainty — Already intent (importance certainty orthogonal axes u62s; certainty=burden, importance=stakes) and the duplicate-bump is built into the shipped guardian (609).
- **I-167** Modality-catch: preserve hedging, Overstated reason, verbatim testimony — Already intent (woku guardian catches over-stated capture; u62s) and built: typed Justification carries Testimony verbatim quotes and the Overstated atom landed/deployed (spirit 0.11.x, report 609).
- **I-168** Court-of-law intent-capture protocol (binary guardian, argued justification) — Already intent (i59i/woku/ll41/7xnx/z3ka guardian=court of law) and built+deployed per 609; the full-court cathedral extras were superseded by the lean core (bwqe, 607).
- **I-169** Lean Phase-1 justification spec (Testimony+Reasoning, five reason atoms, clean-context judge) — Already done: fully implemented and deployed at spirit 0.11.3 on deepseek-v4-pro (609), with the 9-gate checklist, NOTA verdict grammar, over-trained few-shot, and ratifying intent (bwqe/2t89/4jgt/ans1/gad7).
- **I-170** Replayable decision journal as training flywheel — Already intent (guardian training flywheel 0s5u) and its remaining half (raw output, retry status, provider/model/prompt-version) is a named open seam in 609 tracked under task 402, not fresh residue.
- **I-171** Guardian corpus health: shrink corpus, scope bundle to referents (not a cap) — Already tracked and done: retrieval-scoping is CLOSED bead primary-tqe3 (shipped spirit c1952d18), All-bucket seeding CLOSED bead primary-gm78, and relevance-is-semantic is intent (qr5o).

### C · Discipline & skills (16)

- **I-172** Drop Nexus*/Sema* namespace prefix at schema source — already intent: Names don't carry ancestry (ESSENCE/AGENTS, sarw); already tracked: bead primary-8dcn folds the Nexus* drop into the reaction-frame migration, and report 621 step 5 already dropped it in the spirit pilot.
- **I-173** No transparent type aliases in schema-emitted Rust — already intent: Spirit sarw (real-data-bearing types over aliases; bare namespace bindings lower to declarations) and qz6j (bare name+type is a distinct newtype, not an alias).
- **I-174** Actor-boundary granularity: isolation/serialization/supervision, not computation — research backing for existing intent (Spirit zk6y engines-as-kameo-actors, w312/06l6 mechanism-vs-agent split) and skills/actor-systems.md + skills/kameo.md (bead primary-95c, done); the granularity rule belongs in the existing actor-systems skill, not a new record.
- **I-175** Compact architecture digest load surface (top-down walkthrough) — synthesis/teaching recap of already-captured architecture intent (component-triad skill, 7c71, zjmc, zk6y, w312); carries no new durable direction.
- **I-176** Constraint test guarding derive-single-source-of-truth property — already intent: every load-bearing intent maps to a constraint test that fails if unhonored (l50b/7gcs), tests prove real behavior (aipc); the specific guard lands inside bead primary-3rj9 (operator integration fixes).
- **I-177** Worktree cleanup of empty-diff and archived doc branches — already done: cleanup status realizing eh5a (worktree lifecycle); no live idea, pure outcome reporting.
- **I-178** Pin Spirit production by operator-applied tag rather than tracking main — a sharpening of existing intent 88eq (component upgrade = Nix-flake versions, release tags the dependency surface), owned by operator's capture under the one-capturer rule; tag scope already resolved in report 724.
- **I-179** skills.nota description rubric: purpose+trigger, two sentences, positive — already intent: Spirit 9x28 (skills.nota single source of skill identity, 2-sentence positive).
- **I-180** Single-source rule: skills.nota IS the description, skill files carry only teaching body — already intent: Spirit 1p0r/9x28; already done: report 729 confirms frontmatter stripped and 47 taglines removed, committed to main.
- **I-181** Workspace golden rule: state everything positively — already intent: Spirit jlo7 (state everything positively, name what a thing is and why), enriched this session.
- **I-182** Mechanical skill-description realignment execution — already done: pure closeout of work landed and committed to main, executing decisions captured as 9x28/1p0r/jlo7/ljce.
- **I-183** structural-forms.md and active-repositories.md drift fixes — already done: edits landed in skills/structural-forms.md and protocols/active-repositories.md.
- **I-184** structural-forms.md staleness against schema-next main — routine skill-text staleness already partially applied per report 683 (the 1de72dde parenthesized-composite form); ordinary skill maintenance, not a standing bead.
- **I-185** Decorative-discipline smell: discipline that satisfies a checklist not load-bearing — cross-cutting audit observation substantively covered by existing intent (typed self-describing feedback bexd, typed per-crate Error in rust-discipline); concrete instances captured as separate work items in reports 708/709/714.
- **I-186** Bump contract version on every wire break to make skew visible — already intent: version-bump-per-change (hg78/rg2i/nu76) and schema-aware versions, tag-before-migration (h2oa); applying it to the mentci stack is execution foldable into contract-fidelity work, not a new idea.
- **I-187** Cross-surface critic pass over the whole bootstrap — methodological observation already covered by existing intent on the designer counter-ego / completeness-critic pass (tenr/56kv/nifs).

### C · Other (telos / persona-runtime / cloud) (8)

- **I-188** Object-update pulse pushes references, not payloads — Already intent: Spirit m0p2; landed as reference-only AuthorizedObjectUpdate on criome/signal-criome main (verified report 682); the unbuilt fan-out delivery is captured separately under Fork A.
- **I-189** Telos level structure: criome is the authorization organ, not Telos — Already intent: Spirit p3td (superseded obuf) and pviw; the 682 audit verifies obuf is fully gone and the level structure is current.
- **I-190** Contract-scheduled heartbeat (after-time condition, not ambient tick) — Already intent: Spirit m0p2 (after-time condition); contract-programmed Time pulse landed on criome main (255660a, report 682); remaining fire/suppress delivery rides the already-tracked Fork-A fan-out work.
- **I-191** Persona component authority/non-ownership principles (mind/router/message) — Already-established architecture in the digest (mind authority sections) and described as built in report 548 component-map; standing architecture, not new direction.
- **I-192** Persona meta-engine total-vision synthesis — Pure agglomeration of already-captured intent (triad 7sx6, one-reaction-three-planes o8x5/rmm8, daemons-never-parse-NOTA ur16, Nexus catalog z6qu, SO_PEERCRED 9v7h, spirit-as-exemplar ctkv); a teaching recap with no live residue.
- **I-193** Fleet migration landing-witness Refresh — A landing-witness recap of already-intent migration principles (no-back-compat ax2k, wrapping-is-not-migrating hehp/ng1x/v3um, migrate-smallest-first r310, schema-source-of-truth ug6i) plus executed archival; residual contract tail is tracked working state.
- **I-194** Upgrade migration daemon audit + INTENT/ARCHITECTURE refresh — Audit and INTENT/ARCHITECTURE refresh already landed (upgrade main 68939c46, report 703); residual daemon-mount work is captured in intent (tmji sema-upgrade universal component) and is operator runtime work, not a fresh idea.
- **I-195** Designer alignment-interview method (interview to report to slice DAG) — Interview format already captured as intent ljce and constrained by kxzh/7nbu/k4i3/o7zt; the alignment-interview skill already exists (report 728); a synthesis of existing intent, not new direction.

## Appendix — per-report drain map

Each entry → the idea ids drawn from it. A report retires once all its
ideas are routed (intent / bead / abandon). Entries with no live idea
retire immediately.

| Entry | ideas | note |
|---|---|---|
| 528-Intent-md-drafts-and-landing-plan.md | I-086, I-191 |  |
| 548-persona-meta-engine-vision.md | I-191, I-192 |  |
| 568-open-weight-reasoning-models-mid-2026.md | I-165 |  |
| 601-guardian-effect-simulation.md | I-087, I-166 |  |
| 602-guardian-modality-catch.md | I-166, I-167 |  |
| 603-intent-capture-protocol.md | I-168 |  |
| 604-intent-justification-court-design.md | I-168 |  |
| 605-intent-justification-implementation-spec.md | I-169 |  |
| 606-design-doubts-and-load-bearing-parts.md | I-076 |  |
| 607-intent-justification-lean-spec.md | I-169, I-170 |  |
| 608-guardian-example-library.md | I-169 |  |
| 608-guardian-prompt-spec.md | I-169 |  |
| 609-guardian-justice-built.md | I-023, I-169 |  |
| 611-Refresh-spirit-redesign-domain-corpus-guardian-2026-06-13.md | I-088 |  |
| 612-Refresh-schema-triad-runtime-grammar-engine-actor-2026-06-13.md | I-109 |  |
| 613-Refresh-fleet-migration-archival-ecosystem-state-2026-06-13.md | I-193 |  |
| 614-Refresh-intent-maintenance-corpus-governance-history-2026-06-13.md | I-089 |  |
| 615-sema-vc-system-and-spirit-pilot-opus-review-2026-06-13.md | I-014, I-015, I-016, I-017, I-090 |  |
| 616-sema-vc-audit-reconciliation-questions-suggestions-2026-06-13.md | I-091, I-092 |  |
| 617-spirit-guardian-corpus-health-and-referent-activation-2026-06-13.md | I-013, I-073, I-074, I-075, I-171 |  |
| 618-nexus-runtime-naming-and-driver-fork-flaw-2026-06-13.md | I-096, I-172 |  |
| 619-ideal-nexus-plane-generated-code-2026-06-13.md | I-096, I-173 |  |
| 620-nexus-generics-structural-macro-session-2026-06-13 | I-096, I-161 |  |
| 621-schema-generics-impl-plan-and-open-decisions-2026-06-13.md | I-003, I-019, I-096 |  |
| 622-reaction-frame-emission-slice.md | I-096 |  |
| 623-system-resituation-2026-06-13 | I-099, I-149 |  |
| 624-audit-of-report-623-self-hosting-macros.md | I-099, I-150 |  |
| 625-operator-spec-self-host-macro-table-type.md | I-099, I-107 |  |
| 626-vision-language-as-data-macros.md | I-099 |  |
| 627-structural-forms-the-concept.md | I-004 |  |
| 628-reality-check-structural-forms-epic.md | I-099, I-151 |  |
| 629-actor-counts-and-granularity.md | I-174 |  |
| 630-cross-lane-review.md | I-152 |  |
| 631-typeref-reconciliation-outcome.md | I-020, I-104 |  |
| 632-architecture-and-agent-friction.md | I-067, I-077, I-175 |  |
| 633-operator-integration-review.md | I-082, I-176 |  |
| 634-new-moon-2026-06-14 | I-077, I-083, I-100, I-153, I-154 |  |
| 635-structural-forms-derive-deepening-and-self-host-boundary.md | I-100, I-151 |  |
| 636-structural-forms-explained-walkthrough.md | I-100 |  |
| 637-schema-and-type-reference-from-the-ground-up.md | I-100 |  |
| 638-field-name-equals-type-name.md | I-101 |  |
| 639-every-field-a-distinct-type-dimensional-principle.md | I-101 |  |
| 640-positional-struct-syntax-and-differentiator-separator.md | I-101 |  |
| 641-structural-forms-epic-branches-consolidated.md | I-104 |  |
| 642-positional-struct-syntax-migration-spec.md | I-101 |  |
| 643-positional-struct-syntax-landed.md | I-101 |  |
| 644-retired-syntax-reject-response-to-operator-380.md | I-101, I-102 |  |
| 645-streams-and-families-are-not-structs.md | I-102 |  |
| 646-structural-forms-consolidated-design.md | I-103 |  |
| 647-universal-positional-prototype-and-operator-plan.md | I-103 |  |
| 648-spirit-positional-integration-analysis.md | I-084 |  |
| 649-family-stream-positional-syntax-pin.md | I-102 |  |
| 650-cross-check-system-designer-111-message-fastpath.md | I-080, I-141 |  |
| 651-spirit-engine-ecosystem-analysis | I-094 |  |
| 652-schema-cc-design-and-leans.md | I-094 |  |
| 653-schema-cc-integration-merge-ready.md | I-094 |  |
| 654-generics-traits-as-data-review.md | I-001, I-095 |  |
| 655-explicit-generic-syntax-pipe-delimiter-family.md | I-081, I-095 |  |
| 656-reaction-frame-codegen-design.md | I-002, I-096 |  |
| 657-concrete-interface-vs-persisted-generic.md | I-002 |  |
| 658-reactive-component-end-to-end-operator-spec.md | I-096 |  |
| 659-schema-language-and-component-codegen | — | no idea matched origin string — verify before retiring |
| 660-whole-vision-tested-demonstration.md | I-097 |  |
| 661-implied-method-composition | I-097 |  |
| 662-schema-codegen-arc-visual-capstone.md | — | no idea matched origin string — verify before retiring |
| 664-capability-resolver-branch-and-two-branch-comparison.md | I-097 |  |
| 665-state-of-the-arc-full-recap.md | I-097 |  |
| 666-have-what-we-need-and-the-port-plan.md | I-018, I-098 |  |
| 667-design-assessment-gains-costs-strange.md | I-106 |  |
| 668-first-e2e-production-overview.md | I-146, I-147, I-148 |  |
| 669-first-e2e-offline-build | I-032, I-058, I-148 |  |
| 670-first-e2e-offline-unblock | — | zero live ideas — status/handoff/capstone, retire immediately |
| 671-first-e2e-spirit-integration.md | I-148 |  |
| 672-first-e2e-full-chain-harness.md | I-066, I-147 |  |
| 673-offline-first-e2e-proven-capstone.md | — | zero live ideas — status/handoff/capstone, retire immediately |
| 674-criome-internal-engine | I-038, I-039, I-118, I-119 |  |
| 675-system-with-perspective | I-010, I-012 |  |
| 676-contract-machinery-comparison | I-120 |  |
| 677-telos-the-agreement-machine.md | I-121, I-122, I-188 |  |
| 678-criome-agreement-machine-visual.md | I-005, I-122, I-123, I-189 |  |
| 680-telos-integrated-poc | I-026, I-190 |  |
| 681-signal-standard | I-059 |  |
| 682-overview-and-context-maintenance | I-040, I-085, I-184 |  |
| 683-design-review-and-networking | I-007, I-041, I-113, I-124 |  |
| 684-design-woes | I-031, I-032, I-033, I-034, I-101, I-112, I-113, I-142 |  |
| 685-cross-machine-self-mentci-criome-tiers | I-010, I-035, I-114, I-115, I-116, I-136 |  |
| 686-mentci-poc-furthering | I-117, I-136, I-143 |  |
| 687-mentci-full-component | I-046, I-047, I-136 |  |
| 688-handoff-to-system-designer.md | — | zero live ideas — status/handoff/capstone, retire immediately |
| 689-audit-operator-422-mentci-landing.md | — | zero live ideas — status/handoff/capstone, retire immediately |
| 690-engine-audit | — | superseded audit (June 18); residue already in work ideas; see 690 note |
| 691-gaps-and-drifts-fixed.md | I-020, I-036, I-064, I-143, I-183 |  |
| 692-schema-and-schema-rust-gaps.md | I-018, I-021 |  |
| 693-impl-reference-and-method-call-syntax.md | I-105 |  |
| 694-cluster-propagation-poc | I-011, I-037, I-108 |  |
| 695-catalog-placement-decision.md | I-105 |  |
| 696-impl-reference-prototype.md | I-022, I-105 |  |
| 697-propagation-loop-state-blockers.md | I-037, I-057 |  |
| 698-response-to-operator-432-impl-reference-feedback.md | I-105 |  |
| 699-impl-reference-integration-fixes.md | I-105 |  |
| 700-propagation-operator-brief.md | I-037, I-065, I-144 |  |
| 701-multi-machine-criome-cluster-roadmap.md | I-032, I-065, I-126, I-127 |  |
| 702-deep-engine-analysis | I-048, I-060, I-078, I-110, I-128, I-144, I-194 |  |
| 703-engine-fixes | I-065, I-110, I-128, I-137 |  |
| 704-criome-test-cluster | I-079, I-129, I-130, I-131, I-132 |  |
| 705-criome-cluster-reassessment | I-041, I-042, I-133, I-134, I-135 |  |
| 706-criome-e1-peer-transport.md | I-041, I-125 |  |
| 707-mentci-integration-and-worktree-protocol | I-137, I-157, I-158, I-159 |  |
| 708-yesterday-designer-work-audit | I-024, I-051, I-071, I-072, I-138, I-185 |  |
| 709-mentci-criome-orchestrate-problems-and-decisions.md | I-008, I-093, I-137 |  |
| 710-criome-mentci-verdict-by-slot-seam.md | I-138, I-160 |  |
| 711-mentci-bootstrap-phase2-mode-card-and-handoffs.md | I-053, I-138 |  |
| 712-criome-mentci-overview-and-io.md | I-006, I-055 |  |
| 713-criome-mentci-nixostest-draft-and-cli-status.md | I-053, I-054 |  |
| 714-Audit-operator-bootstrap.md | I-029, I-042, I-043, I-048, I-049, I-052, I-053, I-186, I-187 |  |
| 715-Synthesis-working-with-mentci-roadmap.md | I-139, I-155 |  |
| 716-Design-tracing-introspect-slice.md | I-145 |  |
| 717-Runbook-mentci-introspect-live.md | I-061, I-139 |  |
| 719-Design-driveable-mentci-client.md | I-045, I-111, I-140 |  |
| 720-Design-mentci-egui-triad.md | I-044 |  |
| 721-Status-production-watch-and-cleanup.md | I-027, I-028, I-177 |  |
| 722-Audit-recent-criome-mentci-work.md | I-009, I-010, I-027, I-029, I-044, I-050, I-062, I-063 |  |
| 723-Design-criome-guardian-llm-workflow-contracts.md | I-162, I-178 |  |
| 724-Design-guard-substrate-contracts.md | I-030, I-162, I-163, I-164 |  |
| 725-Compare-operator-guard-substrate-build.md | I-068, I-069, I-164 |  |
| 726-Design-orchestrate-workflow-engine.md | I-068, I-156 |  |
| 727-Thin-end-to-end-proof-and-parallel-lane-finding.md | I-025, I-056, I-070 |  |
| 728-Design-alignment-interview-method-and-skill-realignment-2026-06-24.md | I-179, I-180, I-181, I-195 |  |
| 729-Closeout-skill-description-realignment-2026-06-24.md | I-182 |  |

## Appendix — reports retiring immediately (zero live ideas)

- 670-first-e2e-offline-unblock
- 673-offline-first-e2e-proven-capstone.md
- 688-handoff-to-system-designer.md
- 689-audit-operator-422-mentci-landing.md

## Appendix — 690-engine-audit (recovered late)

690 is a June-18 whole-stack engine audit. Its actionable beads are
already represented as work ideas above: criome crypto safety (k>n/2,
BLS-aggregate), close the delivery chain (criome matcher retire / router
branches / mirror endpoint), consumer-build sweep, signal-standard
`ComponentKind` migration, mentci durable SEMA, and the
`skills/structural-forms.md` reconcile. **Disposition: abandon** (superseded
snapshot). Two minor P3 verifiability items not separately captured —
a recorded-transcript guardian test asserting `NegativeGuideline` without a
live provider, and `nix flake check` witnesses at audited HEADs — flagged
here as `possibly useful:` small work, fold into existing test/trace work if wanted.
