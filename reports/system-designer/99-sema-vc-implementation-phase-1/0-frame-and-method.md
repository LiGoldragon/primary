# 99 — Sema version control, implementation phase 1: frame and method

The psyche confirmed the report-98 vision and said go: fix the three
hand-parsing sites in schema-next's macro library (everything on structural
macro nodes; NOTA expressiveness gaps surfaced, not worked around — Spirit
`v0n6`), build the mirror as a dedicated triad with three new repos
authorized (`0yx5`), tailnet TCP transport (`rj9y`), spirit's next schema
bump as the logged-fold migration pilot (`t0tu`), Stage 0 (mind before
spirit) accepted. Repository-ledger pre-work was declined ("don't worry
about repository ledgers").

## Method

One background workflow (`sema-vc-implementation-phase-1`, run
`wf_8724d72d-bd4`, 8 agents, ~1.5M tokens): four parallel implementation
agents on worktree feature branches, each followed by an adversarial
reviewer that re-ran every test suite itself. All four branches were
**approved**; the single must-fix (mind branch based one commit behind
origin/main) was applied by the orchestrator (rebased onto `b9cd8c23`,
pushed as `313b7c87`; the reviewer had already scratch-verified that exact
rebase conflict-free and 65/65 green).

| Chapter | Branches (all pushed) | Verdict |
|---|---|---|
| `1-typed-macro-library.md` | nota-next `structural-shape-extension` (`e92a9295`), schema-next `typed-macro-library` (`d7b34a24`) | approve, 0 must-fix |
| `2-schema-content-identity.md` | schema-next `schema-content-identity` (`3e72902d` after doc hardening) | approve, 0 must-fix |
| `3-tailnet-listener.md` | triad-runtime `tailnet-listener` (`1b5d0f17`) | approve, 0 must-fix |
| `4-family-identity-stage-0.md` | sema-engine `versioned-family-identity` (`53426b14`), mind `memory-graph-family` (`313b7c87`) | approve, 1 must-fix (closed) |

The synthesis — what landed, the NOTA-gap answer for the psyche, residue,
and integration order — is `5-status-and-integration.md`.
