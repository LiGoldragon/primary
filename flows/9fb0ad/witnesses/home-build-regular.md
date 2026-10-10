# Witness: f1c841-home-build-regular.service end (2026-10-03)

Method: at 06:49 the unit was active (started 06:43:57). I waited by event, not by loop: a foreground `tail --pid=2819701 -f /dev/null` (blocks until the unit's main sh exits), plus one background `journalctl --user -f | grep -m1` for the end line (it never matched: the journal's end line for a successful transient unit is only the "Consumed ..." line; I stopped waiting on it). No sleep-and-check loop. Observed at 06:53:01-06:53:15 CST. Nothing changed, activated or released by me.

## Unit
- Result=success, ExecMainStatus=0, ActiveState=inactive, unit gone. Ended 06:53:00 after 9m03s wall, 2m41s CPU, 3.9G peak.
- Journal (only two lines): `06:43:57 Started [systemd-run] sh -c "nix build ... activationPackage ... && nix build ... checks flow-message herdr-agent-executable ..."` and `06:53:00 Consumed 2min 41.841s CPU time over 9min 3.027s wall clock time, 3.9G memory peak.`
- Build log tail: home-manager-files and home-manager-generation built on prometheus and copied back; out-link `scratchpad/home-regular -> /nix/store/1rj6l1lnizjnkjivjmrmwwbnhlkgjd34-home-manager-generation` (06:50). Check log tail: flow-message check printed message-clients paths and was copied; out-links check-flow-message -> ...-flow-message, check-flow-message-1 -> ...-herdr-agent-executable-contract (06:53). Both builds exited 0 (the && chain completed).

## Home-manager
- No new generation. Profile still ends at home-manager-1039-link (09:53 Sep 30); gcroots current-home = new-home = xp12f872...-home-manager-generation (1039). Active = 1039. The built generation 1rj6l1lnizj... is not in the profile.

## Running set (ps, 06:53)
- orchestrate-nexus 0.35.0 pid 1944, up 6d14h: not restarted.
- message-daemon 0.14.0 (13885), message-nexus 0.17.0 (90762), lojix-nexus 8.1.0 (63865), flow-nexus 0.17.4 and 0.12.2 (1965133/1965136): all unchanged.
- f1c841 claude pid 2081112 alive.

## Locks (Observe.Locks, 06:53:15)
- 11723 HomeRegular f1c841 [regular-f1c841 worktree] "Make orchestrate 0.37, flow 0.23, message 0.19 the regular Home versions": STILL HELD.
- 11738 PrimaryPublish f1c841: NO LONGER present (released, by f1c841 presumably).
- 11766 PrimaryPublish 5578cc [/home/li/primary/.PrimaryPublish.lock] "Publish flows/5578cc/log.md": held by Opus 5578cc.

## Commit 9497e4fb
- Gained bookmark `f1c841-regular` (jj op log: created 06:53:14, "push bookmark f1c841-regular to git remote origin" 06:53:16, i.e. seconds after the unit ended). Pushed: `f1c841-regular@origin` = 9497e4fb. Based on 4b863bb5 (f1c841-flow-message-next). main is still 0025894f; not merged.

## flows/f1c841/reports/deployment.md
- mtime 06:44:38.48 (-0600), 4557 bytes, last heading "## The regular-slot commit (CriomOS-home 9497e4fb, on 4b863bb5)". Unchanged since 06:44:38.
