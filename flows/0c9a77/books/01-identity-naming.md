<!-- to-the-living:start -->
Presentation.{ «Flow: identity and naming» }

# Flow: identity and naming

vision-flow.md is on psyche-context's production branch, main. The
Nexus code is shown from the flow repository's main branch; its local
checkout sits on a development branch.

The Nexus: the Rust program, Flow's long-term form, that launches,
names and tracks flows. The short-term tools: what does that work
today, the launcher scripts that start flows and the messenger,
messenger-clj, that registers flows and delivers their messages.

## Crystallization

### Proposal 1: a flow id is a hash

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«A topic's name is a camelCase identifier». "Binds" below means the moment
Flow ties a flow record to the live process that runs it. As it stands:

"A topic's name is a camelCase identifier, uncapitalized. A flow's id is
the hash of the harness's session id, so a transcript is found from the
flow id. Where the harness lets Flow choose the session id, Flow chooses
it before the flow starts and the flow reads it in its prompt; where the
harness assigns it, Flow learns it when the flow binds. No flow declares
its id: every call to Flow is identified by the calling process."

Sources: flow 692df8, 2026-09-15; flow edf227, 2026-10-03.

Removed: none.

Added, after «so a transcript is found from the flow id.»:

"A flow id is a hash, never a string; its written forms are its
serialization, made where it leaves Flow, and Flow itself holds only the
hash."

Lands in the Nexus: `crates/flow-ethos/ethos/library.ethos`, the
shared types the Nexus and its wire use. As it stands, top of the list:

```
Library
[]
[ FlowId.String
```

The machine's proposal, under choice 1: the type holds the harness's
whole session id, sixteen raw bytes, and the short id is written from
it. *Bytes<N>* means N raw bytes.

```
- [ FlowId.String
+ [ ; Sixteen bytes: the harness's session id.
+   FlowId.Bytes<16>
```

Under choice 2 the type holds only the short part of the session id,
the bytes the short id is written from.

Ruling:

1. Land the sentence, and the type as the whole session id.
2. Land the sentence, and the type as the short part only.
3. Land the sentence; the type waits.
4. Neither.

### Proposal 2: the word form of a flow id

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«A topic's name is a camelCase identifier». As it stands:

"A topic's name is a camelCase identifier, uncapitalized. A flow's id is
the hash of the harness's session id, so a transcript is found from the
flow id. Where the harness lets Flow choose the session id, Flow chooses
it before the flow starts and the flow reads it in its prompt; where the
harness assigns it, Flow learns it when the flow binds. No flow declares
its id: every call to Flow is identified by the calling process."

Removed: none.

Added, after «so a transcript is found from the flow id.» (after
Proposal 1's sentence, if it lands), under choices 1 to 3:

"A flow id is also written as words: the first 33 bits of the harness's
session id, as words from a published word list, and read back into
those bits so the transcript is found from the words. When two flows'
words match, the collision is brought to the living."

A published word list: BIP-39 is one, 2048 words, each carrying 11
bits, so three words carry 33 bits; two words need a denser list.

Lands in the Nexus: no word form exists in `crates/flow` or
`crates/flow-nexus`; the title is where it would show (Proposal 5).

Lands outside both: `harness/src/flow_id.rs`, the flow-id tool. Both
the Nexus and the launcher scripts call it to claim a flow id: it takes
the harness's session id and reserves a short id for it by creating
that flow's directory, so no two flows hold the same id. As it stands,
the short id is six hex characters, one more on each collision:

```
const FIRST_CANDIDATE_LENGTH: usize = 6;
```

Ruling:

1. Land now; three words joined as one uncapitalized camelCase word,
   like `wordWordWord` (flow 05c604, 2026-09-15; flow d4ae97,
   2026-10-07; flow 0c85a3, 2026-10-09).
2. Land now; three words apart, with a separator of their own (flow
   05c604, 2026-09-15).
3. Land now; two words from a denser list (flow 05c604, 2026-09-15;
   flow d4ae97, 2026-10-07).
4. Wait until after a minimum viable product; no line now (flow dea0ba,
   2026-10-03).

### Proposal 3: flow ids are for the ledger

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«Flow manages metaflows». As it stands:

"Flow manages metaflows. A metaflow is one address, { Aspect Topic
Layer }, that continues through several flows one after another; the
flow is its current run, and what is addressed is always the metaflow,
never a flow. The default topic is core: the permanent topic, the thing
that keeps the machine going, the last topic to stand."

