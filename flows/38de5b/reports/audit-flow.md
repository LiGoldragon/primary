# Audit: Flow vs vision — 38de5b subflow, 2026-09-25

## Sources (newest weighted most)

- **Raw vision, e51411.** From `flows/e51411/vision/`:
  - `launch.md`, from 2026-09-24 and 2026-09-25, last commit 2026-09-25 13:31.
  - `nexus.md`, from 2026-09-25.
  - `flowAspect.md`, 2026-09-25, speech-to-text.
  - `stack.md`, 2026-09-25, speech-to-text.
- **Notion.** `flows/e51411/notion/v2.md`, 2026-09-25. It binds nothing.
- **Distilled vision.**
  - `Vision/flowNexus.md`, last commit 2026-09-20.
  - `Vision/nexus.md`, 2026-09-11.
- **Older raw records.**
  - `flows/fd0f97/vision/launch.md`, typed, committed 2026-09-17.
  - `flows/05c604/vision/launch.md` and `nexus.md`, typed, 2026-09-15.
  - `flows/d8df70/vision/launch.md`, a merged copy of the e51411 record.
  - `flows/e1953c/vision/nexus.md` and `flows/6cc91b/vision/nexus.md`, 2026-09-13 and 2026-09-14.
- **38de5b reports.**
  - `flows/38de5b/reports/specialties-distillation.md`. This is a proposal the living has not ruled on.
  - `flows/38de5b/reports/vocabulary-acquisition.md`. It includes the d8df70 flowLifecycle quote.
- **Ethos.** `signal-flow/ethos/signal.ethos` at ab70332, the revision Flow 0.7.0 pins, compared with origin/main 968ae3b.
- **flow-clj contract.**
  - `flows/f5a74e/reports/clojure-flow-input.md`, a 2026-09-25 proposal.
  - `flows/38de5b/receipts/flow-clj.md`.
  - `flows/504461/log.md`.

## Witnessed state

- **Release on main.** In the flow repo, main is 812053c "Release Flow 0.7.0". Workspace `Cargo.toml` says version 0.7.0.
- **Contract pins.** `Cargo.toml:17-18` pins signal-flow ab70332 and meta-signal-flow a34bc65. `git branch -r --contains` finds each revision only on `origin/flow/system-prompt-bundle-00f95a`. signal-flow origin/main is 968ae3b, version 1.1.0, and its Signal holds only Start, Restart and ResolveRecipient.
- **Signal at the pin.** Line 3 of `ethos/signal.ethos` at ab70332 lists Start, Restart, ResolveRecipient, Send, Stop and List. LaunchProfile has 13 positions: request ID, sources, skills, aspect, power, harness, model, effort, `Option<FlowId>` predecessor, remembered flows, Herdr session, system-prompt bundle file and instruction prompt. There is no specialty and no title.
- **Live service.** A run of `systemctl --user status flow-nexus` shows `/nix/store/99rqvjxx…-flow-0.6.0/bin/flow-nexus`, active since 13:52.
- **Live registry.** A run of `flow 'List.{}'` returned one row, 5f38bc Codex Active. None of the other running flows is in Flow's registry.
- **Start path.**
  - Start is one complex call (`crates/flow-nexus/src/lib.rs:120-383`).
  - The Flow ID is claimed in code through the `flow-id` helper (`herdr/launch.rs:336-376`, `:932-1006`). This matches the e51411 vision.
  - Restart always returns ResumeRefused (`lib.rs:384-399`).
- **Launch arguments.** `herdr/launch.rs:839-930` builds them:
  - Codex gets `--remote unix://…`.
  - Claude gets `--dangerously-skip-permissions --system-prompt-file <bundle> --model --effort`.
  - Both get a positional startup block of `$skill` lines plus `read <bundle>`.
  - The composed first prompt is then sent separately. For Claude it goes through `herdr agent prompt` (`:1104-1123`). For Codex it goes through app-server `turn/start` (`codex.rs:732ff`).
  - I read this from source and did not run it.
- **Composed prompt.** `composition.rs:262-295` builds it. It includes "Launch request: <id>", every source file's full text, and the footer `FLOW_LAUNCH_RECEIPT_V1 launch_request_id=… prompt_body_sha256=…`.
- **Herdr names.** The agent and workspace label is `claude-<24 hex>` or `codex-<24 hex>` (`launch.rs:196-212`). No native title is set anywhere in the crates. Titles are set only by `tools/native-seat-launch.mjs:463-498`.
- **Client.** The `flow` CLI takes exactly one inline Query datom and sends rkyv (`crates/flow/src/main.rs:27-62`). This matches 05c604: "The CLI translates datom into signal".
- **Nexus process.**
  - `main.rs` panics without `FLOW_SOURCE_ROOT` and 15 `FLOW_CODEX_*` variables.
  - `/home/li/.local/state/flow` and `/run/user/1001/flow` are hard-coded.
  - The repo's `deployment/flow-nexus.service` has no Environment lines. The live unit is hand-written with them.
