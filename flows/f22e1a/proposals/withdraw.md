Presentation.{ «A sender withdraws its own request» Proposal }

# A sender withdraws its own request

Created by Fable 5.1, on the living's words.

### Proposal 1: Withdraw · psyche-belief › vision/flow-nexus.md

::: comment
His words: «Don't we have an operation to turn off a notification like that? We should.» A task's reminder kept firing for a task its recipient would never close, since the task was superseded and the recipient asleep. Only the recipient's Done closed a task; the sender had no word. A request belongs to its sender until it is answered, so the sender may take it back: the reminder stops, and the recipient is told, so that it does no superseded work.
:::

+ A sender withdraws its own open request by the id the Nexus minted for it. The withdrawal cancels the task's reminder and queues a notice to the recipient that the request is withdrawn, so that a flow waking to it does not act on it. A request already answered, or sent by another flow, is not the sender's to withdraw and the Nexus refuses.

```ethos
+ Withdraw.RequestId                             ; input: the sender takes back its request
+ Withdrawn.RequestId                            ; output: the reminder cancelled, the recipient told
+ Refused.[ NotSender.RequestId                  ;   the request was sent by another flow
+           Answered.RequestId                   ;   a Result or Done already closed it
+           UnknownRequest.RequestId ]           ;   no such id
```

```datom
+ ; the sender, after the task was superseded
+ Withdraw.k7ph
+ Withdrawn.k7ph
+ ; delivered to the recipient when it next wakes
+ { Sender.Nexus Soft.Notice.«Withdrawn by its sender: Task.{ k7ph … }» }
```
