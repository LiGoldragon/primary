# Witness — independent read-only review of persona-test `message-flow-0174-successor-8904b1`

Reviewer: subflow of main flow 8904b1. Read-only. Nothing was built, evaluated
or run from the source; no Flow, Message or Herdr command was issued; the
worker's clone was not touched.

Scratch clone (made fresh from `git@github.com:LiGoldragon/persona-test.git`):
`/tmp/claude-1001/-home-li-wt-primary-56ae53/8904b10d-7f06-4e44-9342-3a8a2d7e17bd/scratchpad/pt`

## 1. Refs on the real remote

Method: `git ls-remote git@github.com:LiGoldragon/persona-test.git`.

    c1a23704537813764bf2c416544b87ec337d86d3  HEAD
    c1a23704537813764bf2c416544b87ec337d86d3  refs/heads/main
    b570bce4f25d955fbb17dbe0172a8d2460532dc7  refs/heads/message-flow-0174-8904b1
    f9b50b7605613535e96bc1a5ccba127e06383ffd  refs/heads/message-flow-0174-successor-8904b1

All three match the claim exactly. No other ref exists (no tags, no other
branches). Parent of `b570bce4` is `e3505bfd6732990e84f867a8850ae09ff6ae0d65`,
as claimed (`git log -1 --format=%P`).

## 2. Lock listing

Method: `/home/li/.nix-profile/bin/orchestrate 'Observe.Locks'`, once.

Seventeen locks returned: 988, 1019, 1805, 1819, 1820, 2969, 5477, 6094, 7350,
7435, 7608, 7654, 7815, 7880, 8189, 440, 441. **8200 and 8263 are absent.** No
lock's path vector names a persona-test path; the closest are CriomOS-home and
flow-0174 staging paths held by flows 6fe957 and 56ae53.

## 3. The successor commit

Method: fresh clone, `git log`, `git diff --stat c1a2370 f9b50b7`.

Parent of `f9b50b7` is `c1a23704537813764bf2c416544b87ec337d86d3` — main, as
claimed. Subject: `message-flow: stand-in and live modes on main c1a2370
(successor)`. Trailers: `Co-Authored-By: Claude Fable 5.1
<noreply@anthropic.com>` and `Claude-Session:
https://claude.ai/code/session_01PeQ7sVJXjFg3BHZT1Yy45K`.

19 paths change, +2312 / −135. New files: `checks/message-flow-stand-in.nix`,
`fixtures/herdr/codex-executable-selection.patch` (540 lines),
`fixtures/message-flow/oracle.py` (381), `fixtures/message-flow/stand_in.py`
(327), three fixture SKILL.md files, `lib/components/claude-stand-in.nix`,
`lib/components/flow-id.nix`. Changed: `README.md`, `flake.nix`, `flake.lock`,
`checks/message-flow-binaries.nix`, `lib/default.nix`, `lib/components/{flow,
herdr,message}.nix`, `packages/message-flow.nix` (+535/−… , now 495 lines),
`fixtures/message-flow/flow-system-prompt.md`.

`flake.lock` pins: flow `bc464e5e1b94fcc179af73111f43b69db1f69fc5`, herdr
`9eb521456ac0d19d3ab3d9d7cea3cca10baa8a4c`, harness
`d022427938c0925e55e23dfb2d7ba470bbfea3c1`, message
`f1843dbaa63f38634dc10d3b28df2f4a482d6d35` — each equal to the corresponding
`flake.nix` URL revision.

## 4. Design conformance

### a. Two modes kept apart; stand-in the default and the only checked mode — **met**

`packages/message-flow.nix:102` — `mode="''${1:-stand-in}"`. Unrecognised mode
exits 64 (`:130-134`).

Three checks exist. `checks/message-flow-stand-in.nix:20` —
`timeout 900 ${perSystem.self.message-flow}/bin/message-flow stand-in`, and
`:19` sets `PERSONA_TEST_ROOT_BASE="$TMPDIR"`. `checks/message-flow-binaries.nix`
only realises packages, `test -x` on ten binaries and `python3 -m py_compile` on
the two Python files. `checks/lint.nix` is nixfmt/deadnix/statix. No check
names `live-claude` or `live-codex`.

### b. Live modes reachable only by explicit caller choice — **met**

