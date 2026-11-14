Presentation.{ «The CLI takes the datom and nothing else» Proposal }

# The CLI takes the datom and nothing else

Created by Fable 5.1, on the living's words. Approved by him in the chat: «I approve it, so you can have it changed. Who knows, we might want to configure more things, right?»

### Proposal 1: The CLI's configuration · psyche-belief › vision/nexus-v1.md

- The CLI is `<nexus-name> <place-name> '<datom>'`: named after the Nexus; the place name picks the instance, resolved under the runtime root to the sockets. Two places are two names, and the stable one keeps running while the next is tried.
+ The CLI is `<nexus-name> '<datom>'`: named after the Nexus, and taking the datom and nothing else. Whatever else it knows is its configuration, one datom at `$XDG_CONFIG_HOME/nexus/<nexus-name>.datom`, the place first among its values and more as the CLI gains options. The place name is resolved under the runtime root to the sockets. Two places are two names, and the stable one keeps running while the next is tried; a place is reached by the configuration that names it, so the testing capsule has its own configuration as it has its own sockets and store, and no place is ever typed.

```ethos
+ CliConfiguration.{ PlaceName }        ; what the CLI knows besides its datom; grows as the CLI gains options
```

```sh
+ # ~/.config/nexus/flow-nexus.datom
+ { main }
+ flow-nexus 'Launch.{ designer fable «Read the book» }'
```

### Proposal 2: The examples follow · psyche-belief › vision/complex-v1.md

```sh
- # the CLI: the place's name, then one datom
- flow-nexus main 'Launch.{ designer fable «Read the book» }'
- herdr-nexus main 'Prompt.{ { main wQ:pT } «hello» }'
+ # the CLI: one datom; the place is its configuration's
+ flow-nexus 'Launch.{ designer fable «Read the book» }'
+ herdr-nexus 'Prompt.{ { main wQ:pT } «hello» }'
```

```sh
- # the owner's definitions, replayed into a fresh place
- for f in definitions/*.datom; do flow-nexus next "Define.$(cat "$f")"; done
+ # the owner's definitions, replayed into a fresh place, from the capsule whose configuration names it
+ for f in definitions/*.datom; do flow-nexus "Define.$(cat "$f")"; done
```

### Proposal 3: The examples follow · psyche-belief › vision/herdr-nexus-v1.md

- It is built first, because it proves the translator and the CLI alone, and it is kept usable by hand: any flow, or the living, drives a pane through `herdr-nexus main 'Prompt.{ … }'`.
+ It is built first, because it proves the translator and the CLI alone, and it is kept usable by hand: any flow, or the living, drives a pane through `herdr-nexus 'Prompt.{ … }'`.
