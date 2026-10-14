<!-- to-the-living:start -->
Presentation.{ «Anatomy audit» }

# Anatomy audit

## Figure 1: welds into components that are not ours

```
  Herdr (upstream v0.8.2)
  +--------------------------------+
  | ~~ quiet-hours patch, 817 lines|  unused now
  | ~~ Codex executable allowlist  |  a Flow fact
  |    in agent-start API, 540 l.  |
  +--------------------------------+
  Pi harness
  +--------------------------------+
  | ~~ built-in prompt patched with|  role rule
  |    our role policy             |  = rebuild
  +--------------------------------+
  kameo (actor library)
  +--------------------------------+
  | ~~ our fork, 5 lifecycle       |  under the
  |    commits over upstream       |  harness
  +--------------------------------+
  bolted, not welded: Codex binaries,
  yt-dlp overlay, Claude Code wrapper
```

## Figure 2: our concepts in the wrong component

```
          Flow Nexus (source 0.26)
          launch . name . deliver
          stop . retire . hook
                   |
     nothing calls it; running 0.14,
     CLI on PATH 0.23, they do not
     read each other's messages
                   |
   +---------------+---------------+
   |               |               |
 launcher      messenger        hooks
 scripts x4    -clj             in harness
 compose       route registry   call Primary
 prompt, pick  retire, rebind   scripts and
 skills, mint  move, delivery   hm-send,
 id, title,    lock             not Flow
 register
   = launch       = lifecycle     = signal

 inside Flow itself:
   caller's profile picks skills, model,
     effort, prompt   -> Flow should
   flow CLI runs curriculum, reorders
     skills           -> Nexus work
   Report, Stop, lock release: FlowId is
     a claim in the payload, no peer check
   no Memory ethos: store hand-written
   orchestrate: store decides conflicts,
     no operation or memory part
```

## Figure 3: values welded into the runtime

```
  model + effort per layer, declared in
    voice table (code) . Curriculum roles
    SKILL_VARIABLES   . CriomOS-home list
    Flow defaults crate
    -> five places, they disagree

  cars that start when they have gas:
    reminder hook on every Claude main
      seat, cadence fixed, no off switch,
      launcher says 20, hook file says 1
    Field Luna heartbeat archives,
      deregisters, closes panes; no
      observe-only switch; model in code

  paths and ids in code:
    Flow store moved by rewriting HOME
    census monitor: /home/li paths and
      two recipient ids fixed
  Primary 12 . CriomOS-home 8
  Curriculum 3 . CriomOS 3
```

## Distillation

### Proposal 1: spirit-core, new line

Target: psyche-skills, spirit-core, after the nuts-and-bolts line.

Added: No values in the runtime. The code is the machine that takes the configuration and turns it into the running system; every path, host, id, name, timeout, model and policy is fed in, and every feature has its switch. The one hard fact is the structure of the language itself. A constant that truly is structure stays.

### Proposal 2: vision-flow, new section

Target: psyche-skills, vision-flow, after its last section.

Added:

**Everything that launches, names, delivers to, stops or retires a flow goes through Flow**

A launcher script, a messenger or a hook calls Flow for these; none does them itself.

## Question 1

Figure 2 shows Flow bypassed rather than lacking: its source already launches, delivers, stops, retires and hooks, but the running Nexus is twelve versions behind the source, the CLI is in between, and nothing in Primary calls any of them. Is the next step to cut Primary over to Flow, moving launch, lifecycle and hooks out of the launcher scripts and the messenger into calls to Flow, before any other finding here is fixed?

## Question 2

The two Herdr patches are welds into a component that is not ours. The quiet-hours patch is used by nothing now; the allowlist patch holds a Flow fact, which binary a flow runs. Are both removed, with the allowlist rebuilt as Flow's own check before Flow calls Herdr's unpatched start?

## Question 3

The model and effort per layer live in five places that disagree. Is the one place the skill variables file, with the voice table, the Curriculum roles, the CriomOS-home list and Flow's defaults all reading from it, or is the one place Flow's configuration?

## Question 4

The reminder hook and the Field heartbeat are the two cars that start when they have gas. Do both get a switch and their values fed in now, as the first application of Proposal 1, or does that wait for the Flow cutover, since both would be Flow's to run?

## Question 5

Flow's Report, Stop and lock release accept the flow id the payload names, with no check of who sent it. Is a peer check a design of its own, to be brought to you as a book before anything is built, or a correction to make now?
<!-- to-the-living:end -->
