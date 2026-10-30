Presentation.{ «The reminder» }

# The reminder

Your ideas of 10-29: a task message carries its expected minutes, and Flow reminds the sender when they lapse; a receiver going idle on a task is reported; hooks on every harness event, configurable; the tracker. The record as it stands, then the reminder as the Psyche core Primary ruled it, with its one question, which the Psyche flow Primary's ruling of tonight, in Proposal 2, settles. Then the idle notification, the hooks, the two trackers, and seven features the harness study makes possible, each yours to take or leave. Short means buildable next on Flow 0.40.4; medium means past it. The first proposal by flow eb785b; Proposals 2 to 12 by Opus 5.5, Psyche flow Secondary 2a9116, from the harness study of an Opus subflow.

## primary › flows/b2b87a/vision/flow.md

# Flow

## 2026-10-29 — A reminder in Flow: a task message carries its expected minutes; the done reply names the task and cancels the reminder
Context: the living, in the Psyche core Primary chat b2b87a, after an evening in which Field and the book flow answered no order and nothing told the Primary how long to wait.

you need a function in flow that lets any metaflow (regardless of wether its refreshed) get a "reminder" so that it can check on stuff, using a per-situation timer, so it can be reminded if something is taking too long. it could even be a field in a certain kind of "task" message, which the receiver would see (a number of minutes) which would let the receiver know how long it is expected to take. then the task-done reply would let the sender indicate which task so that the reminder is cancelled when the message is received. what do you think?

```
sender ──Order.{ Minutes … }──▶ Flow ──▶ receiver
  ▲                              │
  │        minutes lapse,        │ Task record:
  │        no Result             │ id, sender,
  ├──Reminder.id─────────────────┤ receiver,
  │  (Notice copy to receiver)   │ deadline, state
  │                              │
  ◀──Result.{ id … } closes it───┘
```

### Proposal 1: A task is an order with its minutes · psyche-context › vision/short/flow.md

**Comment** Your idea, with one reduction the Psyche core Primary ruled: the task is the order itself, named by the message id Flow already answers a send with, so there is no second identifier. I place it short because every piece it stands on exists in Flow today: Order, Result, the message id, and Memory; moving it to medium is one word. The one question that is yours comes last, as two alternatives.

+ ## A task is an order with its minutes
+
+ Every Order carries Minutes, the sender's estimate of how long its doing takes; a sender that cannot estimate gives Flow's configured default. Flow answers the send with the order's message id, as it does today, and the receiver sees the id and the minutes in the order. The order is the task, named by its id. A Result names the order's id, and that closes the task; a Result naming no open task is refused. When the minutes lapse with no Result, Flow sends Reminder.<id> to the sender, waking it, and a Notice copy to the receiver, queued. The receiver may send Extend.{ <id> Minutes } before the lapse; Flow moves the deadline and tells the sender by a Notice. A task is a Flow Memory record keyed by the order's id and the two addresses, so a refreshed sender or receiver finds it; a reminder goes to the address, whichever flow holds it.

**Alternative 1**

+ After a Reminder the task stays open until its Result; a further timer is the sender's Extend.

**Alternative 2**

+ After a Reminder, Flow reminds the sender again every interval, its Minutes long, until its Result.

```ethos
+ Library
+ [ flow:[ Address MessageId ] ]
+ [ Minutes.Integer
+   Instant.String
+   TaskState.[ Open Reminded Done ] ]
+ []
+ []
```

```ethos
+ Signal
+ [ flow:[ Address MessageId Minutes ] ]
+ [ Send.{ Recipient Delivery Message } ]
+ [ SendAccepted.{ MessageId Cursor Admission }
+   Refused.[ NoOpenTask.MessageId ] ]
+ [ Cursor.Integer
+   Recipient.[ Address.Address Up ]
+   Delivery.[ Wake Queue ]
+   Admission.[ Queued ]
+   Priority.[ Soft MiddleAbrupt HardAbrupt ]
+   Message.{ Priority Request }
+   Request.[ Order.{ Minutes String }
+             Result.{ MessageId String }
+             Extend.{ MessageId Minutes }
+             Reminder.MessageId
+             Notice.String ] ]
```

