<!-- to-the-living:start -->
Presentation.{ «Persona's root and what it does» }

## Where things are

Mind is ready to assign an implementer to Persona, the root of the meta harness, and asks two things before it can: which source is the root, and what the root does. Both are yours to say. This book shows the sources as witnessed and proposes the root's duties from your own records.

```
  one repository, two checkouts, diverged
  +----------------------------------------+
  |  Persona (newer, mid-September)        |
  |    the binary speaks NOTA              |
  |    adds a build step and a generated   |
  |    contract; proposals folder          |
  +----------------------------------------+
  +----------------------------------------+
  |  persona (older, three days before)    |
  |    the binary speaks datom             |
  |    adds an upgrades file and a daemon  |
  |    path Nix refuses to read            |
  +----------------------------------------+
  shared by both: the same flake inputs,
  the same components (router, system,
  harness, message, sema-engine, the meta
  signal); no Sops, no Herdr; in
  production: nothing

  CriomOS today
  +----------------------------------------+
  |  deploys persona-router only, from a   |
  |  separate router repository; no input  |
  |  for Persona or persona                |
  +----------------------------------------+
```

The two checkouts share their first commit and almost everything after it; they are the repository the second edition called dormant since September. The newer one has moved its wire language to something named NOTA, the older speaks datom. Neither is deployed anywhere: CriomOS takes only the router. Mind reads in the source a root engine manager with supervised deployment, transient service units, cross-component tests and isolated credential roots; that is Mind's reading, and it does not say which checkout is meant to go on.

What you have said persona does, in three records: it manages all the clusters and layers by default and keeps a harness instance of each of the triad running, always core, usually primary too (typed, 05c604); its first use is a service that checks all the services and keeps them running, changed through the configuration it takes in or what it is sent (2026-09-23, 6fb948); it makes a backup, knows how to restart the whole cluster, every metaflow, with the right context, runs the monitor jobs, and may move to a backup model when a provider is offline (aa887c). None of this is in a skill yet.

## Distillation

### Proposal 1 — «What the root does», in vision-persona

File: `psyche-skills/skills/vision-persona.md`, the file opened by the second edition of «The meta harness has a base»; this section goes after «The root of the meta harness» and before «Credentials».

Above, as proposed there:

Persona is the root component of the meta harness, the tooling that starts and carries the seats. It has everything it needs in its environment, on a CriomOS installation.

Added:

## What the root does

By default Persona manages all the clusters and all the layers. It keeps a harness instance of each of the triad running: always core, and usually primary, because primary is the more interactive and core the more long-term.

Its first use is a service that checks every service and keeps it running. It is changed through the configuration it takes in, or through what it is sent; nothing else changes until a nexus is added or its behaviour is to change at the root.

It makes backups. It knows how to restart the whole cluster, every metaflow, with the right context. It runs the monitors, and when something has failed or a provider is offline it may act, moving to a backup model.

Below, unchanged: «## Credentials».

Source lines appended to «## Sources»: `05c604 persona`, `6fb948 personaServiceAndNexusImagery-20260923`, `aa887c persona`.

Ruling 1: which source is the root Mind builds from. (a) the newer checkout, Persona, speaking NOTA; (b) the older checkout, persona, speaking datom; (c) neither as it stands: a fresh root built against the design from the records above, taking from the old repository what still serves; (d) other, in your words.

Ruling 2: the section as written, or amended by paragraph.

What Mind calls the root's contract follows from ruling 2 and is Mind's to draft against it: the queries and signals by which Persona is configured, sent things, and asked for status. That draft comes back here as a book before it is built.
<!-- to-the-living:end -->
