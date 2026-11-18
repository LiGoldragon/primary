# Proposal 2 isolated bootstrap — raw command packet for Field review

Owner Mind flowNexus Sol/e7552e; runtime operator Field core Sol. Task a8fa,
Order zttr/e9qq. This packet is a proposal, not execution authorization. The
whole immutable gate must finish green and Core must review this packet before
Field runs it. It replaces no production unit, wrapper, place, registry or Memory.

## Inputs and boundaries

- Flow source `7a97f37c01ddcd431b05725c0758d0da81016ad7`, branch
  order-lifetime-2b25fa, worktree `/git/worktrees/flow-order-lifetime-2b25fa`.
- `FLOW_PACKAGE`: that source's `packages.x86_64-linux.default` store output.
- `CURRICULUM_PACKAGE`: same flake's `packages.x86_64-linux.curriculum`,
  pinned source `60609c55f90432782625275294636a4e396d9497`.
- `PLACE_COMPILER`: same flake's `packages.x86_64-linux.nexus-configure` output.
  These three concrete output paths must be filled from admitted build evidence;
  this packet grants no additional build/download/resource phase.
- `HERDR`: Field's installed raw Herdr executable, resolved and recorded before
  clearing environment; no production Herdr session is used.
- `HOST_PATH`: Field-reviewed executable search path, with this Flow package's
  bin first. Explicit private `XDG_CONFIG_HOME` makes every bare flow client reach
  only this place. Field rejects any embedded production Flow wrapper earlier
  in PATH. The raw configured native below is mandatory, not a PATH codex.
- Curriculum owner source packet `flows/d48a05/private-curriculum-60609c.md`
  confirms both Spirit core and Intent main-flow are required; both are selected.
- One private auth.json link to the single next-endpoint auth file is the only
  shared state. See `credential-source.md` for exact release/save provenance,
  file-backend semantics and cross-process-refresh-lock evidence limits.
- Frozen ConfigurationSnapshot confirms Luna=`gpt-6-luna`; source sets medium.
  Only two synthetic Luna addresses are declared. No production row is replayed.

## Stage files (Field only after review)

The shell below is run in Bash from an ordinary login shell, with the five reviewed
inputs above exported. Its commands create only a newly allocated directory.
Do not run the stale capsule helper. Run one block at a time and retain receipts.

