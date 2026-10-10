# Witness: review of flow revision d1df667ae9aa84e9085ff06bda73f2932c29e578

Method: read-only. Scratch clone of the real remote
`ssh://git@github.com/LiGoldragon/flow.git` (confirmed as the real remote by
reading `git remote -v` in two existing local checkouts,
`/home/li/primary/flow` and `/home/li/wt/flow-0174-independent-test-407811`,
both showing `origin ssh://git@github.com/LiGoldragon/flow.git`) into
`/tmp/claude-1001/-home-li-wt-primary-56ae53/8904b10d-7f06-4e44-9342-3a8a2d7e17bd/scratchpad/flow-review`,
branch `flow/multiline-observer-test`. No build, no test run, no binary
invoked; only `git ls-remote`, `git log`, `git diff`, `git show`,
`git merge-base --is-ancestor`, `git rev-list --count`.

## 1. Existence on the real remote

`git ls-remote ssh://git@github.com/LiGoldragon/flow.git` returns:

```
d1df667ae9aa84e9085ff06bda73f2932c29e578  refs/heads/flow/multiline-observer-test
d46ace8cf3db22cd07fd4f8083b3c68c4f16a9e7  HEAD
d46ace8cf3db22cd07fd4f8083b3c68c4f16a9e7  refs/heads/main
bc464e5e1b94fcc179af73111f43b69db1f69fc5  refs/tags/flow-0.17.4
```

Observation: d1df667 exists on the real remote, under
`refs/heads/flow/multiline-observer-test`. Main and the 0.17.4 tag are
exactly the hashes named in the brief.

## 2. Ancestry

Observation (via `git merge-base --is-ancestor`):
- f0e5742263ee66bb91e3cabbe1abaa873635355e8 is an ancestor of d1df667.
- d46ace8cf3db22cd07fd4f8083b3c68c4f16a9e7 (main) is an ancestor of d1df667.
- bc464e5e1b94fcc179af73111f43b69db1f69fc5 (flow-0.17.4 tag) is an ancestor of d1df667.
- `git rev-list --count f0e5742..d1df667` = 1. `git log --oneline f0e5742..d1df667` shows exactly one commit: `d1df667 docs: add multiline observer mutation witness`.

## 3. Changed paths

Observation, `git diff --name-status f0e5742 d1df667`:
```
M  receipts/flow-0174-multiline-observer-test.md
```
Only one path changed since f0e5742, and it is the receipt/evidence file. No
source, build, or lock file changed between f0e5742 and d1df667.

Observation, `git diff --name-status d46ace8(main) d1df667` (whole branch vs main):
```
M  crates/flow-nexus/src/herdr/launch.rs
A  receipts/flow-0174-multiline-observer-test.md
```
`launch.rs` is modified relative to main. Read of the diff: every changed
line falls inside the `mod tests { ... }` block that begins at line 1836,
guarded by `#[cfg(test)]` at line 1835 (checked with `grep -n
"#\[cfg(test)\]\|^mod tests"`, and the diff hunks all start after line 1885).
The edits add a helper fn, rewrite one focused test's refusal-oracle body,
and add one new test — no non-test code, no production logic. No
`Cargo.toml`, `Cargo.lock`, flake, or nix file appears in the branch-vs-main
diff (checked with `git diff --name-only ... | grep -iE
"cargo|version|flake|nix"`, empty). So the whole branch is test-file-and-
evidence-only relative to main.

## 4. Is the focused test's text unchanged f0e5742 -> d1df667?

Observation: `git diff f0e5742 d1df667 -- crates/flow-nexus/src/herdr/launch.rs`
is empty. The file containing the test did not change between those two
revisions at all (consistent with point 3: the only change was the receipt
file). Claim of "unchanged" holds for this pair.

## 5. The receipt at d1df667

Read via `git show d1df667:receipts/flow-0174-multiline-observer-test.md`.
Decisive lines, quoted:

- Mutant (hunk, in `prompt_text_matches_intent`):
  ```
  -            .is_some_and(|body| {
  -                format!("{:x}", Sha256::digest(body.as_bytes())) == intent.prompt_sha256
  -            })
  +            .is_some()
  ```
  stated as "The complete production mutation was this one hunk", applied
  after `strip_suffix(&LaunchReceipt::footer_for(...))`, i.e. the footer
  strip/retention step is untouched — only the hash-equality check after it
  is bypassed. Receipt states "The test source and direct-shape logic were
  unchanged."
