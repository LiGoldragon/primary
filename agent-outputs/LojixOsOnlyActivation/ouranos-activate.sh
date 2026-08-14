#!/run/current-system/sw/bin/bash
# Root-only recovery helper for the approved, OS-owned Ouranos Lojix repair.
#
# Run only from a root-owned, hash-verified staging copy.  Modes are separate:
#   preflight: materialize, independently prove, and dry-activate only.
#   switch:    use the reviewed closure in one bounded transient activation.
# It never requests a reboot or BootOnce. The reviewed system switch may run
# the closure's embedded, independently-equated Home Manager activation.

set -euo pipefail
umask 077

readonly BASH=/run/current-system/sw/bin/bash
readonly SYSTEMCTL=/run/current-system/sw/bin/systemctl
readonly SYSTEMD_RUN=/run/current-system/sw/bin/systemd-run
readonly NIX=/run/current-system/sw/bin/nix
readonly NIX_ENV=/run/current-system/sw/bin/nix-env
readonly NIX_STORE=/run/current-system/sw/bin/nix-store
readonly INSTALL=/run/current-system/sw/bin/install
readonly MKDIR=/run/current-system/sw/bin/mkdir
readonly MV=/run/current-system/sw/bin/mv
readonly STAT=/run/current-system/sw/bin/stat
readonly READLINK=/run/current-system/sw/bin/readlink
readonly GREP=/run/current-system/sw/bin/grep
readonly AWK=/run/current-system/sw/bin/awk
readonly FIND=/run/current-system/sw/bin/find
readonly PS=/run/current-system/sw/bin/ps
readonly LOGINCTL=/run/current-system/sw/bin/loginctl
readonly SLEEP=/run/current-system/sw/bin/sleep
readonly RUNUSER=/run/current-system/sw/bin/runuser
readonly JOURNALCTL=/run/current-system/sw/bin/journalctl
readonly CHOWN=/run/current-system/sw/bin/chown
readonly CHMOD=/run/current-system/sw/bin/chmod
readonly CMP=/run/current-system/sw/bin/cmp
readonly DATE=/run/current-system/sw/bin/date
readonly FLOCK=/run/current-system/sw/bin/flock
readonly MKTEMP=/run/current-system/sw/bin/mktemp

readonly CRIOMOS_REV=271f4b15abeb69fa21a415e0ccb23f28560282df
readonly HOME_REV=e5f2264693c83f31f9991f1f12e2c60e2cdcb4a9
readonly LOJIX_REV=0d968da44bc0be8ed875b8546bebf52c3de53a81
readonly CRIOMOS_FLAKE=github:LiGoldragon/CriomOS/${CRIOMOS_REV}
readonly LOJIX_FLAKE=github:LiGoldragon/lojix/${LOJIX_REV}
readonly SYSTEM_SELECTOR=nixosConfigurations.target.config.system.build.toplevel
readonly HOME_SELECTOR=independentHomeConfigurations.li.activationPackage
readonly PROPOSAL=/git/github.com/LiGoldragon/goldragon/datom.dotos
readonly SECRETS_DIRECTORY=/git/github.com/LiGoldragon/goldragon/secrets
readonly BUILDER_FILE=/etc/nix/machines
readonly BUILDER=@/etc/nix/machines
readonly BUILDER_LINE='ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux /etc/ssh/ssh_host_ed25519_key 6 10 big-parallel,kvm,nixos-test - AAAAC3NzaC1lZDI1NTE5AAAAIAWX4CiSoep1+JuiYEpMzBj/H24eCYR+ZWaG3z2pg4Pk'
readonly STATE=/var/lib/lojix-recovery-primary-mjl2
readonly LOG_DIRECTORY=/var/log/lojix-recovery-primary-mjl2
readonly ROOT_RUNNER=${STATE}/ouranos-activate.sh
readonly GC_ROOT=${STATE}/system-gc-root
readonly TERMINAL_EVIDENCE=${STATE}/terminal-evidence.rkyv
readonly CLOSURE_RECORD=${STATE}/closure
readonly HOME_ACTIVATION_RECORD=${STATE}/home-activation-package
readonly CURRENT_SYSTEM_RECORD=${STATE}/preflight-current-system
readonly PREFLIGHT_OK=${STATE}/preflight-succeeded
readonly DRY_ACTIVATE_REVIEWED=${STATE}/dry-activate-reviewed-by-human
readonly GENERATED_INPUTS_RECORD=${STATE}/generated-inputs
readonly DRY_ACTIVATE_LOG=${LOG_DIRECTORY}/dry-activate.log
readonly STORE_DIRECTORY=/var/lib/lojix
readonly STORE=${STORE_DIRECTORY}/lojix.sema
readonly ORDINARY_SOCKET=/run/lojix/ordinary.sock
readonly OWNER_SOCKET=/run/lojix/owner.sock
readonly TRANSIENT_UNIT=lojix-recovery-primary-mjl2.service
readonly RECOVERY_STATE=${STATE}/RECOVERY_REQUIRED
readonly SWITCH_LOCK=/run/lojix-recovery-primary-mjl2.lock