```sh
set -euo pipefail
: "${FLOW_PACKAGE:?}" "${CURRICULUM_PACKAGE:?}" "${PLACE_COMPILER:?}" "${HERDR:?}" "${HOST_PATH:?}"
RAW_CODEX=/nix/store/r0k59hi2q6di7xhmqxp11vygy4hclzyy-codex-next-candidate-0.161.0-alpha.2/bin/codex
AUTH_TARGET=/home/li/.codex-next-5ck97j38j3sb/auth.json
ROOT=$(mktemp -d /tmp/proposal2-e7552e.XXXXXXXX)
chmod 700 "$ROOT"
mkdir -p "$ROOT"/{home,config/nexus/proposalTwo,config/herdr/sessions/proposal2-e7552e,runtime/nexus/proposalTwo,runtime/curriculum,runtime/codex,state,codex/sessions,source/flows,contexts,bin,evidence}
SESSION=proposal2-e7552e
# Before any credential link or child, verify reviewed absolute executables.
for PROGRAM in "$RAW_CODEX" "$HERDR" "$PLACE_COMPILER/bin/nexus-configure" \
 "$FLOW_PACKAGE/bin/flow" "$FLOW_PACKAGE/bin/flow-meta" \
 "$FLOW_PACKAGE/bin/flow-nexus-daemon" "$FLOW_PACKAGE/bin/flow-hook" \
 "$CURRICULUM_PACKAGE/bin/curriculum" "$CURRICULUM_PACKAGE/bin/curriculum-nexus"
do test -x "$PROGRAM"; done
for PROGRAM in python3 timeout git tar; do command -v "$PROGRAM"; done
printf '#!/bin/sh\nexec "%s" "$@"\n' "$HERDR" > "$ROOT/bin/herdr"
chmod 700 "$ROOT/bin/herdr"
readlink -f "$HERDR" > "$ROOT/evidence/herdr-executable"
# Required before first child: the final cleanup block below owns all starts.
: > "$ROOT/evidence/supervisors"
: > "$ROOT/evidence/flow-ids"
printf '{ proposalTwo }\n' > "$ROOT/config/nexus/flow-nexus.datom"
printf '{ proposalTwo «%s/runtime/nexus/proposalTwo» «%s/state» }\n' "$ROOT" "$ROOT" > "$ROOT/place.datom"
"$PLACE_COMPILER/bin/nexus-configure" "Compile.{ «$ROOT/place.datom» «$ROOT/config/nexus/proposalTwo/flow-nexus.signal» }" > "$ROOT/evidence/place.receipt"
# Require Compiled; a refusal or nonzero exit stops this phase.
# Fresh state: there must be no flow.sema before daemon start.
test ! -e "$ROOT/state/flow.sema"
for SPEC in \
 'psyche-belief:47384885438a86fe522b0baf68607ec3395864da' \
 'mind-belief:622f9104da1e677dbef3530249c3f2da89ca9be4' \
 'field-belief:ebeedf43f5a9df0969fae821fd2778572dd05004'
do
 NAME=${SPEC%%:*}; REV=${SPEC#*:}
 mkdir -p "$ROOT/contexts/$NAME/.git"
 git -C "/git/github.com/LiGoldragon/$NAME" archive "$REV" | tar -x -C "$ROOT/contexts/$NAME"
 printf '%s\n' "$REV" > "$ROOT/contexts/$NAME/.git/HEAD"
done
# Authored files and declarations are immutable copies, not symlinked roots.
# Detached .git/HEAD is the pinned revision metadata Curriculum reads.
printf '#!/bin/sh\nexit 0\n' > "$ROOT/bin/context-refresh"
chmod 700 "$ROOT/bin/context-refresh"
# This is a private native wrapper, not either production wrapper.
printf '#!/bin/sh\nexport CODEX_HOME="%s/codex"\nexec "%s" "$@"\n' "$ROOT" "$RAW_CODEX" > "$ROOT/bin/codex-private"
chmod 700 "$ROOT/bin/codex-private"
printf '[agents]\ncodex_executables = ["%s/bin/codex-private"]\n' "$ROOT" > "$ROOT/config/herdr/config.toml"
cat > "$ROOT/codex/config.toml" <<'CONFIG'
approval_policy = "never"
sandbox_mode = "danger-full-access"
cli_auth_credentials_store = "file"
model = "gpt-6-luna"
model_reasoning_effort = "medium"
CONFIG
# Metadata only; do not cat/hash/copy the target. Stop if not the approved file.
python3 - "$AUTH_TARGET" "$ROOT/evidence/auth-target-metadata.json" <<'PYAUTH'
import json, os, stat, sys
s = os.stat(sys.argv[1], follow_symlinks=False)
assert stat.S_ISREG(s.st_mode) and s.st_uid == os.getuid()
with open(sys.argv[2], 'x') as f:
    json.dump(dict(uid=s.st_uid, mode=oct(stat.S_IMODE(s.st_mode)),
                   device=s.st_dev, inode=s.st_ino, size=s.st_size,
                   mtime_ns=s.st_mtime_ns), f)
PYAUTH
test ! -e "$ROOT/codex/auth.json"
ln -s "$AUTH_TARGET" "$ROOT/codex/auth.json"
test "$(readlink "$ROOT/codex/auth.json")" = "$AUTH_TARGET"
```

The private environment is explicit, and carries no production Flow/Herdr/native
identity. Define it before starting any child; these wrappers are shell functions
in this operator shell, not changes to a user profile:

```sh
private() {
 env -i HOME="$ROOT/home" USER=li LOGNAME=li LANG=C.UTF-8 \
 PATH="$ROOT/bin:$FLOW_PACKAGE/bin:$HOST_PATH" \
 XDG_CONFIG_HOME="$ROOT/config" XDG_DATA_HOME="$ROOT/home/.local/share" \
 XDG_STATE_HOME="$ROOT/home/.local/state" XDG_CACHE_HOME="$ROOT/home/.cache" \
 XDG_RUNTIME_DIR="$ROOT/runtime" CODEX_HOME="$ROOT/codex" \
 CURRICULUM_CONTEXT_LAYOUT=2 \
 CURRICULUM_CONTEXT_REFRESH_PROGRAM="$ROOT/bin/context-refresh" \
 CURRICULUM_PSYCHES_REPOSITORY_DIR="$ROOT/contexts/psyche-belief" \
 CURRICULUM_MIND_CONTEXT_DIR="$ROOT/contexts/mind-belief" \
 CURRICULUM_FIELD_CONTEXT_DIR="$ROOT/contexts/field-belief" \
 CURRICULUM_RECORDS_DIR="$ROOT/source/flows" "$@"
}
pflow() { private "$FLOW_PACKAGE/bin/flow" "$1"; }
pmeta() { private "$FLOW_PACKAGE/bin/flow-meta" "$1"; }
```

## Start only private processes; keep their exact PIDs

The following event-only barrier is part of the proposed command packet. Stage
it as `$ROOT/bin/ready.py` before any process start. Python3 must be present in
HOST_PATH. Its inotify watches are installed before spawn; pidfd exit and the
startup deadline share the selector. It writes one READY/FAIL receipt to a FIFO
and stays the child's supervisor until exit. It never probes on a timer.

```sh
cat > "$ROOT/bin/ready.py" <<'PY'
import ctypes, os, selectors, signal, stat, subprocess, sys, time
fifo, pidfile, seconds, *args = sys.argv[1:]
split = args.index('--')
paths, command = args[:split], args[split+1:]
libc = ctypes.CDLL(None, use_errno=True)
fd = libc.inotify_init1(os.O_CLOEXEC | os.O_NONBLOCK)
if fd < 0: raise OSError(ctypes.get_errno(), 'inotify_init1')
for directory in sorted({os.path.dirname(p) for p in paths}):
    if libc.inotify_add_watch(fd, os.fsencode(directory), 0x100 | 0x80 | 0x4) < 0:
        raise OSError(ctypes.get_errno(), directory)
child = subprocess.Popen(command, start_new_session=True)
with open(pidfile, 'x') as f: f.write(str(child.pid) + '\n')
def stop(*unused):
    try: os.killpg(child.pid, signal.SIGTERM)
    except ProcessLookupError: pass
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGINT, stop)
selector = selectors.DefaultSelector()
selector.register(fd, selectors.EVENT_READ, 'filesystem')
pidfd = os.pidfd_open(child.pid)
selector.register(pidfd, selectors.EVENT_READ, 'exit')
def placed():
    try: return all(stat.S_ISSOCK(os.stat(p).st_mode) for p in paths)
    except FileNotFoundError: return False
end = time.monotonic() + float(seconds)
ready = placed()
while not ready:
    events = selector.select(max(0, end - time.monotonic()))
    if not events: break
    if any(key.data == 'exit' for key, mask in events): break
    for key, mask in events:
        if key.data == 'filesystem':
            try: os.read(fd, 65536)
            except BlockingIOError: pass
    ready = placed()
with open(fifo, 'w') as f: f.write(('READY ' if ready else 'FAIL ') + str(child.pid) + '\n')
selector.close(); os.close(pidfd); os.close(fd)
if not ready:
    stop()
    try: child.wait(timeout=5)
    except subprocess.TimeoutExpired:
        os.killpg(child.pid, signal.SIGKILL); child.wait()
    sys.exit(1)
sys.exit(child.wait())
PY
start_ready() {
 NAME=$1; SOCKETS=$2; shift 2
 FIFO="$ROOT/evidence/$NAME.fifo"
 mkfifo "$FIFO"
 # SOCKETS is a reviewed space-separated list under ROOT; ROOT has no spaces.
 private python3 "$ROOT/bin/ready.py" "$FIFO" "$ROOT/evidence/$NAME.pid" 30 $SOCKETS -- "$@" > "$ROOT/evidence/$NAME.log" 2>&1 &
 SUPERVISOR=$!
 printf '%s %s\n' "$NAME" "$SUPERVISOR" >> "$ROOT/evidence/supervisors"
 if ! RECEIPT=$(timeout --signal=TERM --kill-after=5s 35s sh -c 'IFS= read -r line < "$1"; printf "%s\n" "$line"' sh "$FIFO"); then
  kill -TERM "$SUPERVISOR" 2>/dev/null || :
  wait "$SUPERVISOR" || :
  return 1
 fi
 printf '%s\n' "$RECEIPT" > "$ROOT/evidence/$NAME.ready"
 case "$RECEIPT" in READY\ *) ;; *) wait "$SUPERVISOR" || :; return 1 ;; esac
}
start_ready herdr "$ROOT/config/herdr/sessions/$SESSION/herdr.sock" "$HERDR" --session "$SESSION" server
start_ready curriculum "$ROOT/runtime/curriculum/curriculum.sock" "$CURRICULUM_PACKAGE/bin/curriculum-nexus"
start_ready codex "$ROOT/runtime/codex/control.sock" "$RAW_CODEX" app-server --remote-control --listen "unix://$ROOT/runtime/codex/control.sock"
start_ready flow "$ROOT/runtime/nexus/proposalTwo/flow.sock $ROOT/runtime/nexus/proposalTwo/flow-meta.sock" "$FLOW_PACKAGE/bin/flow-nexus-daemon" proposalTwo
private "$HERDR" --session "$SESSION" workspace list > "$ROOT/evidence/herdr-probe.json"
private "$CURRICULUM_PACKAGE/bin/curriculum" 'ResolveSources.[ { Spirit core Single.0 } { Intent main-flow Single.0 } ]' > "$ROOT/evidence/curriculum-probe.datom"
pmeta Configuration > "$ROOT/evidence/unconfigured-probe.datom"
# The final probe must report Unconfigured, not a production Configuration.
```

