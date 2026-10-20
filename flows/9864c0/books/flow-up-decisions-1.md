<!-- to-the-living:start -->
Presentation.{ «Flow Up: Decisions» }

# Flow Up: Decisions

### Proposal 1: Activate Field's package and stop the other deploy · primary › docs/flow-up.md, a new file

**Comment** Each proposal is one entry of a single new record of the Flow bring-up, in the order the decisions were made. "Corner" means a shortcut taken because you ordered it working now; it names the landing that is still owed. A Type is written with a capital and an example value, as in Layer (Tertiary).

+ Flow Up: the decisions made while bringing the new Flow Nexus up.
+
+ Activation. Two deploys were racing: aa034f's, which declared only the Nexus, and Field's, which declared the Nexus, the twelve-row Models table, the SendServers and the LeaveOuts. The deploy of aa034f was stopped before it changed anything, and Field's package (Flow 0.35.21, Message 0.20.0) was activated by hand.
+ - Why: with only the Nexus declared, every Mind and Field start would be refused as ModelRefused.Unconfigured, and the rest would have been lost on restart.
+ - Corner: Field's own message test and its backup steps were skipped; no home-manager switch ran, so the units and the command links are placed by hand. Landing owed: a Home switch that carries them.
+ - Accepted consequence: every flow running before today is unknown to the new store (Current.Unknown), and old 0.35.11 sessions have their hook calls dropped until each is relaunched.
+ - Way back: flows/4201a3/rollback-20261019.txt relinks the two old units and removes the links.

Ruling: land, amend, or reject.

### Proposal 2: Sol is gpt-6.1-sol · primary › docs/flow-up.md

+ Sol model. Mind and Field Secondary use Model gpt-6.1-sol in both Configure.Models rows.
+ - Why: the endpoint serves both gpt-6-sol and gpt-6.1-sol; the newer one is what the Mind and Field launch declarations already name, and five Mind Secondaries launched on it and answered.
+ - Corner: examples in the docs and tests still say gpt-6-sol. Landing owed: edit the examples.

Ruling: land, amend, or reject.

### Proposal 3: Repair the messenger's Held message · primary › docs/flow-up.md

+ Held reason. A send to a seat whose route is Held, for example Held.{ 42265e Blocked attempt-337b95 }, showed the wrong error (RuntimeBindingOrStore) because the pattern for the attempt name did not accept a hyphenated name. The pattern was widened so the sender sees Held.
+ - Why: the real fault was a blocked pane, not the store; the wrong name hid it.
+ - Corner: pushed to messenger-clj (b86a0b), tests pass locally, but the running messenger gets it only through the overlay of decision 8. Landing owed: a deploy of the repository.

Ruling: land, amend, or reject.

### Proposal 4: One command starts a flow, read on the client · primary › docs/flow-up.md

+ Start command. `flow-start <Aspect> <Topic> <Layer>`, for example `flow-start Mind core Tertiary`, with optional `-p <Predecessor>` (example 68db51), `-n` to print the request only, and a task. A small node program reads the existing seat, voice and module declarations in config/main-flow, builds the Start request, submits it to the Nexus, registers the route and writes the continuation record.
+ - Why: it was the minimal shape that works now. The alternative, teaching the Nexus to accept `Start.{ Psyche core Secondary }` and read the declarations itself, is a change of the Rust program and its contract, and takes hours.
+ - Corner: the client reads the declarations, not the daemon; the program lives in ~/.local/bin, outside any repository, without tests. Landing owed: gap 1 and gap 2 of the last section.

Ruling: land, amend, or reject.

### Proposal 5: Prove it by starting the missing Psyche core Secondary · primary › docs/flow-up.md

+ First real start. The test of flow-start was the flow that was actually missing: `flow-start Psyche core Secondary -p 68db51` (Model claude-opus-5-5, effort medium), answered by Flow as Awake.9864c0.
+ - Why: a missing flow is started through Flow, and a throwaway flow would spend a seat nobody needs and leave a stray address.
+ - Corner: none.

Ruling: land, amend, or reject.

### Proposal 6: A stand-in for the empty Herdr reply · primary › docs/flow-up.md

+ Herdr shim. Herdr 0.8.2 answers `pane report-metadata` with nothing, and the Nexus read that as JSON, so every start ended in StartRejected.NativeLaunchRefused.{ Naming PaneLabelRefused } and the seat was stopped. A shim first on the Nexus path prints `{}` for that one empty reply and passes everything else through.
+ - Why: it worked in minutes. The proper fix is in Flow's source.
+ - Corner: the fix exists on branch 4201a3-report-metadata (647689, on Flow dcb63e), not built or tested on Prometheus, not deployed. Landing owed: build, test, deploy, then remove the shim.

Ruling: land, amend, or reject.

### Proposal 7: Move the Psyche core Secondary route by force · primary › docs/flow-up.md

+ Route re-key. The route "Psyche core Secondary" pointed at 5dd7e5, whose pane was gone, so the normal retire refused (PaneNotFound). The old seat was retired with the messenger's own store functions, evidence kept in the retirement-evidence folder, and the route registered to 9864c0.
+ - Why: waiting for the messenger's owner would have kept the new seat unreachable.
+ - Corner: the live-pane safety check was bypassed for a pane proven gone. Landing owed: a retire that accepts a proven-gone pane.

Ruling: land, amend, or reject.

### Proposal 8: Older flows may send through the messenger's own route · primary › docs/flow-up.md

