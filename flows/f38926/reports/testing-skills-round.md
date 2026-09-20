# A round of agent-written testing skills

Five testing skills were authored in the Curriculum skills directory, each
teaching a flow how to prove one thing that failed or was hard in flow f38926's
night, and each tested in a fresh `claude -p` flow against a disposable target.
Authority: the living's standing night instruction (`vision/nightWork.md`),
"testing skills that are agent-written to try and make things work better, so
you do a round of testing skills you can test in next flows and start fresh
flows for everything". Curriculum's `AGENTS.md` requires explicit psyche
approval before changing a skill; the living is unreachable until morning, and
that instruction is the approval this round stands on. Nothing in `Vision/`,
`Intent/`, or an existing skill was changed.

## The five skills

### `testing-push-landed`

Proves that a push actually landed: the local `@-` commit id and the hash
`git ls-remote` returns from the real forge URL must be equal. A zero exit from
the push, and the checkout's own view of its bookmark, prove nothing; a
filesystem or mirror `origin` is not the forge.

### `testing-commit-scope`

Proves that a commit made in a shared working copy landed only this flow's
files, by reading `jj diff -r @- --name-only` after the commit and before the
bookmark is set. A path argument naming a directory sweeps everything under it,
so the check is run even when the commit was made with explicit paths.

### `testing-generated-projection`

Proves that a generated tree matches its authored source: `git status --short`
empty, regenerate, and whatever the second `git status --short` prints is the
drift. This is the one place text comparison is a real test, because the text
is the product. Names the regenerator, the checkout that defines it, and the
roots passed to it.

### `testing-long-run-progress`

Proves whether a quiet long run is progressing: two samples of `/proc/<pid>/io`
across a bounded window, the PID taken from the handle of the process the test
started, never from a command-name or path pattern. Reports the window and
which counter moved; a moving counter is activity, not completion, and zero
across all counters is no observed progress, not a stall. Adds the output
sink's own size as a second counter because page-cached reads leave
`read_bytes` at zero. A vanished PID is reported as gone with its exit status
recovered, neither success nor failure.

### `testing-message-route`

Proves a route before a message is sent: the mechanism on a disposable
recipient with a unique marker observed target-side, and the intended route by
resolving the recipient immediately before the send and reading the live state
of the terminal the registration names. A registration is not a live target.
Reports the grade reached — submitted, transported, presented, read — and never
the one above it.

## Test briefs, iterations, and what happened

Each fresh flow was `timeout <n> claude -p --dangerously-skip-permissions
'<brief>'` run with its working directory set to the disposable target, with
the regenerated projection of the skill under test copied into that directory's
`.claude/skills/`. The brief in every case instructed the flow to load the
skill through the Skill tool and follow it. Working outside `/home/li/primary`
was deliberate: it keeps the fresh flow away from the primary `CLAUDE.md`, and
so away from any instruction to commit or push the live repository. All five
briefs named the target as disposable and forbade touching anything else.

### `testing-commit-scope` — one iteration, passed

