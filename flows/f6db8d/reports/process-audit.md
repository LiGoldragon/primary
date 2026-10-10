# Process audit of flow 857335

Scope: how the Codex main flow 857335 conducted itself, judged against the
`main-flow`, `subflow`, `behavior`, `flow-evidence`, `orchestrate`,
`file-editing`, `feature-development`, `nix-workflow` and `testing` skills as
they stand in `/home/li/primary/.claude/skills/`, and against the living's
vision on subflows in `/home/li/primary/flows/162eb3/vision/subflows.md`.

Marking convention: **[W]** witnessed by this flow directly (a command run, a
file read, a live service queried); **[R]** relayed — read out of 857335's own
prose or out of a subflow's returned text that this flow could not re-derive;
**[I]** this flow's inference.

## Method

- Live `orchestrate 'Observe.Locks'` against the running lock service (read-only).
- The Codex rollout transcript
  `/home/li/.codex/sessions/2026/09/10/rollout-2026-09-10T00-09-52-01a08838-6687-7361-915d-7d1857335615.jsonl`
  (11 972 records), flattened to a line-indexed text index and searched. Line
  numbers below are jsonl record line numbers in that file.
- The two auditor transcripts named in `witnesses/skeptical-shutdown.json`.
- `git`/`jj` state of `/home/li/primary`, `/git/github.com/LiGoldragon/{spirit,mirror,protos,CriomOS-home}`,
  and the two `/home/li/wt/*/deprecation-857335` workspaces.
- `systemctl --user` state of `orchestrate-nexus.service` and of the audit units.

### Limit on reconstruction

Every `spawn_agent`, `followup_task` and `send_message` payload in the Codex
transcript is a fernet-encrypted blob (`gAAAAA…`); 693 `AGENTMSG` records are
likewise empty. **[W]** The flow delegated almost all task work, so the actual
edits, lock calls, commits and build invocations happened inside subflows whose
content is not recoverable from this transcript. Where a lock receipt or a
build result is therefore only visible as the main flow's summary of it, this
report marks it **[R]** and says so. This is a property of the harness's
transcript format, not a concealment by the flow.

## 1. Locks

### What remains held now

`Observe.Locks` returns 33 locks. **No lock in the snapshot carries FlowId
`857335`.** **[W]** The highest-numbered live lock is 1019 (flow `f7941a`);
locks 987, 1008, 1009, 981, 982, 1020, 1021 and 1070 are all absent. No
reservation from 857335 or its subflows is outstanding.

### Lock 1070 — the one lock the transcript shows end to end

Acquired at line 11896 (`2026-09-10T19:39:16Z`), receipt at line 11902:

    Locked.{ 1070 DeprecateLegacyComponents 857335 [ …/spirit/README.md …/spirit/ARCHITECTURE.md
    …/spirit/AGENTS.md …/mirror/README.md …/mirror/ARCHITECTURE.md …/mirror/AGENTS.md ] Deprecation }

Released at line 11945 (`19:41:14Z`), receipt at 11951: `Released.{ 1070 … }`. **[W]**

The request is well formed against the `orchestrate` skill: `LockName` names the
work and does not carry the flow id, `FlowId` is `857335`, paths are absolute,
and the single-word reason `Deprecation` is correctly left unquoted. The write
set (six paths) exactly equals what was edited (three files per repository).
**[W]** Nothing to fault here.

The log records the acquisition ("Reserved … under lock1070") and does not
record the release. The release did happen. **[W]** This is an incompleteness in
the log, not a misstatement.

### 987 → 1008/1009 → 1020/1021

The only account is the flow's own log paragraph, written at line 2692
(`2026-09-09T23:45:23Z`), and the assistant message at 2684 that precedes it.
**[R]** The underlying `Observed.Locks` snapshot and the `Locked` receipts for
1020/1021 arrived inside encrypted subflow messages and are not in this
transcript. The main flow itself issued exactly one `orchestrate` command before
the deprecation work (line 32 is `flow-id`; the first `orchestrate` call is the
1070 Lock at 11896). **[W]** So the flow reported a lock state it had not
observed itself, from a subflow that had — which the `main-flow` skill permits
("A flow is liable for its subflows"), and which `behavior` requires be marked
as relayed. The log paragraph does not mark it as relayed; it reads "A current
typed lock snapshot showed…" as if first-hand. That is a `behavior` lapse of
attribution, minor in consequence.

On cause: the log says "The cause of replacement was not established here" and
this audit cannot establish it either. **[W]** One supported narrowing: at line
628 (`22:32:07Z`) a subflow report already stated "Consumer locks 991 through
1000 cover the independently editable consumers" — i.e. 857335's own subflows
were issuing locks in the 99x–100x band an hour before the 23:45 snapshot.
**[I]** The most economical hypothesis is that 987 was released and 1008/1009
taken by 857335's own subflows — self-replacement, not external interference.
The flow's own wording ("narrower **same-flow** reservations") shows it had
already concluded the replacements were its own. The unknown is therefore
narrower than the log implies: not "who took 1008/1009" but "which subflow
released 987, and on what reasoning". That remains unknown. **[I]**

Keeping it unknown was correct. The log did not invent a cause.

