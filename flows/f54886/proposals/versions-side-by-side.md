Presentation.{ «Versions side by side» }

# Versions side by side

*Created by Fable.*

His words: "the raw CLI is named by its component and then suffixed with the version, so it would be flow-0.44. The flow by itself is really just a wrapper that redirects to one or another version. Flows will be able to call the flow by version just by calling the right CLI, and then we can have all of these Nexuses deployed in parallel without any problem. If it doesn't work you can deploy another version and take out the one that doesn't work." The concept; the deploy itself is a bead. Lands without his review, on his word.

+ ```mermaid
+ flowchart TB
+     d["the declaration"] -- "one unit per version" --> a["flow-0.44"]
+     d -- "one unit per version" --> b["flow-0.48"]
+     w["flow, the wrapper"] -- "points at one" --> b
+     f["a flow"] -- "calls a version by its CLI" --> a
+     f -- "or the wrapper" --> w
+     x["a version with problems"] -- "is removed; another is added" --> d
+ ```

### Proposal 1: Versions side by side · psyche-belief › vision/versioning.md

**Comment** Stable and next were two; the concept is any number, each its own unit and its own CLI, chosen by name. Which flow runs on which is state, moved by signal, outside the declaration.

- ## Stable and next
+ ## Versions side by side
  
- Every Nexus runs as a stable and a next, each declared in Nix and each on its own sockets; the stable is declared with the Nexuses it pairs with, as the fallback. A configuration names which of the two a new flow or a refresh starts on, and a running flow keeps running where it is. When every flow has moved onto next, next becomes stable and the newer version takes next. An upgrade is never all-or-nothing: the stable is there to fall back on, and a big change carries a countdown rollback that is cancelled once the new stack is seen working. Before the first deployment there is nothing to roll back to, and the system rolls forward.
+ Every version of a Nexus is its own declared unit, on its own sockets and store, and as many run at once as are wanted: two, three, five, since they are cheap to run. Each version has its raw CLI, named by the component and the version, `flow-0.44`; the bare name, `flow`, is a wrapper that points at one version. A flow calls a version by its CLI. Which flow runs on which version is state, moved by signal, outside the declaration. A version that proves to have problems is removed from the declaration and another added; the versions beside it keep running.

```sh
+ flow-0.48 'Send.{ … }'   # this version
+ flow 'Send.{ … }'        # the one the wrapper points at
```

### Proposal 2: The raw CLI carries its version · psyche-belief › vision/nexus.md

**Comment** The repository line named the CLI by the component alone; the component name is the wrapper, the version is the CLI.

- `<nexus>` is the repository holding the Nexus; `signal-<nexus>` its wire vocabulary; `meta-signal-<nexus>` the owner's vocabulary, always present, since configuration flows through it. The CLI is `<nexus>`.
+ `<nexus>` is the repository holding the Nexus; `signal-<nexus>` its wire vocabulary; `meta-signal-<nexus>` the owner's vocabulary, always present, since configuration flows through it. The raw CLI is `<nexus>-<version>`; `<nexus>` is the wrapper that points at one version.
