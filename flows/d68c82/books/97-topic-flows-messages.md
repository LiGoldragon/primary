<!-- to-the-living:start -->
Presentation.{ «Topic flows, a design Fable, and messages from files» }

# Topic flows, a design Fable, and messages from files

### Proposal 1: psyche-context › vision/flow.md

  A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.

+ A main flow hands a specialized topic to a specialized Opus topic flow, a flow specialized to that one topic, instead of doing the topic itself; it keeps track of which topic flows exist.

```
+------------------+
| main flow        |
+------------------+
     |          |
     | hands    | tracks
     | a topic  | which exist
     v          v
+-------------+ +-----------------+
| Opus topic  | | topic flows     |
| flow        | | that exist      |
+-------------+ +-----------------+
```

Ruling: land, amend, or reject.

### Proposal 2: psyche-context › vision/flow.md

  A simplified flow is a kind of flow made for judgment alone: it starts with a system prompt of its own, it has no regular tool, and its response is its message.

+ A topic flow may consult, now and then, a fresh and clean Fable that it uses only for designing. That Fable is a simplified flow: once the topic flow has gathered everything the design needs, it sends it all at once.

```
+------------------------------+
| Opus topic flow              |
+------------------------------+
               |
               | sends everything the
               | design needs, at once
               v
+------------------------------+
| fresh Fable                  |
| (simplified flow)            |
+------------------------------+
               |
               | answers with the design
               v
+------------------------------+
| Opus topic flow              |
+------------------------------+
```

Ruling: land, amend, or reject.

### Proposal 3: psyche-context › vision/model-roles.md

**Alternative 1**

```text
  Sonnet launches Sonnet and Haiku. Opus launches
  Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and
  Sonnet often, and Haiku for small jobs. Fable is main-flow only: no flow
- ever launches a Fable subflow.
+ ever launches a Fable subflow, except that an Opus topic flow consults a
+ fresh Fable for designing alone.
```

**Alternative 2**

```text
  Sonnet launches Sonnet and Haiku. Opus launches
- Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and
+ Sonnet and Haiku, and sometimes Opus, but rarely; an Opus topic flow also
+ consults a fresh Fable for designing alone. Fable launches Opus and
  Sonnet often, and Haiku for small jobs. Fable is main-flow only: no flow
- ever launches a Fable subflow.
+ ever launches a Fable subflow but that consultation.
```

Ruling: land, amend, or reject.

### Proposal 4: psyche-context › vision/messaging.md

  A hash or an identifier in a message is its first six characters.

+ ## A message body is typed or taken from a file
+
+ A message body is typed in the call or taken from a file; a flow does not re-output what a file already holds.
+
+ A call may carry a vector of messages. Each states its own type, and each is typed in or taken from a file, so one call sends a run of messages made of reused content.
+
+ The living's words taken from a file travel as a psyche, with its context typed; they are never put in a msg body.

```
+------------------+   +------------------+
| a file           |   | typed text       |
+------------------+   +------------------+
        |                      |
        | fills                | fills
        v                      v
+--------------------------------------+
| the body of a msg or a psyche        |
+--------------------------------------+
        |
        | travels in a vector, in one call
        v
+--------------------------------------+
| the receiving flow                   |
+--------------------------------------+
```

```sh
# today: one psyche, its words typed in full
printf '%s' '[["why it matters" "his words"]]' |
  FLOW_ID=d68c82 hm-send "Psyche core Primary" \
  --psyches --stdin

# proposed: --messages, a vector of typed entries
FLOW_ID=d68c82 hm-send "Psyche core Primary" \
  --messages --stdin <<'EDN'
[[:psyche "his ruling on topic flows"
  {:file "flows/d68c82/vision/flow.md"}]
 [:msg {:file "flows/d68c82/books/97.md"}]
 [:msg "Rule it, then land what he approves."]]
EDN
```

Ruling: land, amend, or reject.

### Proposal 5: mind-context › inquiry/messenger-files.md, a new file

+ ---
+ description: Which files a message may take its body from, and what the receiver gets, are unsettled.
+ ---
+
+ - Which file paths may a message take its body from? Tried: any path the sender can read; only paths under the workspace root; only a named set of locations such as vision, books and reports. Settled by a call that names a path outside the allowed set being refused, and every body the flows reuse being sent without a refusal.
+ - Does the receiver get the file's content or a reference to it? Tried: the content inserted once into the receiver's prompt; the path alone, which the receiver reads itself with a tool call. Settled by the receiver acting correctly on both, and by the tokens each costs it; a reference may also name a file that has changed since it was sent.
+ - What size limit does a body taken from a file have? Today a message has no character cap, and the only limit the code shows is the Herdr request of one megabyte. Tried: that same limit for the whole call; a smaller cap per file; a reference past a size. Settled by the size above which content in the receiver's prompt does worse than a reference.
+ - How is a psyche verbatim taken from a log file cited exactly? Tried: the file path with the heading of the record; the path with a line range; the path with the quote block's exact text checked against the file. Settled by the receiver being able to confirm the words are byte for byte what the file holds, and a transcription correction in the file being carried or flagged.

```
+----------------------------------+
| a psyche cited from a log file   |
+----------------------------------+
                 |
                 | is located by
                 v
+----------------------------------+
| path, heading or line range      |
+----------------------------------+
                 |
                 | is checked against
                 v
+----------------------------------+
| the exact words in the file      |
+----------------------------------+
```


Ruling: land, amend, or reject.
<!-- to-the-living:end -->