The ledger: the record of every flow that has run.

Sources: flow 01e496, 2026-10-02; flow 4ddfe1, 2026-10-07; flow 7c89aa,
2026-10-13.

Removed: none.

Added, after «never a flow.»:

"A flow id is for the ledger: it finds a flow's transcript and its place
among its metaflow's past flows. Flows name one another, and the living,
by metaflow."

Lands in the Nexus: the *Caller*, what Flow answers when asked who is
calling, names the caller by flow id and aspect. It is declared in
`signal-flow/ethos/signal.ethos`, the wire types `crates/flow-nexus`
uses:

```
- Caller.{ FlowId Aspect PowerLevel ModelName }
+ Caller.{ Address FlowId PowerLevel ModelName }
```

`crates/flow-nexus/src/store.rs`, where a Caller is built (two
places), fills `Address` from the flow's metaflow in place of its
aspect.

Lands in the short-term tools: `messenger-clj/src/messenger_clj/core.clj`
takes a send target either as a flow id or as
«aspect topic layer». As it stands:

```
(defn target-flow! [target]
  (if (m/validate FlowId target)
    target
    (do
      (valid! Metaflow target
        "TARGET metaflow (aspect topic layer)")
      ...
```

```
- (defn target-flow! [target]
-   (if (m/validate FlowId target)
-     target
-     (do
-       (valid! Metaflow target
-         "TARGET metaflow (aspect topic layer)")
-       ...)))
+ (defn target-flow! [target]
+   (valid! Metaflow target
+     "TARGET metaflow (aspect topic layer)")
+   ...)
```

Ruling:

1. Land the sentence and both code changes.
2. Land the sentence; the code keeps taking flow ids as targets.
3. Neither.

### Proposal 4: the caller is found, never declared

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«A topic's name is a camelCase identifier». As it stands:

"A topic's name is a camelCase identifier, uncapitalized. A flow's id is
the hash of the harness's session id, so a transcript is found from the
flow id. Where the harness lets Flow choose the session id, Flow chooses
it before the flow starts and the flow reads it in its prompt; where the
harness assigns it, Flow learns it when the flow binds. No flow declares
its id: every call to Flow is identified by the calling process."

Its last sentence stands, unchanged; the code still reads a declared id.

Source: flow 875960, 2026-10-11.

Removed: none. Added: none.

Lands in the Nexus: `signal-flow/ethos/signal.ethos`, the requests:

```
- ResolveCaller.Option<FlowId>
+ ResolveCaller
- Report.{ FlowId Event }
+ Report.Event
- CallerResolutionRejection.[
-   CallerUnknown
-   CallerMismatch.Caller ]
+ CallerResolutionRejection.[ CallerUnknown ]
```

`crates/flow-nexus/src/caller.rs`. Flow already finds the caller from
the process at the other end of its connection, through the terminal
pane (the terminal window the flow runs in) that process runs in; it then also checks an optional declared id:

```
- fn resolve_caller(&self,
-     pane: Option<CallerPane>,
-     claim: Option<FlowId>) -> Response {
+ fn resolve_caller(&self,
+     pane: Option<CallerPane>) -> Response {
      let caller = pane
          .ok_or(CallerResolutionRejection
              ::CallerUnknown)
          .and_then(|pane|
              self.bound_caller(&pane));
-     match (caller, claim) {
-         (Err(rejection), _) => Response
-             ::CallerResolutionRejected(rejection),
-         (Ok(caller), Some(claimed))
-             if claimed != caller.flow_id => ...,
-         (Ok(caller), _) => Response
-             ::CallerResolved(caller),
-     }
+     match caller {
+         Err(rejection) => Response
+             ::CallerResolutionRejected(rejection),
+         Ok(caller) => Response
+             ::CallerResolved(caller),
+     }
```

`crates/flow/src/hook.rs`, the hook each Claude flow runs on its events,
sends the id it reads from its environment:

```
-     flow_id: env::var("FLOW_ID")
-         .ok()
-         .filter(|flow_id| !flow_id.is_empty()),
...
-     HookCall::Report(format!(
-         "Report.{{ {} {event} }}",
-         flow_id.quoted()))
+     HookCall::Report(format!("Report.{event}"))
```

and `crates/flow-nexus/src/lib.rs` answers a Report for the caller it
finds from the connection, as it does for ResolveCaller.

Lands in the short-term tools: `messenger-clj/src/messenger_clj/core.clj`
takes the sender from the id the flow sets in its environment:

```
- (let [sender (flow-id!
-                (or *flow-id*
-                    (System/getenv "FLOW_ID")
-                    (fail "Set FLOW_ID ...")))]
+ (let [sender (pane-flow!
+                (System/getenv "HERDR_SESSION")
+                (System/getenv "HERDR_PANE_ID"))]
```

`pane-flow!` is new: it finds the one registered route whose session
and pane match those marks, which the terminal multiplexer, Herdr, sets
on every process it starts in a pane.

Ruling:

1. Land both code changes.
2. Land the Nexus change only.
3. Neither.

### Proposal 5: the title names aspect, topic, layer and id

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«Every flow has a topic». As it stands:

"Every flow has a topic; a flow with no special topic has the topic core,
the heart of its aspect. A topic is a core:Name, a camelCaseExpression
checked when created. A flow's title names its aspect, topic, layer and
flow id: { Psyche core Secondary <id> }."

Sources: flow 5578cc, 2026-10-03; flow d4ae97 and flow f5a6e9,
2026-10-07; flow 445410, 2026-10-09.

Under choice 1: removed none, added none; the id is the hex short id,
`{ Psyche core Secondary 38de5b }`.

Under choice 2:

Removed:

"flow id: { Psyche core Secondary <id> }."

Added:

"flow id in its word form: { Psyche core Secondary <words> }."

Lands in the Nexus: `crates/flow-nexus/src/title.rs`. As it stands, the
title is `Psyche.{ Fable 38de5b }`:

```
let model = self
    .model_name
    .model_display_name()
    .ok_or_else(|| TitleRefused::UnmappedModel(
        self.model_name.clone()))?;
let aspect = match self.aspect { ... };
Ok(NativeTitle(format!(
    "{aspect}.{{ {model} {flow_id} }}")))
```

```
- let model = self
-     .model_name
-     .model_display_name()
-     .ok_or_else(|| TitleRefused::UnmappedModel(
-         self.model_name.clone()))?;
- let aspect = match self.aspect { ... };
- Ok(NativeTitle(format!(
-     "{aspect}.{{ {model} {flow_id} }}")))
+ let Address { aspect, topic, layer } =
+     &self.address;
+ Ok(NativeTitle(format!(
+     "{{ {aspect} {topic} {layer} {flow_id} }}")))
```

Removed with it, whole: the table of model display names (`NamesModel`)
and the refusal `UnmappedModel`. The test line:

```
- "Psyche.{ Fable 38de5b }"
+ "{ Psyche core Secondary 38de5b }"
```

Under choice 2 the test reads
`"{ Psyche core Secondary wordWordWord }"` and the title writes the
flow id in its word form (Proposal 2).

`signal-flow/ethos/signal.ethos`: a launch names its metaflow, so the
launch profile carries the address where it carried the aspect:

```
- LaunchProfile.{ ... Aspect PowerLevel ... }
+ LaunchProfile.{ ... Address PowerLevel ... }
```

Lands in the short-term tools:
`primary/tools/main-flow-mode/native-main-flow-launch-shared.mjs`, the
launchers' shared code (JavaScript). As it stands, a topic is
capitalized and core is left out of the title:

```
- // A topic is a dense PascalCase short name:
- // letters only, leading capital.
- export const TOPIC = /^[A-Z][A-Za-z]*$/;
- export const CORE_TOPIC = 'Core';
+ // A topic is a camelCase name, uncapitalized.
+ export const TOPIC = /^[a-z][A-Za-z]*$/;
+ export const CORE_TOPIC = 'core';
```

```
- return topic === CORE_TOPIC
-   ? `{ ${aspect} ${layer} ${flowId} }`
-   : `{ ${aspect} ${topic} ${layer} ${flowId} }`;
+ return (
+   `{ ${aspect} ${topic} ${layer} ${flowId} }`);
```

The comment above it, «The Core topic is left out of the title.», goes.

Ruling:

1. The title carries the hex id (flow dea0ba, 2026-10-03, the word id
   after a minimum viable product); land the code as shown.
2. The title carries the word id (flow 5578cc, 2026-10-03; flow d4ae97,
   2026-10-07); land the sentence and the code with the word form.
3. Land the short-term change only; the Nexus title waits.
4. Neither.

### Proposal 6: a flow knows where it was asked for

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«A layer is Primary, Secondary, Tertiary or Quaternary». As it stands:

