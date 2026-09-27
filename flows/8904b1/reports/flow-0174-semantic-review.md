# Flow 0.17.4: semantic review of the plain direct-form fix

Subflow of 8904b1, read-only, 2026-09-26. Follows
`reports/flow-0173-semantic-review.md` §2 ("Defect found"). Nothing was
built, tested, evaluated, activated, or messaged. One `git fetch` of the
0.17.4 tag into the local flow clone (objects and FETCH_HEAD only).

Labels: **O** observed in source, git, or the remote; **I** inference;
**U** unknown. A commit message, test name, or UPGRADES line is that text's claim.

## 1. What is there (remote)

`git ls-remote git@github.com:LiGoldragon/flow.git` (O):

- `refs/tags/flow-0.17.4` = `bc464e5e1b94fcc179af73111f43b69db1f69fc5`; `main` and HEAD also point there.
- `refs/tags/flow-0.17.3` = `0b512ee0b6681b1925fee7b6435aa7c2eac26bfb`, unchanged; `flow/0173-merge-56ae53` still at 0b512ee.
- Both tags are lightweight (no peeled `^{}` entries).
- `git merge-base --is-ancestor 0b512ee bc464e5e` succeeds. History between them: cb61511 "Flow 0.17.4: attest plain Claude direct startup form", bc464e5 "Release Flow 0.17.4", both by li on 2026-09-26.

## 2. What changed in behaviour

Diff 0b512ee..bc464e5e (O): Cargo.toml/Cargo.lock/flake.nix version strings;
UPGRADES (+10); `crates/flow-nexus/src/herdr/launch.rs` +44 (11 production
lines, 33 test lines). `composition.rs`, `launching.rs`, the store, the wire
crates, and the flake inputs did not change.

The one production change: the Claude branch of `observe_native_target_receipt`
gains a match arm, placed after the pasted-wrapper arm and before
`None if claude_stack > 0 && !input_verified` ("loaded no stacked command"):

    None if Self::prompt_text_matches_intent(text, durable_intent)
        && Self::claude_direct_skill_prompt(text) => { claude_stack = 0; input_verified = true; }

Composition, the prompt sent, argv, the Codex path, the stacked path, and the
Skill/result/companion/receipt checks are untouched (O). In plain terms, a
plain transcript row that is exactly Flow's composed direct-form prompt now
counts as the first prompt, the same way the wrapped form already did.

Correction to the 0.17.3 report (O, `launching.rs` 252–257, 296–299): an
observer `Err` is mapped to `PromptDeliveryResult::Ambiguous`, and the error
text is discarded. So under 0.17.3 the defect left the Start **StartAmbiguous**
(pending, re-observed by `promote_ambiguous`), not recorded as failed.

## 3. Does it close the gap; what it opens

What a plain row must satisfy (O):
- `prompt_text_matches_intent`: the text ends with the fixed Claude footer
  (`strip_suffix`), and SHA-256 of the remainder equals the persisted
  `intent.prompt_sha256`. Both parts are required. The hash is taken over the
  text Claude wrote into its transcript and compared with the hash of the body
  the server composed and stored.
- `claude_direct_skill_prompt`: starts with `"Read "` and contains
  `then load these skills through the Skill tool in this order:`. Given a hash
  match, this adds nothing about identity (I). What it does is keep a plain
  row of a *stacked* prompt (which starts with `/`) on the "loaded no stacked
  command" path.
- Afterwards every selected skill must arrive in order as a Skill tool_use,
  with a successful tool_result carrying the matching `commandName`, and an
  exact source-expansion companion. The single receipt must carry the intended
  model and effort. None of this changed (O).

What ties the entry to this Start (O):
- the Claude body names the per-launch bundle `launch-<16 hex of SHA-256("flow-remote-control-v1\0"+launch_request_id)>.md`, so the hash is per launch request;
- the transcript is read only for the bound `native_session_id`;
- reading starts at the persisted boundary (inode, byte offset, prefix hash).

Candidate false accepts (I from code):
- **Typed or pasted by someone else.** Accepted only if it is byte-identical to Flow's composed text, which includes the per-launch bundle path. Otherwise the row is rejected (the Start stays Ambiguous), not accepted.
- **Messenger delivery into the pane at startup.** If it lands before the prompt, it is rejected, and every re-observation rejects it again: the Start stays Ambiguous permanently. If it lands between the prompt and the last skill, the final `None` arm errors the same way. This is fail-closed and was already so before 0.17.4, but it is a liveness gap.
- **A prompt from an earlier start.** Excluded twice: by the boundary, and by the different bundle path in the hash. A retry of the same launch request has the same body, but that is the same Start.
- **A text that merely contains the footer.** Rejected, because the footer must be the suffix and the body hash must match.

