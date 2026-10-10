# Home messenger pin follow-up

Date: 2026-09-26. Scope: the requested lock-only Home input follow-up. No
bootstrap input, deployment, activation, service, or CriomOS source was changed.

## Current consumer and producer evidence

`CriomOS-home` real remote `main` resolves to
`657f4ba8167132a70357a4326532bcda2416b789` (subject: `field-clj: pin
3e5f450 (clj-build 8cc9991, deterministic deps FOD)`). Inspection of that
immutable revision establishes that it still declares and locks
`messenger-clj` at `dfcf91f0ff8b4b8a5bb6edc18830fdc2d0323494`; its nested
`clj-build_2` lock remains `01126ad41b8f06ebd1469db30e89efc7dc74b649`.

The producer remote was inspected through GitHub's commit and file endpoints.
The requested successor is the full immutable commit
`93c12756f9c00dd3c13762590f17cee3a3712530`, whose remote subject is `Pin
clj-build 8cc9991 for deterministic dependency fetch`. Its `flake.lock` pins
`clj-build` at `8cc9991fcb840636215bf829ca6ed9489e3071d7`. This is the
lock-only successor of the existing consumer, rather than the incompatible
earlier 0.2.6 line that recorded `01126ad`.

The requested `0.2.6` label is historical producer/report evidence; the source
flake inspected here exposes package names but no release-version string. No
new producer build or test was run. Earlier reports' claim of 53 passing tests
and a Prometheus build is therefore not treated as a fresh validation receipt.

## Ownership and handoff

`flows/b7ba00/log.md` records that Fable stopped Home-main work and handed its
Home integration branch (`integration-b7ba00-home` at `b8b45e2f`) and the
second-deploy gate to Field Sol `b7da5d`; its branch was explicitly
main-untouched pending a system-override check. This is the latest explicit
step-2 owner transfer found. It means this flow must not create a duplicate
consumer pin.

The live Messenger route record still names `b7da5d` as bound at
`messaging-build/wQ:pT`, but `hm-list` reports that row `STALE`. With
`FLOW_ID=6fe957`, the exact handoff was submitted to that route with the full
current consumer revision, existing pin, successor revision, clj-build
provenance, and scope boundary. Messenger returned:

```
Held.{ b7da5d RepairRequired 5b8c0596-8495-4edb-80bc-1c9309afa860 } candidates=[]
```

Receipt grade: **held, not presented or delivered**. The message was not sent
to a substitute recipient because no later live step-2 owner was evidenced.

## Remaining gates

The owner must repair or replace the stale exact route before accepting the
handoff, then update only the Home `messenger-clj` input and generated lock to
`93c12756f9c00dd3c13762590f17cee3a3712530`, preserving the field-clj and
next-service pins already on its integration line. It still needs the
appropriate system-override check and an owner-scoped build receipt. No version
increment decision is due from this non-mutating handoff.

## Superseding step-2 ruling and isolated implementation

Psyche Fable `8904b1` later appointed this flow (`6fe957`) the sole Home
step-2 owner. That ruling supersedes the historical Field handoff above. The
first direct acceptance submission to Fable was
`Uncertain.{ 8904b1 attempt-25cde1b6-765 }` after its agent-status wait timed
out. A later read of Fable's own log records the exact acceptance body as
received and marks the ownership accepted; the original Messenger transport
receipt remains uncertain rather than upgraded to presented/read.

An Orchestrate reservation was acquired before edits:

```
Locked.{ 7694 HomeMessengerPinStep2_6fe957 6fe957 [ /home/li/wt/github.com/LiGoldragon/CriomOS-home/home-messenger-pin-6fe957 ] ... }
```

The isolated worktree starts from current Home remote main
`657f4ba8167132a70357a4326532bcda2416b789`. Its review branch and real remote
bookmark now resolve to the same immutable commit:

```
home-messenger-pin-6fe957@origin = 3991923ac2c1be2bb6c661da29401efb5d804d7b
```

