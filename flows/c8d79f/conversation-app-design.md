# Unity conversation app on the Tailnet: first release

Design proposal by Psyche Fable (flow c8d79f), 2026-09-18, for the living to
rule on. Every fork below is framed with my proposal first. Nothing here is
built yet. Comment on any card without Send to Claude, then tell me in the
terminal "read comments" and I will fetch them.

## How we talk until the app exists

Artifact comments reach a cloud agent, not this flow. The interim that works
today: comment on this page without Send to Claude, then say "read comments"
in my terminal. I pull every thread with the comments action and log your
words verbatim. Plain comments never notify me, so the terminal nudge is
required. Typing in the terminal directly is the other route and needs no
nudge. Voice into the terminal is the same as typing for me.

## What the first release is

One structured conversation surface, reachable from the phone and the laptop
over the Tailnet, that shows the live flows and lets the living read and
speak to any one of them.

Roster: every live flow with name, seat, state, and last activity.
Conversation: the living's turns and the flow's final responses, oldest
first, live-updating. Compose: text or speech, delivered to the chosen flow.
Push: the flow's reply arrives without reloading. Nothing else in release
one: no reports, no comment threads, no secrets, no admission of other
people.

## The pieces and how they connect

```
  phone / laptop                     cluster node on the Tailnet
  +-----------------+   Tailnet     +---------------------------------+
  | Unity client    |<============>| Unity server                    |
  |  roster         |  WebSocket   |  session auth (Criome key)      |
  |  conversation   |              |  roster  <---- herdr agent list |
  |  compose        |              |  history <---- transcripts      |
  |  Criome key     |              |  send    ----> messenger        |
  +-----------------+              +---------------------------------+
                                          |              |
                                   herdr agent prompt    tail .jsonl
                                          v              ^
                                   +-------------+  +-------------+
                                   | flow panes  |->| transcripts |
                                   | Claude/Codex|  | per session |
                                   +-------------+  +-------------+
```

The Tailnet is the closed network: only enrolled devices reach the server at
all. The Criome key is who you are on top of that: it signs a challenge per
session. The server is the only new process. Everything under it exists
today: Herder for the roster and delivery, the messenger proof of concept for
send judgement and logging, and transcripts for history.

## History comes from transcripts, and the mapping is already deterministic

Witnessed by me: a Claude flow ID is the first six hex digits of its session
UUID, and the transcript is the file named by that UUID under the Claude
projects directory. Reported by Psyche opus 4a2502 as witnessed: a Codex flow
ID is the first eight hex digits of its session UUID, rollouts live under the
Codex sessions directory by date, and one flow may span several rollout
files. So the server finds any flow's conversation by globbing its flow ID.
No index to build. The server extracts only the living's turns and the
flow's final responses, which is the same selection the transcript-as-log
vision names for the archive layer.

## The four forks, with my proposal on each

### Fork 1. First face: web page now, Slint later, both under the Unity name

Proposal: the first face is a web page served by the Unity server on the
Tailnet, opened in the phone's browser. The server and the Criome login are
built once and do not change when the Slint client arrives. The Slint client
replaces the page, keeps the server. Reason: the web page is a day of work
and gets you talking to flows; Slint on the phone is a packaging project
first. Alternative: Slint from the start, accepting the delay.

### Fork 2. The server is the messenger's home, not the secret holder

Proposal: the Unity server holds the roster, the conversation history it has
read, and the session table. It routes sends through the messenger. It does
not hold secrets and does not decide admission: the Tailnet decides who can
connect, the registered Criome public key decides who is the living. The
secret-holder role from the secrets vision stays a separate node later.
Alternative: one server for everything, simpler to deploy, harder to trust.

### Fork 3. Bootstrap: one manual confirmation, then key-signed sessions

Proposal: the Criome key pair is generated on the phone. On first connection
the server shows the key's short fingerprint on a machine you already trust,
in the terminal of a flow. You say yes there, once. The server stores the
public key. Every later session: server sends a nonce, phone signs it, server
checks the signature and issues a session token that lives until the app
closes. Not bulletproof: a stolen unlocked phone is a session. Secure enough:
the Tailnet gate plus a signature nobody else can make. Alternative: pair by
scanning a code shown on the trusted machine, same trust, more UI.

### Fork 4. The flow's reply reaches you from its transcript, not from the flow

Proposal: the server never asks a flow to report back. It tails the flow's
transcript and pushes each new final response to the app. This gives a real
read witness for free: your turn appearing in the transcript is the delivery
receipt the messenger design wanted. Alternative: flows post their replies to
the server through the messenger, which adds a skill obligation to every
flow and a second copy of every reply.

## What ships, in order

1. Server reads the roster from Herder and the history from transcripts, and
   serves the web page on the Tailnet. Read only. Tailnet gate only.
2. Compose: sends go through the messenger to the chosen flow. Your turn
   shows up in the conversation when the transcript shows it.
3. Criome key: fingerprint bootstrap, nonce-signed sessions.
4. Push: the page updates live from transcript tails; phone notification
   when a flow finishes a turn.
5. Slint client replaces the page.

Steps one and two are what makes the terminal optional. Step three is what
makes it yours. I propose Codex Astra builds one and two as one piece once
you rule on the forks.

## What I do not know

Whether the flow ID of Codex panes is always derived the same way: one Codex
pane carries a six-character ID that neither I nor 4a2502 could derive. How
the two transcript formats differ line by line: uncompared. Whether Tailnet
enrollment of your phone already exists: not checked. Which node the server
should live on: not named by you yet.
