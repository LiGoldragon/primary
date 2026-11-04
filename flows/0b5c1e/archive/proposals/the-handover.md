Superseded by flows/f54886/proposals/the-handover.md

Presentation.{ «The handover» }

# The handover

*Design by Fable, written by Sonnet 5.5*

Tentative: the design is the Psyche core Primary's, not yet ruled. The Warning is for the version after 0.48.

### Proposal 1: The handover is a broad overview · psyche-belief › vision/remembering.md

**Comment** One paragraph replaced: handover-as-book and its composition go; the line that makes them unnecessary is the overview. The module's other line, that a refreshed flow receives the raw logs named at its launch, stays. Tentative.

+ ```mermaid
+ flowchart TB
+     subgraph B["remembering as it stands"]
+         b1["the flow that had the conversation"] -- "composes his words by ancestor" --> b2["Handover book"]
+         b2 -- "he reviews as psyche" --> b3["reviewed file"]
+         b3 -- "is the first prompt of" --> b4["successor"]
+     end
+     subgraph A["remembering proposed"]
+         a1["raw logs"] -- "pass so a flow may write" --> a2["its handover, a broad overview"]
+         a3["Psyche core Primary"] -- "is its main user" --> a2
+         a2 -- "starts fresh" --> a4["successor"]
+     end
+ ```

- A flow is refreshed after its landings: what he approved is landed and live before the handover is written, and the handover holds only what is not landed. The flow that had the conversation writes it, in his words verbatim, composed in inline quotes into what he wants and nothing else, by ancestor, each section marked with the model and the process that made it. It is published as a book of its own kind, `Handover.{ «title» }`, which he reviews as he reviews psyche; the successor's first prompt is that file as reviewed.
+ A flow is refreshed after its landings: what he approved is landed and live before the handover is written, and the handover holds only what is not landed. A handover is a broad overview of what the flow is still trying to do, and only that: no chronology, no commands run, no revisions listed, no opinion to impose. The flow writes it itself, and the successor starts fresh from it with a fresh point of view. The raw vision and notion logs pass to a flow so that it may write its handover; the Psyche core Primary, the flow that speaks with the living, is its main user.

### Proposal 2: The Nexus warns, then hands over the file · psyche-belief › vision/flow-nexus-v1.md

**Comment** Threshold gains Warning; Event gains Warned; the refresh paragraph is rewritten to match. Types the paragraph names are shown as they stand. Tentative.

+ ```mermaid
+ flowchart TB
+     subgraph B["flow-nexus-v1 as it stands"]
+         b1["context passes Threshold"] -- "the flow is told to write its handover" --> b2["flow"]
+         b2 -- "its handover is the first prompt of" --> b3["successor"]
+     end
+     subgraph A["flow-nexus-v1 proposed"]
+         a1["Tokens left falls to Warning percent"] -- "Nexus sends HardAbrupt Notice" --> a2["flow"]
+         a2 -- "writes" --> a3["flows/id/handover.md"]
+         a3 -- "Nexus gives, as first prompt" --> a4["successor"]
+         a5["no file"] -- "successor starts from" --> a6["its definition alone"]
+     end
+ ```

#### Memory, as a block

  ```ethos
  Memory
  [ flow:[ Complex ComplexName FlowName FlowId
           Address Message Event ]
    herdr:[ Pane ] ]
  [ Definition.Complex
    Flow.{ FlowId Address Pane
           State.[ Running Idle Ended ]
           Vector<Event> }
    Queue.{ Address Vector<Message> }
-   Threshold.{ Model.String Tokens.Integer }
+   Threshold.{ Model.String Tokens.Integer
+               Warning.Integer }  ; percent of Tokens left
    Answer.[ Succeeded Failed ] ]
  ```

#### Signal, as a block

  ```ethos
  Signal
  [ flow:[ Complex ComplexName FlowName FlowId
           Address Brief ModuleName Message
           Request Priority Tool Harness ] ]
  [ Define.Complex                     ; add or replace one
    Undefine.ComplexName
    Describe.ComplexName               ; one definition, read back
    Definitions                        ; the names defined
    Launch.{ ComplexName FlowName Brief }
    Stop.FlowId
    Send.{ FlowId Address Priority Request }
    Say.{ ComplexName Request }        ; the living, to a speaker
    Report.{ FlowId Event }            ; from a harness hook
    Subscribe ]                        ; events, as they happen
  [ Defined.ComplexName
    Undefined.ComplexName
    Described.Complex
    Listed.Vector<ComplexName>
    Launched.FlowId
    Stopped.FlowId
    Sent.[ Delivered Queued ]
    Said.[ Delivered Queued ]
    Reported
    Subscribed
    Refused.[ UnknownComplex.ComplexName
              UnknownFlow.FlowName
              NoRoute.{ FlowId Address }
              NoBelief.Vector<ModuleName>
              Unenforceable.Harness         ; Restricted, harness cannot
              HerdrDown BeliefDown
              Running.Address ] ]
  [ Event.[ Started Idle Working Ended
            Responded.String            ; the response, whole
+           Warned                      ; Warning reached
            Threshold ] ]              ;   context past its mark
  ```

#### Types the warning is made of, as they stand

  ```ethos
  Library
  [ flow:[ FlowId Address ComplexName ] ]
  [ Priority.[ HardAbrupt MiddleAbrupt Soft ]
    Request.[ Order.String Question.String
              Living.{ Context.String    ; what his words were about
                       Verbatim.String }  ; his words whole
              Result.String Notice.String ]
    Sender.[ Flow.FlowId Living Nexus ]
    Message.{ Priority Sender Request }
    Waking.Vector<Message> ]           ; a queue delivered whole
  []
  []
  ```

#### The refresh paragraph and the warning it sends

- A perma flow is refreshed when its context passes its model's threshold, configured per model in the Flow Nexus: the flow is told to write its handover, its successor is launched with the same definition, the handover as its first prompt, and the queue that gathered meanwhile; the predecessor ends. The address stays; the flow id changes. An ephemeral flow past its threshold takes no new work and ends when its work ends.
+ A perma flow is refreshed when its context passes its model's Threshold, configured per model in the Flow Nexus. When the Tokens left fall to Warning percent, the Nexus records Warned and sends the flow a HardAbrupt Notice naming its handover path, flows/<id>/handover.md. At the refresh the successor is launched with the same definition and the queue that gathered meanwhile; its first prompt is that file, or, with no file, its definition alone. The predecessor ends. The address stays; the flow id changes. An ephemeral flow past its threshold takes no new work and ends when its work ends.
+
+ ```datom
+ ; the Nexus warns flow 7
+ Message.{ HardAbrupt Nexus
+           Notice.«Write your handover at
+                   flows/7/handover.md» }
+ ```
