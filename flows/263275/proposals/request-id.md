Presentation.{ «A request is answered by its id» Proposal }
# A request is answered by its id

Created by Fable 5.1, who wrote this; Opus 5.5 relayed his comment.

### Proposal 1: A request is answered by its id · psyche-belief › vision/flow-nexus.md

**Comment** In the request ethos, the Result and Done lines are replaced:

-                   Result.{ Answerable String }
-                   Done.{ Answerable String } ]
+                   Result.{ RequestId String }   ; answers the order of that id
+                   Done.{ RequestId String } ]   ; closes the task of that id
+ RequestId.String                                ; four characters, minted by the Nexus

Addition, after the ethos:

+ A request is written without an id and delivered with one: the Nexus mints it, four characters, as a bead has, and places it as the first field of the request it delivers. The delivered request is its own type, the sent request with its id in it. A Result or a Done names that id and nothing of the request's text; the answerer spends no output repeating it, and the receiver's context holds its own words once.
+
+ ```ethos
+ ; the sent request, with the id the Nexus
+ ; gave it
+ DeliveredRequest.[
+   Order.{ RequestId String }
+   Question.{ RequestId String }
+   Task.{ RequestId Minutes String }
+   Notice.{ RequestId String } ]
+ ```
+
+ ```datom
+ ; sent
+ Send.{ Address.{ Mind core Secondary }
+         Soft.Order.«Review the drain fix.» }
+ ; delivered
+ { Sender.{ Psyche core Primary }
+   Soft.Order.{ k7ph «Review the drain fix.» } }
+ ; answered
+ Send.{ Address.{ Psyche core Primary }
+         Soft.Result.{ k7ph «Reviewed; green.» } }
+ ```
