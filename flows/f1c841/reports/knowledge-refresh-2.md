# Knowledge refresh 2: knowledge-nexus and knowledge-flow after the night

Curriculum commit 125ee4cf2bdb on main, pushed. Generate `Generated.{ 68 24 }`, Check `Checked.{ 68 24 }` (curriculum-deploy 0.7.0, built from its main a79cf02d). Curriculum lock 11704 Released.

## knowledge-ethos

- Unchanged: ethos-zero 0edfc0c..c2653dd8 changes only tests/flow_contract.rs; README and UPGRADES are the ones the skill was written from (982929).

## knowledge-nexus

- Running set and the sockets paragraph: unchanged. Witnessed with `ps`: orchestrate-nexus 0.35.0, flow-nexus 0.17.4 and 0.12.2, message-nexus 0.17.0, message-daemon 0.14.0, lojix-nexus 8.1.0. Witnessed with `ls`: sockets under $XDG_RUNTIME_DIR/{orchestrate-nexus,flow,flow-next/flow,message-next/message,message} and /run/lojix. The installed orchestrate-meta wrapper still targets orchestrate-meta.sock.
- New: flow-nexus 0.17.4 pins signal-flow 7.0.0 and meta-signal-flow 11.0.0, and message-nexus 0.17.0 pins signal-message 8.0.0 and meta-signal-message 0.8.0, on signal 5.0.0. Witnessed in Cargo.lock at flow 14325e38 and message 0f345c29, the last commits carrying those versions.
- "orchestrate 0.36.1 ... 4.0.0 on signal 7.0.0" → orchestrate 0.37.0 on signal-orchestrate and meta-signal-orchestrate 5.0.0. Witnessed in Cargo.toml and Cargo.lock at main@origin: orchestrate c7c44cb3, signal-orchestrate 7cc50259, meta-signal-orchestrate 77afda05.
- "signal-ethos-zero ... 1.0.0 ... signal 7.0.0" → 2.0.0 on signal 8.0.0. Witnessed at signal-ethos-zero 5a6ae291 and meta-signal-ethos-zero f8fe91bb; no other repository under /git/github.com/LiGoldragon depends on them.
- "flow 0.18.0 pins signal-flow 7.0.0 ... message 0.17.1 ..." → flow 0.22.0 (signal-flow 10.0.0, meta-signal-flow 14.0.0) and message 0.19.0 (signal-message 10.0.0, meta-signal-message 0.10.0), with lojix 9.0.0 (signal-lojix 7.0.0, meta-signal-lojix 8.0.0, horizon-lib 0.14.0). Witnessed in the main@origin locks: flow 2fa51db8, message ce3eb6c6, signal-flow f95034de, meta-signal-flow 54eb5618, signal-message b94d907c, meta-signal-message 81e12b23, lojix 0eed57fe, signal-lojix 0a83f2d6, meta-signal-lojix 25f7f220.
- "no running Nexus speaks signal 7.0.0" → every main shares signal 8.0.0, and `links = "signal"` admits one signal per graph. Witnessed: signal f35460de Cargo.toml line 10, and each lock above holds a single signal 8.0.0.
- "ethos-zero 13.0.0 and protos 0.31.0 ... only the ethos-zero contracts on 15.0.0" → all mains generate with ethos-zero 16.0.0 on protos and datom-codec 0.32.2. Witnessed: the same locks; ethos-zero c2653dd8 is 16.0.0.
- sema-engine: flow and message pin 0.16.0 (unchanged); orchestrate pins 0.17.0; main is 0.18.0 (9884905f). New: lojix pins 0.15.1 and signal-frame 0.3.1. Witnessed in the locks and in lojix Cargo.toml (sema-engine rev 27e814a7).
- live_nexus.rs line: still at crates/orchestrate-nexus/tests/live_nexus.rs on main. Added the test repositories' scenarios beside it. orchestrate-test b8e2b971 pins orchestrate c7c44cb3, orchestrate-previous bc5cd36e and orchestrate-live 9070cbb8, with seven checks; see its README and checks/. flow-test 36c8d2ca pins flow 2fa51db8 and harness 8604a073, with the pure checks flow and flow-populated-store and the gated runners flow-claude and flow-claude-hook. Witnessed in flake.lock and README.md of each.
- New: CriomOS-home `f1c841-orchestrate-0.37` 61abe3fb. Its parent is `3ec648-orchestrate-0.36` feebd281, which carries the caller-set ORCHESTRATE_SOCKET/ORCHESTRATE_META_SOCKET wrapper change (seen in its diff), and that parent's parent is main 0025894f. Witnessed: the bookmarks, both generations (/nix/store/qda5pkid…, rn8fzfbw…) and /nix/store/kjs1zikz…-orchestrate-0.37.0 exist on the host. The home-manager profile is still home-manager-1039-link, and the installed orchestrate is still 0.35.0.

## knowledge-flow

- "There is no Flow Nexus yet. A flow claims its identity itself" → "A hand-started seat claims its identity itself". Witnessed: the flow-id usage line of installed harness 0.3.4 is unchanged, and two flow-nexus processes are running.
- "No harness hook calls any Flow component" → "No installed harness hook". Witnessed: ~/.claude/settings.json has only the herdr-agent-state.sh hook, and the running flow 0.17.4 and 0.12.2 packages have no flow-hook binary. Added one sentence, marked not deployed, on what flow main 0.22.0 carries: FlowId reserved before Spawn, FLOW_ID exported to the pane, `--session-id` chosen by Flow, flow-hook in the launch's `--settings` on SessionStart/PostToolUse/Stop, and Report appended to events in Memory. Witnessed in flow 2fa51db8 UPGRADES.md (0.22.0, 0.21.0), crates/flow/Cargo.toml `[[bin]] flow-hook`, and crates/flow-nexus/src/herdr/launch.rs.
- "The only running Nexus is orchestrate" → removed. It is false, since `ps` shows four Nexus kinds, and the running set has its home in knowledge-nexus.
- Semi-sandbox script flows/3ec648/witnesses/semi-sandbox-capsule.sh → flow-test's gated runner `flow-claude-hook`. Its parts: a short mktemp /tmp root (108-byte sun_path), HOME/XDG/TMPDIR inside it, credentials file alone, its own Flow Nexus on a fresh store with a fixture Herdr, and a cheapest-model `claude -p` in a 2G scope for 300 s and 4 turns. Witnessed in flow-test 36c8d2ca packages/flow-claude-hook.nix.
- Descriptions are unchanged. knowledge-flow's "before Flow the Nexus exists" is now loose, because Flow Nexus processes run; they launch no seat, though, so it was left.

## Sources

- Host: `ps -eo pid,lstart,args`; `ls -la` of the socket directories; `readlink -f` of orchestrate, orchestrate-meta, claude, flow, flow-id, hm-send; the orchestrate-meta and claude wrapper scripts; ~/.claude/settings.json; ~/.local/state/nix/profiles/home-manager.
- Repositories after `jj git fetch`, at main@origin: Cargo.toml and Cargo.lock of every repository named above; flow UPGRADES.md and src; orchestrate-test and flow-test README.md, flake.lock and packages/flow-claude-hook.nix; ethos-zero `jj diff --from 0edfc0c --to c2653dd8`; CriomOS-home bookmarks and the diffs of feebd281 and 61abe3fb.
- flows/f1c841/reports/morning-deploy-orchestrate-037.md, used for the store path names only; each one was checked on the host.
