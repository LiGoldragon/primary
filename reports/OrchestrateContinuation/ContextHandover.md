# Orchestrate — Context Handover

This document carries the Orchestrate thread into a fresh session. It is written
so that you can act without reading the conversation that produced it.

Read it in order. Section 1 is the psyche's own will and does not change when the
implementation changes. Section 2 is mechanism he chose and may be revised if a
better mechanism serves Section 1. Section 3 is verified current state. Section 4
is what to do next.

One framing fact you need before you read anything else: the psyche does not edit
this workspace. His words: "I dont do ANYTHING. EVER". Every commit, file, and
report here was written by an agent. Git history is evidence of agent behavior,
not of psyche decisions. His intent appears only in what he says, which is why
Section 1 quotes him verbatim rather than summarizing.

## 1. Psyche vision

This is his load-bearing will. It would still direct the work if every mechanism
named in Section 2 were thrown away. Do not paraphrase it into requirements and
then treat the requirements as the source. Quote-check against this section when
a design decision is contested.

### Why coordination exists at all

"we need the system to be fully coherent so that we know about the work tree
before another agent starts to keep working on this repository, leaving behind
the changes that were supposed to be merged"

"what I really want is a fully inter-agent communication system so that there's
always somebody to contact for anything"

"I'm trying to make Orchestrate a sort of typed communication between agents so
that if they work on something and there is a work tree, they get notified, and
they should be trained to know what to do when there is a work tree, a recent
work tree, and they want to work on something. They should probably spawn another
sub-agent to merge it"

The aim is a system where no work is silently stranded and where an agent facing
any situation has someone to ask. Notification plus trained response, not
prevention.

### What the current system costs

"because we're not there yet, Orchestrate is sort of more just acting like an
obstacle right now, although it does keep agents from working on top of each
other, but it seems to be costing us more than it's giving us right now"

"we need to not make Orchestrate such a blocker in terms of giving agents ways to
deal with different situations that they encounter. Like, yeah, all the different
scenarios should be covered in their training. That way they don't bail out all
the time."

"tell your agents to push through and not be intimidated by the broken
orchestration machinery"

Coverage of scenarios in agent training is the remedy he names. An agent that
stops working because coordination machinery confused it has failed, and the
machinery has failed it.

### Correctness

"I really dont like incorrectness, it just creates sprawl and problems"

On a generator that maintained a manifest of its own outputs: "which is wrong; I
can modify the filesystem without modifying that file, so it's a lie. useless."

A record that can drift from the thing it describes is not a weak record; he
treats it as worthless. This governs any design that mirrors state into a second
place.

### Agent behavior

"my agents are neurotic, and theyre trying to deal with my frustration by
constantly undoing what they just did, because theyre scared everything they did
was wrong"

"that sounds like theyve been trained to be stupid. which is why iv been deleting
a lot in the skills, but obviously not enough"

He reads over-cautious churn as a training defect, and he is treating deletion
from the skills corpus as the fix. Adding more rules is against the direction he
is pushing.

### Documentation style

Rejecting an aphoristic draft: "This style really feels counterproductive in
documentation, it's like agents are trying to sound poetic, which is
inappropriate and even harmful"

Write plain declarative prose. No epigrams, no compressed maxims.

## 2. Matter — decisions made this session

These are mechanism. They are current and should be followed, but they are
implementation choices, not vision, and they can be revisited on evidence.

- Orchestrate is a typed message board. His words: "orchestrate is a typed
  message board. it doesnt scan the filesystem or run commands." No scanning, no
  subprocesses, no filesystem access at all, not even read-only.
- It keeps the worktree registry: "and it WILL have worktree registry". The
  registry is fed by agent messages, never by scanning.
- "remove the doing, keep the knowing", and "if we implement doing, we do it in
  another component."
- All filesystem manipulation moves out of the daemon. Agents create and tear
  down worktrees themselves with `jj`.
- He rejected adding openssh to the daemon PATH. A daemon that runs no commands
  needs no ssh.
- Raw time values belong to debugging and canonical interfaces only. Common
  interfaces render elapsed time through the existing `HumanReadableTime` ladder.
- New standard, landed at
  `/git/github.com/LiGoldragon/standards/standard-component-architecture.md`:
  "Daemons keep their state in their own database. Do not write component state
  to files outside it."
- The repository formerly named `documentation` is now `LiGoldragon/standards`.

## 3. State of the work

### Specification

