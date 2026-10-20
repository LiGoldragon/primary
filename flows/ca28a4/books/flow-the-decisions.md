<!-- to-the-living:start -->
Presentation.{ «Flow, the decisions» }

# Flow, the decisions

### Proposal 1: Field's package is the active Flow · primary › docs/flow-up.md, a new file

**Comment** One record, docs/flow-up.md, holds the decisions of the Flow Nexus bring-up, one entry per proposal, each as it now stands. "Corner" is a shortcut taken, with the landing still owed. A Type is written with a capital and an example value, as in Layer (Tertiary).

+ Flow Up: the decisions made while bringing the new Flow Nexus up.
+
+ Activation. Field's package (Flow 0.35.21, Message 0.20.0) is the active Flow. It declares the Nexus, the twelve-row Models table, the SendServers and the LeaveOuts on a new store. The deploy of aa034f, which declared only the Nexus, is stopped before it changes anything. The command links in ~/.local/bin and the unit links are placed by hand, and the Flow 0.35.11 store stays untouched.
+ - Why: with only the Nexus declared, every Mind and Field start is refused as ModelRefused.Unconfigured, and the rest is lost on restart.
+ - Corner: Field's message test and its backup steps are skipped; no home-manager switch ran. Landing owed: a Home switch that carries the units and links.
+ - Accepted consequence: every flow running before today is unknown to the new store (Current.Unknown), and old 0.35.11 sessions have their hook calls dropped until each is relaunched.
+ - Way back: flows/4201a3/rollback-20261019.txt relinks the two old units and removes the links.

Ruling: land, amend, or reject.

### Proposal 2: Sol is gpt-6.1-sol · primary › docs/flow-up.md

+ Sol model. Mind and Field Secondary use Model gpt-6.1-sol in both Configure.Models rows.
+ - Why: the endpoint serves both gpt-6-sol and gpt-6.1-sol; the newer one is what the Mind and Field launch declarations name, and five Mind Secondaries launched on it and answered.
+ - Corner: examples in the docs and tests still say gpt-6-sol. Landing owed: edit the examples.

Ruling: land, amend, or reject.

### Proposal 3: A held message is reported as Held · primary › docs/flow-up.md

+ Held reason. A send to a seat whose route is Held, for example Held.{ 42265e Blocked attempt-337b95 }, is reported to the sender as Held with its id, never as RuntimeBindingOrStore. The attempt-name pattern accepts a hyphenated name.
+ - Why: the real fault was a blocked pane, not the store; the wrong name hid it.
+ - Corner: the fix is pushed to messenger-clj (b86a0b) and tests pass locally; the running messenger gets it only through the overlay of Proposal 10. Landing owed: a deploy of the repository.

Ruling: land, amend, or reject.

### Proposal 4: One command starts a flow · primary › docs/flow-up.md

+ Start command. `flow-start <Aspect> <Topic> <Layer>`, for example `flow-start Mind core Tertiary`, with optional `-p <Predecessor>` (example 68db51), `-n` to print the request only, and a task. A small node program reads the seat, voice and module declarations in config/main-flow, builds the Start request, submits it to the Nexus, registers the route and writes the continuation record.
+ - Why: it is the minimal shape that works now. Teaching the Nexus to read the declarations is Proposal 5.
+ - Corner: the client reads the declarations, not the daemon; the program lives in ~/.local/bin, outside any repository, without tests. Landing owed: Proposals 5 and 6.

Ruling: land, amend, or reject.

### Proposal 5: The daemon composes a start · primary › docs/flow-up.md

+ Composed start. The Nexus composes a flow from `Start.{ Psyche core Secondary }`, with seat, voice and module declarations in a typed Configure store it loads. The client sends Start and nothing else. It lands in the flow repository as the next increment after Proposal 6, not as a gate on it; signal-flow and meta-signal-flow carry only the Configure and Start types.
+ - Why: the client reading declarations (Proposal 4) is the shortcut; the declarations belong to the daemon.
+ - Corner: none for the ruling; until it lands, flow-start reads the declarations.