fail() {
  printf '%s\n' "$*" >&2
  exit 1
}

require_root() {
  [ "$(/run/current-system/sw/bin/id -u)" = 0 ] || fail 'root is required'
}

require_regular_file() {
  local path=$1
  [ -e "$path" ] || fail "missing required path: $path"
  [ ! -L "$path" ] || fail "symlink rejected: $path"
  [ "$("$STAT" -c %F "$path")" = 'regular file' ] || fail "non-regular path rejected: $path"
}

require_private_directory() {
  local path=$1
  [ -d "$path" ] || fail "missing directory: $path"
  [ ! -L "$path" ] || fail "symlinked directory rejected: $path"
  [ "$("$STAT" -c '%U:%G %a' "$path")" = 'root:root 700' ] || fail "directory identity rejected: $path"
}

configure_remote_only_nix() {
  [ "$("$STAT" -Lc '%U:%G %a' "$BUILDER_FILE")" = 'root:root 444' ] || fail 'unexpected builder file identity'
  local active_line_count active_line
  active_line_count=$("$AWK" 'NF && $1 !~ /^#/ { count += 1; line = $0 } END { print count + 0 }' "$BUILDER_FILE")
  [ "$active_line_count" = 1 ] || fail 'exactly one active Nix builder is required'
  active_line=$("$AWK" 'NF && $1 !~ /^#/ { print; exit }' "$BUILDER_FILE")
  [ "$active_line" = "$BUILDER_LINE" ] || fail 'Nix builder line differs from the reviewed Prometheus route'
  export NIX_CONFIG=$'max-jobs = 0\nbuilders = @/etc/nix/machines\nfallback = false'
}

bootstrap_request() {
  printf '%s' "BootstrapRun.{primary-mjl2-os-only BuildOnly.{Horizon.{${PROPOSAL} goldragon ouranos CompleteHost SecretsDirectory.${SECRETS_DIRECTORY} ${CRIOMOS_FLAKE} x86_64-linux ${SYSTEM_SELECTOR}} NixBuilder.${BUILDER} ${STATE} ${GC_ROOT} ${TERMINAL_EVIDENCE}}}"
}

prepare_directories() {
  [ ! -e "$STATE" ] || fail "state path already exists: $STATE"
  [ ! -e "$LOG_DIRECTORY" ] || fail "log path already exists: $LOG_DIRECTORY"
  "$MKDIR" -m 700 "$STATE"
  "$MKDIR" -m 700 "$LOG_DIRECTORY"
  require_private_directory "$STATE"
  require_private_directory "$LOG_DIRECTORY"
  "$INSTALL" -m 700 "$0" "$ROOT_RUNNER"
  require_regular_file "$ROOT_RUNNER"
  [ "$("$STAT" -c '%U:%G %a' "$ROOT_RUNNER")" = 'root:root 700' ] || fail 'root runner identity rejected'
}

record_graphical_state() {
  local label=$1
  "$LOGINCTL" show-user li >"${STATE}/${label}-user-session" || fail 'cannot record li graphical session'
  "$LOGINCTL" list-sessions --no-legend | "$AWK" '$2 == 1001 { print }' >"${STATE}/${label}-li-sessions" || fail 'cannot list li sessions'
  "$PS" -u li -o pid=,ppid=,user=,comm=,args= | "$AWK" '$4 == "niri" || $4 == "codium" { print }' >"${STATE}/${label}-process-tree" || fail 'cannot record niri/Codium process tree'
  "$AWK" '{ print $1 " " $4 }' "${STATE}/${label}-process-tree" >"${STATE}/${label}-graphical-pids"
  [ -s "${STATE}/${label}-graphical-pids" ] || fail 'no li niri/Codium processes were found; graphical session preservation cannot be proven'
  while read -r pid command; do
    [ -r "/proc/${pid}/stat" ] || fail "recorded ${command} process disappeared during preflight"
    "$AWK" '{ print $22 }' "/proc/${pid}/stat" | "$AWK" -v pid="$pid" -v command="$command" 'NF == 1 { print pid " " command " " $1 }' || fail 'cannot record graphical process identity'
  done <"${STATE}/${label}-graphical-pids" >"${STATE}/${label}-graphical-identities"
  [ -s "${STATE}/${label}-graphical-identities" ] || fail 'graphical process identity record is empty'
}