```ethos
+ Memory
+ [ flow:[ Address MessageId Minutes
+          Instant TaskState ] ]
+ [ Task.{ MessageId
+          Sender.Address
+          Receiver.Address
+          Minutes
+          Deadline.Instant
+          TaskState } ]
```

```datom
+ ; the sender's order, forty minutes estimated
+ Send.{ Address.{ Field core Secondary }
+        Wake
+        Soft.Order.{ 40
+                     «Deploy Flow 0.38 to the
+                      testing capsule.» } }
+ SendAccepted.{ 7f3a2c 12 Queued }
+ ; the receiver asks for thirty more minutes
+ Send.{ Up Queue Soft.Extend.{ 7f3a2c 30 } }
+ ; at the lapse, Flow sends both
+ Reminder.7f3a2c
+ Notice.«Order 7f3a2c lapsed.»
+ ; the receiver's result closes the task
+ Send.{ Up
+        Wake
+        Soft.Result.{ 7f3a2c
+                      «Deployed; the capsule
+                       answers Current.» } }
```

### Proposal 2: A lapsed task is reminded four times, then fails · psyche-context › vision/short/flow.md

**Comment** The Psyche flow Primary ruled tonight: the reminder fires at the deadline, then repeats at the same interval until a Result names the task: the first firing plus three repeats, four reminders in all; the third repeat also reaches the sender's Secondary as a failure. This settles Proposal 1's question: Alternative 2, four reminders in all, the last also a failure to the sender's Secondary. Tonight's wire is under ruling between two shapes: the in-place Order.{ Minutes String } and Result.{ MessageId String }, shown here, and the appended Task.{ Minutes String } and Done.{ LogicalDeliveryId String }, which needs no store migration; either refuses a reply naming no open task with Refused.NoOpenTask. Short: Order, Result, the message id and Memory stand in Flow 0.40.4; the timer is new. The sender's Secondary is the Secondary of the sender's aspect and topic, so a sender that is that Secondary hears its own failure. Not ruled: whether an Extend after a reminder resets the count.

+ ## A lapsed task is reminded four times, then fails
+
+ When the minutes lapse with no Result, Flow sends Reminder.{ <id> 0 } to the sender, waking it, and a Notice copy to the receiver, queued. Until a Result names the task, it repeats the reminder at the same interval, its Minutes long, as Reminder.{ <id> 1 }, then 2, then 3: the first firing plus three repeats, four reminders in all. The third repeat is the last, and it also reaches the Secondary of the sender's aspect and topic, as TaskFailed.{ <id> <sender> <receiver> }.

```ethos
+ Signal
+ [ flow:[ Address MessageId Minutes ] ] ; imports
+ []                                     ; queries
+ []                                     ; responses
+ [ Repeat.Integer                       ; types
+   ; a request, as a message carries it
+   Request.[ Order.{ Minutes String }
+             Result.{ MessageId String }
+             Extend.{ MessageId Minutes }
+             ; 0 at the deadline, repeats 1 to 3
+             Reminder.{ MessageId Repeat }
+             ; to the sender's Secondary
+             TaskFailed.{ MessageId
+                          Sender.Address
+                          Receiver.Address }
+             Notice.String ] ]
```

```ethos
+ Memory
+ ; imports
+ [ flow:[ Address MessageId Minutes
+          Instant Repeat ] ]
+ ; record types
+ [ Task.{ MessageId
+          Sender.Address
+          Receiver.Address
+          Minutes
+          Deadline.Instant
+          ; Reminded: the last repeat fired
+          TaskState.[ Open
+                      Reminded.Repeat
+                      Done ] } ]
```

