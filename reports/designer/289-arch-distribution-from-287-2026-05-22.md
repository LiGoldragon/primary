# 289 - ARCH distribution from /287 (2026-05-22)

*Distribution of `/287`'s version-handover substance into the affected
per-repo `ARCHITECTURE.md` files. Five ARCH files edited and committed
in their own repos; persona meta repo deferred because operator has
in-flight changes there. Per psyche directive 2026-05-22: "is /287 in
architecture I like what I see, lets put that in the design in
architecture files (copy relevant parts to the right components) - you
can expand and rewrite the parts of the architecture that seem
contradictory, and report back with what you changed there and why in
your report."*

## TL;DR

Five per-repo ARCH files now stand on their own with /287's substance
inlined: `version-projection` (rewritten — was a thin pointer to the
spec report, now carries the full trait/policy/index shape);
`signal-version-handover` (restructured to the architecture-editor
template, added owner-contract pending in Possible features);
`sema-engine` (added a dedicated `CommitSequence — durable high-water
mark for handover` section, tightened the constraints); `sema-upgrade`
(named its two-role position in the stack, added Possible features for
the future daemon and Mirror payload application); `persona-spirit`
(added the explicit `Active / HandoverMode / PrivateUpgradeOnly` state
machine diagram beside the existing three-socket coverage). Persona
meta repo skipped — operator has six modified files in flight there
including ARCHITECTURE.md, and the existing persona architecture
already names the engine manager's upgrade-orchestration role. All
five commits pushed to `main`.

## §1 What was changed in each repo's ARCH

### §1.1 version-projection

The previous file was 55 lines and contained `reports/designer/285-...`
as its second sentence — a direct violation of
`skills/architecture-editor.md` §"Architecture files never reference
reports". The rewrite removes the report reference and stands as a
self-contained per-repo architecture per the template:

- TL;DR
- Components table
- Projection contract (with trait signature inlined, plus the
  bidirectional + Identity story)
- Policy is separate from projection (load-bearing split between trait
  and runtime behaviour)
- Version identity (ContractVersion 32-byte hash)
- Migration index (compile-time lookup for historical decoders)
- Boundary mermaid diagram showing relations to signal-version-handover,
  signal-sema, runtime crates, and persona-introspect
- Constraints (8 testable obligations)
- Non-Goals (5 items)
- Possible features (3 open questions: owner-side handover authority
  contract; typed Mirror payload shape; per-operation policy generation)
- Code Map
- See also (sibling ARCH files, not reports)

### §1.2 signal-version-handover

The previous file was 35 lines with no `Constraints` / `Possible
features` sections; structure was idiosyncratic. The rewrite restructures
to the architecture-editor template:

- TL;DR (3 sentences)
- Components table
- Protocol shape (operation table + mermaid sequence diagram showing
  marker / readiness / completion / mirror / divergence flow with
  drift-recovery branch)
- Wire vocabulary (the `signal_channel!` macro instantiation inlined)
- Boundary mermaid diagram showing the per-version private upgrade
  socket as a node between two daemons
- Constraints (7 testable obligations)
- Non-Goals (4 items including no atomic-write magic, no selector flip
  decision, no write-freeze enforcement)
- Possible features (companion `owner-signal-version-handover`,
  typed Mirror payload shape, read-during-handover semantics)
- Code Map
- See also

### §1.3 sema-engine

The previous file already had eight constraints touching `CommitSequence`,
but the framing as the **handover** high-water mark was only one bullet.
Two changes:

1. Tightened the existing constraints: added two new bullets making
   explicit that `Engine::current_commit_sequence` returns the durable
   high-water mark and that failed commits don't advance the counter
   (the latter survives reopen).
2. Added a new dedicated section **CommitSequence — durable high-water
   mark for handover** between `Current Surface` and `Non-Goals`. The
   section names the cross-daemon role explicitly: a next-version
   daemon asks current for N, copies state at N, replays from N+1.
   Names `Engine::current_commit_sequence` and `replay_from_sequence`
   as the API surface. Distinguishes `CommitSequence` (cross-daemon
   handover boundary) from `SnapshotId` (subscription replay cursor).

No contradictions; the existing constraints already aligned with
operator commit `e0a7153c`. The new section is pure framing of
existing behavior.

### §1.4 sema-upgrade

The previous file already named `src/handover.rs` as the prototype state
machine and described both `spirit-migration-sandbox` and
`spirit-smart-handover-sandbox`. Two changes:

1. Added a new TL;DR paragraph at the top naming the crate's
   **two roles** in the version-handover stack: protocol witness
   (`src/handover.rs`) and end-to-end sandbox host (Nix-owned apps).
   Names the future `sema-upgrade-daemon` as not-yet-existing.
2. Added a new **Possible features** section at the bottom covering:
   the future `sema-upgrade-daemon` (open question: does it emerge
   separately or does the persona engine absorb the orchestration);
   Mirror payload application on the production socket (still missing
   for production cutover); retiring `sema-upgrade-handover-temporary`
   (the temporary runner exists only because deployed v0.1.0 lacks the
   upgrade socket).

