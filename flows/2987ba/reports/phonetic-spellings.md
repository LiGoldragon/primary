# Phonetic spellings in the user's code

Scope: tracked files and tracked file names under /git/github.com/LiGoldragon/* (one checkout per remote; the `-clean-*`, `flow-*` and branch checkouts were compared afterwards), plus the user's own repos under /git/github.com/Criome, MotherSpirit, PhoenixKriom and sajban, and the 510 checkouts in /git/worktrees. Skipped: forks and third-party code (nixpkgs, kameo, whisrs, wispr-flow-linux, pi-*), the prose book repos, lock files, hashes, target/, result/.

Method: every identifier and file-name token was split at camelCase, snake_case and kebab boundaries; words found in an English dictionary (scowl, web2) were dropped; about 8,000 remaining tokens, plus the words that only exist in the rare part of the dictionary, were read and judged by hand; each candidate was then grepped over every checkout. Zoekt was not needed.

Result: **6 confirmed phonetic words in 6 repositories.** They are few because most of the old phonetic names were already removed; the survivors are in the places below.

## Confirmed

### horizon-rs (checkouts: horizon-rs, horizon-rs-gitserver on branch gitserver, worktrees horizon-rs-codec-7a0079 and horizon-rs-capability-9228ed)

| Phonetic | Canonical | Where (file:line) | Stored or wire data |
|---|---|---|---|
| Ondyfaind | Undefined | horizon-rs: lib/ethos/horizon.ethos:1 (one-line schema, `MotherBoard.[Ondyfaind]`), lib/src/generated/d3.rs:303, 304, 313, lib/src/species.rs:131, lib/tests/datomic_machine.rs:17. horizon-rs-gitserver: lib/ethos/horizon.ethos:67, lib/src/generated/horizon.rs:150, lib/src/projection/names.rs:102, lib/tests/archive_roundtrip.rs:9, lib/tests/contract.rs:18. horizon-rs-codec-7a0079: lib/ethos/horizon.ethos:49, lib/src/generated/horizon.rs:150, lib/src/projection/names.rs:102, lib/tests/archive_roundtrip.rs:9, lib/tests/contract.rs:18. horizon-rs-capability-9228ed: the same lines as gitserver (ethos:67, horizon.rs:150, names.rs:102, tests 9 and 18). | **Yes.** An ethos enum variant of `MotherBoard`; the Rust enum derives Serialize/Deserialize and rkyv Archive and the datom codec, so it is a datom bare symbol and an archived discriminant name; `names.rs:102` also returns the string "Ondyfaind" as the projected name. Changing it changes stored bytes, text and the projection output. No datom data file in /git holds a `MotherBoard` value. |

### kibord

| Phonetic | Canonical | Where (file:line) | Stored or wire data |
|---|---|---|---|
| Kibord / kibord | Keyboard | the repository itself (`github:LiGoldragon/kibord`, /git/github.com/LiGoldragon/kibord); README.md:1 (`# Kibord`), flake.nix:2 (`description = "kibord"`), flake.nix:162, 168, 169, 271, 279 (a flake input and the attribute `kibord = {`) | **Name data.** The repository name is stored in primary (see the primary table). Inside the repo it is a description string and a Nix attribute name. Not a serialized type. |
| Indeks (in `submodulesIndeks`) | Index | flake.nix:97, 113 | No. A Nix attribute holding submodule paths. |

### Criome/hob (github.com/Criome/hob)

| Phonetic | Canonical | Where (file:line) | Stored or wire data |
|---|---|---|---|
| Indeks (in the file name `forkIndeks.nix`) | Index (`forkIndex.nix`) | forkIndeks.nix (the tracked file name) | The file name is tracked, so a rename is a path change. Nothing in the repo imports it. |
| Fleik (in `getFleik`) | Flake | forkIndeks.nix:1, 5, 17, 28 | No. A function argument and call name. |

### CriomOS

| Phonetic | Canonical | Where (file:line) | Stored or wire data |
|---|---|---|---|
| Akses (in `rootUserAkses`) | Access | modules/nixos/users.nix:61, 72. The same two lines are in the CriomOS-flow-d76b4c-* checkouts and in about ten /git/worktrees checkouts of CriomOS. primary/agent-outputs/PersistentSpiritMirror/OperatingSystemImplementer-GuestLoginSubstrate.md:86 quotes it. | No. A Nix `let` binding. |

### sajban/seahawk (github.com/sajban/seahawk)

| Phonetic | Canonical | Where (file:line) | Stored or wire data |
|---|---|---|---|
| Neksys (in `NeksysProposal`) | Nexus (`NexusProposal`; the sibling Criome/aedifico/flake.nix:5 exports `NodeProposal` in the same shape) | flake.nix:5 | **Yes, as a name.** A flake output attribute, which other flakes read by name. No consumer is in /git. |

### primary (the repository name `kibord`, quoted)

| Phonetic | Canonical | Where (file:line) | Stored or wire data |
|---|---|---|---|
| kibord | keyboard | 155 lines in total. Data: protocols/repos-manifest.dotos:198 (`(Repo kibord github:LiGoldragon/kibord ...)`), protocols/component-evidence.generated.json:2831, 2832, 2838, 4235. Prose: reports/persona-system-audit/10-landscape-chronology.md:37, 216; reports/legacy-disposition/PROPOSAL-2026-07-01-repos-manifest-and-active-set.md:121, 129; reports/ProtosEstateAudit-2026-08-13.md:141; about 140 lines in agent-outputs/MiniDox* reports. primary-next holds the same 155, primary-lean-a8ab9c 19. | **Yes.** The manifest row and the generated JSON store the repository name, so renaming the repo changes both. |

## Uncertain (not counted)

| Word | Reading | Where | Why uncertain |
|---|---|---|---|
| Criad (`preCriad`, `preCriadJson`) | Created | CriomOS-lib/lib/default.nix:29 (`preCriad = "/etc/nix/preCriad"`), :41 (`preCriadJson`); CriomOS/modules/nixos/network/yggdrasil.nix:12, 49, 51, 52, 76 | The yggdrasil file holds the key pair generated before the combined config, so "pre-created" fits. It could also be a coined term built on Criome. Stored on disk as `/etc/nix/preCriad` and `<state>/preCriad.json`. |
| iuniks (`iuniksDir`) | unknown; possibly Unix, spelled `uniks` in the old project name | kibord/flake.nix:168, 170, 193, 272, 280 | `uniks` is the old phonetic Unix, and also the name of an old project (maisiliym/uniks). The leading `i` is not explained. |
| kriom / Kriom | Criome | CriomOS/docs/GUIDELINES.md:246; goldragon/AGENTS.md:10; CriomOS/reports/0005-architecture-deep-audit.md:57; sajban/seahawk/flake.nix:2 (`SubKriom`) | Criome is a coined name, and the user may spell its variants on purpose. Used as a common noun for the cluster. |
| Maisiliym / maisiliym | likely a pseudonym, "my silium" or similar | Criome/hob/forkIndeks.nix:4, 16, 27; Criome/criosphere/flake.nix:3; Criome/website/noesis.md:3, 29; CriomOS-test-cluster/checks/source-constraints.nix:22 | A proper name of the user's old cluster and group; no canonical English word is known. |
| maikro | Micro | CriomOS/reports/0005-architecture-deep-audit.md:29, 173, 175, 280 | A user account name in a report, so a proper name. |
| noul | Null / Nool / Bool | judge/src/lib.rs:922, 937, 941, 942, 1027, 1028; judge/src/bin/openrouter-decisions.rs:80, 235, 238, 277, 294, 317, 443, 470; judge/tests/openrouter_decisions.rs:26, 91, 128, 134; judge/tests/openrouter_decisions_cli.rs:35, 69 | The code mirrors the question type of TypeSafe's Jev API (primary/flows/93ba9f/reports/jev-and-openrouter.md:56 calls it "a yes/no proposition"). The tag `"noul"` is serialized on the wire; whether it is the provider's spelling is not known. |
| coleremak | Colemak | kibord/flake.nix:280; the tracked directory kibord/ergodone/coleremak/ (config.h, keymap.c, rules.mk, `#keymap.c#`) | A keyboard-layout name; looks like a variant of Colemak on purpose. |
| Lojix | Logics | all of lojix and its signals | Named by the user as a coined project name; listed only because the spelling is phonetic. |
| kodex | Codex | primary/reports/SkillTemplateEngine/Design.md:73, 79, 404, 406 | An agent's example of an unknown skill target, not the user's spelling. |

## Not phonetic: the nota-to-dotos rename mangled English words

A blind rename of `nota` to `dotos` hit English words that contain "nota". These are damage, not phonetic spelling. The first one is a real bug.

| Mangled | Canonical | Where (file:line) | Stored or wire data |
|---|---|---|---|
| andotostions | annotations | mind/scripts/live-knowledge-judge-eval.py:10 (`from __future__ import andotostions`, which Python rejects); version-projection/ARCHITECTURE.md:181 | No. |
| Dotostion | Notation | spirit/src/production_migration/v13.rs:196 (a variant of `archived_unit_enum!(Language ...)`) | **Yes.** A variant of an archived enum in the v13 production migration. |
| dotostion | notation | mentci/schema/nexus.schema:253 (comment); spirit/tests/fixtures/spirit_judge_live_eval.dotos:4 (`seed dotostion-brackets`) | The fixture seed name only. |

## Legacy phonetic names that exist only as quotations of the Zeus machine (not tracked in /git)

These are quoted in a report about repositories on the machine Zeus. They show which phonetic words the old code held; none is a file in /git.

| Phonetic | Canonical | Where quoted (file:line) |
|---|---|---|
| nvimPloginz, vimPloginz, pkgsNvimPloginz | nvimPlugins, vimPlugins, pkgsNvimPlugins | secondary/flows/57a7aa/reports/zeusRepoReview.md:65, 72, 73 |
| bildNvimPlogin | buildNvimPlugin | same report:74 |
| kynvyrt | convert | same report:73 |
| kreitOvyraidz | createOverrides | same report:73 |
| meikImaksPackage | makeEmacsPackage | same report:159 |
| neksys (a branch) | nexus | same report:162 |
| skiim, skiimInit | scheme (likely) | same report:163, 197 |
| uniks, uniks-rs, unikspod | unix | same report:197, 198; secondary/flows/57a7aa/reports/zeusDiskInventory.md:240 |
| mkSkrip, skrips | mkScript, scripts | same report:198, 199, 252; zeusDiskInventory.md:240; secondary/flows/57a7aa/log.md:129; CriomOS/reports/0005-architecture-deep-audit.md:253, 254, 255, 259 (`world.skrips.root`, flake input `criome/skrips`) |
| kor (`nix/kor`) | core | same report:75 |
| mein (branch `nix-mein`) | main | same report:164, 207 |
| mkKriomDatom | mkCriomeDatom | same report:174 |

## Ordinary misspellings seen on the way (not phonetic, not counted)

| Misspelled | Correct | Count and first locations |
|---|---|---|
| interraction | interaction | 80: Curriculum/review/README.md:16, Curriculum/review/unapproved/main-flow.md:19, 27 (also in core, primary, secondary, tertiary, quaternary) |
| overiddenEmacsPackages | overriddenEmacsPackages | CriomOS-emacs/packages/mkEmacs/default.nix:173, 212 |
| mentionning, tranformation, pysche, upgrate, concistency, rougly, deamon | mentioning, transformation, psyche, upgrade, consistency, roughly, daemon | each once or twice, in primary/design/ProtosEngine/*.md and protos-engine/design/ProtosEngine/*.md, for example primary/design/ProtosEngine/importResolutionWorldMap-2026-08-21.md:54, 89 |
| abandonned, completly, developped, repition | abandoned, completely, developed, repetition | primary/vision-raw/skillsRepository.md:11; protos-engine/design/ProtosEngine/ProtosEngineDesign-2026-07-26.md:58; primary/design/ProtosEngine/deepCenterVision-2026-08-05.md:135; primary/design/ProtosEngine/ethosNonRepetitionLaw-2026-08-01.md:10 |
| opiniated | opinionated | codex-hijack/stock-context/MARKS.md:48 |
