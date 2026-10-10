# Flow one-line Claude prompt: Flow 0.10.2, plus the reap fix in 0.10.3

An Opus subflow of 38de5b did this on 2026-09-25. It follows the main-flow ruling that a Claude first prompt is one line of at most 800 characters with no newline. The coordinator's mid-task addition, that Replace must tell an unreachable Herdr from an absent pane, landed as a separate patch.

- Repository: github.com/LiGoldragon/flow. The work was done in a fresh clone in the scratchpad (`flow-oneline-38de5b-a7`).
- Main moved to 0.10.1 while I worked (0c19364, from another Opus). I rebased onto it, and my change became 0.10.2.
- Revisions pushed to main:
  - d685a213eeb181576d87b83b9933188bf06a34da "Flow 0.10.2: Claude first prompt is one line of at most 800 characters"
  - d864f54bb88aba568c968e03491b424e6243d88e "Flow 0.10.3: Replace refuses the reap when Herdr cannot be read"
- `git ls-remote origin main` returned d864f54.
- Tests:
  - Before, on bbf5fa1: 83+6+3+1+1.
  - Before, on the rebased base 0c19364: 84+6+3+1+1.
  - After 0.10.2: 88+6+3+1+1.
  - After 0.10.3: 89+6+3+1+1, 0 failed.
- `cargo clippy --all-targets` shows 0 warnings, and `cargo fmt --check` is clean. `nix flake check` was not run.
- Version rule, from the versioning skill: a public behaviour change updates the version surface. Neither patch changes the wire, the storage, the argv or the signal-flow contract. The new composition errors map onto the existing `CompositionRefused`, and the reap refusal reuses `ReapRefused.RouteUnavailable`. Each is therefore the next patch.
  - 0.10.1 was taken, so the prompt change became 0.10.2.
  - The reap fix is 0.10.3, because 0.10.2 was already on main when the request arrived.
  - Cargo.toml, Cargo.lock, flake.nix and UPGRADES.md were updated. README.md was updated for 0.10.2 and DESIGN.md for 0.10.3.
- Orchestrate locks 6475 and 6483 were taken and released.

## 0.10.2: the one-line Claude prompt

The Claude `first_prompt_text` is now one line:

- the stacked `/name` commands, at most five, in profile order;
- then `Read <bundle path> for your launch mode`;
- then, if there are more than five skills, `, load <rest> through the Skill tool in this order`;
- then `, then: <instruction_prompt>`;
- then, if there are sources, ` Sources: <abs paths>.`;
- then the footer ` When every skill has loaded, reply once with exactly FLOW_LAUNCH_RECEIPT_V2 and nothing else.`

What changed and why:

- The multi-line `# Flow launch` block (Role, Model, Effort, Predecessor, Remembered flows, Herdr session, Remote control) is gone from the Claude prompt. Codex keeps it.
- The footer is now per harness: `LaunchReceipt::footer_for(&HarnessKind)` replaces `footer()`.
- Composition refuses with a typed error and never truncates:
  - `CompositionError::ClaudeFirstLineBroken` for any CR or LF;
  - `ClaudeFirstLineTooLong(n)` when the length is over 800.
  - Start answers both as `CompositionRefused`.
- `ClaudeFirstLine::LIMIT = 800`. The length is counted in UTF-16 code units. That is conservative: it is never less than the character count.
- `has_canonical_first_prompt` also requires a Claude text to be one line within the limit, so the adapter refuses before the Herdr write.
- Observer changes:
  - `prompt_text_matches_intent` uses the harness footer and requires the one-line shape for Claude.
  - A Claude first turn containing `<pasted_content` is refused ("arrived as pasted content").
  - A plain-text first turn, when commands were expected, is refused ("loaded no stacked command").

Fixtures:

- `claude_prompt_is_one_line_of_at_most_800_characters`: no newline, ≤800 characters, sources inline.
- `claude_line_at_the_limit_is_kept_and_one_past_it_is_refused`: exactly 800 is kept; 801 gives `ClaudeFirstLineTooLong(801)`.
- `claude_instruction_that_breaks_or_overruns_the_line_is_refused`: an LF gives `Broken`; an overlong line gives `TooLong`; the same instruction composes for Codex.
- `claude_canonical_check_refuses_a_line_that_is_no_longer_one_line`.
- Updated tests:
  - `claude_prompt_stacks_at_most_five_commands_and_lists_the_rest` asserts ≤5 commands, with the rest in the same line.
  - `claude_stacked_command_prompt_reaches_its_receipt` is now one line, plus the pasted and literal refusals.
- G3's hash-free test, `composed_prompt_carries_no_hash_request_id_or_source_text`, is unchanged and green for both harnesses.

Codex is unchanged. It still gets typed skill items plus one text through app-server `turn/start`. The codex-harness skill says the turn request's input array takes skill items that expand ahead of the prompt. No terminal paste layer sits in that path, so the 800-character and four-line wrap does not apply.

## 0.10.3: the reap distinguishes an unreachable Herdr

- `HerdrCli::pane_presence` returns one of three answers:
  - `Present`: the binding is shown, and the pane is closed.
  - `Absent`: there is no recorded route, or a readable roster lacks the pane. It counts as reaped.
  - `Unknown`: the snapshot failed, there is no roster, or the pane ID is shown under another binding. The reap is refused as `ReapRefused.RouteUnavailable`: it is retryable, nothing is closed, and the successor is held.
- Fixture `an_unreachable_herdr_refuses_the_reap_instead_of_counting_it_done`:
  - Only the predecessor session's snapshot fails; the successor's session still answers.
  - It asserts the refusal, no `pane close` call, the successor unroutable, and LaunchStatus equal to the refusal.
  - Once Herdr answers again, it retries to `Replaced`, and the close is logged.

## Open, and not witnessed

- There is no live Flow Start of Claude. Nobody has watched the one line expand its stacked commands in a live session.
- The 800 and 4-line thresholds come from e51411's witness on one Claude Code build. The UTF-16 counting has not been witnessed with non-ASCII text.
- Claude's line no longer carries Predecessor, Remembered flows, or the Role, Model and Effort record. The first three live nowhere in Claude's context except the store; model and effort are in the argv. If a Claude successor needs its predecessor named, that belongs in the bundle or the instruction. The ruling did not settle this.
- A 0.10.1 journaled Claude attempt no longer matches the observer's footer, as UPGRADES notes.

## Sources

- `flows/38de5b/receipts/flow-launch-findings.md`; `flows/e51411/reports/pasted-content-threshold.md`.
- The codex-harness and claude-harness skills.
- flow commits bbf5fa1, 0c19364, d685a21 and d864f54.