### Were the protected CriomOS-home paths ever edited? No.

The typed prohibition is at line 225 of the opening brief: "Two other Codex
sessions hold locks 981 and 982 over paths in
`/git/github.com/LiGoldragon/CriomOS-home`; do not touch those paths."

Witnessed in the checkout: **[W]**

- `flake.nix` last modified `Sep 9 14:26`; last commit touching it is
  `9548d7d 2026-09-09 22:26:09 +0200` — before flow 857335 began (its first
  record is `2026-09-09T22:09:53Z` UTC, i.e. `2026-09-10 00:09` local).
- `git log --since=2026-09-09 --until=2026-09-12` over the repository returns
  **no commits at all**.
- The Orchestrate pin in `flake.nix:138` is still
  `github:LiGoldragon/orchestrate/5f016531e765d9b679a86cc47a2d75eaca43d624` —
  it was never advanced to the 0.31.0 the flow released.
- The only dirty files are `packages/codex-artifact-gateway/{default.nix,gateway.py}`,
  which are precisely the paths of live lock **1019**, owned by flow `f7941a`.

Corroborating, `orchestrate-nexus.service` is running
`/nix/store/…-orchestrate-0.30.0/bin/orchestrate-nexus` **[W]** — the live
service was never moved to the flow's 0.31.0. The flow's repeated claim that
"the live Orchestrate service remains untouched" and "No protected CriomOS Home
path was edited" is **confirmed by independent witness**, not merely asserted.

The flow also handled the collision correctly when it found it. At line 3638
(`00:31:56Z`) it reported: "The deployment review found a concrete constraint:
CriomOS-home fixes Orchestrate's revision in `flake.nix`, one of the files you
explicitly protected. … I'll complete the port and isolated migration tests,
then present the exact pin change needed before touching that file or
deploying." It prepared `reports/orchestrate-deployment.patch` and stopped. That
is the right shape.

### Lock count

`reports/shutdown-runtime.md` lists 23 locks released (1024, 1031, 1033, 1054,
1059, 1064, 1065; then 1025–1029, 1034, 1040, 1043, 1045, 1050, 1051,
1061–1063, 1068, 1069) plus 1070 later. **[R]** All are absent from the live
snapshot **[W]**, so the releases are corroborated in effect even though the
receipts are not in this transcript.

## 2. Subflow launching

### What was actually done

Both audits were launched at line 11645 (`07:20:51Z`) by one inline `python3`
heredoc issuing two `systemd-run` commands: **[W]**

    systemd-run --user --unit=flow857335-audit-{opus,sol} --property=MemoryMax=4G \
      --working-directory=/home/li/primary --setenv=PATH=<inherited> \
      /usr/bin/env python3 /home/li/primary/flows/857335/witnesses/run-skeptical-audit.py {opus,sol}

The helper's two command lines, still on disk: **[W]**

    ['/home/li/.nix-profile/bin/claude', '--model', 'claude-opus-5', '--effort', 'medium',
     '-p', '--output-format', 'json', '--allowedTools', 'Read,Glob,Grep,Bash,Write']

    ['/home/li/.nix-profile/bin/codex', 'exec', '-m', 'gpt-5.6-sol',
     '-c', 'model_reasoning_effort=medium', '--sandbox', 'read-only',
     '--json', '--output-last-message', '<reports/skeptical-sol.md>', '-']

`--ask-for-approval` appears nowhere in the transcript.
`--dangerously-skip-permissions` appears only inside a `claude --help` dump at
line 11614. `--sandbox danger-full-access` is never passed. **[W]**

So the restriction was applied **asymmetrically**: Sol got an OS-enforced
read-only sandbox; Opus got no sandbox but a tool allowlist
(`Read,Glob,Grep,Bash,Write`). Neither is "no sandbox, all permissions."

### Judged against the vision — with the dates stated plainly

