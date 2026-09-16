#!/usr/bin/env bash
set -uo pipefail

readonly CODEX=/home/li/.nix-profile/bin/codex
readonly NODE=/home/li/.nix-profile/bin/node
readonly MANIFEST="$(dirname "$0")/overnight-poc-manifest.json"
readonly SOURCE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
readonly RUN_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/core-checkup/overnight-poc-runs/$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$RUN_ROOT"

quota_preflight() {
  : "${CODEX_APP_SERVER_SOCKET:?CODEX_APP_SERVER_SOCKET must name an existing app-server socket}"
  "$NODE" --input-type=module -e '
    const { createAccountClient, createUnixWebSocketTransport } = await import(process.argv[1]);
    const readings = await createAccountClient({transport:createUnixWebSocketTransport(process.env.CODEX_APP_SERVER_SOCKET)}).read();
    const primary = readings["account/rateLimits/read"]?.rateLimits?.primary;
    const spark = readings["account/rateLimits/read"]?.rateLimitsByLimitId?.codex_bengalfox;
    if (!primary || !spark?.primary || !spark?.secondary || !Number.isFinite(primary.usedPercent) || primary.usedPercent >= 100 || Date.parse(primary.resetsAt) <= Date.now()) throw new Error("Codex quota admission unavailable or exhausted");
    process.stdout.write(JSON.stringify(readings)+"\n");
  ' "$SOURCE_ROOT/tools/codex-app-server-client.mjs"
}

run_model() {
  local mode=$1 work=$2 prompt=$3 output=$4 events=$5 exit_file=$6
  quota_preflight >"${events%.jsonl}.quota.json" 2>"${events%.jsonl}.quota.stderr"
  local quota_status=$?
  if [ "$quota_status" -ne 0 ]; then printf '%s\n' "$quota_status" >"$exit_file"; return "$quota_status"; fi
  if [ "$mode" = write ]; then
    "$CODEX" exec --ephemeral --json --model gpt-5.6-luna --sandbox workspace-write --skip-git-repo-check --cd "$work" --output-last-message "$output" "$(cat "$prompt")" >"$events" 2>&1
  else
    "$CODEX" exec --ephemeral --json --model gpt-5.6-luna --sandbox read-only --skip-git-repo-check --cd "$work" --output-last-message "$output" "$(cat "$prompt")" >"$events" 2>&1
  fi
  local status=$?; printf '%s\n' "$status" >"$exit_file"; return "$status"
}

job() {
  local name=$1 origin=$2 base=$3 prompt=$4 audit_prompt=$5 job_root="$RUN_ROOT/$name" work="$job_root/work"
  mkdir -p "$job_root"
  jj git clone --no-colocate "$origin" "$work" >"$job_root/clone.stdout" 2>"$job_root/clone.stderr" || return
  (cd "$work" && jj new "$base" && jj bookmark create "proposal/cf7879-overnight-$name") >"$job_root/base.stdout" 2>"$job_root/base.stderr" || return
  run_model write "$work" "$SOURCE_ROOT/$prompt" "$job_root/job.last-message" "$job_root/job.events.jsonl" "$job_root/job.exit" || return
  run_model read "$work" "$SOURCE_ROOT/$audit_prompt" "$job_root/audit.last-message" "$job_root/audit.events.jsonl" "$job_root/audit.exit"
}

job message-idle-audit git@github.com:LiGoldragon/message.git 08208fd89fa866328aaab63f45739797be111c49 tools/overnight-poc-prompts/message-idle-audit.md tools/overnight-poc-prompts/message-idle-audit-review.md
job cloudflare-readonly-fixture ssh://git@github.com/LiGoldragon/cloud.git 69b4ee0625dc64020d93d39b70101afc5817cee0 tools/overnight-poc-prompts/cloudflare-readonly-fixture.md tools/overnight-poc-prompts/cloudflare-readonly-fixture-review.md