`/home/li/primary/reports/orchestrate-worktree-redesign/spec.md` (rev 756e94ae,
365 lines) is the design specification and has already been corrected to the
typed-message-board design. Read it before building. It is not restated here.

### Deployment

The running daemon is pinned at `be202b51060d098f3c71489859d8e03319ca2f97` in
`/home/li/primary/repos/CriomOS-home/flake.nix:171`, with the same rev in
`flake.lock`. The systemd unit itself is
`repos/CriomOS-home/modules/home/profiles/min/orchestrate.nix`; the pin is not in
that file. The deployed rev is ten commits behind orchestrate main.

It has not been redeployed. A redeploy would ship nine unrelated peer commits and
restart a daemon holding live lanes for roughly six active sessions. That
decision is open and belongs to the psyche.

### The lane reaper in the deployed daemon

The deployed build contains a 24-hour lane reaper that main has already removed:
`ACTIVE_LANE_IDLE_LIMIT_NANOS` in `src/lane.rs` and
`ACTIVE_ORCHESTRATOR_AGENT_IDLE_LIMIT_NANOS` in `src/table_reclamation.rs`.
`reconcile()` deletes an idle lane, drops its claims, and flips its worktrees to
Abandoned. It fires on every read of the lane registry and writes nothing to the
journal. It has fired seven times since 07-19 and produced the current 12
Abandoned rows.

The psyche only ever asked for a warning about potentially stale entries.
Deletion and abandonment were never authorized. Verified: the reaper is
registry-only, has no filesystem effect, and has destroyed no work. The harm is
the delisting itself, because work the system forgets is lost to the agents that
depend on the registry to find it.

### Work at risk on disk

`~/wt/github.com/LiGoldragon/core-schema/AliasAdmissionProposal` holds 2 commits
reachable from no remote: 788 insertions, of which
`src/alias_name_projection.rs` is 620. The local bookmark sits on a divergent
line and does not pin them.

### Landed this session

- orchestrate `35e776e7` renders elapsed time on all seven time-bearing reply
  variants.
- `/home/li/primary/orchestrate/AGENTS.md` corrected (rev b9dfae89). Its
  documented `Register` example had been invalid since 2026-07-05 and was the
  single largest specific source of parse errors in the recorded corpus.

### Contract skew — read the right schema

The deployed daemon builds against `signal-orchestrate` 0.10.1 (rev d5ecda9).
The local checkout at `repos/signal-orchestrate` is 0.5.0, a different line,
missing three verbs. Anything read from that checkout is stale. Read at `-r main`
or from the pinned cargo checkout:
`/home/li/.cargo/git/checkouts/signal-orchestrate-d740ab43cb4f03f1/d5ecda9/schema/lib.schema`

### Built, deployed, and never driven

`MintAgentIdentity`, `LaunchAgent`, and `SendOrchestratorMessage` are implemented
at `repos/orchestrate/src/execution.rs:5838-5988` and push into the messenger
socket. Nothing has ever registered an agent, so `(Observe Agents)` returns
`(AgentDirectory [])`.

The messenger (`message` component) is a real mailbox-and-thread system carrying
`ThreadRelation { RepositoryName FeatureBranchName }`, which is exactly the join
key the worktree-notification design needs. It has never carried a message.

This is the nearest existing path to the "always somebody to contact" aim in
Section 1, and most of it is already built. Driving it is largely a matter of
getting agents registered.

### Do not build on Watch/Unwatch

The payload is `{include_operations, include_effects}`, an untargeted firehose.
The handler at `execution.rs:511-517` returns a token and registers nothing. It
is a stub, not a subscription system.

### worktrees.nota

`/home/li/primary/orchestrate/worktrees.nota` is a git-tracked file that the
daemon writes to mirror its registry. It violates the new standard in Section 2.
It is also already wrong: its `pushed_state` column reads `AncestorOfMain` on all
147 rows, including 8 that are not merged. This is a concrete instance of the
correctness objection in Section 1.

## 4. Open items, ranked

### 4.1 Highest priority — a writing agent has no way to learn how to register a lane

An agent this session searched for an Orchestrate tool, found none, and proceeded
to write without a lane. This is not a training failure by that agent. The
instruction to register exists; the means does not.

The literal `meta-orchestrate` command was removed from the `edit-coordination`
skill and replaced with the phrase "with the orchestration system". The deployed
text at `/home/li/primary/.claude/skills/edit-coordination/SKILL.md` now reads:

    - Register a session lane with the orchestration system before writing;
      success is the registered reply, not exit status.