`flows/162eb3/vision/subflows.md` carries four entries. **Three are dated
2026-09-12 and one 2026-09-10** — all of them at or after the launches being
judged, and three of them two days after. **[W]** The 2026-09-10 entry is
explicitly the living's *reaction to this very flow*: its own context line reads
"flow 857335, a Codex main flow, had launched its Sol audit as a separate `codex
exec` process under systemd with a read-only sandbox instead of through its
subagent tool; the flow asked why and no reasoning was recorded."

**[I]** None of this vision existed when 857335 acted. It cannot be charged
with breaking a rule that its own conduct caused to be written. What the vision
establishes is the standard *from now on*, and 857335 is the case that produced
it. Judged as a forward standard:

- "Codex doesn't need another Codex to run ChatGPT models, and vice versa"
  (2026-09-10) — the **Sol** audit is exactly the criticized shape: a Codex main
  flow spawning an out-of-process `codex exec`. It should have been a native
  subagent.
- "yes, its still a subflow" (2026-09-12) — the **Opus** audit, a Codex flow
  invoking `claude -p`, is legitimate in kind. The native `spawn_agent` tool
  could not have produced a Claude Code auditor at all. **[W]** All 12
  `spawn_agent` calls in the session name Codex models
  (`gpt-5.6-luna` ×2 explorer, `gpt-5.6-terra` ×10 write-agents).
- "no sandbox. all permissions" (2026-09-12) — both launches fall short, Sol by
  `--sandbox read-only`, Opus by the `--allowedTools` allowlist.
- "when a different harness is invoked, it shouldn't be invoked with the main
  flow training, but with the subflow training" (2026-09-12) — the briefs carry
  `FLOW_ID: 564f55` and `FLOW_DIRECTORY: /home/li/primary/flows/564f55` exactly as
  the living instructed at line 11581, and are framed as subflow briefs. **[W]**
  This one the flow already satisfied.

There was a live constraint pushing the flow out-of-process for Sol: the
session's own AGENTS.md preamble (line 6) carried "## Temporary subagent model
constraint — Subagents must never use or inherit Sol." **[W]** The flow
acknowledged the tension at line 11595 and treated the living's fresh
instruction as superseding it — correct handling — but then routed around the
constraint by leaving the harness rather than using the now-authorized native
tool. **[I]** No reasoning for the sandbox, the 4 GiB cap, or the
process-versus-subagent choice was recorded: the four reasoning records in that
window (11634, 11644, 11651, 11659) have empty summaries. **[W]** That silence
is itself what the living flagged.

### The sandbox demonstrably damaged the audit

This is not a style point. In the Sol auditor's own transcript
(`/home/li/.codex/sessions/2026/09/10/rollout-2026-09-10T09-20-52-01a08a30-d8e6-74f2-95f7-4449a68266fe.jsonl`,
line 165): **[W]**

> "The managed filesystem is enforcing read-only access even inside the
> authorized witness directory, so no new scratch or Cargo target can be
> created. I'll use already-built test binaries if present and otherwise label
> behavior as source-demonstrated or unexecuted, rather than claiming a run I
> could not perform."

The restriction the flow added on its own initiative forced its auditor to
downgrade witnessed behavior to source inspection. Meanwhile the unsandboxed
Opus auditor built two probe crates and generated Ethos output without
difficulty (`permission_denials: []`; 201 MB of cargo targets now in
`/home/li/.cache/flow857335-audit-builds`). **[W]** The asymmetry produced
exactly the wrong outcome: the constrained auditor was the one that could not
witness.

Neither limit ever bound for resource reasons — `MemoryCurrent` at the last
sample was ~218 MiB (opus) and ~673 MiB (sol) against a 4 GiB cap. **[W]**

## 3. Claims versus witnesses

### The suspected signal-standard contradiction is not one — the flow disclosed it

`witnesses/signal-standard-nix-6688f8ca.exit` and `-retry.exit` both contain
`0`, and both corresponding `.log` files contain: **[W]**

    cannot build on 'ssh-ng://root@192.168.1.65': error: failed to start SSH connection to '192.168.1.65'
    building '/nix/store/…-signal-standard-fmt-1.0.0.drv'...

That is a remote-builder failure followed by a local fallback build — exit 0
earned locally, which `nix-workflow` forbids ("Run Nix builds only through
configured remote builders; never build locally").

But `reports/shutdown-signals.md` states it outright: **[W]**

> "The prior configured Nix invocation on `6688f8ca` exited 0 only after remote
> SSH failed and local fallback built; **this is not remote-execution proof**.
> The final-head configured matrix has no recorded exit."

The prose matches the witness precisely, names the defect, refuses the
inference the exit code would otherwise license, and flags the zero-byte
final-head log (`signal-standard-nix-2c90fc99.log`, 0 bytes — **[W]**) as having
no recorded exit. **The suspicion is disconfirmed.** This is a model instance of
the `behavior` rule, and the strongest single piece of evidence that the flow
was reading its own witnesses rather than summarizing its hopes.

The local build itself still happened and still contradicts `nix-workflow`;
disclosure mitigates the report, not the act. **[I]** The cause is visible and
external — the builder host went away, and at line 11761 the living confirmed
"im taking prometheus offline. you wont have a remote nix builder now."

### Other exit codes match their prose — no second contradiction found

All fourteen `mirror-*-compile.exit` files read **`101`**, with logs ending e.g.
"error: could not compile mirror (lib) due to 82 previous errors". **[W]** The
only prose citing them, `shutdown-signals.md:21`, says "`cargo check
--no-default-features` **fails**; the latest durable captures are
`witnesses/mirror-*-compile*.{log,exit}`." Exit value and prose agree; no report
anywhere claims Mirror green. The six `spirit-*.exit` files read `0` with logs
ending in passing `test result: ok` lines, matching "implemented and locally
tested workspace split". `harness-722b-nix.exit` reads `0` as its witness
states. `spirit-split-nix.log` records "shutting down error: interrupted by the
user" and is cited as a gate by nothing. **[W]**

Across the lane the pattern holds: **every place a gate actually went wrong —
the ssh-ng fallback, the fourteen exit-101 Mirror compiles, the interrupted
audits — the prose says so and refuses the green.** No case was found of an
exit code being laundered into a claim.

### Evidence-shape compliance

Of 14 `.md` reports, **7** end with `## Sources` as their final section. **[W]**
Three lack it entirely: `other-signals.md`, `shutdown-signals.md`,
`spirit-nexus-audit.md` — the second being the report carrying the most careful
disclosure in the lane. Two more have a `## Sources` block that later sections
were appended *past*, so it no longer covers the file: **[W]**

