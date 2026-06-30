# Per-Repo INTENT.md Fold — Scaffold Handoff

## Task and scope

Phase 1 fan-out of a per-repo doctrine campaign: eliminate `INTENT.md` from each
named repo and move durable direction into `ARCHITECTURE.md`. Doctrine
(psyche-locked): there is no per-repo `INTENT.md`; a repo's durable direction
lives in its `ARCHITECTURE.md`, read on entry before code.

Repos processed (exactly these seven, independently): `signal`, `signal-agent`,
`signal-criome`, `signal-harness`, `signal-introspect`, `signal-message`,
`signal-mind`. Each at `/git/github.com/LiGoldragon/<name>`, own git+jj checkout,
own remote, public.

## Outcome summary

Six of seven repos completed (INTENT folded/dropped, committed, pushed to their
own `main`). One repo (`signal-criome`) skipped at the VCS pre-flight gate
because its working commit sat on a divergent sibling of `main`.

| Repo | Pre-flight | ARCHITECTURE | Pointers retargeted | INTENT deleted | Commit (main) | Push |
|---|---|---|---|---|---|---|
| signal | clean (`@` empty on main) | updated | 0 | yes | `4ff69f06` | main@origin=`4ff69f06` |
| signal-agent | clean | delete-only (redundant) | 2 (AGENTS.md, README.md) | yes | `1075cce4` | main@origin=`1075cce4` |
| signal-harness | clean | updated | 0 | yes | `52cd2ed9` | main@origin=`52cd2ed9` |
| signal-introspect | clean | updated | 0 | yes | `ad64de96` | main@origin=`ad64de96` |
| signal-message | clean | updated | 0 | yes | `e872ad66` | main@origin=`e872ad66` |
| signal-mind | clean | updated | 0 | yes | `2d31e96b` | main@origin=`2d31e96b` |
| signal-criome | DIVERGENT | not touched | not touched | no (intact) | unchanged `5976b287` | not pushed |

All six completed repos verified independently: `main == main@origin` and INTENT.md
absent on disk.

## VCS pre-flight gate — what the gate caught

The campaign warned that a proving run nearly lost committed work via a divergent
parent. The gate was applied to every repo before any edit:

- Six repos were clean: the `default@` working commit was empty and parented
  directly on `main`, and `main == main@origin`. Safe to commit on `@`.
- `signal-criome` was the trap. Its `default@` working commit (`6ee37595`) was NOT
  a descendant of `main` (`5976b287`, also bookmarked `criome-auth-integration`).
  `@` sat on top of the `criome-authorization-push` branch
  (`2986f8f8` -> `0e67ee68` -> ...), a sibling line of main. Committing the
  doctrine edit there would have created a sibling of main and a non-fast-forward
  push that could drop newer work — exactly the named failure.