Gaps (I):
- The new arm (like the older pasted arm) lacks `!input_verified`. A second identical copy of the prompt before skills complete is silently accepted, whereas the final plain arm rejects a second copy. This is small and does not open a false accept.
- The observer requires Claude to record the text byte-exact: newlines kept as `\n`, no trimming, no CR. Whether Herdr `agent prompt` sends a line break as a literal newline or as Enter, which would submit line one alone, is unwitnessed (U). If Enter, the result is fail-closed (Ambiguous), not wrong.
- **Single short line.** Unchanged. It still takes the stacked form, and a plain record of it still errors "loaded no stacked command" (O).

## 4. What the tests test

No new test function. `claude_pasted_direct_skill_prompt_normalizes_the_wrapper_and_requires_each_skill` gains three cases (O). "Seven of seven" plausibly means the seven `claude_*` tests in `herdr/launch.rs`: environment_preparation, receipt_of_a_model_without_effort, stacked_command_prompt_reaches_its_receipt, pasted_direct…, receipt_after_further_skill_loads, title_set_after_claim, title_readback_differs (I; the run command was not seen). Only the extended one touches the change; the other six are unchanged since 0.17.3 (O).

All of it runs on fixtures: `fixture_herdr` stub executables plus handwritten JSONL. No real Claude or Herdr (O). The body is handwritten, not composed: the direct wording plus 34,369 `x`, one line, **no line break**, with bundle path `/tmp/flow-system-prompt.md`. The test computes the hash with SHA-256 over that body and sets it as the persisted intent. That is an input, not an oracle for the tested path.

Added cases (O):
- (a) **plain** = the exact prompt row, then two skill triplets and the receipt; expects Observed, `turn-direct`. Without the fix this row reaches `claude_stack(2) > 0`, the call errors, and `.unwrap()` panics (I), so the case would fail without the fix.
- (b) **plain_altered** = a different direct-wording text with no footer; expects Err "loaded no stacked command". A rejecting case, but it changes body and footer together.
- (c) **incomplete** = the plain prompt, spirit only, then the receipt; expects Err "target receipt preceded native skill confirmation".

Not tested:
- the composer→observer path for a short multi-line prompt, which is the actual defect case;
- a body with `\n`;
- footer present but body hash wrong;
- body right but footer missing;
- a foreign row before or after the prompt;
- a duplicate prompt row;
- a wrong model on the plain path;
- a failed Skill result on the plain path;
- a real Claude/Herdr run.

"Formatting passed" and "seven passed" were not re-run here (U).

## 5. Version and notes

- **Version step.** A patch fits (I): a bug fix in observation only, with no wire, store, or argument change, following 0.17.1 and 0.17.3.
- **What UPGRADES says.** It states the behaviour and keeps "Deploy beside Message 0.17.0". It does not say "non-breaking" and does not name rollback.
- **Move from 0.17.3 to 0.17.4 (I).** The stored intent shape is unchanged. A plain-direct Start left Ambiguous under 0.17.3 would, on `promote_ambiguous` under 0.17.4, re-read from its boundary and reach Started.
- **Move back to 0.17.3 (I).** An already Started row stays Started. A still-pending plain-direct Start stays Ambiguous.
- **Move back to 0.17.1 (I).** It also rejects the wrapped form. Also Ambiguous, not Failed.

## 6. What a live witness must look for

Plan (from brief): two short lines arriving plain, a long prompt arriving
wrapped, and a single short line; plus three cases that must fail: a skill
that cannot load, a wrong model, and a first entry not matching the stored prompt.

- Two short lines. This is the only real test of the fix. It must also show the transcript row byte-for-byte: the `\n` kept and a single row, not the first line submitted alone.
- The long wrapped prompt and the single line are regression checks. They are adequate.
- Failure is **StartAmbiguous with the reason discarded**, not a rejection. Each failing case needs the transcript read to show *which* check held, or all three look alike.
- Missing: a foreign plain row landing in the pane before the prompt (for example a messenger delivery), expected to stay Ambiguous for good.
- Missing: an ordinary message after the receipt, which must not disturb Started.
- Missing: a 0.17.3→0.17.4 promotion of an already-Ambiguous plain-direct Start, if one exists or can be staged.
- Missing: the rejecting case "footer present, body altered", which the fixtures also lack.

## 7. Addendum: 7 against 17, and fixture against live

This addendum weighs 56ae53's second claim: 17 focused Claude tests, 0 failed,
on a clean local tree at the tag. It also weighs 6fe957's claim that cb61511b
adds the plain case. Both are claims; nothing was run here.

Test names at bc464e5e containing `claude_` (O):

