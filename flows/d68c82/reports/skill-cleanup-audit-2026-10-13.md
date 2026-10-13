# Machine-written skills: lines that read as orders, not rules

Scope: every non vision-/intent-/spirit- skill in the authored repositories, read at
field-skills origin/main `c3af84c` and mind-skills origin/main `41b814e`. psyche-skills
holds only intent-, spirit- and vision- skills, so nothing in it was in scope. Line
numbers are those revisions. "Origin" is the commit that introduced the text (`git log
-S`); text older than 2026-10-07 was traced into the Curriculum repository, where the
skills lived before the split. A flow is named only where a commit body or a flow log
names it; otherwise the flow is not recorded.

17 candidates, in 13 skills.

## field-skills

### trial-contact-discipline

    description: A primary seat or another aspect must be contacted.
    user-only: true
    dependencies: [vision-aspects]
    ---
  > L7: Tell the Psyche Primary that its user-only status makes his approval necessary. The Primaries receive prepared packages when their judgment is relevant; their time is reserved for important matters. The living chooses the recipient directly. Routing examples are guidance, never a universal only-questions rule.

1. Candidate: "Tell the Psyche Primary that its user-only status makes his approval necessary." Also unclear: "The living chooses the recipient directly."
   - Origin: Curriculum `2e68411`/`b697c10` (2026-10-02, "Add non-gold skill catch-up wave") as "Tell Fable that its user-only status makes his approval necessary". Written by Field 42265e on assignment from Fable 91ea9f. The flow log `flows/42265e/log.md:380` reads "User-only contact discipline remains manually loaded and is notified to Fable". Reworded in Curriculum `69b4955` (2026-10-03), then field-skills `35888c3` and `1607152` (2026-10-12, session 01FoueK3, this flow d68c82), which changed Fable to Psyche Primary.
   - Record: none for that sentence. The rest is supported by `flows/42265e/vision/routing-examples.md` (2026-10-03, time reserved for important things, examples are not law). `flows/b80e55/vision/userOnlyFlagPurpose.md` says user-only means models cannot load the skill, not that anyone's approval is needed.
   - Why it confuses: the implementer was told to notify Fable, and that note was copied into the skill body as a standing order. No flow can carry it out, and it invents an approval duty that user-only does not carry.

