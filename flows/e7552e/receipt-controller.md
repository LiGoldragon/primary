# Proposal 2 typed receipt enforcement — proposed replacement blocks

This appendix replaces the uncaptured place/configuration/rehearsal/launch calls
in bootstrap.md. It is not permission to execute. All inputs remain candidate
fe5a6930, the private ROOT and explicit binaries. Whole-gate, final cleanup
controller, Field admission and final immutable-packet review remain required.

Stage the checker in ROOT/bin before compiling the Place. It compares semantic
lexical tokens of already typed client outputs, preserving quoted contents and
heads; it is not a second contract decoder. Any mismatch fails the phase.

```sh
cat > "$ROOT/bin/expect-receipt.py" <<'PY'
import re, sys
from pathlib import Path
pattern = re.compile(r'«(?:\\.|[^»])*»|[{}\[\]]|[^\s{}\[\]«»]+')
def tokens(text):
    values = pattern.findall(text.strip())
    return [v[1:-1].replace('\\»', '»') if v.startswith('«') else v for v in values]
actual = Path(sys.argv[2]).read_text().strip()
expected = sys.argv[1]
if tokens(actual) != tokens(expected):
    raise SystemExit('typed receipt mismatch; inspect retained private receipt')
PY
expect_receipt() { private python3 "$ROOT/bin/expect-receipt.py" "$1" "$2"; }
configure() {
 LABEL=$1; REQUEST=$2
 printf '%s\n' "$REQUEST" > "$ROOT/evidence/$LABEL.input.datom"
 pmeta "$REQUEST" > "$ROOT/evidence/$LABEL.reply.datom"
 expect_receipt "${REQUEST/#Configure./Configured.}" "$ROOT/evidence/$LABEL.reply.datom"
}
```

The place compilation becomes:

```sh
"$PLACE_COMPILER/bin/nexus-configure" "Compile.{ «$ROOT/place.datom» «$ROOT/config/nexus/proposalTwo/flow-nexus.signal» }" > "$ROOT/evidence/place.receipt"
expect_receipt "Compiled.«$ROOT/config/nexus/proposalTwo/flow-nexus.signal»" "$ROOT/evidence/place.receipt"
```

The first daemon read becomes:

```sh
pmeta Configuration > "$ROOT/evidence/unconfigured-probe.datom"
expect_receipt Unconfigured "$ROOT/evidence/unconfigured-probe.datom"
```

Each Configure invocation in bootstrap.md is called through `configure`, with
labels `nexus`, `models`, `hook`, `metaflows`, in that order and the exact same
datom payloads. This retains each request and compares the complete echoed
Configured value. No refusal head is accepted as success regardless of exit code.
Afterwards capture Configuration and verify it contains only the two synthetic
rows and explicit private paths before any rehearsal.

Rehearsal is captured and inspected before proceeding. This source pin yields
Rehearsed.Command, whose string is retained, rather than asserted to have run:

```sh
pflow 'Rehearse.{ { Mind proposalTwoSender Luna } Predecessors.0 «Report ready only.» }' > "$ROOT/evidence/sender.rehearsed.datom"
pflow 'Rehearse.{ { Mind proposalTwoReceiver Luna } Predecessors.0 «Report ready only.» }' > "$ROOT/evidence/receiver.rehearsed.datom"
private python3 - "$ROOT" <<'PY'
import pathlib, sys
root = pathlib.Path(sys.argv[1])
for side in ('sender', 'receiver'):
    text = (root / 'evidence' / f'{side}.rehearsed.datom').read_text().strip()
    if not text.startswith('Rehearsed.'):
        raise SystemExit('rehearsal refused; inspect retained receipt')
PY
```

Field records the exact hashes and reviews the complete commands for private
Herdr session/wrapper/home/hook/place and gpt-6-luna/medium. A `Rehearsed` head
alone is not approval. No Launch occurs until Field's exact command review is
recorded in the native admission receipt.

Each Launch then uses this captured helper. This cohort's success is
Started.Launched, not the example Launched.FlowId from another contract.
The helper extracts only the first FlowId field and cross-checks Current:

```sh
launch_checked() {
 SIDE=$1; TOPIC=$2
 REQUEST="Launch.{ { Mind $TOPIC Luna } Predecessors.0 «Report ready only.» }"
 printf '%s\n' "$REQUEST" > "$ROOT/evidence/$SIDE.launch.input.datom"
 pflow "$REQUEST" > "$ROOT/evidence/$SIDE.launch.reply.datom"
 ID=$(private python3 - "$ROOT/evidence/$SIDE.launch.reply.datom" <<'PY'
import pathlib, re, sys
text = pathlib.Path(sys.argv[1]).read_text().strip()
match = re.match(r'^Started\.\{\s*([0-9a-f]{6,})\s', text)
if not match: raise SystemExit('launch not confirmed; inspect receipt before cleanup')
print(match.group(1))
PY
 )
 printf '%s\n' "$ID" >> "$ROOT/evidence/flow-ids"
 pflow "Current.{ Mind $TOPIC Luna }" > "$ROOT/evidence/$SIDE.current.datom"
 expect_receipt "Current.Awake.$ID" "$ROOT/evidence/$SIDE.current.datom"
}
launch_checked sender proposalTwoSender
launch_checked receiver proposalTwoReceiver
```

If an output reports a pending/uncertain launch, stop the matrix; retain that
attempt and inspect its supported typed lifecycle. Do not blindly launch again
or omit a partially started native from cleanup because success extraction
failed. The cleanup controller must capture the private Herdr inventory and
both permaflow Inspect results even on this path. Kernel/cgroup ownership or
still-live process handles, not stale numeric IDs, must bound termination.