- Command: `cargo test -p flow-nexus --lib
  herdr::launch::tests::claude_composed_multiline_direct_skill_prompt_is_observed_byte_for_byte
  -- --exact`, run "in a fresh disposable workspace" at revision
  `f0e574263ee66bb91e3cabbe1abaa873635355e8`.
- Exit code: "mutant_exit=101".
- Failing assertion / row: "It exited `101` after the accepted case passed
  and the lone changed-byte first-row case reached `Observed`; its
  `unwrap_err()` panicked on that `Ok` value." Raw output quoted: "called
  `Result::unwrap_err()` on an `Ok` value: Observed(NativeTargetReceipt {
  ... })".
- Never committed/pushed: "The mutant workspace was not committed or
  pushed."
- Timing: "`/usr/bin/time` was unavailable (exit `127`), so no duration is
  claimed."
- Revision the mutant was applied to: f0e574263ee66bb91e3cabbe1abaa873635355e8,
  "in a fresh disposable workspace."
- Who/where: not stated as a person; receipt describes a "disposable
  Jujutsu workspace" methodology throughout (baseline/successor/mutation
  reruns each in "fresh disposable workspace[s]" or "isolated Jujutsu
  workspaces"), with no named operator, host, or toolchain version given.

## 6. Does the receipt's account hold together against the source? (inference, not a witness of the run)

Read of `prompt_text_matches_intent` at f0e5742 (`git show
f0e5742:crates/flow-nexus/src/herdr/launch.rs`, lines 825-830):
```rust
fn prompt_text_matches_intent(text: &str, intent: &PromptDeliveryIntent) -> bool {
    text.strip_suffix(&LaunchReceipt::footer_for(&intent.harness_kind))
        .is_some_and(|body| {
            format!("{:x}", Sha256::digest(body.as_bytes())) == intent.prompt_sha256
        })
}
```
The mutant replaces `.is_some_and(|body| hash(body) == expected)` with
`.is_some()`: after the footer is stripped (footer presence/retention still
checked), *any* body content is accepted, regardless of hash. In the test's
refusal-oracle row, the first row's newline byte is flipped
(`\n` -> `\r`) but the footer is kept intact
(`assert!(changed.ends_with(&footer))` in the test source), so
`strip_suffix` would still succeed under the mutant, `is_some()` returns
true, and the row is treated as matching → the observer's caller would reach
`Ok(Observed(...))` for that lone-changed-byte case instead of the intended
`Err("native Claude first turn loaded no stacked command")`. The test's
first refusal check calls `.unwrap_err()` on that result; `Result::unwrap_err`
on an `Ok` value panics, and a Rust test binary panic yields process exit
101 (a `cargo test` convention consistent with the receipt's other reported
101 exits). Inference: this reading of the code and the test source makes
the receipt's mechanism plausible and internally consistent, but it is an
inference from static reading — I did not run the mutant myself.

## 7. Any mutant content in branch history?

Observation: scanned every commit on `flow/multiline-observer-test`
(`git log flow/multiline-observer-test --oneline`, five commits: d1df667,
f0e5742, 72dd954, da58712, d46ace8) for the file
`crates/flow-nexus/src/herdr/launch.rs` at each commit, grepping the
`prompt_text_matches_intent` body for the mutant's `is_some())` (without
the `is_some_and` hash check). No match in any commit — the mutant text
does not appear anywhere in this branch's committed history, consistent
with the receipt's claim that the mutant workspace was never committed or
pushed.

## 8. What the receipt omits

- No toolchain/compiler version (`rustc`/`cargo` version) is given for any
  of the runs.
- No exact mutant diff context beyond the one hunk shown (no full file, no
  patch header with line numbers, no diff of the surrounding function
  signature) — enough to identify the check but not a complete, applyable
  patch.
- The receipt asserts a passing run on the unmutated revision (the
  "Reproducible rerun" section, baseline/successor at
  0b512ee.../72dd954..., both exit 0) but this is a different revision pair
  than the mutation-sensitivity revision f0e5742; there is no explicit
  "test passes on f0e5742 without the mutant" run recorded alongside the
  mutation-sensitivity section itself (it says "test source and direct-shape
  logic were unchanged" rather than showing a fresh green run at f0e5742
  immediately before mutating).
- No memory bound is stated for any run.
- No host identity (hostname, OS, architecture) is given, only that runs
  happened in "disposable Jujutsu workspace[s]."
- No named operator/agent identity for who ran the commands beyond the
  general Jujutsu-workspace methodology description.
