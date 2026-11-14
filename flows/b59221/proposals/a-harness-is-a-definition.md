# A harness is a definition

*Created by Opus, drafted by Sonnet.*

## Removed, from vision:flow-nexus-v1

```ethos
  Harness.[ Claude Codex ]
```

Unnecessary beside: a Harness is a defined value (its features and each feature's effect), not a name in a closed list.

```ethos
  Member.{ FlowName Harness ModelName Effort
```

Unnecessary beside: a Member names its harness by HarnessName.

```ethos
  Define.Complex                     ; add or replace one
```

Unnecessary beside: Define takes a Complex or a Harness.

## Added, to vision:flow-nexus-v1

A harness is a definition like a complex: its features, and each feature's effect on the launch, a flag or a variable. The Nexus holds no harness; a harness is added, replaced or removed alone, as a complex is.

```ethos
  HarnessName.String
  Effect.[ Flag.String
           Environment.{ Name.String
                         Value.String } ]
  Feature.{ Name.String
            Effect }
  Harness.{ HarnessName
            Features.Vector<Feature> }
  Member.{ FlowName HarnessName ModelName Effort
```

```ethos
  Define.[ Complex                   ; add or replace one
           Harness ]
```

```datom
Define.Harness.{
   claude
   [ { Bash
       Flag.«--disallowedTools Bash» }
     { ClaudeMd
       Environment.{
          CLAUDE_CODE_DISABLE_CLAUDE_MDS
          1 } } ] }
Defined.claude
```
