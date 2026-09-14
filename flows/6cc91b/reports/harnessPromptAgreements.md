# Harness system-prompt agreements

Subflow of 6cc91b, answering: "What have we agreed on most to change
about the system prompts of the default harnesses? What are we going
to put in the open source one?"

## 1. The living's statements, verbatim, newest first

> Also, now we might as well just start doing the stuff that we agreed
> on. What have we agreed on most to change about the system prompts
> of the default harnesses? What are we going to put in the open
> source one? Let's have a draft of the open source stack, which is
> entirely self-authored. Let's be honest about how I work and ask me
> questions about how I view how to work, how the law should be laid,
> and how behavior should be, which is in nuclei right now, in our
> skills and in our vision.
-- flows/6cc91b/vision/openSourceStack.md, 2026-09-14

> These people don't think right about how to code with AI, but it
> doesn't have mass. What is the best? What is Hermes using? What is
> the best harness right now that is just programmable? Is it
> DeepSeek? What are the best models? I haven't really seen that.
> Make a report.
-- flows/6cc91b/vision/openSourceHarness.md, 2026-09-14

> Today, what is the best open-source stack with remote control,
> essentially the open-source Claude and Codex with a remote control
> solution?
-- flows/6cc91b/vision/openSourceHarness.md, 2026-09-13

> ...if you do the harness right and you give the right ontology and
> guidance, you can make any model in the right harness, essentially,
> by going through a process which we've started to do, right? -
> breaking down the thinking process - the communication process -
> idea reviewing - creating - proof of concepting
-- flows/6cc91b/vision/openSourceHarness.md, 2026-09-13

> It's just the concept that we're going to start flows using a Nexus
> component, which will decide what the system prompt is and
> everything. We're going to replace the harness's concept of
> subagents with this component, which will have specialized harnesses
> launched with specialized system prompts that will make them much
> more efficient at what they're supposed to be doing.
-- flows/1a6ca4/vision/archive-nexus.md, 2026-09-05

> That phase is like the wild west phase of thinking machines, and the
> persona meta-harness is going to bring in the dawn of the more
> complete thinking machine systems, which will be a complex
> infrastructure of a kind of thinking machine legal system
> interworking apparatus.
-- flows/1a6ca4/vision/personaMetaHarness.md, 2026-09-05

> We should just create a separate repository that anyone could use to
> give modified versions with different names of Claude and Codex,
> with different takes on system prompts.
-- flows/38dec9/vision/systemPromptRepository.md (added to tree 2026-09-09)

> I would probably just rename the executable of the wrapper something
> else so that we can still use the stock version, and call the
> wrapper something else, like Claude Light or Claude Unopinionated,
> or maybe Codec Unsafe if we take all the safety out and stuff, or
> Codec Bare where we have almost nothing.
-- flows/38dec9/vision/perHarnessSkills.md (added to tree 2026-09-05)

> There may be some things that I want to remove in all harnesses that
> we could do universally and just replace.
-- flows/38dec9/vision/perHarnessSkills.md

> this overlaps with our own skills. They say to use evidence, but
> don't actually define what evidence is. ... It's like they're trying
> to make a single flow do the job of several flows... I think they're
> trying to cram too much into a single flow, and it's breaking the
> flow.
-- flows/ceb3b9fd/vision/topStratum.md, on Codex's Autonomy-and-persistence
   block, 2026-08-30

> mark as replace, at least in parts.
-- flows/ceb3b9fd/vision/hijackRepositories.md, on Codex's
   "Working with the user" block, 2026-08-30

> In my vision, we're going to have different top stratums for
> different jobs. The top stratum will be programmable per flow.
> Instead of trying to make a single flow take all of the decisions
> and make all of the inference in one action, that's one job...
-- flows/ceb3b9fd/vision/topStratum.md, 2026-08-30

> Since we don't want to actually, it seems that, and even the
> harnesses are kind of actually told to do that. They're told to like
> copy the code they already find. And actually, that's one of the
> things I want to change in the base prompt. I don't think that
> that's a good thing... because if there's bad things and bad things
> get copied.
-- flows/aa4c7747/vision/basePrompt.md, 2026-08-24

> Let's look at the most offensive base prompt blocks first, and
> design replacement for each, and work our way through the entire
> offensive corpus like this
-- flows/2f6b1dc5/vision/systemPrompt.md, 2026-08-23

> I want to replace claude and codex's system prompts with a version
> that doesnt incentivize the sort of behavior im constantly steering
> against. The system/base prompt ... has the highest context priority
> and is currently full (I suspect) of instructions that are
> completly or even partly against my philosophy and approach to LLM
> usage.
-- flows/2f6b1dc5/vision/systemPrompt.md, 2026-08-23 (founding statement)

