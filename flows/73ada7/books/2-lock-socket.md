<!-- to-the-living:start -->
Presentation.{ «Which socket carries the lock» }

## The case

In the next Message and Flow, Message asks Flow for a time-limited lock on a metaflow, then hands Flow the request under that lock, naming the sender. Only Flow writes into a pane. Every Nexus has two sockets: the ordinary socket, which any peer on the host may use, and the meta socket, the Nexus's root user, for configuration and privileged operations. Typing raw text into a pane is meta. Open is which socket the lock and the delivery go through. On the ordinary socket, any process could ask for a lock and hand Flow a request with a sender it names itself, so Flow would have to find the sender on its own rather than take Message's word. On the meta socket, Message holds root on Flow and nothing else can reach a pane. That consequence is this flow's reading of the two designs.

## Distillation

### D1. Which socket carries the lock and the delivery, in vision-flow

Target: `psyche-skills/skills/vision-flow.md`, at the end of «What it does», after the paragraph ending "Flow holds the lock on flows.", before «Starting flows». Nothing removed.

**Option (a), added:** a new paragraph:

Message asks Flow for the lock and hands it a request on Flow's ordinary socket. A request delivered under the lock is an ordinary send; Flow checks the lock and the route and is the only writer into a pane. Writing raw text into a pane is on Flow's meta socket and is not ordinarily reached.

Rests on: flows/1b8ac0/vision/messaging.md:27 (2026-09-21), on raw being meta and locked messages being the ordinary sends; the unruled Flow Signal of f5a6e9's buildable design, which puts Lock, Deliver and Release on the flow socket; vision-nexus «Sockets» (psyche-skills/skills/vision-nexus.md:40-44), which puts privileged operations on the meta socket.

**Option (b), added:** a new paragraph:

Message reaches Flow's lock and delivery only on Flow's meta socket. Message is the one peer with a meta edge to Flow, so no other process can lock a metaflow or place a request in a pane. Flow exposes each of its operations at the authority level it needs.

Rests on: flows/88475f/vision/message.md:63-65 (2026-09-25), on the features Message needs being on the meta socket, so that nothing writes into panes at will; vision-nexus «The graph» (psyche-skills/skills/vision-nexus.md:74), on only some pairs having a meta edge.

**Ruling D1.** (a) The ordinary socket. (b) The meta socket. (c) Amend, by line.

## Voice

One choice. Message locks a metaflow and delivers through Flow. On the 21st you said raw typing is meta and locked messages are the ordinary sends; on the 25th you said to build what Message needs on the meta socket so nothing writes into panes at will. The designs use the ordinary socket. A puts it on the ordinary socket, B on the meta socket. Which one?
<!-- to-the-living:end -->
