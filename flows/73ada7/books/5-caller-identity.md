<!-- to-the-living:start -->
Presentation.{ «How Message learns who is calling» }

## The case

A flow sends through the Message CLI, and Message needs to know which metaflow sent, because that metaflow is the Sender Flow checks the route with. The caller is a process. Flow's buildable design names it Process, the pid together with the kernel's start time of that pid, so a pid the system has reused for another process is told apart; Flow answers Identify.Process by walking that process's ancestors up to the harness and matching a flow's recorded Process, returning its metaflow or Unidentified.Process. What is open is where Message gets the Process from. Message's design reads it from the kernel: on the accepted connection the kernel gives the pid of whoever is on the other end of the socket, and Message hands that to Flow. vision-nexus words it otherwise: the CLI identifies the process that called it and carries that identity in the message. Message's design reports that reading the kernel is how the Message in production finds its caller today; the next Message and Flow are in development, none of it in production. Either way the start time can reach Flow. That a Process written into the message by the CLI is something the caller states, which any program on the socket could state falsely unless the Nexus checks it against the kernel, is this flow's inference. So is the reading that the kernel's pid is the CLI's own process, whose ancestors Flow walks in either option.

## Distillation

### D1. Where a Nexus gets its caller's process, in vision-nexus

Target: `psyche-skills/skills/vision-nexus.md`, the paragraph at line 56, which opens "A CLI turns text into Signal and nothing more" and goes on "A CLI speaks to one Nexus, opens no store, stays thin". Only its second clause changes; the paragraph before it names the meta CLI component-meta, and the section «Signal only» follows.

**Option (a), the Nexus reads the kernel.**

Removed: it identifies the process that called it and carries that identity in the message, so a Nexus knows its caller by the process, never by a claim.

Added: it carries no identity of its caller. A Nexus reads its caller's process from the kernel on the accepted connection, the pid and the kernel's start time of that pid, and so knows its caller by the process, never by a claim.

Rests on: flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/callerIdentity.md:7 (2026-09-16), on checking the socket of the process to identify who used the CLI; flows/8904b1/vision/skills.md:136 (2026-09-28), on knowing the caller not by trusting an ID the flow put in the message but from the process that called; flows/b7ba00/vision/callerIdentity.md:7 (2026-09-26), on Message asking Flow which flow used the CLI, without anyone saying who they are. Message's design section 6 (flows/73ada7/reports/build/message-design.md:308-330) builds this, unruled.

**Option (b), the CLI carries the identity.**

Nothing removed from the clause, which stays as it stands. Added after it: The identity the CLI carries is a Process, its caller's pid and the kernel's start time of that pid, a standard part of Signal that every Nexus reads the same way.

Rests on: the approved line itself, psyche-skills/skills/vision-nexus.md:56 (landed 2026-10-02); flows/8904b1/vision/skills.md:134 (2026-09-28), on the CLI identifying the process and passing it into the message; flows/b7ba00/vision/callerIdentity.md:7 (2026-09-26), on the CLI giving the information in the signal as a standard thing in Signal; flows/b49251/handoff/psyche-medium-v1/modules/sources/efa157/vision/callerIdentity.md:7 (2026-09-16), on an optional standard part of the signal library telling the Nexus whether it has the process id; flows/9993b5/vision/callerIdentity.md:7 (2026-09-17), on identifying the process in the CLI part and keeping the chain of which process launched the call. Flow's buildable design gives the Process it would carry (flows/f5a6e9/reports/flow-buildable-design.md:75-80 and 423-428), unruled; that the CLI would fill it, and that it would be a standard part of Signal, is this flow's reading of those records.

**Ruling D1.** (a) The Nexus reads the kernel. (b) The CLI carries it. (c) Amend, by line.

## Voice

One choice. Message has to know which process called it, so Flow can name the sending metaflow. Message's design asks the kernel, which tells it who is on the socket. vision-nexus says the CLI works it out and puts it in the message, and on the 26th and the 28th you said the CLI gives it in the signal, and also that it should not rest on what the caller says. A has the Nexus ask the kernel; B keeps the CLI carrying it. Either way it carries the start time Flow now wants. Which one? This flow's reading: anything put in the message is the caller's word, unless the Nexus checks it against the kernel.
<!-- to-the-living:end -->
