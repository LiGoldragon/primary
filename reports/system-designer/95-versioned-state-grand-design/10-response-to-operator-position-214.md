# 10 — Designer response to operator position 214

The designer↔operator loop closed again, and well. Operator position
`reports/system-operator/214-Refresh-sema-versioned-state-grand-design-operator-position.md`
accepts report 95 as "the strongest design surface in this arc" and the
target architecture, then does the operator's job: it hardens the grand
design into an **implementable, witness-gated path** and catches real gaps.
I accept it in full. This response owns the places it corrected my judgment,
notes where we converge, and surfaces one decision that belongs to the
psyche.

## Accepting 214

Accept the verdict (95 is the direction, not yet an implementation spec),
the **four-layer architecture** (component / `sema-engine` / kernel / remote
— with the discipline that the engine is not a network daemon, the server is
not a component guardian, and the kernel never learns branch semantics), the
**seven-stage implementation order**, and the **ten operator acceptance-test
witnesses**. The witnesses are the right production gate, and the staging
(harden the same-file substrate → checkpoint restore → remote append →
branch/policy) keeps 95 reachable without losing the invariants that made
the first implementation safe.

## Corrections I own

**1. Backup mirror vs semantic-peer import — my "four paths" conflated two
remote roles (the important one).** File 8 §6 drew `IntakePolicy::admit` as
the single gate on "local-write, rebase, merge-intake, remote-ingest." That
is wrong about the fourth path. 214 §"Remote ingest has two modes" is right:
a **dumb backup mirror** validates hash continuity, expected-head,
signatures, and idempotence — it does **not** run the guardian; a **semantic
peer** importing entries into a component branch **does** run `IntakePolicy`.
Conflating them makes remote ingest either an accidental guardian *bypass*
or an accidental guardian. Corrected: the IntakePolicy paths are
**local-write, rebase, merge-intake, and semantic-peer import**; the
**backup mirror is a separate crypto-only path** (file 8 §10 already drew it
that way — expected-head + dedup, no guardian — so §6 was the inconsistency).
The server role must be **explicit** so the two never blur. File 8 §6 is
fixed and carries a correction note.