```datom
+ ; forty minutes, no Result: four reminders
+ Reminder.{ 7f3a2c 0 }  ; at forty minutes
+ Reminder.{ 7f3a2c 1 }  ; at eighty
+ Reminder.{ 7f3a2c 2 }  ; at a hundred and twenty
+ Reminder.{ 7f3a2c 3 }  ; at 160, the last
+ ; with the third, to Psyche core Secondary
+ TaskFailed.{ 7f3a2c
+              { Psyche core Primary }
+              { Field core Secondary } }
```

### Proposal 3: A receiver that rests with an open task is reported idle · psyche-context › vision/short/flow.md

**Comment** Your words: "somebody should have received a notification that this book flow went idle because we were waiting for something from him. Either he messages back, which cancels the notification, only when the message reaches a particular metaflow, or he goes idle, and then the notification fires." Short: both events reach Flow 0.40.4 today. A Claude flow's Stop hook is installed; Claude Code 2.1.294 gives it `background_tasks` and `session_crons`, which tell a flow at rest from one waiting on its own work, and Flow today passes neither on. A Codex flow's `turn/completed` and `thread/status/changed` idle are already watched. Codex has no background-work signal, so a Codex receiver waiting on a subagent reads as resting. I read "reaches" literally: a Result still queued for a busy sender when the receiver rests does not cancel, and the notification fires. Unknown: whether Claude's Stop fires on the Escape that a hard-abrupt delivery sends.

+ ## A receiver that rests with an open task is reported idle
+
+ When the receiver of an open task comes to rest and no Result naming the task has reached the sender's metaflow, Flow sends Idle.<id> to the sender, waking it. A Claude receiver rests when its Stop binds no Result to the task and names no background task and no session cron; a Codex receiver rests when its turn completes and its thread is idle. A Result naming the task cancels the notification when it reaches the sender's metaflow; a message reaching any other metaflow cancels nothing.

```ethos
+ Signal
+ ; imports
+ [ flow:[ FlowId MessageId NativePrompt
+          NativeSessionId TranscriptPath ] ]
+ [ Report.{ FlowId Event } ] ; queries
+ [ Reported ]                ; responses
+ ; types
+ [ ; the counts are Claude's Stop fields
+   NativeStop.{ Option<NativeSessionId>
+                Option<TranscriptPath>
+                Option<String>
+                BackgroundTasks.Integer
+                SessionCrons.Integer }
+   ; a harness event a hook reports
+   Event.[ Started.Option<NativeSessionId>
+           ToolUsed.String
+           Stopped.NativeStop
+           PromptSubmitted.NativePrompt
+           Ended.Option<NativeSessionId>
+           Cleared.Option<NativeSessionId> ]
+   ; Idle: the receiver of the task rested
+   Request.[ Idle.MessageId
+             Notice.String ] ]
```

```datom
+ ; the receiver's Stop: nothing owed, no work left
+ Report.{ 9c41e0
+          Stopped.{ Some.5b2d17
+                    Some./abs/transcript.jsonl
+                    None
+                    0
+                    0 } }
+ ; task 7f3a2c open, no Result: to its sender
+ Idle.7f3a2c
```

### Proposal 4: Hooks on every harness event, configured · psyche-context › vision/short/flow.md, and vision/medium/flow.md

**Comment** Your words: "The Flow Nexus needs to install hooks in every part of the system where it can get notified of anything that's happening to that particular flow, so that it knows and has the data to be able to act on and implement all these features." And: "Maybe some of the hooks even deliver content, meaning they might deliver the last message because that might actually be useful as a feature to be passed on somewhere. We wouldn't necessarily store it in memory. It might be acted on, or it might not be acted on, and it might just disappear from the Nexus's memory. It might just be an ephemeral piece of data that is either acted on or thrown out." And: "That would be configurable, meaning they would be optional and we wouldn't necessarily have to use them". What stands, read in Flow's source and witnessed in Claude Code 2.1.294: Flow installs five of Claude's 33 hook events, SessionStart, PostToolUse, UserPromptSubmit, Stop and SessionEnd, never answers back, and stores the whole Stopped event, last message included, in its events table. A Codex seat runs no hook; Flow follows it by app-server notifications. The Claude half is short: Flow writes the hooks it installs at launch, so it can write them from configuration, and keeping content out of the events table is a change to one record. The Codex half is medium, as you placed hooks on all harnesses on 10-23, and because whether Codex hooks run for Flow's app-server threads is unknown. The shape is one new configuration family, declared whole as the others are. Reactions Hold, Brief, Rebrief, Progress, Failure and Guard belong to Proposals 6 to 11 and leave with any you reject.