That commit changes only `flake.nix` and `flake.lock`: messenger becomes
`93c12756f9c00dd3c13762590f17cee3a3712530`, with content hash
`sha256-OZ23SBVdFU97nA7FbqWP9b6u6bgnBYr6udw6xiqMzJM=`, and its nested clj-build
becomes `8cc9991fcb840636215bf829ca6ed9489e3071d7`. It makes no bootstrap,
activation, release, tag, service, or unrelated pin change. The producer is
untagged; source inspection establishes package version `0.2.6`.

A temporary Flow 0.17.3 update was prepared after an intervening instruction,
then removed from this uncommitted branch when Fable ruled Flow rollout outside
this assignment. The committed branch contains no Flow pin change.

## Current gates and exact blockers

The required full Home no-build check was invoked with the explicit immutable
system input
`path:/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/system`.
It reached flake evaluation (`__functor`, `homeModules`, `lib`, `packages`) but
did not terminate within a bounded 55 seconds; it was interrupted by that
bound. It is **pending, not green**. The required Home-owned
`messenger-clj-package` build was not started because the preceding ordered
no-build gate is not green. Therefore main was not moved.

Read-only builder probes establish configuration from `/etc/nix/machines` as
`ssh-ng://nix-ssh@prometheus.goldragon.criome`, with `max-jobs = 0` and identity
path `/etc/ssh/ssh_host_ed25519_key` (mode `0600`, root-owned). A 20-second
`nix store info` probe produced no authentication result before timing out. The
historic report of authentication failure is not reproduced by this probe; the
current exact failure is an unfinished remote-store handshake. No credential,
authorization, or Nix configuration change was made.

Fable received a distinct gate report at `attempt-bc9abd9f-520`; it too returned
`Uncertain` after waiting for agent status. No duplicate acceptance or route
test was sent.

## Correction: evaluation observation was not a terminal result

The earlier 55-second result was a tool-observation timeout, not a Nix
terminal. The original Home no-build process remains live as PID `252948`,
started at 19:20:20 in the isolated workspace, with exact argv:

```
nix flake check --no-build --impure --no-write-lock-file \
  --override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/system
```

Its related `nix-daemon 252948` process is PID `252965`. At passive observation
the check process was sleeping with CPU activity and no descendant derivation
builder was present; its argv has `--no-build`. It was started without the
later IFD/build guard options, which are not claimed retroactively. No retained
PTY/session handle exists for its stdout, so only exact-PID passive observation
is available until it exits.

A later duplicate, started by this flow under session `94679`, was PID
`265590` with a 240-second shell timeout and explicit IFD/build guards. It had
already exited before cleanup could address it; no signal was sent, avoiding
PID-reuse risk. An empty poll of its retained session recovered terminal exit
`124`: its no-build evaluation spent the bounded run timing out while fetching
Prometheus-cache `.narinfo` metadata, then its timeout wrapper interrupted it.
That is cache reachability evidence, not a derivation build or SSH
authentication receipt. The original was never stopped or modified.

A later exact ancestry observation of the original found one child,
`git ls-remote --symref https://github.com/LiGoldragon/signal-message.git`.
This is source-input resolution activity. No derivation builder was present at
that observation; no claim is made about activity outside that exact moment.

The original PID `252948` and its associated daemon PID `252965` later exited.
Its initial non-PTY execution response supplied no session ID or redirected
output path, so the terminal exit status and final Nix text cannot be recovered.
Termination is witnessed; the no-build gate's outcome is **unknown, not
green**. No replacement evaluation was launched.

Fable subsequently established that `3991923a` is two commits behind current
Home main `fed50084`. Even a terminal result from the live original covers the
old candidate only. A Messenger-only rebase or rebuild from current main, its
own lock and one fresh gate run remain required before any main move; no such
mutation has begun.

## Current-base Messenger candidate and fresh gate 3

The Messenger-only commit was rebased onto the contemporaneously verified Home
remote main `fed500843629c828a91fa0e06b9946b69c167898`. The result is
`5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc` on
`home-messenger-pin-6fe957` (the same revision observed through its remote
bookmark). Its diff against current Home main remains only `flake.nix` and
`flake.lock`, carrying Messenger
`93c12756f9c00dd3c13762590f17cee3a3712530` and nested clj-build
`8cc9991fcb840636215bf829ca6ed9489e3071d7`.