assert_graphical_preserved() {
  local label=$1 pid command starttime current
  "$LOGINCTL" show-user li >"${STATE}/${label}-user-session" || fail 'cannot re-read li graphical session'
  "$LOGINCTL" list-sessions --no-legend | "$AWK" '$2 == 1001 { print }' >"${STATE}/${label}-li-sessions" || fail 'cannot re-list li sessions'
  "$PS" -u li -o pid=,ppid=,user=,comm=,args= | "$AWK" '$4 == "niri" || $4 == "codium" { print }' >"${STATE}/${label}-process-tree" || fail 'cannot re-record niri/Codium process tree'
  while read -r pid command starttime; do
    [ -r "/proc/${pid}/stat" ] || fail "graphical ${command} process ${pid} disappeared"
    current=$("$AWK" '{ print $22 }' "/proc/${pid}/stat")
    [ "$current" = "$starttime" ] || fail "graphical ${command} process ${pid} was replaced"
    [ "$("$PS" -p "$pid" -o comm= | "$AWK" '{$1=$1; print}')" = "$command" ] || fail "graphical process ${pid} no longer names ${command}"
  done <"${STATE}/preflight-graphical-identities"
  "$CMP" -s "${STATE}/preflight-user-session" "${STATE}/${label}-user-session" || fail 'li graphical-session state changed'
  "$CMP" -s "${STATE}/preflight-li-sessions" "${STATE}/${label}-li-sessions" || fail 'li session IDs changed'
}

find_generated_inputs() {
  local -a journals
  mapfile -t journals < <("$FIND" "$STATE" -mindepth 1 -maxdepth 1 -type d -name '.lojix-bootstrap-v5-*' -print)
  [ "${#journals[@]}" = 1 ] || fail 'expected exactly one private Lojix v5 BuildOnly journal'
  require_private_directory "${journals[0]}"
  local generated="${journals[0]}/generated-inputs"
  require_private_directory "$generated"
  local input
  for input in horizon system deployment secrets; do
    require_private_directory "${generated}/${input}"
  done
  printf '%s\n' "$generated" >"$GENERATED_INPUTS_RECORD"
}

generated_override_args() {
  local generated=$1
  GENERATED_OVERRIDES=(
    --override-input horizon "${generated}/horizon"
    --override-input system "${generated}/system"
    --override-input deployment "${generated}/deployment"
    --override-input secrets "${generated}/secrets"
  )
}

build_remote() {
  "$NIX" build "$@" --no-link --refresh --option max-jobs 0 --builders "$BUILDER" --option fallback false
}

build_remote_print_path() {
  "$NIX" build "$@" --no-link --print-out-paths --refresh --option max-jobs 0 --builders "$BUILDER" --option fallback false
}

preflight() {
  prepare_directories
  exec >"${LOG_DIRECTORY}/preflight.log" 2>&1
  configure_remote_only_nix
  require_regular_file "$PROPOSAL"
  [ -d "$SECRETS_DIRECTORY" ] || fail 'configured encrypted secrets directory is absent'
  record_graphical_state preflight

  build_remote "${LOJIX_FLAKE}#checks.x86_64-linux.fresh-daemon-startup"
  "$NIX" run "${CRIOMOS_FLAKE}#lojix-bootstrap" \
    --refresh --option max-jobs 0 --builders "$BUILDER" --option fallback false -- \
    "$(bootstrap_request)"

  [ -L "$GC_ROOT" ] || fail 'BuildOnly did not create an exact GC root'
  require_regular_file "$TERMINAL_EVIDENCE"
  [ "$("$STAT" -c '%U:%G %a' "$TERMINAL_EVIDENCE")" = 'root:root 600' ] || fail 'terminal evidence identity rejected'
  find_generated_inputs
  local generated independent_closure home_activation closure
  generated=$(<"$GENERATED_INPUTS_RECORD")
  generated_override_args "$generated"

  build_remote "${CRIOMOS_FLAKE}#checks.x86_64-linux.lojix-ownership" "${GENERATED_OVERRIDES[@]}"
  build_remote "${CRIOMOS_FLAKE}#checks.x86_64-linux.home-activation-equivalence" "${GENERATED_OVERRIDES[@]}"
  independent_closure=$(build_remote_print_path "${CRIOMOS_FLAKE}#${SYSTEM_SELECTOR}" "${GENERATED_OVERRIDES[@]}")
  home_activation=$(build_remote_print_path "${CRIOMOS_FLAKE}#${HOME_SELECTOR}" "${GENERATED_OVERRIDES[@]}")
  closure=$("$READLINK" -f "$GC_ROOT")
  [ "$independent_closure" = "$closure" ] || fail 'independent materialized system selector does not equal the BuildOnly GC-root closure'
  "$NIX_STORE" --query --valid "$closure" >/dev/null
  [ -x "${closure}/bin/switch-to-configuration" ] || fail 'built closure lacks NixOS activation program'
  printf '%s\n' "$closure" >"$CLOSURE_RECORD"
  printf '%s\n' "$home_activation" >"$HOME_ACTIVATION_RECORD"
  "$READLINK" -f /run/current-system >"$CURRENT_SYSTEM_RECORD"

  "${closure}/bin/switch-to-configuration" check
  "${closure}/bin/switch-to-configuration" dry-activate >"$DRY_ACTIVATE_LOG" 2>&1
  if "$GREP" -Eiq '(^|[^[:alnum:]_-])(niri|codium)([^[:alnum:]_-]|$)' "$DRY_ACTIVATE_LOG"; then
    fail 'dry-activate reports a niri or Codium effect; graphical-session safety requires separate review'
  fi
  assert_graphical_preserved preflight-post-dry

  "$INSTALL" -m 600 /dev/null "$PREFLIGHT_OK"
  printf '%s\n' 'PRELIGHT_SUCCESS: inspect complete root-only preflight and dry-activate logs before any separately approved switch.'
}

