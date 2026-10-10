# Item 6 on the set

Build host: `hostname` returned `prometheus` for every cargo and nix run. The scratch tree is `/tmp/ez-i6` on Prometheus: 07714b0 plus item12-on-item5-ethos-zero.patch, committed as one commit. Its tree is identical to `/tmp/ez-i5` cf1d79f, and `git diff` between them is empty. Item 6 sits on top of that as a second commit. The overrides were protos `path:/tmp/protos-i5`, whose uncommitted diff equals item12-on-item5-protos.patch, and datom-codec `/tmp/datom-codec-item12b` rev 296b256. Nothing was pushed, and nothing in Primary was committed.

## Comments are not carried

Today, ethos-zero drops ethos comments before generation. protos lexes `;` to the end of the line as a comment (protos README line 43). Nothing in ethos-zero `src/` mentions comments.

Witness: running `cargo run -- "Generate.{ …/flow-library.ethos /tmp/i6gen }"` on the edited fixture gives output whose only difference from the old golden is `pub struct FlowId(pub String);`. `grep -c "unideal\|hash-based"` on that output returns 0. In the same way, the `;` header of ethos-zero.ethos does not appear in src/ethos-zero.rs.

So the comment lives only in the ethos source. Carrying it into the generated Rust rests on invariants Proposal 3 (comments). No comment path was built.

## Content

- `fixtures/print/flow-library.ethos`: `FlowId.Integer` becomes `FlowId.String`, with this comment beside it:
  `; the String is unideal:` / `;   a real hash-based id is the target`.
- The brief says the four Flow fixtures each declare FlowId. Only flow-library declares it. flow-signal, flow-operation and flow-memory import it through `flow:[ FlowId Voice Event ]` and use it as `flow::FlowId`, so their source and output are unchanged. No comment was added to those imports.

## Checks

- `cargo test --offline`: all pass. lib 21, main 0, cli 17, ethos 33, flow_contract 1 (inner package 2), freshness 4, generated 20, print 9, signal_without_datom 2. `cargo fmt --check` passes.
- `nix flake check --keep-going` with both overrides: "running 9 flake checks…" and "all checks passed!". The 8 check attributes are build, test, fmt, clippy, doc, dependency-ethos, no-free-functions and no-inherent-methods. The ninth derivation is the package.
- `git apply --check` of item6-on-set-ethos-zero.patch succeeds on a fresh 07714b0 with the set applied.

## Files touched (5, +47 / -17)

- `fixtures/print/flow-library.ethos`: the declaration and its comment.
- `tests/generated/flow-library.rs`: regenerated.
- `tests/flow_contract.rs`: `FlowId(7)` becomes `FlowId("7".to_owned())` twice.
- `tests/generated.rs`: the same three constructions. The `matches!` on `Started(FlowId(..))` becomes `assert_eq!`, because a pattern cannot hold a call. The set's item 1 size test compared `flow_library::FlowId` with `i64`. It now uses `orchestrate::LockId`, so the Integer new type is still covered.
- `tests/print.rs`: the print drops comments, and two tests now pin that loss. The two comment lines are held in the constant `FLOW_ID_COMMENT`.
  - `the_flow_nexus_four_files_round_trip_byte_identical` still requires flow-signal, flow-operation and flow-memory to reprint byte-identical. For flow-library, it asserts that each comment line is present in the source and absent from the reprint.
  - `a_checked_file_prints_as_it_was_written_in_the_canonical_form` makes the same two assertions against `file.print()`.
  - Each absence assertion fails with "invariants Proposal 3 (comments) has landed: …". So these tests fail on the day the print keeps comments. That failure was not witnessed, because Proposal 3 is not built.
  - Beside those assertions, both tests compare flow-library's print byte for byte with its source after the comment span is removed. That span is held in `FLOW_ID_COMMENT_SPAN`: the two spaces, the comment, and its continuation line. Removing it leaves `[ FlowId.String`. If the span is not in the source, the comparison fails.

## Golden diffs

- Fixtures: only `fixtures/print/flow-library.ethos` changes. Its two declaration lines become three: `FlowId.String` and its comment.
- Outputs: only `tests/generated/flow-library.rs` changes, one line: `pub struct FlowId(pub i64);` becomes `pub struct FlowId(pub String);`.
- Every other fixture and every other generated golden is byte-equal. That includes the other three Flow fixtures and their outputs, src/error.rs and src/ethos-zero.rs. The freshness tests pass over all of them.

Patch: /home/li/primary/flows/1d0733/reports/item6-on-set-ethos-zero.patch (one diff on top of the set).

Provenance receipt: unavailable.
