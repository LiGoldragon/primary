# Recovery status witness — 2026-09-27

Scope: a compact read-only consolidation of retained witnesses.  It makes no
claim of a new live probe, activation, service change, or session mutation.

## Seats and root route

- The recovery roster records **nine native replies** from `56ae53`, `6fe957`,
  `139366`, `22e12b`, `9ac67c`, `184bd8`, `8904b1`, `dc53b4`, and `38f337`
  ([source](../summary.md), lines 4-8; roster at `receipts/roster.md`).
- A later snapshot records **eight interactive-ready** seats (all except Mind
  Sol), while Mind Sol `56ae53` is a live native Codex pane in `default`,
  `w1:p1`, `term_65c6a3b37c3011`.  Flow and Messenger still bind that identity
  to stopped `messaging-build`, `wM:pJ`, `term_65c6462fe47809b`
  ([source](../summary.md), line 26).  Thus the live root pane is not a
  verified current Messenger registration at its native location; a managed
  pane identity readback was pending ([Field source](../../9ac67c/summary-flow-upgrade.md), lines 149, 160).

## Literal `--help` session

- Fable `8904b1` witnessed one socket-addressed stop, exit `0`, for isolated
  `/home/li/.config/herdr/sessions/--help/herdr.sock`: server PID `528364` and
  idle shell PID `528406` were absent afterward; target sockets were gone;
  default PID `4957` and recovery PID `301649` retained their start times;
  default's ten agents were unchanged.  Directory/log/session record remains
  ([Field source](../../9ac67c/summary-flow-upgrade.md), line 159; primary
  witness `../../8904b1/witnesses/accidental-help-session-stop.md`).
- **Explicit gap:** the pre-stop socket inode number was not captured.  The
  stop is witnessed; a pre-inode comparison is unknown.  No directory deletion
  is authorized or evidenced.

## Home and Form-1 gate

- The retained full Home check was red on `2026-09-27`: `agent-daemon-configuration`
  builder exit `65` (old `spirit-deployment` ProviderSeed fixture matcher versus
  current Datom form), and `mentci-deps` `0.5.0` builder exit `101`
  (`meta-signal-criome` `build.rs` imports removed
  `schema_rust::bootstrap::BootstrapInterfaceGeneration`).  The retained report
  says these predate the Flow/Message pins; no pre-pin realized full run is
  witnessed, so that ancestry remains unproven ([Field source](../../9ac67c/summary-flow-upgrade.md), lines 144, 152).
- Form-1 has a captured offline `sd-switch` plan only: next configuration and
  next Flow stop/start, no stable Flow/Message action, with a required fresh
  snapshot/replay before any later activation.  The plan did not run against
  the live manager; other activation gates remain closed ([Field source](../../9ac67c/summary-flow-upgrade.md), line 143).

## Remote boundary

- On the latest retained Ouranos probe, Prometheus
  `200:ca41:6b12:fba:d7bc:cfc6:4aaa:165f` and Zeus
  `200:17f7:4fad:e50b:a50c:2048:2169:41f7` resolved via `yggTun`; one strict
  ten-second BatchMode root SSH to each timed out with exit `255`.
  Prometheus builder and Zeus SSH are unavailable; physical power is unknown
  ([Field source](../../9ac67c/summary-flow-upgrade.md), line 155).
- Laptop attachment remains unverified: `herdr --remote li@100.64.0.2 --session
  default` is a documented command shape and same-host route proof exists, but
  no independent laptop or peer-host attach was witnessed
  ([source](remote-access.md), lines 18-20; [access packet](laptop-remote-attach-access-packet-20260926.md), lines 7-20).

## Version/store boundary

- Source Flow main `9fcd625ac7a0d44be58b9d365a94064e91f09219` is `0.14.0`;
  retained live unit evidence is external Flow `0.12.2`
  ([source](../../38de5b/log.md), line 302; copied-pair witness at
  `stable-flow-message-copied-pair-20260926.md`, lines 33-35).  The copied live
  pair has direct hashes there: Flow `f03f610a9832378ef0f03fee16383266909d923051ccb5a71980cc9db78c0f03`,
  Message `4cb4e9ba3544a12afcb2d1771bfd67eb93e74d9aa6b898ba6251036061719457`.
- No isolated paired target read is proved: target Flow `0.14` was unresolved
  locally and the Message alternate-store/socket launch contract was not
  demonstrated.  The copied-pair witness is complete; target-read status is
  unknown ([source](stable-flow-message-copied-pair-20260926.md), line 35).
