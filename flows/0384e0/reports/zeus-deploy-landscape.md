# Zeus Deploy Landscape

Subflow 0384e0 read-only witness, 2026-09-06.

## 1. Identity

- **Cluster:** `goldragon`
- **Node:** `zeus` (lowercase throughout Lojix, proposal data, and CriomOS source)
- **Host composition:** `CompleteHost`

The node `zeus` is declared in the cluster proposal file
`/git/github.com/LiGoldragon/goldragon/proposal.datom` (line 1, single-line
file) as:

```
zeus {Edge Max Max {Metal Some.X86_64 4 Some.ThinkPadT14Gen2Intel ...}}
```

The CriomOS source does not declare zeus directly; it consumes the projected
Horizon input at evaluation time. The `NON_IDEAL_AGENTS.md` at
`/git/github.com/LiGoldragon/CriomOS/NON_IDEAL_AGENTS.md` line 22 references
the pair explicitly: "Materialize `goldragon` / `zeus` as `CompleteHost`".

Confirmed by Lojix query: `lojix 'Query.ByNode.(goldragon zeus None)'`
returned generation and deployment records with `goldragon zeus CompleteHost`.

## 2. Route

- **Canonical internal hostname:** `zeus.goldragon.criome`
- **Nix store URI (CompleteHost):** `ssh-ng://root@zeus.goldragon.criome`
- **SSH destination (CompleteHost):** `root@zeus.goldragon.criome`

Derived from Horizon cluster data convention found in
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/test-substrate.nix` line 112:

```nix
criomeDomainName = node.criomeDomainName or "${node.name}.${clusterName}.criome";
```

Zeus has no `criomeDomainName` override in the proposal, so the default
`zeus.goldragon.criome` applies. The same pattern is visible for prometheus at
`nix.prometheus.goldragon.criome` in
`/git/github.com/LiGoldragon/CriomOS/reports/0030-handover-2026-04-28-evening.md`
line 233.

I did not find an explicit transport pair written down for zeus. The store URI
and SSH destination above are the Horizon-derived canonical values per the
`GUIDELINES.md` line 276 convention of matching `ssh-ng://user@host` and
`user@host` pairs.

## 3. Latest

### CriomOS (`/git/github.com/LiGoldragon/CriomOS`)

| Field | Value |
|---|---|
| Branch | detached HEAD (no named branch) |
| HEAD | `14a246f5b64c31d1208d9edd76f05acd9b4828b1` |
| HEAD subject | Pin CriomOS-home a83210d3 (Codex main model to gpt-6-astra) |
| HEAD date | 2026-09-05 12:20:27 +0200 |
| Working tree | clean |
| Ahead of origin/main | 0 |
| Behind origin/main | 8 |
| origin/main HEAD | `57ec0138e28d2c389a8d7d4d4424e6840af5acc0` |
| origin/main subject | Pin Orchestrate framed Datom Signals |
| HEAD pushed? | Yes (ancestor of origin/main) |

Commits HEAD is behind origin/main:

1. `57ec013` Pin Orchestrate framed Datom Signals
2. `8f48ff4` Pin CriomOS-home Claude Answers Datom migration
3. `bd6fc54` Pin Plannotator Home review package
4. `a66c938` Pin Codex command Home release
5. `a099bf9` Pin stronger Wispr meter visibility
6. `55a9fa7` Pin Wispr meter Home revision
7. `30fe10e` Pin repaired Wispr control Home revision
8. `a97e9ef` Pin Wispr-only Home activation revision

### CriomOS-home (`/git/github.com/LiGoldragon/CriomOS-home`)

| Field | Value |
|---|---|
| Branch | detached HEAD (no named branch) |
| HEAD | `a83210d3e0afd44fcdb9fa893fa582a22913146f` |
| HEAD subject | Upgrade Codex main model to gpt-6-astra |
| HEAD date | 2026-09-05 12:19:08 +0200 |
| Working tree | clean |
| Ahead of origin/main | 0 |
| Behind origin/main | 20 |
| origin/main HEAD | `654144d71a51f92bba56e405faab3243e2dce4ba` |
| origin/main subject | CriomOS-home: pin current Chroma Datom producer |
| HEAD pushed? | Yes (ancestor of origin/main) |

Both working trees are clean. Both HEADs are pushed (ancestors of their
respective origin/main). Neither is on a named branch.

## 4. Running State

| Component | Value | Source |
|---|---|---|
| lojix-daemon | **active** | `systemctl is-active lojix-daemon` |
| LOJIX_ORDINARY_SOCKET | `/run/lojix/ordinary.sock` | `/etc/set-environment` |
| LOJIX_OWNER_SOCKET | `/run/lojix/owner.sock` | `/etc/set-environment` |
| lojix executable | `/run/current-system/sw/bin/lojix` | `which lojix` |
| meta-lojix executable | `/run/current-system/sw/bin/meta-lojix` | `which meta-lojix` |
| Inline Dotos support (lojix) | **Yes** | Confirmed: `lojix 'Query.ByNode.(test test None)'` decoded and returned `Queried.([] [] (5387 5387))` |
| Inline Dotos support (meta-lojix) | **Yes** | Confirmed: `meta-lojix 'Query.ByNode.(test test None)'` returned `(CliRejected [DOTOS request did not decode: unknown z2VW7Q variant Query])` -- the rejection is a contract mismatch (Query is not in signal-meta-lojix), not a Dotos parse failure |

