# Flow 0.17.3 Home Stage — Recheck of Three Review Points, and Mind Astra Status

Recheck of the stage review at flows/8904b1/witnesses/flow-0173-stage-review.md
(stage revision fccc26523589c9b40cd1aa1479e63c571fa4c061, branch
flow-0173-stage-56ae53-5ba2e1e), asked because three of that review's points
rested on less than direct remote/derivation evidence.

## 1. Remote itself, now

**Observed** (2026-09-26, via `git ls-remote ssh://git@github.com/LiGoldragon/CriomOS-home`,
queried live against the forge, not a local clone's remembered refs):

    fccc26523589c9b40cd1aa1479e63c571fa4c061  refs/heads/flow-0173-stage-56ae53-5ba2e1e
    5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc  refs/heads/main

**Method:** direct `git ls-remote` against the repository's own SSH URL (from
`git remote -v` in /git/github.com/LiGoldragon/CriomOS-home), not a cached
`remotes/origin/*` ref.

**Verdict:** confirms the review's claims. The stage branch exists on the
remote at exactly fccc265..., and Home main on the remote is still at
5ba2e1e..., unmoved. No discrepancy found.

## 2. The Messenger pin

**Observed:** read flake.lock at both revisions directly from git
(`git show <rev>:flake.lock`). Relevant nodes, identical at both revisions:

- `message` input: rev 930c5169ffcf5fa3784b34b2751763009e926d1d
- `message-next` input: rev 481b579fcf72797ffa9ccf8ce4e2283a58cdff97
- `messenger-clj` input: rev 93c12756f9c00dd3c13762590f17cee3a3712530

Also read flake.nix comments at main (5ba2e1e): line ~184 names the `message`
input "Message — the messenger: stateful local messaging daemon..."; line
~105 names `messenger-clj` "Standalone compatibility messenger used by the
live Flow routes." A repo-wide grep for the identifiers the review named
(`stableMessage`, `nextMessage`) at both revisions finds them only in
checks/flow-message-next/default.nix, where `stableMessage = expected field
"930c5169..."` is asserted against `inputs.message.sourceInfo.rev`, and
`nextMessage` against `inputs.message-next.sourceInfo.rev`. `messenger-clj`
is not referenced in that check file at all.

**Method:** `git show <rev>:flake.lock` and `git grep` for the field names,
at both the main and stage revisions, no build or evaluation.