`live-claude` requires argv 2 as an absolute executable path
(`:109-111`: `requireAbsolute "the real Claude executable" "$realClaude"`, then
`[ -x "$realClaude" ] || … exit 70`). `live-codex` requires all three of
`PERSONA_TEST_CODEX_CLIENT`, `PERSONA_TEST_CODEX_HOME`,
`PERSONA_TEST_CODEX_CONTROL_SOCKET`, each `requireAbsolute` (`:114-119`);
`requireAbsolute` exits 70 when unset or relative (`lib/default.nix:22-30`).
Neither can be reached from a check or the default run.

### c. No login in stand-in — **met**; live authentication is by copied file — **observed**

`packages/message-flow.nix:177-191`: `${flake.lib.seatCredentialEnv}` is inside
`if [ "$mode" = live-claude ]`; the `else` branch makes
`$stateRoot/seat/home/.claude` and `$stateRoot/seat/work` fresh. The caller's
`$HOME` is read only at `:178` (`realHome="$HOME"`), inside that same branch.
No gopass, no API-key variable, no `CLAUDE_CONFIG_DIR`/`CODEX_HOME` read from
the caller: both are *set* outward, to run-owned paths
(`lib/components/flow.nix:57-58`, `lib/components/herdr.nix:73`).

In `live-claude`, authentication reaches the run as two file copies
(`lib/default.nix:104-115`): `$realHome/.claude/.credentials.json` →
`$seatHome/.claude/.credentials.json` and `$realHome/.codex/auth.json` →
`$seatCodexHome/auth.json`, each `chmod 600`. From `~/.claude.json` only
`.oauthAccount` is extracted with `jq` (`:119`). **No secret is passed by argv
or environment.** It is passed by file, inside the `mktemp -d` root, removed by
the exit trap. In `live-codex`, `seatCredentialEnv` is *not* called at all; the
caller's `PERSONA_TEST_CODEX_HOME` path (which presumably holds `auth.json`) is
handed to flow-nexus as `FLOW_CODEX_*_HOME` — a path in the environment, not a
secret value.

Residual exposure (observation, not a rule violation): in `live-claude` the
live credential file exists as a copy under `/tmp/pt.XXXXXXXX` for the run's
duration; `mktemp -d` gives 0700 and the file 0600.

### d. Scratch paths — **met in substance, one stated check absent**

`lib/default.nix:66-78`: `rootBase="''${PERSONA_TEST_ROOT_BASE:-/tmp}"`,
`requireAbsolute PERSONA_TEST_ROOT_BASE "$rootBase"`, then
`stateRoot="$(mktemp -d "$rootBase/pt.XXXXXXXX")"`. Every per-component HOME and
XDG_RUNTIME_DIR is derived under `$stateRoot`
(`packages/message-flow.nix:150-159`), and each is re-checked absolute before
its component starts (`flow.nix:38-40`, `message.nix:22-24`, `herdr.nix:63-65`).

There is **no explicit comparison against the user's live HOME or
XDG_RUNTIME_DIR**. Inference: the comparison is unnecessary, because `mktemp -d`
always appends a fresh `pt.XXXXXXXX` component, so no derived path can equal
`/run/user/<uid>/flow`, `~/.local/state/flow` or `~/.config/herdr`, whatever
`PERSONA_TEST_ROOT_BASE` is set to. The design point is satisfied by
construction rather than by a check.

`env -i`: used for flow-nexus (`flow.nix:53`), message-nexus (`message.nix:27`),
the Herdr server (`herdr.nix:68`), every Herdr CLI call (`herdr.nix:87`) and
every Flow client call (`flow.nix:73`, and
`packages/message-flow.nix:238,277,284,432,434`).

`HERDR_SOCKET_PATH`, `HERDR_SESSION`, `HERDR_ENV` are **not cleared in the
runner's own shell** — the runner inherits the caller's environment. They are
nevertheless cleared for everything that could act on them, because every Herdr
and Flow invocation goes through `env -i` and names `--session` /
`FLOW_SOCKET` explicitly. `herdr.nix:16-17` states the intent: "an explicit
`--session` wins over any socket variable". Processes that do inherit the
caller's environment are `jq`, `cp`, `sha256sum` and `python3 oracle.py`, none
of which reads those variables.