#### psyche-context › vision/short/flow.md

+ ## Harness hooks are configured
+
+ Flow installs a Claude flow's hooks from its Hooks configuration: one rule per harness and event, naming whether the hook carries the event's content and what acts on it. An event with no rule is not hooked. Content a hook carries is held only while it is acted on, then dropped; Flow records the event without it.

#### psyche-context › vision/medium/flow.md

+ ## Every harness event can be hooked
+
+ Flow offers a hook on every event each harness offers, Codex as well as Claude, under the same Hooks configuration; a Codex flow's hooks join its app-server notifications.

```ethos
+ Signal
+ ; imports
+ [ signal_flow:[ Address HarnessKind ]
+   meta_signal_flow:[ ConfigureModel
+                      ConfigureThreshold
+                      ConfigureLeaveOut
+                      ConfigureNexus
+                      ConfigureSendServer
+                      ConfigureMetaflow ] ]
+ [ Configure.ConfigurationChange ] ; queries
+ ; responses
+ [ Configured.[ Replaced Unchanged ] ]
+ ; types
+ [ ; one family declared whole; Hooks is new
+   ConfigurationChange.[
+     Models.Vector<ConfigureModel>
+     Thresholds.Vector<ConfigureThreshold>
+     LeaveOuts.Vector<ConfigureLeaveOut>
+     Nexus.ConfigureNexus
+     SendServers.Vector<ConfigureSendServer>
+     Metaflows.Vector<ConfigureMetaflow>
+     Investigation.Address
+     Hooks.Vector<ConfigureHook> ]
+   ; one rule per harness and event
+   ConfigureHook.{ HarnessKind
+                   HarnessEvent
+                   Content
+                   Vector<Reaction> }
+   ; Carried: held while it is acted on
+   Content.[ Bare Carried ]
+   ; open: any other event by its own name
+   HarnessEvent.[ SessionStart
+                  UserPromptSubmit
+                  PreToolUse
+                  PostToolUse
+                  PostToolBatch
+                  PostToolUseFailure
+                  Notification
+                  Stop
+                  StopFailure
+                  SubagentStop
+                  PreCompact
+                  PostCompact
+                  SessionEnd
+                  Interrupt
+                  TurnStarted
+                  TurnCompleted
+                  ThreadStatusChanged
+                  Error
+                  otherEvent ]
+   ; what acts on the event
+   Reaction.[ Record
+              Reply
+              Rest
+              Forward.Address
+              Hold
+              Brief
+              Rebrief
+              Progress
+              Failure
+              Guard ] ]
```

```datom
+ ; today's hooks, the last message no longer stored
+ Configure.Hooks.[
+   { Claude SessionStart Bare [ Record ] }
+   { Claude UserPromptSubmit Bare [ Record ] }
+   { Claude PostToolUse Bare [ Record ] }
+   { Claude Stop Carried [ Record Reply Rest ] }
+   { Claude SessionEnd Bare [ Record ] }
+   ; a failed turn's last words, passed on
+   { Claude StopFailure
+     Carried
+     [ Record
+       Forward.{ Psyche core Secondary } ] } ]
```

### Proposal 5: Two trackers, one beat · psyche-context › vision/tracker.md, a new file, and vision/short/tracker.md, a new file