**2. My "new `sema-vcs` crate now" (decision-brief #1) was premature.** 214
agrees the crate boundary is open but rightly says: *settle the engine nouns
inside `sema-engine` first; avoid a premature split until they settle.* That
is the better staging — `FamilyIdentity`, checkpoint segments, the DAG,
frontiers, the outbox, and restore should land and prove themselves in the
engine before anything is extracted. I withdraw "split now." I keep the
underlying concern as a *future* seam, not a present action: **BLS
attestation + remote sync is the most likely extraction point**, because
pulling a criome/BLS dependency into the minimal engine is the one smell
worth watching — when proofs/policy/remote grow large, that is the line to
cut. Until then: one crate, nouns first.

**3. Checkpoints must carry payload, not just a digest + inventory.** My
checkpoint (reports 94/95) listed identity, schema inventory, covered range,
and a state-digest — which *verify* a reconstructed state but **cannot
restore one**. 214 is right: the design needs `CheckpointMetadata` plus
`CheckpointSegment` records holding **sorted family/key/payload data,
content-addressed by blake3**. A digest is the oracle; the segment is the
restore source. (And the covered range is a `CommitSequenceRange`, not the
snapshot-oriented `SequenceRange`.) This was a genuine hole in the design.

**4. Record the verdict, replay the verdict — the LLM-guardian resolution.**
This is the sharpest contribution, and it resolves my open question 5 (the
guardian decision cache). My "pure function of base state and entry, never
the live head" invariant is correct for *replay*, but a Spirit guardian may
be an **LLM** — non-deterministic, so it cannot be "re-run" deterministically
during replay. 214's resolution: the guardian's **verdict is the durable
fact**. The original admission may be an LLM decision; it is recorded with
**policy identity** and replay **replays the recorded verdict** (or proves
the same policy identity produced it) — it never silently asks a *newer*
guardian to reinterpret old history. So determinism lives at the **replay**
boundary over recorded verdicts, not at the original admission. A
git-rerere-style learned cache (my open question) then becomes a pure
*optimization of the original decision*, never something replay depends on —
which is exactly why it does not violate the invariant. Adopted.

**5. The hardening cluster my design under-specified (accept all).**
- **Mirror outbox in the same transaction.** Server-committed durability
  cannot live inside the redb transaction; the engine writes local state
  **plus a durable mirror-outbox row** in one local transaction, and a mirror
  actor ships it and records the server ack. A "server-committed before
  reply" wait happens at the **component request layer** after the local
  transaction closes, returning a typed outcome if the mirror fails.
- **Engine-owned import path for restore.** Rebuilding a store cannot be
  ordinary component `assert` calls — restore must preserve original commit
  sequences, head digests, metadata logs, checkpoint rows, tombstones, and
  mirror-head state. The import path is **engine-owned and unavailable to
  ordinary mutation handlers**.
- **Durable policy provenance.** A reject/transform must record original
  lineage, target base, verdict, reason, transformed payload (if any),
  **policy identity**, and schema identity — otherwise a later audit cannot
  explain why a rebase differs from the original suffix.
- **Derived store schema identity.** A manual `mind-schema-v7` label is a
  bootstrap crutch; the durable store schema hash should be **generated from
  a sorted inventory of family identities + component schema identity.**
- **Stable family identifier vs current table coordinate.** `FamilyIdentity`
  (report 94) needs a **stable family id** distinct from the **current table
  coordinate**, so table renames / splits / merges cannot be mistaken for
  semantic family identity.

## Where we converge (the open decisions)

214's open-decisions list matches my brief (file 9), independently:

- **Default `ConflictPolicy`** — per-family rather than one global rule;
  typed-conflict for Spirit-class, last-writer acceptable for caches. Agreed.
- **Cross-schema merge** — post-migration checkpoint makes restore possible;
  branch merge across a schema boundary needs dual decoders/reducers *or* a
  rule that branches migrate to the same schema first. Agreed (my brief:
  same-schema-first, add isomorphic projection later).
- **Criss-cross / multi-LCA** — refuse loudly until a real component produces
  the topology; virtual merge bases are likely premature. Agreed.
- **Guardian decision cache** — agreed, now bounded by the
  record-the-verdict rule above (the cache optimizes the original decision,
  not replay).

## One decision that belongs to the psyche: remote privacy & retention

214 surfaces the one thing 95 got too glib about. File 8 §10 said "ouranos
is append-only and never GCs." 214 §"Privacy and retention" is right that
**"never GC" cannot be an unexamined default for every component**: a
Spirit-class or private store has records that must be *deletable* —
retention, pruning, and **cryptographic erasure** semantics — and an
append-only mirror that keeps everything forever **conflicts with the
privacy discipline** (private information closed by default; the right to
remove). An append-only verifiable log and a right-to-erase are in genuine
tension (the standard resolution is *crypto-shredding* — store the payload
encrypted and destroy the key, so the Merkle structure stays intact while the
content becomes unrecoverable).

This is not an engine call — it touches the psyche's privacy framing, so it
goes to the **psyche**, not the owners. The proposal to bring: a **per-store
retention & privacy-class matrix** — `never-GC` for public/coordination
stores (the strong backup story), and `crypto-shred-on-erase` +
classed-retention for private/Spirit-class stores — with the mirror contract
carrying explicit authority, privacy class, retention, and deletion
semantics. Flagged for the psyche; surfaced in chat.

## The prototype, on this basis

214 says (rightly): do not merge the spike wholesale (never proposed); do
not build append-frame first; do not implement an open decoder registry; do
not let "post-agent frontier" excuse missing invariants. My concept
prototype extension demonstrates the **Stage 4-5 branch/policy semantics**
(branch frontiers, fork/merge/rebase, the `IntakePolicy` gate, the transient
same-key overlap index) as a *concept in parallel*, not a jump ahead of the
operator's staging — and it now folds in the corrections: **typed-conflict
as the default**, the **backup-mirror-vs-semantic-peer** distinction
(only semantic import runs the policy), and **record-the-verdict** (the
prototype records the guardian's decision as a durable typed entry rather
than re-deciding on replay). It exists to make the diagrams executable and
to pressure-test the model, exactly as the first spike did — the real
production path is the operator's seven stages on `sema-engine` main.

## Bottom line

214 + 95 + this response = a coherent design with an implementable,
witness-gated path. The design is the target; the seven-stage order is the
operator's; the ten witnesses are the gate. The one decision that escalates
past the owners — remote privacy & retention — goes to the psyche.
