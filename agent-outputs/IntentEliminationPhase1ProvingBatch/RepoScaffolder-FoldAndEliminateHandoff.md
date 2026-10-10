# Phase 1 Proving Batch — INTENT.md fold-and-eliminate handoff

## Task and scope

Phase 1 proving batch of a per-repo doctrine campaign: eliminate per-repo
`INTENT.md`; move durable direction into `ARCHITECTURE.md` (or author one where
absent). Six repos, each its own git+jj checkout under
`/git/github.com/LiGoldragon/<name>` (symlinked from `/home/li/primary/repos/`):

meta-signal-criome, meta-signal-harness, meta-signal-introspect,
meta-signal-message, meta-signal-system, meta-signal-upgrade.

Doctrine (psyche-locked): no per-repo `INTENT.md`; durable direction lives in
`ARCHITECTURE.md`, read on entry before code; direction is agent prose 100%
backed by what INTENT.md and the repo already state.

## Per-repo outcome

All six succeeded, committed and pushed via their own jj store. `main@origin`
in sync with local `main` on every repo; working copies clean; no INTENT.md
remains; ARCHITECTURE.md present everywhere.

| Repo | ARCHITECTURE | INTENT.md | Commit | Push |
|------|--------------|-----------|--------|------|
| meta-signal-criome | updated (added Direction: pair role + meta-socket MVP authority boundary) | deleted | 3c51eac3 | pushed |
| meta-signal-harness | updated (added Direction: Persona-manager authority surface, lifecycle ops extend channel) | deleted | 667fa3f2 | pushed |
| meta-signal-introspect | updated (added Direction: peer fan-out set + introspect.sema config, UnknownPeerComponent) | deleted | 8bcf6044 | pushed |
| meta-signal-message | authored from scratch (had none) | deleted | 2549d25b | pushed |
| meta-signal-system | updated (added Direction: backend selection, ComponentPaused, force-focus/drift-suppression future ops) | deleted | 3b00673e | pushed |
| meta-signal-upgrade | unchanged — already carried full direction | deleted | 91e78ad9 | pushed |

### Fold scope per repo

- criome: ARCHITECTURE already covered the channel; folded the only missing
  INTENT nuance — the meta socket is the MVP authority boundary for
  intercept-policy mutation and parked-request answers — into a new Direction
  section. Plus the two-contract-pair framing.
- harness, system: added Direction sections for the two-contract-pair "why",
  and the system-specific ComponentPaused reason + future privileged OS ops
  (force-focus, focus-drift suppression). Channel/invariants already present.
- introspect: added Direction (peer-daemon fan-out set + introspect.sema as
  config; peer registration lives in the Configure payload, not bespoke ops)
  and surfaced the UnknownPeerComponent rejection reason in the Surface block.
- message: authored a full ARCHITECTURE.md modeled on the criome schema-derived
  layout (both are schema/lib.schema + build.rs + src/schema + canonical.nota).
  Grounded in INTENT.md + schema/lib.schema + Cargo.toml + tests. Direction:
  ingress socket mode + engine-owner origin policy for the stamp-and-forward
  boundary; registration inside the Configure payload.
- upgrade: INTENT.md was fully redundant with an already-thorough
  ARCHITECTURE.md (seven verbs, authority-not-state split, schema-derived stack,
  AttemptHandover exclusion, owner-signal-sema-upgrade archive, binary-default).
  Delete-only; no direction lost.

No invention: every folded statement traces to the repo's INTENT.md, schema,
Cargo.toml, or existing ARCHITECTURE.md.

## Secret flags

None. All six INTENT.md files were wire-contract direction prose with zero
secret-adjacent content (no passwords, tokens, or key paths).

## Checks run

- Pre-edit: confirmed no target repo claimed by another role (Observe Roles);
  claimed all 6 paths under repo-scaffolder; released after.
- Scaffold check used: in-repo reference integrity. Grepped every repo for
  `INTENT.md` references in md/rs/toml/nix/schema and retargeted all dangling
  on-entry pointers to ARCHITECTURE.md (see hazard below) before deleting.
  Post-edit re-scan: zero remaining in-repo self references.
