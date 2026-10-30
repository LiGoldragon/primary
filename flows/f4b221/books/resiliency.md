Presentation.{ «Resiliency» }

# Resiliency

Three of your asides of 10-29, each a line of its own in the Flow vision: usage and quotas accounted for; the system logs itself back in; a refresh never leaves the system without a core Primary. The record as it stands, then the three proposals, each with what stands in Flow today under it.

## primary › flows/b2b87a/vision/flow.md

## 2026-10-29 — Usage and quotas accounted for; the system relogs in when tokens expire; a refresh never leaves the system without a core Primary
Context: the living, in the Psyche core Primary chat b2b87a, after the Primary's relaunch was refused by the composer. Parts of one message; the persona and ethos parts are in vision/persona.md and vision/ethos.md.

I know that you don't have a good track record so far of making a nexus that works. With everything that I've said about creating reliability and a way for things to not have you fall asleep (to not have things go into a flow that ends up doing nothing, not replying, or failing), we want to get to the point where, I think, at this point, if we created a loop, every time you have enough usage in your quota (and this is another thing), we need some kind of system, whether it's the Flow Nexus or another one, to start accounting for our usage and our quotas.

By the way, this is another aside: we need a way for the system to be able to relog in because the tokens seem to expire after a certain time.

And I hope that once you reach your context limit, your current flow doesn't get killed, and that this problem that is keeping you from starting a new flow doesn't prevent the new flow from starting (which would leave us without a primary core).

### Proposal 1: Usage and quotas are accounted for · psyche-context › vision/flow.md, and vision/short/flow.md, a new file

**Comment** Your words: "we need some kind of system, whether it's the Flow Nexus or another one, to start accounting for our usage and our quotas." The perennial line keeps your "or another one": the account is Flow's until it is split out. The short line names what the harnesses already hand over, read from their source and docs today, nothing run: Claude Code gives every turn's status line two windows, five hours and seven days, each a used percentage and a reset instant; the Codex app-server pushes a rate-limit snapshot with the same two windows whenever it changes. Flow records them and answers for them; spending the whole quota by the week's end stays the long line of Flow by horizon, proposal 10. vision/short/flow.md is the file Flow by horizon proposes; these lines go under its lines.

#### psyche-context › vision/flow.md

  A flow refreshes before compaction; a compaction is a refresh that was missed.

+ Usage and quotas are accounted for. The Flow Nexus, or a Nexus split out of it, keeps the account of every provider window the system draws on, and a flow is started knowing what is left.

#### psyche-context › vision/short/flow.md

+ ## The account of usage
+
+ Flow reads the windows the harnesses already report: a Claude flow's five-hour and seven-day windows, their used percentage and reset instant, from the status-line data at each turn's end; a Codex flow's primary and secondary windows from the app-server's rate-limit snapshot as it changes. Flow keeps one Usage record per account and window in Memory, answers Observe.Usage with them, and carries them in the heartbeat. A launch asked for while its account's window is spent is queued until the window resets, and the requester is told so by a Notice.

```ethos
+ Memory
+ [ flow:Instant ]
+ [ Account.[ Claude Codex ]
+   Window.[ FiveHour SevenDay
+            Primary Secondary ]
+   Usage.{ Account
+           Window
+           UsedPercent.Integer
+           ResetsAt.Instant } ]
```

```ethos
+ Signal
+ [ flow:Usage ]
+ [ Observe.Observation ]
+ [ Observed.[ Usage.Vector<Usage> ] ]
+ [ Observation.[ Usage ] ]
```

```datom
+ ; the account as Flow holds it, read at a Stop
+ Observe.Usage
+ Observed.Usage.
+   [ { Claude FiveHour 41
+       2026-10-29T22:00:00Z }
+     { Claude SevenDay 63
+       2026-11-03T15:00:00Z }
+     { Codex Primary 12
+       2026-10-30T03:10:00Z } ]
+ ; a launch while the week is spent
+ Notice.«Launch of { Mind core Tertiary }
+         queued: Claude SevenDay at 100,
+         resets 2026-11-03T15:00:00Z.»
```

### Proposal 2: The system relogs in when tokens expire · psyche-context › vision/flow.md, and vision/short/flow.md, a new file

**Comment** Your words: "we need a way for the system to be able to relog in because the tokens seem to expire after a certain time." What was read today, token values untouched: Claude Code's login is an access token of about eight hours and a refresh token of about twenty-eight days, one file shared by every Claude session on the host; the harness refreshes it itself, and its own error texts name a refresh race between sessions sharing that file, which is my hypothesis for what you see, unproven. Claude Code also makes a one-year token, `claude setup-token`, meant for unattended runs, which a flow takes from its environment. Codex's app-server holds the login for every Codex session and offers a headless device-code login; its stored access token here expired on 10-05 and was never rewritten, cause unknown. Two ways to the short line; the first is one step from what exists, the second keeps the subscription login as it is.

#### psyche-context › vision/flow.md

+ The system logs itself back in when a token expires. A login that needs the living reaches him through the provider's own device flow, before the token lapses, and no flow is left waiting on a login it cannot renew.

