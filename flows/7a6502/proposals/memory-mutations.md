# Flow v1: complete typed Memory mutation

For Mind flowNexus Primary ee0934. This is the requested batch/restore shape against rulings 21162/21261; it is a machine proposal awaiting approval, not implemented behavior.

## One owner, one transaction

Every stored record has one definition in the shared `flow-nexus-types::memory` module generated from Memory Ethos. Both the runtime and meta contract name that definition. The ordinary contract imports only its public types. A private request id may occur in meta records and Debug, never an ordinary envelope or prompt.

Meta `Mutate` carries a vector of typed puts/removals. Operation authenticates the owner connection, then asks the component-owned Memory actor to validate and commit the whole batch as one kernel transaction. The typed reply distinguishes a definite integrity rejection, definite committed mutation, storage failure and actor-transport uncertainty. There is no persisted reply transport. A lost actor reply causes reconciliation by the private attempt identity; it does not authorize another external effect.

## Proposed vocabulary

The Ethos below belongs in the shared Memory vocabulary. Referenced domain records are those in the corrected anatomy. ConfigurationRecord and AddressReservation make explicit facts the initial scaffold did not yet hold. Queue holds private admission id, sender address, arrival order and typed request.

```ethos
Memory
[ :crate:[ Configuration Address FlowId State ] ]         ; imports
[ MetaConfigureOccurred.Boolean                           ; records: the standard first-Configure fact, named
  ConfigurationRecord.{ Configuration MetaConfigureOccurred } ;   persisted standard first-Configure metadata
  AddressReservation.{ Address FlowId RequestId }         ;   one launch reservation and the owning attempt
  VerificationTarget.[ Binding.FlowId                     ;   only executable records need restoration verification
                       Launch.RequestId
                       End.RequestId
                       Reservation.Address ]
  VerificationState.[ Unverified                         ;   imported bytes confer no process authority
                      Reconciled.StartWitness
                      RecoveryRequired.ResourceEvidence ]
  Verification.{ VerificationTarget VerificationState }
  Record.[ ConfigurationRecord                           ;   the complete set of stored record kinds
           Flow Permaflow ProcessBinding
           LaunchAttempt EndAttempt AddressReservation
           Queue Verification ]
  RecordKey.[ ConfigurationSingleton                     ;   identity of the stored row, not textual field names
              Flow.FlowId Permaflow.Address
              ProcessBinding.FlowId
              LaunchAttempt.RequestId EndAttempt.RequestId
              AddressReservation.Address Queue.Address
              Verification.VerificationTarget ]
  Mutation.[ Put.Record Remove.RecordKey ]
  MutationBatch.Vector<Mutation>
  ReconciliationTarget.VerificationTarget
  Invariant.[ DanglingReference.RecordKey                 ;   rejection points to a typed target
              DuplicateIdentity.FlowId
              DuplicateAddress.Address
              HistoryOwnership.FlowId
              PredecessorCycle.FlowId
              PredecessorAddress.FlowId
              QueueOrder.Address
              AttemptReservation.RecordKey
              SnapshotMismatch.RecordKey
              UnresolvedEffect.RecordKey
              LiveResource.RecordKey
              ReconciliationRequired.VerificationTarget
              StoreRelocation ] ]
```

The corresponding meta input adds `Mutate.MutationBatch` and `Reconcile.ReconciliationTarget`, with paired typed accepted/refused outputs. `Debug` and a typed meta record selector expose the persisted projection; ordinary Observe excludes private admission identities. Exact Input/Output/root capability generation follows the upstream approved generator, not local aliases for its old Query/Response output.

## Result-state validation

The Memory handler applies changes to a candidate resulting state, validates it whole, then commits or changes nothing:

- Each reference resolves in that resulting state. Every Flow appears in exactly one matching address's Permaflow history. Histories are ordered vectors with no repeated identity.
- Predecessors exist, belong to the same address and form no cycle.
- At most one active Flow/reservation owns an address. FlowIds are unique. A launch reservation and attempt agree on private attempt id, reserved FlowId, address and resolved snapshot.
- Queue arrival orders increase strictly within each address and are retained across append/restart. Admitted request identities are unique.
- Profile/module references resolve uniquely. An active attempt retains the resolved configuration and captured content it started with.
- Effective MemoryPath agrees with the opened store. Configure is not live relocation.
- Deleting an active Flow, binding, attempt or reservation requires verified stop/absence. Deleting metadata is never an exit witness.
- A change conflicting with an unresolved effect is rejected or remains reserved for explicit reconciliation. It cannot erase uncertain resources.

The Memory actor performs typed atomic state changes only. External observation and reconciliation are Operation's effects; a transaction consumes server-owned reconciliation evidence, not an owner's assertion that a process exited. Every later execution rechecks the exact process incarnation/resource target.

## Restoration and authority

A meta put of historical records can become durable after integrity validation. A meta put of a binding, active attempt or active reservation stores it as **Unverified** and makes its address unavailable for new conflicting work. It cannot launch, kill, submit a prompt, or authenticate a caller by being written. The explicit Reconcile operation inspects kernel/session resources, then requests one atomic verification transition. Ambiguity yields RecoveryRequired and keeps the reservation.

The `Verification` record is itself writable through meta, but requesting its Reconciled variant without server-owned matching evidence yields ReconciliationRequired. This retains complete record coverage while preserving the distinction between requesting a state change and proving its external prerequisites. The owner cannot synthesize authority from archived process fields.

Fresh next writes configuration/declarations/models into an empty store; it restores no history, queue, active binding or old Herdr handle. The complete mutation surface supports later, independently tested migration; it does not activate migration now.

## Decisions requested

Approve or refine this explicit verification-record projection versus embedding verification in each executable record. Confirm where private monotonic request/arrival allocation counters live: a typed allocator record would also join Record/RecordKey and meta coverage. No missing allocator fact should be hidden in an untyped table or inferred solely from live records. Once settled, the meta schema and Memory handler can be implemented together against these invariants.
