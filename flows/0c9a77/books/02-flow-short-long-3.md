<!-- to-the-living:start -->
Presentation.{ «Flow: short term and long term, third edition» }

# Flow: short term and long term, third edition

vision-flow.md is on psyche-context's production branch, main. Primary,
messenger-clj and harness are on main. The flow repository is shown
from a development branch. The Nexus: Flow's long-term form, the Rust
program in the flow repository that will launch, track and message
flows.

## Crystallization

### Proposal 1: the refresh, in the short term

File: `psyche-context/skills/vision-flow.md`, a new heading «Short term»
after «A replaced session is reaped by the refresh itself». The two
paragraphs above the landing, as they stand:

"Every harness event reaches Flow through the harness's hooks calling the
Flow CLI, so Flow knows each flow's state without polling; a marked block
landing in a transcript becomes an action, a book among them, with no tool
call by the flow; a flow nearing its context limit is told, writes its
handover, and is refreshed as it goes idle. Polling is forbidden; a poller
that must exist is registered and reported."

"A flow is refreshed when its context passes the layer's threshold: it is
told, writes its handover, and is replaced as it goes idle; while the
refresh runs the metaflow is locked, and the predecessor is reaped in the
same event. Every harness event reaches Flow through its hooks calling the
Flow CLI, which identifies the calling process."

Below it: «Subflows replace the harness subagent facility».

Words used here: the *launcher* is the script that starts a flow
(`tools/claude-main-flow-launch.mjs`, `tools/codex-main-flow-launch.mjs`);
the *messenger* is messenger-clj, the tool that registers flows and
types messages into them; *flow-id* is the small program, from the
harness repository, that claims a new flow's id.

Sources: flow d68c82, 2026-10-13.

Removed: none.

Added:

+ ## Short term
+
+ Short term: when a flow's context reaches its threshold, the context-refresh hook (`tools/context-refresh-hook.mjs`) tells the flow and Field that its refresh has started. The flow writes its handover and names what of its context goes to existing or new topic flows. The launcher starts its successor from the predecessor's flow id, and the messenger retires the predecessor.

Under choice 2 below, one more sentence:

+ Compaction is used only as an absolute emergency, when starting a successor has failed.

Lands in the short-term tools. Witnessed: the hook exists and is not
yet committed; no launcher installs it, so it runs for no flow today.
Its message to the flow still offers Field a path other than a
successor. In `tools/context-refresh-hook.mjs`, the handover, whose
instruction string and unresolved reason are replaced whole:

```
- instruction: 'The refresh procedure has '
-   + 'started. ... ',
+ instruction: 'The refresh procedure has '
+   + 'started. Write a judgment-only '
+   + 'handover of decisions and unresolved '
+   + 'reasons, name the context topics to '
+   + 'split to existing or new topic flows, '
+   + 'and include no facts that tools can '
+   + 'look up. Your successor is started '
+   + 'once the handover is written.',
- unresolvedReasons: [ ... ],
+ unresolvedReasons: ['refresh requires a '
+   + 'successor flow'],
```

In `tools/claude-main-flow-launch.mjs`, `mainFlowMode`, which today
installs only the reminder hook and, for the committer, one Stop hook:

```
+ const refresh = [sh(process.execPath),
+   sh(path.join(workspace, 'tools',
+     'context-refresh-hook.mjs'))].join(' ');
+ settings.hooks.Stop = [
+   ...(settings.hooks.Stop ?? []),
+   {hooks: [{type: 'command',
+     command: refresh, timeout: 20}]}];
```

Witnessed: the hook acts only for sessions listed in its own JSON
list (`config/context-refresh.json`), which holds one session; no
launcher adds to it. Its thresholds are set per harness and model,
not per layer. The Codex launcher installs no hook; whether Codex
can run this one is unknown.

Ruling:

1. Land the heading and paragraph and both code changes, without
   the emergency sentence.
2. As 1, with the emergency sentence.
3. As 1 or 2, and the hook reads a flow's aspect, topic and layer from
   the messenger's records in place of its own list.
4. Land with changes the living names.
5. Drop.

### Proposal 2: a flow in transition receives nothing

File: `psyche-context/skills/vision-flow.md`, under «Short term», after
Proposal 1's paragraph.

Words used here: a *route* is the messenger's record of where a flow is
reached: its pane (the terminal area in herdr, the third-party terminal
program the flows run in) and its aspect, topic and layer. A flow *in
transition* is one being replaced. A *held* message is one the messenger
did not type; it keeps it as a *pending* record (a message stored to
be typed later) in its Datalevin
database (the database the messenger keeps all its records in).

Sources: flow d68c82, 2026-10-13. The long-term counterpart already
stands in «What it does»: "a metaflow under refresh queues what arrives
until its successor has started."

Removed: none.

Added, the vision:

