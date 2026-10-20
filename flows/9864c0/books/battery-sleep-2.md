Presentation.{ «Battery drain in sleep, second edition» }

# Battery drain in sleep, second edition

### Proposal 1: mind-context › knowledge/hardware.md, a new file

+ ---
+ description: Hardware facts that change how a host is configured.
+ dependencies: []
+ ---
+ 
+ ## Ouranos, a ThinkPad T14 Gen 5 Intel
+ 
+ Ouranos, a ThinkPad T14 Gen 5 with Intel Meteor Lake, sleeps by s2idle only. Its battery lasts in sleep only when the chip reaches S0ix; a sleep with zero S0ix residency drains almost as if awake.
+ 
+ On Meteor Lake the Ethernet controller, driver e1000e, can hold the chip out of S0ix. On this model it shares wake line GPE 6D with the USB controller, so turning off USB wake alone leaves Ethernet free to wake the chip.
+ 
+ The DDR5 memory temperature sensor, driver spd5118, fails at resume with error -6. This is a resume error, not the drain.
+ 
+ A sleep fix is declared in CriomOS for its model and proven by one real sleep whose S0ix residency is above zero.

### Proposal 2: psyche-context › vision/context-modules.md

  A context repository holds one section of role modules per layer, Primary, Secondary, Tertiary and Quaternary, and may hold sections for specialized topics.
  
+ ## One hardware module, for now
+ 
+ For now, hardware knowledge lives in one hardware module. When it grows past a set size, the living is warned through a book.
+ 
+ ## Modules visible to the flows that need them
+ 
+ A context module may be visible only to the flows that need it; a hardware module is one such.

## psyche-context › vision/criomos.md

## CriomOS

CriomOS is a declarative operating system: nobody edits a file on a host.

A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy.
Every hotfix in place is removed and replaced by that fix.

CriomOS is made more modular; an anatomy of it shows what should be taken out.

## Nix code

Every store path in Nix code is the output of evaluating a package, a flake input or an option; Nix code never names a store path.

## Hardware

CriomOS has a hardware type, so that it supports several kinds of hardware, the Librem 5 Linux smartphone among them; a module may be gated on it.
A fix that only some hardware needs is a value in the cluster data, marked by the chip or part that makes it necessary.
A library reads the cluster's list of its hardware and answers, by processor, model and variant, which fixes a computer needs.

## Harnesses

The harnesses and their desktop apps are kept stock in at least one version, under their ordinary executable names.

## Services

A new service lives in CriomOS.
A service is updated by bringing it up at its latest version.

## Desktop

A new artifact does not open a browser tab on its own.