load_reviewed_closure() {
  require_private_directory "$STATE"
  require_private_directory "$LOG_DIRECTORY"
  require_regular_file "$ROOT_RUNNER"
  require_regular_file "$PREFLIGHT_OK"
  require_regular_file "$CLOSURE_RECORD"
  require_regular_file "$HOME_ACTIVATION_RECORD"
  require_regular_file "$CURRENT_SYSTEM_RECORD"
  require_regular_file "$TERMINAL_EVIDENCE"
  require_regular_file "$GENERATED_INPUTS_RECORD"
  local closure
  closure=$(<"$CLOSURE_RECORD")
  [ -n "$closure" ] || fail 'empty recorded closure'
  [ "$("$READLINK" -f "$GC_ROOT")" = "$closure" ] || fail 'GC root no longer names reviewed closure'
  "$NIX_STORE" --query --valid "$closure" >/dev/null
  [ -x "${closure}/bin/switch-to-configuration" ] || fail 'reviewed closure changed'
  [ "$("$READLINK" -f /run/current-system)" = "$(<"$CURRENT_SYSTEM_RECORD")" ] || fail 'current system changed after dry-activation review'
  printf '%s' "$closure"
}

assert_service_stopped_and_masked() {
  "$SYSTEMCTL" mask --runtime lojix-daemon.service
  "$SYSTEMCTL" stop lojix-daemon.service
  [ "$("$SYSTEMCTL" show --property=ActiveState --value lojix-daemon.service)" = inactive ] || fail 'old Lojix service did not stop'
  [ "$("$SYSTEMCTL" show --property=MainPID --value lojix-daemon.service)" = 0 ] || fail 'old Lojix service retained a process'
  [ "$("$SYSTEMCTL" is-enabled lojix-daemon.service)" = masked-runtime ] || fail 'old Lojix service is not runtime-masked'
}

secure_store_directory_for_move() {
  [ -d "$STORE_DIRECTORY" ] || fail 'configured Lojix store directory is absent'
  [ ! -L "$STORE_DIRECTORY" ] || fail 'configured Lojix store directory is a symlink'
  [ "$("$STAT" -c '%U:%G %a' "$STORE_DIRECTORY")" = 'li:users 750' ] || fail 'configured Lojix store directory identity is unexpected'
  require_regular_file "$STORE"
  [ "$("$STAT" -c '%U:%G %a %h' "$STORE")" = 'li:users 644 1' ] || fail 'configured disposable store identity is unexpected'
  STORE_DEVICE=$("$STAT" -c %d "$STORE")
  STORE_INODE=$("$STAT" -c %i "$STORE")
  STORE_ORIGINAL_IDENTITY=$("$STAT" -c '%U:%G %a %h' "$STORE")
  # Chowning the parent first removes li's rename/create ability before this
  # root operation rechecks and moves the one approved regular file.
  "$CHOWN" root:root "$STORE_DIRECTORY"
  "$CHMOD" 700 "$STORE_DIRECTORY"
  [ "$("$STAT" -c '%U:%G %a' "$STORE_DIRECTORY")" = 'root:root 700' ] || fail 'cannot exclusively secure Lojix store directory'
  STORE_DIRECTORY_CUSTODY=yes
  require_regular_file "$STORE"
  [ "$("$STAT" -c '%U:%G %a %h' "$STORE")" = 'li:users 644 1' ] || fail 'store identity changed before root custody'
  STORE_FILE_CUSTODY=yes
  "$CHOWN" root:root "$STORE"
  "$CHMOD" 600 "$STORE"
  [ "$("$STAT" -c '%U:%G %a %h' "$STORE")" = 'root:root 600 1' ] || fail 'cannot take exclusive custody of disposable store'
}