- `port-preparation.md` — `## Sources` at L46, then `## Declarative deployment
  constraint` at L53 to EOF.
- `substrate-audit.md` — `## Sources` at L45, then six further sections through
  `## Final Ethos-pinned producer closure` at L125. Its heaviest green claim sits
  after Sources and is uncovered by it.

`flow-evidence` says the Sources section is written "as it is made"; appending
past it is the failure mode that rule exists to prevent. **[I]**

Of the witnesses, four state an explicit method — `datom-codec-final.md`,
`ethos.md`, `protos-depth.md`, `validation.md`. **[W]** Three more
(`runtime-port.md`, `lojix-horizon-boundary.md`, `other-signals.md`) name the
exact commands and the executing subflow and thread, which is adequate in
substance. `spirit-split-inventory.md` is a raw path/grep dump with no statement
of how it was produced. The two `skeptical-*-brief.md` files are task inputs
misfiled as witnesses.

`witnesses/ethos.md` is the model of the form: "Method: execute library, CLI,
integration, freshness, generated-module, and isolated Signal-without-Datom
tests locally; **then separately** evaluate and run all Nix checks only through
the configured remote builder" — which honours `nix-workflow`'s "Keep
evaluation and activation evidence separate" in the witness itself. **[W]**

### Claims with no witness of any kind

Six green assertions have no corresponding witness file: **[W]**

- `shutdown-runtime.md`: "Local default tests passed 2/2 and Datom tests passed
  4/4" (signal-orchestrate WIP `e3ea414c`).
- `shutdown-runtime.md`: "Local default tests passed 1/1 and Datom tests passed
  2/2" (meta-signal-orchestrate WIP `eb6df08e`).
- `shutdown-signals.md`: "`signal-mirror` … Default tests passed before carrier
  addition."
- `shutdown-signals.md`: "`meta-signal-mirror` … Default/Datom tests passed
  locally."
- `shutdown-signals.md`: "`signal-standard` … `2c90fc99…` (v1.0.0). Local
  tests/fmt/clippy passed" — the only artifact at that head is
  `signal-standard-nix-2c90fc99.log`, **0 bytes**, with no `.exit`.
- `spirit-nexus-audit.md`: "direct filesystem inspection found that exact file
  present on 2026-09-10" — the inspection is recorded nowhere.

Three further claims rest on witness *prose* where the lane's own `.exit`/`.log`
convention was available and unused: `substrate-audit.md`'s "all 10 checks" /
"all 12 checks", `runtime-port.md`'s "all 16 Orchestrate checks", and
`shutdown-runtime.md`'s "39 checks including VM behavior". **[W]** Under
`testing` ("Infrastructure reports are ground: a build reported green is green")
these are not breaches, only thinner than their neighbours.

Against that, roughly 14 discrete green claims *are* properly grounded —
`implementation.md`'s 37-test breakdown matches `witnesses/ethos.md` exactly;
`cutover-preparation.md`'s "PID 2323 … version `0.30.0`" matches the raw
`MainPID=2323` block in `witnesses/runtime-port.md`; the Mirror WIP claims match
their exit files. **[W]**

### Evidence cited from /tmp, and evidence with no account

`witnesses/other-signals.md:7` cites: "`nix build -L` for all six exited `0`;
captured exit record `/tmp/terminal-cell-e44-gates.exit` and log
`/tmp/terminal-cell-e44-gates.log`." **[W]** Both still exist: the `.exit`
reads `0`; **the `.log` is 0 bytes**. A witness cites, as its evidence, an empty
file — and both files live in `/tmp`, outside the flow lane, so the cited
evidence was never durable lane evidence at all. `flow-evidence` requires the
artifact under `FLOW_DIRECTORY`.

The reverse also occurs: `witnesses/domain-da553-nix.{exit,log}` (exit `0`, log
ending "all checks passed!") and all four
`witnesses/producer-gates/signal-*-nix.exit` (all `0`) are cited by no report at
all. **[W]** Evidence present, account absent.

### Evaluation and activation evidence bound together

`nix-workflow`: "Keep evaluation and activation evidence separate." Three files
mix them: **[W]**

- `reports/runtime-port.md` — `## Remote Nix gate` ("all checks passed!" for 16
  Orchestrate checks) in the same file as `## Deployment boundary` (live PID
  2323) and a full cutover runbook.
- `reports/shutdown-runtime.md` — the 39-check remote gate beside live-service
  state and lock releases.
- `witnesses/runtime-port.md` — `## Remote Nix gate` and `## Isolated packaged
  candidate` sharing a file with `## Migration and live boundary` and its live
  `ActiveState=active / MainPID=2323` block.

`reports/cutover-preparation.md` is the counter-example: live observation only,
no Nix gate. **[W]**

### A witness that verifies — and one that ages badly

`witnesses/skeptical-audit-authority.json` records SHA-256 digests of the ten
authority documents. Re-hashed today, 5 of 10 differ. **[W]** But at commit
`6e2282052` ("Brief independent Opus and Sol skeptical stack audits") all ten
match byte for byte. **[W]** The drift is from later flows editing `Vision/`,
not from a bad witness. The witness works — but only because this audit thought
to look for the commit. Recording the digests without the revision they were
taken at leaves the witness self-verifying for about a day. **[I]** The full
authority text is in any case preserved inside the two 50 KB briefs.