```text
+----------------------------------+
| flow-start                       |
+----------------------------------+
        |
        | sends Start to
        v
+----------------------------------+
| flow-nexus                       |
+----------------------------------+
        |
        | reads
        v
+----------------------------------+
| typed Configure store            |
+----------------------------------+
        |
        | opens
        v
+----------------------------------+
| Herdr pane                       |
+----------------------------------+
```

Ruling: land, amend, or reject.

### Proposal 6: Running first, redesign second · primary › docs/flow-up.md

+ Order of work. What starts a flow today (flow-start into flow-nexus 0.35.21) is deployed as it is, this day. flow-start moves into the flow repository, versioned and deployed by CriomOS-home; the Home flow-nexus unit and the messenger repin are activated; the hand-made links in ~/.local/bin are removed; the /home/li/primary paths become skill variables. This is one piece of work.
+ - Why: Our reading: the order was a working system now, and the redesign must not hold it back.
+ - Corner: until the Home switch runs, the hand-made links and the pin stay. Landing owed: that Home switch.

Ruling: land, amend, or reject.

### Proposal 7: The first real start is the missing Psyche core Secondary · primary › docs/flow-up.md

+ First real start. The test of flow-start is the flow that is actually missing: `flow-start Psyche core Secondary -p 68db51` (Model claude-opus-5-5, effort medium), answered by Flow as Awake.9864c0.
+ - Why: a missing flow is started through Flow, and a throwaway flow would spend a seat nobody needs and leave a stray address.
+ - Corner: none.

Ruling: land, amend, or reject.

### Proposal 8: A stand-in answers the empty Herdr reply · primary › docs/flow-up.md

+ Herdr shim. Herdr 0.8.2 answers `pane report-metadata` with nothing. The Nexus treats that empty reply as no metadata. Until the Flow build carrying that is deployed, a shim first on the Nexus path prints `{}` for that one empty reply and passes everything else through.
+ - Why: read as JSON, the empty reply ends every start in StartRejected.NativeLaunchRefused.{ Naming PaneLabelRefused } and stops the seat. The shim works in minutes.
+ - Corner: the fix exists on branch 4201a3-report-metadata (647689, on Flow dcb63e), not built or tested on Prometheus, not deployed. Landing owed: build, test, deploy, then remove the shim.

Ruling: land, amend, or reject.

### Proposal 9: A retire accepts a pane proven gone · primary › docs/flow-up.md

+ Route re-key. When a route points at a seat whose pane is proven gone, the normal retire refuses (PaneNotFound). The old seat is then retired with the messenger's own store functions, evidence kept in the retirement-evidence folder, and the route registered to the successor. Example: the route "Psyche core Secondary" moved from 5dd7e5 to ca28a4.
+ - Why: waiting for the messenger's owner would keep the new seat unreachable.
+ - Corner: the live-pane safety check is bypassed for a pane proven gone. Landing owed: a retire that accepts a proven-gone pane.

Ruling: land, amend, or reject.

### Proposal 10: Older flows send through the messenger's own route · primary › docs/flow-up.md

+ Unidentified senders. A fresh Flow store does not know the flows born before it, so Message refuses their sends (MessageRefused Unidentified). An overlay placed ahead of the messenger jar delivers on the messenger's own live registration instead, and the hm-* commands are copies that use that overlay.
+ - Why: relaunching every flow would kill work in flight, and no query exists to adopt them into the new store.
+ - Corner: the overlay is outside messenger-clj; the next Home switch replaces the wrappers and drops it. Landing owed: carry the fallback in the repository.

Ruling: land, amend, or reject.

### Proposal 11: A sleeping seat is reached through a sender relay · primary › docs/flow-up.md

+ Sender relay. A seat that sleeps after its turn has no pane; the only way in is Message, then the Flow queue, then wake, and that needs a sender Flow knows. A small relay replays the sender's Bind request on its own connection, with the sender's Address from hm-list, then runs the send as its child. A bound relay Address (Current.Awake.flow-2, say) is treated as unmanaged, so sends to it use the pane route. The relay binds the sender whenever the awake flow has no live process, not only when the sender is Unknown. A Wake query is added to Flow, and a relay version.
+ - Why: no Wake query exists in 0.35.21; patching Message or Flow identity needs a rebuild and a redeploy; typing into panes is refused.
+ - Corner: each relayed send leaves the sender Address Awake as a new flow-N bound to a dead process, and Flow trusts the bind without proof that the caller is that flow. Not in any repository. Landing owed: an identity route in Flow, the Wake query, then removal of the relay.