Nothing anywhere tells a writing agent how. Earlier agents managed only because
the older generated skill still carried the literal command.

The psyche's constraint: putting the command in AGENTS.md would tax every
read-only agent with instructions it can never use.

Proposed resolution, not yet approved: the concrete command belongs in a module
preloaded only into the write-capable role packets, reaching the four `write-*`
roles and none of the `read-*` roles.

Verified today in `/git/github.com/LiGoldragon/skills`, replacing earlier stale
findings:

- Roles are now the cross product of permission and depth. `role-permissions.nota`
  gives `read` and `write`; `role-depths.nota` gives `trivial`, `ordinary`,
  `demanding`, `critical`. That is the eight roles, and there is no per-role
  source file to edit.
- Every generated role packet receives exactly one module list:
  `manifests/universal-role-modules.nota`, currently `[general-instructions
  tenets]`. This is confirmed in `src/assembly.rs:669-695`, where `packets()`
  expands `universal_role_modules.payload()` for every role with no
  permission-dependent branch.
- There is therefore no existing hook for attaching a module to some roles and
  not others. Implementing the proposal requires a generator and schema change in
  `LiGoldragon/skills` — either a permission-scoped module manifest or a modules
  field on `role-permissions.nota` — not a manifest edit alone.
- `skills/edit-coordination-core.md` does exist and is declared in
  `manifests/module-dependencies.nota:11` with use `RoleComposition`, but it is
  named by no manifest, so it currently reaches zero role packets. Its body is
  identical to the runtime skill and contains no command either. The earlier
  finding about an 11-role preload list is stale; no such list exists.
- Confirmed by inspection: none of the eight files in
  `/home/li/primary/.claude/agents/` mentions orchestrate, lanes, or claims.

Whatever text lands must contain the working commands. This syntax was
re-verified today against the shipping binary, and both calls succeeded. The
prose documentation has been wrong repeatedly; trust the binary.

    meta-orchestrate "(Register ((SessionName laneName ([SessionName Discipline] Structural) [why this lane exists]) Fresh))"
    orchestrate      "(Claim (laneName [(Path /absolute/path)] [why you are editing]))"
    orchestrate      "(Release laneName)"
    meta-orchestrate "(Retire (Lane laneName))"

Traps that must be taught alongside the commands:

- A semantic refusal exits 0. `ClaimRejection` and `PartialApplied` are failures
  that report success to the shell. Only malformed NOTA exits 1. Read the reply
  record; never branch on exit status.
- A bracketed reason needs two or more tokens. A single word goes bare and
  unbracketed.
- Neither CLI has `--help`. A valid verb given no payload reports `unknown Input
  variant <Verb>`, identical to the error for a verb that does not exist. That
  message caused roughly 1,100 recorded failures of agents brute-forcing verb
  names.
- A claim enforces nothing mechanically. `apply_claim` checks lane registration,
  compares path prefixes, and writes redb rows. There is no flock and no
  interlock. It is advisory bookkeeping, and agents must not abandon work over
  it.

### 4.2 Deploy decision

Ten commits behind. Redeploying kills the lane reaper described in Section 3,
which is currently deleting lanes nobody authorized it to delete. It also ships
nine unrelated peer commits and restarts a daemon holding live lanes for about
six sessions. The psyche decides.

### 4.3 Unreferenced commits in core-schema

The 2 commits at `~/wt/github.com/LiGoldragon/core-schema/AliasAdmissionProposal`
are reachable from no remote and not pinned by the local bookmark. Push or
otherwise anchor them before any worktree drain touches that tree.

### 4.4 The general-instructions module

It reaches every role. It is six prohibitions and one style rule, and it grants
no authority to act. The psyche called it garbage. A four-line replacement was
drafted this session and remains unapproved. It is listed here as an open
question, not as a decision.

### 4.5 Worktree backlog drain

186 stale jj workspace entries; 21 workspaces rooted in `/tmp`, which is an
active generator rather than a backlog; 40 in `~/agent-worktrees`; about 17
corpses under `~/wt`; 9 flat independent clones.

Data-loss rules for the drain: never run `jj util gc` on a source checkout during
a drain, and never `jj workspace forget` followed by `rm -rf` before a push is
verified showing a non-`git` remote.

### 4.6 Nota version skew

Three `nota` versions coexist. The manifest encodes via 0.5.1, which writes
`[a purpose]`, while `relative-age-display` pins 0.9.0, which writes
`(a purpose)`. Any tool reading both will mis-parse one of them.