- **Serving.** Serving is serial (`lib.rs:697-708`). The ordinary thread ends in `.unwrap()` (`main.rs:80-82`).
- **flow-clj.** There is no checkout anywhere on disk. `gh repo view LiGoldragon/flow-clj` returns "Could not resolve". 504461 says it has no branch, and that flow-clj is third in its queue, after 0.7 activation and two test flows.
- **Stale grounding.** `/home/li/primary/flow` is a nested clone at 42b98ba from 2026-09-17. The f5a74e contract's claim that signal-flow has "only Start and Restart" is true of that clone and of signal-flow main. It is false of the revision Flow 0.7 pins.

## Gaps (one Opus task each)

### G1. Flow 0.7.0 is not live, and Flow is not the launcher

- **Vision.** fd0f97: "Is this the flow component launching a flow? If not, it should be." Also: "Once you get the Flow component working properly with an easy, cheap test model like Haiku or Sonnet, then relaunch yourself properly in a new Flow".
- **Current.** The live service runs 0.6.0. The registry has one row. Flows are launched by `tools/native-seat-launch.mjs`.
- **Change.** Activate 0.7.0 through the declarative consumer. Then do one Start with a cheap model.
- **Owner.** 504461 owns this. Dispatch it only to 504461 or with its release.
- **Files.** The CriomOS-home Flow consumer pin and module.
- **Acceptance.**
  - ExecStart points to a `flow-0.7.0` path.
  - `flow 'List.{}'` answers from 0.7.0.
  - One Haiku or Sonnet Start returns Started, and List shows it Active.

### G2. One prompt at start

- **Vision.** e51411, 2026-09-24: "There should be only one prompt when we start a fresh flow, not two". Also: "All that matters is that everything comes in as one block." 05c604: "Everything should be in one prompt."
- **Current.** A positional startup block goes out at agent start (`launch.rs:906-927`), and then a separate first prompt follows (`:1104-1123`, and `codex.rs:732ff`). The Claude startup lines use the Codex `$skill` syntax.
- **Change.** Send one first prompt per harness. It carries the skill invocations in native syntax (Claude `/name`, Codex `$name`), then the goal. There is no second write.
- **Files.** `crates/flow-nexus/src/herdr/launch.rs`, `codex.rs` and `composition.rs`, plus the fixtures.
- **Acceptance.**
  - The fixtures assert exactly one prompt-bearing call per harness.
  - A native transcript of a Haiku Start shows one user turn before the receipt.

### G3. Lean prompt, no hashes

- **Vision.** 2026-09-24, to 9ddcbc: "Let's not give them too much prompt. Let's make sure there are no hashes, garbage, and stuff like that in there."
- **Current.** The body carries the launch request ID, full source texts and a sha256 receipt footer (`composition.rs:262-295`).
- **Change.**
  - Keep hashes in the store and the observer only.
  - Detect the receipt by native turn identity, or by a short marker that is not a hash.
  - Reference sources by path, or leave them to the system prompt, instead of inlining them.
- **Files.** `composition.rs` and `herdr/launch.rs:1126ff` (`observe_native_target_receipt`).
- **Acceptance.** The composed prompt contains no hex run of 16 or more characters and no request ID, and the Start fixtures still reach Started.

### G4. Native title and session name

- **Vision.** `Vision/flowNexus.md`: "A session is named after its direct ancestor". fd0f97: "It's not very obvious what you're called from the terminal, which is a problem." The notion v2, which binds nothing, has "Psyche V2 Fable, and then the flow ID".
- **Current.**
  - The Herdr label is a hash (`launch.rs:196-212`).
  - Flow sets no native title.
  - The predecessor field exists (`LaunchProfile Option<FlowId>`) but nothing uses it for naming.
- **Change.** After the claim, Start sets and reads back the canonical native title, and the Herdr label matches it. First resolve the naming tension listed under Unknowns.
- **Files.** `herdr/launch.rs` and `codex.rs`, possibly a `NativeTitle` in `signal.ethos`.
- **Acceptance.**
  - Native title readback equals the expected string for both harnesses.
  - `herdr agent list` shows the same name.

### G5. Claude launches are remotely controllable