#### psyche-context › vision/short/flow.md

**Alternative 1**

+ ## Login
+
+ Flow holds one Login per account in its configuration and watches its expiry. A Claude flow is launched with Flow's one-year token in its environment, so it depends on no session token and on no file shared with other sessions; thirty days before that token expires, Flow asks the living for a new one by a Notice, and takes it over the meta socket. A Codex flow runs on the app-server's login; when the app-server reports it lost, or Flow sees it expired, Flow starts the device-code login and the code reaches the living through that flow. A flow whose turn fails on authentication reports it to Flow through the harness's failure hook, and Flow renews the login before it serves that flow again.

**Alternative 2**

+ ## Login
+
+ Flow holds one Login per account in its configuration and watches its expiry. Every flow runs on the host's subscription login, as today; three days before its refresh token expires, Flow starts the harness's login in a pane of its own and sends the living its link by a Notice, so the login is renewed before any flow fails on it. A Codex flow runs on the app-server's login; when the app-server reports it lost, or Flow sees it expired, Flow starts the device-code login and the code reaches the living through that flow. A flow whose turn fails on authentication reports it to Flow through the harness's failure hook, and Flow renews the login before it serves that flow again.

```ethos
+ Memory
+ [ flow:[ Instant Account ] ]
+ [ LoginState.[ Valid Expiring Expired ]
+   Login.{ Account
+           ExpiresAt.Instant
+           LoginState } ]
```

```ethos
+ Signal
+ [ flow:[ FlowId Account ] ]
+ [ Report.{ FlowId Failure } ]
+ [ Reported ]
+ [ Failure.[ Authentication.Account
+             RateLimit.Account ] ]
```

```datom
+ ; the Claude failure hook, through the Flow CLI
+ Report.{ 8552cc Authentication.Claude }
+ ; what reaches the living, thirty days ahead
+ Notice.«Claude login expires 2026-11-26.
+         Renew: claude setup-token, then
+         flow-meta Configure.Login.»
```

### Proposal 3: A refresh never leaves the system without a core Primary · psyche-context › vision/flow.md, and vision/short/flow.md, a new file

**Comment** Your words: "once you reach your context limit, your current flow doesn't get killed, and ... this problem that is keeping you from starting a new flow doesn't prevent the new flow from starting (which would leave us without a primary core)." Read in the Flow that serves today, 0.40.4, which is not the 0.37.1 our knowledge module names: on a maintained metaflow the successor starts first, and the predecessor is closed only after the successor is confirmed started; when the successor's composition or launch is refused, the predecessor stays awake with its queue kept, nothing stays locked, and the refresh is retried at the flow's next rest. So the killing you feared cannot happen on that path. What stands open: the kept predecessor receives only pressing messages, soft ones are held until a successor stands; the refusal is written to the journal and reaches no flow; a metaflow that is not maintained is closed first and composed at its next wake. The one composer refusal in the journal that evening, "invalid, duplicate or cross-placement module ID", was a launch, not a refresh; which metaflow it was for I could not tell from the log. The perennial line changes the refresh paragraph; the short lines name the three gaps. Your "we might even be contemplating compacting you before this dreadful possibility" is the last short line.

```
 predecessor ──rest, over threshold──▶ Flow
      │                                 │
      │ serves on,          compose and start successor
      │ soft requests too        │              │
      │                     confirmed        refused
      │                          │              │
      │                     reap, Replaced   Notice to the
      ▼                          ▼           Secondary; retry
   successor ◀── queue ────── metaflow      at the next rest
```

#### psyche-context › vision/flow.md

- A flow is refreshed when its context passes its model's threshold: Flow keeps the metaflow's next messages for its next flow, and the flow is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Each model's threshold is configured in Flow; an OpenAI model's is lower than a Claude model's.
+ A flow is refreshed when its context passes its model's threshold: Flow keeps the metaflow's next messages for its next flow, and the flow is replaced as it goes idle; while the refresh runs the metaflow is locked. The successor starts first, and the predecessor is reaped only once the successor is confirmed started, so a refresh never leaves a metaflow, the core Primary of an aspect above all, without a flow. A successor refused leaves the predecessor serving, and the refusal, with its cause, reaches the metaflow's Secondary. Each model's threshold is configured in Flow; an OpenAI model's is lower than a Claude model's.

#### psyche-context › vision/short/flow.md

+ ## A refused successor
+
+ Every core metaflow is maintained: its successor is composed and started before its predecessor is closed. A predecessor kept after a refused successor is served as any awake flow, soft requests included, until its successor stands. The refusal reaches the metaflow's Secondary as a Notice naming its cause, and Flow retries the refresh at the flow's every rest and at every request queued for it. A predecessor whose successor is still refused when its context reaches its model's ceiling compacts, and the compaction is reported as the refresh that was missed.

```datom
+ ; to { Psyche core Secondary }, at the refusal
+ Notice.«Refresh of { Psyche core Primary }
+         refused: ComposerRejected, duplicate
+         module ID. b2b87a kept serving; soft
+         requests delivered; retry at its rest.»
```
