# Programs: the Energy translator's own record

As declared (energy-nexus branch ethos-565bc8, `ethos/programs.ethos`, generated into `crates/translator/src/generated/programs.rs`):

```ethos
Memory
[]
[ Programs.{ CodexProgram.Option<String>        ; the stored root of energy-translator.rkyv, format version 1
             FlowProgram.Option<String>         ; the Flow Nexus client the reminder is sent through
             ClaudeCredentials.Option<String> } ] ; the Claude credentials file the usage is read with
```

Where it lives: `<State>/energy-translator.rkyv`, under an envelope (magic `ENXTRNSL`, version 1); the earlier bare archive upgrades whole. A new memory is all `None`.

Who writes it: the translator alone, from the meta surface. `Configure.Program.{ Codex|Flow <path> }` and `Configure.Credentials.<path>` arrive at the meta translator, are applied to a candidate copy, saved, and only then made the one in use (`configure`, translator lib.rs about line 355). The daemon never sees or holds it.

Who reads it: the translator alone, at each emission. `codex_call` spawns the Codex program for the app-server reading; `Emittable for ClaudeUsage` reads the credentials path to call the usage endpoint; `Emittable for Send` runs the Flow client for the reminder. A missing value makes that emission Down, or "unconfigured" for Codex.

So it is the configuration of the translator's emissions, held in the process that makes them, written only through the meta surface, one value at a time.
