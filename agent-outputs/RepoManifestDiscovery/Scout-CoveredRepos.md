# Scout — Covered Repos Verification

## Task and scope

Read-only verification of the 62 repos covered by the per-repo doctrine campaign
(fold `INTENT.md` into `ARCHITECTURE.md`). Source list: the symlink targets of
`/home/li/primary/repos/` that point into `/git/github.com/LiGoldragon/` (62
entries). The 2 private-repos symlinks (`../private-repos/assistant-reports`,
`../private-repos/counselor-reports`) are excluded; they are not LiGoldragon
repos.

For each covered repo, this file records:
- Whether the fold held: `ARCHITECTURE.md` present AND `INTENT.md` absent.
- Last local commit date (`jj log -r '@-'`) and remote liveness (`gh repo view`).
- Anomaly flags: defects and dormancy candidates.

## Commands consulted

- `ls -la /home/li/primary/repos/` — symlink inventory
- Presence test loop (`-f ARCHITECTURE.md`, `-f INTENT.md`) over all 62 repos
- `jj log -r '@-'` for last commit date + subject — all 62 repos
- `gh repo view LiGoldragon/<repo> --json isArchived,isFork,pushedAt` — all 62 repos
- `ls` and `head` on top-level files for the 6 repos missing `ARCHITECTURE.md`
- `jj log` full history spot-check for repos without a fold-commit message

## Per-repo table (all 62 covered repos)

Legend: ARCH = `ARCHITECTURE.md` present; INTENT = `INTENT.md` present (YES is a defect);
Remote = archived/fork/live from GitHub API; Last commit from local `jj log -r '@-'`.

| Repo | ARCH | INTENT | Last commit | Remote |
|---|---|---|---|---|
| arca | yes | no | 2026-06-30 | live |
| chroma | yes | no | 2026-06-30 | live |
| chronos | yes | no | 2026-06-30 | live |
| criome | yes | no | 2026-06-30 | live |
| CriomOS | yes | no | 2026-06-30 | live |
| CriomOS-emacs | yes | no | 2026-06-08 | live |
| CriomOS-home | yes | no | 2026-06-30 | live |
| CriomOS-lib | yes | no | 2026-05-29 | live |
| **CriomOS-pkgs** | **no** | no | 2026-05-28 | live |
| forge | yes | no | 2026-06-30 | live |
| **goldragon** | **no** | no | 2026-06-20 | live |
| harness | yes | no | 2026-06-30 | live |
| hexis | yes | no | 2026-06-19 | live |
| horizon-rs | yes | no | 2026-06-30 | live |
| introspect | yes | no | 2026-06-30 | live |
| kameo-testing | yes | no | 2026-06-19 | live |
| **library** | **no** | no | 2026-06-13 | live |
| lore | yes | no | 2026-06-30 | live |
| mentci-egui | yes | no | 2026-06-30 | live |
| mentci-lib | yes | no | 2026-06-30 | live |
| message | yes | no | 2026-06-30 | live |
| meta-signal-criome | yes | no | 2026-06-30 | live |
| meta-signal-harness | yes | no | 2026-06-30 | live |
| meta-signal-introspect | yes | no | 2026-06-30 | live |
| meta-signal-message | yes | no | 2026-06-30 | live |
| meta-signal-system | yes | no | 2026-06-30 | live |
| meta-signal-upgrade | yes | no | 2026-06-30 | live |
| mind | yes | no | 2026-06-30 | live |
| nexus | yes | no | 2026-06-30 | live |
| nexus-cli | yes | no | 2026-06-30 | live |
| nota-next | yes | no | 2026-06-30 | live |
| orchestrate | yes | no | 2026-06-30 | live |
| persona | yes | no | 2026-06-30 | live |
| router | yes | no | 2026-06-30 | live |
| schema-next | yes | no | 2026-06-30 | live |
| schema-rust-next | yes | no | 2026-06-30 | live |
| sema | yes | no | 2026-06-30 | live |
| sema-engine | yes | no | 2026-06-30 | live |
| signal | yes | no | 2026-06-30 | live |
| signal-agent | yes | no | 2026-06-30 | live |
| signal-criome | yes | no | 2026-06-30 | live |
| signal-derive | yes | no | 2026-06-19 | live |
| signal-forge | yes | no | 2026-06-17 | live |
| signal-harness | yes | no | 2026-06-30 | live |
| signal-introspect | yes | no | 2026-06-30 | live |
| signal-message | yes | no | 2026-06-30 | live |
| signal-mind | yes | no | 2026-06-30 | live |
| signal-orchestrate | yes | no | 2026-06-30 | live |
| signal-persona | yes | no | 2026-06-30 | live |
| signal-router | yes | no | 2026-06-30 | live |
| signal-system | yes | no | 2026-06-30 | live |
| signal-terminal | yes | no | 2026-06-30 | live |
| signal-upgrade | yes | no | 2026-06-30 | live |
| spirit | yes | no | 2026-06-30 | live |
| **substack-cli** | **no** | no | 2026-06-19 | live |
| system | yes | no | 2026-06-30 | live |
| terminal | yes | no | 2026-06-30 | live |
| terminal-cell | yes | no | 2026-06-30 | live |
| TheBookOfSol | yes | no | 2026-06-30 | live |
| **tree-sitter-nota** | **no** | no | 2026-06-13 | live |
| **tree-sitter-schema** | **no** | no | 2026-06-13 | live |
| upgrade | yes | no | 2026-06-30 | live |

