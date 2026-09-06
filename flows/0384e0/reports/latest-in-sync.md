# Latest CriomOS / CriomOS-home Sync Report

## 1. Newest pushed CriomOS

**origin/main tip: `57ec0138e28d2c389a8d7d4d4424e6840af5acc0`**

Witnessed by `git fetch --all` then `git rev-parse origin/main` in
`/git/github.com/LiGoldragon/CriomOS`.

origin/main is the newest pushed tip that matters for deployment. Three
feature branches (`horizon-flake-integration-542442` at 15 ahead,
`horizon-module-consumer-fix-542442` at 4 ahead,
`horizon-module-migration-542442` at 2 ahead) carry unmerged work; none
is a deployment candidate.

## 2. What CriomOS origin/main pins

Read from `git show origin/main:flake.lock`:

| Input | Pinned revision | Repository |
|-------|----------------|------------|
| criomos-home | `08717ef8950e514c346cbdfbc69143e4369056fb` | LiGoldragon/CriomOS-home |
| lojix | `d3c0ac9032250e0b12ade7d8c71a8fc8311ab5bf` | LiGoldragon/lojix |
| orchestrate | `5f016531e765d9b679a86cc47a2d75eaca43d624` | LiGoldragon/orchestrate |

The pinned CriomOS-home revision `08717ef8` is **not** the current
CriomOS-home origin/main tip `654144d7`.

