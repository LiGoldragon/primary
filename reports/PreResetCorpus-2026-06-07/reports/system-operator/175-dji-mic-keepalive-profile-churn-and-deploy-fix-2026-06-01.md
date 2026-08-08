# DJI Mic Keepalive Profile Churn And Deploy Fix

## Frame

The DJI Mic keepalive was intermittently failing to keep the microphone hot for
Whisrs. The symptom was a two to three second wake-up delay at speech-to-text
start, with the keepalive loop sometimes present and sometimes ineffective.

The live system also exposed two unrelated deployment blockers while rolling the
fix through production:

- CriomOS depended on repository-ledger through localhost gitolite URLs, which
  cannot be fetched by remote builders.
- repository-ledger production config still emitted quoted NOTA strings, which
  the current NOTA decoder correctly rejects.

## Probable Cause

The DJI Mic advertises a Handsfree UUID but not a Hands-Free Audio Gateway UUID.
The previous keepalive implementation repeatedly called BlueZ `ConnectProfile`
for the handsfree profile during recovery. Local bluetoothd logs showed repeated:

- `Unable to get Hands-Free Voice gateway SDP record: Host is down`
- `br-connection-page-timeout`
- `Failure: No such entity`

BlueZ documents `ConnectProfile(string uuid)` as a request to connect a specific
remote service UUID on the device. WirePlumber documents distinct HSP/HFP roles:
`hsp_hs`, `hsp_ag`, `hfp_hf`, and `hfp_ag`, and notes that `bluez5.roles`
controls which roles are enabled. The host using a Bluetooth microphone as a
peripheral should behave as the audio gateway side, not hammer the remote device
as if it provided the opposite gateway role.

The Red Hat BlueZ bug for the same bluetoothd log pair ties this error to
profile connection failures, matching the local failure shape.

Sources:

- https://lira.epac.to/DOCS/wireplumber/html/daemon/configuration/bluetooth.html
- https://bluez.readthedocs.io/en/latest/device-api/
- https://bugzilla.redhat.com/show_bug.cgi?id=2179045

## Implemented

CriomOS-home:

- Removed all BlueZ `ConnectProfile` calls from `dji-keepalive`.
- Recovery now reasserts only the PipeWire/Pulse profile and default source.
- Added bounded retry backoff for repeated failed preparation.
- Added a check that the generated keepalive script does not contain
  `ConnectProfile`.

CriomOS:

- Restricted WirePlumber Bluetooth roles to the host-as-audio-gateway side for
  HSP/HFP while keeping A2DP/BAP roles.
- Added a desktop audio policy check for the role split.
- Repinned CriomOS-home to the keepalive fix.

Deployment portability:

- Created/pushed GitHub mirrors for repository-ledger and its signal contracts.
- Moved repository-ledger Cargo dependencies off localhost gitolite URLs.
- Moved CriomOS `repository-ledger` flake input to GitHub and repinned it.
- Converted repository-ledger generated daemon config and gitolite hook output
  to bracket-form NOTA, with checks preventing quoted string regression.

## Verification

Passed locally or through Prometheus:

- CriomOS-home `dji-keepalive` check.
- CriomOS `desktop-audio-policy` check.
- repository-ledger and owner-signal-repository-ledger `cargo fmt` and
  `cargo test --jobs 2`.
- CriomOS `repository-receive-role-policy` check.

Live observed after the first switch:

- `dji-keepalive.service` active.
- `wireplumber.service` active.
- Keepalive loopback process attached to the DJI Bluetooth source.

## Current State

The audio fix is live in the current system generation. The final FullOS switch
for the tuple-form repository-ledger config succeeded after Whisrs returned to
idle.

Live verification after the switch:

- `repository-ledger.service` active.
- `dji-keepalive.service` active.
- `wireplumber.service` active.
- PipeWire shows an uncorked `dji-mic-keepalive-capture` source-output targeting
  the DJI Bluetooth source.
- Recent bluetoothd logs showed no new `Hands-Free Voice gateway`,
  `br-connection-page-timeout`, or DJI-related failures.
- System temperature returned to ordinary idle range after the remote-build
  switch completed; no runaway local build process was present.

## Follow-Up

The gitolite direct hook request still deserves a separate focused test. The
module now emits valid bracket strings, but the direct CLI request should be
checked against the current signal operation head shape so that commit
observations are not silently falling back to spool-only notification capture.