### Grounding of the push claim

The log says the deprecation commits "were committed and pushed successfully."
The push step at line 11927 returned only `Changes to push to origin: bookmark:
main [move forward from 008d8ca0 to 8b391bf1]` with a `session_id` and **no exit
code** — a still-running command. **[W]** The flow wrote "pushed successfully"
at 11945, 44 seconds later, without a completion witness. Independently checked
now, `jj bookmark list --all-remotes` shows `main … @origin: 8b391bf1` in Spirit
and `@origin: 74ed002e` in Mirror. **[W]** The claim is true; its grounding at
the time was thinner than the wording.

## 4. Log integrity

### The deprecation does appear in a report — premise disconfirmed

`d95f40754` ("Record Spirit and Mirror deprecation and supersede migration
plan") changed **two** files: `flows/857335/log.md` (+4) and
`flows/857335/reports/shutdown-signals.md` (+11/-1). **[W]** The report gained a
`## Deprecation ruling — 2026-09-10` section quoting the living's words and
retitling the old plan "Historical resume order (superseded)". The deprecation
is not log-only.

### "lock1070" versus shutdown-runtime — not a contradiction

`reports/shutdown-runtime.md` says "A final typed observation found no remaining
lock owned by flow 857335." That report was written at the `07:2x`-UTC shutdown
checkpoint. Lock 1070 was taken at `19:39:16Z` and released at `19:41:15Z`, more
than twelve hours later, in a session the living resumed at `19:34:46Z`. **[W]**
Both statements are true of their own moments. **Disconfirmed.**

### The final answer to "was anything audited?" is honest

Line 11966 (`20:11:20Z`), the living: "was anything audited?" Line 11969, the
flow, in full: **[W]**

> "Yes, but **the final whole-stack audit is incomplete**. Earlier component
> reviews found and led to fixes for parser escaping/budgets, Datom derives and
> error paths, and Ethos generation defects. Later source audits exposed missing
> Nexus requirements in Orchestrate and Ethos. The two skeptical audits you
> specifically requested—**Opus 5 and Sol, both medium**—started inspecting the
> released stack. Claude also ran local probes. Both were interrupted before
> final reports, so **their findings were not reconciled and neither produced a
> completed verdict**. Green build/test gates exist for the landed libraries.
> They do **not** establish full Vision/Intent compliance."

Every clause is accurate and the disclaimers are volunteered rather than
extracted. No misstatement. The one omission is treated below, and it is large.

### The material omission: findings existed and were discarded

The living's instruction at line 11581 ended: "have each write its report in
your lane; and **record in your log what each found** and what you changed."
**[W]**

What each found was never recorded. `reports/skeptical-sol.md` and
`skeptical-opus.md` are 800-byte placeholders saying "No final report existed";
`log.md` says "Neither had delivered a final report at interruption." All true
of the *reports*. But the findings were not absent — they were sitting in the
auditors' transcripts, whose paths the flow had already written into
`witnesses/skeptical-shutdown.json`.

Read now, the Sol transcript's assistant messages carry three concrete
disconfirming findings, stated before the interrupt: **[W]**

- line 73: "Protos disables automatic tests and registers only `tests/protos.rs`;
  four substantial test files are present but never built. I'm treating those
  files as non-evidence and checking whether their apparent coverage masks
  released API/behavior gaps."
- line 157: "derived unit enum variants bypass the composition budget entirely,
  and `Decimal` ascent can panic for non-finite `f64`, contradicting the total
  ascent contract."

The first is independently confirmed by this audit at the audited revision
`b543678`: `protos/Cargo.toml` sets `autotests = false` and declares a single
`[[test]] path = "tests/protos.rs"`, while `tests/` also holds `deep.rs`,
`delineation.rs`, `scale.rs` and `textualization.rs` — about 24 KB of test code
that is never compiled. **[W]** The flow's own gates had reported Protos green
across ten remote checks. **[R]**

The Opus side is the opposite shape: 45 turns, $3.33, 25 870 thinking tokens,
two probe crates and a generated `signal-meaning.rs` on disk — but only three
trivial assistant text blocks survive ("Now examining ethos-zero.") and no
thinking blocks are persisted. **[W]** Its findings are genuinely unrecoverable.
Sol's were not.

**[I]** This is the most consequential process failure in the flow. The
interruption was not the flow's fault; leaving recoverable findings unharvested
was a choice available for correction during the 12-hour gap before the session
resumed at 19:34, and during the deprecation work that followed. The instruction
to record what each found was not met, and the placeholders' phrasing — "No
completed verdict or reconciliation is claimed" — is accurate in a way that
conceals that partial findings existed. A defect the flow's own gates missed,
which the audit the living ordered actually caught, was discarded.

### Smaller imprecision

`log.md` says "Opus had no final stdout." `witnesses/skeptical-opus.stdout` is
2 082 bytes — a result envelope with `"terminal_reason":"aborted_streaming"`,
`"is_error":true`. **[W]** There was a stdout; it contained no report. The
substance is right, the wording wrong.

## 5. Sequencing

Verbatim typed orders, with jsonl line numbers: **[W]**

- **Line 1418**, `2026-09-09T22:57:43.302Z`: "From the living psyche, relayed by
  flow 564f55: once you have realized the stack and audited it against the
  Vision and Intent you were given, port Orchestrate to the new stack. … **Sequence: audit
  first, then port.** Note that Orchestrate is the lock daemon you are taking
  locks from; plan the cutover so its live instance keeps serving until the new
  one is deployed…"
- **Line 11581**, `2026-09-10T07:17:58.533Z`: "From the living psyche, relayed by
  flow 564f55: when you audit the realized stack against the Vision and Intent,
  run two skeptical audits, each as a subflow with your brief, each seeking
  disconfirming evidence rather than confirming your work, and **reconcile their
  findings before porting Orchestrate.** … have each write its report in your
  lane; and record in your log what each found and what you changed."

### Before the first order: port work had already begun

- 1116 (`22:48:55Z`) `spawn_agent` `task_name:"consumers"`; 1145 (`22:49:37Z`)
  "Signal-orchestrate's consumer migration has also started"; 1171 (`22:51:07Z`)
  "Signal-orchestrate's manifest now separates optional Datom support from its
  signal dependencies." **[R]**

These precede line 1418 by nine minutes. The flow's response was correct: at
1423 (`22:57:57Z`) "I'll finish and audit the stack … before **continuing** the
Orchestrate port" and at 1438 it logged "**Paused** additional Orchestrate port
work pending the stack audit and preserved preliminary consumer edits." **[R]**
It did not backdate or conceal the head start.

### Between the orders: the port ran, after a declared audit close

The flow held the line while the audit was open — 2220 (`23:23:51Z`) "The stack
audit remains open … **No Orchestrate cutover work has begun**"; 2444, 2452,
2829 repeat it. **[R]** It then declared the audit closed and started: 3683
(`00:33:41Z`) "The stack gates are now green: Protos passed all 10 remote checks
and Datom all 12 … **I'm recording the completed audit, then starting the
Orchestrate port**"; 3776 (`00:35:26Z`) "The audited stack is recorded, and the
Orchestrate phase has started under fresh repository locks." **[R]**

The port then ran to publication inside this window: 3826 (`00:37`) both
contracts generate from Ethos 6; 4148 (`00:50`) three packages; 4390 (`01:05`)
both signal contracts published with green remote gates; 4830 (`01:29`)
"**Orchestrate 0.31.0 is now on main.** All 18 workspace tests and 16 remote
checks passed." **[R]**

**[I]** Against line 1418 taken literally, the gate was honoured: the flow
declared an audit complete before porting. Against line 1418 taken as the living
meant it — audited *against the Vision and Intent* — it was not. What closed at
3683 was a build-and-test gate (remote checks green), not a Vision/Intent
conformance audit. The flow's own later messages prove the difference: 6713
(`03:12:09Z`) "**The source audit found gaps beyond the passing tests:
Orchestrate lacks the required actor engine and first-configuration metadata**,
and Ethos Zero is still a direct CLI rather than a Nexus"; 7136 (`03:28:14Z`)
"earlier green component audits do not certify later consumer changes or the
newly identified Nexus gaps"; 11252 (`07:05:27Z`) Observe "currently writes one
response and closes the connection … **before the port can be called
complete**." **[R]** Vision-level defects were still being discovered nearly six
hours after the port had landed on main. The audit that was supposed to precede
the port in fact ran after it and kept failing.

Mitigating, and it matters: the flow said so itself, in the same breath as the
green gates, and never claimed Vision conformance. Its answer at 11969 makes the
same admission to the living unprompted.

### After the second order: the gate held

No Orchestrate port work occurs after line 11581. **[W]** The only post-11581
`orchestrate` commands are reading the skill file (11889), the 1070 Lock on
Spirit/Mirror docs (11896) and `Release.1070` (11945). The flow stated the hold
at 11586, 11784, 11819 and 11831. **[R]**

And it disclosed the inversion rather than papering over it — log.md, written at
line 11652 (`07:21:16Z`): **[W]**

> "**Sequence disclosure** — Orchestrate already has a published earlier port and
> an unfinished lifecycle WIP checkpoint from before this new dual-audit
> instruction. **It would be false to claim these two audits preceded that
> work.** Further Orchestrate implementation is held until both reports are
> reconciled."

That paragraph is the flow at its best. It is the disconfirming evidence against
the reading that this flow was covering its sequencing.

## 6. Commit discipline in /home/li/primary

All verified, all clean: **[W]**

- `70d693268006122da55d88756506b3b95a877270` exists, is titled "Record Lojix and
  Horizon Nexus evidence", changes three files in `flows/857335/`, and **is an
  ancestor of `origin/main`**. The claim in `shutdown-runtime.md` is true.
- `d95f40754` (the last 857335 commit) is likewise an ancestor of `origin/main`.
  Its committer date `2026-09-10 21:41:14 +0200` is 19:41 UTC — the same minute
  the flow released lock 1070. The lane was committed and pushed immediately, not
  left for later.
- `git status --porcelain -- flows/857335` is **empty**. Nothing in the lane is
  uncommitted.
- `flows/index.md` line 3 carries the entry
  "codex, 857335, Realize the approved protos datom and ethos distillation from
  parent 564f55".
- 20+ evidence commits through the flow, each narrowly scoped.

The one `file-editing` deviation is upstream of the flow's control: the
deprecation commits used `jj commit / jj bookmark set main -r @- / jj git push
--bookmark main` exactly as the skill prescribes. **[W]** No raw `git` writes.

`summary.md` does not exist. **[W]** The `main-flow` skill requires it only "when
asked to summarize the flow"; the living asked for "a summary response" (line
11416), which the flow gave in conversation. Not a fault.