**Comment** Your words of 10-29: "as a to-do manager, as a reminder, he would get these hard beats maybe every 20 minutes. His job would be to keep this to-do list, this list of tasks". "Can we modify the beads to assign meta flows for them?" "The bead could also indicate the creator of the bead, or maybe it's a field that talks about somebody that needs to be notified when this task progresses, blocks, or is considered to be done, right?" And: "You could even have two trackers: you could have a Codex and a Cloud tracker, just in case one of them fails. They could talk to each other and wake up at the same time, then talk to each other and decide who should be notified of what and who's going to send the messages." The Psyche flow Primary ruled the rest: beat numbers, nudges naming their beat, duplicates dropped, observations written and exchanged, Psyche to the Claude tracker, Mind and Field to the Codex tracker, a twin silent for one beat leaving the other to send alone. Short: both trackers run tonight from a role file, with the Claude tracker's cron sending the beat and a hash of the bead id choosing the tracker; these lines replace both. I propose a user timer sending the beat to both, so neither twin's failure stops it. bd 1.0.3 has labels and JSON metadata; labels hold several per bead and filter by pattern, and a label such as `Assigned.{ Psyche flow Secondary }` was accepted and filtered in a scratch database. Two tensions are yours: your record puts the tracker in Field as a Haiku Quaternary that messages Secondaries, while vision:model-roles places Claude in Psyche and vision:aspects lets a Quaternary speak only to its Tertiary; and this twenty-minute beat is not the sanity heartbeat of an hour or longer that Flow by horizon proposes.

#### psyche-context › vision/tracker.md

+ description: The tracker, which keeps the open tasks from being forgotten, is designed or judged.
+ dependencies: [vision-flow]
+
+ ## Two trackers, one beat
+
+ Two trackers keep the open tasks, a Claude tracker and a Codex tracker. Every heartbeat carries its beat number, and both wake on it. Each writes its observation of the beat to the tracker file and sends the other a Notice carrying it. The Claude tracker nudges Psyche metaflows; the Codex tracker nudges Mind and Field metaflows. Every nudge names its beat, and a receiver drops a nudge it already has. A tracker that has heard nothing from its twin for one beat sends every nudge of that beat alone, and says so.

#### psyche-context › vision/short/tracker.md

+ description: The tracker is built or repaired as it runs now.
+ dependencies: [vision-tracker]
+
+ ## A bead names its metaflows by labels
+
+ A bead names each metaflow assigned to it by a label Assigned.<address>, and each metaflow to be notified when it progresses, blocks or is done by a label Progress.<address>, Blocked.<address> or Done.<address>.
+
+ ## A timer beats
+
+ A user timer sends Beat.<number> to both trackers through Flow every twenty minutes, each number one above the last.

```ethos
+ Library
+ [ flow:Address ] ; imports
+ ; types
+ [ BeatNumber.Integer
+   BeadId.String
+   ; a bead's labels, one per metaflow
+   BeadLabel.[ Assigned.Address
+               Progress.Address
+               Blocked.Address
+               Done.Address ]
+   ; why a metaflow is nudged
+   Cause.[ Asleep Progressed Blocked Done ]
+   Nudged.{ Address BeadId Cause }
+   ; what the trackers send
+   TrackerMessage.[
+     ; from the timer, to both
+     Beat.BeatNumber
+     ; to a metaflow
+     Nudge.{ BeatNumber BeadId Cause }
+     ; to the tracker file and the twin
+     Observation.{ BeatNumber
+                   Twin.[ ClaudeTracker
+                          CodexTracker ]
+                   Partner.[ WithTwin Alone ]
+                   Vector<Nudged> } ] ]
+ [] ; traits
+ [] ; associations
```

```sh
+ bd label add primary-f6g4 \
+   'Assigned.{ Psyche flow Secondary }'
+ bd label add primary-f6g4 \
+   'Done.{ Psyche core Primary }'
+ bd list --status open \
+   --label-pattern 'Assigned.*'
```