### e. Stop by held PID; trap — **met, with one qualification**

`flowNexusPid` (`flow.nix:65`, killed `:79`), `messageNexusPid`
(`message.nix:32`, killed `:38`), `herdrServerPid` (`herdr.nix:80`; `server
stop`, then `kill "$herdrServerPid"` at `:101-107`). No `killall`, no `pgrep`.

The one `pkill` in the tree is `packages/message-flow.nix:279` —
`pkill -P "$observer"`: selection is by *parent PID*, a PID the scenario holds,
not by name or path pattern. It reaps the background `observeLaunch` subshell's
children.

Seat processes are never killed by the scenario at all: `seatProcesses`
(`:246-249`) enumerates descendants of `$herdrServerPid` via
`oracle.py processes` (which walks `/proc/<pid>/stat` parent links —
`oracle.py:145-176`) and filters argv basename `claude`; the scenario then only
*waits* for them to vanish (`:390-401`). The name filter is used for
observation, never for signalling.

Cleanup: `trap cleanup EXIT` (`lib/default.nix:77`); `cleanup` calls
`beforeRootRemoval` (defined `packages/message-flow.nix:208-215`, stopping
Flow, Message and Herdr and printing the report) then `rm -rf "$stateRoot"`.
`writeShellApplication` sets `set -euo pipefail`, so an errexit failure runs the
EXIT trap. Qualification: only `EXIT` is trapped — `INT`/`TERM`/`HUP` are not,
so a killed run leaves `$stateRoot` (and in `live-claude`, the copied credential
file) behind.

### f. One Herdr; isolation; socket length — **met**

`lib/components/herdr.nix` is the single Herdr component; one server, one
session `persona-test` (`packages/message-flow.nix:160`). Own
`XDG_CONFIG_HOME`, `XDG_STATE_HOME`, `XDG_RUNTIME_DIR`, all under `$stateRoot`
(`:156-158`, `herdr.nix:70-72`), `chmod 700` on the runtime directory.

`packages/message-flow.nix:166-172` loops `requireSocketLength` over six
sockets: Flow ordinary and meta, Message ordinary and meta, and Herdr's
`herdr.sock` and `herdr-client.sock` — before anything starts.
`requireSocketLength` (`lib/default.nix:31-37`) refuses over 107 bytes, exit 70.

### g. One build of Flow bc464e5e; socket always named — **met**

`lib/components/flow.nix:21-24`: `package = inputs.flow.packages.${system}.default`,
and `nexus`, `client`, `metaClient` are all `${package}/bin/…` — one build.
`flake.nix:11` pins `github:LiGoldragon/flow/bc464e5e…`; `flake.lock` agrees.

Every client invocation sets `FLOW_SOCKET` under `env -i`. `flow.nix:6-9`
records why: "the `flow` client falls back to the live socket when FLOW_SOCKET
is unset". I found no invocation of `${flow.client}` or `${flow.metaClient}`
without an explicit `env -i FLOW_SOCKET=…`. No path by which a 0.17 client here
could reach the host's stable socket.

### h. Service binaries run with no argument — **met**

`flow.nix:64` starts `${nexus}` with no argument; `message.nix:31` likewise.
Neither is run with `--version` or any help option anywhere in the tree; the
only `--version` occurrence is inside a comment (`flow.nix:12`). Herdr is run as
`herdr --session <name> server` (`herdr.nix:79`) and, for calls, `pane get`,
`pane close`, `server stop`. `grep` for `--help` over the tree: no hit.

### i. Unused cleanup helper resolved, not silenced — **met**

`grep -rn shellcheck` over all `*.nix` and `*.py` in the successor: **zero
hits**. Same grep over `c1a2370`: zero hits. So no disable directive was added
(and none existed to inherit). The helper is genuinely used:
`beforeRootRemoval` is defined in `packages/message-flow.nix:208` and invoked by
`lib/default.nix:71` via `if declare -F beforeRootRemoval >/dev/null`.

## 5. The oracle's independence

`fixtures/message-flow/oracle.py` imports nothing from Flow (`hashlib, json, os,
re, sys` only). Its expectations are written into it: `FOOTER` (`:23-26`),
`RECEIPT` (`:27`), the stacked/direct first-prompt templates
(`expected_text`, `:250-258`), and Claude Code's skill-expansion form
(`expansion`, `:190-197`).

