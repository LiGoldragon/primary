#!/usr/bin/env bash
# Disposable Form-1 rollback drill.  It intentionally creates all state below
# mktemp and implements service control as files, never systemctl.
set -euo pipefail

root="$(mktemp -d "${TMPDIR:-/tmp}/form1-rollback.XXXXXX")"
trap 'rm -rf "$root"' EXIT
profile="$root/home/profile"
units="$root/home/systemd/user"
state="$root/home/state"
copies="$root/copied-stores"
control="$root/mock-service-control.log"
timer="$root/rollback.timer"
mkdir -p "$profile/generations/41" "$profile/generations/42" "$profile/bin" "$units/flow-nexus.service.d" "$state/flow" "$state/message" "$copies"

printf '%s\n' 'generation=41' 'flow=/nix/store/old-flow-0.12.2/bin/flow-nexus' > "$profile/generations/41/profile"
printf '%s\n' 'generation=42' 'flow=/nix/store/new-flow-0.17.4/bin/flow-nexus' > "$profile/generations/42/profile"
ln -s "$profile/generations/41" "$profile/current"
# This is deliberately separate from the generated profile generation: it
# models the undeclared user-profile client entry that wins PATH resolution.
ln -s /external/flow-0.12.2/bin/flow "$profile/bin/flow"
printf '%s\n' '[Service]' 'ExecStart=' 'ExecStart=/external/flow-0.12.2/bin/flow-nexus --stable' > "$units/flow-nexus.service.d/override.conf"
printf '%s\n' 'flow-row=seat-a' 'flow-row=seat-b' 'route=herdr:stable-seat-a' 'route=herdr:stable-seat-b' > "$state/flow/flow.sema"
printf '%s\n' 'message-row=registry-a' 'message-row=ledger-a' 'route=message:stable-seat-a' > "$state/message/messenger.sema"
cp "$state/flow/flow.sema" "$copies/flow.sema"
cp "$state/message/messenger.sema" "$copies/messenger.sema"

sha() { sha256sum "$1" | awk '{print $1}'; }
rows() { grep -c -- '-row=' "$1"; }
routes() { grep '^route=' "$1" | LC_ALL=C sort | tr '\n' ';'; }
expect_eq() { [ "$1" = "$2" ] || { printf 'ASSERTION FAILED: %s\n' "$3" >&2; exit 1; }; }
expect_file() { [ -e "$1" ] || { printf 'ASSERTION FAILED: missing %s\n' "$1" >&2; exit 1; }; }

old_profile_hash="$(sha "$profile/generations/41/profile")"
old_override_hash="$(sha "$units/flow-nexus.service.d/override.conf")"
old_profile_entry_target="$(readlink "$profile/bin/flow")"
flow_hash="$(sha "$state/flow/flow.sema")"; flow_rows="$(rows "$state/flow/flow.sema")"; flow_routes="$(routes "$state/flow/flow.sema")"
message_hash="$(sha "$state/message/messenger.sema")"; message_rows="$(rows "$state/message/messenger.sema")"; message_routes="$(routes "$state/message/messenger.sema")"

start_pair() { touch "$root/flow.running" "$root/message.running"; printf 'start %s\n' "$1" >> "$control"; }
stop_pair() { rm -f "$root/flow.running" "$root/message.running"; printf 'stop %s\n' "$1" >> "$control"; }
restore() {
  [ ! -e "$root/flow.running" ] && [ ! -e "$root/message.running" ] || { printf 'restore while service running\n' >&2; exit 1; }
  rm "$profile/current"; ln -s "$profile/generations/41" "$profile/current"
  rm "$profile/bin/flow"; ln -s "$old_profile_entry_target" "$profile/bin/flow"
  cp "$copies/flow.sema" "$state/flow/flow.sema"; cp "$copies/messenger.sema" "$state/message/messenger.sema"
  printf '%s\n' '[Service]' 'ExecStart=' 'ExecStart=/external/flow-0.12.2/bin/flow-nexus --stable' > "$units/flow-nexus.service.d/override.conf"
  printf 'restore generation=41 stores=atomic-while-stopped override=exact profile-entry=exact\n' >> "$control"
  start_pair old
}

# The production-form timer is recorded without waiting; a distinct accelerated
# clock invokes exactly the same failure branch below.
printf '%s\n' 'RollbackTarget=generation-41' 'OnActiveSec=300' 'CancelAuthority=remote-access-and-network-witness' > "$timer"
grep -qx 'OnActiveSec=300' "$timer"
grep -qx 'RollbackTarget=generation-41' "$timer"

cancel() {
  [ "${network_witness:-0}" = 1 ] && [ "${remote_access_witness:-0}" = 1 ] || return 42
  printf 'cancelled by witnessed authority\n' >> "$control"
}

start_pair old
stop_pair old
rm "$profile/current"; ln -s "$profile/generations/42" "$profile/current"
rm "$profile/bin/flow"; ln -s /nix/store/new-flow-0.17.4/bin/flow "$profile/bin/flow"
printf '%s\n' '[Service]' 'ExecStart=' 'ExecStart=/nix/store/new-flow-0.17.4/bin/flow-nexus --next' > "$units/flow-nexus.service.d/override.conf"
printf '%s\n' 'CORRUPTED-CANDIDATE-FLOW' > "$state/flow/flow.sema"
printf '%s\n' 'CORRUPTED-CANDIDATE-MESSAGE' > "$state/message/messenger.sema"
start_pair candidate
if cancel; then printf 'ASSERTION FAILED: premature cancellation accepted\n' >&2; exit 1; else expect_eq "$?" 42 'cancellation must require both witnesses'; fi

# Accelerated one-second expiry (the 300-second definition above is separately asserted).
sleep 1
stop_pair candidate
restore

expect_eq "$(readlink "$profile/current")" "$profile/generations/41" 'prior profile target'
expect_eq "$(sha "$profile/generations/41/profile")" "$old_profile_hash" 'prior profile content'
expect_eq "$(readlink "$profile/bin/flow")" "$old_profile_entry_target" 'exact user-profile client entry'
expect_eq "$(sha "$units/flow-nexus.service.d/override.conf")" "$old_override_hash" 'exact external override'
expect_eq "$(sha "$state/flow/flow.sema")" "$flow_hash" 'Flow store hash'
expect_eq "$(rows "$state/flow/flow.sema")" "$flow_rows" 'Flow row count'
expect_eq "$(routes "$state/flow/flow.sema")" "$flow_routes" 'Flow routes'
expect_eq "$(sha "$state/message/messenger.sema")" "$message_hash" 'Message store hash'
expect_eq "$(rows "$state/message/messenger.sema")" "$message_rows" 'Message row count'
expect_eq "$(routes "$state/message/messenger.sema")" "$message_routes" 'Message routes'
expect_file "$root/flow.running"; expect_file "$root/message.running"
grep -q '^stop candidate$' "$control"; grep -q '^restore generation=41 stores=atomic-while-stopped override=exact profile-entry=exact$' "$control"

printf 'PASS fixture=%s production_timer=300s accelerated_expiry=1s flow_rows=%s message_rows=%s\n' "$root" "$flow_rows" "$message_rows"
