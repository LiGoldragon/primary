# v2xj / fnih / 4u71 — observer implementation and synthetic fixtures

**Prepared, not live-armed.** No real ObserveSends/Inspect invocation, native transcript access, provider/model/harness action, install, build, configuration change, Realize or Activate was performed. Ordinary Flow messages were sent to Field core. This report answers the implementation/pre-arm preparation order; ROOT retains activation and arm authority.

## Artifacts and evidence

Scratch directory: `/tmp/browser-cb6b4a-observer.Eijj7K` (0700).

- `observer.py`: standard-library-only Python collector; SHA256 `8f99d7361d268367fc67015f70602be2c5763593693b5cb5c9d8346d7ced9ec1`.
- `test_observer.py`: synthetic fixtures, SHA256 `6331cfca11993db1649ede95962115253b0e1c247eed497069e7d939cfeab8eb`.
- `limits.json`: explicit trial controls, SHA256 `f8962b72cb3a18e66e705a6551eb3bcfe48088dbdb214de1f56684978f6a2983`.
- `fixtures.log`: **22 tests passed**, SHA256 `95848da10a66859d60c5ac41932e47f8e40b67541b6ba4e352a9cafdd37cb8ab`.
- `SHA256SUMS`: checks those four artifacts. Repeat fixtures with `cd /tmp/browser-cb6b4a-observer.Eijj7K && python3 -m unittest -v`; this runs only local synthetic children and temporary synthetic transcripts.

Fixtures cover the five retained pinned-source examples at every byte split; split UTF-8, nested/escaped guillemets and multiline delimiters; malformed/truncated/oversized/unknown frames; typed address/request/state rejection; baseline identities versus transitions/replay; one resume with exact cursor, changed store/regression and second EOF refusal; baseline queued request first received after CUT; mirrored/pre-cut/ambiguous receipts; actual non-short-UUID Flow identifier rendering; deferred Inspect and exact UUID filename lookup; non-Fable exclusion before mapping; selected Notice-only export from a bundled private row; actual synthetic inotify receipt follow and CUT; no-candidate/witness deadlines; injected suspend/clock/backlog gaps; missing file, rotation/truncation and inotify overflow; normal and SIGTERM-resistant child cleanup, descriptor closure and empty final owned groups.

These fixtures are synthetic acceptance evidence, not a running-server or real native-receipt witness. The helper deliberately fails closed on unsupported wire/native grammar, incomplete mapping, limits or timing ambiguity.

## Precise launch, only after a new explicit arm order

ROOT must confirm the input configuration remains applicable, verify hashes, and choose fresh nonexistent output, CUT and FIFO paths. Example invocation below is concrete and **has not been executed**:

```sh
python3 /tmp/browser-cb6b4a-observer.Eijj7K/observer.py --arm \
  --inputs /tmp/field-0v72-deploy-83rhvist/observer-inputs.json \
  --limits /tmp/browser-cb6b4a-observer.Eijj7K/limits.json \
  --output /tmp/browser-cb6b4a-observer.Eijj7K/live-01 \
  --cut-file /tmp/field-0v72-deploy-83rhvist/observer-cut-01.json \
  --control-fifo /tmp/browser-cb6b4a-observer.Eijj7K/control-01.fifo \
  --flow /home/li/.local/bin/flow \
  --flow-meta /home/li/.local/bin/flow-meta
```

Run as the foreground managed command, retaining its PID and eventual exit. Do not add a shell pipeline or background follower. Output/FIFO/CUT must be absent; the helper refuses an existing CUT, so it must arm before the actual activation. The ROOT input was supplied mode0600 and names configuration SHA256 `2672fcfd9468a55c72b66b762ace11abd41d72ac9bf01780015472fc32820d67`; it contains eleven policies with identical exact ReminderText and the configured scoped roots. It is read only when explicitly armed.

The collector launches `flow ObserveSends.None`. A first complete opening is typed, its store/cursor/baseline and request evidence are atomically persisted and fsynced, then `events.jsonl` receives a fsynced **READY** containing the exact child's PID, start ticks and process group. **PREPARED is not READY.** ROOT must read READY and check the observer has not subsequently emitted GAP/EOF before activating. No actual READY exists now.

On the first complete EOF the collector retains metadata, bounds the exact child's reap, and allows one sequential `ObserveSends.Some.<durable cursor>` launch. Same-store/nonregressing typed replay is required before REPLAY_READY. Partial EOF, second EOF, refusal or failed replay ends in GAP. Every reconnect is explicitly a coverage interruption; this implementation does not promote successful replay into continuous silence/queue proof.

## ROOT-controlled actual CUT

After actual activation, ROOT atomically renames a fresh mode0600 JSON file onto the exact CUT pathname. The parent already has an inotify watch. The file must belong to the invoking user, be regular, fit the configured bound, and contain:

