# SD Versioned-State Grand Design Exchange Critique

Variant: Audit.
Role: system-operator.
Source reviewed: the psyche / system-designer exchange about report 95,
including SD's Spirit captures `i4ak`, `x0ja`, `jys2`, the visible frame at
`reports/system-designer/95-versioned-state-grand-design/0-frame-and-method.md`,
and the prior operator audits 211 and 212.

## Verdict

The exchange moved the design in the right direction. SD correctly recognized
that the ask was not "add a backup log" anymore; it became a foundational
database-DVCS design with branches, forks, rebase, merge, backup/mirroring, and
per-component policy. The most important design move in the exchange is the one
the psyche named back to SD: **`IntakePolicy` becomes a universal reusable
admission interface, with per-component implementations**.

I recorded that narrower point as gap-fill Spirit record `2uhh` because the
earlier record `i4ak` captured per-component policy generally, but did not quite
capture the universal-interface clarification. The rest of SD's three captures
look valid.

My main caution: SD's architectural preview is promising but too confident in a
few places before the research/prototype has landed. The claims about being
cheaper than Dolt, migration-as-branch, and rebase-through-guardian should be
kept as hypotheses until report 95 shows the exact invariants, failure modes,
and executable witnesses.

## Spirit And Process Feedback

SD was right to run the Spirit gate. The prompt contains durable psyche intent:
this version-control layer is foundational, it must support database-level DVCS
semantics, it must use consistent crypto, and it should aim at a post-agent best
end-shape rather than a historically cautious compromise.

The three records are mostly well-formed:

- `i4ak` captures the foundational DVCS scope and per-component policy. I would
  keep it.
- `x0ja` captures the blake3 plus criome-BLS consistency constraint. It is a
  little stronger than the exact wording because it says no component diverges,
  but that is a fair clarification of "same hashing mechanism, same crypto"
  for a reusable system-wide substrate.
- `jys2` captures the post-agent design principle. It should be treated as
  license to consider better end-shapes, not as license to skip operational
  witnesses.
- `2uhh` now captures the gap-fill: `IntakePolicy` is the universal admission
  interface with per-component implementations, not just a rebase callback.

The process weakness is that SD guessed the live Spirit shape several times
before reading the current CLI skill/source. That created noise and led to
unsupported narration like "schema changed since earlier today" and "likely
deployed." The durable lesson is simple: before Spirit writes, read
`skills/intent-log.md` and `skills/spirit-cli.md`, then query the active shape
from source if needed. The trial-and-error did eventually converge, but the
first few calls were avoidable.

## Design Feedback

The `IntakePolicy` generalization is the strongest part of the exchange. It is
the right abstraction if it stays semantic, deterministic, and replayable. The
core should not own Spirit's guardian logic, but it should own the universal
shape: an entry attempts to enter a branch, the component policy sees enough
context to decide, and the decision becomes part of durable history.

The four caller model is right:

- local write;
- rebase replay;
- merge/import from another branch;
- remote ingest or pull from a peer.

The subtle correction is that "remote ingest" has two meanings and they must not
be conflated. A dumb backup mirror can validate hash-chain continuity and BLS
authority without understanding Spirit semantics. A semantic peer importing
entries into a component branch must run the component `IntakePolicy`. If the
server is only the remote append store, it should not become an accidental
guardian service. If the server is a semantic collaboration node, then it needs
the component policy code, schema set, and authority model explicitly.

Rebase-through-guardian is also a good fit, but it is not plain Git rebase. If
Spirit's guardian can reject or transform entries, the rebase creates a new
semantic history, not just a different parent pointer. The durable log needs to
record original-entry lineage, the target base/head, the guardian verdict, any
transformed payload, and the policy/schema identity that produced the verdict.
Without that, later auditors cannot explain why a rebased branch differs from
the original suffix.

Merge needs a separate interface from admission. `IntakePolicy` answers "may
this entry enter this branch?" It does not by itself answer "how do two
concurrent writes to the same family combine?" A sibling `MergePolicy` or
per-family reducer is still needed for conflict resolution. Some families can
commute or behave like CRDTs; other families must surface conflicts or ask the
component guardian. Keeping admission and conflict resolution distinct will keep
the reusable core from becoming a vague policy bag.

The crypto direction is right, but report 95 should draw the layers carefully:
blake3 for entry, checkpoint, segment, and state identity; BLS for signed heads,
checkpoints, mirror acknowledgements, or quorum attestations. It should not
casually imply BLS on every hot-path entry unless that cost and key-management
shape are intentional.

The post-agent frontier principle is useful, but it changes only the migration
cost model. It does not remove correctness cost. Agents can rewrite large
stacks, but the system still needs small typed nouns, replay witnesses,
checkpoint restore witnesses, crash boundaries, and branch-policy auditability.
The design should use the freedom to choose the clean end-state, not to hide
complexity behind "agents can fix it later."

## Claims To Reframe As Hypotheses

"Branching is cheaper than Dolt" is plausible for log suffixes, but incomplete
for checkpoints and distant peers. Branch creation can be O(1), and suffix diff
can be cheap when both sides share a base. Full-state transfer after pruning,
large checkpoints, schema discontinuities, and peer cold-start may still need a
Merkle state structure or chunked checkpoint segments. SD already noticed this;
the final report should keep that nuance.

"You never need prolly-tree machinery to compute a diff" is true only for
operation-log diffs on unpruned shared history. It is not automatically true for
state snapshots, cold restore, partial checkout, or cross-schema comparison.
Report 95 should say exactly where structural trees are rejected and where they
remain candidates.

"Migration becomes a branch" is the right metaphor, but the design must specify
whether migration replay preserves original commit sequence, emits a synthetic
checkpoint, signs a new head, and leaves old entries available for audit. The
operator audit 212 already called out that a checkpoint digest alone cannot
restore state; migration-as-branch only works if the post-migration checkpoint
has payload or content-addressed segment references.

"The guardian protects Spirit identically no matter how an entry arrives" is the
right invariant. The report should also show the bypass cases it prevents:
direct table import, raw mirror restore without semantic admission, replay under
the wrong schema/policy identity, and transform without durable verdict logging.

## What Report 95 Should Show

The visual design should not be a decorative architecture overview. It should
show the actual moving parts and what each invariant protects:

- commit DAG: branch heads, parent digests, merge parents, per-branch sequence
  cursors, and monotonic sequence versus digest identity;
- write path: component command to `IntakePolicy`, engine transaction, payload
  log entry, materialized view, outbox, mirror acknowledgement;
- rebase path: source suffix, target base, per-entry policy admission,
  transform/reject outcomes, new entries with lineage;
- merge path: shared base, candidate entries, per-family merge policy,
  admission gate, conflict surface;
- backup path: local log/checkpoint to remote append store, expected-head
  validation, idempotent duplicate handling, fsync acknowledgement, signed head;
- restore path: checkpoint payload or segments plus suffix replay into a fresh
  engine, then normal query-surface equivalence;
- migration path: side branch, reducer/checkpoint, state digest oracle, signed
  head swap, and retained old-history policy;
- cleverness section: version the log not the store, universal admission gate,
  policy-mediated rebase, verifiable mirror, migration as branch, generated
  closed decoders;
- risk section: pruned-history restore, policy non-determinism, schema drift,
  remote authority, conflict semantics, and crash boundaries.

## Bottom Line

The exchange is directionally strong and the psyche's clarification about
`IntakePolicy` is probably the most reusable abstraction discovered so far in
this arc. SD should continue report 95, but the final design needs to be stricter
than the preview: every "clever" claim should come with a data path, a failure
case it solves, and a witness the operator can eventually test.
