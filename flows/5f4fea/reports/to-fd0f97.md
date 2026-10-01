# Corrected consolidated report for fd0f97

Date: 2026-09-15. Target: current Claude session
`fd0f9762-d293-432b-a425-4f590fe9c8d5`. This file is a report prepared for
delivery, not a receipt that fd0f97 received it.

## Delivery correction

The earlier claim that eleven AgentIntercom sends reached fd0f97 is retracted
as a target-delivery claim. The tools acknowledged sends, but the current peer
reports they did not reach fd0f97. The actual Claude socket is
`/run/user/1001/cc-socks/1206265.sock`; this report did not open or guess at
that socket. The existing resend candidate at
`/tmp/5f4fea-fd0f97-consolidated-resend.txt` remains only a candidate, with no
delivery receipt.

## Existing items 28b, 29, and 33

Item 28b is an existing Ghostty/Claude launch proof, not full item 31. Its
launch packet records the first failed display attempt, the Wayland retry,
Ghostty PID 1206233, Claude PID 1206265, session
`fd0f9762-d293-432b-a425-4f590fe9c8d5`, first user UUID
`137840f0-3fa5-4881-a9d2-358beb7a5b03` at
2026-09-15T20:23:07.882Z, and no app-server `turn/start`. It does not prove a
daemon-managed Flow component, per-flow daemon ownership, or a complete item
31 successor launch.

Item 29's existing packet records Curriculum main commit `0a622756`, exactly
four approved breaking-upgrades lines, external generation
`Generated.{ 44 21 }`, projections pushed at `2219d916`, and a fresh native
test session `01a0a6bd-298b-7073-bfdb-5101145e7212` exiting zero. The stated
gate remains network connectivity plus an actual remote Zeus login/session;
the fifteen-minute value was an unapproved model proposal. No deployment
occurred.

Item 33 is a delegated source witness, not a deploy decision: Lojix requires
the basename `horizon-definition.datom`; `proposal.datom` is rejected.
CompleteHost requires explicit `NoSecrets` or `SecretsDirectory`; encrypted
repository files do not witness Zeus secret selection. BootOnce is supported.
Cancelable countdown and boot counting were not source-witnessed.

## Item 31 daemon and hook witnesses

The disposable daemon probe `7bca5ddf` was rostered, remote control was
active, and `prompt-relay claude` wrote a transcript-derived human turn. This
is a bounded Haiku witness only.

The current `claude --bg` contract blocks the required real successor launch:
it ignores a caller-supplied `--session-id`, creates a daemon-generated short
and full session identifier, and records `dispatch.isolation: "none"` in the
daemon roster. A client-side `systemd-run --scope` did not own the resulting
daemon worker cgroup. The exposed `claude agents` and `claude respawn` commands
provide no per-job cgroup or scope option. Therefore fixed successor identity
and independent per-flow scope are not proved or available through this path.

Stop hooks do run under `--bg`; a disposable hook saw the hook event and a
transcript response containing an addressed marker. Delivery is **not
proven**: the first temporary hook failed because its Node path was absent;
the follow-up exposed daemon short-versus-full identifier handling and then a
later unaddressed assistant record. The isolated adapter now selects the last
explicit `Send.{ Codex.<thread> }` section and binds to a launcher-written full
session record. Its fixture passed, but no successful hook-to-Codex delivery
was witnessed.

Commit `321050ff6` on `proposal/5f4fea-item30-launcher` contains that bounded
adapter and fixture. It is not primary main and does not activate a hook for a
live flow.

The minimum future daemon-adapter design is a persisted typed launch record
mapping requested alias to daemon-generated identifier, daemon-owned per-flow
unit/cgroup creation, and persisted hook configuration. This is a design
conclusion from the witnesses, not an implemented deployment.

## Prompt assembly witness

The existing full-context primary-profile prototype is at
`/tmp/5f4fea-primary-full-context.t8cGYk/`. Its system prompt is 134125 bytes;
its user prompt is 71106 bytes. Its exact coverage manifest has 73 entries:
nine primary skill bodies, 25 recursive Vision files, nine recursive Intent
files, 20 topic-selected raw Vision files, nine predecessor raw Vision files,
and one predecessor Notion file. The inputs in that prototype include whole
recursive `Vision/` and `Intent/` trees; it is not a newly launched successor.

No new successor has been launched from this assembly. Any proposed command
for a named, remote-controlled, daemon-managed successor with a clean
environment is **not executed**, because the fixed-ID and independent-scope
requirements above remain unmet.
