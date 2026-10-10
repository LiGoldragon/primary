# Stable Flow override and clients — facts gathered read-only

Gathered by a read-only companion subflow of main flow 8904b1
(`PsycheV2.{ Fable 8904b1 }`), whose harness forbade file writes; its
findings existed only as the final assistant message of its transcript.
Saved here, verbatim in substance, by a second 8904b1 subflow on
2026-09-26, by extracting that final message mechanically from the
transcript JSONL (undoing only the JSON string escaping the transport
applied — no retyping, no paraphrase, no reordering).

The saved body below is the full final `SubflowReturn` datom the
companion returned, unchanged except for that unescaping.

---

```
SubflowReturn.{
  Request «Check the facts behind the third route: move Home's stable Flow pin back to 0.12.2's source and leave the external drop-in alone.»
  Findings «
Observed (O), Inferred (I) and Unknown (U) are marked. Nothing was built, evaluated, activated or edited. I ran `--version` on the 0.12.2 and 0.14.0 flow-nexus binaries and one `flow 'List.{}'` through the installed client, which resolved to 0.12.2.

1. What runs now
- O: `systemctl --user show flow-nexus` reports ExecStart = /nix/store/c044v5pa2qh4xcjkbiqiqb9qax6l36bd-flow-0.12.2/bin/flow-nexus. /proc/1937/exe is the same path, and it answers `flow-nexus 0.12.2`. The service has been running since the reboot at 2026-09-26 16:19:37.
- O: the source is Flow commit 34aaf7875af1, whose Cargo.toml says 0.12.2. Its deriver is 0bh3gvqf…-flow-0.12.2.drv. The only things in the store that refer to the output are `nix profile` generations; no Home generation does.
- O: the drop-in is /home/li/.config/systemd/user/flow-nexus.service.d/override.conf. It is an ordinary file, not a link, mode 0600, one hard link, owner li, modified 2026-09-25 20:52:09. It contains `[Service]`, then `ExecStart=`, then `ExecStart=/nix/store/c044v5…-flow-0.12.2/bin/flow-nexus`. Its directory was created at 19:03:34 the same day.
- Who made it, as the records claim: e51411's message to b7da5d says an e51411 Luna subflow set up a "reversible drop-in" for 0.10.5. U: who rewrote it to 0.12.2 at 20:52. The transcripts I searched do not show the write.

2. The live generation
- O: home-manager generation 1033 is wz9f16mh…. It is also the generation /run/current-system's home-manager-li unit names. Its stable unit says flow-0.14.0 (j689l77b…), next says flow-0.17.1, and the stable Message daemon is message-0.14.0. The generation has no flow-nexus.service.d.
- I: it was built from Home fed50084, locked by CriomOS d04257a (17:00). Evidence: next Flow is 0.17.1 and messenger-clj is 0.2.5, which fits fed50084 and nothing later.
- So the drop-in is doing real work today. Without it, stable would run 0.14.0.
- O: the 0.14.0 stable unit was already in the generation activated at 09:24 (lojix deployment 38). That activation stopped and started flow-nexus with the drop-in in place. The drop-in then survived activations at 09:24, 17:17 and 17:38.

3. History of the stable pin
- O: Home commit 8a60835c (2026-09-26 00:26, author "li", no flow ID in the message) is titled "Pin Flow 0.14.0 (9fcd625a) and message 0.14.0 (930c5169); flow-service-path expects the new rev". It gives no reason beyond the title.
- O: in the same step it moved stable Message from 8aa6d7b4 (0.12.0, signal-flow 2.0.0) to 930c5169 (0.14.0, signal-flow 6.2.0), and changed the expected revision in checks/flow-service-path.
- O: Flow 0.12.2 speaks signal-flow 5.1.0. Message 0.14.0 sends raw rkyv `FlowQuery::ResolveRecipient`. It has been running (pid 13885) against Flow 0.12.2 since 16:31.
- I: it works because the only change between the signal-flow versions 0.12.2 and 0.14.0 use is two new variants at the end of `FlowLifecycle` (Retired, Exited). An older service never sends those. The Message journal since boot shows only unit start failures at 16:19 and no decode error in what I filtered.

4. The client on the path
- O: both the live and the candidate generation (8fx6k2w4…) put the 0.14.0 `flow`, `flow-meta` and `flow-nexus` into home-manager-path.
- O: that is not what runs. The user's ~/.nix-profile manifest has a separate, undeclared element `flow` = c044v5…-0.12.2 at priority 4, which beats home-manager-path at priority 5. `which -a flow` therefore finds only 0.12.2. /etc/profiles/per-user has no flow.
- O: the ordinary request vocabulary (`Query`) is identical in signal-flow 5.1.0 and 6.2.0. The meta wire (6.0.4 to 8.0.2) only adds `Retire` and two replies at the end.
- I: a 0.14.0 client sends byte-identical requests to 0.12.2 and can decode every reply. The one exception is a 0.14.0 meta `RegisterFlow` carrying Retired or Exited.
- O: the garbled reply this flow saw from 0.17.4 is explained by signal-flow 7.0.0, which removes `Send` from `Query`. A 0.17.x `List` is then variant 4, which on 0.12.2 is `Stop`.

5. Can the route be built
- O: 34aaf787 is on origin/main of Flow.
- O: Flow 34aaf787's own lock pins crane eb35abda, fenix f8ac2cd5 and nixpkgs 0e251e24. Those equal Home's crane_4 and fenix_5 nodes at 5f14f9da, and Home's nixpkgs (0e251e24) on every revision since.
- O: the 0.12.2 and 0.14.0 derivations share the same stdenv-linux.drv.
- I: Home repinned to 34aaf787 should give exactly c044v5…, which is already in the store, so Flow itself would not need building. The Home generation (and the system through lojix) still needs one build.
- O: Home's modules/home/profiles/min/flow.nix has not changed since 4a9d85d7, the commit that integrated Home with Flow 0.12.2. 0.12.2 reads FLOW_SOURCE_ROOT and FLOW_CODEX_*.
- U: I did not evaluate, so it is not proven that Home evaluates at that pin.

6. The drop-in under each outcome
- O: neither generation links anything into flow-nexus.service.d.
- O: home-manager's orphan cleanup only deletes links that point into an earlier generation (the 09:24 log shows it skipping other paths), and checkLinkTargets checks only declared targets.
- I: activation leaves the file alone. Three activations have confirmed this.
- I (systemd semantics): with the drop-in, `ExecStart=` clears the base and then c044v5 is set. Without it, the base ExecStart applies. With a base of c044v5, both give 0.12.2, and the same store path.

7. Cost of moving the pin back
- In Home: flake.nix/flake.lock `flow`; the expected revisions in checks/flow-service-path and checks/flow-message-next (`expected.stableFlow`); and the UPGRADES text that says "stable Flow 0.14.0". The only other user of the stable package is `stablePackage` in flow-message-next.nix, which supplies the stable clients.
- Stable Message should stay at 0.14.0, because moving it back to 0.12.0 would bring back a mismatch.
- Nothing I found depends on 0.14.0 behaviour (List writing nothing, Start answering Started, Retire).
- Side effect: once the pin is back, the nix-profile `flow` element can be retired later without the client changing.

My judgment: sound, on three conditions.
(a) Home must lock Flow 34aaf787 with its own crane, fenix and nixpkgs, so the output stays c044v5. Build or dry-run first to confirm no Flow rebuild is needed.
(b) Both checks and the UPGRADES text must move together with the pin.
(c) The design must count the second undeclared external artifact: the priority-4 nix-profile `flow` element. The route does not rely on it.
The route removes the drop-in from the correctness path altogether.

Hazard of a client speaking across versions:
- 0.14.0 client to 0.12.2 service: not real today, because the profile element shadows the 0.14.0 client. If that element went, I judge it still low risk: the wire is compatible, though this is inferred and not witnessed.
- Any 0.17.x client to a 0.12.2 socket: real and dangerous, because List decodes as Stop.

Unknowns: who rewrote the drop-in to 0.12.2; which Home revision the live generation came from (inferred, not read from provenance); whether Home evaluates at the pin; whether the path is exactly the same without evaluating; why the stable unit that said 0.14.0 was not restarted at 17:38 (the unit was probably unchanged since 09:24, not checked).

Not reached: the Codex session transcripts; the lock content of CriomOS d04257a beyond the one search; the effects of Message 0.14.0 on 0.12.2 beyond wire types.

No report file was written, because the harness forbids report files.»
  Sent Nothing
  Next Act.«Decide the route with its three conditions, and weigh the undeclared nix-profile `flow` element (priority 4) as a second external artifact to be retired once the pin is back.»
}
```

## Comparison

The body above was compared against the mechanically extracted final
assistant-message text (from the transcript JSONL, decoded only for
JSON string escaping). Apart from this head and this comparison note,
the saved body is identical to the extracted message: same content,
same order, same markers (O/I/U), same judgment language attributed to
the companion itself, same "Not reached" list.

## Sources

- Companion transcript (final assistant message, this flow's own
  extraction): `/tmp/claude-1001/-home-li-wt-primary-56ae53/8904b10d-7f06-4e44-9342-3a8a2d7e17bd/tasks/a6a4a003b61ad2630.output`
