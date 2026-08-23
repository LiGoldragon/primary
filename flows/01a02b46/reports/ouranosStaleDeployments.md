# Ouranos stale deployments: read-only diagnosis

## Outcome

The two durable nonterminal records are real and remain at `Copying`: IDs 5
and 7 have admission/state markers 62 and 98, respectively, while the current
node marker is 687. Their complete event-log phase sequences are 5:
`Submitted`/9, `Building`/10, `Copying`/11, and 7: `Submitted`/14,
`Building`/15, `Copying`/16. The later successful deployments prove that their
mere presence does not globally block durable admission.

Lojix 0.17.5 admits against an eight-slot daemon actor `active_count`, not a
count of public nonterminal records. Persisted `Copying` deploy-job rows are
startup resume candidates and could occupy slots if successfully resumed, but
the ordinary public interface does not expose those private rows or the live
count. Therefore this evidence cannot establish that a new deployment has a
free slot now, and it cannot establish that IDs 5 and 7 are inactive.

There is no typed deployment cancellation/retirement operation. `Retire` is a
generation GC-root operation and is not a safe way to resolve these records.

## Safe continuation gate

Keep the no-unrelated-active-job gate closed. Continue only after an
explicitly approved supported observation establishes the private job/activity
state, or after an explicitly approved recovery design. Do not submit, reset,
restart, activate, copy, or retire either generation as a proxy for deployment
cancellation.

## Unknowns

- whether private deploy-job rows for 5 and 7 still exist;
- whether startup resumed either row, and the daemon's current `active_count`;
- whether either pipeline is still making progress or is stalled at an effect;
- the original flow/actor that created the two records; no prior transcript
  witness was found;
- whether the installed daemon's ordinary adapter panic will be fixed by a
  compatible future version.

See the [diagnostic witness](../witnesses/ouranosStaleDeployments.md) for the
source-level recovery details, exact query interpretation, and operation
distinctions.

## Sources

- [diagnostic witness](../witnesses/ouranosStaleDeployments.md)
- [Ouranos preflight witness](../witnesses/ouranosLojixSelfUpgradePreflight.md)
- [execution report](ouranosLojixSelfUpgradeExecution.md)
