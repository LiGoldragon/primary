<!-- to-the-living:start -->
Presentation.{ «Battery drain in sleep» }

# Battery drain in sleep

```
 lid closed: s2idle
     |
     v
 +----------------------+
 | the processor idles; |
 | the system stays on  |
 +----------------------+
     |  every block
     |  powers down?
     v
 +----------------------+
 | yes: S0ix, deep      |
 | idle, a few % a day  |
 +----------------------+
     |
     |  no: one block
     |  holds the chip
     v
 +----------------------+
 | Ethernet controller  |
 | holds it, or wakes   |
 | it on the shared     |
 | wake line            |
 +----------------------+
     |
     v
 +----------------------+
 | zero S0ix: drains    |
 | almost as if awake   |
 +----------------------+
```

Ouranos is a ThinkPad T14 Gen 5 with an Intel Meteor Lake chip. It sleeps only one way, s2idle: the processor idles while the rest stays powered. The battery lasts only when every block of the chip powers down and the chip reaches S0ix, its deepest idle state.

The sleep of the 15th, nine hours long, reached S0ix for zero seconds. On the 10th, twelve hours of sleep took the battery from 90% to 43%.

## What holds the chip awake

| | on Ouranos | others on this model |
|---|---|---|
| Ethernet controller | an active wake source; shares wake line 6D with USB | holds Meteor Lake out of S0ix; fixed with its wake and wake-on-LAN off |
| USB controller | wake off, declared in CriomOS | — |
| wake line 6D | off by hand, in no source | firing in thousands of events |
| memory temperature sensor | fails at resume | resume error only; the system works |

The declared fix turned off USB wake only. The Ethernet controller shares USB's wake line and was left awake.

## The proper fix, under way with Field

```
 Ethernet wake off and
 wake-on-LAN off, in
 CriomOS for this model
     |
     v
 +-----------------------+
 | wake line 6D declared |
 | off only if it still  |
 | fires                 |
 +-----------------------+
     |
     v
 +----------------------+
 | the hand-made switch |
 | removed              |
 +----------------------+
     |  deploy, then
     |  one real sleep
     v
 +----------------------+
 | S0ix above zero:     |
 | fixed                |
 +----------------------+
```

The Ethernet controller is the strongest match, from this model's evidence and others' reports. A real sleep with S0ix above zero is what proves it.

## Crystallization

### Proposal 1: Sleep on Ouranos

File: mind-context/skills/knowledge-sleep.md, new

+ ---
+ description: A laptop drains its battery in sleep, or sleep and wake are checked.
+ dependencies: []
+ ---
+
+ ## Sleep
+
+ Ouranos, a ThinkPad T14 Gen 5 with Intel Meteor Lake, sleeps by s2idle only. Its battery lasts in sleep only when the chip reaches S0ix; a sleep with zero S0ix residency drains almost as if awake.
+
+ On Meteor Lake the Ethernet controller, driver e1000e, can hold the chip out of S0ix. On this model it shares wake line GPE 6D with the USB controller, so turning off USB wake alone leaves Ethernet free to wake the chip.
+
+ The DDR5 memory temperature sensor, driver spd5118, fails at resume with error -6. This is a resume error, not the drain.
+
+ A sleep fix is declared in CriomOS for its model and proven by one real sleep whose S0ix residency is above zero.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