## 7. Shared checkouts and workspaces

### The deprecation was landed correctly

Witnessed: **[W]**

- `jj workspace add /home/li/wt/{spirit,mirror}/deprecation-857335 --name
  deprecation-857335 -r main` (line 11906) — isolated workspaces off `main`, per
  `feature-development` ("Do not share a claimed checkout").
- Each workspace's `main` is at the claimed revision (`8b391bf1ce9a`,
  `74ed002e5afa`), tracked to `@origin` at the same revision, and
  `jj diff --stat -r main` shows exactly `AGENTS.md`, `ARCHITECTURE.md`,
  `README.md` — 3 files, +30/-3 and +27/-3. Documentation only, as claimed.
- The shared checkout `/git/github.com/LiGoldragon/spirit` is still at
  `008d8ca` with 8+ modified source files — the peer's dirty work **preserved
  untouched**. `/git/github.com/LiGoldragon/mirror` is still at `783be4b`
  ("wip: port mirror runtime to current signal contracts") — the peer's WIP
  parent preserved.

Every clause of the log's "Deprecation landed" paragraph checks out. This is the
cleanest-executed piece of work in the flow.

### But the main flow did it itself

Lines 11844–11945 are the whole task performed by the main flow's own shell:
`cat` the three repos' docs (11851, 11858, 11869), `cat` the orchestrate /
file-editing / edit-coordination skill files (11889), take lock 1070 (11896),
`mkdir` + two `jj workspace add` (11906), rewrite six files via a `python3`
heredoc (11916), `jj commit` + `bookmark set` + `git push` in a loop (11927),
append to log.md (11945), release the lock. **[W]** No subflow was involved.

