# Listener Fresh-Context Handover

## Focus

Next session focus: get Listener from the landed first vertical slice to a usable production trial, while preserving intended future direction. Prioritize low-hanging correctness fixes, deployment under a separate keybinding from the existing working speech solution, and real daily testing.

## Settled Intent

- Listener is our own speech-to-text component family, not an extension of the forked Whisrs.
- The target shape is the local component mold: runtime repo with daemon and thin CLI, typed contract repo, and `signal-*` contract repo.
- Vertical slices are the priority because real use is the evidence path.
- The first capture path should follow the system default input source, not hard-bind to a removable node.
- The first delivery target is the system clipboard.
- Delivery must remain open to multiple configurable outputs, including later Mentci integration.
- PCM is the authoritative capture path for now. For batch transcription, post-stop compression/re-encoding can be conditional on file size.
- Opus/WebM is plausible for OpenAI batch upload when size matters, but realtime transcription should keep a PCM-oriented path unless current API evidence says otherwise.
- Future reliability features remain intended but deferred behind the usable slice: redundant multi-track capture, event-driven Bluetooth/default-source guard, RMS/silence alarms, heartbeat/watchdog, multi-channel alerts, typing into a window, and window/application tracking.

## Completed State

- Tracker epic `primary-qvud` and children `.1` through `.5` were closed.
- Repos were created and pushed:
  - `/git/github.com/LiGoldragon/signal-listener`
  - `/git/github.com/LiGoldragon/meta-signal-listener`
  - `/git/github.com/LiGoldragon/listener`
- `signal-listener` was updated to version `0.2.0` at commit `e2a390b0`.
- `meta-signal-listener` was updated to version `0.2.0` at commit `30ed2770`.
- `listener` final audited state is commit `2aaca2d4` on `main`.
- Listener currently has daemon/CLI start, status, and stop.
- Listener's ordinary Unix socket uses the exported `signal_listener::Frame` boundary and preserves exchange identity.
- Capture uses `parecord --device=@DEFAULT_SOURCE@`.
- Active capture writes one growing `.listenerlog` file containing PCM records.
- `.listenerlog` records are bounded, checksummed, and committed with `sync_data()`.
- Creation uses exclusive file creation so existing logs are not overwritten.
- Idle runtime paths discover/recover existing `.listenerlog` artifacts and advance session allocation above existing names.
- Stop recovers/truncates a valid log prefix, exports `.raw.s16le` for the configured STT backend, and dispatches the transcript to configured outputs.
- Clipboard delivery is the default output target.
- Real STT is configuration-dependent; when no backend is configured, the current stub behavior is explicit rather than claiming real transcription.

## Known Follow-Ups

- `primary-z1aq`: add typed Start/Stop conflict replies. Current ordinary state conflicts are still represented too generically; examples are start while already recording, stop when idle, and stop with the wrong session.
- `primary-llep`: validate crash durability on disposable storage. Needed evidence includes process-kill and storage/power-crash style tests around acknowledged sync boundaries.
- `primary-gm05`: decide policy for pre-header crash artifacts and trusted capture-store assumptions.
- Add post-stop transcription preparation: choose direct PCM/lossless upload versus compressed upload based on size/configuration. This should preserve PCM as the capture artifact and make compression a derived batch-upload artifact.
- Deploy Listener through CriomOS-home under a different keyboard binding from the existing working speech solution so both can be used side by side during the trial.
- Run a real microphone/clipboard smoke test after deployment, then daily-use testing.

## Live Uncertainties

- OpenAI batch transcription upload supports `webm` and other containers, with a 25 MB upload limit in current official docs. The docs list containers/extensions, not a precise codec acceptance matrix for Opus.
- OpenAI realtime transcription evidence points to raw audio session formats such as `audio/pcm` at 24 kHz plus G.711 variants. Treat WebM/Ogg Opus chunks as not established for realtime JSON audio-buffer input unless freshly verified.
- The durable `.listenerlog` design is suitable as an internal PCM spool for the current slice, but it should not be treated as a settled public audio format.
- Real crash durability still depends on filesystem/device honesty and needs disposable-storage validation.
- Orphan recovery is runtime-visible but not yet exposed as a distinct public wire status/reply.
- Session numbers avoid collision while same-named logs exist; old numbers may be reused if artifacts are manually removed.

## Evidence Pointers

- Scaffold handoff: `/home/li/primary/agent-outputs/RepoScaffolderListenerHandoff/RepoScaffolder-ScaffoldHandoff.md`
- Contract evidence: `/home/li/primary/agent-outputs/ListenerContractVerticalSlice/GeneralCodeImplementer-Evidence.md`
- Runtime slice evidence: `/home/li/primary/agent-outputs/PrimaryQvud4/GeneralCodeImplementer-Evidence.md`
- First audit: `/home/li/primary/agent-outputs/PrimaryQvud/RustAuditor-Review.md`
- Frame-boundary fix evidence: `/home/li/primary/agent-outputs/ListenerBoundaryFix/GeneralCodeImplementer-Evidence.md`
- Durability research: `/home/li/primary/agent-outputs/ListenerDurabilityStrategy/Scout-SituationalMap.md`
- Durability implementation evidence: `/home/li/primary/agent-outputs/ListenerDurabilityStrategy/GeneralCodeImplementer-Evidence.md`
- Fix-pass audit: `/home/li/primary/agent-outputs/ListenerFixPassAudit/RustAuditor-Review.md`
- Lifecycle durability fix evidence: `/home/li/primary/agent-outputs/ListenerLifecycleDurability/GeneralCodeImplementer-Evidence.md`
- Final lifecycle audit: `/home/li/primary/agent-outputs/ListenerLifecycleDurability/RustAuditor-Review.md`
- Tracker closeout: `/home/li/primary/agent-outputs/PrimaryQvud/TrackerWeaver-Closeout.md`
- OpenAI speech format scout: `/home/li/primary/agent-outputs/OpenAiSpeechToTextFormats/Scout-SituationalMap.md`

## Suggested Fresh-Session Entry

Load this handover, then start from the current Listener repos and tracker items. Keep the first pass practical: fix the small public-contract correctness issue if it blocks testing, add conditional post-stop encoding only if needed for the chosen STT backend, deploy under a separate keybinding, and run the first real microphone-to-clipboard trial.
