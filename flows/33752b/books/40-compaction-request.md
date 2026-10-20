<!-- to-the-living:start -->
Presentation.{ «A guarded compaction request» }

# A guarded compaction request

```
+------------------------------+
| compaction request           |
| Command.{ flow Compact }     |
+------------------------------+
        | arrives at
        v
+------------------------------+
| Flow Nexus                   |
+------------------------------+
        | observes, for the flow
        v
+------------------------------+
| occupancy: tokens in context |
| age: time since launch       |
| last compaction: time since  |
+------------------------------+
        | compares with
        v
+------------------------------+
| configured guard             |
| size, age, interval          |
+------------------------------+
        |
   +----+-----------+
   | under a limit  | over every limit
   v                v
+-------------+  +-----------------+
| refuses:    |  | types /compact  |
| typed       |  | into the flow's |
| rejection   |  | pane            |
+-------------+  +-----------------+
```

Development branch: nothing here is implemented or deployed; implementation is Mind Core Primary's.

## What the request is

A compaction request is a signal to the Flow Nexus naming one flow and the word Compact. The Nexus already receives it (witnessed in the Flow source) and today types `/compact` into the flow's pane after checking only that the flow has a route and a writable pane. Nothing looks at the flow itself. The proposal puts a guard between receiving and typing. The request stays the existing Compact command to the Flow Nexus, now naming a flow or a metaflow; the code landing goes to Mind Core Primary.

A request may name a metaflow instead of a flow: the Nexus resolves the name to the flow awake in it, then guards that flow (inference: the resolution exists for messages, not yet for this request).

A person typing `/compact` into the pane bypasses the guard. The guard covers requests that arrive as signals.

## The three observations

- Occupancy, the tokens the flow's context holds now. Observable today: the transcript's last machine reply records its usage, and input plus cache creation plus cache read is the occupancy (witnessed in a working census tool). Right after a compaction that reply is superseded and occupancy is unknown until the next reply. Whether the Nexus knows a flow's transcript path is not yet checked; without it the occupancy is unknown and the request is refused.
- Age, time since launch. Observable today as the transcript's first timestamp (witnessed). Flow does not record it.
- Last compaction. Observable today as the transcript's `compact_boundary` record, which carries its time and the tokens before and after (witnessed). Flow does not record it.

Short term the transcript is the observation. Long term Flow records launch and each compaction itself: the harness's session-start hook already reaches Flow, and it carries whether the session began fresh or from a compaction; Flow discards that today (witnessed). The harness value names are a claim from its hook documentation, not observed here; whether Codex reports the same is unknown.

## The refusal

The Nexus refuses, with a typed rejection, when occupancy is unknown, when it is under the configured size, when the flow is younger than the configured age, or when the last compaction is more recent than the configured interval. The refusal is a typed rejection, one kind per cause, and each carries the value it observed. No guard configured refuses every request.

## Configuration

The three limits are configuration, fed in as data like the existing handover and refresh thresholds, never constants in the runtime: size in tokens, age and interval in seconds, no value held in the code. Today the Nexus stores those thresholds and nothing reads them (witnessed).

## The case it stops

One witnessed case, this flow's own transcript on 13 October: a `/compact` compacted it from 460,965 tokens to 18,781 at 18:09; a second `/compact` sent at 18:10 compacted the already small flow again at 18:11, from 18,892 to 18,865. The transcript does not record who sent either. The guard refuses exactly the second, and a request aimed at a flow just launched.

## Questions

1. What size, in tokens, must a flow's context reach before a compaction request for it is accepted?
2. How old, in time since launch, must a flow be before a compaction request for it is accepted?
3. How long after a flow's last compaction must a new compaction request wait before it is accepted?
4. When the Nexus cannot tell how many tokens a flow's context holds, as right after a compaction, does the compaction request refuse?
5. Does the same guard, size and age, also apply to a request to refresh a flow by handover?
6. On keeping the Psyche topic flows small: is it each topic flow's context that should stay small, or the number of topic flows?

## Crystallization

File: `psyche-context/skills/vision-flow.md`, under the refresh paragraph (line 58). No lines removed.

As it stands, lines 56-58:

```text
Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
```

### Line 1

Added:

```text
Short term: a compaction request names a flow or a metaflow, and is refused when the flow's context is under a configured size or the flow is younger than a configured age.
```

Ruling: land as written, reword, or reject?

### Line 2

Added:

```text
A compacted flow still carries noise; compaction remains while large contexts cannot be afforded.
```

Ruling: land as written, reword, or reject?
<!-- to-the-living:end -->
