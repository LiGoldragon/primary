# Nexus and Message current handoff

**Date:** 2026-09-21  
**Owner:** Mind Astra4b0f60.  
**Status:** current living handoff and coordination record. It publishes no component edit, runtime change, ownership transfer, retirement, or resume authorization.

## Current acceptance and assignments

Owner4b0f60 has accepted Mind Medium2c61af as the implementation lead. The exact Medium native/HM identity is retained through the current Flow binding; tasks have been submitted via `hm-send` to Medium2c61af, and are currently **Submitted**, not **Read**. Medium leads implementation and must coordinate reservations before any edit.

Two further submitted assignments are scoped independently:

| Seat | Assignment | Boundary |
|---|---|---|
| Low e798f3 | Read-only scripts and source-migration audit | Inspect and report; do not mutate components or claim runtime parity. |
| Ultra 23d977 | Adversarial test matrix | Produce the test matrix; it does not authorize implementation or lifecycle action. |

The living request is to carry Flow locks, Message queue/deadline state, and Field recovery through the handoff. Message remains the durable request/receipt authority; Flow remains exact logical/native identity and lifecycle authority; Field recovery is lifecycle work under its exact authority. A submitted message is not delivery, acknowledgement, execution, or a new owner.

Low e798f3 has directly acknowledged the read-only audit. The f72 full coordination proposal is acknowledged by root and the division is accepted in principle only; root submitted it to 0ab019 and 2c61af. All current coordination sends remain **Submitted**, not **Read**. Field9ddcbc has a submitted bounded lookup for the 553901 route/status and physical-path alias; absence from HM does not release it.

## Retained handles, locks, and non-actions

f72 is **COMPLETE**, acknowledged through 0ab019; its handles remain retained. Requests to coordinate the division of work do not authorize unreserved resume of f72. Preserve reported protected locks 2836, 2862, and 2864 for f72, plus 1834 and 1835 for 553901. The Flowstore owner is unknown in this handoff; that uncertainty prevents a claim to its state, locks, or lifecycle actions.

No item here authorizes releasing a lock, retiring a route, killing a session, resuming a closed native, or transferring ownership. Where implementation needs a path, Medium coordinates the actual reservation first. Existing reserved writers and the completed/restricted boundaries remain in force.

The proposed division is preparatory: Medium is to enumerate and reserve Flow `store.rs` plus registration/rebind/tests. The intended retained f72 Message writer set is `src/{tables.rs v7,runtime_model.rs,delivery_gate.rs,engine.rs,delivery_receipts.rs}` with exact tests, only after reconciliation. `signal-flow` `ethos/signal.ethos` plus generated source/contract tests and `signal-message` ethos/generated work are separate producer sets; neither is newly owned or reserved. Historical FieldSol `codex.rs` scope belongs to 8565e8 and is not new Mind Medium work. The retained isolated lock paths are `/home/li/wt/github.com/LiGoldragon/{flow,signal-flow,message}/night-messaging-0ab019`.

## Audit posture and qualification

The current audit evidence distinguishes remote state from local tracking state. A remote relationship or a local branch/tracking report is not, by itself, proof of deployed runtime parity. Persona's reported 17-ahead migration state likewise identifies migration work, not an accepted deployed cutover. Orchestrate's reported unmerged session/lane lines remain coordination evidence, not a basis to infer a live owner, a released lock, or a successful delivery.

Runtime parity remains unknown until an exact runtime witness establishes the deployed artifact, configuration, and behavior at the relevant endpoint. This handoff does not rerun probes or reinterpret source/branch observations as runtime evidence. It preserves Field recovery as a distinct dependency: an unavailable or ambiguous target yields the typed recovery/uncertainty route already established by the checkup architecture, rather than autonomous restart or reaping.

## Related architecture and next boundary

The published [context-usage Nexus integration contract](context-usage-nexus-integration.md) defines the observation/query/process/SEMA boundaries for native context usage. It establishes that snapshot observations, source epochs, and metric uncertainty do not grant lifecycle or Message authority. The [Field census and Mind checkup architecture contract](field-census-and-checkup-architecture.md) defines the Field observation, Flow identity, Message receipt, duty, recovery, and structural-invariant boundaries. Neither report turns this handoff into an implementation mandate outside explicit reservations.

The next operational transition is evidence-driven: Medium accepts or refuses the submitted request through the owned delivery path; any implementation begins only after exact reservations are coordinated; Low and Ultra return bounded audit/test evidence. Deadlines remain Message-tracked rather than reconstructed from terminal presence. If Field recovery is required, route it to the configured lifecycle owner with identity/provenance evidence. Missing acknowledgement, unknown owner, or stale tracking state remains uncertain and does not create a replacement actor.

## Sources

- **Current conversation/living request:** owner4b0f60 acceptance of Mind Medium2c61af; submitted `hm-send` assignments to Medium2c61af, Low e798f3, and Ultra23d977; Low's direct audit acknowledgement; f72 division accepted in principle and submitted to 0ab019/2c61af; Field9ddcbc bounded lookup; retained f72/0ab019 status and handles; reported locks 2836/2862/2864 and 1834/1835; required Flow-lock, Message-queue/deadline, and Field-recovery handoff. These are current coordination statements, not independently rechecked runtime facts.
- **Audit evidence:** source-map/audit findings returned by `/root/census_contract_design` and `/root/checkup_architecture`, including remote-versus-tracking qualification, Persona 17-ahead migration, Orchestrate unmerged session/lane lines, unknown Flowstore ownership, and runtime-parity limits. Report-path precision is pending those companions' reply; no runtime claim is made from the summaries.
- **Related committed architecture:** `flows/4b0f60/reports/context-usage-nexus-integration.md` and `flows/4b0f60/reports/field-census-and-checkup-architecture.md`; used only for established identity/evidence/recovery boundaries.