No contradictions; the existing sandbox descriptions and the limitation
paragraph after `spirit-smart-handover-sandbox` correctly named the
v0.1.0-doesn't-have-the-socket-yet truth post-/161. The Possible
features section formalises future work that was implicit.

### §1.5 persona-spirit

The previous file already had three-socket coverage in the daemon
section (lines 105-120 of the pre-edit file) and Status section bullets
naming the upgrade socket + handover frame handling as implemented.
What was missing: an explicit **state machine** diagram naming
`Active / HandoverMode / PrivateUpgradeOnly` as defined in /287 §4.

Added a mermaid stateDiagram-v2 right after the upgrade-socket
paragraph, plus three short bullets defining each state's socket-serving
behavior:

- Active: ordinary, owner, and upgrade sockets all serve; public writes
  accepted.
- HandoverMode: ordinary and owner sockets serve reads only; public
  writes paused; upgrade socket exchanges with sibling daemon.
- PrivateUpgradeOnly: ordinary and owner socket paths removed; only
  upgrade socket bound; receives mirrored writes from next.

The existing Constraints / Status sections already cover the witnessing
discipline: the test
`persona_spirit_daemon_serves_version_handover_frames_through_upgrade_socket`
proves the upgrade socket path, and the constraint "Handover completion
removes the ordinary and owner socket paths" names the
PrivateUpgradeOnly transition's observable effect. No contradictions
needed rewriting.

## §2 Contradictions found + how they were rewritten

### §2.1 version-projection's report citation

**Found**: the file's second sentence read "...the version-handover
foundation described in `reports/designer/285-...`". This violated
`skills/architecture-editor.md` §"Architecture files never reference
reports". Reports retire; numbering shifts; the architecture has to
stand without time-stamped citations.

**Fix**: the rewrite inlines the substance directly. The whole file is
now self-contained — trait signature, policy taxonomy, migration index
shape, ContractVersion as 32-byte Blake3 hash, the Identity blanket
impl, and the load-bearing trait-vs-policy split are all stated in
present tense in the architecture body. The Possible features section
names report-tracked open questions as **questions** (with a "Lean:"
direction), not as report pointers.

### §2.2 signal-version-handover lacking template structure

**Found**: the previous file did not have a Constraints section or a
Possible features section, despite the architecture-editor template
naming both as load-bearing (Constraints as the test seed; Possible
features as the uncertainty home off the reports lane).

**Fix**: the rewrite adds both. Seven Constraints are testable
obligations (e.g. "Operations and replies round-trip through rkyv and
NOTA inside `tests/`") suitable for direct witnessing. Three Possible
features cover the owner contract, typed Mirror payload, and
read-during-handover wire questions.

### §2.3 sema-engine's CommitSequence framing thin

**Found**: not a contradiction strictly, but the existing eight
constraints touching `CommitSequence` were buried in a 90-bullet
Constraints section. A reader could miss the cross-daemon handover
purpose entirely.

**Fix**: added a dedicated section between `Current Surface` and
`Non-Goals` that names the handover purpose explicitly, distinguishes
the cross-daemon role from `SnapshotId`'s subscription-replay role,
and points at the load-bearing API methods. The existing constraints
stay where they are; the new section is pure framing.

### §2.4 sema-upgrade's role-naming implicit

**Found**: not a contradiction, but the crate's **two simultaneous
roles** in the version-handover stack (protocol witness via
`src/handover.rs`; end-to-end sandbox host via Nix apps) were spread
across the file's Handover Prototype and Nix Live Sandbox sections
without a top-level naming.

**Fix**: added a single paragraph at the top of the file naming both
roles + flagging the future `sema-upgrade-daemon` as not-yet-existing.
Names the persona engine's orchestration role as the alternative path
(open question whether `sema-upgrade-daemon` emerges separately).

### §2.5 persona-spirit's handover-state-machine implicit

**Found**: not a contradiction, but the daemon's state transitions
through `Active / HandoverMode / PrivateUpgradeOnly` were only implicit
in the daemon section's prose ("removes the ordinary and owner socket
paths") and Status bullets ("private upgrade Unix socket binding").
The named-state vocabulary from /287 §4 was nowhere in the ARCH.

**Fix**: added the mermaid stateDiagram-v2 + three named-state bullets
right after the upgrade-socket paragraph. Now the named states match
/287 §4 directly and the ARCH carries the state vocabulary an agent
reading only the ARCH can reason from.

## §3 Files created

None — all five affected ARCH files existed already. Per the task
description's pre-flight: the `ls` of each path returned the file, so
the work was all editing + restructuring, no creation.

## §4 Commits made

| Repo | Commit | Subject |
|---|---|---|
| version-projection | `b5adda0c` | ARCHITECTURE: rewrite without report refs, add policy/migration index sections |
| signal-version-handover | `eb80f588` | ARCHITECTURE: restructure per architecture-editor template |
| sema-engine | `8a740ac1` | ARCHITECTURE: CommitSequence section + handover constraints |
| sema-upgrade | `5dd65bc3` | ARCHITECTURE: name handover-stack role and add possible features section |
| persona-spirit | `f1e2223b` | ARCHITECTURE: explicit handover state machine (Active/HandoverMode/PrivateUpgradeOnly) |

All five commits pushed to `main` via standard `jj` flow per
`skills/jj.md`: `jj commit -m '<msg>' ARCHITECTURE.md && jj bookmark
set main -r @- && jj git push --bookmark main`. Each commit isolated
to its own repo; each push reported `Move forward bookmark main from
<old> to <new>` cleanly.

## §5 Anything that couldn't be cleanly distributed + recommended psyche follow-up

### §5.1 persona meta repo skipped

The task's #6 was conditional: "if `persona/ARCHITECTURE.md` doesn't
exist, skip this one (don't create the meta repo's ARCH from scratch
in this slice)." The file exists (1524 lines), so the conditional
fired the other way — I should have edited it. But `jj st` in the
persona repo showed six modified files already in flight from operator:

```text
M ARCHITECTURE.md
M TESTS.md
M flake.nix
M src/manager.rs
M src/upgrade.rs
M tests/manager.rs
```

The ARCHITECTURE.md modification was a single-line addition naming
"persona engine drives version handover through a component's private
upgrade socket" as an architectural-truth test row — consistent with
the meta architecture's existing engine-manager-as-upgrade-orchestrator
framing. Per `skills/jj.md` §"Before you commit — the working-copy
check": **don't bundle peer files into your commit**. The right move
was to leave the persona repo alone.

The existing persona ARCH already covers the engine manager's
upgrade-orchestration role at §"Engine Manager Model" and §"Startup
Strategy" and in the §9 architectural-truth tests (rows naming
"engine manager prepares a component upgrade by emitting the first
version-handover marker request" and "engine manager records the
active component version only after handover completion"). The
active-version-snapshot reducer described under §1.7 Startup Strategy
covers what /287 §5 names as the persona engine's "owns the
active-version selector" responsibility.

**Recommended psyche follow-up**: once operator's in-flight persona
work lands, a follow-up slice can verify the persona ARCH carries
explicit framing of the persona engine as the upgrade orchestrator
named in /287 §5 — particularly the active-version selector being
the persona engine's responsibility (replacing the prior
CriomOS-home symlink mechanism per spirit record 209). If the
existing coverage is sufficient, no edit is needed; if a §"Possible
features" section about cross-domain handover or owner-contract
authority would help, it can land then.

