Presentation.{ «Messaging: a message routes by the metaflow triple» }

# Messaging: a message routes by the metaflow triple

Created by Fable; first composition by Opus

### Proposal 1: vision:messaging · psyche-belief › vision/messaging.md

**Comment** The six entries of the raw record become one statement, placed after the module's first section. The living's later words correct the first reading: the ids are not useless to the runtime, which routes and correlates by them; they are useless to a flow, which never sees them, and a debugging query exposes them when one must be explicit. The query shown is an example of the shape, not its name. The module holds no line on identifiers, so no line is removed.

  ## A message is a datom, and it arrives as one
  
  The message body is a datom that lands in the recipient's prompt as a
  datom-formatted object. The datom is the whole message.
  
+ ## A message routes by the metaflow triple alone
+ 
+ A metaflow triple is { Aspect topic Layer }. A metaflow is a continuation of flows, not one particular flow, and a peer is known only as its metaflow. A message is sent to a triple and arrives from one: the sender's triple is the whole provenance a flow sees, and no flow names its own flow id.
+ 
+ ```datom
+ Send.{ Address.{ Mind flow Secondary } Wake
+   Soft.Order.«Review the book.» }
+ ```
+ 
+ It lands in the recipient as:
+ 
+ ```datom
+ Sender.{ Psyche core Secondary }
+ Soft.Order.«Review the book.»
+ ```
+ 
+ The flow id and the delivery id are backend abstractions: the Flow Nexus routes and correlates by them, and a user never sees them. A debugging query type exposes them when one must be explicit, as one example of its shape:
+ 
+ ```datom
+ Deliveries.{ Address.{ Mind flow Secondary } }
+ [ { Delivery.20084 Flow.a27c64 Sender.{ Psyche core Secondary } Soft.Order.«Review the book.» } ]
+ ```
+ 
  ## Priority is a head on the datom
  
      Priority.[HardAbrupt MiddleAbrupt Soft]
  
  ## Delivery is harness-specific
  
  A pressing message wakes its recipient; a message that only queues carries what may wait.
  
  A request to deliver a recipient's queue delivers every queued message, or nothing when none is queued.
  
  ## An interrupt witness is not a delivery witness
  
  Inducing an interrupt, placing prompt text, submitting it, and the recipient
  consuming it are four separate observations. None of them stands for
  another, and a submission is never a read receipt.
  
  ## A message carries what its reader acts on
  
  A message carries what its reader acts on: what the sender intends, or what it has done.
