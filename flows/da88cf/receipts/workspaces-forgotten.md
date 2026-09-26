# Stale jj workspace forget — 2026-09-25

## CriomOS — skipped, lock held
`Lock.{ WorkspaceForget da88cf [ /git/github.com/LiGoldragon/CriomOS/.jj ] }` was
rejected: `LockRejected.PathOverlap` — held by lock 6975,
`BranchDiscard2 da88cf [ /git/github.com/LiGoldragon/CriomOS/.jj ] «Delete landed
and superseded CriomOS bookmarks»` (same flow, da88cf, different task). None of
the 15 listed CriomOS workspaces were touched.

Directories left on disk for morning (not deleted, just not forgotten):
ChromaNoctaliaDeployIntegration, DotosMapKeyCompatibility, IntegrateLojix0191,
ZeusVscodiumDeployment, criomosDotosRepair, default-opener-nhb-pin,
dotos-upper-integration, fixlojixbootownership, home-orchestrate-main-pin,
lojix-breaking-upgrade-docs, lojix-ownership-mjl6-criomos,
modifier-architecture-20260811, remove-lojix-timeout-consumer,
repair-home-dependency-chain-20260811, schema-rust-main-repair
(all under `~/wt/github.com/LiGoldragon/CriomOS/<name>`).

## CriomOS-home — done
Lock 6976 acquired on `/git/github.com/LiGoldragon/CriomOS-home/.jj`.

Re-verified `home-canonical-llm-packages` (xysxxwkl):
- `jj diff --ignore-working-copy -r xysxxwkl --stat`: 59 files changed,
  2638 insertions(+), 434 deletions(-) — matches the report.
- `jj log -r '4e36d4406f11 & ::main' --ignore-working-copy`: parent
  `4e36d4406f11` ("Preserve Codex remote launch directories") is an ancestor
  of main.

Ran `jj workspace forget home-canonical-llm-packages`. Confirmed gone from
`jj workspace list --ignore-working-copy`. Lock 6976 released.

Directory left on disk (not deleted):
`~/wt/github.com/LiGoldragon/CriomOS-home/home-canonical-llm-packages`.

## Untouched
wifi-country-da88cf, tailnet-repair-da88cf, and every workspace not in the
stale list were not inspected or touched.

## CriomOS — done (lock released, this run)
Lock 6980 acquired on `/git/github.com/LiGoldragon/CriomOS/.jj`
(`WorkspaceForget2`). Re-verified `jj workspace list --ignore-working-copy`
and `jj diff --ignore-working-copy -r <change> --stat` for all 15; each still
showed only the single `.claude/settings.json | 26 --------------------------`
removal against its recorded parent. Ran `jj workspace forget` on all 15:

ChromaNoctaliaDeployIntegration (vkrxnnyu), DotosMapKeyCompatibility
(lktmttoy), IntegrateLojix0191 (wkymzkxu), ZeusVscodiumDeployment (xuswlysm),
criomosDotosRepair (oooywuno), default-opener-nhb-pin (ulmnzotp),
dotos-upper-integration (vskktpnr), fixlojixbootownership (urqrpsnq),
home-orchestrate-main-pin (uqywwzyp), lojix-breaking-upgrade-docs (lovywlul),
lojix-ownership-mjl6-criomos (xmxwnput), modifier-architecture-20260811
(wpzpomtk), remove-lojix-timeout-consumer (wkoukzqw),
repair-home-dependency-chain-20260811 (uzwlutlx), schema-rust-main-repair
(xorxrtrw).

Confirmed all 15 gone from `jj workspace list --ignore-working-copy`.
wifi-country-da88cf, tailnet-repair-da88cf, step2-fixes-da88cf, and every
other name not in the stale list were not touched. Lock 6980 released.

Directories left on disk (not deleted), all under
`~/wt/github.com/LiGoldragon/CriomOS/<name>` (ZeusVscodiumDeployment's is
`zeus-vscodium-deployment`, lojix-ownership-mjl6-criomos's is
`lojix-ownership-mjl6`):
ChromaNoctaliaDeployIntegration, DotosMapKeyCompatibility, IntegrateLojix0191,
zeus-vscodium-deployment, criomosDotosRepair, default-opener-nhb-pin,
dotos-upper-integration, fixlojixbootownership, home-orchestrate-main-pin,
lojix-breaking-upgrade-docs, lojix-ownership-mjl6,
modifier-architecture-20260811, remove-lojix-timeout-consumer,
repair-home-dependency-chain-20260811, schema-rust-main-repair.
