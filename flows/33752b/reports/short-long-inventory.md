# Short-term and long-term inventory, by area
Gathered 2026-10-13 for 33752b's short/long book. W = witnessed by this subflow (file read or
command run 2026-10-13); C = claim (comment, README, or an earlier audit's finding not re-run).
AA = flows/33752b/reports/anatomy-audit.md, VA = values-audit.md (cited, not redone).
PS = psyche-skills origin/main 5eecff3 (fetched). `flows/` paths are in /home/li/primary.
Ordering record, flows/d68c82/vision/deployment.md, 2026-10-13: "I want to move towards using the
nexuses everywhere. They're the long-term vision and then we have this short-term mission."
The terms are his (flows/d68c82/vision/psyche.md, 2026-10-13T17:12): "have the short-term
vision, the long-term vision, and that's it."
Deployment chain, witnessed once for all areas (W):
- Home packages reach the machine through CriomOS's flake.lock (origin/main 790bd75), not
  CriomOS-home's own lock: home-manager-path `orchestrate` is 0.37.0, matching CriomOS's pin
  c7c44cb, not CriomOS-home's pin 9070cbb (0.35.0).
- Last home generation 1057 is 2026-10-08 (CriomOS-home origin/main c2c0d6bf is 10-12). Hand
  `nix profile` entries: activate-messenger-clj, curriculum-resolver-deployment(-1).

## 1. Messaging
Long term:
- PS vision-flow.md 22 (W): "Message asks Flow to send a request to a metaflow; Flow owns the
  lock and the delivery, answers sent or queued, and Message subscribes to Flow's events".
- flows/d68c82/vision/deployment.md, 2026-10-13 (W): "The send command should use the same
  identifier that we're using now, which is the 3-field identifier of a metaflow. I want the
  whole system to use that everywhere."
Short term in use:
- W: `hm-send` is ~/.local/bin/hm-send, linked 2026-10-13 10:13 to messenger-clj-0.3.0
  (store zqq5v5…). Generation 1057 links hm-send to another store path (pqx78…), so the live
  link was placed outside the declared generation.
- W: `hm-list` keys routes by six-char flow id (`33752b psyche_core_primary_33752b`).
- W: messenger-clj core.clj 516-521 requires aspect, topic and layer together (`metaflow!`):
  the three-field id exists as TARGET. C (AA B4): the sender is still env `FLOW_ID` (core.clj 906).
- W: message-nexus 0.14.0 is installed, but no message-nexus unit runs and
  /run/user/1001/message does not exist. `message-daemon.service` failed 2026-10-11
  (start-limit-hit).
- Records call this shape makeshift (W):
  - flows/056f6d/vision/messaging.md, 2026-09-18: "the message Nexus for messaging each other,
    which we'll just use"; "for now, the agents will know that it's me because of how the
    message is formatted".
  - CriomOS-home modules/home/default.nix 81 calls it a "Compatibility messenger CLI" (a
    machine comment).
Unused or undeployed:
- W: Message source 0.19.1 (990f5bc); CriomOS pins 0.14.0 (930c516), 87 commits behind, plus a
  parallel `message-next` pin (481b579).
- W: five messaging stores in ~/.local/state, last write: hacky-messenger 09-25,
  messenger 10-03, message 10-03, message-next 09-26, messenger-clj 10-13.
- W: hacky-messenger is still watched by field-luna-heartbeat.nix 43 (unit masked) and read by
  tools/reaper 31 (AA B3) and tools/reap-flow.
Readjust (flow's inference):
- Deploy Message and Flow main through CriomOS. Once Message routes `Send` through Flow's Deliver, retire messenger-clj and the hm-* links.
- Rewrite the hm-send paragraph of the base prompt and knowledge-messenger to name Message and
  metaflow addresses.
- Delete the four dead stores, tools/reaper, tools/reap-flow and field-luna-heartbeat.

## 2. Flow launch and lifecycle
Long term (W):
- PS vision-flow.md 26-28: "A Nexus component decides the system prompt and everything about a
  launch, replacing the harness's subagents".
- PS vision-flow.md 56: "Every harness event reaches Flow through the harness's hooks calling
  the Flow CLI, so Flow knows each flow's state without polling".
Short term in use:
- W: launches run through tools/claude-main-flow-launch.mjs (plus codex-, opencode- and
  native-worker copies). Its mainFlowMode (150-162) installs a UserPromptSubmit reminder hook
  and a Stop hook to primary-committer/turn-end.mjs.
- W: no Primary launcher calls `flow`. Only tools/field-flow-preflight.mjs 13 names it, at the
  wrong path ~/.local/bin/flow (the binary is in ~/.nix-profile/bin).
- W: flow-nexus 0.14.0 runs, but ~/.local/state/flow/flow.sema was last written 2026-10-08.
  Ids are minted by `flow-id` from harness-0.6.1 (AA B4).
- Records sanction scripts for now (W):
  - flows/f5a6e9/vision/flow.md 91, 2026-10-07: "Let's modify the scripts that we're using now
    to launch all this."
  - flows/15b67974/vision/flowDaemon.md, 2026-08-21: "flow launches an existing harness for
    now; our own custom harness later".
- Tension (flow's observation, unruled):
  - flows/33752b/vision/committing.md, 2026-10-12 wants the env-var flow id as default: "We
    could just set the flow ID in the environment variable of that harness".
  - PS vision-flow.md 20 says: "No flow declares its id: every call to Flow is identified by the
    calling process". Which one is the short term is not stated.
Unused or undeployed:
- W: Flow source 0.26.0 (9f159d0) has Start/Restart/Stop/List/ResolveRecipient and
  crates/flow/src/hook.rs. CriomOS pins 0.14.0 (9fcd625), 119 commits behind, plus `flow-next`
  (bc464e5) and `flow_2` (ac6ab64).
- W: ~/.local/bin holds flow-next*.bak files (2026-09-26).
- W: no file outside their own directories references tools/flow-cli-poc (09-17),
  tools/flow-message-sandbox (09-26), tools/third-seat or tools/network-mode-nexus-poc.
- C (AA B7): tools/claude-native-seat-refresh.py is a second launch and refresh path.
Readjust (flow's inference):
- Deploy Flow main. Move skill selection, session id, title, hooks and registration from the four launchers into
  Flow's Start, and point the hooks at the `flow` CLI.
- Delete the launcher copies, seat-refresh script, POCs and extra pins; touches knowledge-flow
  (AA B11) and Curriculum's generated standing-skill-selection.mjs (AA B10).

## 3. Locking
Long term (W):
- PS vision-orchestrate.md 8-10: "Orchestrate is deployed unconditionally, in the home, for every
  user. Its meta binary is part of it".
- flows/5578cc/vision/locking.md, 2026-10-03: "No, Flow locks the sessions and [Orchestrate]
  locks the files."
Short term:
- W: orchestrate-nexus 0.37.0 runs. `orchestrate` and `orchestrate-meta` are in
  home-manager-path (CriomOS-home min/orchestrate.nix).
- C (AA B3): messenger-clj takes the delivery lock from orchestrate (core.clj 446-470) and
  retries every 50 ms. The session lock sits in Orchestrate and the messenger, not in Flow.
Unused or undeployed: W: source 0.37.1 (96e08e0) is 1 commit ahead of the deployed version. The
local working tree is a stale 0.36.1 checkout.
Readjust (flow's inference): the file lock is already in its long-term shape. Move the session
lock into Flow and drop the polling retry (PS vision-nexus 141-144).

## 4. Committing Primary
Long term:
- No record states a goalpost beyond the committer itself (W: grep "committer" finds three
  files).
- PS vision-committing.md 8-12 (W): "A commit made without paths takes the whole working copy,
  and is made only while the whole repository is locked".
- flows/33752b/vision/committing.md, 2026-10-12 (W): "a simple fucking system where there's one
  agent that commits and he just holds the lock and everybody just messages".
Short term (W):
- tools/primary-committer/ holds turn-end, seat-process, publish-selected and restart.
- recipient.json names 89fbc1, which hm-list shows as `field_quaternary_89fbc1 done`.
- The Stop hook is installed only when a committer id is passed (launcher 158-162).
- seat-process.mjs 38 fixes gpt-6-luna, low effort.
- CLAUDE.md still says "Only a main flow commits and pushes Primary, under its acquired
  PrimaryPublish turn".
- flows/d68c82/vision/committing.md, 2026-10-12: "We're only talking about primary committing".
Unused or undeployed: W: restart-service.nix defines a systemd unit inside Primary; none is
installed.
Readjust (flow's inference): propose removing CLAUDE.md's PrimaryPublish paragraph, which
contradicts the committer record. Move the committer seat's launch, model and hook to Flow.

## 5. Context modules and the system prompt
Long term (W):
- flows/d68c82/vision/context-modules.md, 2026-10-13T17:07: "Let's rename all of these repos.
  Psyche skills becomes Psyche context and so on."
- Same file, 17:27: "we have to modify the tool to use context modules from the context repos".
Short term (W):
- The repositories are still psyche-skills, mind-skills and field-skills; no context-* repo
  exists.
- curriculum-nexus.service (curriculum-0.1.0) projects .claude/skills (115 entries) and four
  other trees.
- tools/main-flow-mode/system-prompt.md (17 lines, uncommitted edits) is read by the launcher
  at line 152.
- flows/183ae0/vision/skills.md, 2026-09-29: "or we just scrap the whole idea of deploying
  skills for now".
Unused or undeployed:
- W: two hand `curriculum-resolver-deployment` profile entries.
- C (VA): CriomOS-home sets CURRICULUM_PSYCHES_SKILLS_DIR; Curriculum reads ..._REPOSITORY_DIR.
- C (AA A2): the Pi role patches duplicate roles.datom.
Readjust (flow's inference):
- Rename the three repositories and SKILL_VARIABLES `Psyche/Mind/Field skills`. Move system-prompt.md into psyche context as a non-agent-visible module.
- Let Flow compose prompts (PS vision-flow 30).
- Drop the Pi patches. Touches CLAUDE.md "Skills", PS vision-flow 36-42 and Curriculum projection.rs.

## 6. Books and the living's interface
Long term (W):
- flows/d68c82/vision/messaging.md, 2026-10-13T17:28: "we're hardcoding the idea that the
  living is reached through the books and this will eventually change to a better user
  interface ... just have one place where the machine is instructed on how to contact the
  living".
- flows/056f6d/vision/messaging.md, 2026-09-18: "Should create a way for me to send messages to
  certain layers eventually".
Short term (W):
- Books are claude.ai artifacts: 34 `claude.ai/artifact/` URLs appear in flows/33752b/log.md.
- operation-flashbook.md 35 orders "one fresh artifact for every presentation".
- Comments are fetched by tools/book-fetch.mjs.
- flows/1b8ac0/vision/finalResponse.md, 2026-09-21: "published on a public commentable website
  for now".
Unused or undeployed: none found (not searched deeply).
Readjust (flow's inference): collect "how the living is reached" into one module (today in PS
vision-book, intent-main-flow, the base prompt's Books section and operation-flashbook).
Everywhere else, write only "present it to the living".

## 7. Psyche records
Long term (W):
- flows/88475f/vision/nexus.md, 2026-09-25: "Psyche Nexus is going to replace how we log Psyche
  and Mind."
- flows/bad807/vision/sema.md, 2026-10-04: "eventually, not right now, design the [Sema]
  language to have appropriately annotated, marked-up psyche information".
Short term (W):
- Markdown records at flows/<id>/vision|notion/<topic>.md, crystallized into psyche-skills.
- flows/48cff7/vision/visionAsSkillSource.md: "until we do this fully typed in the psyche
  database, that basically becomes the anatomy for that."
Unused or undeployed (W):
- Repositories psyche (2026-08-14; README "isolated scaffold"), mind (08-13), spirit (08-13)
  and persona (09-12). None has a binary on PATH or a running unit.
- Their state remains: ~/.local/state/spirit (last write 09-10), spirit.bak-*, persona*,
  spirit-db-test-copy.sema.
Readjust (flow's inference): no near-term code. vision-psyche and knowledge-psyche "Where
psyche lives" would mark the file layout as short term and the Psyche Nexus as long term.

## 8. Deployment
Long term (W):
- flows/ebbe30/vision/deployment.md, 2026-10-09: "Eventually, we're going to have [Lojix] take
  care of the operation."
- flows/ebbe30/vision/lojix.md, 2026-10-09: "[Lojix] is my answer to [Nix]".
Short term (W):
- flows/d68c82/vision/deployment.md, 2026-10-13: "the only way to install anything on our
  system is to install it from source"; "all of the harness components installed in the home
  environment for now".
- In use: lojix 8.1.0 in /run/current-system; system generation 189 (2026-10-11); home
  generation 2026-10-08.
Unused or undeployed (W):
- Lojix source 9.0.1 (745bbe3); CriomOS pins 8.1.0, 4 commits behind.
- The hand profile entries and hm-* links (area 1).
- Leftover state directories lojix-location-33a4d4-retry1..5 and lojix-bootstrap-*.
- The field-luna-heartbeat unit is masked. No field-census or checkup unit is installed,
  though tools/field-census/*.service exist (VA 10).
- C (AA A3): the quiet-hours Herdr patch is applied but unconfigured.
Readjust (flow's inference):
- Bump the CriomOS pins (flow, message, lojix, orchestrate) to main and redeploy.
- Remove the hand profile entries, the .bak files, stray links and the next/_2 pins.
- Move the systemd units held in Primary into CriomOS-home, or delete them.

## 9. Memory and stores
Long term:
- PS vision-nexus.md 66 (W): "Its Memory is its own typed store, reached only through the
  memory engine; there is no central store".
- No record found names a central "Memory root" (W, grep). In edf227 and PS vision-nexus 182,
  "Memory" is each Nexus's ethos root for what it remembers.
Short term:
- W: flow.sema, lojix.sema, message.sema and orchestrate-nexus/.
- C (AA B3): messenger-clj uses Datalevin. C (VA H2): Flow's store is placed by rewriting HOME.
Unused or undeployed: W: the dead stores of areas 1 and 7.
Readjust (flow's inference): stores already follow the per-Nexus shape. The work is deleting
dead stores and moving the messenger's data onto Message's Sema.

## 10. Models per layer
Long term (W):
- PS vision-model-roles.md 39-40: "The model is declared once, as typed configuration in Flow,
  mutated only through the meta wire."
- flows/1ac573/vision/operational-modelDeclaredInOnePlace.md, 2026-09-18: "which is, for now, we
  can put it in Flow".
Short term: model names are declared in eight places (W): (1) PS vision-model-roles table;
(2) tools/native-voice-profiles.mjs 4-16; (3) SKILL_VARIABLES.md 5-7; (4) Curriculum roles.datom
(opus/sonnet/haiku, gpt-5.6-sol/luna, gpt-5.4-mini); (5) flow-defaults lib.rs 103-106; (6)
CriomOS-home min/default.nix 79, flow-message-next.nix 80-82, 158; (7)
native-main-flow-launch-shared.mjs 84; (8) primary-committer/seat-process.mjs 38.
Disagreements (W):
- roles.datom and flow-defaults still use gpt-5.6, and flow-defaults names Terra, which
  flows/d68c82/vision/model-roles.md (2026-10-12) says "was abandoned".
Unused or undeployed: C (VA 12): native-worker-launch.mjs 9 `gpt-5.6-terra`.
Readjust (flow's inference): Flow's meta Configure holds the one declaration, and skill
variables carry it by name. Delete copies 2 and 4-8 (Curriculum, flow-defaults, two
CriomOS-home modules, three Primary tools).

## 11. Added: welds into third-party software
Long term (W): flows/d68c82/vision/design.md heading "Never build our abstraction inside someone
else's"; base context "Herdr is third-party software that we never modify."
Short term: C (AA A1-A4): Herdr patches (executable selection, quiet hours), Pi prompt patches
and a Claude Desktop app.asar rewrite, all built by CriomOS-home.
Readjust (flow's inference): drop the patches as Flow takes executable choice and role text
moves to context modules.

## Unknowns
- Whether deployed Flow 0.14.0 already accepts hooks or Start: not run, no Flow query sent.
- That the 10:13 hm-* links came from `activate-messenger-clj` is inferred from time and name.
- Consumers of tools/messenger, msg, prompt-relay and extractor were not traced.
- That home deploys only through CriomOS's lock rests on one package version (orchestrate).
- No record found gives a stated shape for the committing goalpost or the "better user
  interface".
- No subflow ran; no Skill tool was used; FLOW_ID and FLOW_DIRECTORY were empty; no provenance
  receipt is available.