> I think we should really consider replacing both Claude and Codex's
> harness' system prompts with some heavy modifications to give them
> ... [training against false confidence, rewarding admission of
> ignorance]
-- flows/358f143a/vision/falseConfidence.md, 2026-08-17

> essentially the analogs of what the basic harness training prompt is
> currently that is built into the harnesses, which we will completely
> ... behave in a harness, but with our own take on it.
-- flows/e06e4c07/vision/archive-flowDaemon.md, 2026-08-19

## 2. What the skills already assert

- claude-harness (Curriculum): "Claude Code's top stratum is the
  system prompt. The --system-prompt and --system-prompt-file flags
  replace the whole of it... CLAUDE.md and the other entry files are
  delivered as a user message after the system prompt, never inside
  it: they are middle stratum... The living witnesses the stock
  system prompt only through the machine's transcription of it."
  Replacing it "removes its behavioral guidance and nothing else" —
  tool schemas, permissions, hooks, subflow-output scanning,
  entry-file injection, and training persist.
  /git/github.com/LiGoldragon/Curriculum/skills/claude-harness.md

- codex-harness (Curriculum): "Codex's top stratum is the base
  instructions, sent as the instructions field... The
  model_instructions_file config key replaces the base instructions
  with a file's text and outranks the instructions config key... the
  source discourages both, and we use the file." AGENTS.md "cannot
  override base instructions." Both the living and the machine can
  read Codex's base instructions.
  /git/github.com/LiGoldragon/Curriculum/skills/codex-harness.md

- context-strata (Curriculum): "The top stratum is the base context:
  the standing instructions the harness sends before any
  conversation, and any text authored into that seat. Universal
  invariants belong here... Harness seizure is authoring the top
  stratum ourselves."
  /git/github.com/LiGoldragon/Curriculum/skills/context-strata.md

- spirit (Curriculum): carries the psyche's standing invariants
  (extension-of-psyche framing, no backward compatibility, name the
  wanted not the avoided, admit not-knowing, seek disconfirming
  evidence) — the exact content the living has repeatedly said
  belongs at the top stratum of a replaced prompt.
  /git/github.com/LiGoldragon/Curriculum/skills/spirit.md

## 3. Agreed changes, most-said/most-recent first

1. Replace both Claude Code's and Codex's stock system/base prompts
   outright (not merely append) — founding decision, restated at
   least four times across the record.
   Sources: flows/2f6b1dc5/vision/systemPrompt.md (2026-08-23),
   flows/358f143a/vision/falseConfidence.md (2026-08-17),
   flows/e06e4c07/vision/archive-flowDaemon.md (2026-08-19),
   Vision/flowNexus.md.
2. Work block-by-block through each stock prompt, worst offenders
   first, marking each block replace/keep/replace-in-parts.
   Sources: flows/2f6b1dc5/vision/systemPrompt.md; enacted in
   flows/ceb3b9fd/vision/hijackRepositories.md and
   flows/4ddc321d/reports/{codexHijackRepo,claudeHijackRepo}.md.
3. Drop the harness's "reward false confidence" shape; retrain toward
   admitting ignorance, keeping unknowns unknown (now also stated
   directly in the spirit skill).
   Source: flows/358f143a/vision/falseConfidence.md (2026-08-17).
4. Stop telling the model to copy code it finds already in the
   repository — bad code propagates.
   Source: flows/aa4c7747/vision/basePrompt.md (2026-08-24).
5. Replace the Codex "Autonomy and persistence" block: it crams the
   jobs of several flows into one, defines no evidence, is thin and
   contradictory.
   Source: flows/ceb3b9fd/vision/topStratum.md (2026-08-30).
6. Replace, at least in parts, the Codex "Working with the user"
   block: keep the channel/compaction facts and a rare-commentary
   rule, drop the 60-second narration decree and the assumption
   mandate.
   Source: flows/ceb3b9fd/vision/hijackRepositories.md (2026-08-30).
7. Replace imposed personality/tone prescriptions ("concise, direct,
   friendly") and OpenAI's output-formatting/verbosity rules —
   flagged worst-offender candidates by the extraction subflow, not
   yet a direct psyche quote.
   Source: flows/4ddc321d/reports/codexHijackRepo.md.
8. Move to per-flow, per-job top strata instead of one prompt for
   everything: "the top stratum will be programmable per flow."
   Sources: flows/ceb3b9fd/vision/topStratum.md (2026-08-30),
   flows/1a6ca4/vision/archive-nexus.md (2026-09-05).
9. Put spirit's (and behavior's) content in the highest reachable
   stratum, reinforcing their primacy in words; practically landed as
   an entry-files top section (middle stratum) rather than an actual
   system-prompt rewrite, pending the meta-harness.
   Sources: flows/358f143a/vision/behavior.md (2026-08-17),
   vision-raw/spirit.md (2026-08-22).