+ Unidentified senders. A fresh Flow store does not know the flows born before it, so Message refuses their sends (MessageRefused Unidentified). An overlay placed ahead of the messenger jar delivers on the messenger's own live registration instead, and the hm-* commands are copies that use that overlay.
+ - Why: relaunching every flow would have killed work in flight, and no query exists to adopt them into the new store.
+ - Corner: the overlay is outside messenger-clj; the next Home switch replaces the wrappers and drops it. Landing owed: carry the fallback in the repository.

Ruling: land, amend, or reject.

### Proposal 9: Reach a sleeping seat by binding the sender's Address · primary › docs/flow-up.md

+ Sender relay. A seat that sleeps has no pane; the only way in is Message, then the Flow queue, then wake, and that needs a sender Flow knows. A small relay replays the sender's Bind request on its own connection, with the sender's Address from hm-list, then runs the send as its child. A bound relay Address (Current.Awake.flow-2, say) is treated as unmanaged, so sends to it use the pane route.
+ - Why: patching Message or Flow identity needs a rebuild and a redeploy; typing into panes was refused.
+ - Corner: each relayed send leaves the sender Address Awake as a new flow-N bound to a dead process, and Flow trusts the bind without proof that the caller is that flow. Not in any repository. Landing owed: an identity route in Flow, then removal of the relay.

Ruling: land, amend, or reject.

### Proposal 10: Core means Psyche, Mind and Field; start only what is missing · primary › docs/flow-up.md

+ Roster. "Main aspects" for Primaries and Tertiaries is read as Aspect Psyche, Mind and Field, each on Topic core, so nine seats: Psyche core Primary, Secondary, Tertiary, and the same for Mind and Field. Only Mind core Tertiary and Field core Tertiary were missing; they got declarations (config/main-flow/metaflow/Mind-Core-Tertiary.edn, Field-Core-Tertiary.edn, copied from the neighbours, voice gpt-6-luna medium) and were started: 6f2dce and 4a16cc.
+ - Why: the seats already live answered and were reachable, so restarting them would only spend context.
+ - Corner: the two declaration files are not committed, no tests, no review. Landing owed: commit by the Primary committer.

Ruling: land, amend, or reject.

### Proposal 11: Keep a live seat; replace it only when it is dead or full · primary › docs/flow-up.md

+ Keep rule. Psyche core Primary stays Fable 39bd0c while its context is under the refresh threshold (15% or 100,000 tokens; it stood near 10%); a fresh Fable successor starts only above it. Field core Secondary 42265e is kept while its pane is live, replaced only if dead.
+ - Why: a second expensive flow in one role needs an explicit ruling, and a live seat holds the work.
+ - Corner: none.

Ruling: land, amend, or reject.

### Proposal 12: A failed start is fixed in its repository, then retried · primary › docs/flow-up.md

+ Repair rule. When a start fails, a small fix goes into Flow or the messenger, is committed in that repository, and the start is retried. A large fix goes to a flow that owns it.
+ - Why: the order was a working system now, and a workaround that stays outside a repository is lost.
+ - Corner: decisions 6, 8 and 9 are the cases where the fix was not yet in the repository.

Ruling: land, amend, or reject.

### Proposal 13: Flow implementation goes to Mind, its decisions to Fable · primary › docs/flow-up.md

+ Routing. Flow implementation goes to Mind core Secondary (Flow 41fa34) with the gap list; a decision inside that work goes to Psyche core Primary (Fable 39bd0c).
+ - Why: Mind implements what Psyche sees.
+ - Corner: none.

Ruling: land, amend, or reject.

### Proposal 14: What now works, and what is left · primary › docs/flow-up.md

+ Works. One command starts a flow: `flow-start <Aspect> <Topic> <Layer>`, for example `flow-start Mind core Tertiary`. Nine core seats are live. Messages reach them, sleeping seats included.
+
+ Left, each one line:
+ - Gap 1, large: the Nexus composes a start from `Start.{ Psyche core Secondary }` itself, with seats, voices and modules in a typed Configure store in Flow.
+ - Gap 2, small to medium: flow-start moves into a repository, deployed by CriomOS-home, with the Primary paths as skill variables.
+ - Gap 3, medium: subagent role transport, a tmpfs agents directory from book to illustrator; the ComposeRole branch is not installable.
+ - Gap 4, medium: integrate the branches sleep 0.35.22, rules and compose-role, which are claimed to conflict.
+ - Gap 5, medium: deploy hygiene, meaning the profile on old links, the hand-made links, and the Home Nexus unit and messenger pin not yet activated.
+ - Gap 6, small: a start with -p into a cell whose predecessor is still registered fails after opening a pane and leaves an unregistered orphan; the launcher must check registration first.
+ - Defect: the Herdr empty reply is only shimmed (decision 6).
+ - Defect: 0.35.11 sessions have their hooks dropped.
+ - Defect: the Held fix and the relay live in the overlay only (decisions 3, 8, 9).
+ - Defect: there is no Wake query.
+ - Defect: the NotResumable stop of 6f2dce and 4a16cc is not investigated.
+ - Defect: hm-list shows Psyche core Secondary 9864c0 as STALE after its pane moved, cause unknown.

```text
+----------------------------------+
| person                           |
+----------------------------------+
        |
        | types
        v
+----------------------------------+
| flow-start Mind core Tertiary    |
+----------------------------------+
        |
        | reads config of
        v
+----------------------------------+
| config/main-flow declarations    |
+----------------------------------+
        |
        | builds and submits Start
        v
+----------------------------------+
| flow-nexus                       |
+----------------------------------+
        |
        | opens
        v
+----------------------------------+
| Herdr pane                       |
+----------------------------------+
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
