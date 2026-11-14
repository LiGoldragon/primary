Presentation.{ «The configurator» Proposal }

# The configurator

Created by Fable 5.1, on the living's words of 2026-11-09, from the transcript of the previous Fable flow; edition 2, after his comment.

### Proposal 1: A new module · psyche-belief › vision/configurator.md

::: comment
His design: a tool that turns a configuration datom into the target's own Configuration signal file; a Nexus reads that file before it opens any socket, so it is configured before the first signal reaches it, and the bootstrap over the ordinary socket is no longer needed. The same tool configures the Nexus's CLI, so a tester reaches the place `next` by configuring the CLI, typing no place. One configurator per Nexus, because only a binary compiled with that Nexus's types can actualize its Configuration.
:::

+ ---
+ description: The configurator, the tool that writes a Nexus's or a CLI's configuration as a signal file read at start, is designed or judged.
+ dependencies: [vision-nexus-v1, vision-signal]
+ ---

+ ## A Nexus starts configured

+ A Nexus needs no socket to be configured at start: it reads its configuration directly. The configurator takes a configuration datom and writes it as the target's own Configuration type, in signal, to the target's configuration file. A Nexus starting in its place reads that file before it opens any socket, so the first signal it ever receives is already under its configuration; when the file is absent it writes its defaults there and starts on them. The meta socket keeps its configuration interface whole: every change while the Nexus runs goes through it, one value at a time, and is written back to the file, so a restart finds the configuration it left. The file and the meta socket are two doors to the one configuration.

+ Every Nexus has one configurator, `<nexus-name>-configure`, built from the Nexus's meta signal, since only a binary compiled with the Nexus's types actualizes its Configuration. It configures two targets: the Nexus in a place, and the Nexus's CLI. The CLI's configuration names the place the CLI reaches, so a tester reaches `next` by configuring the CLI once, and types no place.

+ ```ethos
+ Library
+ [ nexus_v1:[ PlaceName CliConfiguration ]
+   meta_signal:Configuration ]                 ; the Nexus's own Configuration type, from its meta signal
+ [ Target.[ Nexus.{ PlaceName Configuration }  ; the Nexus in that place
+            Cli.CliConfiguration ]             ; the Nexus's CLI
+   ConfigurationFile.String ]                  ; where the signal is written
+ []
+ []
+ ```

+ ```sh
+ # the Nexus in the place next, configured before it starts; the names are an example
+ flow-nexus-configure 'Nexus.{ next { [ { Mind core Sonnet } ] 1200 } }'
+ # the CLI, pointed at next: from here every flow-nexus command reaches next
+ flow-nexus-configure 'Cli.{ next }'
+ flow-nexus 'Launch.{ designer fable «Read the book» }'
+ ```

+ ```datom
+ ; the files: one per Nexus per place, one per CLI, both signal
+ ; $XDG_CONFIG_HOME/nexus/next/flow-nexus.signal
+ ; $XDG_CONFIG_HOME/nexus/flow-nexus-cli.signal
+ ```

+ ```mermaid
+ flowchart TB
+     d["a configuration datom"] -- "the configurator actualizes into" --> f["the target's Configuration, as signal, in its file"]
+     f -- "read before any socket opens" --> n["the Nexus, configured from its first signal"]
+     f -- "read by" --> c["the CLI, which reaches the place the file names"]
+     m["the meta socket"] -- "changes one value at a time, written back to" --> f
+ ```

### Proposal 2: Startup takes the file, the bootstrap goes · psyche-belief › vision/nexus.md

::: comment
Configuration and First configuration described a Nexus configured through its sockets, with a bootstrap window on the ordinary socket. The file makes both unnecessary: the Nexus is configured before any socket exists.
:::

- For now, a Nexus starts with no arguments and there is no bootstrap
- binary. Its executable holds a default configuration as a constant. On
- start it looks for its memory at the default location: a memory that
- exists holds the configuration; a memory created new is seeded with the
- defaults. The meta socket carries a Configure interface, and changed
- values are accepted through it.
+ A Nexus starts in its place and reads its configuration file, written by its configurator, before it opens any socket; a file that is absent is written with the executable's defaults. The meta socket carries a Configure interface, and changed values are accepted through it and written back to the file.

- ## First configuration

- A Nexus keeps a standard metadata tree. In it a type records whether
- the meta Configure was ever done; that record is reversed only on the
- meta socket, and while it is unset Configure is accessible on the
- ordinary socket. The tree holds everything standard about the Nexus:
- its socket paths — its own and those of every edge-socket it connects
- to — and whatever else comes up as standard nexus configuration data.
- The built-in default configuration is independent of this and is
- what gives the socket path on which the Configure signal arrives.

### Proposal 3: The CLI's configuration is a signal file · psyche-belief › vision/nexus-v1.md

::: comment
The line landed this morning put the CLI's configuration in a datom file. The configurator writes it as signal, as it does the Nexus's, and a Place gains its configuration root.
:::

- A Nexus reads nothing from the environment: it is started with one datom, its place. Runtime holds its sockets and defaults to `$XDG_RUNTIME_DIR/nexus/<place-name>/`; State holds its memory and defaults to `$XDG_STATE_HOME/nexus/<place-name>/`, `~/.local/state/nexus/<place-name>/` when the variable is unset. Both roots are the CLI's fixed defaults, taken from the standard XDG variables and from nothing else, never an argument. The CLI is `<nexus-name> '<datom>'`: named after the Nexus, and taking the datom and nothing else. Whatever else it knows is its configuration, one datom at `$XDG_CONFIG_HOME/nexus/<nexus-name>.datom`, the place first among its values and more as the CLI gains options. The place name is resolved under the runtime root to the sockets. Two places are two names, and the stable one keeps running while the next is tried; a place is reached by the configuration that names it, so the testing capsule has its own configuration as it has its own sockets and store, and no place is ever typed.
+ A Nexus reads nothing from the environment: it is started with one datom, its place. Runtime holds its sockets and defaults to `$XDG_RUNTIME_DIR/nexus/<place-name>/`; State holds its memory and defaults to `$XDG_STATE_HOME/nexus/<place-name>/`, `~/.local/state/nexus/<place-name>/` when the variable is unset; Configuration holds its configuration file and defaults to `$XDG_CONFIG_HOME/nexus/<place-name>/`. The roots are the CLI's fixed defaults, taken from the standard XDG variables and from nothing else, never an argument. The CLI is `<nexus-name> '<datom>'`: named after the Nexus, and taking the datom and nothing else. Whatever else it knows is its configuration, one signal file at `$XDG_CONFIG_HOME/nexus/<nexus-name>-cli.signal`, written by the Nexus's configurator, the place first among its values and more as the CLI gains options. The place name is resolved under the runtime root to the sockets. Two places are two names, and the stable one keeps running while the next is tried; a place is reached by the configuration that names it, so the testing capsule has its own configuration as it has its own sockets and store, and no place is ever typed.

```ethos
  Library
  []
  [ PlaceName.String                   ; main, next
    Place.{ PlaceName                  ; what every Nexus starts with
            Runtime.String             ; the sockets
-           State.String }             ; the memory
+           State.String               ; the memory
+           Configuration.String }     ; the configuration file
    CliConfiguration.{ PlaceName } ]   ; what the CLI knows besides its datom; grows as the CLI gains options
  []
  []
```

```sh
- # ~/.config/nexus/flow-nexus.datom
- { main }
+ # ~/.config/nexus/flow-nexus-cli.signal, written by: flow-nexus-configure 'Cli.{ main }'
  flow-nexus 'Launch.{ designer fable «Read the book» }'
```
