# Authored skill kinds

Source: Curriculum `skills/` at origin/main, 69 skills. Kind is read from the name prefix; gold = no prefix.

| name | kind | description | dependencies |
|---|---|---|---|
| agent-harness-packaging | gold (no prefix) | An external manager for coding harnesses must be selected, packaged, installed, configured, or integrated. | nix-workflow |
| beads | gold (no prefix) | Work must be tracked across sessions or between agents. | secrets |
| behavior | gold (no prefix) | A claim is relayed, a thing is called verified, an act is explained, or a value that differs between setups is written. | - |
| breaking-upgrades | gold (no prefix) | A breaking change must be deployed. | documentation-placement |
| claude-harness | gold (no prefix) | Invoking, seizing, or reasoning about the Claude Code harness: its system prompt flags, what they replace, what persists, and where its entry files land. | context-strata |
| codex-harness | gold (no prefix) | Invoking, seizing, or reasoning about the OpenAI Codex CLI harness: its base instructions, developer instructions, AGENTS.md, and what persists outside them. | context-strata |
| compensation-default-effort | compensation | A model or its effort must be chosen. | - |
| compensation-messenger-clj | compensation | A flow runs an hm-* command, reads its output, or changes messenger-clj. | - |
| compensation-nix-rationale | compensation | The shape of a `<repo>-test` repository or its Nix code is being discussed with the living psyche and the reasoning behind it is needed. | compensation-nix |
| compensation-nix | compensation | A `<repo>-test` repository is being created, or an integration scenario, sandbox, or other Nix code in one is being written, run, or landed. | nix-workflow, testing, repository-lifecycle, secrets |
| compensation-primary-commit | compensation | Publish one flow's Primary paths without rewriting shared history. | - |
| compensation-subflow | compensation | A subflow carries a message body. | - |
| compensation-update | compensation | Rotate stable and Next after consumer migration while preserving running sessions. | - |
| context-strata | gold (no prefix) | Designing or implementing something that depends on where text enters a thinking machine's (an LLM's) context. Almost never arises in ordinary task work. | - |
| correction | gold (no prefix) | A correction has been received, or an output has been found wrong. | - |
| datom | gold (no prefix) | Constructing, reading or interpreting datom text, or giving a Rust type its datom kinds. | protos |
| design | gold (no prefix) | The psyche is designing — vision anatomy is fleshed out. | main-flow, psyche-interraction |
| disk-hygiene | gold (no prefix) | Space must be reclaimed, or data removed to reclaim it. | - |
| documentation-placement | gold (no prefix) | Something must be written down and where it goes is not obvious. | - |
| edit-coordination | gold (no prefix) | Another agent may be writing the same paths. | orchestrate |
| feature-development | gold (no prefix) | Feature work would collide with a checkout someone else holds. | - |
| file-editing | gold (no prefix) | Editing files means committing and pushing them. | - |
| flow-evidence | gold (no prefix) | The main flow has delegated a report or witness, or a named tool or flow will consume one. | vocabulary, edit-coordination |
| knowledge-codex | knowledge | Read the version-pinned Codex app-server control surface without turning protocol shapes into runtime claims. | - |
| knowledge-ethos | knowledge | Rust is generated from an ethos file with ethos-zero as it runs today, or what the generator accepts is read. | vision-ethos |
| knowledge-flow | knowledge | A flow must be launched, named, claimed or reached, or a hook or sandbox seat run, with what is deployed today rather than with Flow as designed. | vision-flow |
| knowledge-nexus | knowledge | What the nexuses are today — which run, on which sockets and versions, from which branches — is read, before judging or changing one. | vision-nexus |
| lojix | gold (no prefix) | A Lojix request must be constructed, submitted, observed, or interpreted. | nix-workflow |
| main-flow | gold (no prefix) | A user starts the main flow that coordinates subflows and owns their shared flow lane. | vocabulary, edit-coordination, psyche-interraction, psyche |
| nix-input-upgrade | gold (no prefix) | Nix flake inputs are being upgraded across a layered repo structure. | nix-workflow |
| nix-workflow | gold (no prefix) | The change lands in Nix. | - |
| operating-system | gold (no prefix) | The operating system itself must change. | lojix |
| operation-book | operation | A presentation must be made available to the living messenger. | operation-flashbook-illustration |
| operation-flashbook-illustration | operation | An illustration for a flashbook page must be made. | - |
| operation-flashbook | operation | A flashbook must be made from a source written in a flow's transcript, or an existing flashbook is judged. | operation-flashbook-illustration, behavior, vocabulary |
| operation-relaying-the-living | operation | Living words are passed to another flow. | - |
| orchestrate | gold (no prefix) | An ordinary Orchestrate Lock request must be constructed, submitted, or interpreted. | - |
| prompt-crafting | gold (no prefix) | A prompt must be crafted for another flow. | - |
| protos | gold (no prefix) | Reading or writing any protos dialect, or touching the protos crate. | - |
| psyche-acquisition | gold (no prefix) | Reacquiring what the psyche has expressed. | psyche |
| psyche-distillation | gold (no prefix) | Psyche records across flows touch the same topic and a self-standing articulation is owed. | psyche |
| psyche-grasp | gold (no prefix) | 'A code site needs marking with how deeply the psyche has seen and understood it.' | psyche |
| psyche-interraction | gold (no prefix) | An agent is directly conversing with the psyche. | psyche |
| psyche | gold (no prefix) | What agents are reading when they read psyche. | - |
| realization | gold (no prefix) | The flow is realizing — psyche is realized into code. | main-flow, psyche-interraction, testing |
| repository-lifecycle | gold (no prefix) | A repository does not yet exist, or work in one is finishing. | - |
| secrets | gold (no prefix) | A secret must reach a program without reaching the agent. | - |
| skill-designing | gold (no prefix) | Reusable behavioral instructions are being written, changed, proposed, or reviewed. | - |
| spirit | gold (no prefix) | Every agent task. | behavior, correction, vocabulary |
| stale-lock | gold (no prefix) | An Orchestrate lock is held by a flow that no longer answers. | orchestrate, compensation-messenger-clj |
| testing | gold (no prefix) | A change needs proof it works. | - |
| transcript-search | gold (no prefix) | A transcript must be searched — for the psyche's typed words, for what a flow said or did, for what another flow said or did that this flow did not itself witness, or for one record by line. | - |
| trial-contact-discipline | trial | A primary seat or another aspect must be contacted. | - |
| trial-generated-projection | trial | A generated tree is claimed to match its authored source, or an authored source has changed and the consumers may be stale. | testing, file-editing |
| trial-independent-review | trial | A middle tier brings the living's words to a higher tier for review. | - |
| trial-low-power | trial | Quota is near or the living declares low power. | - |
| trial-no-polling | trial | Work would check state repeatedly. | - |
| trial-presentation-book | trial | A main flow has just written a presentation block for the living. | operation-flashbook |
| trial-psyche-injection | trial | Context lacks recent psyche on the current topic. | - |
| trial-questions-book | trial | The living's questions overflow the current conversation. | - |
| trial-reaping | trial | A seat is abandoned, duplicated, or past its successor. | - |
| trial-recurring-failure | trial | A failure recurs after being fixed once. | - |
| trial-succession | trial | A seat must start, refresh, replace, or request a flow. | - |
| trial-unblocking-commands | trial | A command could stop a seat while awaiting living approval. | - |
| versioning | gold (no prefix) | A change may or may not warrant a version bump. | - |
| vision-ethos | vision | An ethos file is written, or a type, kind or layout is judged against what the living wants ethos to be. | datom, protos |
| vision-flow | vision | Flow — the Nexus that launches, names, tracks and ends flows — or a voice, a side flow, a hook or the Capsule is being designed or judged against what the living wants. | vision-nexus, vision-ethos |
| vision-nexus | vision | A long-running Nexus — its sockets, clients, wire contracts and store — is being designed or judged against what the living wants it to be. | vision-ethos, datom |
| vocabulary | gold (no prefix) | One of our own terms is used, or a term is being defined. | - |