```datom
+ ; beat 42, from the timer, to both trackers
+ Send.{ Address.{ Psyche tracker Quaternary }
+        Wake
+        Soft.Notice.«Beat.42» }
+ Send.{ Address.{ Field tracker Quaternary }
+        Wake
+        Soft.Notice.«Beat.42» }
+ ; the Claude tracker nudges a Psyche metaflow
+ Send.{ Address.{ Psyche flow Secondary }
+        Wake
+        Soft.Notice.«Nudge.{ 42 primary-f6g4
+                             Asleep }» }
+ ; its observation, to the file and its twin
+ Observation.{ 42
+               ClaudeTracker
+               WithTwin
+               [ { { Psyche flow Secondary }
+                   primary-f6g4
+                   Asleep } ] }
+ ; beat 43: no word from its twin in 42
+ Observation.{ 43
+               ClaudeTracker
+               Alone
+               [ { { Mind core Secondary }
+                   primary-sq95
+                   Asleep } ] }
```

### Proposal 6: A flow that owes a Result is held · psyche-context › vision/short/flow.md

**Comment** One line the harness study makes possible, yours to take or leave. Short for Claude: a Stop hook may answer block with a reason, and `stop_hook_active` tells Flow the Stop was already held once. Codex's Stop can block alike once Flow installs Codex hooks.

+ A Stop that owes a Result for an open task is held once: Flow answers the Stop hook with the task's id, and the flow goes on.

```datom
+ { Claude Stop Carried [ Record Reply Rest Hold ] }
```

### Proposal 7: A prompt carries its open tasks · psyche-context › vision/short/flow.md

**Comment** Yours to take or leave. Short: Claude's UserPromptSubmit hook may answer with added context; Codex's runs only for user input.

+ A prompt submitted to a flow carries, as added context, its open tasks and the minutes left on each.

```datom
+ { Claude UserPromptSubmit Bare [ Record Brief ] }
```

### Proposal 8: A flow gets its brief back after compaction · psyche-context › vision/short/flow.md

**Comment** Yours to take or leave. Short: Claude's SessionStart fires with source compact, resume or clear and may answer with added context.

+ After a compaction, a resume or a clear, Flow gives the flow back its brief and its open tasks as added context.

```datom
+ { Claude SessionStart Bare [ Record Rebrief ] }
```

### Proposal 9: A late task still worked on is reported working · psyche-context › vision/short/flow.md

**Comment** Yours to take or leave. Short for Claude: PostToolBatch fires once per batch of tool calls. Codex's `item/*` notifications would serve alike; Flow does not watch them today.

+ A receiver of a late task that is still using tools is reported to its sender as working.

```datom
+ { Claude PostToolBatch Bare [ Progress ] }
```

### Proposal 10: A failed turn is reported at once · psyche-context › vision/medium/flow.md

**Comment** Yours to take or leave. Medium: Claude's StopFailure and PostToolUseFailure, Codex's `error` with `willRetry` false, `model/rerouted` and `account/rateLimits/updated` carry it; retry and quota-aware routing are undesigned.

+ A turn that ends on an error is reported at once to the sender of the open task it holds.

```datom
+ { Claude StopFailure Carried [ Record Failure ] }
```

### Proposal 11: A tool use outside a flow's role is denied · psyche-context › vision/medium/flow.md

**Comment** Yours to take or leave. Medium: Claude's and Codex's PreToolUse may deny a tool; what a role forbids is not yet declared anywhere Flow reads.

+ A tool use outside a flow's role is denied before it runs.

```datom
+ { Claude PreToolUse Bare [ Guard ] }
```

### Proposal 12: Codex hook runs are recorded · psyche-context › vision/medium/flow.md

**Comment** Yours to take or leave. Medium: the app-server sends `hook/started` and `hook/completed`; it waits on Codex hooks of Proposal 4.

+ Every Codex hook run is recorded, so a hook that fails or never runs is seen.

```datom
+ { Codex hookCompleted Bare [ Record ] }
```