restore_store_directory_owner() {
  [ "$("$STAT" -c '%U:%G %a' "$STORE_DIRECTORY")" = 'root:root 700' ] || fail 'unexpected Lojix store directory during ownership restoration'
  "$CHOWN" li:users "$STORE_DIRECTORY"
  "$CHMOD" 750 "$STORE_DIRECTORY"
  [ "$("$STAT" -c '%U:%G %a' "$STORE_DIRECTORY")" = 'li:users 750' ] || fail 'cannot restore declared Lojix store directory ownership'
  STORE_DIRECTORY_CUSTODY=no
}

restore_store_directory_owner_for_cleanup() {
  # This deliberately never calls `fail`: the failure trap must continue even
  # if the diagnostic state file cannot be written or a first restoration
  # attempt fails. Its boolean result is the only authority to unmask.
  "$CHOWN" li:users "$STORE_DIRECTORY"
  "$CHMOD" 750 "$STORE_DIRECTORY"
  [ "$("$STAT" -c '%U:%G %a' "$STORE_DIRECTORY" 2>/dev/null)" = 'li:users 750' ]
}

restore_exact_file_custody_for_cleanup() {
  local path=$1 device=$2 inode=$3 original_identity=$4
  [ -n "$device" ] && [ -n "$inode" ] && [ -n "$original_identity" ] || return 1
  [ -e "$path" ] || return 1
  [ ! -L "$path" ] || return 1
  [ "$("$STAT" -c '%d:%i %F' "$path" 2>/dev/null)" = "${device}:${inode} regular file" ] || return 1
  "$CHOWN" li:users "$path"
  "$CHMOD" 644 "$path"
  [ "$("$STAT" -c '%U:%G %a %h' "$path" 2>/dev/null)" = "$original_identity" ]
}

move_recognised_sidecar_if_present() {
  local suffix=$1 source="${STORE}${suffix}" target="${STATE}/discarded-lojix${suffix}"
  if [ -e "$source" ]; then
    require_regular_file "$source"
    [ "$("$STAT" -c '%U:%G %a %h' "$source")" = 'li:users 644 1' ] || fail "unexpected recognised sidecar identity: ${suffix}"
    SIDECAR_CUSTODY_PATH=$source
    SIDECAR_DEVICE=$("$STAT" -c %d "$source")
    SIDECAR_INODE=$("$STAT" -c %i "$source")
    SIDECAR_ORIGINAL_IDENTITY=$("$STAT" -c '%U:%G %a %h' "$source")
    [ ! -e "$target" ] || fail "recovery target already exists: $target"
    SIDECAR_FILE_CUSTODY=yes
    "$CHOWN" root:root "$source"
    "$CHMOD" 600 "$source"
    [ "$("$STAT" -c '%U:%G %a %h' "$source")" = 'root:root 600 1' ] || fail "cannot take root custody of recognised sidecar: ${suffix}"
    "$MV" -- "$source" "$target"
    SIDECAR_FILE_CUSTODY=no
  fi
}

write_recovery_state() {
  local phase=$1 status=$2
  {
    printf 'timestamp=%s\n' "$("$DATE" --iso-8601=seconds)"
    printf 'phase=%s\n' "$phase"
    printf 'status=%s\n' "$status"
    printf 'previous_profile=%s\n' "${PRE_PROFILE:-unset}"
    printf 'current_profile=%s\n' "$("$READLINK" -f /nix/var/nix/profiles/system || true)"
    printf 'previous_current_system=%s\n' "${PRE_CURRENT_SYSTEM:-unset}"
    printf 'current_system=%s\n' "$("$READLINK" -f /run/current-system || true)"
    printf 'discarded_store=%s\n' "${STORE_MOVED:-no}"
    printf 'runtime_masked_before_recovery=%s\n' "$("$SYSTEMCTL" is-enabled lojix-daemon.service 2>&1 || true)"
  } >"$RECOVERY_STATE"
  "$CHMOD" 600 "$RECOVERY_STATE"
}