"A layer is Primary, Secondary, Tertiary or Quaternary, in every
aspect; the layer decides the model, declared once in Flow as
configuration and changed only over its meta socket. A launch names the
metaflow, the context modules composed into its prompts, and a brief of
a small paragraph; the Nexus composes the prompt from its module
registry, checking each module's hash against its source."

The meta socket, in that sentence: the Nexus's privileged connection,
the one through which its configuration is changed.

Source: flow 9993b5, 2026-09-17.

Removed: none.

Added, at the end:

"Every flow carries where it was asked for: the flow, session and turn
that requested it, found by Flow, so why it was started is read in that
transcript."

Lands in the Nexus: the record exists as `OriginClue.{ FlowId
SessionId TurnId }` in `signal-flow/ethos/signal.ethos`, but the
requester writes it into its Start request:

```
- StartRequest.{ LaunchProfile OriginClue }
+ StartRequest.LaunchProfile
```

`crates/flow-nexus/src/launching.rs`, start:

```
- let origin = request.origin_clue.clone();
+ let origin = self.caller_origin(peer)?;
```

`caller_origin` is new: it builds the origin from the caller Flow finds
(Proposal 4).

The short-term tools record no origin today.

Ruling:

1. Land the sentence and the code changes.
2. Land the sentence only.
3. Neither.

### Proposal 7: why the word flow

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«Flow is the Nexus that manages flows». As it stands:

"Flow is the Nexus that manages flows. A flow is one run of a voice; the
component is named for what it manages. A flow the living asks for is
launched, properly and surely. Flow holds the lock on flows."

Source: flow 4ddc321d, 2026-08-26.

Removed: none.

Added, after «A flow is one run of a voice;»:

"a flow is a flow of thought, and an intelligence is many of them, so
agent, a word that carries one subject, names none of them;"

Lands in no code.

Ruling:

1. Land it.
2. Not in vision-flow.

### Proposal 8: the messenger holds a flow's messages while it refreshes

File: `psyche-context/skills/vision-flow.md`, a new heading after «A
replaced session is reaped by the refresh itself». The paragraph above
it, as it stands:

"Reaping belongs to the refresh event, not to a later sweep. A
refreshed flow takes the replaced end out of receiving messages, so a
dead end is never left registered and addressable."

Source: flow d68c82, 2026-10-13.

Removed: none.

Added, under choices 1 and 2:

"## Messages wait while a flow refreshes

The short-term tools carry messaging. When a flow reaches its context
limit it is marked in transition, and from then its messages are
queued, not delivered, so it can refresh rather than spin on new ones."

Added also under choice 2, the machine's proposal, not the living's
words:

"Its successor receives them, oldest first."

Lands in the short-term tools: `messenger-clj/src/messenger_clj/core.clj`
already holds a send to a route marked in transition (a *route* is
the messenger's record of where a flow runs; *held* means stored and
not delivered):

```
(defn in-transition? [route]
  (or (:transition route)
      (= "transition" (:state route))))
...
(when (in-transition? raw-stored)
  (held! flow :InTransition request stored))
```

Nothing marks a route in transition, and nothing gives the held
messages to anyone. Added to the same file, under choices 1 and 2:

```
+ (defn begin-transition! [flow]
+   (save-route! flow
+     (assoc (load-route (registry) flow)
+            :transition true)))
```

Added also under choice 2, the machine's proposal:

```
+ (defn end-transition! [flow successor]
+   (doseq [request (held-in-transition flow)]
+     (send-request! successor request
+                    false nil))
+   (retire! flow))
```

`save-route!` and `held-in-transition` are new: one writes the route
back, the other reads the held messages back as requests, oldest first.
`end-transition!` runs once the successor is registered.

`primary/tools/context-refresh-hook.mjs` (JavaScript), which warns a
flow at its threshold, marks it as it warns, under choices 1 and 2:

```
  if (measurement.state !== 'threshold')
    return {state: 'unknown', measurement};
+ beginTransition(identity.seatTarget);
```

`beginTransition` is new; it calls the messenger's `begin-transition!`.

The Nexus side already stands in vision-flow.md: «a metaflow under
refresh queues what arrives until its successor has started».

Ruling:

1. Land the heading, the paragraph and the marking code.
2. As 1, and also the machine's proposal: the successor receives the
   queued messages, oldest first, with `end-transition!`.
3. Land the paragraph only; the code waits.
4. Neither.
<!-- to-the-living:end -->
