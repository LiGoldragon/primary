# Builder purge: search for local-only Nix build hints

Scope: every skill source in the Curriculum repository and the generated
`/home/li/primary/{.agents,.claude,.codex,.pi}` trees; every git-tracked file
in every repository under `/git/github.com/LiGoldragon/`; user Nix config;
Claude Code and Codex harness settings. Searched for `--builders`,
`builders =`, `max-jobs`, `--option builders`, substituters-style
local-only hints, `NIX_CONFIG`/`NIX_REMOTE`, and prose telling a flow to
build locally.

## Table of hits

| # | Location | What it was | Disposition | Action |
|---|----------|-------------|-------------|--------|
| 1 | `Curriculum/skills/lojix.md` (and its generated copies in `.agents/`, `.claude/skills/lojix/SKILL.md`) — "extra substituters" | Lojix protocol vocabulary about a `substituters` request field, unrelated to how this flow builds | Not a hit — no local-build instruction | none |
| 2 | `/home/li/primary/.pi/continue/*.md` — many entries with `--option max-jobs 0 --builders '@/etc/nix/machines'` | Historical transcript records of prior remote-only build commands actually run | Not a hit — these force remote building correctly; `.pi` is generated read-only evidence and not edited regardless | none |
| 3 | `/home/li/primary/.pi/continue/MDE5ZjRjY2YtNmUwYS03NGFlLTgwZDktN2UxZmZhMjQ1OWE5.md:21` — `nix build --option builders '' .#checks...spirit-deployment` | A one-off ad-hoc command typed in a past session against a `CriomOS-home-spirit-domain-all` checkout that no longer exists on disk or as a tracked repo path | Stale, unreachable; `.pi` is generated read-only evidence, never edited | none (reported only) |
| 4 | `content-identity/README.md:47`, `raw-discovery/README.md:21` — `nix flake check --max-jobs 0` | Correct pattern for forcing remote-only builds | Not a hit | none |
| 5 | `goldragon/AGENTS.md:38` | Instructs `nix run` validation to use `max-jobs = 0`, `@/etc/nix/machines`, and disable fallback so Prometheus performs realization | Not a hit — this is the desired remote-forcing instruction | none |
| 6 | `lojix/ARCHITECTURE.md:333-341`, `CriomOS/NON_IDEAL_AGENTS.md:30-46` | Both instruct remote-only evaluation/realization via `--option max-jobs 0 --builders '@/etc/nix/machines'` and inherited `NIX_CONFIG` forcing the same | Not a hit — desired behavior | none |
| 7 | `CriomOS/checks/nix-role-policy/default.nix:97,108,111` | Asserts specific `nix.settings.max-jobs` values (1, 1, 4) for NixOS host *roles* being deployed (base/edge-builder/service), unrelated to how this dev flow builds | Not a hit | none |
| 8 | `CriomOS-test-cluster/checks/cluster-contracts.nix:125` | Asserts `nix.settings.substituters` value inside a deployed test-node's own NixOS config, unrelated to this flow's own build path | Not a hit | none |
| 9 | `CriomOS-test-cluster/lib/deploy-flake.nix:254` — `NIX_CONFIG = "... substituters =\n"` | Sets an empty-substituters `NIX_CONFIG` as the build environment for a trivial `runCommand` derivation that only assembles a fixture flake text for a simulated VM node; not a directive about this flow's own builds | Investigated, treated as a non-issue | none |
| 10 | `signal-message/README.md:19-20` — `` nix --option substituters https://cache.nixos.org flake check --print-build-logs `` | Documented proof-matrix command narrowed substituters to `cache.nixos.org` only, excluding the configured `nix.prometheus.goldragon.criome` substituter and diverging from default config | **Hit** — removed the override | Edited to `nix flake check --print-build-logs`; committed (`8b1b0db5`) and pushed to `origin/main` on the real remote, verified with `git ls-remote https://github.com/LiGoldragon/signal-message.git refs/heads/main` |
| 11 | `spirit-ethos/README.md:82-86` — `` nix flake check --option eval-cache false --option substituters '' -L `` | Documented reproducible-source-gate command disabled substituters entirely (`--option substituters ''`) | **Hit** — removed the override | Edited to `nix flake check --option eval-cache false -L`; committed only `README.md` (`dfca49b3d08c`, leaving the repo's pre-existing unrelated dirty files — `Cargo.lock`, `Cargo.toml`, `meta-allocation-manifest.nota`, `meta-batch-config.json`, `meta.ethos`, `tests/meta_allocation.rs` — untouched) and pushed to `origin/main`, verified with `git ls-remote origin refs/heads/main` |
| 12 | `~/.config/nix/nix.conf` | `max-jobs = 0`, `builders = @/etc/nix/machines`, `builders-use-substitutes = true` | Correct — already forces remote building via Prometheus | none |
| 13 | `/etc/nix/nix.conf`, `/etc/nix/machines` | System default `max-jobs = 1`; machines file lists only Prometheus (`ssh-ng://nix-ssh@prometheus.goldragon.criome`) | Not overridden locally in a way that bypasses the machines file; the per-user override in #12 already forces remote for interactive/agent work | none |
| 14 | `~/.zshrc`, `~/.bashrc`, `~/.bash_profile`, `~/.profile`, `~/.zprofile`, current environment | No `NIX_CONFIG`, `NIX_REMOTE`, `builders`, `max-jobs`, or `substituters` settings | Clean | none |
| 15 | `~/.nix-channels` | Does not exist | N/A | none |
| 16 | `CriomOS/.envrc`, `horizon-rs/.envrc` (only tracked `.envrc` files across all LiGoldragon repos) | Plain `use flake` / direnv boilerplate | Clean | none |
| 17 | `~/.claude/settings.json` | No hooks, no `env` entries, and no permissions related to nix builders/max-jobs/substituters | Clean | none |
| 18 | `~/.codex/config.toml` | No `[hooks]`, no nix-related keys in `[shell_environment_policy.set]` or elsewhere | Clean | none |
| 19 | `/home/li/primary/.claude/settings*.json` | File does not exist in this project | N/A | none |

## Coordination

- `signal-message` was already reserved by this flow's own Lock 1274
  (`SignalMessageFrameUnfork`, path `/git/github.com/LiGoldragon/signal-message`),
  covering the edited path; the working copy was clean there beforehand, so
  no new lock was needed or taken, and Lock 1274 was left alone since it
  belongs to unrelated in-progress work under this same flow.
- Acquired Lock 1332 (`BuilderPurgeSpiritEthos`, path
  `/git/github.com/LiGoldragon/spirit-ethos/README.md`) for the second edit
  and released it (`Released.{ 1332 ... }`) after the push was verified.
- Both pushes were confirmed against the real GitHub remote via
  `git ls-remote`, not merely the local `origin` config.

## Sources

- `git grep` across every repository directory under `/git/github.com/LiGoldragon/` for `flake.nix`, `nix.conf`, `*.sh`, `justfile`/`Justfile`, `Makefile`, `*.yml`/`*.yaml`, `AGENTS.md`, `README.md`, `CLAUDE.md`, `checks/*`, `.github/**`, plus a separate pass for `NIX_CONFIG`/`NIX_REMOTE`.
- `grep -r` across `/git/github.com/LiGoldragon/Curriculum/skills` and the generated `.agents/`, `.claude/`, `.codex/`, `.pi/` trees under `/home/li/primary`.
- Direct reads of `~/.config/nix/nix.conf`, `/etc/nix/nix.conf`, `/etc/nix/machines`, `~/.zshrc`/`~/.bashrc`/`~/.bash_profile`/`~/.profile`/`~/.zprofile`, the current shell environment, `~/.claude/settings.json`, `~/.codex/config.toml`.
- `jj`/`git` commit, push, and `git ls-remote` output for the two edited repositories.
- `orchestrate 'Observe.Locks'` output for existing Lock coverage, and `Locked`/`Released` replies for Lock 1332.
