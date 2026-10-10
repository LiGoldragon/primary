<!-- to-the-living:start -->
Presentation.{ «The meta harness has a base, second edition» }

## Where things are

Persona is the root of the meta harness: his ruling of 2026-10-10 on the first edition. The persona vision has no skill yet; its records lie raw in many flows, from the machine person of each living person to the service that checks every service. This edition opens that skill with the base, and leaves persona's other records to their own books.

```
  Persona, the root
  +----------------------------------------+
  |  a CriomOS installation, assumed       |
  |  +----------------------------------+  |
  |  |  the environment persona needs   |  |
  |  |  Flow, messenger, launch, hooks  |  |
  |  |  Herdr, the seats' panes         |  |
  |  +----------------------------------+  |
  |  credentials: not bundled; they      |
  |  arrive encrypted, through Nix,      |
  |  from the cluster data               |
  +----------------------------------------+
            |
            v
  live tests: flows on an API key;
  the subscription handled later

  today, on this computer, in production
  +----------------------------------------+
  |  Flow admits one user, paths fixed     |
  |  Herdr started by hand                 |
  |  only the Codex login carried forward  |
  |  two launch paths, none chosen         |
  |  persona repository: dormant since     |
  |  September, slated for this role       |
  +----------------------------------------+
```

The first drawing is his answer: Persona has everything it needs in its environment, on a CriomOS installation; credentials are deployed encrypted through Nix. CriomOS already holds secrets that way, through sops-nix, and declares each node in the Horizon cluster data, so the path he names exists for other secrets and is not yet used for persona's. The second drawing is what runs the seats today, each line checked by the Flow Secondary's survey; the persona repository, last touched in September, names itself the engine manager and integration repository, which is the role his 2026-08-21 record gave it.

Two persona records are needed to define the term before the base can be stated: every living person has a persona, a machine person, which is a thinking machine (his words of 840e42); and one persona is one unified whole that can spawn several machines, while one machine can run parts of several personas (typed, 2026-09-25). They open the file.

## Distillation

### Proposal 1 — a vision-persona skill, opened with the base

File: `psyche-skills/skills/vision-persona.md`, new. Shown whole.

```
---
description: Persona, the root of the meta
  harness, or what it carries, deploys or
  holds, is designed or judged.
dependencies: []
---
```

## What Persona is

Every living person has a persona: a machine person, machina persona, a thinking machine. One persona is one unified whole; it can spawn several machines, and one machine can run parts of several personas.

## The root of the meta harness

Persona is the root component of the meta harness, the tooling that starts and carries the seats. It has everything it needs in its environment, on a CriomOS installation.

## Credentials

Persona's credentials are never bundled with it. They are deployed encrypted, through Nix, from the cluster data.

## Tests

A test that runs live flows runs them on an API key, which is easier to hold than a subscription login. How a subscription is handled is decided later.

## Sources

840e42 persona
752e0f persona
875960 harness
875960 persona

Ruling 1: the file as written, or amended by section; the four sections are numbered by their order.

Ruling 2: «The root of the meta harness» says persona deploys whole on an installation, and «Credentials» says how secrets reach it. Both would guide every component. (a) they stay Vision in vision-persona; (b) they become Intent, in an intent- skill on deployment, with vision-persona pointing to it; (c) other.

The first edition's vision-flow proposal is withdrawn by this one: the base is persona's, and Flow stays one component it carries. Persona's remaining records, among them the triad kept running, the service that checks services, backup and restart, and quota, come in their own books.
<!-- to-the-living:end -->