Lock `7734` covered the isolated workspace for that rebase and one fresh gate;
it was released after the terminal result. The frozen system input was again
`path:/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/system`,
with `lastModified=1790465761` and
`narHash=sha256-KW3DUTifDJ6m2JuYiTVtJz+9ieAgqjCb46wgrMqxJJU=`.

The one retained-session gate used session `91871`, a 240-second process bound,
`--no-build`, `max-jobs = 0`, no builders, and
`allow-import-from-derivation = false`. It exited **1**. It first recorded
bounded Prometheus-cache metadata/content timeouts. The decisive terminal gate
is structural: while evaluating Home's `checks`, Nix requires
`/nix/store/mmdwbyjfhr3qkbvbzan9mb3lawkcaqq3-herdr-config.toml.drv^out` and
refused because IFD was disabled. Thus this check set intrinsically requires
IFD; it cannot complete under the no-IFD safety condition. IFD was not enabled.

Gate 3 is blocked and red, not green. The Home-owned Messenger package build
was not started because the ordered preceding gate failed. No main move,
activation, Flow change, bootstrap change, tag, or release was performed.

The exact Gate 3 report was delivered to the current Fable binding `8904b1`;
the receipt is `Presented.{ 8904b1 done }`. The remote bookmark for the
candidate was subsequently witnessed at
`5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc`.

## Authorized local-IFD rerun

Following explicit local-IFD authority from `56ae53`, and after confirming the
candidate and the frozen system override remained unchanged, one and only one
replacement Gate 3 run was started. The required IFD boundary is
`pkgs.writeText "herdr-config.toml"`: it interpolates the local stable and
next Codex client wrapper paths. No model-bearing dependency was identified at
that boundary.

Retained PTY session `33785` ran `nix flake check --no-build --keep-going
--impure --no-write-lock-file` on candidate
`5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc`, using the same system override
(`lastModified=1790465761`,
`narHash=sha256-KW3DUTifDJ6m2JuYiTVtJz+9ieAgqjCb46wgrMqxJJU=`), local builders
only, `max-jobs=2`, `cores=2`, and a 600-second process limit. IFD was
intentionally enabled under that authority. Its actual terminal was **exit
0**, ending `all checks passed!` (with `aarch64-linux` omitted). Durable
complete output is `reports/logs/messenger-ifd-gate3-5ba2e1e-20260926.log`.
Prometheus-cache NAR/narinfo requests timed out and the cache was disabled by
Nix; the completed evaluation used available local paths.

The Home Messenger package check remains **not started**. The ordered Gate 3
is green, but the local-IFD exception did not authorize a local full-package
build; the authorized package route is Prometheus-only and its cache/store path
was unavailable. No additional probe or retry was made. Main move and
activation remain withheld.

This completed Gate 3 / package-blocker report was sent to `8904b1` using the
existing binding; receipt: `Presented.{ 8904b1 done }`.

## Authorized local Gate 4 package check

`56ae53` subsequently gave a one-package local-build exception after the
witnessed Prometheus route failure. Gate 3's retained-session terminal (`33785`,
exit 0) and the unchanged candidate/system-input witness were reconfirmed; the
full flake check was not rerun. The check source fixes the demanded contract:
Messenger input `93c12756f9c00dd3c13762590f17cee3a3712530`, its
`messenger-clj` executable, and all ten compatibility commands (`hm-send`,
`hm-send-abrupt`, `hm-list`, `hm-register`, `hm-repair`, `hm-deregister`,
`hm-rebind`, `hm-move`, `hm-retire`, `hm-heartbeat-state`) from one closure.