| File | Count | Tests |
|---|---|---|
| composition.rs | 8 | stacks_its_skills_as_head_commands, stacks_at_most_five…, launch_records_its_remote_control_flag, short_claude_prompt_keeps_native_command_expansion, past_the_native_command_limit_uses_direct_skill_form, instruction_with_line_breaks_uses_direct_skill_form, canonical_check_keeps_a_hashed_long_prompt, launch_copy_carries_predecessor… |
| herdr.rs | 1 | claude_idle_ready_snapshot_is_unchanged |
| herdr/launch.rs | 7 | the seven in §4 |
| herdr/pane.rs | 1 | a_claude_composer_reads_by_its_own_glyph |

That is **17**. The substring `claude_` selects exactly these 17. The same
filter restricted to `herdr::launch` selects the **7** (I). Two submission
tests (`…claudes_interrupt…`) have no `claude_` substring, so they are not
selected. Only one test changed in this delta (O, the diff adds no `fn`). So
16 of the 17 are 0.17.3 tests, and the one extended test holds every plain-path
assertion. cb61511b is the delta commit (O), matching 6fe957.

Rejecting cases. All run the observer against handwritten JSONL behind
stub executables; none runs Claude or Herdr (O).
- "Altered", on the plain path: `plain_altered`. On the wrapped path: `altered`.
- "Missing": `incomplete`, which omits main-flow before the receipt.
- "Forged skill receipts": no test uses that word. The closest are in
  `claude_stacked_command_prompt_reaches_its_receipt`: first-turn text differs,
  stacked command differs, loaded no stacked command, and Skill order differs.
  They are on the **stacked** path, not the plain direct path.
- Wrong model/effort and a replaced/truncated/changed transcript are asserted
  only in `claude_receipt_of_a_model_without_effort_is_observed`.
- The composer's `claude_instruction_with_line_breaks_uses_direct_skill_form`
  uses a two-line instruction with **zero** skills. It checks composition only
  and never feeds the observer.

Covered by fixtures (I from reading):
- Observer acceptance of an exact plain direct row; a single line with no `\n`.
- Rejection of a different plain text without footer.
- Skills still required on the plain path.
- The boundary and model checks (other tests, not on the plain path).

Not covered by any fixture:
- A multi-line body through the observer.
- Composer output fed to the observer.
- Footer present with the body altered.
- A foreign or messenger row before or during the first turn.
- A duplicate prompt row.
- Wrong model or failed Skill on the plain path.

Only a live start can show:
- whether Herdr `agent prompt` and Claude Code keep a two-line prompt as one row, with `\n` byte-exact and `content` a string;
- which shape (plain or wrapped) Claude actually picks at each size;
- that a real pane message at startup leaves the Start Ambiguous rather than Started.

## Concerns

1. No fixture exercises a multi-line body or the composer→observer path for the defect case, and the only live-relevant question (Herdr/Claude keep `\n` byte-exact) is unwitnessed. Blocks activation only.
2. Failing Starts surface as StartAmbiguous with the error text discarded. The live plan must read transcripts to see why. Blocks activation only (witness design).
3. A pane message before or during the first turn leaves the Start Ambiguous forever. This predates 0.17.4. To be noted.
4. The new and pasted arms accept a duplicate prompt row; the plain arm rejects one. To be noted.
5. UPGRADES does not state "non-breaking" or rollback behaviour. The 0.17.3 report said "failed" where the code gives "ambiguous". To be noted.

Nothing found blocks pinning 0.17.4 in Home: the tag is on the remote, it descends from 0.17.3, 0.17.3 is intact, and the change is one observer arm that accepts only the exact composed text of this launch.

## Unknowns

Which seven tests ran and on what command; whether formatting and the tests
passed at bc464e5e; Herdr `agent prompt` newline handling; whether Claude
Code 2.1.280 stores a two-line plain entry byte-exact as a string `content`.

## Sources

- Remote: `git ls-remote git@github.com:LiGoldragon/flow.git`; `git fetch origin refs/tags/flow-0.17.4`.
- /git/github.com/LiGoldragon/flow: `git log`, `git diff 0b512ee bc464e5e`; at bc464e5e: `crates/flow-nexus/src/herdr/launch.rs` (676–729, 822–854, 1371–1832, 2789–2927, test list), `crates/flow-nexus/src/composition.rs` (73–90, 130–140, 176–258, 551–745), `crates/flow-nexus/src/launching.rs` (240–330), `UPGRADES.md`.
- Test enumeration: `#[test]` names in every `.rs` at bc464e5e; `composition.rs` `claude_instruction_with_line_breaks_uses_direct_skill_form`.
- Claims weighed, not verified: 56ae53 (7/7, then 17/17 by an independent tester); 6fe957 (cb61511b).
- flows/8904b1/reports/flow-0173-semantic-review.md.
- Skills: claude-harness (wrap thresholds), testing, versioning.
