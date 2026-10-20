# Audit: vision not deployed, and compensation that works around vision

Read-only audit for 379e7a, 2026-10-19, observed 18:15–18:23 CST on ouranos. W = witnessed in this audit (command or file read, named). C = claim from a flow log or record, not re-observed. I = this subflow's inference.
Sources read at: psyche-context origin/main 2d9fbb6, field-context origin/main 785ceb0 (the local checkout is detached at 5070467 and stale), CriomOS origin/main 8d38ffd, CriomOS-home origin/main 5a52224e.

## 1. The CriomOS declarative statement

| Item | Finding | Mark |
|---|---|---|
| Statement | psyche-context `vision/criomos.md:8` "CriomOS is a declarative operating system: nobody edits a file on a host." `:10-11` "A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy. Every hotfix in place is removed and replaced by that fix." | W |
| "Nothing is stateful" | That phrase is in no psyche-context module. The nearest record is raw `flows/379e7a/vision/deployment.md` (18:13 today): ".local/bin ... This is stateful. This is against our rule to use the declarative operating system deployment." | W |
| Short or long term | Neither line has a short-term marker. Under `intent/psyche.md:10` ("an unmarked vision is long-term"), both read as long-term. No "now" or "deploy now" text appears in criomos.md or in book 82-criomos-4. This weighs against the living's reading that the module was "marked to be deployed now". | W (I for the reading) |
| Landing | 4de1d9a, 2026-10-19 11:38. Message: "Approved by the living: flows/d68c82/log.md ... proposal 1 of book 82-criomos-4". Raw source: `flows/d68c82/vision/criomos.md:1-4` (2026-10-11). | W |
| Deployed to flows? | Not deployed. No `vision-criomos` skill exists in `.claude`, `.agents`, `.codex`, `.opencode` or `.pi` under /home/li/primary (each tree has 133 skills, all dated 2026-10-15 19:46). | W |
| Who promised deployment | No sentence promising that the criomos vision in particular would be deployed was found in flows/*/log.md, books or the relay ledger. The general promise is field-context `compensation/book-crystallization.md:28`: "A book puts vision to the living's ruling; the implementation of landed vision follows without a ruling of its own." It was landed by dd87edb on 2026-10-16 11:41 as one of "three approved lines" (d68c82 log:1892, C). It was shown to the living in 39bd0c book 10 (line 178) and in d68c82 books 69 (line 266) and 84 (line 49). The living's 18:18 words name "you", meaning Psyche core Secondary: `flows/379e7a/log.md:26`. | W for the lines, C for the approval |
| Known before today's complaint | d68c82 log:2315: "approved vision not deployed. Asked Mind Core Secondary to repin". ca28a4 log:20 (17:07): "landed psyche-context vision never deployed to skills (no generator; inquiry, criomos, subflows absent)". Both are claims that this audit confirms (section 2, row S1). | C, confirmed W |

### Stateful exceptions on ouranos (all W)

| Exception | Observation |
|---|---|
| `~/.local/bin` is first on PATH | It precedes `/etc/profiles`, `/run/current-system` and `~/.nix-profile`, so every entry below shadows the declared one. |
| `~/.local/bin/flow`, `flow-hook`, `flow-meta` | Hand links made 15:23 today to `i3ni…-flow-deployment` (Flow 0.35.21). |
| `~/.local/bin/message`, `message-mcp-send`, `message-meta` | Hand links made 15:23 to `l48vzf…-message-deployment`. |
| `~/.local/bin/flow-start` | Unversioned Node script dated 15:25. It imports `/home/li/primary/tools/flow-start-adapter.mjs` and `tools/main-flow-mode/launch-config.mjs`, both tracked in Primary, and reads `config/main-flow`. |
| `~/.local/bin/herdr` | Bash shim made 15:28 by 4201a3, labelled "Temporary shim". It wraps `~/.nix-profile/bin/herdr` so that empty `report-metadata` output becomes `{}`. |
| `~/.local/bin/hm-*` (10 links) and `messenger-clj` | Links made 18:09 to `messenger-clj-0.4.0`. They come from the `activate-messenger-clj` script, which is installed in the nix profile and written in CriomOS-home `packages/messenger-clj-deployment`. |
| `~/.local/bin` leftovers | `flow-next*.bak` and `message-next-meta` (Sep 26) hard-code store paths of flow-0.17.0 and message-0.17.0. `message-write-configuration` is a 984 KB binary from Sep 17. `cloud-maintainer-chrome` is from Jun 19. |
| `~/.local/bin/xdg-open` | Declared: it links to `home-manager-files` from CriomOS-home `default-opener.nix`. CriomOS-home main also declares `.local/bin/hm-*` through `messenger-clj.nix:35`. Even the declared Home therefore uses `~/.local/bin`. |
| Imperative nix profile (`~/.nix-profile` → `.nix-profile-31-link`, Oct 18 16:48; generations 18–31 on Oct 16–18) | Entries: activate-messenger-clj, artifact-auto-open-session-vars, curriculum-resolver-deployment, flow-deployment (Flow 0.35.11), harness-home-profile (herdr, orchestrate, orchestrate-meta, flow-id), home-manager-path, message-deployment. |
| User units hand-linked into `~/.config/systemd/user` | `flow-nexus.service` → i3ni flow-deployment (15:23). `message-nexus.service` → l48vzf message-deployment. `curriculum-nexus.service.d/50-declared-runtime.conf` → rf5a9p curriculum-resolver-deployment (13:25). `default.target.wants/flow-nexus.service` and `message-nexus.service` point to Oct 16 store paths; the flow one is no longer in the store. `field-luna-heartbeat` and `opencode` are masked to /dev/null. Empty `.d` directories exist for codex-remote-control, message-daemon, spirit-daemon and spirit-judge. |
| Running services | flow-nexus runs Flow 0.35.21 (`dhw43…`) from 15:23:59. Flow main is 0.35.11 (67b80b3). message-nexus runs 0.20.0. orchestrate-nexus has run 0.37.0 since Oct 7. The herdr 0.8.2 server has run since Sep 26 in a ghostty transient scope, started by hand. |
| Flow versions reachable at once | 0.35.21 (via ~/.local/bin and the unit), 0.35.11 (via the nix profile), and flow-next 0.17.4 (via home-manager-path). This goes against raw `d68c82/vision/deployment.md:2-7`: "one source ... no version divergence". |
| Home deployment | The last Home activation was 2026-10-11 14:46 (`~/.local/state/home-manager/gcroots/current-home`, `home-manager-files g5kld6`). The system generation is 190 (16:48 today), but its closure holds no Home, flow-deployment or message-deployment. CriomOS-home main declares `systemd.user.services.flow-nexus` (`checks/flow-service-path`), and that declaration is not what runs. |
| `config/main-flow` | Tracked in Primary, except three untracked files: `metaflow/Field-Core-Secondary.edn`, `Field-Core-Tertiary.edn` and `Mind-Core-Tertiary.edn`. |
| Build result links | `result` links in curriculum-deploy, Curriculum, lojix-test and LiGoldragon/primary. These go against `vision/nix-builds.md:8` "A machine keeps links only to the profiles in use on it." |
| Disconfirming | Nix builds are offloaded: `max-jobs = 0`, builder prometheus. `CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0` is set and declared in CriomOS-home `codex-remote-control.nix:52`. The suspend fix is declarative: `disable-spurious-wakeups.service` is in the system, `/proc/acpi/wakeup` shows GLAN and XHCI disabled, and gpe6D is unmasked, so no live mask is in place. |
| In flight (uncommitted) | `/home/li/worktrees/criomos-home-379e7a-localbin` has staged changes: it deletes `checks/messenger-clj-deployment` and `checks/harness-profile`, adds `packages/flow-start`, and edits `flow.nix`, `messenger-clj.nix` and `flow-deployment`. Its effect has not been witnessed. |

## 2. Vision marked short-term, "now", or to be deployed

| # | Statement (psyche-context unless raw) | Term | Implemented? | Witness or gap |
|---|---|---|---|---|
| S1 | Every landed vision module reaches flows as a skill | implied by book-crystallization:28 | No | 6 modules are missing from every generated tree (chronos, criomos, git-server, inquiry, nix-builds, subflows). 9 differ from source (book 70 lines, ethos 158, flow 104, nexus 96, protos 10, context-modules 9, datom 9, model-roles 6, messaging 4, psyche 3). Also, 20 compensation modules differ from field-context main and `illustration` is missing. (W) |
| S2 | criomos.md:8 declarative, nobody edits a file on a host | long | No | Section 1 table. (W) |
| S3 | criomos.md:10-11 every hotfix replaced by a proper fix | long | Partly | The suspend fix is declarative (W). The herdr shim and the hand units are hotfixes in place (W). |
| S4 | criomos.md:17 Nix code never names a store path | long | No | 9 literals in CriomOS-home main outside checks: `codex-remote-control.nix:24-25`, `codex-next.nix:16-17`, `herdr.nix:53-54`, `harness-profile/default.nix:4,12`, `lib/primary-committer-hook-trust.nix:7`. 6 in CriomOS main: `modules/nixos/userHomes.nix:17-32`. (W) |
| S5 | criomos.md:21-23 hardware type with a cluster-data fix library | long | Partly | `checks/metal-suspend-policy` keys on gen5. The library and the hardware type themselves were not inspected. (W partial) |
| S6 | criomos.md:27 harnesses kept stock under ordinary names | long | Not checked | — |
| S7 | criomos.md:31-32 a new service lives in CriomOS and updates by coming up at its latest version | long | No | flow-nexus and message-nexus are hand-linked, not from CriomOS. orchestrate-nexus has not been restarted since Oct 7. (W) |
| S8 | criomos.md:36 no artifact tab opens on its own | long | Yes | The environment variable is set and declared. (W) |
| S9 | flow.md:40 "Flow deploys first and is used raw to send messages, until Message sends through Flow's socket" | short | No | Messages go through hm-send typed by Herdr (compensation messenger-clj:6). Flow is not the route. (W for the skill text, C for practice) |
| S10 | flow.md:60 "Short term, a Primary is not started without its Secondary" | short | Outside Flow | Done in Primary `tools/flow-start-adapter.mjs:236-249`, reached through the hand-placed `~/.local/bin/flow-start`. Not found in flow main source. (W) |
| S11 | flow.md:76 short term, no hash check | short | Trivially | (I) |
| S12 | 2d9fbb6 (18:15 today): one-call start, presentation, refresh by model threshold, compaction | long and short | No | 379e7a log:25 "Implementation ... follows the running integration". (C) |
| S13 | nexus.md:29 short term, a Nexus has no declared traits | short | Consistent | The deployed `compensation-design` instead forbids hand-written traits (row K8). (W) |
| S14 | nexus.md:52 default clients packaged as separate crates | short ("for now") | Yes for Flow | crates `flow` and `flow-meta`, one per socket. (W) |
| S15 | ethos.md:8 Chronos is the example built with Ethos and Nexus, short term | short | No new work | chronos origin/main last commit a5cf51f is from 2026-09-06, before chronos.md landed (b938651, 10-18). (W) |
| S16 | model-roles.md "model is declared once ... in Flow ... Nothing else holds a model name" | long | No | Model names appear in `config/main-flow/{psyche,mind,field}.edn` and `metaflow/*.edn`, and in `SKILL_VARIABLES.md` ("Psyche Secondary Claude model"). (W) |
| S17 | orchestrate.md "deployed unconditionally, in the home, for every user", with its meta binary | long | Partly | The service comes from home-manager-files. `orchestrate` and `orchestrate-meta` come from the imperative `harness-home-profile` profile entry. Users other than li were not checked. (W) |
| S18 | raw d68c82/vision/deployment.md (10-13) "harness components ... in the home environment for now" | short (raw) | No | They come through the nix profile and `~/.local/bin`, not the Home generation. (W) |
| S19 | raw d68c82 deployment.md "one source for every Flow part"; "everything installed from source"; "audit ... everything is deployed declaratively" | raw | No | Three Flow versions are live (section 1). (W) |
| S20 | raw 379e7a/vision/deployment.md "eradicate .local/bin"; raw 379e7a/vision/flow.md (18:20) "approved vision gets deployed, everybody retrained, then implemented" | raw, today | In flight | Worktree above. The skills regeneration was dispatched (379e7a log:26). (C) |

## 3. Compensation lines that contradict or work around vision (field-context origin/main)

| # | Compensation line | Vision line | Implementation that removes it | Owner (I) |
|---|---|---|---|---|
| K1 | `update.md:14` "Preserve its process, service, socket, state root ... Do not restart, recreate..." (with the whole stable/Next procedure, :6-26) | criomos.md:32 "A service is updated by bringing it up at its latest version"; criomos.md:17 (d68c82 log:2290 traces the store literals to this line, C) | Services declared in CriomOS/CriomOS-home that restart at their new version on deploy, with the `occupied*` literals removed | Field core (CriomOS deploy, d68c82 log:1393) |
| K2 | `network-temporary.md:8` "Use NetworkManager's checkpoint rollback for a remote Wi-Fi change" | criomos.md:8, :10-11 | Wi-Fi profiles declared in CriomOS from goldragon cluster data | Field core, with Mind for Horizon data |
| K3 | `operating-system.md:14` "...before a reboot or emergency runtime mutation" (it permits a runtime mutation with approval) | criomos.md:10-11 | None; a ruling is needed. `:6` restates criomos.md:8 and can be leaned out now | Psyche ruling |
| K4 | `messenger-clj.md:8` `#msg [sender machine-prose]` envelope; `:6` "Use hm-send ... never ... another intercom" | messaging.md:32-33 "There is no envelope around it"; flow.md:40 Flow used raw until Message sends through Flow's socket; flow.md:33 Flow owns delivery | Message delivering datom bodies through Flow's socket | Mind (message, flow) |
| K5 | `messenger-clj.md:8,20` `FLOW_ID=<self> hm-send`; `main-flow.md:26-31` run `flow-id ...` | flow.md:29 "No flow declares its id: every call to Flow is identified by the calling process" | Flow and Message resolve the caller from its process | Mind flow |
| K6 | `messenger-clj.md:22` no public-name sleep; report the missing contract | flow.md:27 "A metaflow sleeps ... the harness closes" | Flow sleep and wake by metaflow address | Mind flow |
| K7 | `primary-commit.md:6` "No main flow or subflow stages, commits ..." | committing.md:20-21 "A flow commits the files it edited" | Ruling needed on which stands; the order of the two records is unknown | Psyche ruling, then Field |
| K8 | Deployed `.claude/skills/compensation-design`: "hand-written code that is not ethos-generated declares no trait" (main `design.md:24` already reads "until Ethos generates traits, hand-written traits are allowed") | intent mandatory-traits:8 "Every method call ... lives under a trait"; nexus.md:25,29 | Regenerate skills now. Ethos trait generation then makes `design.md:24` removable | Mind context (generator), Mind ethos |
| K9 | `flashbook-illustration.md:6,12` "elaborate ... curved paths, gradients ... the things around it drawn in"; `:10` "a dashed grey alternative"; `illustration.md:13` "Dashed means proposed" | book.md:18 the figure "keeps every box, label and arrow, and adds nothing the source does not say"; "colour carries a role or is absent" | An Illustrator role and figure check that enforce the book.md grammar | Psyche book with Field roles |
| K10 | `book-crystallization.md:22` "a new book follows with ... the inquiry, knowledge or compensation review it needs"; `main-flow.md:58` (duplicate of book.md:82) | book.md:46 "A compensation line reaches a book only to be removed"; book.md:82 | Lean-out only; no code | Psyche book |
| K11 | `launch.md:6-10` the Primary only after a verified Secondary | flow.md:60 (short term) | Flow's start enforces it instead of the Primary-side adapter | Mind flow |
| K12 | `launch.md:24-32` refresh at threshold; `:45` first response is a presentation | 2d9fbb6 flow.md (P4, P5) | Flow implements per-model thresholds, reaping, and the startup presentation | Mind flow |
| K13 | `default-effort.md:17-18` "A Fable flow is launched or woken only on the living's word" | model-roles.md: roles by layer; "Nothing else holds a model name" | A Flow configuration gate on Primary launch by layer | Mind flow (I, tension) |
| K14 | `temporary.md:8` "what needed the missing host builds or runs locally" | nix-builds.md:8 "Nix builds live in the remote builder's store" | A second builder, or a ruling | Field (I, tension) |
| K15 | `nix-workflow.md:20` (duplicates nix-builds.md:8); `operating-system.md:6` (duplicates criomos.md:8) | — | Lean-out; vision covers them | Field |

Lines that support vision rather than contradict it: agent-harness-packaging:10,16; nix-workflow:6-12; orders:8. No compensation module exists in psyche-context or mind-context (W).

Open causes for S1 (several are possible): the Curriculum generator has no supported producer for current sources (d68c82 log, C); the Nexus pins psyche-context b938651 (d68c82 log:2315, C); no step ties a landing commit to regeneration (I); vision moved into type folders on 10-16 (53f68b6) while the generated trees date from 10-15 (W dates, I link).

## Sources
- /git/github.com/LiGoldragon/psyche-context origin/main 2d9fbb6: vision/*.md, intent/psyche.md, intent/mandatory-traits.md
- /git/github.com/LiGoldragon/field-context origin/main 785ceb0: compensation/*.md
- /git/github.com/LiGoldragon/CriomOS origin/main 8d38ffd; /git/github.com/LiGoldragon/CriomOS-home origin/main 5a52224e; flow, chronos, orchestrate, messenger-clj origin/main
- /home/li/primary/.claude/skills (and .agents, .codex, .opencode, .pi)
- /home/li/primary/flows/379e7a/{log.md,orders.md,vision/}; flows/d68c82/{log.md,vision/criomos.md,vision/deployment.md,books/82-criomos-4.md,books/84-book-dynamics-2.md}; flows/39bd0c/books/10-what-a-book-is-2.md; flows/ca28a4/log.md; flows/7c89aa/comment-relay-ledger.jsonl; flows/d68c82/receipts/comment-edition-register.md
- Host: ~/.local/bin, ~/.nix-profile, `nix profile list`, ~/.config/systemd/user, `systemctl --user show`, `ps`, /proc/acpi/wakeup, /sys/firmware/acpi/interrupts/gpe6D, `nix config show`, /home/li/worktrees/criomos-home-379e7a-localbin
- Receipt handles: none (no PROVENANCE handoff received)
