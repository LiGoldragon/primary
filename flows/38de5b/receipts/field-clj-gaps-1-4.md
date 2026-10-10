# field-clj gaps 1–4 — receipt

Repository: LiGoldragon/field-clj, `main`. Base `9026513c` (D1). Worked in a fresh clone under the subflow scratchpad, Orchestrate lock 6358.

## Revisions

- `d34059e2cd8f4bc316c460aa89ae2e9eed00ebb1` — Exact filesets, repository root, refusal evidence and restore, URL-verified push (code, tests, flake check inputs, `.gitignore`).
- `df4ac6db5ddddabe29efb1702a7fc7b0ae9bbbdf` — README. This commit was landed by field-clj itself, run from `src/` with `README.md` named repository-relative. Output was `:status :success`, and `git ls-remote https://github.com/LiGoldragon/field-clj refs/heads/main` returns `df4ac6db…`.

## Test counts

- Before: 11 tests, 30 assertions, 0 failures.
- After: 21 tests, 89 assertions, 0 failures (`clojure -M:test`: fake-runner `field-clj.core-test` plus real-repository `field-clj.repo-test`).
- Mutation checks: passing bare paths to `jj commit` again gives 13 failures and 3 errors. Disabling `jj op restore` gives 12 failures.
- Not run: `nix flake check`. The check now lists `jujutsu` and `git` as inputs. Whether its sandbox can fetch the Maven dependency is outside this task.

## What changed

- **Gap 1:** each path goes to `jj commit` as `root-file:"<path>"`, with `"` and `\` escaped. The installed jj 0.44 documents `root-file:` in `jj help -k filesets`. Paths with control characters are refused at input. `jj op log -n1` is recorded right before the commit. Any refusal after the commit runs `jj op restore <op>`, and the refusal names it with `:restore` and `:restored-operation`.
- **Gap 2:** `jj root` is resolved from the caller's directory. Every jj and git command then runs there.
- **Gap 3:** every repository-stage refusal carries `:stage`, `:stderr`, `:old-main`, `:new-main` and `:remote-id`, plus `:local-commit` when a commit exists. After a push attempt it also carries `:divergence` when a remote holds the commit that was restored away. Input refusals are unchanged.
- **Gap 4:** the remote is resolved as `git.push`, else the only remote, else `origin`, and passed as `--remote`. The push URL comes from `git remote get-url --push`, and verification is `git ls-remote <url> refs/heads/main`. A local path, `file://`, a loopback host or a gitolite URL is refused before committing unless `:remote-url` is given.
- **`:remote-url` placement:** it is data, as an optional third element of the command: `commit ["msg" ["p"] {:remote-url "…"}]`. The old two-element form is unchanged. The success output is unchanged. Refusals gained keys only.

## Real-repository tests

Each test uses a colocated jj clone of a local bare Git remote.

- The names `all()`, `p(1).txt`, `a file with spaces.txt` and `q"uote\d.txt` are each committed alone while other files stay dirty.
- From `sub/`, `c.txt` is refused and `sub/c.txt` lands.
- A forced sweep of an extra fileset at commit gives a mismatch, a restore, an identical `jj log -r 'all()'`, the files still dirty and the remote unchanged.
- A pre-receive hook rejection gives `:push-failed` with the hook's stderr, a restore, `main` back at its old id and no divergence.
- A local remote with no `:remote-url` is refused before committing.

## Known limit

`jj op restore` restores the whole repository view. An operation another writer makes in the same workspace between the recorded operation and the refusal is undone with it. This is stated in the README.