The FIFO wait has its own35-second deadline. A supervisor failure before its
receipt stops this phase and terminates/waits only that supervisor; Field still
reconciles any recorded child group before cleanup. The roots/socket-parent
directories exist before these commands. The30/35-second startup deadlines are
proposed test configuration; accept them explicitly, without silent retry.

## Configure only fresh Memory

After those barriers, the following raw datoms are the complete test
configuration; each must answer Configured with the exact submitted family.
No HandoverPolicy, Heartbeat, production protected-address set or replay is added.

```sh
pmeta "Configure.Nexus.{ «$ROOT/source» { «$ROOT/bin/codex-private» «$ROOT/codex» «$ROOT/runtime/codex/control.sock» [ gpt-6-luna ] } { «$ROOT/bin/codex-private» «$ROOT/codex-unused» «$ROOT/runtime/codex/unused.sock» [] } [ { Codex [ / «!» ] [ esc ] [] } ] [] None None «$ROOT/runtime/curriculum/curriculum.sock» 60 None $SESSION }"
pmeta 'Configure.Models.[ { Luna gpt-6-luna } ]'
pmeta "Configure.HarnessHook.«$FLOW_PACKAGE/bin/flow-hook»"
pmeta 'Configure.Metaflows.[ { { Mind proposalTwoSender Luna } None [] [ spirit:core:0 intent:main-flow:0 ] [] Regular Default Maintained «Send only the explicitly assigned synthetic test requests. Stop after the assigned request; perform no other task.» [] } { { Mind proposalTwoReceiver Luna } None [] [ spirit:core:0 intent:main-flow:0 ] [] Regular Default Maintained «Receive the assigned synthetic requests and answer only Questions by Result and Tasks by Done when instructed. Keep each assigned identifier exact.» [] } ]'
pmeta Configuration > "$ROOT/evidence/fresh-configuration.datom"
pflow 'Rehearse.{ { Mind proposalTwoSender Luna } Predecessors.0 «Report ready only.» }'
pflow 'Rehearse.{ { Mind proposalTwoReceiver Luna } Predecessors.0 «Report ready only.» }'
```

