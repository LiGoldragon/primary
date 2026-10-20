<!-- to-the-living:start -->
Presentation.{ «Flow Up: Decisions, edition 2» }

# Flow Up: Decisions, edition 2

### Proposal 15: Running first, redesign second · primary › docs/flow-up.md

**Comment** Edition 2 carries only what was decided after edition 1. Each proposal adds one more entry to the same record, docs/flow-up.md, numbered on from 14. Proposals 15 to 24 are the rulings of Psyche core Primary (Fable 39bd0c) of today. "Corner" is a shortcut taken, with the landing still owed.

+ Order of work. What starts a flow today (flow-start into flow-nexus 0.35.21) is deployed as it is, this day. flow-start moves into the flow repository, versioned and deployed by CriomOS-home; the Home flow-nexus unit and the messenger repin are activated; the hand-made links in ~/.local/bin are removed; the /home/li/primary paths become skill variables. Gaps 2 and 5 are one piece of work.
+ - Why: Our reading: the order was a working system now, and the redesign must not hold it back.
+ - Corner: until the Home switch runs, the hand-made links and the pin stay. Landing owed: that Home switch.

Ruling: land, amend, or reject.

### Proposal 16: The daemon composes a start · primary › docs/flow-up.md

+ Composed start. Gap 1 lands as the next increment after Proposal 15, not as a gate on it. The Nexus composes a flow from `Start.{ Psyche core Secondary }`, with seat, voice and module declarations in a typed Configure store it loads. The client sends Start and nothing else. It lands in the flow repository; signal-flow and meta-signal-flow carry only the Configure and Start types.
+ - Why: the client reading declarations (Proposal 4) is the shortcut; the declarations belong to the daemon.
+ - Corner: none for the ruling; until it lands, flow-start still reads the declarations.

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

### Proposal 17: Subagent roles reach the harness by files · primary › docs/flow-up.md

+ Role files. At flow start the daemon writes each composed role as an agent file into the flow's agents directory (a tmpfs is fine). The ComposeRole branch (03ec9e2) is abandoned, not repaired.
+ - Why: Our reading: files are what the harness already reads; the ComposeRole branch is not installable (gap 3).
+ - Corner: none. Landing owed: the daemon writing the files.

Ruling: land, amend, or reject.

### Proposal 18: Merge order is sleep, rules, compose-role · primary › docs/flow-up.md

+ Merge order. Branch sleep 0.35.22 merges first, then rules, then compose-role. The claimed conflict between them is settled by the merge itself, not by reading. A branch that does not merge cleanly is rebased by its owner the same day.
+ - Why: gap 4 rests on a claim; the merge is its test.
+ - Corner: Our reading: compose-role is abandoned by Proposal 17, so its merge may be moot. Landing owed: the merges.

Ruling: land, amend, or reject.

### Proposal 19: Registration is checked before a pane opens · primary › docs/flow-up.md

+ Pane order. A start with `-p` into a cell whose predecessor is still registered is refused before any pane opens (gap 6). Registration is checked first.
+ - Why: Our reading: the old order left an unregistered orphan pane.
+ - Corner: none. Landing owed: the check in the launcher.

Ruling: land, amend, or reject.

### Proposal 20: The registry reads liveness from the pane · primary › docs/flow-up.md

+ Liveness. A registry that shows STALE for a live pane is wrong; liveness is read from the pane. The ruling records the fix as landing with Proposal 19; nobody has witnessed it.
+ - Why: hm-list showed Psyche core Secondary 9864c0 as STALE after its pane moved.
+ - Corner: the cause of that entry is still unknown. Landing owed: the fix, and a witness that hm-list now shows 9864c0 live.

Ruling: land, amend, or reject.

### Proposal 21: The defects are fixed in source and the stand-ins removed · primary › docs/flow-up.md

+ Defect list. The empty Herdr reply is treated as no metadata, fixed in launch.rs, and the shim of Proposal 6 is removed. The messenger fix b86a0b upstreams and its overlay (Proposals 3 and 8) is removed. A Wake query and a relay version are added. The NotResumable stops in 6f2dce and 4a16cc are investigated after the work of Proposals 15 to 20, not before.
+ - Why: Our reading: each stand-in outside a repository is lost at the next Home switch.
+ - Corner: shim, overlay and relay stay until their fixes are deployed. Landing owed: all of them.

Ruling: land, amend, or reject.

### Proposal 22: A claim is acted on as unverified · primary › docs/flow-up.md

+ Claims. Anything marked "claimed" in a gap or report is acted on as unverified: the act that lands it is its verification.
+ - Why: Our reading: gaps 4 and 8 are claims, and waiting for proof would stop the work.
+ - Corner: none.

Ruling: land, amend, or reject.

### Proposal 23: A Flow address held by a dead flow is taken by the live one · primary › docs/flow-up.md

+ Address taking. A Flow address held Awake by a flow with no live process is taken by the live process that claims it. Example: 39bd0c bound Psyche core Primary over b3fcde, an empty directory with no process, a leftover duplicate.
+ - Why: Our reading: the binding of the Psyche core Primary had to return to the flow that is alive.
+ - Corner: Flow still trusts the claim without proof that the caller is that flow (see Proposal 9). Landing owed: an identity route in Flow.

Ruling: land, amend, or reject.

### Proposal 24: The overlay reports Held, and binds the sender whenever the flow is dead · primary › docs/flow-up.md

+ Overlay fixes. A message held for repair is reported by the overlay as Held with its id, for example Held.{ 42265e Blocked attempt-337b95 }, never as RuntimeBindingOrStore. The relay binds the sender whenever the awake flow has no live process, not only when the sender is Unknown.

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

+ - Why: Our reading: an awake flow with no process, like b3fcde, blocked the old Unknown-only rule.
+ - Corner: still in the overlay, outside messenger-clj. Landing owed: Proposal 21.

Ruling: land, amend, or reject.

### Proposal 25: The stray profile removal is stopped · primary › docs/flow-up.md

+ Profile removal. A second stray `nix profile remove` of the Flow and messenger packages, started at 15:40, is stopped. The services keep running from the Home-unit store paths, not from the profile.
+ - Why: Our reading: the removal would have taken packages the hand-made links point at.
+ - Corner: Our reading: the profile is still on old links. Landing owed: gap 5, deploy hygiene (Proposal 15).

Ruling: land, amend, or reject.

### Proposal 26: Codex starts fail under 0.35.21 · primary › docs/flow-up.md

+ Codex defect. Starts of Codex seats fail under 0.35.21 with HarnessSpawnRefused after the Herdr agent-startup timeout. aa034f is diagnosing; the cause is a claim, not witnessed here. Mind and Field flows cannot be restarted until it is fixed.
+ - Why: Our reading: recorded because it limits Proposals 10 and 11: the nine live seats must be kept, not restarted.
+ - Corner: none yet; no fix exists. Landing owed: the diagnosis and its fix.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
