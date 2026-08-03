# Spirit 0.25.1 Recovery Activation Evidence

Date: 2026-08-03, Europe/Madrid  
Node and account: `goldragon/ouranos`, `li`  
Outcome: **accepted; rollback was not invoked**

## Transaction boundary

The approved executor activated only this immutable user-environment target:

- CriomOS: `e658bf55bb0f06af012c8edf429d519c3b238c93`
- CriomOS-home: `d2d02bb61eb3557594b2c302e2862e5e0f58fb86`
- Spirit: `eabe6c6d96112b46d15443e1c1a29d940605785f`
- requested effect: `ActivateNow`
- immutability policy: `RequireImmutable`

The preflight also resolved the immutable fallback revision
`3938a9235977b3edf1a37b2f982fd47a851a2a85`. It was not used because every
required acceptance witness passed.

## Recovery flow

```text
failed judge + collected unmanaged override
                  |
                  v
private verified backup -> isolated-copy Marker
                  |
                  v
Lojix immutable admission -> deployment 1 / generation 1 Current
                  |
                  v
managed override migration -> judge active -> daemon active
                  |
                  v
three listeners + 0.25.1 + unchanged logical Marker
                  |
                  v
                 ACCEPT
```

## Before activation

- `spirit-judge.service` was `failed/failed`, result `start-limit-hit`, with a
  three-line unmanaged drop-in replacing `ExecStart` with a collected target.
- `spirit-daemon.service` was `inactive/dead`; its `Requires` and `After`
  dependency on the judge remained correct.
- The target, fallback, Home, and Spirit revisions resolved exactly.
- The official Codex login status surface reported an authenticated session.
  No credential value was read or transported through an argument,
  environment variable, temporary file, or report.

## Store protection and pre-marker

The live database was copied while both Spirit services were down:

- retained directory:
  `/home/li/.local/state/spirit/recovery-backups/2026-08-03-e658bf55bb0f`
- directory mode: `0700`
- retained database copy: `spirit.sema`, mode `0600`
- size: `987136` bytes
- pre-activation `cmp` against the live database: identical
- retained Marker witness: `pre-marker.dotos`, mode `0600`

Remote-pinned Spirit 0.25.1 opened only a distinct copy with isolated socket
paths. Two consecutive Marker reads were stable, and Version reported 0.25.1.
The first disposable listener path exceeded the Unix socket length limit and
was rejected; the successful retry used a short private runtime path. Neither
attempt opened the production database. The disposable database copy and its
socket directory were removed after acceptance; the recovery backup and Marker
witness remain.

Pre-activation logical Marker:
`(974 7784350440604474991)`.

## Lojix activation

Lojix admitted the exact request as:

```text
(DeployAccepted (1 (9 9)))
```

Admission was not treated as success. The executor waited until the read-only
node query reported:

- deployment `1`
- generation `1`
- `UserEnvironment`
- `LiveActivation`
- `Current`
- exact immutable CriomOS revision `e658bf55bb0f06af012c8edf429d519c3b238c93`
- query marker `(19 19)`

## Acceptance witnesses

| Witness | Observed result |
|:--|:--|
| Managed migration | Obsolete override absent; effective `DropInPaths` empty |
| Judge unit | `active/running`, result `success`, main status `0` |
| Daemon unit | `active/running`, result `success`, main status `0` |
| Dependency | Daemon retains both `Requires` and `After` on the judge |
| Effective wrappers | `spirit-judge-daemon-service` and `spirit-daemon-service`, both executable |
| Live processes | `spirit-judge-0.1.0` and `spirit-0.25.1` |
| Unix listeners | Judge, working, and owner/meta sockets all listening |
| Spirit version | `0.25.1` |
| Judge request | `OpenAiCodex`; provider `codex-0.146.0`; model `gpt-5.6-terra`; effort `Medium`; timeout `180000` ms; session reference `codex-login` |
| Logical Marker | Live `(974 7784350440604474991)` equals isolated pre-marker exactly |
| Bounded read | Independent `Count` returned `24`; no corpus body was requested or printed |
| Failed-unit delta | Independent verifier observed no failed user units and no new unrelated failure |

The retained pre-activation bytes and live database bytes now differ, which is
permitted after a live database open. Because the logical Marker is identical,
no byte restore was attempted. No accepted production write test, corpus-body
read, service restart test, direct `systemctl` activation, or direct database
restore was performed.

## Independent verification

The independent read-only lane reached the same result and declared the
deployment **ACCEPTED**. Its durable evidence is:

`/home/li/primary/agent-outputs/SpiritRuntimeVerification/IndependentRuntimeEvidence.md`

No rollback condition remains open.