10. Publish a separate open-source repository offering modified,
    differently-named Claude/Codex builds with different system
    prompts (e.g. "Claude Light/Unopinionated", "Codex Unsafe/Bare"),
    letting anyone choose a take.
    Source: flows/38dec9/vision/systemPromptRepository.md,
    flows/38dec9/vision/perHarnessSkills.md.
11. Longer-range: a persona meta-harness / Nexus component decides
    each flow's system prompt at launch and replaces the harness's
    subagent concept with specialized harnesses carrying specialized
    prompts.
    Sources: flows/1a6ca4/vision/personaMetaHarness.md (2026-09-05),
    flows/1a6ca4/vision/archive-nexus.md (2026-09-05),
    Vision/flowNexus.md.
12. Today's addition: the open-source stack is to be entirely
    self-authored, and its content is to come from asking the living
    directly how work, law, and behavior should be laid out — not
    inferred solely from what is already in skills/Vision.
    Source: flows/6cc91b/vision/openSourceStack.md (2026-09-14).

## 4. Implemented vs. only stated

Implemented:
- Entry files (CLAUDE.md, AGENTS.md, NON_MANAGEMENT_AGENTS.md,
  SKILL_VARIABLES.md) exist at primary's root, generated from
  Curriculum's authored AGENTS.md and distributed as the middle
  stratum on both harnesses.
- Generated per-harness trees (.claude/, .agents/, .codex/) carry the
  claude-harness, codex-harness, context-strata, and spirit skills as
  read-only evidence, loaded through the skill interface (middle
  stratum), not the top.
- Two public extraction repositories stood up and populated with the
  verbatim stock prompt text and a block inventory:
  /git/github.com/LiGoldragon/codex-hijack (17 blocks, from Codex
  0.149.1 source) and /git/github.com/LiGoldragon/claude-hijack (21
  system-prompt blocks + 8 system-reminder messages, extracted from
  the Claude Code 2.1.241 binary). Each repo currently holds only a
  README and stock-context/ — the stock text, not yet replacement
  text.
- Individual blocks marked replace / replace-in-parts / keep for a
  few Codex blocks (Autonomy-and-persistence, Working-with-the-user)
  in flows/ceb3b9fd/vision/hijackRepositories.md and
  flows/ceb3b9fd/vision/topStratum.md.
- flows/7b4d4c/reports/proposal.md: a full harness-anatomy proposal
  (382 lines, F1-F22 open forks) comparing all three strata across
  Claude Code, Codex, and dsh, with a vocabulary-cleanup table — drafted,
  not ruled block-by-block.

Only stated, no artifact yet:
- No replacement system-prompt or base-instructions file has been
  drafted or committed for either harness; --system-prompt-file /
  model_instructions_file are not wired into any launch config in
  primary.
- No open-source stack repository (today's ask) exists yet.
- The persona meta-harness / Nexus component that would choose a
  per-flow system prompt is unbuilt (referenced only as vision and an
  empty, remote-less local git directory named `persona`,
  witnessed in flows/7b4d4c/reports/proposal.md).
- No "Claude Light/Unopinionated" or "Codex Unsafe/Bare" wrapper
  executable exists.
- Personality/tone and output-formatting blocks are flagged but not
  yet marked replace/keep by the psyche directly.

## 5. Unknowns

- Whether the worst-offender rankings in
  flows/4ddc321d/reports/codexHijackRepo.md and claudeHijackRepo.md
  (personality/tone, autonomy-persistence duplication, output
  formatting) have since been ruled on by the psyche directly, or
  remain the flow's own reading.
- Whether flows/7b4d4c/reports/proposal.md's F1-F22 forks were later
  resolved in a subsequent flow not surfaced by this search.
- Whether "open source Claude and Codex" in the 2026-09-13/14
  statements means the codex-hijack/claude-hijack repos are meant to
  become the open-source stack, or a new, separate repository is
  intended.
- Which specific replacement wording (if any) exists today for the
  blocks already marked "replace" — none was found in the hijack
  repos, which hold only the extracted stock text.
- Whether the entry-files placement of spirit/behavior is considered
  the final answer to "put it in the top stratum," or a stopgap
  pending the meta-harness (the record shows both framings, at
  different dates, without an explicit reconciling ruling).
