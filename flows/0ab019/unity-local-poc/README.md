# Unity localhost POC implementation boundary

This isolated localhost POC has the edge
Unity Web -> Mentci Nexus -> labelled Persona POC seat. Mentci owns
`ObserveRoster`, `ObserveConversation`, and `SubmitPsyche`; Persona alone reads
Herdr and transcripts and targets an exact live pane. The old Mentci daemon,
Persona manager, Criome, provider APIs, XMPP, ntfy, and Tailnet are outside
this POC.

The browser bridge carries one binary WebSocket message per complete Signal
frame: four big-endian length bytes followed by the rkyv archive. Both sides
must refuse a declared length that differs from the message body. Signal's
archive validator retains depth 64. The POC additionally caps body bytes at
256 KiB, composition text at 64 KiB, and a conversation snapshot at 500
entries. The remotely built Rust-to-WASM wrapper exposes only constructors for the three
Mentci queries and decoders for their three paired replies plus typed
`OperationUnavailable`; it will not own roster, conversation, delivery, or
provenance policy.

Only an unforgeable `AcceptedUnityRoute` minted by the loopback listener lets
Mentci create `PsycheViaUnity` and call Persona with a `PsycheInput`. A decoded
`SubmitPsyche` by itself has no origin authority. Persona's reviewed one-flow
source reads only `flows/.effa1b.flow-id`, checks its full native UUID against
the exact Herdr pane/process, requires that process to hold the one observed
rollout path, and verifies the rollout's `session_meta` ID. It holds on any
mismatch, missing file, restart, or new rollout; no alias or path scan occurs.
Other flows are unavailable in this POC. The one-file Codex final-response
normalizer scans at most the first 4 MiB per request, at most 256 KiB per
line and 500 candidate entries, and reports `Partial` even when that first
page reaches EOF because user-role origin remains unproved. It never loads the
whole transcript, tails, polls, or invents a Living label. The bounded
Herdr/Persona and Mentci read path still requires a live witness. The
target-pane send witness is separately owned by the root flow.
The raw `psyche_text` is preserved; trimming is solely an emptiness check.
Historical transcript input with unresolved origin stays `Unknown`. A final
machine response is `source_kind=FinalResponse` with `Machine` provenance;
actor attribution is displayed as an attributed claim. Persona failure yields
`OperationUnavailable(PersonaUnavailable)`, never an empty successful
conversation. The send path preserves the input string exactly and reports
only the receipt grade actually witnessed. Mentci's accepted route mints a
private `PersonaApply` envelope; Persona also checks the kernel Unix peer PID
and rejects public `Query::SubmitPsyche` bytes. Before the fixed
`msg-psyche-poc` call, Persona writes and syncs a persistent SHA-256
request-ID/body/target attempt record. An identical retry returns its stored
transport receipt or a held-uncertain result without a new bridge call;
conflicting body/target is rejected. The ledger stores no raw text. Bridge
exit success can mean `TransportAccepted`, never target presentation or read.
Failure or uncertainty remains held without retry.

The process shape is one worker per local component, bounded requests, no
polling or transcript tail, localhost binding, and a combined user-systemd
ceiling of 384 MiB memory / 20% CPU. A live send witness uses the controlled
owned `effa1b` recipient, one benign unique marker, exact pane/native-session
binding, and separate target-side observation. The systemd ceilings are
configured limits; idle RSS must be measured after start.

No local compilation or browser suite is authorized while the living's
low-resource policy is active. `flake.nix` uses one fixed-output Cargo
prefetch stage for the committed lockfile and pinned Git/registry closure,
then offline host and wasm32 builds. It never relaxes the sandbox. The remote
daemon build uses `--option max-jobs 0 --option builders '@/etc/nix/machines'`.
Prometheus built the host package, generated the browser JS/WASM pair, and
ran the workspace tests. `packages.assets` places `index.html`, `app.js`,
`unity.css`, and the exact JS/WASM pair under the paths served by the Nexus.
The built WASM is not the native host `.so`.

The bounded unit serves `http://127.0.0.1:38081/`. `run-local.sh` starts
Mentci first to obtain its PID, then Persona with `UNITY_POC_MENTCI_PID`,
the reviewed `messaging-build` Herdr session, a private socket, and the
persistent attempt directory. The witnessed host and assets outputs are
`/nix/store/ck1qvkxxd91idmzyby8wa9ab1wipv4yg-unity-local-poc-0.1.0`
and `/nix/store/128cqrcpqs7ykkigxlzga80xk35v9a9m-unity-poc-assets`.
The exact start command is:

```sh
systemd-run --user --unit=unity-local-poc-0ab019 --collect \
  --property=MemoryMax=384M --property=CPUQuota=20% --property=TasksMax=32 \
  --setenv=UNITY_POC_PACKAGE=/nix/store/ck1qvkxxd91idmzyby8wa9ab1wipv4yg-unity-local-poc-0.1.0 \
  --setenv=UNITY_POC_ASSETS=/nix/store/128cqrcpqs7ykkigxlzga80xk35v9a9m-unity-poc-assets \
  /home/li/primary/flows/0ab019/unity-local-poc/run-local.sh
```

`probe-local.sh` checks the asset request graph. The read-only, Nix-built
canonical Signal/WS probe is:

```sh
/nix/store/ck1qvkxxd91idmzyby8wa9ab1wipv4yg-unity-local-poc-0.1.0/bin/unity-poc-mentci-probe read
```

The 2026-09-19 READ witness returned one exactly correlated `effa1b` roster
flow (`Working`) and three machine final-response entries from the initial
bounded transcript page; roster and conversation both reported `Partial`.
The selected entry's text was represented only by a SHA-256 and short
excerpt. This does not claim recent/full history. `send` requires an explicit
request ID and verbatim text; only the root flow conducts that controlled
witness. No browser suite runs on this laptop.
