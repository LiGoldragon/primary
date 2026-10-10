# Skill garbage audit

Subflow of 8904b1 (Psyche Fable), 2026-09-28. Read-only. All 72 authored skills in `/git/github.com/LiGoldragon/Curriculum/skills/` read whole. Word counts are `wc -w` on the source file, frontmatter included. The Curriculum head was 3726da5 (the logging edit to main-flow and psyche-interraction by the other subflow, landed 10:34). I suggest no wording for the lines that edit touched.

## Totals

- Now: 72 skills, 26,501 words.
- After these recommendations: 61 skills, about 17,500 words. That is about 9,000 words (34%) less.
- Mind seat startup (the launcher `tools/codex-main-flow-launch.mjs`, `ASPECT_SKILLS.Mind`: main-flow plus 17 others): now 7,444 words, 48,073 characters of source (the launcher measured 49,984 bytes including the brief). After: about 4,950 words, or about 32,000 characters. If refresh and testing-flow-titles are also taken off the Mind startup list, about 4,730 words, or about 30,000 characters.

## The ten largest cuts

| # | Cut | Words saved |
|---|---|---|
| 1 | Delete `field`. The Field seats ended today, and its Luna timers and census were removed (witnesses/services-0928.md). | 958 |
| 2 | `claude-harness`: remove the Operators' notes section (four 2026-09-16/17 incidents, with session UUIDs) and the version-dated permission paragraph. | 516 |
| 3 | Delete `operational-status-presentation`. It requires a datom message body, against today's ruling. | 514 |
| 4 | `main-flow`: remove the Terra/Luna lines, the psyche-audit companion paragraph, the subflow-scripts paragraph, the launcher paragraph (repeated in refresh) and the duplicate native-seat sentence. | ~490 |
| 5 | Delete `operators-notes`, a procedure written for incidents. | 490 |
| 6 | `refresh`: remove the Field two-seat refresh, the source-hash audit, and the launcher paragraph that repeats main-flow. | ~460 |
| 7 | Delete `subflow-scripts`. No script in its catalogue is registered anywhere. | 420 |
| 8 | `lojix`: remove the version history ("Since lojix 6.0.0", schema v2/v3/v4), the Rust library surface and the 0700 story. | ~350 |
| 9 | `testing-transitive-network-topology`: keep the invariants and the chain case, and remove the WPA-Enterprise, EAP-TLS and AP gate procedure. | ~315 |
| 10 | Delete `testing-session-registry`. It describes a Transition/supervisor mechanism the launcher does not run. | 304 |

Next in size: `compensation-messenger-clj` (~300), `flow-communication` (~270, which absorbs operational-layer-communication), `metaflow` (241), `messaging` (~235).

## Delete whole (11)

