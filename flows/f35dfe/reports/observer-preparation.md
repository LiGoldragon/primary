# fnih — bounded read-only observer preparation; NOT ARMED

Publication/readbacks and source/gate controls are terminal; scoped Lock370 is Released. No ObserveSends process, transcript reader, inotify follower, clock observer, nix shell, provider call, harness session or runtime mutation has been started for this task. This is the requested pre-arm capability/command/fixture/limit report, not a live witness.

## Verified interface and exact commands

Actual PATH client is `/home/li/.local/bin/flow`, through the Home-managed executable; its local-only `--version` returns `flow 0.56.2`. A separate stale `.nix-profile` link is not the selected client. No endpoint query was used for this version read. Version alone does not establish the running server revision or the live opening frame.

Supported ordinary query arguments, each one argument, are:

```sh
/home/li/.local/bin/flow 'ObserveSends.None'
/home/li/.local/bin/flow 'ObserveSends.Some.<last-durably-retained-integer-cursor>'
```

The second line is a template: substitute the actual retained integer as part of the single Datom argument. There is **no StoreIdentity parameter** in the resume call. Compare the reconnect opening StoreIdentity to the first one before accepting replay; a changed identity or regressed highwater is a coverage failure, not a new baseline.

Source provenance: Flow612 `crates/flow/src/client.rs`, `crates/flow/src/main.rs`, `crates/flow-nexus/src/observe_sends.rs`, `crates/flow-nexus/src/message_projection.rs` and `crates/flow-nexus/src/store/logical_delivery.rs`. Its pinned signal-flow64 source is `83c04fefc087cf76dd3ca04792ff38b53b283b74`; exact generated fields are in `src/generated/signal.rs:1646–1660`, canonical round-trip fixtures in `tests/contract.rs:984–988`. Those authored fixture strings have been retained, without executing Rust or calling an endpoint, in `/tmp/browser-f35dfe.DEQupE/observer-preparation/source-contract-fixtures.json`.

Observed-by-source frame forms:

```datom
SendsObserved.{ store1 2 [ { req2 2 Sender.{ Mind flow Sol } { Psyche flow Opus } Attempting } ] }
SendChanged.{ req3 3 Sender.{ Mind flow Sol } { Psyche flow Opus } Delivered }
```

These exact two examples are **authored source fixtures**, not this observer's live output. The opening fields in order are StoreIdentity string, highwater DeliveryCursor integer, vector of snapshots. Snapshot fields in order are RequestId string, DeliveryCursor integer, VisibleSender variant, Address, VisibleDeliveryState variant. Flow-origin `SentBy::Flow` projects to **Notification**, not Sender.Flow. Neither frame includes message text, admission time, delivery time, flow generation, native-session identity or transcript path.

`None` returns current nonarchived snapshots plus a highwater; it is not an exhaustive historical-request inventory. `Some.cursor` returns retained events newer than the cursor. Opening replay can contain multiple state snapshots for one RequestId. Save every baseline ID and deduplicate **request identities** separately from `(cursor, state)` evidence. The subsequent stream uses `SendChanged`. The source client treats a streaming UnexpectedEof as normal CLI completion; client exit0 alone does not mean uninterrupted coverage. The service only writes supported output frames; `Refused`/unknown/malformed frames are failures to cover, not silence.

## Proposed collector anatomy and event ownership

One foreground Python supervisor in a new mode0700 scratch directory; at most two ordinary `flow` child processes, strictly sequential. No hidden shell pipe, tail follower or polling. The Python process owns inotify, a command pipe supplied by ROOT, a CLOCK_BOOTTIME timerfd and all child pipes; it blocks in one selector. It writes the opening frame and parsed metadata to durable scratch before READY, with fsync for StoreIdentity/cursor/baseline IDs and each replay checkpoint. Streaming parser framing must respect container depth and quoted strings, including chunk-split UTF-8/guillemets and embedded whitespace/newlines/braces. It must apply the pinned grammar rather than split on whitespace or lines. Unknown quoting/escaping cannot be guessed.

ROOT supplies a separate explicit CUT event with UTC, monotonic and BOOTTIME readings and actual serving Flow PID/start identity. Preserve the latest opening/highwater and all pre-cut IDs separately from post-cut observations. The collector must continue while ROOT performs its own Lojix operation and may receive one EOF at the daemon switch.

On first EOF, reap that exact child and retain stderr/exit/time/partial-frame state. If a complete persisted opening exists, allow **one** immediate supported `Some.lastCursor` child; no timer retry or fallback to None. Its opening must have the same StoreIdentity, nonregressing highwater and valid typed replay before a REPLAY_READY event. A failed launch, second EOF, refused cursor, new store, malformed/truncated frame or incomplete replay ends observation with a coverage gap. Event cursor need not be assumed contiguous without an explicit contract.