Exactly one retained-PTY local build, session `67580`, built only
`.\#checks.x86_64-linux.messenger-clj-package` with the same frozen system
override, `--impure`, `--no-write-lock-file`, local builders only,
`max-jobs=2`, `cores=2`, and a 600-second bound. The actual terminal was
**exit 0**. It realized the supplied check derivation
`/nix/store/24ad0v1vppg90wv3k5j4lmsjj59bwkfz-messenger-clj-home-package.drv`,
after `messenger-clj-uberjar` and `messenger-clj-0.2.6`. No other package or
whole-flake build was started. Its durable output is
`reports/logs/messenger-package-gate4-5ba2e1e-20260926.log`.

The observed Prometheus cache timing out preceded the local realization. No
model-weight dependency was identified in the package/check closure. Gate 3
and this Gate 4 are green; main move and activation remain withheld pending the
separate authorized decision.

The combined Gate 3 / Gate 4 witness was delivered to Fable `8904b1` through
the existing binding; receipt: `Presented.{ 8904b1 done }`.

## Gate 5 protected fast-forward blocker

Before mutation, the real Home remote still reported `main` at
`fed500843629c828a91fa0e06b9946b69c167898` and
`home-messenger-pin-6fe957` at
`5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc`; local revision-set evidence also
showed the former as an ancestor of the latter. The retained Gate 4 terminal
was independently recovered as exit 0 (session `67580`); the durable Gate 4
log records the exact package derivations it realized.

The required write coordinator nevertheless rejected both a `6fe957` and a
unique `6fe957-home-messenger-gate5` lock request with the same unrelated
response: `LockRejected.DuplicateName.{ 1805 Name cf7879 ... }`. No lock was
acquired. Therefore no `main` bookmark was changed or pushed, despite the
otherwise valid fast-forward precondition. No activation was performed.

The Gate 5 blocker was delivered to Fable `8904b1`; receipt:
`Presented.{ 8904b1 done }`.

## Gate 5 completed fast-forward

The corrected lock request used the supported positional form
`Lock.{ <LockName> <FlowId> [ <paths> ] <reason> }`, rather than the prior
malformed field-label form. It acquired `Locked.{ 7775
home-messenger-main-6fe957 6fe957 [ /home/li/wt/github.com/LiGoldragon/CriomOS-home/home-messenger-pin-6fe957 ] ... }`.
While it was held, the real Home remote was re-read at
`fed500843629c828a91fa0e06b9946b69c167898`. `main` was moved only forward to
`5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc` and pushed without force. Both a
real-remote API readback and `main@origin` then returned that exact candidate.
The lock was released with `Released.{ 7775 ... }`.

No source, tag, bootstrap, Flow, or activation change accompanied the move.
The first post-move Fable report attempt is retained as
`Uncertain.{ 8904b1 attempt-8f2b737a-7d6 }`: its wait for agent status timed
out, so it is transport-uncertain rather than a delivery or acceptance claim.

The immutable-green handoff was then submitted once to the current `9ac67c`
binding, requesting an explicit target acceptance. Its result is likewise
`Uncertain.{ 9ac67c attempt-830f44b5-256 }` because the agent-status wait
timed out. It is not an acceptance receipt; no duplicate send or route probe
was performed.

## Passive reconciliation of the Gate 5 and Gate 6 attempts

The Fable attempt `8f2b737a-7d6` has a stronger passive witness than its
original `Uncertain` transport grade: the current target-side Fable log at
`/home/li/wt/primary/56ae53/flows/8904b1/log.md` records the full `Gate5.{ ...
Lock.Id.7775 ... Main.Before.fed50084... After.5ba2e1e... }` body under
“gate 5 reported passed by Mind Astra 6fe957”. This is a target-side transcript
witness that Fable received/read the report; it is not an additional send.

For Field attempt `830f44b5-256`, current available `9ac67c` target-side logs
contain no matching immutable-green handoff, candidate revision, attempt ID,
or explicit `Accepted` response. `hm-list` passively reports its current
binding as `9ac67c / field-sol-9ac67c / default / idle`, which does not itself
prove delivery or acceptance. The strongest Field grade remains **Uncertain**;
the remaining Gate 6 requirement is Field's explicit acceptance of immutable
green source `5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc`. No resend, route test,
or binding change was performed.
