# Psyche criomos Opus d719b8: handover, 2026-11-11 00:46 CST

State log: flows/d719b8/state.md. Deploy requests and await-watch.sh (opens a Lojix watch, submits, reads to the terminal): flows/d719b8/deploy/. Worktrees in my scratchpad /tmp/claude-1001/-home-li-primary/d719b84f-596f-53d5-a309-d47d53d60e0a/scratchpad/: system (CriomOS, branch kernel-d719b8), home (CriomOS-home), pkgs (CriomOS-pkgs). The shared /git/.../CriomOS-home checkout holds someone else's uncommitted work: leave it alone.

## Pursuing: the kernel on every host (w92o, b0wv, qvwl from Psyche core Opus; bead primary-dig9)
- nixpkgs fork LiGoldragon/nixpkgs main fast-forwarded to nixos-unstable f4a03c00: kernel 7.3.3 (hosts run 7.1.8).
- CriomOS branch kernel-d719b8, pushed, NOT on main. Its head carries: nixpkgs, microvm, sops-nix, home-manager, blueprint, rust-overlay updates; CriomOS-pkgs e1285df8 then 2f668923 (GTK backport dropped, joshuto built with vendored libgit2); llama.cpp source pin dropped (nixpkgs 0.9.0, Vulkan); gcr -> gcr_4; Home 6446a465 (old Flows retired, sema->memory repoints, noctalia HM module disabled, stylix overlays off, aspell en-computers/en-science dropped, wispr-flow-linux 7ad7804 on Electron 43).
- Running at handover: Realize of ouranos, zeus, prometheus at the branch head (background; read each result with lojix 'Query.ByDeployment.{ id }'). Prometheus had already realized at 48abebe and 2fbc069c.
- Next: when all three succeed, fast-forward CriomOS main to the branch head (git push origin <head>:main), then ActivateNow each with deploy/<host>-host-ActivateNow.datom (revs already set; re-set with sed if the head moves). Do NOT reboot. Check `readlink /nix/var/nix/profiles/system/kernel` per host. Answer Psyche core Opus w92o (Result) in one line per host: ouranos, prometheus, zeus: kernel 7.3.3 boots next; tiger, mirror-alpha: no answer; mirror-beta, vm-testing: connection closed; balboa: no DNS name.
- If a build fails: read the failing derivation's log tail in the record, fix in the owning repo, push, repin, realize again.

## Open requests
- **w92o / b0wv / qvwl:** above.
- **xw9d (herdr sound):** declared in CriomOS-home f998a000 (in Home now); Psyche core Opus silenced it by hand; the host switch above carries it. Then answer xw9d in one line.
- **l33p (updater on the Lojix watch):** fixes in CriomOS 13bd3c9 (pin override of its own Home commit; XDG_RUNTIME_DIR for notify), in the branch. After the switch, start it as root: ssh root@ouranos.goldragon.criome systemctl start --no-block harness-update; follow journalctl -u harness-update; Done l33p with lojix 321682e (0.10.6), signal-lojix 0.11.0 bd5d250, meta-signal-lojix 0.12.0 1b0aaeb and the CriomOS revision.
- fz3n answered (bh2o). Note for the next chroma switch: check that Claude Code with theme auto follows (Mode 2031 through Herdr), unverified.

## Known
- The horizon proposal /nix/store/m6ndykwgi2gwk8j64mvngyzg8g15aahy-horizon-definition can be garbage-collected; rebuild with nix build .#horizon-definition in /home/li/.cache/flow-4a42e3/goldragon (at 6490c11).
- regreet option rename warning on zeus (programs.regreet -> services.displayManager.regreet), not yet fixed.
