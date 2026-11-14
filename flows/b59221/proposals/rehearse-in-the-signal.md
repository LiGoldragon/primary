# Rehearse in the Signal

*Created by Opus, drafted by Sonnet.*

## Added, to vision:flow-nexus-v1

The Signal's Launch has a rehearsal: the same input asked as a dry run, answering with the whole command the Flow Nexus would run, and running nothing. The answer is one string, the shell command as the shell is to receive it.

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
  Rehearse.{ ComplexName FlowName Brief }   ; added: a Launch as a dry run
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
  Rehearsed.Command.String           ; added: the shell command, whole
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
```

```datom
Rehearse.{ designer fable «Read the version one book» }
Rehearsed.«herdr --session main agent start … -- --system-prompt-file /…/bundle --model … --effort …»
```
