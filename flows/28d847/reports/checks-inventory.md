# Checks that block work: inventory

Every guard, refusal check, verification step and review gate in the stack that blocked or stalled work in the flows of 2026-10-01 to 2026-10-03, each described as it is now (2026-10-03, evening).

Tags: **W** witnessed (code read, command run, probe, or a record read first-hand; the place is named). **W(rec)** the record was read first-hand, but the event it describes was not re-run. **S** supposed: inference, or a flow's claim that was not checked; whose it is is named.

The living's intuition ("a class of checks … bullshit") was tested without leaning either way. The verdict column answers one question: can the failure the check guards against still happen today?

## Table

| # | Check | Where it lives | Blocked work | Guarded failure | Still possible today? | Without it | Model work code could do |
|---|---|---|---|---|---|---|---|
| 1 | Messenger link guard `retireProvenLegacyMessengerBindings` | CriomOS-home `modules/home/profiles/min/messenger-clj.nix`, on `origin/main` only | 13:00 activation; deployments 79 and 81 | `force = true` silently overwriting a hand-installed messenger link | No on the deployed line (guard and `force` both gone; Home Manager refuses foreign files itself). Yes, falsely, on any build from main. | Home Manager's own collision check refuses | Yes: each fix was a store path a model pasted in by hand |
| 2 | Launcher VCS guard (main must be an ancestor of `@`) | Primary `tools/claude-main-flow-launch.mjs`, removed | Successor launches (91ea9f, caf622, 3ec648) | Launching a seat on unpublished skill text | Yes, and it happens now: launches read the live tree, which holds uncommitted skill edits | Already removed | Was code |
| 3 | Flow Start pane environment marker | flow `crates/flow-nexus/src/herdr/launch.rs:185-237` | First private Start (54-column pane wrapped the marker) | Claude starting with the parent's `FLOW_ID`/session or no `FLOW_SOCKET` | Impossible on flow main (test passes); unknown on live Herdr. The false refusal is still possible on deployed Flow 0.23. | Hooks report under the wrong flow or Nexus | Is code |
| 4 | Flow Start flows-root claim refusal | flow `launch.rs:338-375` → `ClaimRefused` → answered as `BindingRefused` | One private Start | A flow id claimed into a missing or wrong root | Impossible: `flow-id` exits 2 on a missing root | Claims written outside Primary, or a later random failure | Is code; mislabelled refusal |
| 5 | Flow Start native-session binding (`BindingRefused` at Title) | flow `launch.rs:1161, 410, 1403-1520`; `launching.rs:232-237` | Three private Starts (prepared, combined, pre-reservation) | Typing the first prompt into a pane with no live session of the expected Claude | Possible, and it was the real state: the pane sat on Claude's first-run theme screen | First prompt typed into the theme picker; a flow registered with no session | Is code; the missing step (mark onboarding done in the sandbox) is code too |
| 6 | `FLOW_ID`/`FLOW_DIRECTORY` from the environment, checked by the model | Skill prose (`main-flow`, subflow role text); launcher export decided but not built | Indirect: `$subflow` in briefs; flows without an identity | A flow working without its identity | Possible: this subflow has neither variable | n/a | Yes, entirely |
| 7 | flow-test provenance pin | flow-test `packages/flow-claude-hook.nix:94-96` | Review returns; would refuse now | A witness run under unreviewed skill text credited to the reviewed one | Impossible: fails closed, and fails now on every regeneration | Witness credited to the wrong skill text | Is code; pinning the skill into the derivation would end the drift |
| 8 | flow-test credential boundary (bwrap, `dontAsk`, tool deny list, one MCP tool) | flow-test `packages/flow-claude-hook.nix` | Several review returns | The seat reading or emitting the copied credential | Unknown: only a fixture without credentials has run | Credential exposed to a test seat | Is code |
| 9 | Herdr "not inside Herdr, stop" | Prose in Herdr's bundled skill, `skills/herdr/SKILL.md:13-16` | Field's attach and first-turn witness | An agent outside Herdr driving the living's Herdr | Possible: the binary does not enforce it | Nothing in code stops it | A model rule; a private socket is the code form |
| 10 | Orchestrate locks: PrimaryPublish and path overlap | orchestrate-nexus `store/transition.rs:51-69`, `normalize.rs:127-140`; skill `compensation-primary-commit` | Publishes rejected (9fb0ad, 42265e, 5578cc); quiet windows | Concurrent jj in the one shared checkout dropping work | Possible: advisory only; two jj operations ran at once today; 26 files were lost today | Every publish races every other | Yes: the hand-typed jj sequence is what `primary-publish.mjs` automates (present, not on main, not enrolled) |
| 11 | Orchestrate lock-path validation | orchestrate-nexus `normalize.rs`; session drop `transport/mod.rs:254-262` | Field's Curriculum lock (quoted paths), others | Locks on relative, empty or escaping paths | Impossible (reproduced refusal). The refusal arrives as a fake "Unreachable". | Locks that reserve nothing | Yes: models diagnose a misleading frame error |
| 12 | jj bookmark and push refusals | jj 0.44.0 built-ins | dea0ba, 3ec648, 5578cc | Overwriting origin main from a stale or diverged line | Possible: origin main is unprotected; push is force-with-lease | Silent loss of origin history | Yes: models pick targets by hand |
| 13 | Lojix meta client request decoding | lojix `clients/meta/src/lib.rs` | Once, before deployment 79 | A malformed transport reaching build and activation | Guard present; a well-typed wrong value passes | Wrong transport used | Yes: a model builds a 14-field request by hand; no retry command exists |
| 14 | Throwing `system`/`horizon` stubs in the Home and CriomOS flakes | CriomOS-home `flake.nix:18`; CriomOS `flake.nix:124,137` | Redirected one direct build to Lojix | A Home closure built outside Lojix with a stale or default horizon | Guard present (stubs throw) | Unrelated closure activated outside Lojix | Is code |
| 15 | Messenger delivery holds (`Held`/`RepairRequired`, `Blocked`) | messenger-clj `core.clj:426-430, 509-510, 329` | Sends held or blocked (3ec648, 9fb0ad, f1c841, 1bc255, 5104af, 6997eb) | Typing into a pane that no longer matches its binding | Possible (S) | Messages typed into the wrong pane | Partly: retiring a predecessor is done by models by hand |
| 16 | Claude Code's built-in dangerous-`rm` prompt | Claude Code 2.1.284, ignores bypass mode | Two waits on the living: 11 h 20 m (approved), 54 min (declined) | `rm` with an empty variable deleting from root | Possible: no hook or setting answers it | Possible root-relative deletion | Yes: a lint or `${VAR:?}` rewrite in code |
| 17 | Provenance receipts and checksum handoffs | Skills `behavior`, `flow-evidence`, `knowledge-codex`, `knowledge-flow`, `knowledge-nexus`; subflow role text | Review cycles keyed on full SHA-256s; hedged reports | Hashes in model context; unverifiable provenance | Possible: full hashes in 41fa34's log today; the receipt tool does not exist | n/a | Yes, by the rule's own words; the code is missing |
| 18 | `trial-generated-projection` | Skill; Curriculum regenerator self-checks | No stall found | Stale generated tree | Possible (a stale `book.md` was caught by the regenerator's Check) | Stale projections | Yes: the regenerator's Check already does it |
| 19 | Mind review of flow-test candidates | Model gate (Mind Sol) | Seven candidates in about 24 min, several returns | Bad test witness | Possible: the review missed a shellcheck build failure and a 10 s live failure | Unreviewed infrastructure lands | Partly: `nix build` would catch the build failure |
| 20 | Mind review of Home candidates | Model gate (Mind Sol) | Accepted two candidates that then failed activation | Bad activation | Possible: activation caught it twice; review did not | Activation and rollback are the real check | Yes: an activation test in a VM or sandbox |
| 21 | Evidence and co-report requests after "no extra approval gate" | Model gates (Mind Astra, Mind Sol, Field Astra) | Deployment, 17:43–17:57 | None found | Unknown | Nothing lost that the records show | n/a |
| 22 | Psyche Opus's holds and grants | Model gate (5578cc) | Build of the old Flow design; deploy order turned into questions for about 2.5 h | Building a superseded design; leaving a credential behind | Credential leftover impossible in source; rework unknown | Probable rework (S) | No |
| 23 | Guarded worktree removal | `private-repos/worktree-retirement-tools/42265e/guarded_remove.py:93-173` | All worktree cleanup stopped through 10-03 | Deleting a worktree with unpreserved work | Possible (rec): an unguarded deletion lost a flake pair | Work lost (it happened) | Is code |
| 24 | ethos-zero kind refusal (`KindWanted`) | ethos-zero `error.ethos:21` | The `dependency-ethos` check (3ec648) | Concrete types in input position | S: the refusal was intended | n/a | Is code |

## Per check

### 1. Messenger link guard
- W: The guard is on CriomOS-home `origin/main` (`messenger-clj.nix:41` `force = true`; `:57` `refusing to replace non-legacy messenger binding`). It admits only the hand-made 0.2.5 chain or one pinned Home Manager files root.
- W: The live Home generation is 1045. Its `activate` has no `retireProven`. `~/.local/bin/messenger-clj` points into 1045's own `home-manager-files`. The guard's removal is on branch `origin/flow-home-guard-orchestrate-037-56ae53` only, not on main.
- W: Built from main today, activation would refuse again: the live link is neither the pinned root nor the 0.2.5 chain.
- W(rec): It refused at 13:00 (generation 1040), at deployment 79 (1041) and at deployment 81 (1043). 1040 and 1041 have a link time in the profile; the refusals themselves are from `flows/9fb0ad/log.md:32` and `flows/5578cc/reports/deployment-timeline-2026-10-03.md`.
- W: The failure it guarded: the original commit placed the eleven messenger links under Home Manager with `force = true`, which turns off Home Manager's own collision check. The guard replaced that check for the one known hand-made chain (`~/.local/libexec/messenger-clj` → 0.2.5, hand-made symlinks on 2026-09-25, `flows/da88cf/reports/inventory-system.md:35`).
- W: Whether a hand-installed copy can still occur:
  - No tracked code in any repo under the ghq root, nor in Primary, writes `~/.local/bin/messenger*` or `hm-*`.
  - messenger-clj's README now says Home manages the binding.
  - A model typing `ln -s` by hand remains possible (S).
  - The leftover `~/.local/libexec/messenger-clj` was hand-pointed to 0.2.8 on 10-02 11:19 by an unknown writer. Nothing reads it as a binding.
- W: Without the guard, Home Manager 26.11's `check-link-targets.sh` refuses any existing file or working link at a target that is not inside `*-home-manager-files` ("Existing file … would be clobbered"), unless a backup variable is set.
- Gap, W in the code: a broken foreign symlink is not checked. S: the link step would replace it silently.
- W/S: The guard itself is code. The model work around it was re-pinning a store path by hand for each deployment (S, from commit messages), which Home Manager's own pattern match already does generically.
- Verdict: guarded failure witnessed impossible on the deployed line. A false refusal is witnessed possible on any build from main.

### 2. Launcher VCS guard
- W: Removed. Neither Primary launcher on origin main calls jj. Skills are read from the live working tree.
- W(rec): It refused successors at `flows/91ea9f/log.md:80` and `flows/caf622/log.md:483`.
- W: The failure it guarded now happens. The working tree holds uncommitted `.claude/skills/*` edits (git status at this session's start), so a launch now delivers unpublished skill text.
- S: The living accepted this by design.
- Verdict: guarded failure witnessed possible (and present).

### 3. Pane environment marker (Flow Start)
- W: How it works:
  - Flow types an unset and export chain, then `printf FLOW_CLAUDE_ENV_READY_<request digest>`.
  - It waits for the marker with `herdr pane wait-output`, then requires an exact pane id and line.
  - Only then does it start Claude.
- W: On flow main the source is `recent-unwrapped`. Its narrow-pane test passes in a scratch clone.
- W: Deployed `flow-nexus` and `flow-nexus-next` run Flow 0.23.0, whose binary lacks `recent-unwrapped`.
- S, from the code: it guards against Claude inheriting the parent seat's `FLOW_ID` or `CLAUDE_CODE_SESSION_ID`, or lacking `FLOW_SOCKET`. It is not the wrong-pane guard; that one is the exact pane and terminal check at Bind.
- W: In the private runs, the launched Claudes had the right `FLOW_ID` and the sandbox `FLOW_SOCKET` (`/proc/<pid>/environ`).
- Verdict: guarded failure witnessed impossible on main with the fake Herdr; unknown on the live Herdr. A false refusal is witnessed possible on deployed 0.23.

### 4. Flows-root claim refusal
- W: Reproduced in scratch: `flow-id` exits 2 when the root is missing.
- W: Flow answers this as `BindingRefused`. Its reason goes only to the Nexus's stderr.
- Verdict: guarded failure witnessed impossible.

### 5. Native-session binding at Title
- W: In the private Herdr, both Flow-launched Claudes show `interactive_ready:true` and `agent_session:null`.
- W: Pane w4:p1 shows Claude 2.1.284's first-run theme screen. The sandbox `.claude.json` lacks `hasCompletedOnboarding`.
- W: Herdr's SessionStart hook was installed before that launch.
- W: The three live seats launched with `--settings` all have Herdr sessions.
- S: So SessionStart never fired because onboarding blocked it. Flow's `--settings` did not displace the hook.
- W: The refusal reason is a stderr line only on flow main. It is not stored and not on the wire. Deployed 0.23 has none of this.
- Verdict: guarded failure witnessed possible. The refusal was correct: there was no session.

### 6. Model-checked flow identity
- W: `main-flow` says to run `flow-id` by hand. The subflow role text asserts that `FLOW_ID` and `FLOW_DIRECTORY` are in the environment.
- W: Both are empty in this subflow (`env`).
- W: The launchers claim through `flow-id` after spawn and export neither variable. The "missing value fails" decision (`flows/5578cc/log.md:130`) is not built.
- W: The living: "there's no reason for us to make the model check the flow ID" (`flows/5578cc/vision/flow.md`).
- Verdict: guarded failure witnessed possible.

### 7 and 8. flow-test provenance pin; credential boundary
- W: The provenance check hashes the Curriculum source and the Primary projection before the credential copy, with exit 2 on mismatch.
- W: Today both hashes differ from the pins, so a run would refuse.
- W: The credential boundary: bwrap, `--permission-mode dontAsk`, a deny list of Bash, Read, Edit, Write, Glob, Grep and the web tools, and one MCP tool.
- W: Only a fixture without credentials has run.
- S: Unlisted tools rely on `dontAsk`, which might also deny the MCP tool. Unverified.
- Verdict: provenance, witnessed impossible (fails closed). Credential boundary, unknown.

### 9. Herdr external-session rule
- W: The rule is prose in Herdr's bundled skill.
- W: The binary uses `HERDR_ENV` only to block nesting. `herdr agent list` with every `HERDR_*` variable removed still listed the live agents.
- Verdict: guarded failure witnessed possible (only a model's choice prevents it).

### 10. Orchestrate locks and PrimaryPublish
- W: Rejections: `DuplicateName` and `PathOverlap`, comparing path strings only.
- W: Today's operation log shows a push and a fetch running at once in Primary (14:22:12 and 14:22:13), later reconciled.
- W(rec): Losses in the shared checkout today: six files rewritten by a rebase (`flows/5578cc/log.md:108`) and 26 files deleted by an unscoped commit-then-abandon (`flows/5578cc/log.md:114`).
- W: `tools/primary-publish.mjs` is in the working copy, absent from origin main, and has no authority file or state directory. Its design builds the commit with a private index and pushes without force.
- W: The sentinel `.PrimaryPublish.lock` was reported present as an Added file. At this receipt's check it is absent.
- Verdict: guarded failure witnessed possible.

### 11. Lock-path validation
- W: The datom lexer keeps `"` inside a bare word, so a quoted path fails the absolute-path check.
- W: The `StoreError` ends the session. The client prints `Unreachable … failed to fill whole buffer` while the Nexus stays up (PID unchanged).
- W: The contract has no typed rejection for invalid paths.
- W: Reproduced by a read-only subflow: two Lock requests sent to the live Orchestrate, both refused before any store write. They left two journal lines.
- Verdict: guarded failure witnessed impossible. The refusal's delivery is wrong.

### 12. jj refusals
- W: `jj git push` is force-with-lease, not fast-forward-only. GitHub reports `main` unprotected.
- W: Right now `main`, `main@git` and `main@origin` coincide.
- S: A diverged local main pushed plainly would overwrite origin.
- Verdict: guarded failure witnessed possible.

### 13 and 14. Lojix request decoding; flake stubs
- W (by subflow): The parenthesised transport fails client-side decoding. The braced form decodes. Nothing reaches the socket.
- W (by subflow): The `system` and `horizon` stubs throw on eval.
- W (by subflow): The deployment record keeps no transport or horizon. No retry request exists in Lojix 8.1.0 or 9.0.1.
- S: That missing retry, not a check, stalled the 17:52–18:00 retry.
- Verdict: the guards hold and the guarded failure is witnessed possible (the refusals still fire). The stall was the missing retry inputs.

### 15. Messenger delivery holds
- W (by subflow): The code paths exist in messenger-clj.
- W(rec): Holds and blocks are recorded in several logs. Whether a message would have been lost without the hold is unchecked.
- Verdict: unknown whether the holds prevented real harm. The mechanism is S possible.

### 16. Dangerous-`rm` prompt
- W (by subflow): No PreToolUse or PermissionRequest hook is set in Primary, user or Flow-passed settings.
- W (by subflow): The user setting is `bypassPermissions`. The `claude` wrapper adds `--dangerously-skip-permissions`.
- W(rec): Both waits are from `flows/f1c841/reports/blocked-commands.md`.
- W: The living: "I don't want to have to allow stuff manually" (`flows/5578cc/vision/permissions.md`).
- S: Whether a hook can answer this particular prompt is unknown.
- Verdict: the failure of seats waiting on him is witnessed possible.

### 17 and 18. Skill-made checks
- W: The receipt and checksum lines say "Deterministic code retains and compares raw checksums". No such code exists. The subflow role text says to report the receipt "unavailable" until it does.
- W: These lines are uncommitted in Curriculum and Primary.
- W(rec): Full SHA-256s drove Mind Sol's review cycles (`flows/41fa34/log.md:186-196`). The living: "no hashes in a model's context", "You sent them giant hashes".
- W: `trial-generated-projection` has the model run git status and the regenerator. The regenerator already prints `Checked`.
- Verdict: possible for both. Both are deterministic work done by a model.

### 19 to 22. Model review gates
- W (by subflow, from git): The flow-test loop ran seven candidates in about 24 minutes.
- W: One real defect was caught: the first candidate ran without `--settings`. Later: the credential left after failure was fixed in source.
- W(rec): Missed:
  - a shellcheck failure after acceptance (caught by `nix build`);
  - a live run failing in 10 s;
  - two Home candidates that failed activation on the guard in check 1.
- W(rec): The 17:43–17:57 evidence requests found nothing (deployment timeline).
- W(rec): The 12:40 deploy order sat about 2.5 h as questions while a fix existed.
- Verdict:
  - flow-test and Home reviews: possible (the reviews did not prevent the failures; activation and builds did);
  - the 17:43 requests: unknown;
  - credential leftover: impossible.

### 23 and 24. Worktree removal guard; ethos-zero `KindWanted`
- W(rec): An unguarded removal lost a `flake.nix`/`flake.lock` pair, reconstructed but not byte-exact (`flows/42265e/log.md:464`, `flows/3ec648/log.md:93`).
- W: The guard tool's source exists (by subflow).
- S: Whether today's cleanups go through it is unchecked.
- W(rec): `KindWanted` failed `dependency-ethos` (`flows/3ec648/log.md:76-78`). Per that log the refusal was intended.

## What the evidence says about the class

- W/S: The checks that are code and sit at a real boundary refused correctly and held (4, 5, 7, 11, 13, 14). Check 5 refused because there truly was no session.
- W: The checks that caused the most lost time had one of three properties:
  - they were code holding a value a model pinned by hand (1);
  - they were model gates or model-followed prose that did not catch the failures that followed (6, 9, 17, 19, 20, 21, 22);
  - they asked the living to act (16).
- W: Several failures are guarded only in prose while the code form is missing or unlanded: 6, 10, 12, 17.

## Sources

- `flows/5578cc/log.md`, `flows/5578cc/handover.md`, `flows/5578cc/vision/{checks,permissions,flow,publishing,locking}.md`, `flows/5578cc/reports/deployment-timeline-2026-10-03.md`
- `flows/42265e/reports/home-deployment-2026-10-03.md`, `flows/9fb0ad/reports/messenger-guard-fix.md`, `flows/f1c841/reports/blocked-commands.md`, `flows/da88cf/reports/inventory-system.md`
- Logs of flows 9fb0ad, 42265e, 41fa34, edf227, 6e782c, dea0ba, 3ec648, 91ea9f, caf622, f1c841, 1bc255, 5104af, 6997eb
- Code: CriomOS-home (origin/main and `flow-home-guard-orchestrate-037-56ae53`), CriomOS, flow (main), flow-test (main), orchestrate-nexus 0.37.0, protos and datom-codec 0.32.2, lojix, messenger-clj, herdr, ethos-zero, `private-repos/worktree-retirement-tools`, Primary `tools/*.mjs`
- Live reads: the Home Manager profile and its `activate` and `check-link-targets.sh`; `~/.local/bin` links; flow-nexus unit binaries; Orchestrate journal and two refused Lock probes; private Herdr panes and `/proc` environments; `env`
- Five read-only subflows of Psyche Opus 28d847 did the reading. Claims marked "by subflow" were not re-checked by this flow. This flow itself re-checked check 1 (live links, generation 1045's `activate`, main's guard lines, Home Manager's `check-link-targets.sh`) and check 10 (sentinel absent, publish program present).
- Provenance receipt: unavailable (no receipt handoff; `FLOW_ID` empty in this subflow).