`signal-mind` looked superficially suspect (a `technical-query-shapes*` bookmark
shares main's commit) but was clean: that bookmark belongs to a separate
workspace, `main` was not behind origin, and `@` was empty on main. Processed
normally.

## signal-criome — skipped, recommended recovery

Skipped per the gate: "If divergence cannot be cleanly resolved, SKIP that repo
and report it." Also per edit-coordination: the repo is visibly in active use
(multiple live jj workspaces: `default`, `criome-auth-integration`,
`criome-authorization-push`, `docs-emit-schema-rename`,
`signal-criome-auth-submit-stream`, `signal-criome-peers`; many in-flight feature
bookmarks). No edit was made; INTENT.md is intact; `main` is untouched.

Recommended recovery for a later pass (do NOT run blindly — the `default`
workspace `@` is positioned on `criome-authorization-push` deliberately by whoever
is doing that work):

- Because `@` is empty, a clean reparent is `jj -R <criome> new main` to get a
  fresh working commit on main, then fold + delete + commit + `bookmark set main
  -r @-` + push. But this moves the active `default` workspace off the auth-push
  line, so it should be coordinated with the auth-push worker, or done from a
  fresh `main`-based workspace dedicated to the doctrine edit.
- INTENT.md secrets check on signal-criome was performed during reconnaissance:
  its INTENT.md holds only wire-contract/architecture prose (BLS auth/attestation
  vocabulary, channel shape, non-ownership). No passwords, tokens, or key paths.
  Safe to fold when the VCS state allows.

## Fold decisions (what moved into each ARCHITECTURE)

Folds were 100% backed by what each repo already stated; no invented direction.

- signal: folded the NOTA text-boundary constraint (no shadow types; consumers do
  not re-derive text projection) and signal-frame / contract-repo cross-references.
  Most INTENT direction was already covered by ARCHITECTURE.
- signal-agent: ARCHITECTURE already fully covered the direction (the two Spirit
  decisions `iucr`/`f8k7`, no-concrete-provider constraint, the discarded
  agent-harness framing), so this was delete-only. The on-entry pointers in
  AGENTS.md ("then this repo's INTENT.md") and README.md ("INTENT.md for the
  psyche-stated scope") were retargeted to ARCHITECTURE.md before deletion.
- signal-harness: folded one durable point not already present; rest covered.
- signal-introspect: folded three points absent from ARCHITECTURE — the
  "ordinary peer-callable wire contract" role label, the Spirit authorization
  observation in component trace events (traced `spirit` daemon exposes the criome
  authorization-return point as structured introspection rather than a log line),
  and the request-payloads-mint-nothing boundary (added as a constraint/test-seed
  row). The "asks and wraps / not a shared schema bucket", closed-enum, three-layer,
  and non-ownership material was already present.
- signal-message: added an Overview-and-direction section and a Constraints
  section (schema/lib.schema source-of-truth + generated freshness-checked
  artifact, no `signal_channel!`, stateless boundaries / no durable ledger, NOTA
  no-shadow-types, two-sockets split). The three-layer model, provenance stamping,
  and channel shape were already present.
- signal-mind: folded the `signal-orchestrate` scope boundary (ordinary
  role/activity/handoff/activity-log orchestration is NOT this contract) plus
  non-ownership and See-Also direction; rest delete-only.

In each repo, INTENT meta scaffolding ("Repo-scope only", "Maintenance",
"See also -> INTENT.md") was dropped, not folded. `---` horizontal rules were not
introduced.

## Secrets

None. All seven INTENT.md files (the six folded and signal-criome inspected during
recon) carried only wire-vocabulary / architecture direction. No passwords,
tokens, credentials, or key file paths in any of them. Nothing redacted, nothing
propagated.

## Checks run

- Per-repo VCS pre-flight: `@` parent vs `main`, `main` vs `main@origin`,
  descendant check via `main..@` revset, workspace and bookmark inventory.
- Post-push verification per completed repo: `main == main@origin` at the new fold
  commit, INTENT.md absent on disk, no remaining `INTENT` references in any `*.md`.
- Workspace dangling-reference sweep: no primary-workspace guidance surface
  (`AGENTS.md`, `skills/`, `.claude/skills/`) referenced any of these repos'
  `INTENT.md` files, so the deletions leave no dangling on-entry pointer at the
  workspace level.
- No language build/test was run: these are markdown-only documentation
  reorganizations of already-committed content; the meaningful checks are the VCS
  gate and the dangling-pointer sweep, both run.

## Blockers, unknowns, follow-up

- FOLLOW-UP (signal-criome): complete the fold once its VCS state is clean or a
  dedicated main-based workspace is used; coordinate with the active auth-push
  worker. No direction lost.
- OBSERVATION (stale generated surface): the live skill-list system-reminder for
  `repo-intent` still carries the OLD one-liner asserting a per-repo `INTENT.md` is
  "the first and most important file per repo." The authoritative
  `repo-intent` SKILL.md body already reflects the new doctrine (no per-repo
  INTENT.md; direction lives in ARCHITECTURE.md). This is a generated-surface
  drift to reconcile in the skills source (LiGoldragon/skills) so the runtime
  one-liner matches the campaign doctrine. Recorded as a recommendation, not new
  authority.
- OBSERVATION (concurrency): some fork workers narrated that signal-agent/harness/
  message were completed by a "concurrent campaign run." Ground-truth inspection
  shows each repo carries exactly one clean fold/drop commit at `main == main@origin`
  with the campaign commit style; no divergence, no double-commit, no collision on
  any repo. Whether one or two campaign runs produced them, the end state is
  correct and singular per repo.
- Three fork workers (signal, signal-agent, signal-mind) reported an API
  rate-limit error as their final "rest" event. Ground truth confirms all three
  had already committed and pushed before that idle ping; the rate limit did not
  truncate any repo's work. signal-introspect's fork made no edit (it never got
  past waiting); that repo was completed directly by the lead.

## Claims

`repo-scaffolder` Orchestrate lane claimed the six clean repos before editing and
released all claims after completion (lane now shows `[]`). `signal-criome` was
never claimed (skipped before edit).
