# Second witness — Home Messenger 0.2.6 step, gate 5 pre-check

Flow: 8904b1 (Psyche Fable). Subject: Mind Astra 6fe957's gate 1-4 report on
Home main -> home-messenger-pin-6fe957. Read-only witness only; no branch,
build, check, or push performed by this seat.

## Repositories used (public remotes, fetched fresh)
- /git/github.com/LiGoldragon/CriomOS-home  (`origin` = ssh://git@github.com/LiGoldragon/CriomOS-home)
- /git/github.com/LiGoldragon/messenger-clj (`origin` = ssh://git@github.com/LiGoldragon/messenger-clj.git)
- `git fetch origin main home-messenger-pin-6fe957` and `git fetch origin main` run in each, immediately before inspection.

## Point 1 — candidate exists on the real remote branch
`git ls-remote origin home-messenger-pin-6fe957` -> `5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc refs/heads/home-messenger-pin-6fe957`.
Matches the reported candidate exactly. BEARS OUT.

## Point 2 — what it changes relative to its base; nothing but the Messenger pin
`git diff fed500843629c828a91fa0e06b9946b69c167898 5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc`:
- `flake.nix`: one line, `messenger-clj.url` rev `dfcf91f0...` -> `93c12756f9c00dd3c13762590f17cee3a3712530`.
- `flake.lock`: the `messenger-clj` locked entry (same rev), and the `clj-build`
  locked entry moves `01126ad4...` -> `8cc9991fcb840636215bf829ca6ed9489e3071d7`.
  Checked messenger-clj's own flake.lock at 93c1275: it pins `clj-build` to
  exactly `8cc9991fcb840636215bf829ca6ed9489e3071d7` (clj-build is not set to
  follow nixpkgs inside messenger-clj). The clj-build lock movement in Home is
  therefore the required transitive consequence of the single declared input
  bump, not an independent change. Commit message: "Home: pin messenger-clj
  0.2.6 determinism successor". BEARS OUT — one declared input changed; the
  lock's second entry is that change's own dependency closure, not a
  separate edit.

## Point 3 — base is the present head of Home main; fast-forward possible now
`git rev-parse origin/main` -> `fed500843629c828a91fa0e06b9946b69c167898`, equal
to the candidate's parent and to the reported base. `git merge-base
--is-ancestor origin/main 5ba2e1e2b...` succeeds. BEARS OUT: fast-forward is
possible right now, as of this fetch.

## Point 4 — pinned Messenger revision is the one named and is on producer's real main
`git cat-file -t 93c12756f9c00dd3c13762590f17cee3a3712530` -> commit.
`git merge-base --is-ancestor 93c12756... origin/main` in messenger-clj succeeds;
`git branch -r --contains` lists `origin/main`. Commit message: "Pin clj-build
8cc9991 for deterministic dependency fetch", dated 2026-09-26. BEARS OUT.

## Point 5 — each log exists, names this candidate/input, runs the gate's check, ends passing
Logs read from the lead checkout `/home/li/primary/flows/6fe957/reports/logs/`
(paths as given, relative to that checkout — both present).

- `messenger-ifd-gate3-5ba2e1e-20260926.log` (28242 bytes, mtime 19:58): evaluates
  flake `path:/home/li/wt/github.com/LiGoldragon/CriomOS-home/home-messenger-pin-6fe957`
  with the `system` input supplied from
  `/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/system`,
  evaluates all packages/checks (binary-cache timeouts are non-fatal, local
  builds proceed), ends `all checks passed!` with only an aarch64-linux system
  omission noted (not a failure/skip of a checked system). No failed or
  skipped check found in the body.
- `messenger-package-gate4-5ba2e1e-20260926.log` (5765 bytes, mtime 20:22):
  same flake path/system input; builds `messenger-clj-uberjar`,
  `messenger-clj-0.2.6`, then `messenger-clj-home-package`; the middle
  derivation's `installCheckPhase` runs `--help`/`hm-repair --help` checks
  (their usage banners appear, consistent with success — a failing `grep`
  there would abort the whole build) and phase completes; log then shows the
  final derivation starting to build with no error afterward.

Independent, out-of-band corroboration (not requested by the report, sought to
disconfirm it): the jj-managed worktree at
`/home/li/wt/github.com/LiGoldragon/CriomOS-home/home-messenger-pin-6fe957`
(the exact directory named in both logs) has its working-copy commit's parent
at `5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc` (jj `commit_id`), zero working
changes (`jj diff -r @ --stat` = 0 files), confirming the checkout really was
the named candidate when the logs were produced. A `result` symlink in that
same directory, dated **2026-09-26 20:22** (matching gate4's log mtime to the
minute), resolves to `/nix/store/2sfhrajamgv96hdbzpm15m321pns7bxs-messenger-clj-home-package`
— an empty regular file (standard Nix "check passed" marker; a failing build
produces no `$out` and no `result` link). This is independent, read-only
proof that gate 4's build actually completed and passed, closing the gap left
by the log's own text (which shows the last build starting but not an
explicit "succeeded" line).

Also checked the "ten command names" claim independently: messenger-clj
commit 93c12756's `nix/package.nix` lists exactly ten:
`send send-abrupt list register repair deregister rebind move retire
heartbeat-state`, each linked as `hm-$command`. BEARS OUT.

## Overall
Every material point in Mind Astra's gate 1-4 report bears out under this
second, read-only witness; nothing material contradicts it; nothing was left
unsettled after the jj/result-symlink corroboration for gate 4.

## Part 2 — delivery to 6fe957

Route check immediately before send: `FLOW_ID=8904b1 flow 'List.{}'` showed
6fe957's row `{ 56ae53 default meta-bind-existing } Pending` (control socket
Unavailable, messenger route Available in the `default` session); `FLOW_ID=8904b1
hm-list` showed `6fe957 mind-astra-6fe957 default done` — same live pattern as
this flow's two prior successful sends to 6fe957. Judged live; sent.

One send:
`FLOW_ID=8904b1 hm-send 6fe957 "Ruling.«...»" --wait-presented`

Receipt printed: `Presented.{ 6fe957 done }`.

`herdr pane read --session default w1:p2` immediately after showed the exact
sent datom rendered verbatim in the pane's `#msg` line — landed body matches
the submitted bytes exactly, no truncation or mangling.

Within under a minute, 6fe957 replied (exact words):
> I withheld the move because the preceding instruction required a report
> before any fast-forward. This ruling clears that checkpoint.
> I'll delegate the fast-forward after verifying Home main is still at the
> witnessed base. If it has moved, the worker will stop. After remote
> verification, it will hand the immutable source to Field for acceptance. No
> activation is authorized.

This is a Read/reply witness (content-specific, not generic): it states its
reason for withholding (an earlier standing instruction to report before any
fast-forward, now cleared by this ruling), and restates the fast-forward,
stop-if-moved, and handoff-to-Field conditions correctly. No activation
claimed or authorized by it.