- **Vision.** fd0f97: "we should always make it remotely controllable"; "You don't seem to be remotely accessible. That's a big problem, a huge bug in production."
- **Current.** Codex gets `--remote`. Claude's arguments (`launch.rs:887-891`) include no Remote Control enablement.
- **Change.** Enable Remote Control on Claude Start and record it in the receipt.
- **Files.** `herdr/launch.rs`.
- **Acceptance.**
  - The fixture asserts the flag.
  - A `testing-harness-visual-state` witness shows Remote Control enabled on a Flow-started Claude.

### G6. Codex gets the Flow system prompt

- **Vision.** `Vision/flowNexus.md`: "A Nexus component decides the system prompt and everything about a launch". e51411: "put our spirit and stuff there and our vision".
- **Current.** Codex keeps its stock base instructions (comment at `launch.rs:908-911`). It only gets a "read <bundle>" line.
- **Change.** Pass the bundle as Codex base or developer instructions. Take the mechanism from the `codex-harness` skill.
- **Files.** `herdr/launch.rs` and `codex.rs`.
- **Acceptance.** The Codex rollout's session or turn context shows the bundle as instructions, and there is no "read <bundle>" line in the prompt.

### G7. Shorthands around the central Start

- **Vision.** e51411, 2026-09-25: "It should have a complex Flow start call and then it should have shorthands for partly preconfigured minimal calls that don't require so many arguments passed." fd0f97: "we should always have a simple command for everything."
- **Current.** The CLI takes one 13-position datom (`crates/flow/src/main.rs:27-43`).
- **Change.**
  - First, write the pattern up as a proposal for the living's review, as they asked.
  - Then add client-side shorthands that expand into the full Start Query. The Nexus still receives only Signal.
- **Files.** `crates/flow/src/main.rs`, plus a proposal under the flow's reports.
- **Acceptance.**
  - A unit test shows a shorthand yields a Query byte-identical to the long form.
  - The long form is unchanged.

### G8. Refresh replaces, and reaps in the same event

- **Vision.** `Vision/flowNexus.md`: "Reaping belongs to the refresh event, not to a later sweep." d8df70: "A seat starts receiving. The old seat stops receiving first."
- **Current.** Restart always refuses (`lib.rs:384-399`). The Signal has no Replace or Refresh.
- **Change.** Add a Replace query in signal-flow and the Nexus. It starts the successor with predecessor set to the old flow. On Started, it marks the old flow Stopped before the successor is routable, then closes the old pane.
- **Files.** `signal-flow/ethos/signal.ethos`, `src/generated`, `tests`, and flow-nexus `lib.rs` and `store.rs`.
- **Acceptance.** A fixture shows:
  - List has the old flow Stopped and the new one Active.
  - ResolveRecipient on the old ID is refused.
  - There is no state in which both are routable.

### G9. Launch outcome by request ID, by subscription

- **Vision.** `Vision/flowNexus.md`: "It is assigned a request ID, by which it asks later for status". `Vision/nexus.md`: "Polling is forbidden"; "State is observed by subscription".
- **Current.** Start returns LaunchPending or StartAmbiguous, and the caller has to send Start again to learn the outcome (`lib.rs:120-183`).
- **Change.** Add a status query and a subscription keyed by LaunchRequestId. It streams LaunchAttempt phases until Started or Rejected. Drive it from file-change notification on the transcript, not from re-reading.
- **Files.** signal-flow ethos, flow-nexus `lib.rs` and `herdr/launch.rs`.
- **Acceptance.** A fixture subscriber receives each phase once. There are no repeated Start calls and no sleep loops.

### G10. Nexus configuration

- **Vision.** `Vision/nexus.md`: "A Nexus starts with no arguments and there is no bootstrap binary. Its executable holds a default configuration as a constant." Also: "The meta socket carries a Configure interface".
- **Current.**
  - `main.rs` panics without its environment variables.
  - It hard-codes `/home/li` and uid 1001.
  - `codex.rs:500` and `:805` hard-code `/home/li/primary/flows`.
  - The repo unit file cannot start.
- **Change.** Derive defaults from HOME and XDG_RUNTIME_DIR. Store the source root and the Codex endpoints in the Sema configuration, settable through meta Configure. Fix the unit file.
- **Files.** `crates/flow-nexus/src/main.rs`, `store.rs` and `codex.rs`, `deployment/flow-nexus.service`, and meta-signal-flow if Configure needs the fields.
- **Acceptance.** flow-nexus starts with an empty environment and a temp HOME. After meta Configure, `flow 'List.{}'` answers.

### G11. Specialized Start (gated: do not dispatch before the living rules)

