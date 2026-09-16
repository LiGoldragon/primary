# Audit 2 of item 50, the cluster relay — Codex cf7879's corrections, 2026-09-16

Fable audit subflow of flow efa157, read-only. Witnessed unless marked *claim*. Scratch
copies were made under `/tmp` (source export, fixture, test run); nothing outside this
report was written in any repository.

## Verdict

1. **Fix (a) Context receipt optional — works, witnessed.** `context_for` falls back to a
   `Context` stamped `unreviewed: Context receipt unavailable` when `RELAY_CONTEXT_RECEIPT`
   is unset, and still refuses a receipt whose provenance does not match the selected
   source. Both branches covered by passing tests.
2. **Fix (b) ordinary Claude `type:user` — works, witnessed.** `user_body` matches
   `type=="user"` with `message.content` (e017054). Tests run offline: 14/14 green
   (10 `--bin relay` unit, 4 `tests/relay_process.rs`).
3. **Fix (c) Claude leg and Nexus leg with fanout — claimed only, and half-absent by
   design.** Fanout exists and excludes the source (81e6534), but *only the Codex leg
   delivers*. `RouteHarness::Claude` returns a hardcoded `Unavailable` ("no Flow-owned
   Claude prompt-relay invocation is installed"); `RouteHarness::Nexus` a hardcoded
   `BusyParkRequired`. No code path in the crate invokes `tools/prompt-relay` or the
   `FlowDeliver` transport. Codex states this honestly; it is not yet the fix. Nothing is
   enumerated live: routes come from a JSON file named by `RELAY_FLOW_ROUTE_FIXTURE`,
   members from the `RELAY_CLUSTER_MEMBERS` env string.
4. **Fix (d) process-level end-to-end test in a Nix check — works, witnessed.** Real
   `UnixListener` sockets, a fake Codex app-server thread, the relay binary spawned via
   `CARGO_BIN_EXE_relay`; wired into four Nix checks. Not a change-detector: it asserts
   bytes on the wire.
5. **Fix (e) reconcile the signal-message pins — MUST CHANGE, disconfirmed.** The dual pin
   is still live. `cargo tree -i signal-message` on the branch answers *ambiguous*, listing
   both `rev=a9708f3384af` and `rev=81f659e5ceb4`, and the build compiles both copies of
   `signal-message v3.0.0`. Commit 76e391d ("Drop the dual signal-message pin") removed the
   direct duplicate; the second still arrives through `meta-signal-message`. The
   store-migration branch pins `81f659e5…` directly, the relay branch `a9708f3384af`.
6. **MUST CHANGE — new, witnessed loop hazard.** The relay binary's loop guard
   (`is_cluster_relay_record`) only recognises *its own* emitted header (`Relay.{ … }`), not
   the header the tool actually in use emits. Fed the real record `611f76ba` from this
   session — a turn already relayed — relay accepted it and emitted a fresh `Relay.{…}`
   whose body is the previous relay's `{"provenance":…}` header plus the living's words,
   sha `862fb694…`, exit 0. The tool that delivered today's turns refuses exactly this.
7. **Today's four turns were delivered by `/home/li/primary/tools/prompt-relay`, not by
   Codex's relay binary.** The header is a JSON stand-in, not the `ClusterMessage` datom.
   The "no unmarked human user input matches" refusal is a loop guard by design.
8. **Sha discrepancy.** Codex cites the process test at
   `109065a4ec61960823f0a98859f537ad93692270`. No such object; it is
   `109065a4ec6108e79f83ac380d5249f519470d0d`. The other three cited shas resolve exactly.

## Evidence

**(1) Branch and commits.** `origin/proposal/cf7879-message-ordinary-claude-parser-signed-upstream`
(tip `c60a8f2556dedc8e4124e49a2b87cfba464f096c`). Codex's stated branch name
`proposal/cf7879-message-ordinary-claude-parser` does not exist; the `-signed-upstream`
suffix does. Fixes in source: `e0170540e811e7821e5b0308157b1bf3315ebbb9` (parse ordinary
Claude records, preserve text parts) and `7d262e2` (that parser as a Nix check) = (b);
`b445785`, `a19db25`, `6be5ca0ec9bbdc2fa07c8111d6eee98e9c909de4` and
`109065a4ec6108e79f83ac380d5249f519470d0d` (bound fixture socket) = (d);
`81e65343d408d7a5f8410bdcaaa9a72fbffa8f04` = the partial (c); the Context fallback is in
`src/bin/relay.rs`. The incident is preserved: `origin/…-preserved-78ad6915`
(`78ad691594f03…`) and `origin/…-preserved-2ba7a9d3` both exist, sharing parent
`73cd2ec8210f8ed990a4399f0a0f46637c48393e`. Absent from every branch: any Claude delivery
invocation, any `FlowDeliver` invocation from fanout, any live route or member lookup.

**(2) Parser and tests, run offline.** Source exported with `git archive` to `/tmp/msg-audit`,
built with `CARGO_NET_OFFLINE=true` reusing the repository's existing target dir; finished
in 8.03 s, no network. `--bin relay`: 10 passed, incl.
`ordinary_claude_user_record_is_selected_without_a_queue_operation` and
`ordinary_human_discussion_of_relay_is_not_excluded`. `tests/relay_process.rs`: 4 passed. None is a change-detector — each runs the binary or the parser over a record and
asserts the selected body/sha, not a stored string. The flake's `cargoTestFile` helper
`rg`-greps the test name out of the test file before running, so a renamed test fails the
check instead of silently filtering to zero.

**(3) Fanout.** `fanout()` iterates `RELAY_CLUSTER_MEMBERS` (comma-separated `flow@session`,
validated for session uniqueness), filters out the member whose flow *and* session equal the
located source's, and maps each survivor to an independent `FanoutOutcome`
(`accepted` / `unavailable` / `busy-park-required`) — a failing target cannot erase another
target's receipt. Per member the route must be exactly one in the fixture, else
`Unavailable`; a Codex route without an endpoint, or a socket error, likewise degrades to
`Unavailable` rather than aborting. The fanout test witnesses 3 outcomes from 4 declared
members, two accepted against two real fake sockets, one unavailable.

**(4) The process test.** `tests/relay_process.rs` binds real `UnixListener`s under a temp
dir, runs a hand-rolled websocket server on a thread, spawns the real binary, and asserts
`turn/start` carried `params.input[1].text == BODY` byte-for-byte and `threadId` per target.
Seven `message-relay-*` Nix checks on the branch cover the parser, the process fixture, the
Codex socket fixture, the route fanout, both loop-exclusion cases, and the context refusals,
beside the pre-existing flow_delivery and relay_fixture checks. The auditor did not run nix.

**(5) Who delivered today's four turns.** Records 611f76ba, 0485c592, 3f7ed6fb, 1108ba10 are
`type:"user"`, `origin.kind:"human"`, `message.content` a single string beginning
`{"provenance":{"source_path":"/home/li/.codex/sessions/…","source_format":"codex","source_message_id":"msg_01a0a72…","source_timestamp":…,"sha256_utf8":…}}`, then a blank line, then the
living's words. That object is exactly `payload()` in `/home/li/primary/tools/prompt-relay`
(node, 105 lines), written into the session PTY as a bracketed paste by `claudeDeliver`. It
is **not** a `ClusterMessage` datom — no `Relay.{`, no guillemets, none of the nine
`ClusterRelay` positions. All four name a Codex rollout as source: Codex → prompt-relay →
Claude. Codex's relay binary was not involved. The refusal is by design: `marked()` treats a
record as already-relayed when its first paragraph parses as JSON carrying
`provenance.source_message_id` and `provenance.sha256_utf8` (it also rejects `[RELAY `,
`[PEER `, `[WAKE `, `[SYSTEM `, `<system-reminder>`), and `select()` then raises
`no unmarked human user input matches`.

**(6) The witnessed re-relay.** Fixture: record `611f76ba` copied verbatim to
`/tmp/fixture.jsonl`. `FLOW_ID=efa157 RELAY_SESSION_ID=efa15708-… RELAY_CLUSTER_MEMBERS=efa157@efa15708-…
RELAY_TRANSCRIPT=/tmp/fixture.jsonl relay '<first six>' '<last six>'` → exit 0, stdout
`Relay.{ efa157 efa15708-… /tmp/fixture.jsonl «{"provenance":{…}} So, are you the primary»
«tree, and then you merge primary?» 862fb694…`. The prior relay's provenance header is now
inside the relayed body and inside `Context.what_living_said`. `is_cluster_relay_record`
misses it twice: it only inspects *array* content (this record's content is a plain string)
and only matches a `Relay.{ … }` header. Until relay and prompt-relay agree on one marking,
running both over one transcript loops.

**(7) Pins.** Relay branch `Cargo.toml`: `signal-message rev = "a9708f3384af"`.
`origin/message-store-migration-cf7879`: `rev = "81f659e5ceb498edee84c1a3ac336d188916714f"`.
The relay branch's own build compiles both revisions. Fix (e) not done.

## Files read

`/home/li/primary/.claude/worktrees/flow-840e42/flows/840e42/reports/clusterRelayAudit.md`;
`/home/li/primary/tools/prompt-relay`; the live transcript
`…/-home-li-wt-github-com-…-claude-successor-840e42/efa15708-dc5d-42ce-af62-8ffb84c9815e.jsonl`
(read only); and in `/git/github.com/LiGoldragon/message`, via `git show`/`git log` on the
parser branch, both preserved branches, `origin/message-store-migration-cf7879` and
`origin/main`: `src/bin/relay.rs`, `src/relay.rs`, `tests/relay_process.rs`, `flake.nix`,
`Cargo.toml`.