**Verdict:** this is a different field, not a slip and not a real pin
change. There are two distinct flake inputs that can each be called "the
Messenger": `message` (930c5169..., what the repository's own comment calls
"the messenger," and what the check code's `stableMessage`/`nextMessage`
assertions gate) and `messenger-clj` (93c12756..., a separate "standalone
compatibility messenger" package). The review's "930c5169" is the `message`
input; my belief of "93c12756" is the `messenger-clj` input. Both are
independently confirmed unchanged between main and stage (identical rev in
both flake.lock reads above), so the substantive claim — the Messenger and
Message-next pins are retained — holds either way. The naming ambiguity does
not itself justify a hold, since both candidate "Messenger" pins are
unchanged.

## 3. The package output

**Observed:** the check log (flow-0173-full-check-1.log:194-195) names the
derivation path /nix/store/28c0x4j91pyv528jgq37qd5ci69aqhz2-flow-message-next.drv
for the `checks.x86_64-linux.flow-message-next` attribute. That .drv file
exists in the local store. Reading its content directly (`nix derivation
show`, a read of an existing file — no build, no evaluation) gives:

- `outputs.out.path` = `msqnddfrxzfrg48yaw32cjdivp5lvlq4-flow-message-next`
  — an exact match to the disputed store path.
- Its input derivations include `4c0pq7biq5n8yay15j3p1lih42wgj9n5-flow-0.17.3.drv`
  and its build script invokes `/nix/store/qxf524wk1dwyfs26qmpsd9frsrvci88g-flow-0.17.3/bin/flow-nexus`
  as "Next Flow" — tying the derivation to Flow 0.17.3, consistent with this
  stage (the stage is the one pinning flow-next to Flow 0.17.3 at 0b512ee0).

**Method:** located the .drv the check log names, confirmed it exists on
disk, and read its stored content (`nix derivation show`) rather than
matching store-object mtimes. No build, evaluation, or check was run.

**Verdict:** established properly, without a build. The store path
msqnddfrxzfrg48yaw32cjdivp5lvlq4-flow-message-next is the declared `out`
output of the exact derivation the check log names for this stage's
`flow-message-next` check, and that derivation's own inputs name Flow
0.17.3. The review's time-matching method was weaker than necessary, but
the underlying tie is real and now shown directly from derivation content.

## 4. Mind Astra's status (read-only)

**Observed**, from Mind Astra's pane (w1:p2, "MindV2.{ Astra 6fe957 }") as
displayed, read via `herdr pane read` (no input sent):

- The visible scrollback (buffer runs out above this point, so earlier
  turns are not visible) shows Astra received a hold instruction whose
  tail reads: "...reconciliation: .../flow-0173-stage-review.md. Do not
  move on this seat's witness alone. This seat will send the recheck's
  result. The gate stays yours; no activation."
- Astra's reply, exact words: "I'll keep the hold. The log read supports
  that the check printed success, but it does not establish the terminal
  result. I'll incorporate the three recheck points—real remote identity,
  the Messenger pin discrepancy, and the package output's link to this
  stage—before treating the gate as green. No move or activation is
  authorized on the current evidence."
- A later inbound message (`#msg` from "56ae53"), the "Flow-only release
  brief," told Astra: "...Please own final Flow-stage gate review and
  protected FF of Home main with real remote readback once your own check
  clears. This is separate from Messenger integration. No activation or
  deployment has happened."
- Astra's reply, exact words: "I own the final Flow-stage review and
  protected fast-forward. The source scope is confirmed; I'm closing the
  remaining evidence questions about the real remote, retained Messenger
  pin and exact derivation-to-output link. Fable's evidence hold remains
  in place until those findings are reconciled. No activation or
  deployment is included."
- Pane status line currently reads "Working."

**Observed**, from the lock service (`orchestrate 'Observe.Locks'`, listing
only, no lock action taken): the current lock set has no lock owned by
FlowId 6fe957 (Mind Astra) anywhere in it. The only lock touching this
stage's paths is 7815 `HomeFlow0173Validation56ae53`, owned by 56ae53 (this
flow's owner), not by Astra.

**Observed**, from the remote (see point 1, same query): Home main is still
at 5ba2e1e2bd4e9fa045e1773e74d5822beb67e7fc — unchanged, not fast-forwarded
to fccc265....

**Inference:** the "Flow-only release brief" (which told Astra to "own
final Flow-stage gate review and protected FF... once your own check
clears") is plausibly the message the brief calls "the gate-opening
message," since it is the message that hands Astra ownership of the move —
though the pane buffer does not show far enough back to see an earlier
message using the words "the move is open to it" verbatim, if one exists
separately.

**Verdict:** Astra has received at least one message opening the gate to
it, has explicitly held pending the same three points this recheck covers,
holds no lock for the move, and Home main has not moved.

## Overall

On this evidence: no reason to tell Mind Astra to hold — it is already
holding on its own initiative, pending exactly these three points, and this
recheck resolves all three in the stage's favor (point 1 confirmed as
reported; point 2 is a naming difference between two inputs, not a pin
change, and both are unchanged; point 3 is now tied to the stage without a
build). Home main has not moved and Astra holds no lock for the move.

## Method summary

- `git remote -v` and `git ls-remote <ssh-url>` against the live forge for
  point 1.
- `git show <rev>:flake.lock` and `git grep` across both revisions for
  point 2.
- `nix derivation show` (a read of existing store content) on the .drv the
  check log names, for point 3. No build, evaluation, or check invoked.
- `herdr pane list` / `herdr pane read` (display read, no input sent) and
  `orchestrate 'Observe.Locks'` (listing only, no lock action) for point 4.

## Sources

- ssh://git@github.com/LiGoldragon/CriomOS-home (queried live)
- /git/github.com/LiGoldragon/CriomOS-home (local clone, for `git show`/`git grep` at fixed revisions)
- /home/li/wt/github.com/LiGoldragon/CriomOS-home/flow-0173-validation-56ae53/flow-0173-full-check-1.log
- /nix/store/28c0x4j91pyv528jgq37qd5ci69aqhz2-flow-message-next.drv
- herdr pane w1:p2 ("MindV2.{ Astra 6fe957 }"), read-only
- `orchestrate 'Observe.Locks'`, read-only listing
- flows/8904b1/witnesses/flow-0173-stage-review.md (the review under recheck)
