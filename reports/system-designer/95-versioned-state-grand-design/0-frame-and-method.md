# 95 — The versioned-state grand design: frame and method

The psyche escalated the reusable version-control arc (reports 92/93/94,
operator mainline `c970d3f2`, audit 211) into its full ambition: this is
"going to become the basis and one of the most important parts of this
entire meta-work." The ask, in the psyche's words:

- **Show the design with visuals** — "what the design looks like," "how
  everything is theoretically going to work," and **what parts are clever**.
- **Latest and greatest** — make sure the design uses the best ideas in
  version control for efficiency and cleverness.
- **Full distributed-version-control semantics over the database** —
  **branching / forking** in the database, **rebasing**, merging. Per the
  psyche: "we can start having different branches in the database … and
  then rebasing." With **per-component policy** — "it's going to be
  different in every context"; Spirit's **guardian** must admit certain
  entries, so "a rebase in that case would have to go through the
  guardian." A default implementation, customizable per component.
- **Consistent crypto** — "keep using the same hashing mechanism, the same
  crypto." blake3 for content addressing, criome BLS for signing.
- **Used by all major components** — "they're going to have backups, which
  is basically the same thing as the version-control system."
- **Design at the post-agent frontier** — "we aren't constrained by the
  same thing that people were constrained even a year ago," because agents
  now do "very complex database upgrades with zero runtime, zero downtime."
  "What was thought to be impractical even just a year ago is now possible …
  shoot for the absolute best design … extremely elegant and modular and
  reusable and beautiful."

## Spirit gate

Outcome: **Record** (three durable, explicitly-stated psyche intents):

- **`i4ak`** (Decision) — the reusable component VC system is foundational
  and must support full DVCS semantics (branch / fork / rebase / merge) over
  the typed database, with per-component customizable intake / merge /
  rebase policy (default + override; Spirit's guardian mediates rebase by
  admitting / rejecting / transforming each incoming entry). Extends
  `29pb` / `j487`.
- **`x0ja`** (Constraint) — one consistent cryptographic basis across the
  whole VC + backup system: blake3 for all content addressing, criome BLS
  for signing and attesting history; no per-component divergence.
- **`jys2`** (Principle) — design at the post-agent capability frontier;
  target the best end-shape, not a historically-practical compromise.

The mechanism remains design (this report); only the psyche's intents above
are recorded.

## Method

A background research Workflow (`versioned-state-frontier-research`, run
`wf_eb9488d2-07d`) extends report 92's general survey into the **new
dimensions** — six web-verified agents → synthesis → adversarial critic →
revise:

| Agent | Question |
|---|---|
| `branch-merge-rebase-on-logs` | How branch/fork/merge/rebase map onto an append-only typed event log (where the log already carries each diff), with a per-entry intake policy. |
| `conflict-free-and-policy-merge` | Patch theory + CRDTs (eg-walker, Loro, diamond-types, Automerge) → per-family conflict-free vs policy-mediated merge. |
| `verifiable-and-signed-history` | Transparency logs, Merkle inclusion/consistency proofs, and BLS-signed (aggregate/quorum) heads → a verifiable, attestable log. |
| `zero-downtime-migration` | Online schema evolution + the agent-era "migration as a validated branch, fast-forwarded with zero downtime." |
| `efficient-content-structures` | Honest re-examination of prolly trees / MST now that branching is in scope — log (no tree needed) vs full-state checkpoint (where a Merkle state helps). |
| `frontier-and-clever-combination` | The newest 2024-2026 ideas and the clever combination for our exact shape. |

The deliverable is the **visual design synthesis** (the highest-numbered
file in this directory): a heavily-diagrammed design showing the layered
architecture, the commit-DAG / branch model, the write / replay / sync /
rebase-through-guardian / merge / migration-as-branch flows, the consistent
blake3 + BLS crypto layering, a "what's clever" section, and positioning
against the state of the art. The research chapters are numbered beneath it.
A companion prototype extension (branch / fork / merge / rebase + a guardian
intake-policy hook) follows on the `sema-engine` concept branch.

## Builds on

Reports 92 (constraint map), 93 (the spike), 94 (per-family identity /
checkpoint / remote append next-slice design), the operator's mainline
versioned commit log (`versioning.rs`), and system-operator audit 211.