### §5.2 owner-signal-version-handover not yet existing

The task's §1 named `owner-signal-version-handover` as pending per
bead `primary-7kge`. The contract crate does not exist on disk
(checked: `/git/github.com/LiGoldragon/owner-signal-version-handover/`
absent). I named it under Possible features in both
`version-projection/ARCHITECTURE.md` and
`signal-version-handover/ARCHITECTURE.md` so a reader of either ARCH
sees the open question without the contract crate having to exist.
When the contract crate lands, its own ARCH inherits the typed
authority verbs (ForceFlip / Rollback / Quarantine) and the
Possible-features entries in both peers retire to one-line "see
sibling ARCH" pointers.

### §5.3 Mirror payload shape

Named identically as "Possible features" in three ARCH files
(`version-projection`, `signal-version-handover`, `sema-upgrade`)
because the resolution touches all three: today bytes + `RecordKind`,
alternative typed enum forcing `version-projection` to import every
signal-X crate. **Recommended psyche follow-up**: this answers itself
the second a second component (beyond persona-spirit) gets a real
cutover. Until then the three Possible-features entries stay
consistent; the entry retires from each ARCH the moment the decision
lands.

### §5.4 No /287 contradictions in the landed code

I cross-checked /287 against operator/158, /160, /161 and the actual
ARCH bodies. The current landed state matches /287 §5 precisely:
`version-projection` carries the trait + policy taxonomy (operator
commit `69bd2dd0`); `signal-version-handover` carries the six
operations and seven replies (commit `f2dfe3b4`); `sema-engine`'s
`CommitSequence` is the per-database high-water mark (commit
`e0a7153c`); `sema-upgrade`'s `src/handover.rs` is the protocol
witness; `persona-spirit` v0.1.1 owns the real upgrade socket
(commit `40c0c93e`). No code-vs-design drift; the distribution work
was pure inlining + framing + uncertainty-section discipline.

## See also

- `reports/designer/287-version-handover-component-explained.md` — the
  source of the distributed substance.
- `reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md`
  — the canonical spec /287 references; deeper detail.
- `reports/operator/158-version-handover-foundation-implementation-2026-05-22.md`
  — the foundation commits.
- `reports/operator/160-spirit-smart-handover-sandbox-test-2026-05-22.md`
  — end-to-end smart-handover sandbox witness.
- `reports/operator/161-spirit-private-handover-socket-2026-05-22.md`
  — persona-spirit's first production-owned upgrade socket.
- `skills/architecture-editor.md` — the discipline this distribution
  followed (no report refs; uncertainty sections; constraints as test
  seeds).
- `skills/jj.md` — the per-repo commit + push workflow used.