activation_failure() {
  local exit_code=${1:-$?} phase=${2:-${ACTIVATION_PHASE:-unknown}}
  local custody_restored=yes directory_restored=yes service_stopped=no recovery_state_written=no
  trap - ERR EXIT
  trap - HUP INT TERM
  # No cleanup step may be short-circuited. In particular, an I/O error while
  # recording evidence must not prevent custody restoration.
  set +e
  "$SYSTEMCTL" stop lojix-daemon.service
  if [ "$("$SYSTEMCTL" show --property=ActiveState --value lojix-daemon.service)" = inactive ] \
    && [ "$("$SYSTEMCTL" show --property=MainPID --value lojix-daemon.service)" = 0 ]; then
    service_stopped=yes
  fi
  if [ "${STORE_FILE_CUSTODY:-no}" = yes ]; then
    if restore_exact_file_custody_for_cleanup "$STORE" "${STORE_DEVICE:-}" "${STORE_INODE:-}" "${STORE_ORIGINAL_IDENTITY:-}"; then
      STORE_FILE_CUSTODY=no
    else
      custody_restored=no
    fi
  fi
  if [ "${SIDECAR_FILE_CUSTODY:-no}" = yes ]; then
    if restore_exact_file_custody_for_cleanup "${SIDECAR_CUSTODY_PATH:-}" "${SIDECAR_DEVICE:-}" "${SIDECAR_INODE:-}" "${SIDECAR_ORIGINAL_IDENTITY:-}"; then
      SIDECAR_FILE_CUSTODY=no
    else
      custody_restored=no
    fi
  fi
  if [ "${STORE_DIRECTORY_CUSTODY:-no}" = yes ]; then
    if restore_store_directory_owner_for_cleanup; then
      STORE_DIRECTORY_CUSTODY=no
    else
      directory_restored=no
    fi
  fi
  if write_recovery_state "$phase" "failed-exit-${exit_code}"; then
    recovery_state_written=yes
  else
    # A root-only durable state record is preferred, but this fallback is
    # intentionally unable to interrupt the remaining service cleanup.
    printf 'HIGH_SEVERITY_RECOVERY_FAILURE phase=%s exit=%s file_custody_restored=%s directory_restored=%s service_stopped=%s\n' \
      "$phase" "$exit_code" "$custody_restored" "$directory_restored" "$service_stopped" >"${STATE}/RECOVERY_REQUIRED.fallback" 2>&1
  fi
  # Never restart the old daemon or guess a system-profile rollback.
  if [ "$custody_restored" = yes ] && [ "$directory_restored" = yes ] && [ "$service_stopped" = yes ]; then
    "$SYSTEMCTL" unmask --runtime lojix-daemon.service
    "$SYSTEMCTL" reset-failed lojix-daemon.service
  else
    # Failed custody restoration is a hard stop: preserve the mask so neither
    # old nor new daemon can observe an ambiguous store directory.
    "$SYSTEMCTL" mask --runtime lojix-daemon.service
  fi
  printf '%s\n' "ACTIVATION_FAILED: phase=${phase}; file_custody_restored=${custody_restored}; directory_restored=${directory_restored}; service_stopped=${service_stopped}; recovery_state_written=${recovery_state_written}; inspect root-only recovery state and log before any recovery." >&2
  exit "$exit_code"
}

activation_signal() {
  local signal=$1
  activation_failure 1 "signal-${signal}"
}

assert_live_service() {
  local closure=$1
  [ "$("$SYSTEMCTL" show --property=ActiveState --value lojix-daemon.service)" = active ] || fail 'Lojix service is not active'
  [ "$("$SYSTEMCTL" show --property=SubState --value lojix-daemon.service)" = running ] || fail 'Lojix service is not running'
  [ "$("$SYSTEMCTL" show --property=Result --value lojix-daemon.service)" = success ] || fail 'Lojix service result is not success'
  "$SYSTEMCTL" show --property=ExecStart --value lojix-daemon.service | "$GREP" -F 'lojix-0.17.5/bin/lojix-daemon' >/dev/null
  require_regular_file "$STORE"
  [ "$("$STAT" -c '%U:%G %a' "$STORE")" = 'li:users 600' ] || fail 'fresh store ownership or mode is unexpected'
  [ "$("$STAT" -c '%U:%G %a' "$ORDINARY_SOCKET")" = 'li:users 660' ] || fail 'ordinary socket ownership or mode is unexpected'
  [ "$("$STAT" -c '%U:%G %a' "$OWNER_SOCKET")" = 'li:users 600' ] || fail 'owner socket ownership or mode is unexpected'
  "${closure}/sw/bin/lojix-inspect-store" "$STORE" | "$GREP" -F 'Schema matches version=4' >/dev/null
}