## 5. Current Generation

Query: `lojix 'Query.ByNode.(goldragon zeus None)'`

**Current CompleteHost generation (marked `Current`):**

```
(181 181 goldragon zeus CompleteHost LiveActivation Current
  Some./nix/store/c3753yv0095xj97hld1mszyx6585xv5k-nixos-system-zeus-26.11.20260813.0e251e2
  Some.59d12e6fc664c8be0f8dc8af2846c81abdf860cb)
```

- Generation ID: 181
- Deployment ID: 181
- Action: `Host.ActivateNow`, LiveActivation
- Source revision: `59d12e6fc664c8be0f8dc8af2846c81abdf860cb`
- Store path: `/nix/store/c3753yv0095xj97hld1mszyx6585xv5k-nixos-system-zeus-26.11.20260813.0e251e2`
- Terminal state: `Succeeded`

**Current UserEnvironment generations (marked `Current`):**

- **bird** (gen 167, dep 167): `/nix/store/dhwq1j6ndp5kh47nqasmfblv2w93h82d-home-manager-generation`, source `eefa86f117ee173670b82b49f1a60e86b94fac27`
- **li** (gen 49, dep 49): `/nix/store/czqlj0ws84i9v9mxhv95bvk07xirff17-home-manager-generation`, source `756ce723ea7f1a58d20e2b6f153f15e30aa9b885`

Full verbatim reply omitted for length; it contains 19 generations and 41
deployments. The above are the entries marked `Current`.

## 6. Proposal

Four absolute regular non-symlink `proposal.datom` files found containing zeus:

| # | Path | Context |
|---|---|---|
| 1 | `/git/github.com/LiGoldragon/goldragon/proposal.datom` | Main goldragon checkout |
| 2 | `/home/li/wt/github.com/LiGoldragon/goldragon/generic-nodes-542442/proposal.datom` | Worktree (flow 542442) |
| 3 | `/home/li/wt/github.com/LiGoldragon/goldragon/lojix-canonical-proposal/proposal.datom` | Worktree |
| 4 | `/home/li/wt/github.com/LiGoldragon/goldragon/goldragon-main-canonical/proposal.datom` | Worktree |

All four are regular files (not symlinks). All contain the zeus node declaration.

## 7. Drift

The current deployed CompleteHost generation (181) was built from source
revision `59d12e6fc664c8be0f8dc8af2846c81abdf860cb`.

| Measure | Count |
|---|---|
| Deployed rev to local HEAD | 11 commits behind |
| Deployed rev to origin/main | 19 commits behind |

Commits from deployed revision to origin/main:

1. `57ec013` Pin Orchestrate framed Datom Signals
2. `8f48ff4` Pin CriomOS-home Claude Answers Datom migration
3. `bd6fc54` Pin Plannotator Home review package
4. `a66c938` Pin Codex command Home release
5. `a099bf9` Pin stronger Wispr meter visibility
6. `55a9fa7` Pin Wispr meter Home revision
7. `30fe10e` Pin repaired Wispr control Home revision
8. `a97e9ef` Pin Wispr-only Home activation revision
9. `14a246f` Pin CriomOS-home a83210d3 (Codex main model to gpt-6-astra)
10. `fd6e275` Pin CriomOS-home befd927 (remove VSCodium)
11. `f8cda85` Pin CriomOS-home 5be7121 (terminal scope OOM policy)
12. `f3d8b2c` Update Home ownership pin invariant
13. `4d1309f` Pin CriomOS-home d9bec96
14. `1523375` Document Home partial activation gate
15. `bc0dc04` CriomOS: advance Home to claude-code 2.1.261, codex 0.153.3, claude-desktop 1.46388.2
16. `840ed01` CriomOS: advance Home Wispr recovery inputs
17. `0b690db` Advance Home Noctalia startup repair
18. `d869176` Advance Home Wispr provider to 1.6.774+criomos.4
19. `1c0f7ef` Advance Home Wispr provider to 1.6.774+criomos.3

Zeus is behind. The locally checked-out CriomOS HEAD (`14a246f`) is itself 8
commits behind origin/main, so "latest CriomOS" depends on whether the deploy
targets the local checkout or the remote tip.

## Sources

- `lojix 'Query.ByNode.(goldragon zeus None)'` -- ran on this host, ordinary socket
- `lojix 'Query.ByDeployment.(181)'` -- ran on this host, ordinary socket
- `/git/github.com/LiGoldragon/goldragon/proposal.datom` -- read
- `/git/github.com/LiGoldragon/CriomOS/NON_IDEAL_AGENTS.md` -- read
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/test-substrate.nix` line 112 -- read
- `/git/github.com/LiGoldragon/CriomOS/docs/GUIDELINES.md` lines 276-289 -- read
- `/git/github.com/LiGoldragon/CriomOS/reports/0030-handover-2026-04-28-evening.md` line 233 -- read
- `/etc/set-environment` -- read (socket variable source)
- `systemctl is-active lojix-daemon` -- ran
- `git log`, `git status`, `git rev-list` in both CriomOS and CriomOS-home -- ran