## Counts by kind

| kind | count |
|---|---|
| gold (no prefix) | 39 |
| vision | 3 |
| knowledge | 4 |
| operation | 4 |
| compensation | 7 |
| trial | 12 |

## Members

- **gold** (39): agent-harness-packaging, beads, behavior, breaking-upgrades, claude-harness, codex-harness, context-strata, correction, datom, design, disk-hygiene, documentation-placement, edit-coordination, feature-development, file-editing, flow-evidence, lojix, main-flow, nix-input-upgrade, nix-workflow, operating-system, orchestrate, prompt-crafting, protos, psyche-acquisition, psyche-distillation, psyche-grasp, psyche-interraction, psyche, realization, repository-lifecycle, secrets, skill-designing, spirit, stale-lock, testing, transcript-search, versioning, vocabulary
- **vision** (3): vision-ethos, vision-flow, vision-nexus
- **knowledge** (4): knowledge-codex, knowledge-ethos, knowledge-flow, knowledge-nexus
- **operation** (4): operation-book, operation-flashbook-illustration, operation-flashbook, operation-relaying-the-living
- **compensation** (7): compensation-default-effort, compensation-messenger-clj, compensation-nix-rationale, compensation-nix, compensation-primary-commit, compensation-subflow, compensation-update
- **trial** (12): trial-contact-discipline, trial-generated-projection, trial-independent-review, trial-low-power, trial-no-polling, trial-presentation-book, trial-psyche-injection, trial-questions-book, trial-reaping, trial-recurring-failure, trial-succession, trial-unblocking-commands

## Unclear kind

- design, realization: no prefix, `user-only: true` mode skills (design/realization phases), not a topic skill; main-flow is also `user-only`. Filed as gold by prefix rule; kind ambiguous.
- No other skill carries a prefix outside the named set.