exercise_clients() {
  local closure=$1
  LOJIX_OWNER_SOCKET="$OWNER_SOCKET" "${closure}/sw/bin/meta-lojix" 'Pin.(fresh-cluster fresh-node 1 fresh-pin)' | "$GREP" -F 'PinRejected' >/dev/null
  LOJIX_ORDINARY_SOCKET="$ORDINARY_SOCKET" "${closure}/sw/bin/lojix" 'Query.ByNode.(fresh-cluster fresh-node None)' | "$GREP" -F 'Queried' >/dev/null
}

assert_cross_tier_rejection_does_not_restart() {
  local closure=$1 before_pid
  before_pid=$("$SYSTEMCTL" show --property=MainPID --value lojix-daemon.service)
  if LOJIX_ORDINARY_SOCKET="$ORDINARY_SOCKET" "${closure}/sw/bin/lojix" 'Pin.(fresh-cluster fresh-node 1 fresh-pin)'; then
    fail 'ordinary client accepted owner-tier request'
  fi
  assert_live_service "$closure"
  [ "$("$SYSTEMCTL" show --property=MainPID --value lojix-daemon.service)" = "$before_pid" ] || fail 'cross-tier rejection restarted Lojix'
}

assert_expected_tools() {
  local home_path=$1
  [ "$("${home_path}/bin/codex" --version)" = 'codex-cli 0.147.0' ] || fail 'current Home path does not expose expected Codex 0.147.0'
  [ "$("${home_path}/bin/claude" --version)" = '2.1.231 (Claude Code)' ] || fail 'current Home path does not expose expected Claude 2.1.231'
  "$RUNUSER" -l li -c 'test "$(codex --version)" = "codex-cli 0.147.0"; test "$(claude --version)" = "2.1.231 (Claude Code)"'
}

assert_home_boundary_and_tools() {
  local home_activation=$1 home_path
  [ "$("$SYSTEMCTL" show --property=ActiveState --value home-manager-li.service)" = active ] || fail 'Home Manager service is not active'
  [ "$("$SYSTEMCTL" show --property=Result --value home-manager-li.service)" = success ] || fail 'Home Manager service result is not success'
  [ "$("$READLINK" -f /home/li/.local/state/nix/profiles/home-manager)" = "$(<"$HOME_ACTIVATION_RECORD")" ] || fail 'current Home activation is not the independently verified package'
  home_path=$("$READLINK" -f "${home_activation}/home-path")
  [ ! -e "${home_path}/bin/lojix" ] || fail 'Home path unexpectedly exports Lojix'
  [ ! -e "${home_path}/bin/lojix-bootstrap" ] || fail 'Home path unexpectedly exports Lojix bootstrap'
  assert_expected_tools "$home_path"
}

activate_inner() {
  exec >"${LOG_DIRECTORY}/switch-and-acceptance.log" 2>&1
  local closure home_activation restarts pid
  closure=$(load_reviewed_closure)
  PRE_PROFILE=$("$READLINK" -f /nix/var/nix/profiles/system)
  PRE_CURRENT_SYSTEM=$("$READLINK" -f /run/current-system)
  ACTIVATION_PHASE=pre-switch
  STORE_MOVED=no
  STORE_DIRECTORY_CUSTODY=no
  STORE_FILE_CUSTODY=no
  SIDECAR_FILE_CUSTODY=no
  trap 'activation_failure $?' ERR EXIT
  trap 'activation_signal HUP' HUP
  trap 'activation_signal INT' INT
  trap 'activation_signal TERM' TERM
  assert_graphical_preserved pre-switch
  assert_service_stopped_and_masked
  ACTIVATION_PHASE=store-custody
  secure_store_directory_for_move
  [ ! -e "${STATE}/discarded-lojix.sema" ] || fail 'discard target already exists'
  "$MV" -- "$STORE" "${STATE}/discarded-lojix.sema"
  STORE_MOVED=yes
  STORE_FILE_CUSTODY=no
  move_recognised_sidecar_if_present '.schema-pre-v3.backup'
  move_recognised_sidecar_if_present '.schema-v3.pending'
  move_recognised_sidecar_if_present '.schema-v3.pending.owner'
  [ ! -e "$STORE" ] || fail 'old store remains at configured service path'
  restore_store_directory_owner

  ACTIVATION_PHASE=profile-set
  "$SYSTEMCTL" reset-failed lojix-daemon.service
  "$NIX_ENV" --profile /nix/var/nix/profiles/system --set "$closure"
  [ "$("$READLINK" -f /nix/var/nix/profiles/system)" = "$closure" ] || fail 'system profile is not the reviewed closure after set'
  # The old retry has been stopped and the profile now selects only the
  # reviewed 0.17.5 unit; unmask immediately before declarative switching.
  "$SYSTEMCTL" unmask --runtime lojix-daemon.service
  ACTIVATION_PHASE=declarative-switch
  "${closure}/bin/switch-to-configuration" switch
  "$SYSTEMCTL" start lojix-daemon.service

  ACTIVATION_PHASE=acceptance
  assert_live_service "$closure"
  exercise_clients "$closure"
  assert_cross_tier_rejection_does_not_restart "$closure"
  home_activation=$(<"$HOME_ACTIVATION_RECORD")
  assert_home_boundary_and_tools "$home_activation"
  assert_graphical_preserved post-switch

  restarts=$("$SYSTEMCTL" show --property=NRestarts --value lojix-daemon.service)
  pid=$("$SYSTEMCTL" show --property=MainPID --value lojix-daemon.service)
  "$SLEEP" 600
  assert_live_service "$closure"
  [ "$("$SYSTEMCTL" show --property=NRestarts --value lojix-daemon.service)" = "$restarts" ] || fail 'Lojix restarted during ten-minute dwell'
  [ "$("$SYSTEMCTL" show --property=MainPID --value lojix-daemon.service)" = "$pid" ] || fail 'Lojix PID changed during ten-minute dwell'
  if "$JOURNALCTL" -u lojix-daemon.service --since '10 minutes ago' --no-pager | "$GREP" -E 'WireShape|schema|panic' >/dev/null; then
    fail 'Lojix journal contains a prohibited failure event during dwell'
  fi
  assert_graphical_preserved post-dwell

  ACTIVATION_PHASE=explicit-restart-acceptance
  "$SYSTEMCTL" restart lojix-daemon.service
  assert_live_service "$closure"
  exercise_clients "$closure"
  "${closure}/sw/bin/lojix-inspect-store" "$STORE" | "$GREP" -F 'Schema matches version=4' >/dev/null
  assert_graphical_preserved post-restart
  trap - ERR EXIT HUP INT TERM
  printf '%s\n' 'ACTIVATION_SUCCESS: no reboot was requested or performed.'
}

