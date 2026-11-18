# Proposal 2 production witness — proposed read-only commands

This appendix supplies the missing pre/post definitions. Field runs it only
within its admitted native packet. Private roots are environmental isolation,
not a kernel filesystem sandbox: `danger-full-access` permits native terminal
access beyond ROOT. The exact bounded synthetic prompts and operator admission
are the work boundary. No OS-level filesystem isolation is claimed.

Before clearing the private environment, record the reviewed production inputs:
REAL_HOME=/home/li; REAL_RUNTIME is the actual user's XDG_RUNTIME_DIR;
PRODUCTION_FLOW_UNIT is the actual serving Flow unit confirmed by Field's
fresh metadata (earlier inventory: flow-nexus-0550.service). This is not a
permission to restart, reconfigure or replay that unit. The native test's private
unit/scope, if admitted for ownership, must have a distinct reviewed name.

```sh
: "${REAL_HOME:?}" "${REAL_RUNTIME:?}" "${PRODUCTION_FLOW_UNIT:?}"
PROD_FLOW="$REAL_HOME/.local/bin/flow"
PROD_META="$REAL_HOME/.local/bin/flow-meta"
capture_production() {
 SIDE=$1
 env -i HOME="$REAL_HOME" XDG_RUNTIME_DIR="$REAL_RUNTIME" \
   PATH="$HOST_PATH" "$PROD_META" Configuration \
   > "$ROOT/evidence/production-$SIDE.configuration.datom"
 # Typed whole Configuration must be present; refusal is a failed witness.
 python3 - "$ROOT/evidence/production-$SIDE.configuration.datom" <<'PY'
import pathlib, sys
assert pathlib.Path(sys.argv[1]).read_text().strip().startswith('Configuration.')
PY
 env -i HOME="$REAL_HOME" XDG_RUNTIME_DIR="$REAL_RUNTIME" \
   PATH="$HOST_PATH" "$PROD_FLOW" 'Current.{ Psyche core Fable }' \
   > "$ROOT/evidence/production-$SIDE.fable-current.datom"
 systemctl --user show "$PRODUCTION_FLOW_UNIT" energy-nexus.service \
   energy-translator.service harness-daemon.service \
   -p Id -p MainPID -p ExecMainStartTimestampMonotonic -p ExecStart \
   -p FragmentPath -p ActiveState -p SubState \
   > "$ROOT/evidence/production-$SIDE.services"
 for NAME in flow flow-meta flow-hook; do
   printf '%s ' "$NAME"
   readlink -f "$REAL_HOME/.local/bin/$NAME"
 done > "$ROOT/evidence/production-$SIDE.clients"
}
capture_production before
```

The before capture precedes every private child and auth link. Repeat `after`
only after synthetic native/process closure, then compare all retained files:

```sh
capture_production after
for PART in configuration.datom fable-current.datom services clients; do
 cmp "$ROOT/evidence/production-before.$PART" "$ROOT/evidence/production-after.$PART"
done
```

Any difference is reported with its exact boundary; it is not waived by guessing
that another flow caused it. Whole configuration equality includes protected
addresses. Current equality proves Fable retained its receiving FlowId, not its
internal attention or absence of ordinary activity. Service identity equality
covers only the named serving processes; this is a bounded witness, not a census
of every unrelated program on the host.

Before linking, bootstrap's lstat-style metadata check requires the production
auth target itself to be a regular file owned by the executing user. After
linking record only `readlink` text and `lstat` link metadata; after cleanup
record target type/owner metadata again. Never read/hash/copy auth content.
Opus60hv explicitly accepts refresh writes/races to this shared file; target
mtime/size are observations, not an equality promise. Its contents are outside
the production-equality comparison by that exact ruling. No login/logout,
credential-store-mode change or device login is permitted.