```text
+----------------------------------+
| sender hm-send                   |
+----------------------------------+
        |
        | passes through
        v
+----------------------------------+
| relay                            |
+----------------------------------+
        |
        | binds Address when no
        | live process holds it
        v
+----------------------------------+
| Flow                             |
+----------------------------------+
        |
        | delivers, or reports Held
        v
+----------------------------------+
| target seat                      |
+----------------------------------+
```

Ruling: land, amend, or reject.

### Proposal 12: A dead flow's Flow address goes to the live one · primary › docs/flow-up.md

+ Address taking. A Flow address held Awake by a flow with no live process is taken by the live process that claims it. Example: 39bd0c bound Psyche core Primary over b3fcde, an empty directory with no process.
+ - Why: Our reading: the binding of the Psyche core Primary had to return to the flow that is alive.
+ - Corner: Flow trusts the claim without proof that the caller is that flow (see Proposal 11). Landing owed: an identity route in Flow.

Ruling: land, amend, or reject.

### Proposal 13: Core means Psyche, Mind and Field; keep a live seat, start only what is missing · primary › docs/flow-up.md

+ Roster. Primaries and Tertiaries of the main aspects are Aspect Psyche, Mind and Field, each on Topic core: nine seats, Primary, Secondary and Tertiary of each. A live seat is kept: Psyche core Primary stays Fable 5ec12c while its context is under the refresh threshold (15% or 100,000 tokens; it stood near 10%), and a fresh Fable successor starts only above it; Field core Secondary 42265e is kept while its pane is live and replaced only if dead. Only Mind core Tertiary and Field core Tertiary were missing; they got declarations (config/main-flow/metaflow/Mind-Core-Tertiary.edn, Field-Core-Tertiary.edn, copied from the neighbours, voice gpt-6-luna medium) and were started: 6f2dce and 4a16cc. Their NotResumable stops are investigated after Proposals 14 to 17, not before.
+ - Why: the seats already live answered and were reachable, so restarting them would only spend context; a second expensive flow in one role needs an explicit ruling.
+ - Corner: the two declaration files are not committed, no tests, no review. Landing owed: commit by the Primary committer.

Ruling: land, amend, or reject.

### Proposal 14: Subagent roles reach the harness by files · primary › docs/flow-up.md

+ Role files. At flow start the daemon writes each composed role as an agent file into the flow's agents directory (a tmpfs is fine), from book to illustrator. The ComposeRole branch (03ec9e2) is abandoned, not repaired.
+ - Why: Our reading: files are what the harness already reads; the ComposeRole branch is not installable.
+ - Corner: none. Landing owed: the daemon writing the files.

Ruling: land, amend, or reject.

### Proposal 15: Merge order is sleep, rules, compose-role · primary › docs/flow-up.md

+ Merge order. Branch sleep 0.35.22 merges first, then rules, then compose-role. The claimed conflict between them is settled by the merge itself, not by reading. A branch that does not merge cleanly is rebased by its owner the same day.
+ - Why: the conflict rests on a claim; the merge is its test.
+ - Corner: Our reading: compose-role is abandoned by Proposal 14, so its merge may be moot. Landing owed: the merges.

Ruling: land, amend, or reject.

### Proposal 16: Registration is checked before a pane opens · primary › docs/flow-up.md

+ Pane order. A start with `-p` into a cell whose predecessor is still registered is refused before any pane opens. Registration is checked first. When the predecessor's route is stale, it is retired first (Proposal 9), then the start runs.
+ - Why: Our reading: the old order launched the seat and then failed at registration, leaving a launched, unregistered orphan pane.
+ - Corner: witnessed at 16:45 that flow-start still opened the pane before the registration step. Landing owed: the check in the launcher.

Ruling: land, amend, or reject.