## Summary counts (observed)

| Metric | Count |
|---|---|
| Covered repos verified | 62 |
| INTENT.md absent (fold held) | **62 / 62** |
| ARCHITECTURE.md present (doctrine surface exists) | **56 / 62** |
| ARCHITECTURE.md missing (doctrine gap) | **6** |
| Remote archived | 0 |
| Remote fork | 0 |
| Remote live | 62 |

## Flag A — Residual INTENT.md or missing ARCHITECTURE.md defects

**INTENT.md residuals: none.** Every one of the 62 covered repos has INTENT.md
absent. The fold held completely on the elimination axis.

**ARCHITECTURE.md missing — 6 repos:**

| Repo | Direction surface found | Last commit | Notes |
|---|---|---|---|
| CriomOS-pkgs | `AGENTS.md` (direction prose inline) | 2026-05-28 | No fold commit in history; never had INTENT.md |
| goldragon | `README.md` (cluster proposal prose) | 2026-06-20 | No fold commit; never had INTENT.md |
| library | `CLAUDE.md` (one-liner scope description) | 2026-06-13 | No fold commit; never had INTENT.md |
| substack-cli | `AGENTS.md` + `README.md` | 2026-06-19 | No fold commit; never had INTENT.md |
| tree-sitter-nota | `README.md` only | 2026-06-13 | Very new (2 commits total); no INTENT.md |
| tree-sitter-schema | `README.md` only | 2026-06-13 | Very new (2 commits total); no INTENT.md |

Interpretation (not fact): these 6 repos were never given an ARCHITECTURE.md at
any point — their direction lives in CLAUDE.md, AGENTS.md, or README.md. The
campaign skipped them without error on the INTENT.md axis (nothing to fold), but
they are now identifiable as missing the canonical direction surface that doctrine
wants. This is a separate, pre-existing gap from the campaign itself; the
campaign did not regress them.

None of these 6 repos had an INTENT.md at any point in their jj history (no
fold-commit message appears). All 6 are active (not dormant): `goldragon` and
`substack-cli` had functional commits in June 2026; `tree-sitter-nota` and
`tree-sitter-schema` are newly created repos (2 commits each, both dated
2026-06-13).

## Flag B — Covered-but-apparently-dead repos (deprecation candidates)

**None found.** All 62 covered repos:

- Are live (not archived, not forks) on GitHub.
- Had at least one commit between 2026-05-28 and 2026-06-30.
- The oldest last-commit among the 62 is `CriomOS-pkgs` at 2026-05-28 (~33 days
  before today's date 2026-07-01). No repo is dormant by any reasonable threshold.
- No repo is a fork, so none is a vendor copy that could be retired.

Repos with commits older than 2026-06-15 (less campaign-recent, for awareness):
`CriomOS-pkgs` (2026-05-28), `CriomOS-lib` (2026-05-29), `CriomOS-emacs`
(2026-06-08), `library` (2026-06-13), `tree-sitter-nota` (2026-06-13),
`tree-sitter-schema` (2026-06-13). All of these are active in function; the
older dates reflect normal maintenance cadence, not abandonment.

## Unknowns not checked

- Whether ARCHITECTURE.md content in the 56 covered repos is substantively
  complete (direction-quality prose) vs. a minimal stub. Only presence was
  checked; content quality was spot-checked on 5 repos (arca, chroma, lore,
  persona, spirit) and appeared substantive.
- Whether any covered repo has a dependency on a not-yet-covered repo (the 54
  missed set) that could affect fold order for the follow-on campaign run.
- Spirit intent records: not queried; not load-bearing for the file-presence
  and activity facts this brief requested.