After ROOT provides exact mapping, follow **only** the authorized non-Fable native transcript by inode/offset with inotify. Extract only the exact matching delivered Notice with RequestId, sender Notification, expected ReminderText plus newline and exact handover path. Persist only that selected notice, native session/path, byte offset/row identifier and timestamp anchor; export no surrounding row/prompt/configuration or unrelated transcript text. A row that bundles unrelated content must be projected to the selected Notice rather than copied whole. Deduplicate mirrored native rows by the same RequestId; ordinary unrelated Notification requests are not additional reminders.

Exclude every Fable model/address before witness selection and transcript access. Choose the first qualifying natural reminder **observed/delivered after CUT**, with exact text and request join. Start the1200-second window at its retained anchor, or end after3600 seconds from CUT with no qualifying candidate. The latest possible total is4800 seconds from CUT when a candidate occurs near the end of the hour. Use CLOCK_BOOTTIME absolute deadlines so suspend counts; retain UTC and normal monotonic values for comparison. Known suspension/clock discontinuity or unread backlog at a deadline requires explicit coverage assessment; timer expiry alone cannot turn unprocessed events into silence. The final claim is bounded observed event coverage, not a global absence theorem.

Finite cleanup: close/reap the active flow child, both child pipes, inotify descriptors, timerfd and command pipe; TERM then a configured five-second KILL bound if necessary, retaining PIDs/start/group/exits and a final owned-group membership check. No broad kill or daemon action. Preserve stdout metadata, per-child stderr, readiness/cut/reconnect/gap/deadline/cleanup receipts and hashes. A disabled/killed collector reports incomplete observation, never success.

## Helper fixture acceptance BEFORE live arm

No collector implementation or fixture execution is claimed in this preparation report. These are the exact acceptance cases for its next bounded scratch-only preparation step:

1. Parse the five retained source fixtures into the declared field types; accept full opening and event frames independently of chunk boundaries. Test every UTF-8/chunk split and multiline/string-contained delimiters. Include malformed nesting, oversized frame and incomplete EOF: each must yield a gap without retaining string bodies from unknown frames.
2. Opening baseline req2/cursor2, then req3 transitions at cursors3/4: one new request identity, two state observations. Replayed req3 after EOF is still one identity. An unseen pre-cut req4 received before CUT belongs to the pre-cut set.
3. Notification to an authorized non-Fable address selects a candidate only after exact native Notice correlation. Sender-address messages, Fable, unmatched text, duplicate/mirrored native rows and other Notification notices do not increment reminder count.
4. EOF once after checkpoint2 permits exactly `ObserveSends.Some.2`; same-store opening with replay reaches REPLAY_READY. Different store, cursor regression, refusal, partial frame and second EOF each terminate incomplete. No retry sleeps and no None restart.
5. Synthetic ROOT CUT/timer events distinguish3600-second no-candidate from candidate+1200-second observation; simulate suspend through injected clock values and prioritize unread available data before a terminal decision. An explicit clock/backlog ambiguity ends with a gap.
6. Synthetic transcript files contain unrelated user text plus one matching delivered Notice. Output contains only the selected Notice and its metadata; no unrelated text. Rotation/truncation/inotify overflow, missing authorized file, changed native session or unrecognized native row grammar cause gaps.
7. Spawn only a local synthetic producer in the fixture test, force ordinary exit/hung-child cleanup, and verify supervisor/child/descriptor termination. No `flow`, model, account, Nix, service or real transcript is used in fixture execution.

Proposed configurable trial limits for review: initial/reconnect opening deadlines30 seconds each; one reconnect; wait3600 seconds; witness interval1200 seconds; outer post-cut4800 seconds; cleanup5 seconds; bounded parser bytes/row/backlog cap to be supplied before execution, with overflow a gap. These are proposed observer controls, not new Flow configuration or universal defaults. No exact Python launch command is represented as runnable until the helper and its fixture receipt exist.

## Explicit pre-arm gaps and required ROOT input

1. ROOT must provide exact non-Fable address/model exclusions, authorized native-session→transcript path/row mapping, exact ReminderText and handover path derived from its preserved Configuration, and the supported row shape to select the delivered Notice. None is inferred from an unrelated live transcript or global search.
2. No live opening has yet been read. After later explicit arm, readiness requires actual client PID/start/group and parsed/fsynced StoreIdentity/cursor/opening; source fixtures are not live endpoint evidence. ROOT must gate its switch on READY and retain any subsequent EOF/replay gap.
3. The CLI metadata has no request-admission timestamp. A frame first received after CUT can concern a request admitted before CUT and delayed in transit, especially across replay. Native receipt timestamps likewise establish receipt, not admission. If acceptance means **admitted** post-CUT rather than **delivered/observed** post-CUT, the current interface cannot prove that from these witnesses; ROOT must resolve the required meaning or supply independent creation-time evidence. Do not label a known pre-cut RequestId a new post-cut reminder.
4. Datom quoting/escaping and native notice-row extraction require verified parser behavior and synthetic fixture receipts before any live arm. This report identifies the exact pinned source/fixtures; it does not claim that a custom untested parser is a supported codec.

This returns the requested gap promptly and preserves the supported exact CLI path. ROOT retains configuration/Fable/actual-parent/Lojix/switch custody; no observer is armed and no new heavy/harness slot is consumed.