### Proposal 17: Liveness is read from the pane, and a Secondary without a pane is asleep · primary › docs/flow-up.md

+ Liveness. A registry that shows STALE for a live pane is wrong; liveness is read from the pane. A Secondary whose pane is gone is asleep, not stale. The fix lands with Proposal 16.
+ - Why: hm-list showed Psyche core Secondary 9864c0 as STALE after its pane moved, and Flow showed it Asleep.
+ - Corner: nobody has witnessed the fix. Landing owed: the fix, and a witness that hm-list shows a live pane as live.

Ruling: land, amend, or reject.

### Proposal 18: A sleeping Secondary is started again through Flow · primary › docs/flow-up.md

+ Restart. Psyche core Secondary, asleep with its pane gone, is started again through Flow, `flow-start Psyche core Secondary -p 9864c0`, by the live Psyche core flow that holds the Flow order, 4201a3. The messenger's stale route is retired in the same act, by whatever means the PaneNotFound refusal needs. Result: Flow Awake.ca28a4, registered as Psyche core Secondary.
+ - Why: a Secondary with a gone pane is asleep, and the hub of the topic must answer.
+ - Corner: the retire bypassed the live-pane check for a pane proven gone (Proposal 9).

Ruling: land, amend, or reject.

### Proposal 19: The defects are fixed in source, the stand-ins removed, a failed start repaired in its repository · primary › docs/flow-up.md

+ Defect list. When a start fails, a small fix goes into Flow or the messenger, is committed in that repository, and the start is retried; a large fix goes to the flow that owns it. The empty Herdr reply is treated as no metadata, fixed in launch.rs, and the shim of Proposal 8 is removed. The messenger fix b86a0b upstreams and its overlay (Proposals 3 and 10) is removed. A Wake query and a relay version are added (Proposal 11). The NotResumable stops are investigated after the work of Proposals 14 to 17.
+ - Why: the order was a working system now, and a workaround outside a repository is lost at the next Home switch.
+ - Corner: shim, overlay and relay stay until their fixes are deployed. Landing owed: all of them.

Ruling: land, amend, or reject.

### Proposal 20: A claim is acted on as unverified · primary › docs/flow-up.md

+ Claims. Anything marked "claimed" in a gap or report is acted on as unverified: the act that lands it is its verification.
+ - Why: Our reading: waiting for proof would stop the work.
+ - Corner: none.

Ruling: land, amend, or reject.

### Proposal 21: Flow implementation goes to Mind, its decisions to Fable · primary › docs/flow-up.md

+ Routing. Flow implementation goes to Mind core Secondary (Flow 41fa34) with the gap list, flows/9864c0/flow-gap.md; a decision inside that work goes to Psyche core Primary (Fable 5ec12c).
+ - Why: Mind implements what Psyche sees.
+ - Corner: none.

Ruling: land, amend, or reject.

### Proposal 22: A stray profile removal is stopped · primary › docs/flow-up.md

+ Profile removal. A second `nix profile remove` of the Flow and messenger packages, started at 15:40 by a re-run of deploy.sh, is stopped, together with that deploy.sh. Profile generation 31 keeps flow-deployment and message-deployment; the services keep running from the Home-unit store paths, not from the profile.
+ - Why: Our reading: the removal would have taken packages the hand-made links point at.
+ - Corner: Our reading: the profile is still on old links. Landing owed: the deploy hygiene of Proposal 6.

Ruling: land, amend, or reject.

### Proposal 23: Codex starts wait for the fix before Flow is redeployed · primary › docs/flow-up.md

+ Codex start. Starts of Codex seats under Flow 0.35.21 end in HarnessSpawnRefused after Herdr's 30 s agent-start wait, because the first turn is sent before Herdr attaches the Codex TUI to the idle thread; witnessed in the code and the logs. The fix, commit bae1fcd (Flow 0.35.22, flow repository), is written and not deployed. It clashes on 0.35.22 with the branches of Proposal 15. Mind and Field flows are not restarted until it is deployed.
+ - Why: restarting a Codex seat now would only fail and spend the seat.
+ - Corner: not deployed. Landing owed: the merge of Proposal 15, then the deploy.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
