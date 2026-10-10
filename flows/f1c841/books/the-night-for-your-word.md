Presentation.{ «The night, for your word» }

Your standing order, STT, 2026-10-02: "pretending you're going to play the role of the psyche here, using the records that we have ... favor recency and emphasis. When decisions are made ... if it's clear, it's going to be the highest authority." Twelve rulings were taken under it; each is yours to overturn by number. Nothing is deployed.

## 1. Rulings and names that need your word

Name a number to overturn; silence keeps the ruling.

1. Gold is retired; every skill carries a prefix: vision-, intent-, notion- for your levels; operation-, knowledge-, question- for kinds; compensation- and trial- stay flow-written. Taken on your hedged words, typed 2026-10-02: "I think I want to get rid of the gold skills concept and every skill is typed. Psyche skills will be vision or intent, or maybe notion but I don't know." and "vision has to become skills now. The skills have to be prefixed with "vision" and something else and maybe even split up".
2. The Operation root's sections are imports, operations, outcomes, types — proposed, no words of yours. Your words name the layers only, typed 2026-10-02: "Yeah the memory is good. That's what it is I guess: signal, operation, and memory."
3. Every root's types derive rkyv and carry the datom kinds behind a `datom` feature (ethos-zero 16.0.0, landed) — taken on vision-nexus's "datom and all text handling are compiled out of the Nexus".
4. A harness event reaches Flow as `Report.{ FlowId Event }` answered `Reported`; an unknown FlowId is refused, never adopted. Your question stays open, typed 2026-10-01: "Where are those hooks? What are those hooks calling? They're going to call the Nexus CLI so which Nexus do we use for this? Is this Flow, or is it Transcript, or is it something else?" The night sent the event to Flow and left the transcript's content for your ruling.
5. Five kind names chosen by a flow, resting on your "a type is too specific" and "launchable": Spendable, Branchable, Budgeted, Positional, Composable.
6. `Unsubscribe` remains beside signal's `Abandon`, which already ends a subscription — no words of yours exist; a vocabulary decision.
7. In signal-flow the old reply type `Started` was renamed `Launched` so that `Event.Started` keeps the vision's word; the other way was to rename the Event variant.
8. `GenerationRejected` and `GenerationRefused` keep their names in the ethos-zero contracts; the vision's `Refused` would change every refusal's datom text.

```
Signal
[ flow:[ FlowId Event ] ]
[ Report.{ FlowId
           Event } ]
[ Reported
  Refused.[ UnknownFlow.FlowId ] ]
[ Event.[ Started
          ToolUsed.String
          Stopped ] ]
```

## 2. Deployments to approve

Candidates are built, held from garbage collection, and witnessed from their own binaries in sandboxes; none is switched. Name the numbers you approve.

1. Orchestrate 0.35.0 → 0.36.1, the generation 3ec648 prepared. Witnessed only in its own tests.
2. Orchestrate 0.35.0 → 0.37.0, the night's generation: same wire and store as 0.36.1, on ethos-zero 16 and signal 8. Witnessed: the Nexus starts, `Observe.Locks` answers `Observed.Locks.[]`, the meta `Configure` answers `Configured.{ … True }`; 0.37.0 resumes the live 0.35.0's store through the old `meta-orchestrate.sock` name; 0.35.0 resumes a store 0.37.0 served (the rollback). Before either switch: `orchestrate 'Observe.Locks'` must answer `Observed.Locks.[]`, since the 0.35→0.36 wire break is total. After: the unit runs the new version, `Observe.Locks` answers, then `Configure` through the old socket name moves the meta socket to `orchestrate-meta.sock`, restart, `Configure` through the wrapper answers `Configured`.
3. Flow 0.17.4 → 0.23.0 and Message 0.17.0 → 0.19.0 in the next slot, one generation on top of 2: Flow carries the Operation root, the hook on SessionStart/PostToolUse/Stop reporting into Memory, the reserved FLOW_ID and the launching Nexus's socket in each launched seat. Witnessed: 0.23.0 opens a 0.17.4-made store; Message starts after Flow and answers typed replies; both roll back. Before: copy both next-slot stores aside. Effects: the stable flow-nexus 0.12.2 restarts without its FLOW_* variables; seats launched before the restart keep their old environment; Codex seats get no FLOW_ID.
4. Retire the stable flow-nexus 0.12.2 for good: a later commit with `criomosHome.flow.enable = false`, plus removing its hand-written drop-in, profile element and the `message-next` wrappers.
5. The installed `claude` wrapper forces `--dangerously-skip-permissions` on every seat and sandbox flow: 5a keep; 5b honour a requested mode; 5c default to another mode (unattended seats would stop at prompts; needs a Flow release too). 5b restarts both Flow Nexuses, so it belongs with 3.

## 3. What landed on main

- Every repository on ethos-zero 16.0.0, signal 8.0.0, protos/datom-codec 0.32.2: orchestrate 0.37.0 and its contracts 5.0.0; flow 0.23.0, signal-flow 10.0.0, meta-signal-flow 14.0.0; message 0.19.0 and its contracts 10.0.0/0.10.0; lojix 9.0.0 with horizon-lib 0.14.0 and its contracts; signal-ethos-zero and meta-signal-ethos-zero 2.0.0; meaning-language, claude-answers, curriculum-deploy, clavifaber, chroma. The remaining lag is the store engine (sema-engine 0.16/0.17 behind 0.18.0).
- The Operation root compiles in a Nexus: flow's thirteen effects are generated operations performed through one trait, each answered by one outcome.
- The first harness hook: in flow-test's sandbox, a Flow-launched haiku seat's events land in Flow's Memory as `[ Started ToolUsed.Bash Stopped ]`; the dead-socket case was witnessed red on 0.22.0 and green on 0.23.0.
- The ethos-zero contracts rewritten in the vision's shape: vertical print enforced at build, a Library root, eleven holder types gone, declarations 31 → 8. Every other contract file still conflicts with the vision (one-line sections, holder types, no Library/Operation/Memory); reshaping them changes digests, so it waits for your word.
- knowledge-ethos, knowledge-nexus, knowledge-flow describe tonight's state; compensation-primary-commit names its conflict check, its sentinel lock path and the reconciliation remedy.

## 4. Incidents and the unverified

- A haiku publisher read the word "conflicts" inside the log's own text as a jj conflict and abandoned a clean copy; it also took no Orchestrate lock, creating and removing a file in Primary instead. Publication is Opus-only from now and the skill names the check.
- The log conflicted twice because a reconciliation on main left the working copy without the landed lines; the remedy is in the skill and witnessed clean.
- A stray `.git` under the message worktrees hides its flake from Nix; not ours, left alone.
- Not run: the live switch sequences themselves; Configure of an old-format store under 0.37.0 is witnessed only in the sandbox; Message 0.17.x against Flow 0.21+ untested; the live light-model scenario awaits your first run.
- Three earlier books are uncommented: «Where the edit goes, and vision as skills», «Ethos as two skills, the case study», «Ethos, six statements and the voices».
