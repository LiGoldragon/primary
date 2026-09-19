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
256 KiB and composition text at 64 KiB. Each on-demand history page reads at
most a 4 MiB source window, a 256 KiB line, and 20,000 records, retaining at
most 100 entries and 128 KiB of entry text. The remotely built Rust-to-WASM
wrapper exposes only constructors for the three
Mentci queries and decoders for their three paired replies plus typed
`OperationUnavailable`; it will not own roster, conversation, delivery, or
provenance policy.

Only an unforgeable `AcceptedUnityRoute` minted by the loopback listener lets
Mentci create `PsycheViaUnity` and call Persona with a `PsycheInput`. A decoded
`SubmitPsyche` by itself has no origin authority. Persona reads the complete
current Herdr roster. It associates a flow ID only for the two reviewed,
exactly bound seats: Codex `effa1b` and Claude `c8d79f`. Other seats have no
invented ID and report `Unknown`; a reviewed seat with a failed binding reports
`Unavailable`. Persona checks each full marker identity against the exact
pane/process and transcript header. Codex also requires the process to hold
the exact rollout FD; Claude requires its exact native task descriptor and
`uuid-version=uuid-v4` marker. A mismatch or restart holds the flow
unavailable; there is no alias/path scan. Conversation pages seek backward
through one fixed file snapshot via a typed cursor that checks native UUID,
device, inode, size, and byte boundary. Appends are separately reported as
`current_bytes`; truncation or replacement invalidates the cursor. `Complete`
means the observed snapshot was fully traversed, not that user-role origin is
known. Malformed or omitted records keep coverage `Partial`; they never become
inferred text. Reads never load a whole large transcript, tail, or poll. The
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
conflicting body/target is rejected. The ledger stores no raw text. Only an
exact `Delivered` line from the fixed bridge, followed by a fresh exact
Persona binding, can produce `TransportAccepted`; process exit alone cannot.
This does not attest target presentation or read. Failure or uncertainty
remains held without retry. The earlier held attempt is preserved.

The process shape is one worker per local component, bounded requests, no
polling or transcript tail, localhost binding, and a combined user-systemd
ceiling of 384 MiB memory / 20% CPU. The fixed bridge permits only the two
reviewed recipients; any next send witness is a living browser press with
fresh exact binding and separate target-side observation. The systemd
ceilings are configured limits; idle RSS must be measured after start.

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
`/nix/store/kiisxfwnfalhjivc6v65jn9v3nr415g9-unity-local-poc-0.1.0`
and `/nix/store/x6011cvd07ani3d8ikqm465i8fc19kzc-unity-poc-assets`.
The exact start command is:

```sh
systemd-run --user --unit=unity-local-poc-0ab019 --collect \
  --property=MemoryMax=384M --property=CPUQuota=20% --property=TasksMax=32 \
  --setenv=UNITY_POC_PACKAGE=/nix/store/kiisxfwnfalhjivc6v65jn9v3nr415g9-unity-local-poc-0.1.0 \
  --setenv=UNITY_POC_ASSETS=/nix/store/x6011cvd07ani3d8ikqm465i8fc19kzc-unity-poc-assets \
  /home/li/primary/flows/0ab019/unity-local-poc/run-local.sh
```

`probe-local.sh` checks the asset request graph. The read-only, Nix-built
canonical Signal/WS probe is:

```sh
/nix/store/kiisxfwnfalhjivc6v65jn9v3nr415g9-unity-local-poc-0.1.0/bin/unity-poc-mentci-probe read [effa1b|c8d79f [pages 1..16]]
```

The 2026-09-19 READ witness returned a `Complete` 12-seat Herdr roster with
exactly verified `effa1b` and `c8d79f`; the other seats have no asserted flow
ID. Claude `c8d79f` returned a `Complete` 1,726,029-byte snapshot with 51
entries. Codex `effa1b` returned `Partial` with an older cursor; a deliberate
second-page probe traversed backward and reported an intervening append via
`current_bytes` without shifting the fixed snapshot. The probe prints counts,
coverage, full UUID/path, and at most one entry's hash and short excerpt per
page, not a transcript dump. HTTP GET for the page, JS, CSS, codec JS, and
WASM returned 200. `send` requires an explicit request ID and verbatim text;
only the living browser press is authorized for the next witness. No browser
suite runs on this laptop.
