# Naming plan and process authentication -- findings

## 1. Naming plan (Messenger / Orchestrator, noun vs verb)

Most direct hit, this flow's own vision:

`flows/6cc91b/vision/messenger.md` ("Whatever message is called, Messenger or
the noun, use that for the messaging"), psyche, STT, verbatim:

> Yeah, on your first point, the message was also slated to be called
> Messenger or Messenger. I think also, orchestrate was to become
> orchestrator, but it looks like we've been leaning more towards the noun
> lately, because psyche, orchestrate, or what was the plan anyway? Whatever
> it is called, we should use that for the messaging.

Same file, earlier entries (psyche, STT, verbatim): "A hook that sends my
prompt to the other harnesses" (no name yet); "A small model runs the
open-source harness with a really simple job: the messaging"; "Talk through
Claude; the messenger tells the other half" -- first use of "messenger" as
the job's name.

Corroborating, not ruling: `flows/019fe728/vision/agentIntercom.md:21,30-31`
(psyche, verbatim) -- "which is Messenger and Orchestrator, which are not
ready to be used yet... I think Agent Intercom has a server called
Orchestrator, so there may be some confusion there" -- flags a name
collision with Agent Intercom's own component, not a plan.
`flows/024bc7/vision/router.md:5` (psyche, verbatim) uses "messenger"
associatively while discussing the router, not as a naming ruling.

**No general psyche ruling on "noun vs verb" as a naming policy was found**
beyond the 2026-09-13 statement above. Every landed component name (Orchestrate,
Nexus, Sema, Signal, Psyche, Router -- see `Vision/nexus.md`, `Vision/sema.md`,
`Vision/orchestrate.md`, `vision-raw/archive-rustComponentArchitecture.md`
2026-08-14) is already a noun, but none of those entries state noun-vs-verb
as a deliberate rule -- they just introduce noun names. The "plan" the living
asks about appears never to have been written down as a general rule, only
enacted case by case; 2026-09-13 is the only place the living names the
pattern ("we've been leaning more towards the noun lately") and rules that
whatever name lands, use it for messaging. The crate is still named
`message` on disk (`/git/github.com/LiGoldragon/message/`) -- no rename has
landed.

## 2. Process authentication (peer credentials / provenance)

Also already logged in this flow, `flows/6cc91b/vision/agentAuthentication.md`
(psyche, STT, verbatim):

> Also, there was a concept somewhere that has maybe landed in one of our
> components, but maybe not in production. It was supposed to check which
> process was actually using the tool. Essentially, we could authenticate or
> secure the layer between agents to a pretty high degree, even on the
> computer itself. There are also multiple layers to do that with, like
> where every harness runs in its own sandbox...

and: "We can enforce that even at the system operating system layer, where
the whole messaging layer and spawning new harnesses layer would be
authenticated at multiple layers, sandboxed, and controlled by more highly
permissioned nexuses." No other psyche/Vision entry on this was found.

### Code

**`message` crate, CODE, production route.**
`/git/github.com/LiGoldragon/message/src/provenance.rs:1-218`. Doc: "Provenance
is never accepted from a caller payload -- it is minted here from the
operating-system trust boundary: the accepted connection's kernel-vouched
`SO_PEERCRED` credentials classify the origin, and the sender's agent
identity is resolved by walking the peer's `/proc` ancestry against the
process pins the registry already holds... the start time defeats pid
recycling." `OriginPolicy::origin_for_connection` (~L48) classifies
owner-uid/non-owner-uid/TCP; `SenderResolver::resolve_unix` (~L114) walks
`/proc/<pid>/stat` ancestry (`ProcessAncestry::matching_pin`, ~L150) against
registered pid+start-time pins -- exactly "which process is actually using
the tool." Wired live: `message/src/engine.rs:48-58`, `MessageEngine::handle`
`Query::Submit` calls both on every submission -- production, not a fixture.

**`criome` daemon, CODE, production route, narrower.**
`/git/github.com/LiGoldragon/criome/src/daemon.rs:399-436`,
`MetaSocketAuthority`: "the daemon reads `SO_PEERCRED` on every accepted meta
connection and serves only the Unix user that owns the socket... kernel-
enforced rather than path-secrecy-only." `authorize()` (~L422) is a uid-only
gate (owner vs not), not per-process identity resolution. Similar peercred
checks recur at lines 626, 639 (not fully read).

**`triad-runtime`, CODE, shared primitive.**
`src/process.rs:22-97` safely wraps `rustix::net::sockopt::socket_peercred`
("no payload claim can forge it") -- what both crates above build on.

**`router` crate, CODE, known gap noted.**
`src/forward_attestation.rs:5`: "`SO_PEERCRED` dies at the TCP hop, so the
kernel's local vouching is [...]" -- flags that this scheme doesn't survive a
network hop.

**Contract/stubs, CODE, not implemented.**
`persona/src/bin/wire_emit_message_reply.rs:101` and
`signal-message/src/generated/signal.rs:309` carry a typed
`PeerCredentials`/`ResourceKind::PeerCredentials` unimplemented case in the
wire contract. `spirit/src/schema/daemon.rs:140` references the pattern in a
schema doc, not an enforcement site. `forge/src/uds.rs:13`:
`todo!("bind UDS socket; SO_PEERCRED check; return listener")` -- unbuilt.

**Verdict:** the living's memory is accurate -- it landed, in `message`'s
`provenance.rs` (full ancestry resolution, live in `engine.rs`) and more
narrowly in `criome`'s meta-socket uid gate; both are production routes, not
fixtures. Not implemented: the broader "sandboxed, multi-layer, higher-nexus-
controlled" picture -- `forge`'s stub and `router`'s cross-hop note are the
open pieces.

## Agent Intercom MCP server

Path: `/git/github.com/dataforxyz/agent-intercom-claude/README.md`. Per its
own README (agent-authored, not psyche): a cross-harness, same-machine
messaging system for coding agents -- Pi, Codex, Claude Code, and OpenCode
adapters share one local broker and protocol so sessions discover and
message each other across harnesses; this repo is the Claude Code adapter
(shared `pi-intercom` protocol v3), with durable per-session outboxes
replayed on reconnect and two local transports (`native`, bridging Claude
Code's cross-session Unix socket protocol, and `mcp`, the plugin/inbox/
Monitor path), defaulting to `auto`. Grew from Nico Bailon's `pi-intercom`.
`vision-raw/agent-intercom.md` holds only a one-line notion ("we're also
going to have to set up intercom") -- a notion, not a ruling.
