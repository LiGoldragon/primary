<!-- to-the-living:start -->
Presentation.{ «Back on the grid» }

# Back on the grid

This is the state at about ten on 2026-10-11, after Prometheus came back and Ouranos woke. "Witnessed" means an audit run from Ouranos saw it. "Reported" means a flow said it and no one has checked.

## The hosts

Prometheus booted at 09:38 today. It is the remote builder again: a trial build sent from Ouranos ran on Prometheus and came back (witnessed). It still runs the system from 24 September, older than the current CriomOS (witnessed). Rebuilding it waits on a missing request packet for its four parts (reported by Mind).

Ouranos has run since 26 September. It suspended on 10 October at 17:15 and resumed on 11 October at 09:55. That is about 16.7 hours, not 12 (witnessed in its log). It runs a system that was switched on as a trial that day, not its saved profile; a reboot brings the saved profile back (witnessed).

Zeus has run since 17 September. Its update from 10 October is live but not yet booted into (witnessed). That the update is the current CriomOS is reported by Field.

## The network now

```
          internet
             │
     ┌───────┴───────┐
     │  house router │
     │ (not ours)    │
     └───┬───────┬───┘
   cable │       │ house Wi-Fi
         │       ├──────────┐
┌────────┴───┐ ┌─┴──────┐ ┌─┴─────┐
│ Prometheus │ │Ouranos │ │ Zeus  │
│ builder    │ │ laptop │ │laptop │
└────────┬───┘ └────────┘ └───────┘
         ┆
         ┆ its own Wi-Fi (access point)
         ┆ some clients fail to join
         ▼
     ┌────────────┐
     │ failing    │
     │ client     │
     └────────────┘
```

The house router is not ours. Prometheus is wired to it. Both laptops use the house Wi-Fi, not Prometheus's own (witnessed).

Prometheus's own Wi-Fi works as an access point, and some clients fail to join it. Field's checkpoint: the failing client associates, asks for an address, and Prometheus's address server answers with offers. The client never accepts one and drops after about 18 seconds. The access point reports a transmit power of 3 dBm. No cause is established yet. A flow reported earlier that 3 dBm is a display defect of the kernel's driver, not the real power; that is a claim.

Mind has one worker designing the Wi-Fi fix and another scope for Ouranos's sleep drain. Both wait on Field's evidence.

## What runs on Ouranos

The cluster services are up. No virtual machine is running. The message daemon has failed since 9 October (witnessed).

## The repository

The shared working copy of Primary has diverged from main: 24 commits only here, 101 on main that it lacks, and many files uncommitted (witnessed). Several locks are held by two flows (witnessed).

## Work in flight

- History backport: ordered, not started; no branch exists for it (witnessed).
- Persona contract: Astra is drafting; the choice of root source is open.
- Commit queue: design only; nothing built.
- Flow and Message: on development branches, not on main. Message waits on an integration test (reported).

## Distillation

### Proposal 1: the temporary conditions after arrival

File: `field-skills/skills/compensation-temporary.md`, shown whole as it stands on field-skills main. The NixBuilder-off paragraph, the Ouranos-off paragraph and the placeholder topology sentence are removed. The topology line is added. The front matter is unchanged: a description, "A temporary condition holds: a host, builder, service or network route differs from its standing state for a stated period.", and no dependencies.

Removed:

NixBuilder is powered off from 2026-10-10 until the morning of 2026-10-11. There is no remote builder; build locally. Work continues, slower.

Ouranos, the host of the cluster machine, powers off later on 2026-10-10 for travel. It may come up during the trip when power or internet allows.

The network topology, while it differs from the standing one, is stated here.

Added:

Prometheus is connected to the internet router, which is not ours, and both laptops, Ouranos and Zeus, are connected to the Wi-Fi that Prometheus is connected to through LAN.

Unchanged:

A temporary condition does not stop work: what needed the missing host builds or runs locally, or waits for it; everything else goes on.

A condition's line is removed when it ends.

Ruling 1: keep this wording, or amend it?
<!-- to-the-living:end -->
