<!-- to-the-living:start -->
Presentation.{ «The meta harness has a base» }

## Where things are

«Meta harness» is your word of 2026-10-10. The seats have read it as the tooling that starts and carries seats: the Flow Nexus, the messenger, the launch commands, and the harness hooks that report a seat's events to Flow. Whether that is what you mean is the first ruling below; the drawing uses that reading.

```
  this computer, in production
  +----------------------------------------+
  |  Flow Nexus: admits one user only,     |
  |    its state and socket paths fixed    |
  |  Herdr: started by hand; the declared  |
  |    service is never turned on          |
  |  logins: only the Codex one is carried |
  |    forward; nothing creates a first    |
  |  launch: two paths, the Flow launcher  |
  |    and the Primary scripts; nothing    |
  |    says which a redeployment uses      |
  +----------------------------------------+

  message-test, in development (Nix)
  +----------------------------------------+
  |  throwaway virtual machine             |
  |  Flow + Message + headless Herdr       |
  |  checked by the flake, then discarded  |
  |                                        |
  |  live runner: copies the subscription  |
  |  login file into a temporary home;     |
  |  no API key; never run                 |
  +----------------------------------------+

  wanted
  +----------------------------------------+
  |  one base, from the repositories,      |
  |  deployed the same on any host         |
  |  tests of live flows on an API key,    |
  |  the key a secret the flows never see  |
  +----------------------------------------+
```

The first box is what runs the seats today, each line checked in the configuration by the Flow Secondary's survey: the deployment admits one user and one home, the terminal server that holds every pane was started by hand, no login is created on a fresh host, and two launch paths coexist. A second host has never had it. The second box is Mind's reading of the message-test source, not a run: a Nix-checked virtual machine proves Flow and Message against each other and then disappears; its one live runner reaches a model only by copying the subscription login, has no key provider, and has never been run. Within that repository Mind finds no component and no secret provider for a base on a key; the host configuration and the other repositories were not read. The third box is what your record asks for.

What the Flow vision carries already: Flow sets up and starts a flow; the Capsule makes where a flow runs, first as a semi-sandbox that copies only the credential files; the flow repository is a runtime repository built by Nix, with every skill outside it. What it does not carry: that the whole base, not Flow alone, deploys the same on any host; and that flows under test run on an API key rather than a login. The intent-testing skill today lets a proof of concept run outside a sandbox when it needs a browser login with your credentials; an API key removes that need, so the live test goes into the sandbox like every other.

## Distillation

### Proposal 1 — the base, in vision-flow

File: `psyche-skills/skills/vision-flow.md`, section «What it does», after the Capsule paragraph (line 14).

Above, as it stands:

Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.

The Capsule is the component that makes where a flow runs. Its first embodiment is the semi-sandbox: only the credential files are copied, everything else is recreated, with its own sockets and store, running light models. Later it encrypts the sensitive parts of the filesystem under a volatile key.

Added, after it:

The meta harness is the tooling that starts and carries seats: the Flow Nexus, the messenger, the launch commands, and the harness hooks. It is a base: it works smoothly and deploys the same on any host from its repositories, never a one-off on one machine.

A test that runs live flows runs them on an API key, which is easier to hold than a subscription login. How a subscription is handled is decided later.

Below, unchanged: «## Starting flows».

Source line appended to «## Sources»: `875960 harness` (the record is at `flows/875960/vision/harness.md`, 2026-10-10, relayed from the core Secondary).

Ruling 1: what «meta harness» names. (a) the tooling that starts and carries seats, as in the first paragraph; (b) the message-test harness, the virtual machine that runs Flow, Message and Herdr; (c) both, one base that is deployed to a host and also proven in the machine; (d) something else, in your words. The first paragraph's opening sentence takes the answer.

Ruling 2: the two paragraphs as written or amended.

Ruling 3: the first paragraph says a base deploys the same on any host from its repositories. That reads wider than Flow: it would guide every Nexus and every tool. (a) it stays Vision in vision-flow; (b) it becomes Intent, in an intent- skill on deployment, with vision-flow pointing to it; (c) other.

Following this book if ruling 2 stands, for Mind and Field rather than for vision: who owns the new component, and how the key reaches it as a secret.
<!-- to-the-living:end -->