Genuinely external computation:
- `prompt-hash` (`:286-291`) — `hashlib.sha256` of the transcript text *less
  the footer*, read from the seat's own `.jsonl` on disk, compared against the
  hash **Flow** reported. Two independently produced artifacts, not a value read
  back from Flow and compared to itself.
- `first-entry-bytes` (`:300-304`) — the typed text against the oracle's own
  template.
- `skill-expansions` (`:318-329`) — each expansion recomputed from the SKILL.md
  file on disk.
- `model` / `effort` (`:336-343`) — read from the transcript's assistant rows,
  compared with the intent the runner passed.
- `processes` / `alive` — read from `/proc` directly.

Not independent: `route` (`:278-282`) compares the stand-in's own paste-wrapping
decision (`stand_in.py:189-198`) against a per-case literal (`true`/`false` in
`runCase`). In stand-in mode this witnesses the fixture's reimplementation of
Claude Code's paste rule, not Flow and not Claude.

Must-fail cases:

| case | what is made wrong | what the oracle concludes from |
| --- | --- | --- |
| D | the skill list contains `absent-skill-message-flow`, for which no `SKILL.md` exists (`message-flow.nix:487`) | **weak.** Accepts `first_failed` ∈ {`first-entry-present`, `transcript-located`, `no-native-session`} (`:346`) — i.e. "the seat was never given its first prompt". These are the same symptoms as *any* failure to start. It does not distinguish "refused because the skill could not load" from "refused for an unrelated reason". |
| E | stand-in behaviour `other-model`: assistant rows are written with `claude-sonnet-5` instead of the intended `claude-haiku-4-5-20251001` (`stand_in.py:29,184-187`) | `first_failed` must be exactly `model` — meaning `transcript-located`, `first-entry-present`, `footer-present`, `prompt-hash`, `bundle-copy`, `first-entry-bytes`, `one-entry`, `skill-expansions`, `receipt` all passed first. Discriminating. Note `claude-sonnet-5` *is* in Flow's display map, so the refusal is a model mismatch, not an unmapped identifier. |
| F | stand-in behaviour `footer-dropped`: records the prompt with Flow's receipt footer removed (`stand_in.py:176-177`) | `first_failed` must be exactly `footer-present`. Discriminating: `prompt-hash` is only reached after the footer check. |
| J | stand-in behaviour `body-altered`: footer kept, the last byte of the body changed (`stand_in.py:178-181`) | `first_failed` must be exactly `prompt-hash`, with `footer-present` having passed. Discriminating, and cleanly separated from F by check order. |

## 6. The stand-in

`fixtures/message-flow/stand_in.py` is a ~330-line Python program that draws a
minimal Claude screen (`Screen.idle`, `:128-131`), sends Herdr the
`pane.report_agent_session` request Herdr's own Claude hook sends
(`:143-173`), reads the pane's tty in raw mode handling bracketed paste
(`:274-323`), and appends Claude-Code-shaped JSONL rows for the first turn,
skill loads and a `FLOW_LAUNCH_RECEIPT_V2` reply.

It is labelled loudly. `stand_in.py:1-7`: "This is **NOT** Claude and witnesses
nothing about Claude." `lib/components/claude-stand-in.nix:10-15`: "THE
STAND-IN IS NOT CLAUDE… A run on the stand-in witnesses nothing about the
Claude harness." `checks/message-flow-stand-in.nix:6-7`: "It witnesses nothing
about the Claude harness: the seat is the stand-in, which is not Claude."

The printed report labels the mode on its second line
(`packages/message-flow.nix:223`):

    say "mode: $mode$([ "$mode" = live-claude ] && printf ' (%s)' "$realClaude")"

so a stand-in run's report reads `mode: stand-in`. Per case it prints
`case A — seat stand-in faithful — expect started` (`:272`, seat string set at
`:476` to `stand-in faithful`). Inference: the mode is unambiguous to a reader
who reads the report, but the report header itself contains no sentence saying
"this witnesses nothing about Claude" — the word `stand-in` alone carries it.
A reader who sees only `cases failed: 0` and the header could take it as a
green live witness. Low risk, not zero.

## 7. The worker's three claims about main (c1a2370)

