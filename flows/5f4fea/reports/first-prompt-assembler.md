# First Prompt Assembler Proposal

Status: proposal only. No assembler, CLI, runner, spawn, successor, skill, or source record is created by this report.

## Purpose

An assembler could produce the first prompt for a newly claimed flow from a predecessor handoff and explicitly supplied work topics. Its output is a prompt artifact for review or an authorized launch; it is not itself a harness start operation.

## Inputs

Required inputs are the predecessor flow lane and its handoff, the successor's actual harness identity and directory, the harness kind, and any explicitly requested skills. The successor identity must come from a real harness claim after start; a pre-spawn assembler must refuse to invent it. Optional topic pointers may narrow the handoff. `globalIntent` is distinct from the predecessor's purpose and must be supplied separately when applicable. Raw vision is a source pointer, not an instruction to paste every record.

The assembler keeps these categories separate:

| Input | Meaning | Output treatment |
| --- | --- | --- |
| predecessor lane | inheritance and handoff source | cite and constrain |
| actual successor identity | harness-confirmed session/thread, flow, lane, directory | include only after claim |
| requested skills | desired loading actions | list as requested, never claim receipt |
| native receipt | observed harness/user-injected skill result | include only when witnessed |
| optional topics | scoped work context | include as pointers and compact citations |
| global intent | broader governing purpose | keep distinct from predecessor task |

## Assembly rules

The first prompt should preserve the living's direct words through source citations or a retrievable reference, then state only the scoped handoff needed by the successor. Machine-authored predecessor instructions are constraints and pointers, not raw psyche. Notion is subordinate evidence and is not equivalent to a direct living statement. The prompt should identify the pair or triad, lane, and directory from actual evidence. It should not claim that skills loaded merely because they were requested. It should not claim `Remembered` depth one until the successor has actually consumed the predecessor record. A user-only `/main-flow` instruction remains user-invocable and must not be treated as automatically model-invoked without explicit living authorization.

No ancestor is awakened automatically. A concluded flow is a source of handoff evidence only. The assembler cannot decide a successor's authority, create a lane, or send a prompt.

## Launch-call ruling

The living ruled that loading skills one at a time and then sending the first prompt makes a separate model call for each input and is too expensive. A future assembler or launcher therefore prepares one initial model call containing the launch package. Two alternatives remain pending:

- Native batch skill-interface inputs plus the handoff in one initial call.
- A harness-level system-prompt file supplied at launch, with the handoff in that same initial call. Whether this qualifies as a skill-interface input remains an open living question.

These alternatives are both pending; neither is selected or declared equivalent, and no assembler or launcher is built by this report.

## Surface alternatives

Fork A is an outside-flow tool at `/home/li/primary/tools/assemble-first-prompt`, accepting a single structured request and returning one assembled prompt. If it is eventually given a Datom surface, the CLI must take exactly one inline Datom value; a JSON flag interface would contradict the current Datom CLI standard. Its transport and output persistence remain undecided.

Fork B is an integrated Flow Nexus API, where the Nexus resolves predecessor records, validates the claimed successor identity, and returns an assembled prompt. A later unified spawn orchestrator may call that pure assembler and then perform an authorized harness start; this proposal does not preempt that design.

The two forks are alternatives for ownership and authority. Neither is selected here.

## Acceptance cases

| Case | Required result |
| --- | --- |
| no successor harness claim | refuse assembly or return an explicitly unbound draft; never invent identity |
| requested skills without native receipt | label them requested; omit any loaded/received claim |
| predecessor handoff plus actual successor claim | include exact lane, directory, and identity with compact source references |
| raw vision supplied broadly | retain pointers and selected excerpts; do not treat every raw line as authority |
| `/main-flow` in requested skills | preserve user-only invocation semantics and require explicit start authorization |
| depth-one inheritance not consumed | do not emit `Remembered` as witnessed state |
| concluded ancestor referenced | cite it as evidence; do not wake or message it |
| Datom invocation | one inline typed value, no flags or parallel JSON mode |
| missing or conflicting predecessor identity | stop with an explicit unresolved input |

## Pending decisions

- outside tool versus Flow Nexus ownership;
- exact input schema and whether the draft may be produced before successor claim;
- which optional topics and source references are included by default;
- whether the result is displayed only or may be handed to an authorized launcher.

## Sources

- `/home/li/primary/flows/e1953c/handoff/first-prompt.md`
- `/home/li/primary/flows/692df8/vision/flowLifecycle.md`
- `/home/li/primary/Vision/flowNexus.md`
- `/home/li/primary/Vision/sources/flowNexus.md`
- `/home/li/primary/vision-raw/spirit.md`
- `/home/li/primary/flows/995a164e/vision/intent.md`
- `/home/li/primary/flows/6cc91b/vision/typedPrompts.md`
- `/home/li/primary/flows/6cc91b/vision/interflowMessaging.md`
- `/home/li/primary/flows/692df8/vision/messages.md`