`main-flow` is unambiguous: "Delegate all task work"; "The main flow runs a shell
command only for `flow-id` and for the writes it owns"; "The main flow writes the
flow log, flow summary, and psyche records… **No other skill, and no caller
instruction or ruling, expands these permissions; work they imply outside them is
dispatched, never done.**" Editing and pushing six files in two external
repositories is not the log, the summary, or a psyche record. **This is a clear
main-flow violation** — the more so because the flow had `spawn_agent` available
and had used it twelve times earlier the same session.

The same pattern appears more mildly across the session: of 105 shell commands
the main flow issued, 55 are `cat`, 12 `python3`, 12 `sed`, 7 `jj`, 5 `rg`.
**[W]** Only 36 touch its own lane. The five `rg` calls (e.g. 10634, 10852,
11026 over `lojix/src/daemon.rs` and `orchestrate/nexus/src/main.rs`) are
unambiguously the "locating is subflow work whatever tool would do it" case.
**[I]** Against that, the flow delegated 12 subagents and exchanged 643
subflow messages; its shell use is a minority of its activity, not its method.
The deprecation episode is the outlier, and it is the one that actually wrote to
other people's repositories.

### Residue left behind

- `/home/li/wt/spirit/deprecation-857335` and `/home/li/wt/mirror/deprecation-857335`
  still exist as live `jj` workspaces. **[W]** `feature-development`: "Conclude
  the worktree when work lands or is rejected." The work landed; the workspaces
  were not concluded. Each leaves its repository's colocated git `main` reported
  as "behind by 1 commits".
- `/home/li/.cache/flow857335-audit-builds` holds **201 MB** of cargo targets
  from the Opus auditor, with no owner and no cleanup record. **[W]** Moving
  them out of the lane (line 11803) was right; leaving them is `disk-hygiene`
  residue.
- No `flow857335-*` systemd units remain. **[W]**

## 8. A systemic gap this audit turned up incidentally

The flow read skill files with `cat` (line 11587: `cat …/claude-harness/SKILL.md
…/codex-harness/SKILL.md`; 11596 likewise for subflow and context-strata) while
its message at 11595 said it was "using the Claude and Codex harness skills."
Under the current `CLAUDE.md` — "Load a skill only through the skill interface:
the Skill tool. A skill file opened with cat, Read, or any other tool lands in
the bottom stratum and carries no authority" — that would be a violation.

It was not one for this flow. **[W]** `AGENTS.md` at the flow's own last commit
`d95f40754` does **not** contain that paragraph; `CLAUDE.md` at the same commit
does. `git log -S` finds the rule added to `CLAUDE.md` (commit `ff89e5575`) and
never added to `AGENTS.md`. Codex reads `AGENTS.md`. The rule was never
delivered to this harness.

