<!-- to-the-living:start -->
Presentation.{ «Short term and long term» }

# Short term and long term

```
   today, per area
        |
        v
   short-term vision: what runs now,
   named so
        |
        | the nexus lands, declared
        v
   long-term vision: the nexus, used
   everywhere
        |
        v
   short-term removed with its
   documentation
```

## Crystallization

Each proposal below is a section for the vision module of its area, in two tenses, resting on your records; the short term is named so, the long term is unmarked. Below each, what readjusting to it would touch.

### Proposal 1: messaging

```
  hm-send (messenger-clj)   short term
     | flow id, six chars
     v
  Herdr pane
  - - - - - - - - - - - - - - - - - -
  Message Nexus              long term
     | metaflow id, three fields,
     | resolved by Flow
     v
  the seat
```

Target: vision-messaging.

Messages move through the Message Nexus, addressed by the metaflow's three-field identifier; the runtime resolves it to the current flow. Short term: the messenger-clj commands carry messages addressed by flow id, until the Message Nexus runs.

Readjusts: the messenger-clj repository and the five messaging stores, four of them dead; the hooks and launcher scripts that call hm-send; the Message Nexus source, eighty-seven commits ahead of what is deployed and not running.

### Proposal 2: flow launch and lifecycle

```
  launcher scripts x4, Herdr panes,
  harness hooks               short term
     |
     v
  Flow Nexus: launch, name, deliver,
  stop, retire, hook          long term
```

Target: vision-flow.

Flow launches, names, delivers to, stops and retires every flow; a launcher, a messenger or a hook calls Flow for these. Short term: the Primary launcher scripts and the harness hooks do these beside Flow, until Flow 0.26 is deployed and called.

Readjusts: four launcher scripts; the hooks; the messenger's route registry; Flow deployed at 0.14 against source at 0.26; the Flow store, last written five days ago.

### Proposal 3: locking

```
  orchestrate CLI -> Orchestrate Nexus
     (as deployed)             now
  session lock in messenger-clj
     -> Flow                   long term
```

Target: vision-orchestrate.

Locks live in the Orchestrate Nexus. The session lock belongs to Flow. Short term: the session lock sits in the messenger, until Flow holds it.

Readjusts: one lock moved; the least of the gaps.

### Proposal 4: committing Primary

```
  flows commit under turns     gone
     |
     v
  one standing committer,
  woken by a turn-end hook      now
     |
     v
  ?                             long term
```

Target: vision-committing.

Primary is committed only by the standing committer, woken by a turn-end hook when Primary is dirty. Your records state no long-term shape beyond this.

Readjusts: CLAUDE.md, which still says a main flow commits under a turn; the committer's restart unit, defined but not installed.

### Proposal 5: context modules

```
  skills repos -> Curriculum ->
  generated trees in Primary    short term
     |
     v
  context repos -> launcher composes
  the seat's SYSTEM             long term
```

Target: vision-context.

A seat's context is composed by the launcher from the context repositories: psyche, mind, field. Short term: the generated trees in Primary carry the modules, until the launcher composes from the repositories.

Readjusts: Curriculum's generation; the repositories' names; the seat prompt, now in psyche context; every generated tree.

### Proposal 6: books and your interface

```
  artifact pages, comments      short term
     |
     v
  a better interface            long term
     (not yet described)
```

Target: vision-book.

The living reads books and answers by comment. Short term: books are artifact pages in the living messenger, until the interface you named replaces them. Your records do not yet describe that interface.

Readjusts: the book renderer and checker; the comment fetch; how you are reached, stated in one place.

### Proposal 7: psyche records

```
  flows/*/vision files, raw     short term
     |
     v
  annotated psyche in Sema      long term
```

Target: vision-psyche.

Psyche is carried annotated, what is vision, what is instruction, what is a situational intervention, in Sema. Short term: raw records in each flow's lane, untangled by hand, until Sema carries them.

Readjusts: every raw record; the logging rules; crystallization's sources.

### Proposal 8: deployment

```
  home generation from CriomOS-home   declared
  hand-placed links, nix profile
  entries, parallel inputs            short term
     |
     v
  every component declared, one
  source, from main                   long term
```

Target: vision-deployment.

Everything runs as declared, from one source on main; nothing is placed by hand. Short term: the hand-placed messenger links and the parallel Flow and Message inputs, until the declared generation carries them.

Readjusts: the three hand profile entries and the links; the flow-next, flow_2 and message-next inputs; Lojix at 8.1 against 9.0 in source; the four dormant repositories and their state.

### Proposal 9: memory

```
  one store per nexus     now and long term
  (vision-nexus: no central store)
```

Target: vision-nexus.

Each nexus holds its own store; there is no central store. Your records state no Memory root; the Flow source's note that store types wait on one is a machine's, not yours.

Readjusts: nothing in vision; Flow's hand-written store waits on its Memory ethos.

### Proposal 10: models per layer

```
  eight declarations           short term
     |
     v
  one declaration, in Flow    long term
```

Target: vision-model-roles.

One declaration, in Flow, sets the model and effort of every layer, by family. Short term: the declarations in the skill variables, the voice table, Curriculum's roles, CriomOS-home and Flow's defaults, until Flow holds the one.

Readjusts: eight places; Flow's defaults still naming a retired model.

### Proposal 11: patches in others' software

```
  Herdr: quiet hours, allowlist
  Pi: role prompt
  Claude Desktop: patch         short term
     |
     v
  our parts bolted beside, none inside   long term
```

Target: vision-design, beside «Nuts and bolts».

Nothing of ours sits inside another's component. Short term: the Herdr, Pi and Claude Desktop patches, until each is rebuilt as our own part on the component's interface.

Readjusts: the two Herdr patches, the Pi prompt patch, the Claude Desktop patch, the kameo fork.

## Question 1

Your committing record wants the flow id set in the harness environment as the default; vision-flow says no flow declares its own id, Flow knows it by the calling process. Which is the short term and which the long?

## Question 2

Three areas have no long-term statement in your records: committing beyond the standing committer, the interface that replaces books, and memory beyond one store per nexus. Do they stay as the short term stands, with the long term open, or do you give the goalpost now?

## Question 3

The readjustment of code the inventory found, four dead messaging stores, dormant repositories, hand-placed links, parallel inputs, tools reading a dead store, is machine work once the vision above lands. Is it one cleanup, in the order of the gaps, messaging, launch, deployment, models, or area by area as each long-term vision lands?
<!-- to-the-living:end -->