`field`, `metaflow`, `operational-status-presentation`, `operators-notes` (and the notes sections of claude-harness and codex-harness), `subflow-scripts`, `testing-session-registry`, `testing-harness-visual-state`, `testing-flow-titles`, `deepseek-harness` (the living approved it on 2026-09-05; dsh is not installed; **the choice is the living's**), and the two merged below, which leave no file.

## Merge (4)

- `operational-layer-communication` into `flow-communication`.
- `testing-message-route` into `compensation-messenger-clj`, which already carries the same receipt grades.
- `testing-push-landed` and `testing-commit-scope` into `file-editing`, which already states both rules, and `field-clj #commit` performs the commit-scope check itself.

## Contradictions

C1, remote title.
- main-flow: "A main flow's remote native title is a Datom struct, `<Aspect>V2.{ <Model> <FLOW_ID> }`". testing-flow-titles: "High, Medium, Low, and Ultra Low remain typed behavioral powers and do not appear in the native title."
- Against these, refresh: "derive its remote title as `<Aspect> <Power> <FLOW_ID>`". correction: "require the corrected format <Aspect> <Power> <FLOW_ID>".
- The launcher writes the V2 form (read back "MindV2.{ Astra 6f51ad }"), so refresh and correction are the stale side.

C2, testing a route before a send.
- messaging: "Use a safe isolated test before relying on a route: disposable recipient, harmless unique marker, one exact identity binding, bounded wait, target-side observation, then cleanup."
- testing-message-route: "A routine send needs no preflight probe or second resolution."

C3, fallback after a refusal.
- compensation-messenger-clj: "When HM refuses, a flow may prompt the target pane directly through Herdr, and names the refusal in that message."
- testing-message-route: "Do not retry an `Uncertain` result, reroute, or fall back to another channel."

C4, conflicting psyche records.
- psyche-distillation: "When readings overlap or contradict, the more recent and the more certain statement is favored."
- psyche: "surface the tension to the psyche rather than choosing by a strict supersession rule."

C5, skill approval.
- psyche-interraction: "Get approval before every skill edit."
- skill-designing: "`testing-` is machine-generated and mostly unreviewed: field-level authority, approved by Mind automatically."
- A second tension inside the same topic: skill-designing says "`operational-` has been reviewed and approved by the psyche". The psyche skill says operational skills "support faster iteration with an overview to the living". The living, on 2026-09-20, called the mind layer "integrated, but not specifically reviewed by the psyche" (flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md).

C6, dirty changes.
- file-editing: "Commit existing dirty changes first with an appropriate message before starting new work."
- The same skill: "only the files this flow edited". testing-commit-scope: "Every path returned must be one this flow edited."
- The two can be reconciled (a separate commit for found changes), but the testing skill would mark that commit as failed.

C7, green builds.
- testing: "Infrastructure reports are ground: a build reported green is green, wherever it ran."
- nix-workflow: "A Nix command alone does not prove offload: retain the remote-builder evidence for a claimed remote build."

C8, against today's ruling. operational-status-presentation: "The status presentation is one datom ... passed directly as the body of one message". The living (8904b1-2): "we don't need Datom syntax where the program doesn't need it".

C9, vocabulary. vocabulary: "Use machine, not AI; use flow, not agent". The spirit and psyche skills (the living's words) say "AI" and "Agents" throughout. I note this only. The spirit and psyche wording is the living's.

## Repetitions (one home each)

| Rule | Where it is stated now | Keep in |
|---|---|---|
| Receipt grades Submitted/Transported/Presented/Read/Completed | messaging, behavior, testing-message-route, compensation-messenger-clj, testing | compensation-messenger-clj |
| "When the living names ... Terra, Luna, or low power ... address the other native main seat" | main-flow, flow-communication, operational-layer-communication, field | flow-communication (with Terra removed) |
| Launcher composes one first prompt led by main-flow, reads it back | main-flow, refresh (almost word for word) | main-flow, or better only in launcher code |
| Remote title format | main-flow, testing-flow-titles, refresh, correction (conflicting) | main-flow, one sentence |
| Up for authorization, down for delegation, cross then escalate | flow-aspect, flow-communication, operational-layer-communication | flow-communication |
| Every seat logs the living's words and forwards to Psyche | main-flow, flow-aspect, flow-communication | main-flow |
| Push proof by `git ls-remote` | file-editing, testing-push-landed | file-editing |
| Commit only own paths / `jj diff -r @- --name-only` | file-editing (twice, with the field-clj text), testing-commit-scope | file-editing |
| Do not wake a flow to test delivery | behavior, testing, testing-message-route, messaging | behavior |
| Stop a process by the PID held, never by pattern | testing, testing-long-run-progress | testing |
| CLI takes exactly one inline datom, no flags, never a file | nexus (twice), datom, orchestrate, lojix | datom (the tool skills name only their own requests) |
| Subflow script definition | vocabulary, main-flow, subflow-scripts | none (delete) |
| Field refresh: two seats, `field-*-of-<id>`, crossover | field, refresh | none (delete) |
| Testing-worker role | testing (last paragraph), the roles.datom `tester` description | roles.datom |
| Psyche's four levels and where psyche lives | psyche; psyche-interraction repeats the Vision/Intent/Spirit entry rules | psyche |
| Flow Nexus "do not call a subagent a Flow Nexus flow" | nexus, field | none |

## Dead references found

- **Terra** (withdrawn): main-flow lines 11 and 14, flow-communication, operational-layer-communication, field, voice-psyche.
- **Pi** (deprecated): skill-designing "`{% if pi %}`"; nix-input-upgrade "(Pi v0.83 grew a new argument)".
- **Flow Nexus as the launch path**:
  - messaging "Flow Nexus 0.3 is the identity and resolution design". The installed unit is 0.12.2/0.14.0, and it is not used to launch seats.
  - field "Do not call collaboration-tool subagents native Flow-Nexus flows".
  - nexus's Flow Nexus paragraph.
  - file-editing "field-clj 'observe []' reads only the current flow-nexus user-service state".
- **Message Nexus versions**: messaging "Message Nexus 0.12 is installed ... The published-not-deployed 0.13 receipt query is not live" is an "as of" statement.
- **Field seats and cadence**: field "Field Luna runs ... every thirty minutes" (the timers were removed today); field and refresh on Field Astra and Field Sol as seats (they ended today).
- **`meta-lojix`** (operating-system): no such command; it is `lojix-meta`.
- **`transcript`** (transcript-search): not on PATH. The repository `/git/github.com/LiGoldragon/transcript` exists. It should be installed or the skill deleted.
- **`ethos-zero`** (ethos): not on PATH. It may be run from its repository; I did not check.
- **dsh** (deepseek-harness): not installed.
- **The subflow-scripts catalogue** (`find-codex-session`, `queue-to-codex`, `read-transcript-tail`): not registered anywhere I found (tools/, ~/.claude/agents).
- **testing-session-registry**: "A SessionStart hook registers that binding atomically in the registry". The only SessionStart hook is Herdr's own `herdr-agent-state.sh`. The `Transition.{ predecessor successor-expected since deadline }` the launcher sets does not exist; messenger-clj has only a boolean `transition`.
- **testing-harness-visual-state**: "Every harness's visual indicators are documented in operators' notes by harness and version". No such notes exist.
- **visual-report-from-md**: "a fitting one- or two-emoji favicon". The Artifact tool now takes an `icon` word, and `favicon` is deprecated.
- **Old names in datom examples**: operational-status-presentation's examples name flows 6288d1 and 3c91a7, Flow 0.4, and seat 5f38bc.

## Per skill

Columns: words now; verdict; words after; kind of garbage (numbers as in the brief: 1 dead reference, 2 incident residue, 3 repetition, 4 contradiction, 5 gate growth, 6 unused test/operational mechanism, 7 ornamental); confidence.

| Skill | Now | Verdict | After | Kind | Conf. | Passages |
|---|---|---|---|---|---|---|
| agent-harness-packaging | 173 | trim | 110 | 2,5 | med | Cut "StablyAI Orca is `orca-ide`, not GNOME `orca`" (one incident) and "A skill catalog projection also needs a receipt that its explicit, user-only route loads..." |
| beads | 460 | trim | 380 | 3 | low | Parts of the Fields/Lifecycle lists restate `bd --help`. Keep the conventions (title is the outcome; close reason carries evidence; no parallel bd). |
| behavior | 213 | trim | 140 | 3 | high | Cut "Grade delivery claims at the observed boundary..." (kept in compensation-messenger-clj) and merge "Prefer passive observations..." into one sentence. |
| breaking-upgrades | 113 | keep | 113 | — | med | The countdown rollback may be 5; its source is not traced. |
| claude-harness | 1076 | trim | 560 | 2,1 | high | Cut the whole "## Operators' notes" (2026-09-16/17, session and record UUIDs), "Use operators-notes to read or compose...", and "Claude Code 2.1.280's code shows it only while ... read from code, not yet witnessed live". The rest was approved by the living (d9dfeeb). |
| codex-harness | 523 | trim | 390 | 2 | high | Cut "### 2026-09-17 — Flow identity helper arguments" and the operators-notes line. |
| compensation-messenger-clj | 718 | trim, absorb testing-message-route | 420 | 3,2,4 | med | Cut "Whoever changes messenger-clj updates `skills/compensation-messenger-clj.md` in the same landing" (a landing gate), the 1,048,576-byte and JSON-escaping detail, "Historical numbered psyche attempts remain readable; current sends do not write part fields", and most of the hm-repair argument walk-through (the command's own refusal output teaches it). Resolve C3. In the Mind startup set. |
| compensation-nix | 429 | keep | 429 | — | high | Traced to the living, 2026-09-26 (flows/e167d8/vision/testRepos.md). |
| compensation-nix-rationale | 434 | trim | 400 | 2 | med | Cut "as CriomOS-test-cluster's 586 lines show" and "The gate was seen failing ... built on the remote builder" (a receipt). |
| context-strata | 213 | keep | 213 | — | high | Approved by the living. |
| correction | 178 | trim | 125 | 4,2 | high | Cut "For a correction to a flow's remote title ... <Aspect> <Power> <FLOW_ID>..." (C1, one incident). |
| datom | 1019 | trim lightly | 960 | 2,3 | med | Cut "Today a parenthesized text lands as a plain String, with the Meaning type marked in code." and "omittable fields are not yet". A tool-syntax skill the living wants kept ("If a tool requires datom syntax, then the skill is going to say it"). |
| deepseek-harness | 153 | delete (**living-approved; choice open**) | 0 | 1 | med | dsh is not installed. The whole skill describes a harness nobody runs. |
| design | 100 | trim | 65 | 5 | low | "Every second or third turn, check whether a subject ... has raw vision accumulating across flows. When it does, dispatch a subflow..." is a recurring step; source not traced. User-only role skill. |
| disk-hygiene | 33 | keep | 33 | — | high | |
| documentation-placement | 146 | keep | 146 | — | med | |
| edit-coordination | 71 | keep | 71 | — | high | |
| ethos | 978 | keep | 978 | 1? | med | ethos-zero is not on PATH; check. Otherwise a tool-syntax skill. |
| feature-development | 40 | keep | 40 | 7? | low | Close to "true of any competent agent"; NON_MANAGEMENT_AGENTS.md already says RequestWorktree. |
| field | 958 | delete | 0 | 1,2,5,6 | med | The Field seats ended today, and the thirty-minute Luna pass and the census and checkup timers were removed. It is full of gates: judge input requirements, "no-new-work preflight", readiness gates, crossover. Its one-line definition already lives in flow-aspect ("Field is fixing, deploying, debugging, and maintaining"). If a Field seat returns, write it fresh. |
| file-editing | 349 | trim, absorb two testing skills | 230 | 1,3,4 | high | Cut "field-clj 'observe []' reads only the current flow-nexus user-service state..." and "A source file is written in pieces of a few hundred lines..." (misplaced). Keep one sentence each for scope proof and push proof. Resolve C6. |
| flow-aspect | 311 | trim | 230 | 3,7 | med | Cut "Every aspect logs the living's words..." (main-flow has it), "Each maps to a nexus, a data repo, and a skill type. Flow is the field aspect. Message is the mind aspect. A psyche nexus is coming." (intention), and the vertical-authority paragraph (flow-communication has it). |
| flow-communication | 477 | trim, absorb operational-layer-communication | 210 | 6,3,1 | med | Cut the rung/cell routing paragraph ("select the unique eligible cell ... nearest eligible rung ... explicit undeliverable result"): hm-send implements no such router. Cut "Low-priority channels exist below the user prompt ... MCP server at tool-call strata" (intention), the Terra sentence, and "Keep aspect, exact native model identifier, model display, behavioral power, Flow ID, and native binding as separate typed facts." |
| flow-evidence | 75 | keep | 75 | — | high | |
| herdr | 291 | trim | 90 | 1,7,2 | high | Cut "Version at the time of this skill: 0.8.2", the verb list (the skill itself says to run `--help`), "The tier-priority messaging system (hard abrupt / middle / soft) will deliver its bytes..." (intention), and the "not 'herder'" story beyond one line. In the Mind startup set. |
| lojix | 1803 | trim | 1450 | 2 | med | Cut "## Rust library surface" ("Since `lojix` 6.0.0 ..."; for developers, not for callers), "Reset removes and recreates recognized v2/v3/v4 stores as v5", and "A parent left at the default umask (`0755`) is refused ... `chmod 700` each parent" (keep only "each parent must be mode 0700"). The request anatomy stays by the living's word. |
| main-feature-integration | 30 | keep | 30 | — | med | |
| main-flow | 1274 | trim | 780 | 1,3,5,4 | high | Cut: "Default routine inspection ... Luna worker. Use Terra for implementation..."; the psyche-audit paragraph "When auditing work against psyche, delegate the substantive comparison to a judgment-capable companion at medium effort: Terra in Codex..." (a gate, and Terra); "*Subflow scripts.* ..."; "Before the first implementation edit ... retain the dispatch receipt" (keep "delegate implementation"; drop the receipt); the native-model paragraph (flow-communication has it); the launcher paragraph "Before any native launch is treated as a main flow..." (the launcher code does this; seats do not need it); and the empty heading "## Flow summary" that sits above "## Flow refresh" (misplaced). Leave the lines touched by 3726da5 alone. |
| messaging | 344 | trim | 110 | 1,2,3,4 | high | Cut the Flow Nexus 0.3 and Message Nexus 0.12/0.13 paragraphs, the receipt grades (moved to compensation-messenger-clj), and "Use a safe isolated test before relying on a route..." (C2). Keep: name the layer; submission is not a read; re-resolve after a terminal replacement; body only. |
| metaflow | 241 | delete | 0 | 6,7 | med-low | Four Field power tiers for Field seats that ended today; mostly "a tier changes the amount of judgment". A status-presentation example cites "6cc91b metaflow Distilled", but there is no Vision/metaflow.md. **If a record of the living's is found, the choice is the living's.** |
| nexus | 1174 | trim | 1080 | 1,3 | med | Cut "Do not call a collaboration-harness subagent a Flow Nexus flow. A Flow Nexus is ... Message Nexus owns ... when deployed." and the second "Datom passes inline at a CLI boundary, never as a Datom file." Design doctrine is largely the living's (see nexus-rationale). |
| nexus-rationale | 167 | keep | 167 | — | high | The living's reasoning. |
| nix-input-upgrade | 349 | trim | 200 | 2,1 | high | Cut "GTK 4.22.4 (nixos-unstable, Aug 2026) did not contain MR !10130 ... 4.23.3", "niri-flake pinned v25.08 while nixpkgs already carried v26.04", "(Pi v0.83 grew a new argument)", and the "e.g. home-manager renaming `programs.vscode`..." example. Keep the rules they illustrate. |
| nix-workflow | 184 | keep | 184 | 4 (C7) | med | |
| operating-system | 92 | fix one word | 92 | 1 | high | "`lojix` and `meta-lojix`" should read `lojix-meta`. |
| operational-layer-communication | 196 | merge into flow-communication | 0 | 3,1 | high | Keep only "The living speaks to the top seat of each component... A psyche session is for the exchange of ideas; work goes to subflows." Cut the Terra field-power line. |
| operational-status-presentation | 514 | delete | 0 | 4,1,2 | high | A datom message body, against today's ruling; examples full of flow ids and version numbers. No psyche record for it found. |
| operators-notes | 490 | delete, with the notes sections | 0 | 5,2 | high | The living asked for notes "so I don't have to review it so much" (flows/9993b5/vision/operatorsNotes.md, 2026-09-17). The skill added attention states (`pending`/`seen`), acceptance states (`awaiting-glance`), five block categories, and "Keep pending blocks visible in the next psyche-facing response ... until seen". That is more review, not less. |
| orchestrate | 285 | trim | 230 | 2 | med | Cut "The current `orchestrate` CLI reads one `Observed` frame and exits; it does not yet hold the connection open ... not the designed one." Keep "re-issue Observe.Locks to see a change". Also cut the "FlowIdDocumentation remains valid" aside. |
| prompt-crafting | 82 | keep | 82 | — | high | |
| protos | 788 | keep | 788 | — | high | Design, approved by the living. |
| psyche-acquisition | 307 | keep | 307 | 5? | low | The "Capture audit" procedure (counts, citation quality, coverage) is heavy but only loaded when asked. |
| psyche-distillation | 500 | trim | 470 | 4 | med | Resolve C4 by cutting "When readings overlap or contradict, the more recent and the more certain statement is favored." The rest carries the living's rules. |
| psyche-grasp | 111 | keep | 111 | 7? | low | "provisional — TO BE REVIEWED by the psyche" since August; marks exist in core-ethos, core-schema and core-nomos. Ask the living. |
| psyche-interraction | 1013 | trim (after the other subflow lands) | 850 | 3,1 | med | Candidates: the relay sentence "retrieve each verbatim ... send it as its own `hm-send TARGET --psyche CONTEXT VERBATIM`" (tool detail, in compensation-messenger-clj); "A tier word beside a model, such as 'Sonnet low'..." (vocabulary's); the repeated Vision/Intent/Spirit entry rules (psyche's). Much of the rest is the living's recorded rules; mark each before cutting. |
| psyche | 695 | keep (**the living's**) | 695 | — | — | Distilled Vision (Vision/psyche.md). Two passages a flow may wish to ask about, choice open: "Operational vision skills use the `operational-` prefix and support faster iteration with an overview to the living..." (part of C5) and "Psyche data belongs in a dedicated repository ... Primary Next ... This is a target shape, not authorization..." (a target, not a present fact). |
| realization | 50 | keep | 50 | — | high | |
| refresh | 678 | trim | 220 | 1,3,5,4 | high | Cut the Field refresh paragraphs ("create exactly two fresh main seats: `field-astra-of-...`", crossover, "A Field refresh is ready only when..."), "Each launch profile declares an audited list of the newest applicable Vision sources ... accept the launch only after the selected source hashes still match" (the launcher does no such check; C1), and the first-prompt assembly paragraph (it repeats main-flow; the launcher code owns it). Keep the witness-before-continuing rule, 60%/20%, and "never resume a known-corrupted history". Consider taking it off the Mind startup list. |
| repository-lifecycle | 90 | keep | 90 | — | med | |
| secrets | 92 | keep | 92 | — | high | |
| skill-designing | 675 | trim | 560 | 1,4 | med | Cut "`{% if pi %}`" from the target-condition sentence. Rewrite "## Authority by prefix" to one line that matches the living's words (C5). Move "A skill stays within a couple of hundred lines..." out of that section. "Write a rule only when it prevents a failure that has happened ... Name the incident" is the root of the incident residue: it should say the rule names the failure, never the incident's date, flow or version. |
| spirit | 268 | keep (**the living's**) | 268 | — | — | |
| stale-lock | 112 | keep (**text approved by the living**, dd14ce7) | 112 | 5 | low | "record the lock, its paths and the holder's state in a receipt" is a receipt step; the living's quoted words ask only "break the locks". |
| subflow | 159 | keep | 159 | — | high | |
| subflow-scripts | 420 | delete, with the main-flow paragraph and the vocabulary term | 0 | 6,5 | med-high | No script is registered; "New scripts are proposed to the living before landing" and the profile-approval rule are gates. |
| testing-commit-scope | 128 | merge into file-editing | 0 | 3 | high | field-clj #commit already refuses when `jj diff -r @- --name-only` differs from the named set. |
| testing-flashbook | 263 | keep | 263 | — | med | In use (flows/d8df70/flashbooks); rendering rules traced to flows/0625c3/vision/flashbook*. |
| testing-flashbook-illustration | 179 | keep | 179 | — | med | The living's taste, traced to 0625c3. |
| testing-flow-titles | 180 | delete | 0 | 3,6,5 | med | The launcher code enforces the title and reads it back. The adapter test matrix ("wrong aspect, model, power declaration... rollback after partial mutation") describes a test suite nobody runs. The format stays in one sentence of main-flow. In the Mind startup set. |
| testing-generated-projection | 158 | trim | 120 | — | med | In use (skills are regenerated today). Cut "This is the one place text comparison is a real test" (testing says it). |
| testing-harness-visual-state | 171 | delete | 0 | 6,1 | med | Depends on a catalogue of indicators in operators' notes that does not exist. |
| testing-long-run-progress | 197 | trim | 150 | 3 | low | Useful and generic. Cut the PID line (testing has it). |
| testing | 392 | trim | 250 | 3,4 | med | Cut the testing-worker paragraph (the roles.datom `tester` holds it) and "Live acceptance has a boundary..." (messaging's topic). Resolve C7. In the Mind startup set. |
| testing-message-route | 209 | merge into compensation-messenger-clj | 0 | 3,4 | high | Keep only "one `hm-send` call is the route proof; report the printed grade". |
| testing-push-landed | 139 | merge into file-editing | 0 | 3 | high | file-editing already says "confirm the pushed revision against the real remote directly — `git ls-remote <real-remote-url>`". |
| testing-session-registry | 304 | delete | 0 | 6,1 | med | See the dead references above. |
| testing-transitive-network-topology | 515 | trim | 200 | 6,5 | med-low | Keep the living's pattern (built-in port up, USB down), the invariants, and the Ouranos → Prometheus → Zeus chain case. Cut the stable Ethernet / Optional AP / WPA-Enterprise / EAP-TLS paragraphs ("requires an authorized network-admin action, a transactional health gate, an audit record, and rollback"), which describe features not built. The cable chain is live work today, so keep the rest. |
| transcript-search | 111 | keep if `transcript` is installed; else delete | 111 | 1 | med | The command is not on PATH. |
| versioning | 39 | keep | 39 | — | high | |
| visual-report-from-md | 405 | trim | 330 | 1,3 | low | Cut "fitting one- or two-emoji favicon" (now an `icon` word). Its design block largely repeats testing-flashbook. Whether anyone calls it is unknown. |
| vocabulary | 290 | trim | 220 | 3,1 | med | Cut "Subflow script: ...", "Past: ...", "Vision impurity: ..." (psyche-interraction defines it in use). In the Mind startup set. |
| voice-psyche | 107 | trim | 75 | 1 | med | Cut "If Luna cannot resolve it, send Terra the unresolved question together with Luna's findings and context." |

## Kinds of skills: what the living allowed, and what happened

### What the living allowed (the living's words)

- **Operational skills.** 2026-09-17, flows/108ab0/vision/operational-skillsAreVision.md: "If there's an operational skill, these can be agent-written on a light proposal, like glance-type approval. That doesn't mean they're fully endorsed, but that they are thought to be valuable enough for the agents to load them."
- **Overview for operational vision.** 2026-09-18, flows/8393ca/vision/operational-herdrVoiceAccess.md: "log all of this psyche, as vision, as operational vision, and present it back to me ... Give me the the quick o-overview of it all".
- **No prefix.** Same file, 2026-09-18: "Put that in the right vision/skill, without a prefix, or accepted by the Psyche as well. The unprefixed stuff is like the gold of the Psyche, basically the most reliable."
- **Test skills.** 2026-09-18, flows/1ac573/vision/operational-testTypeSkills.md: "they can put test skills in of their own judgment if they're using psyche as a base, so they put in that justification. That's basically what the message, the log description, and the commit messages are all going to be about."
- **Field layer.** 2026-09-20, flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md: "Once it's all approved, the field layer can operate by releasing skills without asking for permission because they need to operate." Same record: "The mind, as I said, is integrated, but not specifically reviewed by the psyche."
- **The prefix rule itself.** 2026-09-21, flows/1b8ac0/vision/skills.md: "Keep this civilized and well-labeled and well-separated, with the prefix to say, 'Testing is machine-generated, mostly not reviewed.' That's like field-level authority ... operational things that have been slightly reviewed by the psyche, by the living, and approved by the psyche. The testing is approved by the mine [Mind] automatically."
- **Compensation.** 2026-09-24, flows/752e0f/vision/layers.md: "Let's call it compensation ... compensation is Field ... it's welded in place for now to compensate, to make the system run". 2026-09-25, flows/e51411/vision/launch.md: "Do we have a compensation skill that documents how to use this HM panoply of tools and keeps it up?"
- **Operators' notes.** 2026-09-17, flows/9993b5/vision/operatorsNotes.md: "where you can put your stuff so I don't have to review it so much."
- **What is not ruled.** No record governs the `-rationale` suffix. The psyche skill's sentence (Vision/psyche.md) names operational-, testing- and no prefix, but not compensation-.

### What happened (Curriculum history, 2026-09-07 to 2026-09-28)

- **Current skills by kind.** 72 skills: 56 unprefixed (counting `testing` itself), 11 `testing-`, 2 `operational-`, 3 `compensation-`. Across history 18 prefixed skills were created: 12 testing-, 3 operational-, 3 compensation-. Deleted: operational-final-response and testing-datom-messaging (09-27) and flow-message (09-21, unprefixed).
- **Who wrote the testing skills.** All 11 were made by flows. Five (commit-scope, push-landed, generated-projection, long-run-progress, message-route) came in one Claude Fable 5.1 commit (dad80ad, 09-19, "each proving one thing that failed or was hard in flow f38926's night"). Six came in commits with no model trailer, which I read as Codex seats; the author field is always "li". That fits the 09-18 ruling.
- **Who wrote the operational skills.** Psyche Fable wrote all three. final-response and layer-communication (4526932, 09-19) were "On the living direct request of 2026-09-19". status-presentation (210befc, 09-24) has no psyche record I could find. The final-response skill was deleted on 09-27 by the living's ruling. Evidence of the quick overview being shown exists only for the 09-19 pair (via the direct request). For status-presentation I found none.
- **Who wrote the compensation skills.** messenger-clj (09-25, no trailer, changed 16 times in four days) and nix (Opus 5.5, 09-26). Both trace to the living's requests.
- **Churn.** 105 commits touched skills. 34 carry a Claude trailer; the other 71 carry none. Only 11 of the 105 commit messages cite an approval, a request or a ruling of the living.
- **Unprefixed skills changed by flows.** 36 unprefixed skills (one, flow-message, since deleted) were changed in commits that cite no approval. The most changed: main-flow (18 such commits), field (12), refresh (7), messaging (6), file-editing (4), claude-harness (4).
- **New unprefixed skills.** These were created in the window by flows, carrying no prefix, and most describe operational mechanism: field, metaflow, messaging, refresh, flow-aspect, flow-communication, herdr, operators-notes, stale-lock, subflow-scripts, voice-psyche, visual-report-from-md. Some of them may have been approved in conversation; stale-lock was ("Land stale-lock text as the living approved it"). I did not trace the other 94 commits into flow logs, so "no cited approval" is not proof of "no approval".

### Verdict in plain words

The prefixes were half respected. Flows used `testing-` freely, as allowed. But most operational text went into unprefixed skills, which by the living's rule are the "gold", approved by the living: field, metaflow, messaging, refresh, flow-communication, operators-notes and subflow-scripts are operational in content with no prefix. main-flow and refresh were rewritten about 25 times by flows, mostly without a cited approval.

Two skills now state the prefix rule differently from the living's own looser words. skill-designing says operational means "reviewed and approved by the psyche"; the living on 09-20 said the mind layer is "not specifically reviewed". psyche-interraction still says "Get approval before every skill edit", which no testing skill obeyed. The overview that operational skills were to come with shows up only where the living asked directly.

On implementation, of the prefixed and flow-written operational skills:
- **In use:** compensation-messenger-clj, compensation-nix, testing-message-route, testing-flow-titles, testing-generated-projection, testing-push-landed, testing-commit-scope, testing-long-run-progress, and the flashbook pair.
- **Describing mechanisms that do not run:** testing-session-registry, testing-harness-visual-state, most of testing-transitive-network-topology, field, metaflow, subflow-scripts, the routing rungs of flow-communication, and operators-notes' attention states.
- **Against today's ruling:** operational-status-presentation.

It was not a circus in the testing prefix. It was a mess in the unprefixed skills, where flows kept adding procedure on their own reading.

## What I was unsure of

- Whether `transcript`, `ethos-zero` and dsh are meant to be run from their repositories rather than PATH.
- Whether any flow still calls visual-report-from-md.
- Whether Field seats will return. If they do, parts of field and metaflow may be wanted, but rewritten short.
- Whether metaflow and status-presentation have a psyche record I missed.
- Whether the 94 commits without a cited approval had approval in conversation.
- Character counts after trimming are estimates scaled from word counts.

## Sources

- `/git/github.com/LiGoldragon/Curriculum/skills/*.md` (72 files) at 3726da5; `roles.datom`; `ARCHITECTURE.md`; `git log` of Curriculum since 2026-09-07 (105 commits touching skills/).
- `/home/li/primary/tools/codex-main-flow-launch.mjs` (`ASPECT_SKILLS.Mind`); `/home/li/primary/SKILL_VARIABLES.md`; `~/.claude/settings.json` hooks and `~/.claude/hooks/herdr-agent-state.sh`; `command -v` for hm-*, flow-id, field-clj, orchestrate, transcript, lojix, lojix-meta, meta-lojix, herdr (0.8.2), bd, ethos-zero, dsh, pi, claude (2.1.280).
- `/home/li/wt/primary/56ae53/flows/8904b1/witnesses/services-0928.md`, `witnesses/mind-astra-launch-0928.md`, `launch/mind-astra-brief.md`, `vision/datom.md`, `vision/logging.md`, `log.md` (tail).
- Psyche records: Vision/psyche.md; flows/108ab0/vision/operational-skillsAreVision.md; flows/8393ca/vision/operational-herdrVoiceAccess.md; flows/1ac573/vision/operational-testTypeSkills.md; flows/b81560/vision/operational-ethosSpecSkillAndTriadBranches.md; flows/1b8ac0/vision/skills.md; flows/752e0f/vision/layers.md; flows/e51411/vision/launch.md; flows/e167d8/vision/testRepos.md; flows/9993b5/vision/operatorsNotes.md; flows/0625c3/vision/flashbook*.md (the psyche record search was done by a read-only subflow).
- `/git/github.com/LiGoldragon/messenger-clj/src/messenger_clj/typed_store.clj` (transition field); psyche-grasp marks in core-ethos, core-schema, core-nomos.
