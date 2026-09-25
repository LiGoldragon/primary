# field-clj gaps 6–8 — receipt

Repository: LiGoldragon/field-clj, `main`. Base `df4ac6d` (gaps 1–4). Worked in a fresh clone in the subflow scratchpad (`field-clj-g678-opus`), under Orchestrate lock 6391. `flake.nix`, `deps.edn` and the Nix files were not touched; D2 had pushed nothing to `main` at either push.

## Revisions

- `fb050bd4ed79144023c139e63e6cc86c042215dd`: code and tests, pushed with `git push`.
- `8c5b0cecd907164276572985b77bba4fdfaf7bd1`: README. field-clj landed this commit itself, run from `src/` with `FLOW_ID=38de5b` and the input `#commit ["Document the datom-emulating input and output, traits and caller\n\nCo-Authored-By: …" ["README.md"]]`. It printed `#success ["38de5b" "8c5b0cecd907164276572985b77bba4fdfaf7bd1" ["README.md"] :main :pushed :present]`. `git ls-remote https://github.com/LiGoldragon/field-clj refs/heads/main` returns `8c5b0cec…`. The description ends with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` and then `Flow: 38de5b` in the same trailer block. The commit holds `README.md` only.

## Tests

- Before: 21 tests, 89 assertions, 0 failures.
- After: 33 tests, 163 assertions, 0 failures, with `clojure -M:test`. There are three suites: `core-test` (the jj traits over a fake runner, plus parsing and caller checks), `commit-test` (a fake for each trait) and `repo-test` (real repositories, now including the `Flow:` trailer on a real commit through `core/output`). Every output a test produces is checked with `schema/valid-output?`.
- Mutation checks:
  - Dropping the trailer gives 10 failures.
  - Dropping the flow position from `#success` gives 24 failures and 7 errors.
  - Disabling the restore gives 16 failures.
- Not run: `nix flake check` (D2's area).

## Choice for the remote URL (gap 6)

It is a second variant, `#commit-to [message [path ...] remote-url]`, which mirrors the datom `CommitTo.{ message [path ...] url }`. The URL was not made an optional third position, because datom has no omittable positions yet. The old forms `commit [...]`, `commit "m" [...]` and `{:remote-url …}` are refused as `:invalid-command`, with no compatibility path.

## Input, whole

```
#commit    [message [path ...]]
#commit-to [message [path ...] remote-url]
```

Exactly one form, and `FLOW_ID` set in the environment.

## Output, whole

```
#success [flow commit [path ...] :main :pushed :present]

#refused :no-caller
#refused #invalid-caller flow
#refused #input [flow InputReason]
#refused #<stage> [flow Reason stderr old-main new-main remote-id local-commit Restoration Divergence]

InputReason  = :invalid-edn | :invalid-command | :invalid-paths | :expected-one-argument
Restoration  = nil | #restored operation | #restore-failed [operation stderr]
Divergence   = [[url remote-id] ...]
stderr, old-main, new-main, remote-id, local-commit = string or nil

#root     :root-failed
#remote   :git-root-failed | #push-url-failed remote | #unverifiable-remote [remote push-url] | :remote-mismatch
#scope    :diff-failed | #missing-paths [path ...] | :committed-diff-failed
          | #committed-path-scope-mismatch [[expected ...] [committed ...]]
#commit   :operation-log-failed | :commit-failed | :local-commit-id-failed
#bookmark :bookmark-failed
#push     :push-failed
every stage: #fault "text"   (an exception, such as a missing jj, or a broken trait signature)
```

Every evidence key that gaps 1–4 added is now a position:

- `:stage` is the tag.
- `:reason`, `:stderr`, `:old-main`, `:new-main`, `:remote-id` and `:local-commit` are positions 2–7.
- `:restore`, `:restored-operation`, `:restore-target` and `:restore-stderr` are the `Restoration` variant.
- `:divergence` is position 9.
- `:missing`, `:expected`, `:committed`, `:remote` and `:push-url` are the data of their reason tags.

The schema validates the output before it is printed. An output that broke the schema would not be printed: the process would write to stderr and exit 2. Exit status is 0 for `#success` and 1 for `#refused`.

## Traits (gap 7)

`src/field_clj/` is now `schema.clj`, `commit.clj`, `jj.clj`, `core.clj` and `remote.clj`. `protocol.clj` was removed.

- `commit.clj` defines four protocols:
  - **Scope**: `locate`, `admit`, `confirm`.
  - **Committer**: `mark`, `commit`, `restore`.
  - **Publisher**: `target`, `advance`, `publish`.
  - **Verifier**: `local-main`, `remote-main`, `verify`.
- Each method returns `[:ok value]` or `[:refused reason stderr]`, and each call is checked against its `[args result]` signature in `schema/Traits`.
- A short-circuit pipeline runs the calls in order: locate, target, local-main, admit, mark, commit, confirm, advance, publish, verify.
- `jj.clj` implements all four protocols over the injectable runner `(run dir & args)`.
- The 16 original core tests keep their meaning, rewritten against positional output through a test-only view (`test/field_clj/support.clj`). The 5 real-repository tests keep theirs too.
- `commit-test` covers each trait through a fake: Scope refuses and stops the pipeline before the Committer, Committer refuses with nothing to restore, Publisher refuses and restores through the Committer, Verifier reports a mismatch, and a result that breaks a signature gives `#fault`.

## Caller (gap 8)

- `FLOW_ID` is read from the environment.
- Unset or empty gives `#refused :no-caller`, before anything is read or run.
- An id outside `[A-Za-z0-9._-]+` gives `#refused #invalid-caller "<id>"`.
- The description gets the trailer `Flow: <id>`. It joins the message's closing trailer block when there is one; otherwise a blank line comes first.
- The id is the first position of `#success`, of `#input` and of every stage refusal.

## Proposed sentence for Curriculum `skills/file-editing.md` (not edited)

Replace line 23 with:

> `FLOW_ID=<id> field-clj '#commit ["message" ["path" ...]]'` runs this landing under one rule: it commits exactly the named repository-relative paths with a `Flow: <id>` trailer, leaves other dirty paths uncommitted, refuses when `FLOW_ID` is unset, when a named path is clean, or when `jj diff -r @- --name-only` differs from the named set, and prints one positional variant, `#success [flow commit [path ...] :main :pushed :present]` or `#refused …`.