+ Short term: the messenger also marks a flow in transition when its context reaches its threshold. From then on it holds every message addressed to that flow's metaflow instead of typing it in, so the flow can write its handover and be replaced rather than be kept turning by new arrivals. When the successor registers, the messenger delivers what it held to it, oldest first.

Witnessed in messenger-clj today: a route carries a `:transition`
mark (`typed_store.clj`, the route schema); `in-transition?` reads it;
a send to a marked route is held with the reason `InTransition` and
stored as pending. No command sets or clears the mark, and only
`repair` releases a held message, and only one held for a broken
route. A marked flow cannot send at all: `sender-origin!` refuses it.
A message held in transition does not keep its sender's envelope,
so it could not be delivered later as it was sent. The messenger has
no daemon and no listener of its own: each command runs once and ends.

The machine's design, each a numbered choice below:

A. Who sets the mark. A1: the context-refresh hook, right after its
warning is delivered, so the warning itself is not held. A2: the flow
itself, when it begins its handover.

B. The marked flow's own sending. B1: it still sends (its handover
messages to topic flows need this). B2: it sends nothing; its handover
is a file only.

C. Who releases. `hm-register` is the messenger command that records a
new flow's route; `hm-retire` is the one that takes a flow's route out
of use for good. C1: the successor's registration (`hm-register` with
the same aspect, topic and layer) delivers the held messages and
retires the predecessor. C2: retiring the predecessor (`hm-retire`)
moves them.

D. The tools. D1: the launcher and the messenger stay two tools; the
launcher already registers each flow through the messenger. D2: they
become one tool.

Lands in `messenger-clj/src/messenger_clj/core.clj`. Setting the mark
(under A1 the hook runs it; under A2 the flow does):

```
+ (defn mark-transition! [flow on?]
+   (with-reservation flow
+     (fn []
+       (let [route (read-route flow)]
+         (save-route! (registry) flow
+           (assoc route :transition on?))
+         (str (if on? "InTransition" "Live")
+              ".{ " flow " }")))))
```

`main.clj` gains the command `transition FLOW on|off`, and the
`hm-transition` shorthand beside the others.

Keeping the sender, in `held!`:

```
- repair-envelope (when (= reason
-                          :RepairRequired)
+ repair-envelope (when (#{:RepairRequired
+                          :InTransition}
+                        reason)
```

Under B1, in `sender-origin!`:

```
- (when (or (needs-binding? route)
-           (in-transition? route)
-           (:route_hold route))
+ (when (or (needs-binding? route)
+           (:route_hold route))
```

Releasing, under C1 at the end of `register!`, under C2 in `retire!`.
`deliver-held!` types one stored envelope into the successor's pane
by the same steps `repair!` uses today. Oldest first is by time: the
existing `pending-for` sorts by a random id.

```
+ (defn transition-held [flow]
+   (->> (store/pending-for (root) flow)
+        (filter #(= :InTransition
+                    (get-in % [:attempt
+                               :reason])))
+        (sort-by #(get-in % [:attempt :at]))))
+
+ (defn release-held! [successor]
+   (let [address (metaflow!
+                   (read-route successor))]
+     (doseq [[flow route] (route-records)
+             :when (and (not= flow successor)
+                        (in-transition? route)
+                        (= address
+                           (metaflow! route)))
+             held (transition-held flow)]
+       (deliver-held! successor held))))
```

Lands in the Nexus, long term: `crates/flow-nexus/src/delivery.rs`
refuses a flow that is stopped, retired or exited and passes one that
is pending or active; there is no state for a flow being replaced, and
`crates/flow-nexus/src/lib.rs` refuses every queue request because Flow
holds no queue yet. The lifecycle is declared in signal-flow, the
repository of the message types the Nexus sends and receives (Signal
is the name of that typed message format):

```
- FlowLifecycle.[ Pending Active Stopped
-   Retired Exited ]
+ FlowLifecycle.[ Pending Active Refreshing
+   Stopped Retired Exited ]
```

and `delivery.rs` stores a message for a `Refreshing` flow instead of
typing it.

Ruling, one number from each group:

The vision:
1. Land.
2. Land with changes the living names.
3. Drop.

Who sets the mark:
4. A1, the context-refresh hook.
5. A2, the flow itself.

The marked flow's sending:
6. B1, it still sends.
7. B2, it sends nothing.

Who releases:
8. C1, the successor's registration.
9. C2, the predecessor's retirement.

The tools:
10. D1, two tools.
11. D2, one tool.

The long-term code:
12. Land now.
13. Land after the short term works.

### Proposal 3: the short term, as a figure

File: `psyche-context/skills/vision-flow.md`, under «Short term», after
Proposal 2's paragraph. The steps marked † stand only if Proposal 2
lands. *EDN*: a plain-text data format from the Clojure world, the one
the messenger is written in.

Sources: flow d68c82, 2026-10-13.

Removed: none.

Added:

```
+ +--------------------------------------+
+ | EDN files: shared, per aspect,       |
+ | per metaflow                         |
+ +--------------------------------------+
+         | configure
+         v
+ +--------------------------------------+
+ | the launcher                         |
+ +--------------------------------------+
+         | starts
+         v
+ +--------------------------------------+
+ | a flow, on its topic                 |
+ +--------------------------------------+
+         | is warned at its threshold
+         v
+ +--------------------------------------+
+ | the flow, in transition;             |
+ | its messages held †                  |
+ +--------------------------------------+
+         | writes
+         v
+ +--------------------------------------+
+ | its handover                         |
+ +--------------------------------------+
+         | precedes
+         v
+ +--------------------------------------+
+ | the successor, started by the        |
+ | launcher                             |
+ +--------------------------------------+
+         | registers with
+         v
+ +--------------------------------------+
+ | the messenger                        |
+ +--------------------------------------+
+         | delivers the held messages † to
+         v
+ +--------------------------------------+
+ | the successor, at work               |
+ +--------------------------------------+
+         | is retired into
+         v
+ +--------------------------------------+
+ | the topic, idle                      |
+ +--------------------------------------+
+         | is woken by new input into
+         v
+ +--------------------------------------+
+ | a new flow, clean context            |
+ +--------------------------------------+
```

Ruling:

1. Land.
2. Change.
3. Drop.

### Proposal 4: the EDN launch

File: `psyche-context/skills/vision-flow.md`, under «Short term», after
Proposal 3's figure.

Sources: flow d68c82, 2026-10-13.

Removed: none.

Added:

+ Short term: flow starting is configured in EDN files under `config/main-flow/`: one shared by every aspect, one per aspect, and one per metaflow holding what differs. From them the launcher, through `tools/main-flow-mode/launch-config.mjs`, finds each flow's model and each context module, and whether it goes in the system prompt or the user prompt.

Witnessed: `shared.edn` holds the three skill repositories at fixed
revisions and the tool sets; each aspect file holds its harness, its
model and effort per layer, and its system and user modules; five
metaflow files hold their own modules. Both launchers load them.
The files and `launch-config.mjs` are not yet committed.

The long term, under choice 2: `crates/flow-nexus` keeps its settings
in its own store, entered as typed configuration changes. The added
line:

+ Long term: the EDN files go when `crates/flow-nexus` launches; their settings are entered into it as typed configuration changes and kept in its store.

Under choice 3, the existing line in «Starting flows», as it stands:

"A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect;
the layer decides the model, declared once in Flow as configuration and
changed only over its meta socket."

The meta socket, in plain words: a second, restricted connection to the
Nexus that only its managers may use, apart from the ordinary one every
flow uses.

```
- changed only over its meta socket.
+ changed only by a configuration change
+ to Flow.
```

Ruling:

1. Land the short-term line only.
2. Land it and the long-term line.
3. As 1 or 2, and the wording change in «Starting flows».
4. Land with changes the living names.
5. Drop.

### Proposal 5: lean, specialized flows

File: `psyche-context/skills/vision-flow.md`, «What it does», the
paragraph that begins «A topic never dies». As it stands:

"A topic never dies; it goes idle, its flows turned off. When the living
touches on it again, whether to wake a flow for it, and at which layer,
is a judgment, made by a small model; a topic is bound to its context
modules, so Flow knows what to start it with, together with the new
input that warrants it."

Sources: flow d68c82, 2026-10-13.

Removed:

- A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

Added:

+ Starting a specialized flow is cheap: it carries only the context modules and tools its purpose needs, so its output is of higher quality; when its work is done it is spun down, and waking its topic starts a new flow with a clean context.

Who spins a flow down; in the short term each retires it through the
messenger (`hm-retire`):

+ A: A flow spins itself down when its work is done.
+ B: The flow that asked for it spins it down when its work is done.
+ C: Flow spins down a flow that has gone idle; long term, `crates/flow-nexus/src/performing.rs`, which carries stop and retire.

Who wakes an idle topic in the short term; either starts it with the
launcher:

+ D: A Field Quaternary flow judges when new input wakes an idle topic.
+ E: The Secondary that receives new input wakes the idle topic.

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

Who spins a flow down:
4. A.
5. B.
6. C.

Who wakes an idle topic:
7. D.
8. E.

### Proposal 6: the handover carries judgment

File: `psyche-context/skills/vision-flow.md`, after the last paragraph of
«A replaced session is reaped by the refresh itself» (shown in
Proposal 1).

Sources: flow d68c82, 2026-10-13.

Removed: none.

Added:

+ A handover carries what needs judgment; what a tool returns in one call, such as which revision was pushed or the order of events, the successor looks up.

Witnessed: the hook's message already asks for no facts a tool can
look up (Proposal 1).

Ruling:

1. Land.
2. Change.
3. Drop.
<!-- to-the-living:end -->
