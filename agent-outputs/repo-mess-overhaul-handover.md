# Repo Mess Overhaul Handover

Focus: fresh-context pickup for overhauling the repository/worktree sprawl under `/home/li/primary`.

## Psyche direction

- The psyche says Orchestrate is fixed now.
- The desired next focus is the repo mess itself: understand and overhaul the active repository/worktree situation rather than continue diagnosing Orchestrate as the primary problem.

## Evidence base

This handover is synthesized from the current chat, read-only Spirit query conclusions, and two scout returns. The orchestrator did not directly inspect repositories.

- Public Spirit grounding used: `n9fl`, `346n`, and `ty3g`, which support using specific agents for specific work, prioritizing quality, and treating agent failures as guidance/system-design signal rather than blame.
- Orchestrate scout: `24edade3-31a8-4ab`, output file `/tmp/pi-subagents-1001/home-li-primary/019f31f7-5ad2-70ad-97c9-69c88939e0d5/tasks/24edade3-31a8-4ab.output`.
- VCS scout: `40aafcf0-f2ae-463`, output file `/tmp/pi-subagents-1001/home-li-primary/019f31f7-5ad2-70ad-97c9-69c88939e0d5/tasks/40aafcf0-f2ae-463.output`.

## Settled observations

- Orchestrate was reported working at scout time: daemon active, sockets/state present, and read-only `Observe`/`Query` commands returned valid NOTA.
- At scout time Orchestrate showed sparse active coordination state: many role names, no active lanes, no registered worktrees, and one active path claim by `cloud-maintainer` on `/git/github.com/LiGoldragon/cloud`.
- The VCS scout found 219 repository roots under `/home/li/primary`, `private-repos`, `agent-worktrees`, and `worktrees`.
- `/home/li/primary` itself was dirty with one added `agent-outputs/...Evidence.md` file.
- `/home/li/primary` had 146 local Jujutsu heads at scout time.
- `repos/` existed but no repository markers were found under it in the scout's scoped search.
- Most active repositories appeared to be Jujutsu workspaces backed by Git.
- Several worktrees had dirty state:
  - `/home/li/primary/private-repos/social-media`: dirty private repo with local receiver/browser-agent artifacts and one modified setup doc; content was not dumped.
  - `/home/li/primary/worktrees/worker21-landing/landing-run/CriomOS-home`: dirty `flake.lock`.
  - `/home/li/primary/worktrees/worker9-landing/triad-runtime`: dirty source/docs/tests, including `ARCHITECTURE.md`, `ESSENCE.md`, `src/...`, and `tests/...`.
- `worker4-residue` contained stale Jujutsu working copies and many anonymous/local heads, including stale working copies named `meta-signal-criome`, `orchestrate`, `repository-ledger`, and `signal-cloud`.
- Many landing and integration worktrees existed and were mostly clean, but with varied `main` bookmarks and many heads not clearly landed.

## Current interpretation

- The main problem is not an Orchestrate outage; it is workspace coordination debt: too many repos, worktrees, heads, landing areas, and residue areas without a compact disposition ledger.
- `/home/li/primary` is not a safe casual base for new agents until the local heads and dirty files are understood.
- `worker4-residue` should be treated as archival/rescue material unless a fresh agent proves otherwise.
- Active implementation agents need exact repo paths and intended disposition; broad prompts like “fix the repo” are likely to worsen the mess.

## Open questions for the overhaul

- Which repositories and worktrees are active work, which are landed, which are abandoned, and which are archival evidence?
- Which local heads correspond to valuable unpushed work versus stale anonymous Jujutsu changes?
- Which landing/integration worktrees are authoritative for each repo family?
- Should the overhaul produce a durable repo/worktree disposition ledger, tracker beads, or both?
- What is the desired clean end shape: fewer worktrees, a named integration area, per-repo recovery branches, or a formal repository registry?

## Privacy boundary

- Private repo content remains closed by default. The scout reported only state-level metadata for `private-repos/social-media`; do not paste its contents into public reports or commits without explicit authorization.

## Suggested pickup shape

Start a fresh lane for repo/worktree overhaul. Use Orchestrate claims for exact paths before mutating anything. The first useful durable artifact is likely a concise disposition map of repo path → owner/purpose/state/next disposition, backed by read-only `jj`/Git evidence.