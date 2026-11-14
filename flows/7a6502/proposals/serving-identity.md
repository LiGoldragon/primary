# Authenticated entry and OS identity: proposed next anatomy

Latest scope: Psyche22197/22220/22240 and Primary22222/22239 supersede the cgroup/ancestry authentication proposal below. Socket permissions alone authenticate; ordinary access permits Launch bound or unbound. Process-derived identity is retained for Send routes, not an added Launch gate. No cgroup/UID/ancestry authentication prerequisite or host provisioning. OS wrapper shape approved22230: small platform crate; implementedb5c9722. Historical alternatives below are retained as proposal history, not current implementation authority.

For Mind flowNexus Primary ee0934, following22171. Implementation proposal, not psyche. No bodies for this slice yet. Internal checkpoint: Flow9c063a58870a770dde5f6340bf54f42be4358847, tests04d30131920f110270213b9d9907dbeaeeb2d9c0; independently47 green.

## Observation and authority

Two listeners own their socket role. Accepted Unix connection captures kernel peer UID/GID/PID before packet decoding. A private-field ConnectionContext carries socket role, kernel credentials, observed process incarnation and classified principal. No packet field, public constructor or deserialized context creates authority. Ordinary and meta admission are separate capabilities; Operation receives context beside the decoded input. Context is not a Memory row and imported records cannot mint it.

Linux evidence mechanism proposed: SO_PEERCRED on accepted socket; process start ticks and PPid from proc stat; device/inode of proc PID namespace; boot ID. Open proc process directory and retain a pidfd where available to detect peer death/PID reuse, compare start ticks and each parent edge before/after traversal. Server proc visibility and credentials must use the same PID namespace; initially refuse unsupported cross-namespace mapping, access denial, disappearing or changed ancestry. Namespace-private filesystem paths alone do not imply PID namespace equality.

Binding classification checks all managed candidates first. An exact verified binding on the live ancestry yields FlowCaller(Address); any matching unverified/restored candidate, inconsistent chain, ambiguous match or unavailable witness yields Uncertain and refuses. Route denial on a FlowCaller never falls back to owner. Meta owner permission and ordinary OwnerLauncher remain distinct policies.

**Uncovered decision:** current PPid ancestry cannot prove historical non-descent after a flow descendant reparents or is adopted by a subreaper. UID equality plus a currently unmatched chain is insufficient to prove OwnerLauncher is unbound. Choices needing Primary judgment: require an independently trusted operator-root process incarnation whose ancestry chain must be witnessed for OwnerLauncher, or add lifetime process membership evidence (such as enforced distinct cgroup per managed flow). Neither is present in current configuration/launch proof. Until a sufficient mechanism is chosen, owner bootstrap Launch remains unavailable rather than elevating an unmatched same-UID peer. Sandbox tests can exercise explicit classification evidence without claiming general absence proof.

No real model launch: first serving proof uses sandbox Unix child peers, actual accepted credentials, ordinary/meta separation, forged claimed addresses, verified-bound precedence, route denials, missing/unverified binding and ancestry-race refusal. Bound authority tests require a private trusted fixture witness rather than owner-written Verification rows becoming authority. Production live-verification producer remains unavailable until implemented.

## Proposed implementation traits (signatures only)

Rust proposed surface; no generated conformity claim:

```rust
trait PeerObservable {
    type Observation; type Failure;
    fn observe(&self) -> Result<Self::Observation, Self::Failure>;
}
trait PrincipalClassifiable {
    type Observation; type Bindings; type Principal; type Failure;
    fn classify(&self, peer: &Self::Observation, bindings: &Self::Bindings)
        -> Result<Self::Principal, Self::Failure>;
}
trait OrdinaryAdmissible {
    type Context; type Input; type Authorized; type Refusal;
    fn admit(&self, context: &Self::Context, input: Self::Input)
        -> Result<Self::Authorized, Self::Refusal>;
}
trait OwnerAdmissible {
    type Context; type Input; type Authorized; type Refusal;
    fn admit_owner(&self, context: &Self::Context, input: Self::Input)
        -> Result<Self::Authorized, Self::Refusal>;
}
```

Bearers: accepted connection for observation, process-observation policy with trusted root/membership facts for classification, socket-role entry configuration for admission. Authorized envelopes have private fields. No behavior-only namespace. Transport closes on malformed/oversize/archive validation failure; authorization returns typed refusal where an input has been decoded; disconnect never rolls back committed Memory. No detached store-owning tasks. Connection actors finish or cancel their own IO on shutdown, Memory shutdown still owns all transactions.

Shared Signal0cad1d1 exposes AsyncFrameReading::read_frame(capacity) and AsyncFrameWriting::write_frame(body,capacity), Signalizable and Restorable archive validation. Its exchange IDs stay private transport state and grant no authority. Exact current closure and depth/capacity configuration must be checked at integration; reuse compatible framing/validation, not private Nexus Admission.

## OS-backed identity capability

Existing IdentityPolicy is data-bearing and can bear Identifiable plus an entropy-fill capability. Proposed default mint algorithm validates configured alphabet, performs six independent byte rejection selections (accept byte below 256 minus 256 modulo alphabet length), and returns case-sensitive FlowId. No fixed alphabet or path in generation logic. Linux getrandom is the proposed OS source; libc is already pinned0.2.191 transitively, direct use requires explicit dependency and closure update. Interrupted reads retry only while cancellation is unset; OS failure is typed. Nonblocking entropy mode is proposed so uninitialized entropy yields typed unavailable instead of an uninterruptible wait.

A stateful scripted source supplies deterministic test entropy through the same trait; production bearer is the configured policy, not a zero-sized randomness namespace. Tests include rejection sampling, six selections, invalid alphabet, interrupted/short reads, entropy error and cancellation. OS-only smoke test demonstrates actual syscall success separately from deterministic distribution logic.

Reservation orchestration retries only definite IdentityCollision, never transport uncertainty. Count unique occupied valid six-character IDs from all relevant historical/current records against alphabet_size^6 using checked arithmetic (maximum62^6 fits u64); intentional reservation/attempt/Flow links count once. Exhausted returns typed exhaustion. Before each candidate/retry, cancellation is checked; non-saturated repeated random collisions yield cooperatively, not a CPU spin. Saturation and collision are distinct from RequestId CounterAdvanced, which requires a new observed expected counter. Exact payload ticket recovery remains unchanged.

**Judgment requested:** approve these mint capability/algorithm/dependency shapes, and choose sufficient OwnerLauncher non-descent evidence before authenticated serving bodies depend on it. No external Translator/effect implementation is implied.

## Existing shutdown/saturation evidence (22158)

Current Flow handlers call MemoryStore synchronously; Store::mutate validates then calls kernel.write synchronously, with no await/spawn/spawn_blocking. Actor on_stop drops store; restart waits shutdown before exclusive same-file reopen. No Flow-owned store work is detached. Any future blocking offload needs a new joined ownership witness before recovery.

The saturation test current-thread executor manually polls64 readonly asks, then manually polls submit and asserts Pending at its sole pre-ticket mailbox await before dropping it. It does not infer pending merely from capacity. Actual death-before-processing test polls submission to confirmed enqueue, interrupts before yielding, observes uncertain reply, then shutdown/reopen resolves absent. Immutable19 reservation tests and full47 are green; these are internal lifecycle witnesses, not external process authority.