```json
{"utc":"<actual activation UTC with timezone>","boottime":0.0,"monotonic":0.0,"new_flow_pid":1,"new_flow_start":"<proc stat start ticks>","boot_id":"<proc sys kernel random boot_id>","uncertainty_seconds":0.0}
```

The numeric examples are placeholders, not measurements: ROOT supplies actual CLOCK_BOOTTIME, normal monotonic and UTC readings with their uncertainty, and the **new serving Flow process** PID/start ticks. The helper compares current boot/PID/start and clock consistency. It refuses an early/repeated/replaced, malformed or timing-inconsistent CUT. Never substitute Evaluate start, build completion, observer start or predicted activation time. ROOT retains the actual activation receipt alongside this event.

A matching first native receipt already observed while CUT delivery was pending is reevaluated against actual CUT time. A pre-switch receipt stays pre-switch; a baseline queued ID first received afterward is eligible. Overlapping uncertainty intervals remain a gap. Admission time remains unknown.

## Mapping, correlation and privacy

Each first non-Fable Notification address schedules one exact `flow-meta 'Inspect.{ Aspect topic Model }'`. Only the current exact-address FlowNode projection is retained; the full reply, queues, history and unrelated strings are not written. A canonical native UUID is required. Only filenames matching that UUID under the supplied Claude/Codex roots are inspected; no file content is read during filename lookup. Missing/ambiguous mappings end with GAP. Every Fable address is excluded before Inspect or transcript access.

The helper follows only mapped exact files by inotify/inode/offset. It supports Claude user text/string-text-block rows and Codex `event_msg` user-message rows, including the Flow source's `payload.item.UserMessage` form with matching native thread identity. It extracts a typed delivered Notification Notice from the native input vector, even when context shares the row. The text must be exactly configured ReminderText plus `\nflows/<actual Inspect FlowId>/handover.md`; the Flow identifier is not inferred from native UUID or length. Request identity and trustworthy timezone-qualified native row timestamp must correlate. Only the selected Notice and request/native/path/offset/row/time metadata are exported. Mirrored rows retain one first receipt per RequestId.

The live grammar and correspondence have not been inspected in this preparation. Unknown forms are not evidence of absence. Current Inspect binding alone cannot prove which previous native generation received a request; an unavailable/inexact mapping remains an explicit limitation. The observer makes no post-CUT admission claim.

The Datom parser is a bounded, tested subset: all five source fixtures, ordinary unit states and the two authored retry payload forms are supported. Other payload-bearing states, including Failed and other Retryable reasons, conservatively end in `unsupported-state-payload` rather than being guessed. This can shorten a live trial and must be accepted before arm or extended/tested in a further preparation release.

Raw native rows and full Inspect replies remain memory-only. Stderr is bounded in memory and represented on disk by length/hash/completeness, not raw strings; this preserves the Notice-only content-export limit at the cost of raw stderr diagnostics.

## Bounds and terminal contract

`limits.json` supplies opening/Inspect30s, one reconnect, no-candidate3600s, witness1200s, post-CUT outer4800s, total arm5400s and cleanup5s. Frame/child output1MiB each; native row4MiB; per-event transcript read64MiB; exact-filename traversal200000 entries; mapping32 addresses; ledger5000 requests/10000 distinct evidence rows. Every overflow ends with GAP. Times, counts, paths and commands are explicit invocation/configuration, not environment defaults.

Linux CLOCK_BOOTTIME absolute timerfd deadlines count suspension. Known suspend, wall-clock inconsistency, queued readable backlog, partial frames/rows or pending Inspect at deadline ends incomplete. Data ready in the same selector batch is processed before the timer; remaining readiness becomes a gap. No periodic polling, retry sleep, broad transcript search, hidden tailer or None fallback is used.

`BOUNDED_END` means only that this observer's supported continuous interval reached its configured end; it explicitly carries `global_absence_proven:false`. It is neither a global silence theorem nor queue proof. A reconnect, killed observer, ambiguous cut, unknown row/mapping or unprocessed backlog cannot produce a complete result. `final.json` is authoritative only after cleanup and process exit: `complete:true` requires bounded end with no gap; exit2/`gap:true` is incomplete. Natural receipt evidence may be retained with explicit incomplete coverage.

ROOT can request event-driven bounded stop with `printf 'STOP\n' > /tmp/browser-cb6b4a-observer.Eijj7K/control-01.fifo`; this intentionally records incomplete observation. TERM/INT likewise request incomplete cleanup. Owned children receive TERM then configured BOOTTIME-bounded KILL through their own process groups, are reaped, and final group membership is checked. Pipes, pidfds, selector, inotify, timerfd and transcript files close; the FIFO is removed. No daemon or unrelated process is signalled. Final receipts retain PID/start/group/exit and remaining-group facts. An external SIGKILL cannot produce a successful cleanup receipt.

ROOT must retain output/exit and inspect `events.jsonl`, `checkpoint.json` and `final.json`; scratch removal is ROOT's later choice after receipt retention. No observer or fixture child remains running from this preparation.
