# Flow 2f6b1dc5 — design

Base-prompt replacement design: the psyche wants Claude's and Codex's
harness base/system prompts replaced so the top stratum stops
incentivizing steered-against behavior. a60a9e85 remembered with its
layer beyond (cff271af, 68512643); 68512643's negatives/distillation
insights incorporated. Base-prompt vocabulary entry deployed. Both
harnesses' full-replacement doors witnessed (claude
--system-prompt[-file]; codex config instructions /
model_instructions_file). Offensive-corpus block walk begun on the
psyche's method ruling; block 1 (completion pressure) replacement
proposed, awaiting ruling.

## 2026-08-23

- Flow opened on the psyche's words (verbatim in
  vision/systemPrompt.md): replace claude and codex's system prompts
  with a version that doesn't incentivize the constantly
  steered-against behavior; the system/base prompt has the highest
  context priority; contents suspected largely against the psyche's
  philosophy ("I suspect" — the psyche's own marker). Vocabulary
  definition requested.
- Skills loaded: design, subflows, spirit, flows, psyche, vocabulary,
  behavior, psyche-interraction.
- Remembered: a60a9e85, cff271af, 68512643 — depth 2. a60a9e85:
  understanding-by-enactment ruling, three enactment stagings
  composed into an opinion, concept walk live (distillation is
  comprehension), outputNoise ruling (phatic output; training levers
  asked). cff271af: software-design draft thread, distillation turn,
  the strata words in vision/reports.md (the prompt is the precious
  stratum). 68512643: distillation clarified main-flow-only;
  orchestrate/meta-orchestrate bypass directive for subflows. Light
  state check: draft v5 present at
  flows/a60a9e85/reports/SkillDrafts/softwareDesign/draft.md.
- Psyche-ground search (rg over Vision/, psyche-raw/, flows/*/vision/
  for system/base prompt, strata, context priority) found standing
  ground this want continues: psyche-raw/Vision/gradientsOfAuthority.md
  2026-08-10 — "completely hijack the harness": every session's top
  layer authored, carrying skills, standards, and the main goal;
  skills primary. 358f143a — context strata vocabulary ruled
  (top/middle/bottom stratum); harness facts only from code ("docs
  are not evidence for code"; "the code is what runs, not the
  docs"); spirit and origin-of-claim rules belong on top. cff271af
  vision/reports.md — tool-call-read information lands in the bottom
  stratum; the parent-given prompt is the precious stratum.
- Dispatched two read subflows (response-only, no files, no lane
  registration per the 68512643 directive): (1) Codex base prompt
  and override mechanisms ascertained from the installed version's
  code; (2) Claude Code override mechanisms witnessed by probe
  (--help, -p system-prompt probes, bundle read), docs relayed only
  as claims.
- Direct-observation assessment of this flow's own Claude Code base
  prompt given in conversation: mechanics / behavior-shaping /
  vendor-policy families; sharpest conflicts named (autonomy
  pressure vs anatomy-first, turn-completion pressure vs awaiting
  rulings, surrounding-code pattern-copying vs the fence-meme
  ruling); partial alignments named honestly (faithful reporting,
  anti-filler).
- Vocabulary proposed to the psyche: base prompt = the harness-built
  portion of the top stratum. Anatomy forks presented (replacement
  boundary, authored source in Curriculum with per-harness
  generation, steered-against list distillation first). Awaiting
  rulings.
- The psyche directed: also incorporate the insights from 68512643.
  Its vision records read in full (68512643-1 main-flow-only
  distillation; 68512643-2 the negatives tick; 68512643-3 the
  inline-data road the negative would have hidden). Incorporated in
  conversation: the replacement is composed as positive duties,
  negatives only with explicit confident psyche license; negatives
  cost context without direct value — doubly wrong in the top
  stratum; prohibitions hide roads; composition is main-flow work
  with subflows only gathering; the carried-modality provenance
  failure named as the risk of rewriting the vendor prompt rather
  than composing from distilled ground. Fork 3 re-articulated:
  design from positive duties, the strike record as evidence of
  missing duties, not as content.
- The psyche approved the base-prompt vocabulary entry verbatim and
  directed deployment ("this is good. approved. deploy" — logged in
  vision/systemPrompt.md). Write-trivial subflow dispatched: land
  the exact entry in the Curriculum vocabulary source, regenerate
  the generated trees, verify the deployed skill, commit scoped to
  its own paths, push. In flight.
- The psyche questioned "agent bodies" in the top-stratum framing.
  Answered from the 358f143a record (door inputs; body not the
  whole top; placement itself not yet code-witnessed) and the
  Claude probe subflow's task extended to witness where a
  .claude/agents body actually lands.
- Vocabulary landing returned: Curriculum vocabulary.md appended
  (Curriculum commit 3c3161a, pushed), trees regenerated (primary
  commit 1763df7f2, pushed; flake.lock swept in by regeneration).
  Deployment witnessed by this flow: code read
  .claude/skills/vocabulary/SKILL.md:21 carries the entry verbatim.
- Claude probe returned (full happenings in its transcript; Claude
  Code 2.1.235, Nix store). Witnessed: --system-prompt and
  --system-prompt-file replace the vendor instructional body
  entirely; one identity sentence always survives ("You are a
  Claude agent, built on Anthropic's Claude Agent SDK."), custom
  text concatenated directly after it. Harness-composed regardless
  of replacement: tool schemas, system-reminder streams (skills,
  agent types, deferred tools), CLAUDE.md injection, user
  email/date/token budget. Environment block (cwd, git status) is
  dropped, not moved, under replacement. Appends:
  --append-system-prompt[-file] all modes; managed-settings
  appendSystemPrompt; --append-subagent-system-prompt print-only.
  Interactive-mode support of --system-prompt is help-text claim,
  not probed. Degradation probe: tools and permissions still work
  under a minimal replacement; vendor behavioral tuning gone, base
  training surfaces. Agent-body placement witnessed on the --agent
  path: the definition body lands inside the system block after the
  identity line and replaces the vendor body wholly; the
  Task-dispatched worker path is the same mechanism by indication
  but was not separately probed.
- Codex extraction returned (full happenings in its transcript;
  codex-cli 0.148.0, source read at tag rust-v0.148.0, commit
  ab52d179). Witnessed: the base prompt is per-model (server-catalog
  instructions_template with compiled-in prompt.md fallback);
  resolution priority is explicit config override, then resumed
  thread metadata, then catalog template. Full-replacement doors:
  config.toml `instructions` and `model_instructions_file`, and
  programmatic SessionCreateParams.base_instructions;
  `developer_instructions` appends as a separate developer-role
  message. Boundary: the instructions slot carries only the base
  prompt; AGENTS.md arrives as a user-role message, permissions/
  collaboration/multi-agent-role/skills as developer messages.
  Behavior-shaping content extracted verbatim, including "keep
  going until the query is completely resolved" and the friendly
  personality template ("optimize for team morale and being a
  supportive teammate").
- The psyche directed the method (verbatim in vision/systemPrompt.md):
  most offensive base-prompt blocks first, a replacement designed
  for each, through the entire offensive corpus. Corpus ranked
  across both harnesses by offense family (completion pressure,
  verdict pressure, friendliness shaping, pattern conformity, plus
  the prohibition-dense form as a composition-level offense).
  Block 1 (completion/autonomy pressure, both harnesses) presented
  with proposed positive-duty replacement. Awaiting ruling.
- Term drift ("system block", "vendor body" for the ruled base
  prompt) surfaced by the psyche. The psyche's cause diagnosis and
  vocabulary-override directive recorded verbatim in
  vision/vocabulary.md; both named context facts confirmed (skill
  loaded pre-deployment; update arrived only as a file read). The
  deployed vocabulary skill reloaded into this flow's context.
  Identity-sentence question answered: it is part of the base
  prompt by the approved definition; the witnessed base-prompt
  anatomy is a fixed identity sentence plus a replaceable
  instructional body. Override line proposed for the vocabulary
  skill. Awaiting approval.