Inspect the rehearsed commands for the private executable/home/Herdr session,
private hook/place and gpt-6-luna/medium before either Launch. Never substitute
a production wrapper if the private executable is refused.

```sh
pflow 'Launch.{ { Mind proposalTwoSender Luna } Predecessors.0 «Report ready only.» }'
pflow 'Launch.{ { Mind proposalTwoReceiver Luna } Predecessors.0 «Report ready only.» }'
```

## Matrix and successor evidence — held for reviewed exact prompts

Use one sender/receiver pair, sequentially, with a reviewed turn/time/token
budget, and close only these synthetic addresses. Native Send tool exposes only
Order, Question, Result and Notice; Task/Done/Living use the ordinary CLI from
the cheap sender's native terminal tool under the private environment. This is
existing vocabulary, not a proposed tool extension.

Record the RequestId and actual delivered/read evidence for each Order,
Question, Task, Notice and Living. A sender's native tool Result to delivered
Order must refuse Unresolved; Result to Question must route correctly; Done to
Task must resolve; wrong-kind, duplicate and unknown-id replies must refuse.
Unbound operator Question/Result additionally proves kept Answer behavior.
No Answer query wording is reinterpreted: the accepted historical Open-bit
exception is retained.

For the successor case, deliver a unique Order, Question and Task, leave the
latter two unanswered, and request Refresh only for proposalTwoReceiver. On its
actual idle/refresh event, record the new native identity and first prompt:
original Question/Task IDs and Task deadline are carried, the delivered Order's
unique marker is absent. Result/Done close the carried requests once. Distinguish
queued/placed/read observations and retain private transcript evidence. Do not
claim a submission is a read. Matrix command/prompt schedule and its observer
cuts remain owed before test execution.

## Stop and evidence custody

Field uses pmeta Close only for the two recorded synthetic FlowIds, then
terminates only the child process groups recorded in evidence/*.pid and waits
for their recorded supervisors; their pidfd/child.wait establishes exit. Never use killall or a name-only match.
Check production service/process/config identity against the pretest receipt,
without replay or restart. Preserve evidence/transcripts/config and hashes in a
separate retained report location before removing only this ROOT; unlink the
private auth link as a link, never operate on its target. Any uncertain remaining
child retains the test resource slot and is reported to Core/Field.

## Review corrections and remaining execution blockers

Core independent source review `/tmp/proposal2-bootstrap-audit.6xPziC/report.md`
accepted the isolation shape and credential-source semantics. This revision
pins bare daemon Herdr through ROOT/bin/herdr, selects both required startup
modules, uses Bash pipefail, validates tool availability, records permitted
credential metadata and reaps a FAIL supervisor. Field/Harness independently
confirmed exact selected raw source semantics (r6ix); no cross-process refresh
lock or atomic-write guarantee exists, so truncate/interleave races must be
explicitly accepted by Opus before execution. No login/logout/device login,
credential copy or mode change belongs to this test.

Still required before this packet becomes executable: enforced captured typed
Compiled/Unconfigured/Configured/Rehearsed/Started comparisons; global cleanup
trap installed before the first child; exact FlowId/native-descendant closure
and production before/after witness commands. Current snippets are not to be
run until these are replaced by a reviewed fail-closed controller. The separate
`native-matrix.md` now supplies the proposed sequence/IDs/cuts and20-minute,
12-instructed-turns-per-address budget; Opus approval requested. Neither this
review nor a green whole gate admits native execution by itself.

## Outstanding admission facts

Concrete package paths/local availability; event-ready helper review; reviewed
native matrix/budget; Field/Harness credential-source review; Core bootstrap
review/resource admission; whole gate terminal result. None is inferred from
this proposal. Source pins and raw configuration are now specified rather than
referring Field to the old2738-line capsule script.
