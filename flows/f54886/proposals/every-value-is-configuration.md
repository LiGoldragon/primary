Presentation.{ «Every value is configuration» }

# Every value is configuration

*Created by Fable.*

Intent, from his words: "we only set them for third-party tools we are forced to use; we ourselves never use environment variables in our own systems." Lands without his review, on his word.

### Proposal 1: Every value is configuration · psyche-belief › intent/context.md

**Comment** Where a value comes from is a layer's context, so the line lives here. It says what a value of ours is; a variable has one place left, the third-party program.

  ## Every layer carries its own context

+ ## Every value is configuration
+
+ A system of ours takes every value as typed configuration or as a field of the datom it is given. A variable is set only for a third-party program, and the value set is itself configuration.

```datom
+ ; the metaflow name picks the sockets
+ flow-nexus main 'Send.{ … }'
```

+ ```mermaid
+ flowchart TB
+     v["a value a system of ours takes"] --> c["typed configuration"]
+     v --> d["a field of the datom it is given"]
+     t["a third-party program"] -- "is given" --> e["a variable, itself configuration"]
+ ```