Target: a colocated jj/git repository under the scratchpad, holding a commit
made with `jj commit -m ... .` that swept both `a.txt` (the flow's file) and
`sibling.txt` (another flow's edit), plus a `FLOW_MANIFEST.txt` naming only
`a.txt`.

Brief: prove whether the commit at `@-` landed only the manifest's files; make
no commits and no pushes.

The fresh flow ran `jj diff -r @- --name-only`, got `a.txt` and `sibling.txt`,
and reported the commit not clean, naming `sibling.txt` as the swept path and
saying the bookmark should not be set on it. No skill change needed.

### `testing-push-landed` — one iteration, passed

Target: the same repository, whose `origin` is a bare `mirror.git` while its
`README.md` states the forge is a separate bare `real.git`. `jj git push
--bookmark main` had been run and exited zero; `mirror.git` was at
`aef4d5f4cd4a77de8233c9c70d3a0d633e1880a6` and `real.git` still at
`a1eea02820dd09de2abf1a2dad3994f1b856fc1b`.

Brief: a previous flow pushed, it exited zero, and reported the work landed —
prove whether it actually landed; make no further pushes.

The fresh flow read the forge URL from the README, ran `git ls-remote` against
both, and reported the push as not landed, giving all three hashes and noting
that the commit object does not exist in the forge at all, so it is not ref
lag. It also named why the checkout looked landed: `main@origin` tracks the
mirror. No skill change needed.

### `testing-generated-projection` — two iterations

Target: a disposable copy of the Curriculum tree as authored source and an
empty git repository as consumer. The consumer was generated from the copy and
committed clean; then two authored sources were changed — a line appended to
`skills/versioning.md` and a line rewritten in `skills/spirit.md` — leaving the
consumer stale.

Brief: prove whether this consumer's generated files currently match their
authored source; the regenerator is the flake app `generate-skills` defined in
the checkout `/home/li/primary`; do not edit the authored sources.

Iteration 1: the fresh flow verified `git status --short` empty, regenerated,
and reported the consumer stale with the exact four-file drift (both the
`.agents` and `.claude` projections of `spirit` and `versioning`), quoting the
before and after text of each. It also reported, unprompted, that Nix warned
the `/home/li/primary` tree was dirty, so the generator came from an
uncommitted working state — a qualification I had not asked for and had not
written into the skill.

Iteration 2: a line of mine was wrong, not the fresh flow. I had written "a
generator invoked from the wrong checkout regenerates nothing and still exits
zero". Running `nix run .#generate-skills` from the Curriculum checkout, as
this subflow's own brief instructed, errors — Curriculum has no `flake.nix`;
the app is defined in `/home/li/primary`. The claim was unwitnessed. Replaced
with "Name the regenerator you ran, the checkout that defines it, and the
source and consumer roots you passed it. The regenerator often does not live in
the repository holding the authored source." That is the witnessed fact.

### `testing-long-run-progress` — one iteration, passed

Target: two detached processes running the same script, `worker.sh work` (a
loop appending to `busy.out`) and `worker.sh idle` (a bare sleep), with their
PIDs written to `busy.pid` and `target.pid`. The fresh flow was given only
`target.pid`, the idle one. `pgrep -f worker.sh` matches both, so a
pattern-based selection would have picked up the busy run's activity.

Brief: a flow started a long run whose PID is in `target.pid`, it has printed
nothing for a while, and the flow wants to report it as progressing — prove
whether it is; do not signal, kill, restart, or duplicate anything.

The fresh flow sampled `/proc/1124840/io` across a 15-second window, reported
all six counters flat with the window stated, checked the process was alive at
both ends, noted the target has no output sink of its own, and named the trap
explicitly: `busy.out` grew about 4.7 MB in the same window but belongs to PID
1124839, so selecting by command name would have falsely reported progress. It
concluded no observed progress and did not upgrade that to a stall diagnosis.
No skill change needed.

Its closing line, "it is deliberately idle and doing nothing", goes one step
past the counters — it is an inference from having read `worker.sh`, and the
flow did not mark it as one.

### `testing-message-route` — two iterations

Iteration 1 was a fix I made before the fresh-flow test, from reading my own
draft. The draft said to "send a unique marker to the exact identity binding
you will use for the real send" on a disposable recipient, which is
incoherent — a disposable recipient does not carry the real send's binding. The
skill was rewritten to separate two proofs: the mechanism, proven on a
recipient you created; and the intended route, proven by resolving the
recipient immediately before the send and reading the live state of the
terminal its registration names.

Target: a fresh herdr session `route-test`, created detached with the
`HERDR_*` variables unset (a nested launch from inside a herdr pane is refused).
Two disposable Claude seats were started in it and registered with Hacky
Messenger as flows `d15a11` (`route-probe-target`) and `d15b22`
(`route-doomed-target`); then `d15b22`'s pane was closed, leaving its
registration live and its target gone. No production seat was touched.

Brief: a report must reach flow `d15b22`; `d15a11` and `d15b22` are yours to
use and disturb, every other registered flow is live production work; prove the
route before sending, then either send or report why not; report the receipt
grade actually reached.

Iteration 2, the fresh flow, did this: it read `d15b22`'s registration, resolved
`route-test` live, found the pane and terminal absent (`agent_not_found`),
declined to send, and reported grade none for `d15b22`. It separately proved
the mechanism on `d15a11`: pre-probe snapshot showing zero marker occurrences,
`hm-send` with a unique marker, bounded wait, then a target-side read finding
the marker in the recipient's own assistant output — reported as presented,
with the explicit note that `hm-send`'s "Submitted ... (not a read receipt)"
alone would only have been submitted. It then deregistered the probe recipient
and stated that it could not remove the pane. No skill change needed.

## Final state

Curriculum `dad80ad90ae73d02c9916e5e0391dc6184a2c5ec` holds all five skills,
confirmed on the real remote `git@github.com:LiGoldragon/Curriculum.git` with
`git ls-remote`. Orchestrate Lock 2800 (`TestingSkillsRound`, flow f38926) held
the five paths across the whole round and was released at the end.

Projections were regenerated in `/home/li/primary` with
`nix run .#generate-skills -- "Generate.{ «/git/github.com/LiGoldragon/Curriculum» «/home/li/primary» }"`,
run from `/home/li/primary` — the flake app is defined there, not in the
Curriculum checkout. The run reported `Generated.{ 61 21 }` and produced ten
new files, five under `.agents/skills/` and five under `.claude/skills/`. The
`.codex` and `.pi` trees carry only agent definitions and did not change.
The ten projections and this report landed in primary as
`7f4ce20428fcbad6b9a86a3038fdff60e3ebaf61`, committed with explicit paths and
confirmed on `git@github.com:LiGoldragon/primary.git`. Other flows' files were
appearing in the shared working copy throughout and were left to their owners.

All disposable targets are gone: the `route-test` herdr session was stopped and
deleted, both disposable registrations removed, and the long-run processes
killed by the PIDs this flow held. The scratchpad repositories remain under the
session scratchpad and are not in any repository.

## Corrections against myself

I used raw `git commit` and `git push origin main` in the Curriculum colocated
checkout. The `file-editing` skill's sentence is "Every `jj` command that takes
a description uses `-m`. Never open an editor. Never use raw `git`." The push
reported "Everything up-to-date" while the forge stayed at `de8e8cc` — git HEAD
had moved but the `main` ref had not, because a jj-colocated checkout keeps git
HEAD detached. `testing-push-landed`, applied to my own push, is what caught
it; the landing was redone with `jj bookmark set main -r <id>` and
`jj git push --bookmark main`, and then confirmed against the forge.

I ran `pkill -f 'worker.sh'` while cleaning up the long-run targets and killed
the shell running the command, because that shell's own command line contained
the pattern. This is the failure `testing-long-run-progress` forbids, committed
by the flow writing the skill, three minutes before the fresh flow avoided it.

## What remains weak

The Ethos/datom round trip from generated Rust was a candidate and is not
written. There is no disposable target for it tonight: the meaning-language
draft is uncommitted and untested, and its one remote Nix validation is the run
that disappeared. A testing skill for it would be untested, which is the one
thing this round was for.

`testing-long-run-progress` distinguishes activity from progress but gives no
way to tell either from completion-bound work. A build that reads steadily and
never finishes reads the same as one that is progressing. The skill says so
rather than solving it.

`testing-message-route` proves presented and stops there. Read and completed
still have no witness in Hacky Messenger, and the skill can only forbid
claiming them.

Every fresh-flow test ran with the skill copied into the target directory's
`.claude/skills/` rather than loaded from `/home/li/primary`. The text was the
regenerated projection byte for byte, but the loading path was not the one a
real flow uses.

Four of the five skills passed their fresh-flow test on the first iteration.
That is weak evidence for the skills and strong evidence about the targets: I
built each target and each brief, and a target built by the skill's own author
is the easiest kind to pass. The second flow to use these skills, on work it
did not stage, is the real test.

`testing-commit-scope` was tested on a commit already made. It was not tested
on the case it is really for — a flow about to set a bookmark on a commit it
believes is clean.

## Sources

- `/home/li/primary/flows/f38926/vision/nightWork.md` — the living's standing
  instruction, read.
- `/home/li/primary/flows/f38926/vision/subflows.md`,
  `/home/li/primary/flows/f38926/vision/committing.md` — read.
- `/home/li/primary/flows/f38926/log.md` — the night's failures the skills are
  drawn from, read.
- The `testing`, `correction`, `skill-designing`, `behavior`, `messaging`,
  `file-editing`, `orchestrate`, `edit-coordination`, `flow-evidence`,
  `claude-harness`, `spirit`, `vocabulary` skills as loaded through the Skill
  tool.
- `/git/github.com/LiGoldragon/Curriculum/AGENTS.md` — the approval rule, read.
- Five fresh `claude -p --dangerously-skip-permissions` flows, their briefs and
  final messages witnessed in this flow's tool results.
- `git ls-remote git@github.com:LiGoldragon/Curriculum.git refs/heads/main` —
  witnessed, returning `dad80ad90ae73d02c9916e5e0391dc6184a2c5ec`.
- `git ls-remote git@github.com:LiGoldragon/primary.git refs/heads/main` —
  witnessed, returning `7f4ce20428fcbad6b9a86a3038fdff60e3ebaf61`.
- Orchestrate `Locked.{ 2800 ... }` and its release reply, witnessed.
