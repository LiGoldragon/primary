# The single-reply example and its concrete contract
Created by Astra; source retrieval by Luna; boundary verification by Sol.

## Review question

The local proposal adds the exact Belief ordinary single-reply contract to `vision:belief-nexus-v1`: one preparation/router boundary, then checked request and connection into fallible unary execution. Preparation owns malformed-request evidence; Subscribe and meta retain their existing paths. The accompanying local proposal gives all types and the exact authored Rust.

The reviewed general example instead takes only Connection and returns Outcome. Which relation should the two modules state? The alternatives below are proposals, not a claim that either has been approved.

## Existing lines — vision:nexus-v1

The whole example below is the exact existing code whose disposition is in question. Under the relocation alternative these lines are removals and are rendered red; under refinement they remain.

```ethos
Library
[ signal:[ Input Output Error ]
  std:[ Connection ] ]
[ Translator.{ NexusSocket.String }   ; the socket of the Nexus it speaks for
  Caller.{ ProcessId.Integer          ; the connection's
           UserId.Integer }           ;   peer credentials
  Call.{ Caller Input }               ; what the translator sends in
  Outcome.[ Answered                  ; one reply written back
            Unreadable.Error          ; the text was not an Input
            NexusDown ] ]
[ Serving.[ serve.{ [ Connection ] [ Outcome ] } ] ]
[ Translator.[ Serving ] ]
```

## Alternative A — local refinement

### Addition to vision:nexus-v1, immediately before the existing example

> This example names completed single-reply service observations at the connection boundary. A component's concrete service contract declares how request preparation and fallible execution compose to produce those observations. The Belief ordinary single-reply contract separates preparation from checked execution and retains native failure evidence in process.

The existing example remains. The exact local addition is the accompanying proposal into `vision:belief-nexus-v1`.

## Alternative B — relocate the concrete example

### Removal from vision:nexus-v1

<pre style="color:red"><code>Library
[ signal:[ Input Output Error ]
  std:[ Connection ] ]
[ Translator.{ NexusSocket.String }   ; the socket of the Nexus it speaks for
  Caller.{ ProcessId.Integer          ; the connection's
           UserId.Integer }           ;   peer credentials
  Call.{ Caller Input }               ; what the translator sends in
  Outcome.[ Answered                  ; one reply written back
            Unreadable.Error          ; the text was not an Input
            NexusDown ] ]
[ Serving.[ serve.{ [ Connection ] [ Outcome ] } ] ]
[ Translator.[ Serving ] ]</code></pre>

### Addition to vision:nexus-v1, at the same position

> A translator's service contract declares request preparation, execution and failure evidence. The Belief ordinary single-reply contract is declared with the Belief Nexus; its successful domain response remains the caller's reply.

The accompanying exact Belief contract lands in `vision:belief-nexus-v1` as the concrete example. The generic three-case example is replaced rather than silently treated as that new signature.