- jj per repo: status clean before/after; diff --stat matched intended changes;
  bookmark set main -r @-; git push --bookmark main returned fast-forward
  ("Move forward bookmark main"); final bookmark list shows main@origin in sync
  with no ahead/behind divergence on any repo.

Note: did not run cargo/flake builds. These are doc-only changes
(ARCHITECTURE.md / README.md / AGENTS.md / skills.md / INTENT.md deletion); no
.rs, schema, Cargo, or flake source was touched, so compilation surface is
unchanged. If a build gate is desired before fanning out, run each repo's
`nix flake check` as the next step.

## Friction and hazards for the ~46-repo fan-out

1. DANGLING ON-ENTRY POINTERS (systemic, must be handled). Deleting INTENT.md
   is not self-contained: AGENTS.md, skills.md, and README.md routinely list
   `INTENT.md` as required on-entry reading (often as the FIRST item, sometimes
   in a numbered list). 5 of 6 repos here had at least one such pointer; 9
   dangling references total. A naive delete-and-fold leaves guidance telling
   future agents to read a missing file. The fan-out MUST grep each repo for
   `INTENT.md` across md/rs/toml/nix/schema and retarget every in-repo self
   reference to ARCHITECTURE.md (dropping the line when ARCHITECTURE is already
   listed, replacing it when INTENT was the sole/first entry, renumbering
   ordered lists). Cross-repo `../<other>/INTENT.md` "See also" links are out of
   scope for the repo being processed but WILL break as their target repos are
   later processed — the campaign should expect a second sweep, or process in
   dependency order, or accept that sibling INTENT links die. Recommend a final
   workspace-wide grep for `INTENT.md` after the whole campaign.

2. STALE / DIVERGENT WORKING COPY (per-repo, not caught by "reported clean").
   meta-signal-message was reported clean but its jj working copy `@` was an
   empty commit parented on an OLD revision (45eb00a1), diverging from
   main/origin (7b0248ee, the "update nota dependency names" commit on an
   unmerged-into-@ bookmark). Committing as-is would have created a SIBLING of
   main, not a child — a non-fast-forward push that drops the newer main work.
   Fix applied: `jj rebase -s @ -d main` reparented the edits onto main; push
   was then a clean fast-forward. LESSON FOR FAN-OUT: "clean working copy" is
   not sufficient. Before editing each repo, verify `@`'s parent is actually
   `main` (jj log -r 'main | @'); if `@` is parented off-main or a feature
   bookmark, rebase onto main first. A blind fan-out that commits on a stale `@`
   will silently lose committed work on a subset of repos. This is the single
   most dangerous failure mode and warrants an automated pre-flight gate.

3. REDUNDANT-INTENT REPOS. Some repos (upgrade here) have an ARCHITECTURE.md
   that already fully absorbs the INTENT.md — these are delete-only. Worth a
   cheap diff/coverage check so the fold step does not duplicate content already
   present (which would violate the architecture-editor no-duplication rule).

4. MISSING ARCHITECTURE.md (author-from-scratch). One repo (message) had no
   ARCHITECTURE.md and required authoring one. This is more work and more
   judgment than a fold; the fan-out should expect a meaningful fraction needing
   authoring, and these benefit from a structural sibling to model on (criome
   was the template for message because both are schema-derived contracts).

5. COMMIT GRANULARITY / VOLUME. 46 repos = 46 independent commits+pushes across
   46 jj stores. Each push is a separate network round-trip and a separate
   chance for a remote-advanced rejection (jj skill: stop and ask, do not
   force). The pattern is mechanically safe per-repo but should be batched with
   per-repo failure isolation (one repo's push rejection must not abort the
   others) — which is how this batch was structured.

## Blockers / unknowns / follow-up

- No blockers; all 6 landed.
- Follow-up: build-level verification (`nix flake check` per repo) was not run;
  recommend running it on the proving batch if the campaign wants a green-build
  gate before fan-out, though no compilation surface changed.
- Follow-up: after the full ~46-repo campaign, run one workspace-wide
  `grep -rIn 'INTENT.md'` to catch cross-repo sibling references that died as
  their targets were processed.
- Recommendation: build a pre-flight gate into the fan-out that (a) confirms
  `@`'s parent is `main` before editing (rebase if not), and (b) greps for and
  retargets dangling INTENT.md pointers as a mandatory step, not an optional one.
