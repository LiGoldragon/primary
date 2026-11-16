# Protected Fable: restart prerequisite, not yet satisfied

Source examined: exact 2a2603d125183c2478cc7481b2e565d4eb33d154, proposed predecessor of the separately gated 0.56.3 release. No source or runtime changes made during this audit.

## Established source behavior
- `crates/flow-nexus/src/lib.rs:2341-2370`: `StopsNexus::stop` requests observer/accept-loop shutdown and announces store/launch/reminder/config changes. This body does not itself close native harnesses.
- `src/main.rs:153,173`: startup reconciles interrupted launches before serving and starts `recover_wakes` alongside sockets.
- `src/store/context.rs:154-198,205-230`: both warning-policy and ordinary-threshold paths return Protected for protected addresses rather than Past. `src/waking.rs:4075` separately excludes protected addresses from the below-threshold legacy warning refresh condition. This proves automatic-context exemption, not all recovery exemptions.
- `src/waking.rs:1719-1830`: recovery takes up deliveries, restarts, launch/reap obligations, pending successors and ordered replacements. These are durable obligations, not unconditional new launches on every daemon start.
- `src/restarting.rs:1625-1654`: a persisted Closing restart can call `closed_old` and then `resumed`. This recovery loop does not check ProtectedAddresses before doing so.
- `src/waking.rs:1780-1816`: ordered/replacement successor intents can be taken up through `take_up_owed`; `2465-2508` recovers ordered replacements. Protection is not a blanket veto on these explicit lifecycle obligations.
- `src/waking.rs:297-348`: `rest_ended_awake` can mark an Awake address Asleep when its stored flow lifecycle is not live, rather than proving native liveness from an extant process.

Consequently protection alone is insufficient to guarantee RUNNING AND UNREPLACED across recovery. The source permits explicitly recorded lifecycle work on protected addresses. This is not evidence that Fable currently has such an obligation. Its actual persisted obligation state is UNKNOWN here; no raw Memory or backup was read. No supported typed query exposing the complete necessary obligation set has yet been verified in this audit.

## Actual process/service evidence
Field inventory receipt `flows/ad72ed/guard86s0-prereq.md`, snapshot 2026-11-16T03:26:30Z: Fable 03ebbe / native session03ebbe1a-df0a-5238-b037-a13fcad9d999 / Claude PID645002, start_ticks36422916, is in Herdr6405 transient Ghostty scope. Flow826231 is in a separate sibling service cgroup, effective KillMode control-group. No observed PartOf/BindsTo linkage or ExecStop/ExecStopPost to Herdr. This supports current kill-scope separation only. It does not prove future source recovery behavior or future identity preservation.

## Disposition
Restart approval remains HELD. Next establish, through a verified supported typed read if one exists, that this exact live Fable binding is live and carries no pending restart, successor, replacement or reap obligation capable of closing/replacing it; then review all startup obligation paths against that concrete state. If the contract cannot expose the prerequisite, report the observability gap before restart rather than substituting raw Memory or assuming no obligation. No source workaround, protection expansion or runtime clearing is authorized by this audit.

Field slot01no permits local source preparation only: ordinary65 generation owns the heavy slot; guard code generation/gate requires later fresh clearance. No witness selection or due-event mutation has been performed.