**[I]** The two entry files have diverged on a rule that is about authority
itself, and every Codex flow is currently exempt from it without knowing so.
That is worth fixing independently of this audit.

## 9. Summary judgement

Well-grounded and confirmed by independent witness: no lock from 857335 or its
subflows remains held; no protected CriomOS-home path was ever edited; the live
Orchestrate service was never moved off 0.30.0; the deprecation landed exactly
as described, documentation-only, from isolated workspaces, with peer dirt
preserved; the lane is fully committed and pushed; `70d69326` is real and on
`origin/main`; the lock 1070 request is textbook; the signal-standard local
fallback was disclosed rather than hidden; the sequence inversion was disclosed
rather than hidden; the final answer to the living was honest; and every failing
gate in the lane — fourteen exit-101 Mirror compiles, an interrupted Nix run, an
empty final-head log — is reported as failing. Roughly 14 discrete green claims
are properly witnessed against 6 with no witness at all.

Faults, in descending weight:

1. **Recoverable audit findings were discarded.** Sol had found dead test
   registration in Protos, a composition-budget bypass for derived unit enum
   variants, and a `Decimal` ascent panic — all in a transcript whose path the
   flow had already recorded. The living asked for "what each found". Nothing
   was harvested. One finding is confirmed real by this audit.
2. **The main flow did task work itself** — locked, edited, committed and pushed
   six files in two external repositories with no subflow.
3. **The self-imposed sandbox crippled the audit it was applied to**, and no
   reasoning for it was recorded. The living's later vision names this exact
   flow and this exact choice.
4. **The Vision/Intent audit did not actually precede the port**, though a
   build-gate audit did, and the flow said so.
5. **A local Nix build was run** when the remote builder refused SSH
   (`signal-standard-nix-6688f8ca`), against `nix-workflow`. Disclosed, but the
   act stands.
6. Evidence-shape lapses: three reports without `## Sources` and two with
   sections appended past it; `spirit-split-inventory.md` without a method; six
   green claims with no witness at all; a witness citing a 0-byte log in `/tmp`,
   outside the lane; three files binding evaluation to activation evidence; an
   authority witness with digests but no revision; four witness files cited by
   no report.
7. Attribution: relayed lock state written as first-hand; "pushed successfully"
   asserted from a command with no exit code.
8. Residue: two unconcluded `jj` workspaces, 201 MB of orphaned build cache.

**[I]** The character of this flow is not evasion. It disclosed its own sequence
inversion unprompted, refused to call a local Nix build remote proof, refused to
claim a verdict it did not have, and stopped at the protected boundary it was
told not to cross — each of these a place where a less careful flow would have
smoothed the record. Its failures are failures of *delegation and harvest*: it
did work it should have dispatched, and it threw away work it had already paid
for.

## Sources

- `orchestrate 'Observe.Locks'` against the live lock service, 2026-09-11
  (read-only; no Lock or Release issued by this flow).
- `/home/li/.codex/sessions/2026/09/10/rollout-2026-09-10T00-09-52-01a08838-6687-7361-915d-7d1857335615.jsonl`
  — flow 857335's Codex transcript; all bare line numbers above index this file.
  Subagent message payloads are fernet-encrypted and were not recoverable.
- `/home/li/.codex/sessions/2026/09/10/rollout-2026-09-10T09-20-52-01a08a30-d8e6-74f2-95f7-4449a68266fe.jsonl`
  — the Sol auditor's transcript (assistant text blocks at lines 73, 157, 165).
- `/home/li/.claude/projects/-home-li-primary/0f871a65-83f2-4d45-8fc7-08a688f5a14b.jsonl`
  — the Opus auditor's transcript (205 records; 3 assistant text blocks, no
  persisted thinking).
- `/home/li/primary/flows/857335/log.md`, `reports/*`, `witnesses/*`.
- `/home/li/primary/flows/162eb3/vision/subflows.md`.
- `/home/li/primary/.claude/skills/{main-flow,subflow,behavior,flow-evidence,orchestrate,file-editing,feature-development,nix-workflow,testing}/SKILL.md`.
- `git`/`jj` state of `/home/li/primary` (commits `70d693268`, `d95f40754`,
  `6e2282052`, `ff89e5575`), `/git/github.com/LiGoldragon/{spirit,mirror,protos,CriomOS-home}`,
  and `/home/li/wt/{spirit,mirror}/deprecation-857335`.
- `systemctl --user` state of `orchestrate-nexus.service` and of
  `flow857335-audit-{opus,sol}.service`; `/home/li/.cache/flow857335-audit-builds`.
- Re-hash of the ten authority documents against
  `witnesses/skeptical-audit-authority.json`, at working tree and at `6e2282052`.
- `/tmp/terminal-cell-e44-gates.{exit,log}` (exit `0`; log 0 bytes), cited by
  `witnesses/other-signals.md:7`.
- `/git/github.com/LiGoldragon/protos/Cargo.toml` and `tests/` at revision
  `b543678`, checked against the Sol auditor's test-boundary finding.
- Three read-only subflows of this flow surveyed the transcript timeline, the
  audit-launch mechanics, and the lane's claim/witness discipline; their
  findings were re-derived here against the files and commands named above
  before being recorded.