(trial-succession, which held "Carry one concentrated vision block with the verbatim psyche from the last three flows", was deleted in field-skills `c3af84c` on the living's 2026-10-13 order. It is not counted.)

## mind-skills

### operation-prompt-crafting

    L6 The crafted prompt is printed once, in the response, for the caller to paste.
    L7 List the related beads with the repository each belongs to.
  > L8 A prompt carries its content, never references to read: the concentrated vision of the last three flows with the verbatim psyche that supports it, in one block, with no full-length hashes.
    L9 A prompt explains nothing the harness does automatically and nothing everybody knows; ...

2. Candidate: L8, "the concentrated vision of the last three flows".
   - Origin: Curriculum `8dbd981` (2026-10-02, "Apply approved gold skill catch-up"), item 6 of «Skill catch-up wave» (`flows/91ea9f/books/skill-catch-up-wave/source.md:52`), which the living approved (`flows/41fa34/vision/skill-catch-up-wave-approved.md`).
   - Record: the book quotes 183ae0, typed 2026-09-29 (fat first prompt, never files to read); not re-read here. `flows/fe945a/vision/concentratedVision.md` ("go back a few flows, like three, in the line of fables").
   - Why it confuses: the living rejected the same sentence in trial-succession on 2026-10-13 (`flows/d68c82/log.md`). The record says "a few, like three" and names Fable lineages; the rule turns that into a fixed count for every prompt. The approval and the rejection conflict, so this needs his ruling.

### knowledge-codex-harness

    L15 A Codex session's model and reasoning effort come from
    L16 `~/.codex/config.toml` at launch and change without notice. A
    L17 launcher that must pin a model passes `-m <model> -c
    L18 model_reasoning_effort=<effort>` rather than inheriting them.
  > L20 A launcher passes the role's model by family name, never a version number, and `model_reasoning_effort=medium` unless the role declares otherwise.

3. Candidate: L20.
   - Origin: Curriculum `8dbd981` (2026-10-02), item 13 of the same book, approved by the living.
   - Record: the book quotes Codex 031b5c, typed 2026-09-29, not re-read here ("no part of the code that hardcodes model numbers… medium is the default").
   - Why it confuses: it conflicts with vision-model-roles "One declaration sets the model everywhere": the model is declared once in Flow and nothing else holds a model name. It also conflicts with `SKILL_VARIABLES.md`, which holds exact versioned ids (`claude-opus-5-5`). It is an order to launchers sitting in a knowledge skill. Approved text that is now in tension.

### knowledge-claude-harness

    L54 A subflow receives no startup prompt of its own. It cannot see or load a
    L55 withheld skill; what it must carry belongs in its brief.
  > L57 A request to update spawned models does not authorize changing the main-flow model.
    L59 The machine reads its system prompt; the living cannot, through ...

4. Candidate: L57.
   - Origin: Curriculum `0c1cd54` (2026-09-29, "Clarify spawned model scope"), flow bea031 (`flows/bea031/log.md:489`, `:513`).
   - Record: there is no vision record. The living's words are at `flows/bea031/log.md:485` ("We're not changing the main model ... This is just going to change the model that the sub-agent spawns"), which clarified the scope of one task.
   - Why it confuses: a one-task scope correction became a permanent authority rule inside a knowledge skill about harness mechanics.

    L43 On 2026-10-09, `claude --version` returned `2.1.294 (Claude Code)`.
    L44 This is an observation of the installed command, not a seat binding:
  > L45 Herdr exposes a seat identity rather than its executable. The retained
  > L46 Field deployment receipt and Quaternary native witness are recorded in
  > L47 `flows/ebbe30/log.md`; they do not establish another seat's version.

5. Candidate: L45–47.
   - Origin: mind-skills `f894096` (2026-10-09, "Record harness loading observations"). The flow is not recorded.
   - Record: none.
   - Why it confuses: it is evidence bookkeeping for one flow, pointing at a "retained receipt" and witness in one flow's log, with no behavior a flow can follow.

### knowledge-codex

    L1 description: Read the version-pinned Codex app-server control surface without turning protocol shapes into runtime claims.
  > L5 Record the installed Codex version with a source-verification receipt before relying on its protocol.
  > L6 The model-facing account names the source artifact, states match or mismatch, and gives the receipt handle; deterministic code retains the raw revision.
  > L7 Until source-verification receipt evidence exists, report that unavailable evidence rather than copying a raw revision into model context.
    L9 Initialize the app-server connection before requests.

6. Candidate: L5–7.
   - Origin: Curriculum `2bb8602`/`dfd6073` (2026-10-03, "Curriculum: keep raw verification outside model context"). The flow is not recorded.
   - Record: none. No receipt or receipt-handle mechanism exists in any repository under `/git/github.com/LiGoldragon` or in Primary's tools. The only "PROVENANCE" hit is an unrelated test fixture note.
   - Why it confuses: it orders flows to use a "source-verification receipt" that does not exist, and in its absence to report missing evidence instead of reading a version. This is a standing refusal built on an invented mechanism.

    L35 Start an allowance collector from a read snapshot, merge sparse updates, ...
  > L37 Keep Flow identity allocation out of this knowledge. Current allocation choices and UUIDv7 collision behavior remain design questions for the living.

7. Candidate: L37.
   - Origin: Curriculum `0701f09`/`363a8a` (2026-10-03, "knowledge-codex: add pinned app-server boundaries"). The flow is not recorded.
   - Record: none.
   - Why it confuses: it is an editing note about the file itself, plus an open question. A reader has no behavior to take from it.

### operation-flow-evidence

    L6 Write the artifact under the supplied `FLOW_DIRECTORY`.
  > L7 Use `reports/<subject>.md` for a carried account and end it with `## Sources` as it is made, naming readable artifacts and receipt handles.
    L8 Use `witnesses/<subject>.md` for an observation and state its method.
  > L9 Deterministic code retains and compares raw checksums; a PROVENANCE handoff names the artifact and says match or mismatch rather than carrying them.
    L10 Write no log or index entry.

8. Candidate: "receipt handles" in L7, and L9.
   - Origin: Curriculum `861951b`/`506cd5a` (2026-10-03, "curriculum: move subflow context into agent roles") and `477944d` (2026-10-03, "Curriculum: scope provenance receipts"). The flow is not recorded.
   - Record: none. There is no PROVENANCE handoff or receipt-handle mechanism, as for 6.
   - Why it confuses: it belongs to the same invented receipt system. The generated subflow agent definitions in Primary `.claude/agents/` (read-*, write-*, tester, book-page) carry the same text in their instruction layer.

### knowledge-nexus

  > L6 The retained Home 83 runtime packet records Home Manager generation 1045 as active. Generation 1039 remains an executable rollback.
  > L8 Field's retained Home 83 result reports the running server engines as Orchestrate Nexus 0.37, Flow Nexus 0.23, Message Nexus 0.19, and Lojix Nexus 8.1. ...
  > L15 ... Until the retained reader receipt is available, treat that closure correspondence as attributed Field evidence. This packet does not establish store-engine versions, a wire contract, active seats, or a successful launch. ...

9. Candidate: the whole body, L6–15.
   - Origin: Curriculum `544a64f` and `3015843`/`f5ca955` (2026-10-03, "record Home 83 Nexus state", "attribute Home 83 runtime evidence"). The flow is not recorded.
   - Record: none.
   - Why it confuses: it is a frozen 2026-10-03 snapshot written as a negotiation over evidence ("retained reader receipt", "attributed Field evidence"). It cannot be understood without its backstory, and the versions and socket paths it gives are stale against what is deployed now.

### knowledge-flow

  > L6 The Flow source repository at commit `ac6ab64193f3c4a43009db5a343284977bd33ea7` declares version `0.24.0` ...
  > L12 A read-only observation recorded in `/home/li/primary/flows/6aa08d/log.md` on 2026-10-07 reports ...
  > L52 ... The retained 2026-10-07 launch report at `/home/li/private-repos/flow-evidence/0c85a3/launch-witnesses.md` records ... The Codex launcher checksum was `03004fcc…`. ... These profile-specific native-launch witnesses do not validate a FlowStart request or hook, qualify a Mind.Primary launch, replacement, or retirement, or establish a deployed Flow 0.24 route.
    L64 Before launching, naming, claiming, reaching, or reporting a Flow, read the matching deployed source and obtain the target's explicit response ...

10. Candidate: L6–62. Only L64–68 states a behavior.
   - Origin: mind-skills `a36f0ca` (2026-10-09, "Qualify current Flow source and retained native launch procedure"). `flows/f5a6e9/log.md:94` attributes it to Astra ("the Today facts landed in mind-skills knowledge-flow (a36f0c)").
   - Record: none.
   - Why it confuses: it is an evidence ledger of single observations (full hashes, a checksum, flow-log paths), mostly saying what the evidence does not prove. It hard-codes `/home/li` and `/run/user/1001` paths that should be skill variables.

### operation-lojix

    L6 `lojix-nexus` owns durable state and two authority-tiered sockets. ...
  > L8 Use `operation-lojix` on the ordinary socket for `Query`, `WatchDeployments`, `WatchCacheRetention`, and `Unwatch`.
    L10 Use `lojix-meta` on the owner socket for `Deploy`, `Pin`, `Unpin`, `Retire`, and `Test`. ...
  > L91 The current `operation-lojix` executable exchanges one request for one reply and exits. ...
  > L383 The supported deployment and observation interface is `operation-lojix` and `lojix-meta`; ...

11. Candidate: L8, L91, L383.
   - Origin: Curriculum `742e100`/`73414b` (2026-10-07, "Replace Curriculum skills with typed Nexus"). The earlier text read `lojix` (Curriculum `bb700c5`, 2026-08-22). `flows/0c85a3/log.md:46` records the publication of `73414b`.
   - Record: none needed. This is a mechanical rename.
   - Why it confuses: renaming skill `lojix` to `operation-lojix` also renamed the executable. The skill's own examples call `lojix '...'`, so a flow is told to run a command that does not exist.

### operation-operating-system

    L8 Before debugging installed software, update it to its latest release.
  > L10 Use `operation-lojix` and `meta-lojix` for deployment and observation; their exact typed contract and terminal verification are defined by the `operation-lojix` instructions.
    L12 Use existing deployment authorization once concrete artifact and execution prerequisites are satisfied; ...

12. Candidate: L10.
   - Origin: Curriculum `742e100` (2026-10-07). It replaced "Use `lojix` and `meta-lojix`" (Curriculum `e560bd9`, 2026-08-14).
   - Record: none needed.
   - Why it confuses: it carries the same executable rename as 11, and `meta-lojix` contradicts operation-lojix, which names the owner client `lojix-meta`.

### operation-orchestrate

  > L6 Use `operation-orchestrate` for ordinary requests. The client takes exactly one inline Datom value and no flags. ...
    L8 Acquire a Lock. Its four positional fields are ...

13. Candidate: L6.
   - Origin: Curriculum `742e100` (2026-10-07). It replaced "Use `orchestrate` for ordinary requests" (Curriculum `abd9279`, 2026-08-26).
   - Record: none needed.
   - Why it confuses: same rename as 11. The skill points at itself as the client, while every example runs `orchestrate`.

    L12 ... Put the actual owning `FLOW_ID` only in `FlowId`, never concatenated into `LockName` merely for uniqueness or title display.
  > L12 (end) A name such as `FlowIdDocumentation` remains valid when flow ID is the subject of the work.

14. Candidate: the last sentence of L12.
   - Origin: Curriculum `41f8366` (2026-09-04, "Clarify Orchestrate Lock field ownership"), flow 444e5e (`flows/444e5e/log.md:2`).
   - Record: none.
   - Why it confuses: it settles one past lock name from the 444e5e task and has no general use.

### operation-stale-lock

    L6 ... In Primary, leave those bytes in place and send the exact holder and path evidence to the sole standing committer for publication; do not commit them yourself.
  > A lifetime PrimaryPublish handover is coordinated with the standing committer's owner; never start a second publisher or infer a handover from stale transport.
    A live holder is messaged, never unlocked. The living: "break the locks. Nobody in particular owns Flow Source."

15. Candidate: the "standing committer's owner" sentence. The rest of the paragraph is the text the living approved in Curriculum `dd14ce7` (2026-09-25).
   - Origin: mind-skills `aa9e6dc` (2026-10-12, "Route Primary publication through its sole standing committer"; body: "Core d68c82, living order relayed 2026-10-12").
   - Record: `flows/d68c82/vision/committing.md` covers one committer for Primary only. Nothing defines an "owner" of the committer or a "lifetime handover".
   - Why it confuses: it invents a role (the committer's owner) and an event (a lifetime handover) that no record or other skill names.

### operation-psyche-grasp

  > L6 Term "psyche-grasp" is provisional — TO BE REVIEWED by the psyche.
  > L7 Psyche-grasp measures the psyche's understanding OF the code. Code-seniority measures alignment WITH the psyche; these are distinct.
    L9 Levels, lowest to highest: `unseen`, `glimpsed`, `slightly-reviewed`, `understood`, `authored`.

16. Candidate: L6–7.
   - Origin: Curriculum `0be9e9e` (2026-08-08, "skills: port awareness, psyche-grasp, ..."), a Claude Opus 4.6 session from before flow ids.
   - Record: none for either term.
   - Why it confuses: a pending-review note has stood for two months. "Code-seniority" is defined nowhere.

### operation-book

    L20 Use the book subflow defined by subagents/book.md to publish the exact
    L21 source. Check it with tools/book-check.mjs before rendering. A non-Claude
  > L22 caller sends its source to the currently qualified book-making seat; it
    L23 does not hand-render a replacement page. ...

17. Candidate: "the currently qualified book-making seat".
   - Origin: mind-skills `b605cd0` (2026-10-09, "Align book preflight and presentation with living records"), Field 42265e (`flows/42265e/reports/book-workflow-audit-2026-10-09.md:9`, `:18`).
   - Record: none for a qualified book-making seat. compensation-launch says a topic Secondary publishes its Primary's books.
   - Why it confuses: it names a status ("currently qualified") that nothing defines and nobody can look up, so a Codex caller cannot tell where to send a book.

## Checked and clean

field-skills: compensation-behavior, compensation-book-distillation,
compensation-breaking-upgrades, compensation-correction, compensation-default-effort,
compensation-design, compensation-launch, compensation-messenger-clj, compensation-nix,
compensation-nix-rationale, compensation-orders, compensation-primary-commit,
compensation-prose, compensation-subflow, compensation-temporary, compensation-testing,
compensation-truth, compensation-understanding, compensation-update,
compensation-versioning, trial-generated-projection, trial-independent-review,
trial-low-power, trial-presentation-book, trial-psyche-injection, trial-questions-book,
trial-reaping, trial-unblocking-commands.

mind-skills: knowledge-context-strata, knowledge-datom, knowledge-ethos,
knowledge-protos, knowledge-psyche, knowledge-vocabulary, knowledge-yt-dlp,
operation-agent-harness-packaging, operation-beads, operation-clojure-development,
operation-design, operation-disk-hygiene, operation-documentation-placement,
operation-edit-coordination, operation-feature-development, operation-file-editing,
operation-flashbook, operation-flashbook-illustration, operation-main-flow,
operation-nix-input-upgrade, operation-nix-workflow, operation-psyche-acquisition,
operation-psyche-distillation, operation-psyche-interraction, operation-realization,
operation-relaying-the-living, operation-repository-lifecycle, operation-secrets,
operation-skill-designing, operation-testing, operation-transcript-search.

psyche-skills: no machine-written skill.

## Sources

- `/git/github.com/LiGoldragon/field-skills` origin/main `c3af84c`; `/git/github.com/LiGoldragon/mind-skills` origin/main `41b814e`; `/git/github.com/LiGoldragon/psyche-skills` main `29119ab`. The local field and mind checkouts are detached behind origin; the mind checkout has diverged and has uncommitted edits.
- `/git/github.com/LiGoldragon/Curriculum` history, for text older than 2026-10-07.
- Flow logs and records: `flows/42265e/log.md`, `flows/42265e/vision/routing-examples.md`, `flows/b80e55/vision/userOnlyFlagPurpose.md`, `flows/91ea9f/books/skill-catch-up-wave/source.md`, `flows/41fa34/vision/skill-catch-up-wave-approved.md`, `flows/fe945a/vision/concentratedVision.md`, `flows/bea031/log.md`, `flows/0c85a3/log.md`, `flows/444e5e/log.md`, `flows/f5a6e9/log.md`, `flows/d68c82/log.md`, `flows/d68c82/vision/committing.md`, `flows/42265e/reports/book-workflow-audit-2026-10-09.md`.
- psyche-skills `vision-model-roles.md`, `vision-committing.md`, `vision-aspects.md`; `/home/li/primary/SKILL_VARIABLES.md`.
