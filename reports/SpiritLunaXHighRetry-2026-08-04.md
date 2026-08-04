# Spirit Luna/XHigh Lojix retry executor ledger — 2026-08-04

## Scope and guardrails

This ledger records only bounded, non-sensitive deployment evidence for the
approved Lojix-only retry. No provider request/output, corpus, credential,
session material, inline configuration, store path, or private filesystem path
is retained. No direct Home Manager/NixOS activation or service restart is used.

Authorized target: CriomOS `9b3d344631628cb19dda1a22af4d7ef25c5f8def`.
Authorized rollback base: CriomOS `b46390940cf641e19bc9bbd243726308286a8bd2`.

## Gate 0 — pre-send bounded baseline

Captured: 2026-08-04T11:54:46Z (2026-08-04T13:54:46+0200).

| Witness | Safe observation | Classification |
|---|---|---|
| Spirit version | `0.26.0` | wired |
| Spirit marker | `(25, 5374348791551424496)` | wired |
| Lojix `ByNode` | typed query accepted; rollback revision observed six times; target revision absent | wired read model; historical rows are not a unique active-profile witness |
| Judge | active/running/success | wired |
| Daemon | active/running/success; `Requires` and `After` include `spirit-judge.service` | wired |
| Spirit listeners | exactly `3` Unix sockets | wired |
| Active Home closure / CriomOS source | profile source revision deliberately not recorded: exact source selection is not safely derivable here without retaining prohibited closure/store-path material | evidence-limited |
| Judge executable | executable identity SHA-256 `45cb7bb321daa7009928cc863e9af39c43443f326b15461b58c6592488e86af2` | bounded provenance witness |
| Kernel predicates | OpenAiCodex=true; Terra=true; Medium=true; Luna=false; XHigh=false | wired, healthy rollback-base selection |

Gate 0 decision: **PASS**. The live bounded runtime matches the expected
`0.26.0` / Terra / Medium base and marker. The target has not been sent at this
point.

## Deployment admission

Captured: 2026-08-04T11:56:25Z.

The sole authorized typed owner-channel request was submitted as
`Deploy(UserEnvironment(...))` for `goldragon` / `ouranos` / `li`, target
CriomOS revision `9b3d344631628cb19dda1a22af4d7ef25c5f8def`, `ActivateNow`,
`RequireImmutable`, `None`, and `[]`. The full reply was parsed as a complete
typed `DeployAccepted` record, rather than substring-matched.

| Safe admission field | Value |
|---|---|
| Deployment identifier | `4` |
| Database marker | `(44, 44)` |
| Classification | wired admission only; not terminal deployment proof |

Next gate: bounded ordinary-query correlation requires this same deployment
identifier, exact target revision, `UserEnvironment`, `LiveActivation`, and
`Current`, plus a correlated Lojix-daemon terminal event.

## Target correlation — STOP / rollback required

Bounded polls beginning 2026-08-04T11:57:29Z returned a typed ordinary-query
reply, but no row containing deployment identifier `4` or the target immutable
revision. Seven recorded attempts through 2026-08-04T11:57:59Z each had zero
correlated `Current` rows. A subsequent bounded query likewise had zero target
revision occurrences.

The same-day system Lojix-daemon journal had one terminal-pipeline line, but
zero safe witnesses for deployment identifier `4`, the target revision, or a
terminal `DeployAccepted`/`DeployRejected` event correlated to identifier `4`.
No journal payload was retained.

Classification: **required correlation absent**. Admission could have started
target activity, so this is a STOP condition for target acceptance and requires
the single authorized Lojix rollback path. No target POST validation was run.

## Rollback admission

Captured: 2026-08-04T11:58:53Z.

The sole authorized rollback `Deploy(UserEnvironment(...))` was sent through
`meta-lojix` for immutable base `b46390940cf641e19bc9bbd243726308286a8bd2`
with `ActivateNow`, `RequireImmutable`, `None`, and `[]`. Its complete reply
was parsed as a typed `DeployAccepted` record.

| Safe admission field | Value |
|---|---|
| Rollback deployment identifier | `4` |
| Rollback database marker | `(46, 46)` |
| Classification | wired admission only; requires revision-specific correlation |

The identifier was reused after the failed target pipeline; therefore marker
and immutable revision are both mandatory disambiguators for rollback evidence.
