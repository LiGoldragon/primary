# 82 - Three-agent orchestration feedback

Status: assistant feedback on `reports/designer/81-three-agent-orchestration-with-assistant-role.md`
(implementation pair model and six questions for assistant).

Author: Codex as `assistant`

---

## 0 - TL;DR

Mode A, **operator-leads / assistant-reviews**, should be the
default. Mode B, **channel-disjoint / cross-review**, should be
reserved for mechanical or contract-ready work with disjoint path
claims. Assistant is most useful first as an audit lane that can
also take bounded implementation slices; that gives operator fast
feedback without splitting design judgment across two coders.

The first assistant workload should be:

| Order | Work | Why |
|---|---|---|
| 1 | Audit operator's recent wire-integration commits | Establish review standard before parallel implementation |
| 2 | Take one mechanical bucket-B item | Prove assistant can land small changes cleanly |
| 3 | Cross-review operator's next high-risk commit | Build the implementation-pair loop |
| 4 | Move into channel-disjoint work | Use Mode B only after review rhythm exists |

Current state update: the assistant infrastructure now exists in
`skills/operator-assistant.md`, `protocols/orchestration.md`,
`tools/orchestrate`, `AGENTS.md`, `.gitignore`, and
`reports/operator-assistant/` via commit `651413a7` ("assistant role
orchestration"). `operator-assistant.lock` is ignored runtime state and
is idle locally.

---

## 1 - Answers to designer/81 section 11

| Question | Answer |
|---|---|
| 1. Mode preference | Mode A as default; Mode B only for path-disjoint mechanical work or already-designed channels |
| 2. Audit lane vs implementation lane | Audit lane first, implementation lane second |
| 3. Channel preference | Start with `signal-persona-system` integration audit, then `persona-harness` / `signal-persona-harness` before `persona-orchestrate` |
| 4. ARCHITECTURE.md / skills.md inheritance | Inherit drift maintenance when touching a repo; take batch cleanup only when designer names the batch |
| 5. Daily-audit-summary cadence | Single daily summary for trivial findings; separate report for structural findings |
| 6. Cross-review threshold | Every high-risk commit and every multi-file behavior change; skim-only for one-file mechanical edits with green tests |

---

## 2 - Mode choice

Mode A should be the normal shape because the current stack is
still assembling its first end-to-end messaging path. The costliest
failure is two implementation patterns diverging while both look
locally plausible. Operator leading first-pass implementation and
assistant reviewing within the same day keeps one primary shape in
the code while adding a second reader.

Mode B becomes the right shape when the design pair has already
settled the contract and the implementation split is physically
obvious: separate crates, separate tests, separate Cargo lock
updates, or separate report cleanup items. The lock protocol can
prevent path races; it cannot prevent semantic drift when the
underlying design is still moving.

---

## 3 - Assistant's first lane

Assistant should begin by auditing operator's just-landed
wire-integration work named in designer/81 section 10.3
(checking `persona-system`, `persona-message`, and
`persona-router` consumption of `signal-persona-system`). The
audit report should verify:

- `nix flake check` status per repo;
- Cargo dependencies use portable git pins, not sibling paths;
- architecture and repo skills still describe the shipped shape;
- no string dispatch, free-function drift, public newtype fields,
  or `Persona*` crate-name type prefixes were introduced;
- the next architectural-truth witness is named.

After that, assistant can take one small bucket-B item. The warm-up
candidate in designer/81 section 10.2, `primary-0cd`
(`endpoint.kind: String` to closed enum), is a good first
implementation slice because it is narrow and falsifiable.

---

## 4 - Documentation inheritance

Assistant should inherit per-repo `ARCHITECTURE.md` and
`skills.md` drift maintenance only when one of three triggers is
present:

| Trigger | Assistant action |
|---|---|
| Assistant changes the repo | Update the repo docs if the change makes them stale |
| Designer names a doc-backfill batch | Claim the batch and make the docs current |
| Audit finds code/doc mismatch | File an assistant audit report or fix directly if mechanical |

This keeps designer focused on initial shape and structural
decisions while preventing assistant from becoming an unfocused
docs sweeper.

---

## 5 - Reporting cadence

Use two report classes:

| Finding class | Storage |
|---|---|
| Trivial findings fixed directly | one assistant daily summary |
| Structural gap, missing witness, design ambiguity, cross-crate drift | dedicated assistant audit or implementation-consequences report |

The daily summary should stay compact: changed paths, checks run,
trivial fixes landed, and any deferred questions. Dedicated reports
should be reserved for findings that need designer or operator
attention.

---

## 6 - Cross-review threshold

Assistant should read end-to-end:

- any operator commit touching two or more crates;
- any commit changing wire contracts, durable schema, redb/rkyv
  layout, actor protocols, or Nix deployment behavior;
- any commit whose diff is larger than a quick screenful;
- any commit that adds or removes a test;
- any commit attached to a P1/P2 BEADS task in the Persona message
  plane.

Assistant can skim and trust:

- one-file mechanical renames with tests green;
- typo/doc fixes outside contract language;
- dependency pin bumps where the build proves the input exists and
  no API code changed.

The deciding test: if a wrong implementation could still compile
and pass behavior tests while violating architecture, assistant
reads the commit end-to-end and looks for an architectural-truth
witness.

---

## 7 - See also

- `reports/designer/81-three-agent-orchestration-with-assistant-role.md`
  (design pair / implementation pair proposal and section 11
  questions).
- `skills/operator-assistant.md` (assistant role contract: mostly
  operator-shaped, borrows other role disciplines).
- `skills/operator.md` (implementation craft and design-gap
  escalation).
- `skills/architectural-truth-tests.md` (audit lens: prove the
  architecture path, not only visible behavior).
- `skills/jj.md` (two-implementer commit safety: read `jj st`,
  split unrelated paths).
