# Flow 0.53.3 cutover report (flow 1da054, 2026-11-09)

Verdict: cut over. 0.53.3 serves main since 14:37:29; 0.53.1 stopped at 14:36, its memory untouched at ~/.local/state/flow-0531/ for rollback.

## Revisions
- flow main a59869d1: candidate 2dee189e's tree whole, merged over main with main's tree discarded (main's two later commits were the Memory relocation, already in the line, and the 0.51.2 Stop-refresh test).
- CriomOS-home main 82c51f3d (flow-0533 relocked to a59869d1, same narHash as 2dee189e).
- CriomOS 2d3e3217 deployed (Lojix Realize 313 Succeeded; ActivateNow 315). CriomOS main is now 1eac5ff: the same Home pin rebased onto the Git server commits.
- psyche-belief main 626d788: flow-nexus-0533-ff3882 merged; knowledge:flow-messaging was refurnished at 15:22.
- Package /nix/store/25mdibvwd00n4yaf9w877kg3j72fls36-flow-configured-0.53.3.

## Witnessed
- Store check opened two fresh copies of the 0.53.1 store (before and after stopping 0.53.1).
- flow-nexus-0533 active, Type=notify; 25 metaflows carried by the memory, 11 Awake; HarnessHook Configured./home/li/.local/bin/flow-nexus-hook, which links into the package above.
- Energy: memory upgraded (ENXMEMRY, ENXTRNSL), both units active, old directories removed, Flow program Configured.Program.{ Flow /home/li/.local/bin/flow-nexus }.
- Restarted onto the stable hook, with each hook witnessed on its command line: 643abe 014939 663f98 ed48ef 228e2b 011913 1da054 b0c913 50e213. 6670d4 (Psyche criomos Opus) has been busy since 14:39; the script (user unit restart-claude-flows-1da054) restarts it at its next rest. 07d926 is not Claude, so it was skipped. Observe.Undecodable is empty.
- Log: flows/1da054/restart-claude-flows.log.

## What broke, and how it was carried
1. ActivateNow 315 ended Failed at reloadSystemd: `Failed to start unit systemd-tmpfiles-clean.timer: Unit is masked` (/etc/systemd/user masks it). Home's systemd.user.tmpfiles makes the switcher start that timer. Until this is fixed, every Home ActivateNow on this host ends Failed. The links, profile and units were in place.
2. The same activation's tmpfiles run had no XDG_RUNTIME_DIR, so `%t` rules were skipped and /run/user/1001/nexus/main was not made. Flow and Energy refused to start ("not a directory"). I ran the declared rules by hand (`systemd-tmpfiles --user --create` on the Home file), then reset-failed and started the units. At the next login the user manager's tmpfiles-setup makes the directory itself.
3. flow-configure-0533 failed: Home's flow-nexus-config models.datom, leave-outs.datom, harness-flags.datom and investigation.datom are still in the layer form (`{ Primary Field … }`); 0.53.3 reads a Model. The declared owner file ~/.local/state/flow-declarations/metaflows-0533.datom does not exist. I applied by hand, from outside every pane: Models in the model form (Unchanged, so the carried memory already held it), thresholds, send-servers and default-minutes (Unchanged), and HarnessHook (Replaced). Leave-outs, harness flags, investigation and metaflows stand as carried from 0.53.1. The unit stays failed until Home's files are rewritten in 0.53.3's form and the metaflows file is declared.
4. Every meta query from a flow pane is refused PeerNotAuthorized, as designed; owner queries ran through systemd-run.
5. Your HerdrRefused to me fell in my own restart window.

## Owed next
- Home: rewrite flow-nexus-config in 0.53.3's form; decide the metaflows-0533 owner file; settle the masked tmpfiles-clean timer and the tmpfiles environment under a Lojix activation. The last two belong to whoever holds CriomOS-home activation.
