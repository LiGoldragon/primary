# Generated against hand-written Rust, three Nexuses

Before = last commit on origin/main before 2026-11-13 18:00 (local time, as git reads `--before`). Now = origin/main head on 2026-11-14. Each revision was extracted with `git archive` into a scratch directory; no clone was checked out or changed. `git fetch` ran in the clones, which moves remote-tracking refs only. The clones are under /git/github.com/LiGoldragon. Per-repo revisions are in generated-lines.csv.

## How generated files were identified

ethos-zero's output carries no "generated" comment. Every ethos-zero output begins with `#![allow(dead_code, non_camel_case_types, non_snake_case ...)]` followed by `#[rustfmt::skip]`. A .rs file counts as generated when it opens with `#![allow(` and has `#[rustfmt::skip]` within its first 10 lines.

I cross-checked this against every build.rs. Each one reads an .ethos file, runs ethos-zero and asserts the result equals a committed .rs file. The build.rs files name 8 outputs in flow-nexus, 3 in Curriculum, 1 in orchestrate-nexus and 1 in each other crate. No build.rs writes into OUT_DIR, and no `include!` is used. Every output a build.rs names was found by the signature. The signature found no other files, with one exception: `src/herdr/claude_paste.rs` in flow-nexus has `rustfmt::skip` but is hand-written, and the `#![allow(` rule does not match it.

Hand-written means every other .rs file under `src/` (crate `src/` in `crates/*` too), plus build.rs. Any file under a directory named `tests` is excluded, including `crates/flow-nexus/src/tests/`. Lines are tokei "code" lines for Rust (blanks and comments left out). The .ethos count is non-blank lines that do not start with `;`, tests/ fixtures excluded.

## Totals per Nexus

| Nexus | Revision | Generated | Hand-written | Generated share | Ethos lines |
|---|---|---|---|---|---|
| Flow | before | 8693 | 75242 | 10.4% | 1288 |
| Flow | now | 10109 | 78299 | 11.4% | 1435 |
| Curriculum | before | 275 | 1713 | 13.8% | 68 |
| Curriculum | now | 490 | 1825 | 21.2% | 82 |
| Orchestrate | before | 245 | 3774 | 6.1% | 57 |
| Orchestrate | now | 411 | 3944 | 9.4% | 75 |

## Doubts

- **meta-signal-curriculum-nexus.** It is an empty repository: the local clone has no commits, and `git ls-remote` on GitHub lists no refs. It counts as zero at both revisions.
- **signal-curriculum-nexus.** Its first commit is 2026-11-14 01:38, so it has no "before" revision and counts as zero there. Curriculum's generated lines at "before" therefore leave out the contract, and its jump is partly the contract's arrival (319 generated lines).
- **Frozen "before-request-ids" copies in Flow.** These are `flow-ethos-before-request-ids`, `signal-flow-before-request-ids`, `meta-signal-flow-before-request-ids` and `flow-nexus/.../send_tool_before_request_ids.rs`. They are committed copies of earlier generated output with no build.rs. They have the signature and are counted as generated: 3146 lines at both revisions. Without them Flow generated is 5547 before and 6963 now, a share of about 7.0% before and 8.2% now.
- **generated/mod.rs files.** They are 1 to 8 lines of `pub mod` and no build.rs checks them, so they count as hand-written. Moving them to generated would change the totals by a few dozen lines.
- **Curriculum's generated lines fell** (275 to 171 in the Curriculum repo). The same repo gained memory.rs and emission.rs as generated files (+54) and curriculum.ethos itself shrank. I did not look at why, and I did not trace the change to a commit.
- **In-crate test modules.** Files like `src/transport/session/tests.rs` (orchestrate-nexus) and inline `#[cfg(test)]` modules are counted as hand-written, since only `tests/` directories were excluded as asked.
- **Other repos.** curriculum-deploy and the other repos of the same name family were not counted, since the brief named only the three Nexuses' repos.
- **Scope of counting.** Only src/ and build.rs were counted. Examples and checks directories contain no .rs files.
