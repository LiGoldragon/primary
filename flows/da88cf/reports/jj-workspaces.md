# jj workspace audit — CriomOS, CriomOS-home, goldragon

Scanned 2026-09-25, read-only, `--ignore-working-copy` throughout. Scope: the
17 workspaces across these three repos whose `jj workspace list` entry shows
a real working-copy change (not `(empty)`) with `(no description set)`. Source
listing: `flows/da88cf/reports/inventory-branches.md`, re-verified live against
the canonical checkouts under `/git/github.com/LiGoldragon/`.

`goldragon` has zero matching workspaces — every one of its jj workspaces is
either `(empty)` or already carries a description; nothing to audit there.

## CriomOS — 15 of 16 candidates are one mechanical, identical diff

All fifteen below have the exact same single-file diff:

```
.claude/settings.json | 26 --------------------------
1 file changed, 0 insertions(+), 26 deletions(-)
```

i.e. each workspace's working copy merely lacks a `.claude/settings.json`
that its parent commit had — a generated/symlinked file drifting out from
under separate checkouts, not authored work. No owning flow was found for
any of them (`grep -rl <name> flows/*/log.md` empty for all 15); parents
range 2026-08-08 to 2026-08-24, all >14 days stale.

| workspace | change id | parent (age, desc) | path exists |
|---|---|---|---|
| ChromaNoctaliaDeployIntegration | vkrxnnyu | 9b8b06438f0e, 2026-08-19, "Pin Home Noctalia state reconciliation" | yes |
| DotosMapKeyCompatibility | lktmttoy | 134103382f2f, 2026-08-08, "CriomOS: pin home and lojix dotos compatibility" | yes |
| IntegrateLojix0191 | wkymzkxu | 65a0e024a1b8, 2026-08-23, "CriomOS: pin Lojix 0.19.2 reconciliation fix" | yes |
| ZeusVscodiumDeployment | xuswlysm | ef12134db512, 2026-08-09, "CriomOS: deploy VSCodium lifecycle recovery" | yes |
| criomosDotosRepair | oooywuno | 35fc6e9896d0, 2026-08-24, "checks: execute complex ClaviFaber publication contract" | yes |
| default-opener-nhb-pin | ulmnzotp | 90da2a6f82ec, 2026-08-22, "Pin CriomOS-home default opener revision" | yes |
| dotos-upper-integration | vskktpnr | 92ec4db338ae, 2026-08-10, "CriomOS: pin current Home contract integration" | yes |
| fixlojixbootownership | urqrpsnq | 02ac43b193ef, 2026-08-23, "pin loader-authoritative lojix" | yes |
| home-orchestrate-main-pin | uqywwzyp | b35522f67e3b, 2026-08-10, "CriomOS: pin Home without retired Orchestrate writer" | yes |
| lojix-breaking-upgrade-docs | lovywlul | c299616e9828, 2026-08-23, "docs: record Lojix breaking upgrade procedure" | yes |
| lojix-ownership-mjl6-criomos | xmxwnput | 3de85f81464b, 2026-08-10, "CriomOS: derive Lojix Persona identity from Horizon" | yes |
| modifier-architecture-20260811 | wpzpomtk | e8277b02509e, 2026-08-11, "docs: record deployment convergence witnesses" | yes |
| remove-lojix-timeout-consumer | wkoukzqw | a4322cd14482, 2026-08-23, "lojix: remove effect timeout configuration" | yes |
| repair-home-dependency-chain-20260811 | uzwlutlx | 2603ba3a510e, 2026-08-11, "CriomOS: pin bootstrap-compatible Home and Orchestrate" | yes |
| schema-rust-main-repair | xorxrtrw | cfeae711b916, 2026-08-10, "CriomOS: pin integrated Home session witness" | yes |

Class: **empty/stale** (all 15) — the diff is not real content, parents are
all >14 days old, and no live flow claims any of these names.

## CriomOS — the one real exception

| workspace | change id | parent (age, desc) | diff | owner | class |
|---|---|---|---|---|---|
| wifi-country-da88cf | yrmwklop | d193bafca6d7, 2026-09-25 (today, current CriomOS main) | 7 files, 88 insertions/3 deletions: `checks/router-wifi-country/default.nix` (new, 59 lines), `checks/router-wifi-horizon-policy/default.nix`, `modules/nixos/router/default.nix`, `flake.nix`, plus small edits to `resolver-role-policy`/`router-wan-recovery`/`router-yggdrasil-ndp` checks | flow **da88cf** (this flow — the branch name carries its own flow id, and `flows/da88cf/log.md` records dispatching "the Wi-Fi feature implementer: horizon-rs country field..., CriomOS PL fallback removed, hostapd verbosity declared" tonight) | **live work** — da88cf is `working` in `hm-list`, and this is exactly the in-flight Wi-Fi-country feature it dispatched this session |

## CriomOS-home — 1 candidate

| workspace | change id | parent (age, desc) | diff | owner | class |
|---|---|---|---|---|---|
| home-canonical-llm-packages | xysxxwkl | 4e36d4406f11, 2026-08-27 (29d old) | large: 59 files, 2638 insertions/434 deletions — owned-agents packaging refactor (chatgpt/claude-code/claude-desktop/codex under `owned-agents/`, new `lib/*.nix` helpers, `docs/UPSTREAM-NOTICES.md`, `ARCHITECTURE.md`/`UPGRADES.md` updates) | flow `01a04524` (found via `grep -rl` on `flows/01a04524/log.md`, bead `home-42n`); not present in current `hm-list` | **stale — already landed elsewhere.** Verified: the parent commit's content ships as `f964853a0c06` ("Migrate canonical Codex and Claude packages"), which `jj log -r 'ancestors(main) & f964853a0c06'` confirms is an ancestor of current CriomOS-home `main`. `01a04524`'s own log records the equivalent work "landed and pushed" as Home `f964853a0c067cdabbe0b8d4904346fadeb9a152`. This workspace's uncommitted diff is a leftover, superseded copy of work that already merged through a different path — not unlanded. |

## Counts

- empty/stale: 16 (15 CriomOS mechanical-diff workspaces + home-canonical-llm-packages, superseded)
- live work: 1 (wifi-country-da88cf)
- unknown: 0
- goldragon: 0 candidates in this category