The pin is explicit (rev-locked in `flake.nix`'s `criomos-home.url`),
confirmed by reading `git show origin/main:flake.nix`.

## 3. Gap between pinned Home and Home origin/main

`08717ef8` is an **ancestor** of `654144d7` (confirmed by
`git merge-base --is-ancestor`). Seven commits separate them:

```
654144d CriomOS-home: pin current Chroma Datom producer
0808afc CriomOS-home: repair Horizon isolation fixtures
a464fd7 CriomOS-home: align Horizon test fixtures
8cda3ba CriomOS-home: read projected machine architecture
ad20d95 Pin corrected Orchestrate migration
4bac7ce Read Horizon Home gates from projected capabilities
b12e3dc Consume Horizon user vectors in Home
```

These 7 commits touch:

- **Horizon user vectors** — new `lib/horizon-user.nix`, consumer changes in
  `modules/home/profiles/min/agent-intercom.nix`, `modules/home/profiles/min/spirit.nix`,
  `modules/home/profiles/min/sway.nix`, `modules/home/default.nix`
- **Orchestrate** — re-pinned from `5f016531` to `ac8a92666f4a` in Home's own flake
- **Chroma** — re-pinned from `1b626d9d` to `c9c11a5b` in Home's own flake
- **Horizon test fixtures** — isolation and alignment repairs in checks
- **Machine architecture projection** — new capability reading in checks

The CriomOS-home commits at origin/main assume a Horizon user-vector
shape that CriomOS origin/main does not yet provide: the new
`lib/horizon-user.nix` in Home expects `horizon.users` to be a vector
with fields like `size`, `publicKeys`, `hasPublicKey`, `sshPublicKey`,
`resolvedTextSize`. This converter is consumed by CriomOS's `flake.nix`
only in the unmerged feature branches (notably
`horizon-flake-integration-542442`), **not** on CriomOS origin/main.

## 4. Would deploying newest CriomOS carry newest Home?

**No. They are not in sync.**

Deploying CriomOS `57ec0138` would carry CriomOS-home `08717ef8`, which
is 7 commits behind CriomOS-home origin/main `654144d7`.

Furthermore, even if CriomOS were updated to pin Home `654144d7`, the
Home code at that tip depends on Horizon user-vector plumbing that
CriomOS origin/main does not yet wire — that wiring lives on the
unmerged `horizon-flake-integration-542442` branch. Pinning Home tip
without merging that branch would produce a build failure or incorrect
behavior.

## 5. Minimal correct action to bring them in sync

There are two layers of drift:

1. **The pin is stale** — CriomOS origin/main pins Home `08717ef8` instead of
   `654144d7`.
2. **The Home tip depends on CriomOS-side Horizon plumbing not yet on main** —
   the `horizon-flake-integration-542442` branch carries the CriomOS-side
   `lib/horizon-user.nix` and the `homeUsers` mapping that the Home tip's
   modules expect.

The minimal correct sequence:

- Merge the Horizon flake integration work from
  `origin/horizon-flake-integration-542442` (or a suitable subset) into
  CriomOS main, which brings the CriomOS-side `lib/horizon-user.nix` and
  the `homeConfigurations` wiring.
- Update the `criomos-home` pin in CriomOS's `flake.nix` to `654144d7`
  (or whatever Home tip is correct at that point).
- Update `flake.lock` accordingly.
- Commit, push, and deploy.

Simply updating the Home pin without merging the Horizon plumbing would
be incorrect — the Home modules at `654144d7` consume a user-vector
shape that only the feature branch provides.

**Alternative**: if the psyche wants to deploy *now* without the Horizon
work, then deploying CriomOS `57ec0138` as-is is coherent — it carries
Home `08717ef8`, which is internally consistent with that CriomOS
revision. It just does not carry the newest Home.

## 6. Do local detached checkouts matter?

**They are irrelevant.** A `RequireImmutable` deployment names a pushed
revision by its hash. The deploy fetches from the forge; the local
checkout's HEAD position does not enter the build or deployment path.
The local checkouts at `14a246f5` (CriomOS, 8 behind) and `a83210d3`
(Home, 20 behind) are working-tree artifacts of prior sessions and have
no effect on a deployment that names `57ec0138`.

Witnessed by: the deployment mechanism resolves the named revision from
the forge, not from any local worktree. The `RequireImmutable` contract
requires a pushed, immutable source revision.

## 7. Changes between deployed 59d12e6f and newest 57ec0138

19 commits separate the deployed CriomOS revision from origin/main.
Files changed: `flake.lock`, `flake.nix`, `ARCHITECTURE.md`,
`UPGRADES.md`, `checks/lojix-ownership/default.nix`.

### Subsystems touched

- **CriomOS-home pin** — advanced from `9c8ded53` through many
  intermediate pins to `08717ef8`. This covers Wispr provider upgrades
  (1.6.774+criomos.3 and .4), Wispr recovery, Noctalia startup repair,
  claude-code 2.1.261, codex 0.153.3, claude-desktop 1.46388.2,
  VSCodium removal, terminal scope OOM policy, Codex main model change
  to gpt-6-astra, Wispr meter visibility, and Orchestrate Datom Signals.
- **Orchestrate pin** — advanced from `885f6e3e` to `5f016531`.
- **Lojix ownership check** — updated expected revision from `34a8e9c`/0.20.2
  to `d3c0ac9`/0.20.3, expected Home revision to `c40ff0cd`, expected
  Orchestrate to `9585484738ce`.
- **ARCHITECTURE.md** — Codex command-family documentation: `codex` is now
  the pinned upstream CLI with native Home approval; `codex-remote`
  explicitly attaches to the persistent local app-server;
  `codex-raw`/`direct-codex` are not published.
- **UPGRADES.md** — three breaking-upgrade records:
  1. ChatGPT Desktop vendor-boundary Home consumer
  2. Flow identity helper Home consumer (Harness `d02242`, explicit
     `flow-id claude` form required)
  3. Orchestrate 0.26.0 Home consumer (WireContract replacement, breaking
     for both sockets)

### Breaking-change flags

**UPGRADES.md documents three breaking upgrades** between the deployed
revision and origin/main. The Orchestrate 0.26.0 WireContract
replacement is the most operationally significant — it is breaking for
both sockets, requires coordinated Nexus stop/preflight/activation, and
rollback is the preceding Home generation with its matching 0.25
wrappers. The flow identity helper change alters Claude parent-flow
invocation syntax. The ChatGPT Desktop change alters the vendor-private
resource tree.

None of these touch boot or the system activation path directly — they
are Home-profile (user environment) changes. However, the Orchestrate
0.26.0 breaking change means **this deployment is a breaking upgrade,
not a routine one**, and requires the coordinated procedure documented
in UPGRADES.md.

## Sources

| Claim | Method | Location |
|-------|--------|----------|
| CriomOS origin/main = 57ec0138 | `git fetch --all && git rev-parse origin/main` | /git/github.com/LiGoldragon/CriomOS |
| CriomOS-home origin/main = 654144d7 | `git fetch --all && git rev-parse origin/main` | /git/github.com/LiGoldragon/CriomOS-home |
| Home pin = 08717ef8 | `git show origin/main:flake.lock` parsed | /git/github.com/LiGoldragon/CriomOS |
| Lojix pin = d3c0ac90 | `git show origin/main:flake.lock` parsed | /git/github.com/LiGoldragon/CriomOS |
| Home pin URL in flake.nix | `git diff 59d12e6f..origin/main -- flake.nix` | /git/github.com/LiGoldragon/CriomOS |
| Ancestor relationship | `git merge-base --is-ancestor 08717ef origin/main` | /git/github.com/LiGoldragon/CriomOS-home |
| 7-commit gap | `git log --oneline 08717ef..origin/main` | /git/github.com/LiGoldragon/CriomOS-home |
| Home diff stat | `git diff --stat 08717ef..origin/main` | /git/github.com/LiGoldragon/CriomOS-home |
| Home horizon-user.nix content | `git diff 08717ef..origin/main -- lib/horizon-user.nix modules/ flake.nix` | /git/github.com/LiGoldragon/CriomOS-home |
| Feature branches ahead | `git branch -r --sort=-committerdate` + rev-list counts | /git/github.com/LiGoldragon/CriomOS |
| 19-commit gap deployed-to-tip | `git rev-list --count 59d12e6f..origin/main` | /git/github.com/LiGoldragon/CriomOS |
| UPGRADES.md content | `git show origin/main:UPGRADES.md` | /git/github.com/LiGoldragon/CriomOS |
| Lojix ownership check changes | `git diff 59d12e6f..origin/main -- checks/` | /git/github.com/LiGoldragon/CriomOS |
| ARCHITECTURE.md changes | `git diff 59d12e6f..origin/main -- ARCHITECTURE.md` | /git/github.com/LiGoldragon/CriomOS |
| No branch ahead of origin/main for deployment | `git rev-list --count origin/main..<branch>` for top branches | /git/github.com/LiGoldragon/CriomOS |
