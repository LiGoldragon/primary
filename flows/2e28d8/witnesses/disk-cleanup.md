# Disk cleanup witness

Method: on 2026-09-10, this flow measured the root filesystem with `df -B1 /`, measured selected authorized directories with `du -sb`, enumerated Nix-rooting `result*` symlinks with scoped `find`, pruned Nix generations with `nix-env --delete-generations old --profile <profile>`, and collected the store with `nix store gc`. Live-system identity was checked by resolving `/run/current-system` and `/nix/var/nix/profiles/system`. Nix profile and root state was verified with scoped link enumeration after collection.

Before cleanup, `/dev/nvme0n1p2` had 752,815,669,248 bytes used and 180,017,094,656 bytes free (81% full). Nix reported 158,774 paths with a 725,766,751,928-byte NAR total before cleanup.

The flow deleted 11 understood Rust `target/` directories under the configured Repository root (`/git/github.com/LiGoldragon`): `claude-answers`, `curriculum-deploy`, `datom-codec`, `ethos-zero`, `harness`, `listener`, `lojix`, `meta-signal-spirit`, `orchestrate`, `protos`, and `signal-spirit`. It deleted the authorized primary artifacts `/home/li/primary/flows/da223f/joint.0jZ7PT` (2,743,906,663 bytes) and `/home/li/primary/.pi-subagents/artifacts` (1,206,417,129 bytes). It unlinked 51 scoped repository/primary `result*` symlinks that rooted Nix closures; subsequent scoped enumeration found zero remaining.

For the Li-owned profiles, `nix-env --delete-generations old` removed Home Manager generations 989 through 1023 and legacy `.nix-profile-6-link` generations 1 through 195. The current heads remained `home-manager-1024-link`, `profile-1996-link`, and `.nix-profile-6-link-196-link`.

`nix store gc` completed successfully. Its terminal report was `42385 store paths deleted, 118.3 GiB freed`; it also reported 78.9 GiB saved by hard linking. It removed stale auto-roots corresponding to the deleted symlinks and generations.

After cleanup, the root filesystem had 602,399,010,816 bytes used and 330,433,753,088 bytes free (65% full): 150,416,658,432 bytes (about 140.1 GiB) more free than baseline.

The booted and current system profiles both resolve to `/nix/store/8y15ayy7dhr2gra53rnq3ml39vns8j65-nixos-system-ouranos-26.11.20260813.0e251e2` (system generation 180). The system profile still has generations 177 through 180. Direct Nix pruning of those paths failed with `opening lock file "/nix/var/nix/profiles/system.lock": Permission denied`; Bird's profiles are inaccessible to this user and noninteractive `sudo` is unavailable. The privileged Lojix owner contract was probed: `Retire.(goldragon ouranos 177)` returned `RetireRejected.(GenerationUnknown ...)`, demonstrating that it accepts Lojix IDs rather than Nix profile numbers. Mapped Lojix generations 112 and 138 were accepted as `Retired`, but the Nix system-generation symlinks remained, so this contract does not perform the needed profile pruning. The untracked system generation 179 has no observed Lojix generation record.

Post-GC scoped root count under `/nix/var/nix/gcroots` was 56. No declarative sources, general caches, Bottles, captures, Trash, or other user data were changed.

## Sources

- Live filesystem, Nix CLI, and profile-link probes run by this flow on 2026-09-10.
- `NON_MANAGEMENT_AGENTS.md`, `SKILL_VARIABLES.md`, and the loaded `disk-hygiene`, `nix-workflow`, `operating-system`, `lojix`, `testing`, `flow-evidence`, `psyche`, `spirit`, `behavior`, `vocabulary`, `orchestrate`, and `subflow` instructions.
