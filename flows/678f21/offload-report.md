# Heavy work on prometheus, laptop quiet (Psyche core Sonnet c3c1a0, 2026-11-11)

Files: `/home/li/primary/flows/678f21/offload/` (samples-20min.txt, sample.sh, remote-eval-*.txt, local-eval-*.txt, test-rev.txt). No system configuration was changed.

## 1. What loads the laptop (120 samples, 10 s apart, 03:11 to 03:31; pidstat and atop are not installed, `top` is used)
Load average 2.0 (max 3.76); RAM used 7.4G average of about 31G (max 7.8G). RAM is not the problem. CPU-seconds over 20 min by kind:

| Kind | CPU-s | Note |
|---|---|---|
| **kernel thread `irq/9-acpi`** | **654** (about 0.55 core, always on) | ACPI interrupt storm: GPE 6D has fired 6.94M times in 11.5 h (about 167 per second); its CPU time went 13:33 to 22:28 min during the sampling. Not a Nix or cargo load. |
| Claude harness processes | 103 | flows' own clients |
| herdr server | 93 | |
| journalctl (a flow reading `-b -7`, 98% of a core for 8+ s) | 60 | other |
| Nix-store binaries (codex, ghostty, wispr-flow, claude-desktop, noctalia) | ~140 | desktop apps, not Nix evaluation |
| Nix evaluation, cargo, zoekt indexer | none in the top 15 | none ran in the window |

So the fan noise heard in this window is mostly the kernel ACPI thread, which prometheus cannot take. Nix evaluation, cargo and zoekt did not run in the window; they are bursts, which the protocol below moves.

## 2. Tools (version as in nixpkgs on prometheus)
| Tool | What it does | In nixpkgs | Cost |
|---|---|---|---|
| `ssh prometheus 'nix eval/build github:OWNER/REPO?rev=R#attr'` | evaluates a pushed rev on prometheus | nix 2.35.3 | free; laptop CPU about 0 |
| `nix build --eval-store auto --store ssh-ng://…` | evaluation on the laptop, build remote | nix | evaluation stays local |
| nix-eval-jobs 2.35.4 | parallel evaluation of many attributes, JSON stream | yes | good for check sets on 32 cores |
| nix-fast-build 2.0.4 | nix-eval-jobs plus builds, with remote builders | yes | convenient for whole checks |
| colmena 0.5.0, deploy-rs 1.0.0 | deployments | yes | not needed: Lojix deploys |
| `git push cluster` (git.goldragon.criome) | makes a rev reachable by prometheus | git | the preferred path for committed work |
| `git bundle`, rsync 3.5.0 | one-off transfer of uncommitted work | yes (rsync installed here) | rsync of a working tree: seconds, deltas only |
| mutagen 0.18.1, unison 2.54.0 | continuous two-way mirror | yes | background watcher on the laptop: costs the CPU we want to save; use one-shot rsync instead |
| ssh remote command runner for agents | `ssh prometheus 'cd tree && cargo test'` | ssh | no daemon; output returns on stdout |

## 3. Protocol draft
1. Committed and pushed work runs on prometheus: `ssh prometheus.goldragon.criome "nix eval --raw 'github:LiGoldragon/<repo>?rev=<40-hex>#<attr>'"`, likewise `nix build`; builds already go through the builder.
2. Uncommitted work: `rsync -a --delete --exclude target --exclude .git ./ prometheus:/tmp/offload/<repo>/` then `ssh prometheus 'cd /tmp/offload/<repo> && <cargo test | rg | nix eval path:.>'`. Prefer to commit and push to `cluster` first.
3. Cargo, tests, `rg` over large trees, flake updates and the zoekt indexer run on prometheus the same way; output returns on stdout, files stay there unless wanted (`rsync` back).
4. The laptop keeps: editing, git operations, the flows' clients, reading results. A host's toplevel evaluation goes through Lojix on prometheus, not by hand.
5. Rev rule: the 40-hex rev must be on a remote prometheus reaches; check with `git branch -r --contains <rev>`.

## 4. Test (real case; a CriomOS host could not be evaluated by hand)
CriomOS's `system`, `horizon` and `pkgs` inputs are stubs that stop evaluation ("use the deploy materialization tool"); a host evaluation belongs to Lojix with a horizon proposal, and was not attempted (it would configure a system). The same comparison was made on a pushed lojix rev (321682e): `nix eval --raw 'github:LiGoldragon/lojix?rev=321682e0…#packages.x86_64-linux.default.drvPath' --option eval-cache false`. Both hosts gave the same `.drv` path (…-lojix-0.10.6.drv).

| Run | Wall | Laptop CPU (user+sys) |
|---|---|---|
| prometheus, first (fetch of sources) | 27.6 s | 0.02 s (ssh only) |
| prometheus, second | 5.3 s | 0.02 s |
| laptop, first (copies nixpkgs source from prometheus's cache) | 74.8 s | 2.8 s |
| laptop, second | 24.1 s | 2.5 s |

Remote is 4.5 to 14 times faster in wall time and takes the laptop CPU from 2.5 s to nothing. The laptop gain per evaluation is small in CPU-seconds; the real load on the laptop is the ACPI thread.

## 5. Other findings
- `cannot link "/nix/store/.links/…": No space left on device` appears in `nix eval` and `nix store optimise` although 222G is free: the store's `.links` directory is probably at the filesystem's per-directory entry limit. Evaluation still succeeds; optimise cannot dedupe more. Cause unconfirmed.
- Candidate fix for the ACPI storm (not applied, configuration change): the BIOS flash the living plans may clear it; otherwise the kernel parameter `acpi_mask_gpe=0x6D` (a CriomOS decision).
