Presentation.{ «Messaging: a message routes by the metaflow triple» }

# Messaging: a message routes by the metaflow triple

Created by Fable; first composition by Opus; redone by Fable

### Proposal 1: vision:messaging · psyche-belief › vision/messaging.md

**Comment** A flow thinks of a peer as its metaflow, never as one flow, so the triple is the whole address and the whole provenance; the ids serve the Nexus's own routing and are shown only when debugging asks for them. Every field is its own typed position, so the Ethos carries the shape.

  ## A message is a datom, and it arrives as one
  
  The message body is a datom that lands in the recipient's prompt as a
  datom-formatted object. The datom is the whole message.
  
+ ## A message routes by the metaflow triple alone
+ 
+ A metaflow triple is { Aspect topic Layer }. A metaflow is a continuation of flows, not one particular flow, and a peer is known only as its metaflow. A message is sent to a triple, nothing else, and arrives from one: the sender's triple is the whole provenance a flow sees, and no flow names its own flow id.
+ 
+ Every field of a message is its own typed position; none is carried inside another's string. What lands in a flow is a type of two positions, the sender's triple and the message, and no id is a position of it.
+ 
+ The Ethos:
+ 
+ ```ethos
+ Library
+ []                                          ; imports
+ [ Address.{ Aspect Topic Layer }            ; types: the metaflow triple
+   Sender.Address                            ;   who sent it: a triple, never a flow id
+   Message.[ HardAbrupt.Request              ;   the priority head over the request
+             MiddleAbrupt.Request
+             Soft.Request ]
+   Delivery.[ Queue Wake ]                   ;   queued for the next wake, or woken now
+   Send.{ Address Delivery Message }         ;   what a flow sends: to an address, nothing else
+   Landed.{ Sender Message } ]               ;   what a flow receives: two positions, no id
+ []                                          ; traits
+ []                                          ; associations
+ ```
+ 
+ The datom, sent:
+ 
+ ```datom
+ Send.{ { Mind flow Secondary } Wake
+   Soft.Order.«Review the book.» }
+ ```
+ 
+ The datom, as it lands in the recipient, a Landed:
+ 
+ ```datom
+ { { Psyche core Secondary }
+   Soft.Order.«Review the book.» }
+ ```
+ 
+ The flow id and the delivery id are backend abstractions: the Flow Nexus routes and correlates by them, they are positions of its own records, and a user never sees them. A debugging query type on the meta socket exposes them when one must be explicit, as one example of its shape:
+ 
+ ```ethos
+ Signal
+ [ flow:[ Address Sender Message FlowId LogicalDeliveryId ] ]   ; imports
+ [ ReadDeliveries.Address ]                                      ; queries: one metaflow's deliveries
+ [ DeliveriesRead.Vector<Delivery> ]                             ; responses
+ [ Delivery.{ LogicalDeliveryId FlowId Sender Message } ]        ; types: the ids are positions here
+ ```
+ 
+ ```datom
+ ReadDeliveries.{ Mind flow Secondary }
+ DeliveriesRead.[ { 20084 a27c64 { Psyche core Secondary } Soft.Order.«Review the book.» } ]
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

### Rulings

1. Proposal 1: land · amend · reject
