# Unity conversation client on Mentci: first release

Design proposal by Psyche Fable (flow c8d79f), 2026-09-18, revised after the
living's two artifact comments the same evening. Every fork below is framed
with my proposal first. Nothing here is built yet. Comment on any card
without Send to Claude, then tell me in the terminal "read comments".

## Revision record

First draft called the server "Unity server" and the phone app "Unity
client". The living ruled on the artifact: Mentci is the server, the mind
tool, the input device of our world; Unity is a client to it. Fork 1 is
accepted: web first, on a trusted node, Tailnet authentication. Security is
open for the prototype, which defers the Criome bootstrap and the
secret-holder question. Persona sits behind Mentci. Verbatim in
`flows/c8d79f/vision/operational-mentci.md`. Mentci was already named the
mind tool on 2026-08-13: a daemon carrying the central logic, distinct from
its front-ends, which are often not Rust. The daemon exists: the mentci
repository holds `mentci-daemon`, a Nexus with SEMA schemas, started from one
`meta-signal-mentci` Configure frame, keeping canonical UI state and letting
clients subscribe to projected views, with `signal-mentci` as its contract and
`mentci-lib` as the model every client shell shares. Last commit 2026-09-12.
Read by me from the checkouts' READMEs, not run.

## How we talk until the app exists

Artifact comments reach a cloud agent, not this flow. The interim that works
today: comment on the page without Send to Claude, then say "read comments"
in my terminal. I pull every thread and log your words verbatim. Plain
comments never notify me. Typing in the terminal directly needs no nudge.

## What the first release is

Unity Web: a page served by Mentci on a trusted node, reached over the
Tailnet from the phone or the laptop, that shows the live flows and lets the
living read and speak to any one of them.

Roster: every live flow with name, seat, state, and last activity.
Conversation: the living's turns and the flow's final responses, oldest
first, live-updating. Compose: text or speech, delivered to the chosen flow.
Push: the flow's reply arrives without reloading. Nothing else in release
one: no reports, no comment threads, no secrets, no other people.

## The pieces and how they connect

```
  phone / laptop                     trusted node on the Tailnet
  +-----------------+   Tailnet     +---------------------------------+
  | Unity Web       |<============>| Mentci, the mind tool            |
  |  (later: Unity  |  WebSocket   |  serves Unity Web               |
  |   Slint, Mentci |              |  roster  <---- herdr agent list |
  |   TUI, anyone's |              |  history <---- transcripts      |
  |   client)       |              |  send    ----> messenger        |
  +-----------------+              |  permission: open, prototype    |
                                   |  later: Persona behind it       |
                                   +---------------------------------+
                                          |              |
                                   herdr agent prompt    tail .jsonl
                                          v              ^
                                   +-------------+  +-------------+
                                   | flow panes  |->| transcripts |
                                   | Claude/Codex|  | per session |
                                   +-------------+  +-------------+
```

The Tailnet is the closed network and, for the prototype, the whole of the
authentication. Mentci is not a new process: it is the existing daemon with
two new projected views, roster and conversation, and one new request, send. Herder gives the roster and
the delivery, the messenger proof of concept gives judgement and logging,
transcripts give history. Anything that speaks to Mentci is a Mentci client;
Unity is the client people will know by name.

## Two shapes, one built now

Shape B, now: a Unity client connecting to the laptop's Mentci runtime.
Shape A, later: the full Unity app carrying its own Linux and its own
Mentci. Both named by the living. Release one is shape B on a trusted node.

## History comes from transcripts, and the mapping is already deterministic

Witnessed by me: a Claude flow ID is the first six hex digits of its session
UUID, and the transcript is the file named by that UUID under the Claude
projects directory. Reported by Psyche opus 4a2502 as witnessed: a Codex flow
ID is the first eight hex digits of its session UUID, rollouts live under the
Codex sessions directory by date, and one flow may span several rollout
files. So Mentci finds any flow's conversation by globbing its flow ID.
Mentci shows only the living's turns and the flow's final responses, the
same selection the transcript-as-log vision names for the archive layer.

## Ruled

Fork 1, first face: Unity Web now, served by Mentci on a trusted node with
Tailnet authentication. Unity Slint later, and Mentci TUI possible.

Forks 2 and 3, secrets and bootstrap: deferred. Open security for the
prototype. When the Slint client arrives, a new key's access request appears
on the laptop's Mentci, which asks to add that key and give it permission.

## Still open, with my proposal on each

### Fork 4. The flow's reply reaches you from its transcript, not from the flow

Proposal: Mentci tails the flow's transcript and pushes each new final
response. Your turn appearing in the transcript is the read witness the
messaging design wanted. Alternative: flows post replies to Mentci through
the messenger, a skill obligation on every flow and a second copy of every
reply.

### Fork 5. Mentci reads Herder and transcripts directly for now; Persona later

Proposal: in release one Mentci talks to Herder and the transcript files
itself. When Persona manages the clusters and layers, Mentci asks Persona
instead and Herder becomes Persona's concern. Reason: Persona's repository is
stale by the living's own record, and the app should not wait on it.
Alternative: Mentci speaks only to Persona from the start, and Persona grows
a roster and transcript face first.

### Fork 6. Which trusted node

Proposal: the laptop the living is at, since the living said "the laptop's
Mentci runtime" and it already holds the transcripts and Herder. Reason:
transcripts and panes are local files and local processes; a remote node
would need them synced. Alternative: a cluster node with the transcripts
mirrored to it.

### Fork 7. Grow the existing Mentci daemon, or stand up a quick separate server

Proposal: grow the daemon. `signal-mentci` gains a roster view, a
conversation view keyed by flow ID, and a send request; the daemon fills the
views from Herder and transcripts and forwards send to the messenger; Unity
Web is a thin shell over `mentci-lib`'s model, reached through a WebSocket
bridge on the daemon's socket. Reason: the daemon's whole shape is clients
subscribing to projected views, which is exactly roster and conversation,
and every later client, Slint or TUI, inherits the same views for free.
Alternative: a separate small server that reads Herder and transcripts and
serves a page, faster to first light, then thrown away or merged into Mentci.

## What ships, in order

1. Mentci daemon gains the roster and conversation views, filled from
   Herder and transcripts, and serves Unity Web on the Tailnet. Read only.
2. Compose: sends go through the messenger to the chosen flow. The living's
   turn shows in the conversation when the transcript shows it.
3. Push: live updates from transcript tails; phone notification when a flow
   finishes a turn.
4. Unity Slint client, with the new-key permission request on Mentci.
5. Criome-signed sessions, when security stops being open.

Steps one and two make the terminal optional. I propose Codex Astra builds
one and two as one piece.

## What I do not know

Whether every Codex pane derives its flow ID the same way: one pane carries
a six-character ID neither I nor 4a2502 could derive. How the two transcript
formats differ line by line: uncompared. Whether the phone is enrolled on
the Tailnet: not checked. Whether the Mentci daemon builds and runs today:
its README read, the binary not run. How a web shell reaches a Nexus socket:
a WebSocket bridge is my assumption, not a witnessed mechanism.