**(i) The nixpkgs Herdr main used lacks the configuration key main writes —
confirmed by reading.** Main's `lib/components/herdr.nix` uses
`inputs.nixpkgs.legacyPackages.${system}.herdr` and writes
`[agents]\ncodex_executables = [ "…" ]`. The successor's patch
`fixtures/herdr/codex-executable-selection.patch` *adds* that key: it inserts
`"agents"` into `KNOWN_TOP_LEVEL_CONFIG_KEYS` (`src/config/io.rs`), adds
`load_live_section(table, "agents", …)`, and defines
`pub struct AgentsConfig { pub codex_executables: Vec<PathBuf> }` with
`pub agents: AgentsConfig` on `Config` (`src/config/model.rs`). So the key does
not exist upstream at v0.8.2, and a fortiori not in nixpkgs' older build:
main's config file named a key its Herdr would not read.

**(ii) Main's model identifiers are unmapped in Flow's display map at bc464e5e —
confirmed by reading.** Main's `lib/default.nix:102-105` has
`claude = "claude-haiku-4-5"` and `codex = "luna"`. Flow bc464e5e
`crates/flow-nexus/src/title.rs:19-36` lists sixteen exact identifiers; it
contains `claude-haiku-4-5-20251001` and `gpt-6-luna` but neither
`claude-haiku-4-5` nor `luna`. The module header states: "An unmapped model
identifier is refused; no alias and no fallback is accepted", and
`NativeTitle::for_flow` returns `TitleRefused::UnmappedModel` (`:66-67`).
Qualification: this establishes that the *title* is refused. That the refusal
aborts the start (rather than only the titling step) I did not trace further;
the successor's `lib/default.nix:146-153` asserts it does and now uses the two
mapped identifiers.

**(iii) The endpoint now reaches Flow by documented overrides — confirmed by
reading.** `packages/message-flow.nix:121-128` builds
`FLOW_CODEX_{STABLE,NEXT}_{CLIENT,HOME,SOCKET,MODELS}` and
`lib/components/flow.nix:63` passes them into the `env -i` line, after
`:41-50` checks each is a `FLOW_*=/absolute` word (or a `_MODELS` list). Flow
bc464e5e reads exactly these: `crates/flow-nexus/src/store.rs:294-303`
(`FLOW_CODEX_{prefix}_CLIENT`, `_SOCKET`, `_HOME`, `_MODELS`), documented at
`store.rs:240` and `DESIGN.md:167` as deployment overrides applied at start.

## 8. What a stand-in run touches outside its root

Network: none. `grep` for curl, wget, `http://`, `https://`, `urllib`,
`requests` over `*.nix`/`*.py`: no hit outside `flake.lock`. The only socket in
the tree is `socket.AF_UNIX` in `stand_in.py:163`, connecting to
`$HERDR_SOCKET_PATH` — this run's Herdr, inside the root. The
`message-flow-stand-in` check runs in the build sandbox, which has no network.

Writes: all under `$stateRoot`. Outside it, the runner creates only
`$rootBase/pt.XXXXXXXX` itself (default `/tmp`; `$TMPDIR` in the check).

systemd / user services: none. `grep -i` for systemd, systemctl, loginctl: no
hit. The README (`:113-116`) *recommends* the operator run a live form as a
transient unit, but the code creates none.

## 9. Tests by text

No check searches or compares source text. `message-flow-binaries` realises the
pinned derivations, `test -x` the ten binaries, and `py_compile` the two Python
files — a smoke check on built artifacts, not a text search.
`message-flow-stand-in` runs the real flow-nexus, message-nexus and Herdr
server and drives seven cases through them. `lint` is formatting.

The oracle's `first-entry-bytes` and `expected_text` compare *runtime output*
against an external specification written in the oracle — legitimate, since the
typed text is the product. Observation worth naming: because that specification
is Flow's prompt wording transcribed by hand, the check goes red on any wording
change in Flow, whether or not behaviour changed.

## 10. Stated absences

Cases G, H, I and K: **not present in the source** (only A, B, C, D, E, F, J are
run, `packages/message-flow.nix:484-490`) and **not named anywhere**. Neither
the README nor any source comment mentions G, H, I or K, nor says that the
lettering has gaps. A reader of the README (`:73-79`) sees a list of seven
cases with no indication that four planned ones are missing.

