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
projects directory. Witnessed by me after Mind Sol effa1b found it: a Codex
flow ID is characters 23 to 29 of its session UUID with hyphens removed,
extended on collision; checked on 893603, 0ab019, effa1b. Rollouts live under
the Codex sessions directory by date, and one flow may span several files.
Herder records no session per pane, so Mentci keeps a small registry of flow
ID to session file, written at launch (Mind Sol's finding). So Mentci finds any flow's conversation by globbing its flow ID.
Mentci shows only the living's turns and the flow's final responses, the
same selection the transcript-as-log vision names for the archive layer.

Provenance, from Mind Sol effa1b's source read of both formats (their
report): a user turn in a transcript does not prove the living wrote it,
since flows prompt each other into the same slot. Codex final = assistant
phase final_answer with matching task_complete, event_msg duplicates
suppressed; Claude final = mainline stop_reason end_turn text, tool_use text
partial. So the conversation view carries a source kind on every turn, and an
input of unknown origin is shown as unknown, never as the living. The
messaging vision holds the eventual discriminator: once every flow speaks
datom, non-datom input is psyche input. Several native sessions per logical
flow need an explicit durable association; Herder lacks native session IDs
per pane.

## Ruled

2026-09-19, the living's comments: Unity Web talks to the daemon and may
run next to it. Mentci talks to Persona, there is no "instead": fork 5 is
ruled against my proposal; Mentci does not read Herder or transcripts
itself. Talking through Unity marks the message as psyche. Verbatim in
`flows/c8d79f/vision/`. The living asked for a Unity Web POC from Mind
Astra; brief in `mind-astra-poc-brief.md`.

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

### Fork 7. Which Mentci daemon, reopened

Mind Sol sized the forward alignment: a daemon-stack rewrite, not a repin.
Their numbers: locked build fails with 158 Criome errors; direct surface
mentci 15 files / 4,298 LOC, criome 38 files / 22,148 of 22,280 LOC,
mentci-egui 9 files / 2,467 LOC, signal-mentci-client 4 files / 747 LOC;
forward migration 8,000 to 15,000 changed lines across 60+ files, about
30,000 LOC to review. Cause: the current contracts replace the retired
frame types with generated Query and Response and a portable Signal. Their
witness. No code changed.

Proposal, revised: a fresh Mentci daemon on the current contracts carrying
only release one: roster view, conversation view, send request, web
surface. Criome and the approval surface stay out while security is open,
and return when the Criome crate is on the current contracts. The old daemon
is retired, not migrated. Alternatives: migrate the whole old stack forward
first, at the size above; or a throwaway server outside Mentci, fastest,
then replaced, against the ruling that Mentci is the server.

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

How the two transcript formats differ line by line: Mind Sol is on it. Whether the phone is enrolled on
the Tailnet: not checked. The Mentci daemon does not build at its pinned
revisions: Mind Astra reports `cargo test --locked` failing on API mismatch
between the daemon's old pins and the newer signal contracts mentci-lib
already pins; repair is dependency alignment. Their witness, not mine. How a web shell reaches a Nexus socket:
a WebSocket bridge is my assumption, not a witnessed mechanism.
