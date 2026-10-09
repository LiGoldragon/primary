<!-- to-the-living:start -->
Presentation.{ «The Nexus starts» }

## Distillation

### 1. `psyche-skills/vision/flow-ethos.md`, after the section «What Flow names»

Lines removed: none. Lines added, a line in the Library root and a new section:

```
   Blake3.Bytes<32>             ; Encodable: hex
```

```
## The Nexus starts

Flow is started by datom commands on its meta
socket, one payload at a time. Its configuration
lives in datom files in the repositories that own
it, one file per concern, and the CLI sends them in
succession; nothing is expanded across files. Each
payload lands whole or is refused whole.

Signal                          ; the meta socket
[  flow_ethos:[ Topic Layer Blake3 ] ]
[  Configure.[
      Module.{                  ; the registry
         Subaspect.[
            Vision
            Intent
            Knowledge
            Operation
            Trial
            Compensation ]
         Topic
         Source.{
            Repository.String   ; the containing
            Hash.Blake3         ; source, hashed
            Path.String } }     ; relative inside it
      Model.{                   ; the layer's model
         Layer
         Model.String }
      Threshold.{               ; percent of window
         Layer
         Handover.Integer       ; 20
         Refresh.Integer } ]    ; 40
   Forget.{                     ; a module leaves
      Subaspect
      Topic } ]
[  Configured
   Forgotten
   Refused.[
      Unknown.Topic
      NoSource.Path
      HashMismatch ] ]
[]

Written, one payload file of psyche-skills:

Configure.Module.{
   Vision
   flow
   { psyche-skills
     a3f1…9c2e
     vision/flow.md } }

A module is found by subaspect and topic; its file's
place is Curriculum's to know and check against the
hash on a read or a write. The Nexus composes from
the registry and reads no path a caller writes.
```

Ruling 1: (a) yes. (b) amend the payloads. (c) the hash is another.
<!-- to-the-living:end -->