Message not driven: **stated**. The report prints
`message revision: … (started, not driven)` (`:227`).  The README does not
repeat it; its scenario table lists Message 0.16 as a component without saying
it is only started.

No Codex transcript oracle: **stated twice**, in the header comment
(`packages/message-flow.nix:30-32`) and in the README (`:111`): "No transcript
oracle is written for Codex yet."

## Defects found, by gravity

1. **Case D's oracle does not establish the reason for the refusal.** It
   accepts any of three "the seat never got its prompt" outcomes
   (`:346`). A Flow that refused case D for an unrelated reason — a socket
   error, a Herdr failure, an unmapped model — would be scored `ok`. Case D
   therefore proves only "this start did not happen", not "an unloadable skill
   stopped it". D is the only must-fail case with this weakness; E, F and J
   each pin an exact first-failed check.
2. **Four planned cases (G, H, I, K) are absent and their absence is nowhere
   stated.** A reader of the README or the printed report has no way to learn
   that the lettering has gaps. Consequence: the scenario reads as complete when
   it covers seven of eleven planned cases.
3. **Only `EXIT` is trapped.** `INT`, `TERM` and `HUP` are not
   (`lib/default.nix:77`). Consequence: a `live-claude` run killed with Ctrl-C
   or SIGTERM leaves `$stateRoot` — including the copied
   `.credentials.json` — in `/tmp`, and leaves its flow-nexus, message-nexus and
   Herdr server running.
4. **The `route` check tests the fixture, not the system.** In stand-in mode it
   compares `stand_in.py`'s own reimplementation of Claude Code's
   800-UTF-16-unit paste rule against a per-case literal. Consequence: case B's
   headline property — that a long first prompt arrives wrapped — is witnessed
   only in `live-claude`, and a green stand-in run does not establish it.
5. **The runner's own shell is not `env -i`.** `HERDR_SOCKET_PATH`,
   `HERDR_SESSION`, `HERDR_ENV` from the caller survive in the runner process.
   Consequence: today none of the processes that inherit them (`jq`, `cp`,
   `python3 oracle.py`) reads them, so nothing leaks; but the guarantee rests on
   every future Herdr/Flow call remembering its `env -i`, not on the shell.
6. **No explicit refusal when a derived path would equal a live one.** The
   design point asks for a check; the code relies on `mktemp -d` making
   collision impossible. Consequence: correct today, but the invariant is
   implicit — a future change that derives a path without `mktemp` would not be
   caught.
7. **`live-claude` copies a live credential file into `/tmp`.** 0700 directory,
   0600 file, removed on normal exit. Consequence: bounded but real exposure for
   the run's duration, compounded by defect 3.
8. **The printed report's mode line is terse.** `mode: stand-in` is accurate but
   the report carries no sentence saying the run witnesses nothing about the
   Claude harness — that sentence lives only in the source and README.

## What I could not establish by reading

- Whether the scenario actually passes. Nothing was built or run, so the
  worker's "bounded build green; a mutated expectation was seen turning it red"
  is an unverified claim; I saw no artifact of that run.
- Whether Flow bc464e5e aborts a *start* on an unmapped model, or only fails to
  title it. I confirmed `TitleRefused::UnmappedModel` exists and is returned;
  I did not trace its callers to the Start path.
- Whether the Herdr patch applies cleanly to `9eb52145` and whether the patched
  Herdr builds. That needs a build.
- Whether the patch is byte-identical to the one CriomOS-home applies at
  `bde3bb7f`, as the comment in `lib/components/herdr.nix:8` claims; I did not
  fetch CriomOS-home to diff it.
- Whether the oracle's transcript-shape assumptions (`isMeta`/`turnCompanion`
  companion rows, `<pasted_content>` wrapping, the
  `<command-message>`/`<command-name>` form) match what the real Claude harness
  writes. In stand-in mode both sides of that shape are written by this
  repository, so a green run confirms only self-consistency.
- Whether case E, F and J's expected `first_failed` values are actually reached
  in practice, or whether an earlier check fails first for an incidental reason.
- Whether locks 8200 and 8263 ever existed. I observed only that they are absent
  now; absence is consistent with release and with never having been taken.