- **Vision.** e51411 flowAspect: "It's a specialized flow so it takes another kind of variant for its specialty".
- **Current.** There is no Specialty in the Signal. The distillation proposes `StartSpecialized` and leaves three questions open.
- **Change.** After the ruling, add the variant to signal-flow and the Nexus, and add `#start-specialized` to flow-clj.
- **Acceptance.** A Monitor Start fixture passes, and the Monitor is woken by a hook, never by polling.

### G12. flow-clj does not exist

- **Vision.** e51411 flowAspect: "Astra should implement that on both sides. It's like a flow [Clojure], simple and easier to implement than the rest. Simple flow with, again, the EDN input, typed input." e51411 stack: "It's just a simple standalone CLI. … compile it for deployment. … Use the power of Nix there."
- **Current.**
  - There is no repo or checkout.
  - The contract is written: f5a74e's four forms with Malli schemas.
  - The contract's grounding is stale (see Improvement I4).
  - There is no `clj-build` Nix library either.
- **Change.** Create LiGoldragon/flow-clj as a Babashka CLI:
  - It reads `#start #stop #list #send`.
  - It validates them with Malli.
  - It translates them into Flow datoms, or into its own Herdr actions, depending on the Unknowns ruling.
  - It is Nix-packaged the way messenger-clj is.
- **Owner.** The dispatch names Field Astra 504461. Coordinate with it first.
- **Acceptance.**
  - The contract's four valid and five rejected examples run as tests.
  - `flow-clj '#list []'` returns the live list.

## Improvements

### I1. A single bad frame kills the ordinary socket

- **Current.**
  - `read_query` uses `?` inside the serve loop (`lib.rs:702-707`), and the ordinary thread ends in `.unwrap()` (`main.rs:80-82`). One malformed frame therefore panics the ordinary thread. The process stays alive on the meta socket, so systemd `Restart=on-failure` never fires.
  - Serving is serial with no read timeout. One idle client, or one Start, blocks every ordinary call.
- **Change.** Handle each connection separately, drop the connection on a frame error and log it, and add a read timeout.
- **Acceptance.** A test sends a garbage frame and then `List`, and `List` succeeds.

### I2. Contract mains lag the pins

- **Current.** signal-flow ab70332 and meta-signal-flow a34bc65 exist only on `flow/system-prompt-bundle-00f95a`. signal-flow main is at 1.1.0.
- **Change.** Merge the branch into each contract repo's main and tag signal-flow 2.2.0.
- **Acceptance.** `git branch -r --contains ab70332` includes origin/main.

### I3. The repo unit file is unusable

Folded into G10, and listed here so it is not lost.

### I4. Stale nested clone

- **Current.** `/home/li/primary/flow` is at 42b98ba from 2026-09-17. It misled the f5a74e contract grounding.
- **Change.** Ask the main flow whether to replace it with a pointer to `/git/github.com/LiGoldragon/flow`. Also correct the contract's Grounding paragraph.

### I5. Possibly stale lock

- **Current.** Lock 5200 by 6288d1 is on a jj workspace last changed on 2026-09-24.
- **Change.** Run the `stale-lock` skill check on it.

## Repo holders

These are the same as in Findings, with more detail:

- **flow.**
  - Git worktrees: `launch-profile-47764b` at be898a4, `start-store-47764b` at 33b9f60, `transcript-schema-repin-47764b` at 4c985b6, and `/tmp/field753-flow-pending` at 481b690.
  - Lock 5200 is held by 6288d1.
  - About 19 jj workspaces exist; I listed them and did not check their owners.
- **signal-flow.**
  - Git worktrees: `launch-profile-47764b` and `start-store-47764b`.
  - jj workspaces: `mind-astra-47764b-lifecycle-contract`, `night-messaging-0ab019` and others.
  - No lock.
- **flow-clj.** Absent.
- **504461.** It has no source holds. It owns Flow 0.7 activation and consumer coordination.

## Unknowns

- Is flow-clj a front end to Flow Nexus, or a separate Herdr-level Flow with its own Datalevin state? The receipt says "over Herdr … Datalevin for state". A separate one risks a second flow registry. This needs a ruling before G12.
- There is a naming tension:
  - `Vision/flowNexus.md` says "named after its direct ancestor".
  - The current titles in `testing-flow-titles` and the V2 notion use aspect, model and Flow ID.
  - This should go to the living before G4.
- The specialty ruling is still open on three questions: sibling call or option, the minimum payload, and whether roles are per model or per model and effort.
- I did not run the Codex path, so I have not witnessed that it produces two user turns. The same goes for the name of Claude's Remote Control flag.
- I did not check whether 6288d1 is alive. I ran no cargo or Nix checks.
- The primary tree has uncommitted `tools/native-worker-launch.mjs` from 00f95a. I did not touch it.
