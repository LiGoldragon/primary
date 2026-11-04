# Handover of b06449, appended to the handover of 383169

Created by Fable, the main flow itself, first-degree, 2026-11-04. Read 383169's handover whole first; this holds only what changed after it. Unreviewed.

## Where things stand

The side-by-side move is done: all seats Awake on the HarnessFlags build of origin/main (flow-configured-0.44.0, unit flow-nexus-harnessflags, sockets /run/user/1001/flow-harnessflags/, store flow-harnessflags), the old Nexus stopped. The hand-written unit still runs; the CriomOS-home switch bead was narrowed to the flow unit alone and then stopped by his order: no more patching of the defective Nexus. The target now is one newer build with every open fix in it, repository cleaned (worktrees merged, main the one line), deployed declaratively from CriomOS-home as a new versioned unit beside the running one, seats moved by signal, old unit removed from the declaration when empty. Mind core owns the build; the core Secondary choreographs; inventory of open fixes and worktrees owed to me first. Mind found flow main heavily dirty in sending/waking/delivery, owner unknown; versionZero to be asked, else preserved on a branch.

Open fixes for that build: delivery into a working seat (every kind answers Queued while a seat is mid-turn, subagent-wait included; nothing reaches it until its turn ends); MiddleAbrupt, Psyche.Said and ObserveSends fail in the profile CLI with the rancor opaque error, the build's own CLI at its store path answers (ObserveSends streams); Curriculum empty records (SuccessorUncomposable RecordMissing on every refresh); the heartbeat; the presentation prompt as typed configuration; nothing read from the environment; HarnessFlags as the harness declaration; Living inline; Custom remembering refusing a Primary whose handover is a file. Bead primary-vgvi holds the delivery fix.

## Landed today on psyche-belief main, on his word

Harness messaging tools out: --disallowedTools SendMessage,ListAgents on all 34 Claude entries (plus the artifact three except the bookmaker and the Field publisher); the deny list in primary/.claude/settings.json. knowledge:flow-messaging, bound to all 46 metaflows. vision:flow-nexus: the presentation paragraph removed; the SendableRequest enum with Living inline. vision:flow-nexus-v1: Living.{ Context.String Verbatim.String } in place of Words. vision:ethos: a defined type is carried bare, no holder struct. vision:nix-builds: a flake input is the bare URL, the lock its pin. vision:criomos home-unit line landed then reverted: everything declarative is already the rule.

## Books up for him, eighteen proposals by subject (flows/b59221/proposals)

Proposals by subject; No environment; What Nix declares (versions in Nix as units, one per version, no stable pointer, state outside); The upgrade protocol (far); Messaging dissolves into the Flow Nexus; Permanent flows (was Job flows: Continuity.[ Permanent Ephemeral ], handover the Primary's alone); Default modules; The handover is a file; Logging his words is removed; A comment on the chat; Unity, a notion; A harness is a definition; A flow knows its metaflow; A new metaflow is told by replaying definitions; Rehearse in the Signal; What a metaflow is; A vector carries a name; Flows send before they spawn (with the roster). The commented books The Flow Nexus (step 5, v1 and v2) are withdrawn as proposals.

## His rulings today, in his words where short

A metaflow: "all of the flows and all of the flow complexes of a particular unit... the equivalent of what people think of today when they think of an agent: a thing they can talk to... You can have multiple metaflows on a single host and they're all running on the same Flow Nexus"; it defines the relationships between its complexes. Metaflow.{ MetaflowName Complexes.Vector<ComplexName> Routes.Vector<Route> Speaker.ComplexName }, Route.{ From.ComplexName To.ComplexName }, tentative. Speaker alternatives discussed: one speaker; open; a conversant complex; addressed per message (Unity).

Nix: "cluster data is just data that is needed to get the hosts and the users set up"; metaflow definitions "cannot live in Nix because it's too stateful a system"; versions of the Flow Nexus are declared in Nix, add one to start, remove when done, "all of the stateful transition is done outside of Nix"; long term a system with an upgrade protocol.

Conduct: a comment on my chat is on my work, answer in code; "Stop being windy"; "when I ask you why you did something, I need an answer"; "I'm not interested in talking about anything except vision and intent and psyche"; a book with nothing added or removed is not a proposal; "an excessive number of artifacts can also have its own type of problems"; his orders go down as they are said, as the kind that lands now, "nobody waits on you"; Perma is Permanent; name vector types; flows send before they spawn, a subagent last resort, cheap for a Primary to send.

Unity is the interface to Manji; Mentci unknown to me.

## Defects met

DeliverAll answered Released. SendChanged prints sender and recipient as { Psyche  Primary }, topic empty. The bookmaker published a book at another's link. A whole-family Configure from a stale read wiped 13 flags (Field core); one writer now.
