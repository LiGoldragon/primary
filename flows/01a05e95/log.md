# Flow identity realization

Realized one parent-owned flow lane with focused child contexts. The parent supplies one shared `FLOW_ID` and `FLOW_DIRECTORY`; each child obtains its own thread identity after launch, performs its work, creates no lane/index/log, and returns its final response. Optional reports and witnesses use the parent lane through `flow-evidence`.

Settled:

- Replaced the overloaded `flows`/`subflows` skills with user-only `main-flow`, model-loadable `child-flow`, and on-demand `flow-evidence`; updated vocabulary, dependencies, generated visibility metadata, deployment documentation, and tests.
- Corrected the initially impossible pre-spawn `THREAD_ID` requirement: only shared flow identity/directory enter the brief; a child obtains its transcript identity after launch.
- Curriculum, curriculum-deploy v0.2.2, and regenerated primary projections are committed and pushed; remote, isolated, and live Nix checks pass.
- A fresh direct child and nested fresh Codex child propagated the parent identity unchanged, acquired distinct thread identities, and created no child artifacts or index rows.
- Transcript-grounded migration consolidated all 24 proven child/extended lanes into their root lanes, preserved 46 durable artifacts byte-for-byte, compacted rather than concatenated logs, normalized the index, and retained all nine legitimate mixed-prefix root directories.
- Live conflicts were resolved without discarding current flow state; all retired lanes are physically absent and no Jujutsu conflicts remain.
- Added the harness-owned `flow-id` helper: Codex claims the normalized hexadecimal `CODEX_SESSION_ID[23:29]` alias, extends collisions, publishes complete private identity markers atomically under a stable filesystem lock, and resumes idempotently; Claude accepts an explicit parent UUID.
- The corrected deterministic publication-race test, 11 helper integrations, full Harness remote checks, focused Home checks, immutable CriomOS activation evaluation/build, and exact closure witness pass; the closure executable returns `715d46`.
- Harness, Home, Curriculum, curriculum-deploy, primary, and the CriomOS consumer pins are committed and pushed. All work locks were released; unrelated locks were untouched.

Open:

- Native automatic child-brief injection is not present in an owned checkout; the witnessed runtime contract is explicit parent-brief propagation.
- Live Home activation was not attempted: Lojix lacks an explicit deployment projection/proposal/transport/selector, and the full Home gate has the pre-existing `home-ol5` orchestrate-wrapper failure even though the immutable activation closure is green.
- The loaded Orchestrate skill's braced release syntax disagrees with deployed Orchestrate 0.26's bare release product; a skill-variable correction awaits living approval.

# Flow identity realization

Investigate why Codex subflows create separate flow directories, recover the prior flow-identity design, determine how every subflow write can use its parent flow ID, and map the affected directories and references before any repair.

- The earlier design and its intended replacement for “protocol.”
- The producing mechanism and exact prompting/context path.
- Which directories are subflow-created rather than independent flows.
- A collision-safe content merge and reference rewrite plan, including checks outside the expected affected files.
- The anatomy and boundary decisions the living must rule before realization.

Codex subflows are being prompted to turn their thread identity into an independent flow directory even though Codex supplies the shared root lineage separately. The intended architecture is one parent flow lane, with subflows performing their work and returning one final response; only the parent owns a rare, high-level rewritten log.

- Codex exposes root lineage as `CODEX_SESSION_ID` and child transcript identity as `CODEX_THREAD_ID`; the active flow skill incorrectly tells each model session/subflow to use its own flow directory and log.
- Prior Vision already says subflows do not create their own lanes; they use the parent's.
- The parent alone should maintain the flow summary. Subflows leave requested edits and return their final response; transcripts preserve detail.
- Root-loaded skills are not inherited by Codex children. A child receives its own context plus the parent's brief, so the canonical flow ID and a small child role contract must be explicitly injected or passed.
- The current `subflows` skill is parent-facing orchestration and should become a user-only main-flow role. Child behavior needs a separate, minimal child-flow role; optional reports/witnesses need an on-demand evidence contract rather than routine logging.
- The configured authored Curriculum skills and active generated trees match; the defect is authored behavior, not generation drift.
- The current inventory found 23 child-only candidate directories, 9 mixed-prefix collisions, nested ancestry, missing parent directories, and references outside candidate directories. Migration therefore requires a transcript-grounded manifest and collision checks, not blind replacement.

- Final names and exact role boundaries for main-flow, child-flow, and optional flow evidence/artifacts.
- Harness injection versus explicit parent-brief loading, including Claude/Pi and nested-child behavior.
- Exact identity helper boundary, collision claim, cold resume, concurrent artifact ownership, and provenance.
- Historical child-log disposition and provenance representation for moved artifacts.
- Approval to realize, test through fresh subflows, regenerate generated skill trees, and migrate the historical corpus.

- Native automatic child-brief injection is not present in an owned checkout; the witnessed runtime contract is explicit parent-brief propagation.
- The later six-character collision-extending flow-ID helper and cold-resume behavior remain a separate realization.