switch() {
  load_reviewed_closure >/dev/null
  require_regular_file "$DRY_ACTIVATE_REVIEWED"
  [ "$("$STAT" -c '%U:%G %a' "$DRY_ACTIVATE_REVIEWED")" = 'root:root 600' ] || fail 'dry-activate review acknowledgement identity is invalid'
  [ ! -e "/run/systemd/transient/${TRANSIENT_UNIT}" ] || fail 'activation transient already exists'
  "$SYSTEMD_RUN" --wait --collect --unit="$TRANSIENT_UNIT" --service-type=exec \
    --property=TimeoutStartSec=45min --property=NoNewPrivileges=no \
    "$BASH" "$ROOT_RUNNER" activate-inner
}

self_test_file_custody() {
  # This isolated root fixture simulates interruption after an exact store
  # inode was chowned root:root/0600 and before its rename. It never names
  # /var/lib/lojix or systemctl and retains its root-only fixture for audit.
  local fixture file device inode original
  fixture=$("$MKTEMP" -d -m 700 /run/lojix-recovery-file-custody.XXXXXX)
  file="${fixture}/lojix.sema"
  "$INSTALL" -m 644 -o li -g users /dev/null "$file"
  device=$("$STAT" -c %d "$file")
  inode=$("$STAT" -c %i "$file")
  original=$("$STAT" -c '%U:%G %a %h' "$file")
  [ "$original" = 'li:users 644 1' ] || fail 'file custody fixture was not initialized as declared'
  "$CHOWN" root:root "$file"
  "$CHMOD" 600 "$file"
  [ "$("$STAT" -c '%U:%G %a %h' "$file")" = 'root:root 600 1' ] || fail 'file custody fixture did not enter simulated interrupted state'
  restore_exact_file_custody_for_cleanup "$file" "$device" "$inode" "$original" || fail 'file custody fixture did not restore exact original inode'
  [ "$("$STAT" -c '%U:%G %a %h' "$file")" = 'li:users 644 1' ] || fail 'file custody fixture final identity is unsafe'
  printf '%s\n' "SELF_TEST_FILE_CUSTODY_SUCCESS: retained root-only fixture ${fixture}"
}

acquire_no_concurrent_switch_lock() {
  exec 9>"$SWITCH_LOCK"
  "$FLOCK" -n 9 || fail 'another Lojix recovery preflight or switch is already running'
}

main() {
  require_root
  acquire_no_concurrent_switch_lock
  case "${1:-}" in
    preflight) preflight ;;
    switch) switch ;;
    activate-inner) activate_inner ;;
    self-test-file-custody) self_test_file_custody ;;
    *) fail 'usage: ouranos-activate.sh {preflight|switch|self-test-file-custody}' ;;
  esac
}

main "$@"
