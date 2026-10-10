# Spirit Luna/XHigh corrected Lojix activation executor — 2026-08-04

## Scope

Authorized target: CriomOS `9b3d344631628cb19dda1a22af4d7ef25c5f8def`.
Authorized rollback base: CriomOS `b46390940cf641e19bc9bbd243726308286a8bd2`.

This ledger retains only bounded non-sensitive evidence. No proposal contents,
provider request or response, Spirit corpus, credentials, session material,
private path, or closure/store path is recorded. No direct Home Manager/NixOS
activation, restart, source edit, bead update, or commit is authorized here.

## Gate 0 — persisted before any request

Captured: 2026-08-04T12:16:40Z (2026-08-04T14:16:40+0200).

| Witness | Safe observation | Classification |
| --- | --- | --- |
| Spirit version | `0.27.0`, not required base `0.26.0` | wired runtime; base gate fails |
| Spirit marker | `(25, 5374348791551424496)` | wired runtime; unchanged base marker |
| Judge | active/running/success | wired |
| Spirit daemon | active/running/success | wired |
| Daemon dependency/order | `Requires` and `After` include `spirit-judge.service` | wired |
| Spirit listeners | exactly `3` Unix sockets | wired |
| Kernel argv predicates | OpenAiCodex=true, Luna=true, XHigh=true, Terra=false, Medium=false | wired target-like activity |
| Judge executable identity | `spirit-judge` | bounded provenance witness |
| Active closure provenance | not retained: an exact source revision cannot be safely established without recording prohibited closure/store-path material | evidence-limited |

Decision: **target deployment is prohibited**. The required healthy
Terra/Medium base is absent, while the live runtime instead shows the target
Luna/XHigh predicates. Under the approved recovery rule, this is evidence of
target activity requiring the single permitted typed Lojix rollback.

## Rollback source gate

Pending immediate pre-send metadata-only reachability check for the exact
approved `.dotos` ProposalSource. No proposal content will be read.

Captured immediately before rollback admission: 2026-08-04T12:17:13Z.

| Witness | Safe observation |
| --- | --- |
| Exact path | `/git/github.com/LiGoldragon/goldragon/datom.dotos` |
| File metadata | regular file; owner `li`; mode `0644` |
| Daemon account and readability | daemon account `li`, equal to the checking account; readable |
| Parent traversal | every parent through `/git/github.com/LiGoldragon/goldragon` is traversable by that account |

The first attempted account-switch probe was unavailable to the unprivileged
operator and was not used as evidence; identity equality plus same-account
read/traversal checks above are the accepted witness.

## Rollback admission

Exactly one rollback request was sent through `meta-lojix`, with the approved
`UserEnvironment` owner tuple, exact `.dotos` ProposalSource, immutable base
revision, `ActivateNow`, `RequireImmutable`, `None`, and `[]`. The CLI's typed
reply was parsed as a complete `DeployAccepted` record, not substring-matched:

| Safe field | Value |
| --- | --- |
| Deployment identifier | `4` |
| Accepted marker | `(53, 53)` |

The submit shell did not capture a UTC clock value, and the user-unit journal
has no admission line from which to reconstruct one. The prior metadata gate
was at `2026-08-04T12:17:13Z`; this admission was its immediately following
operation. This timestamp gap is recorded rather than inferred.

## Bounded rollback correlation — failed

Seven ordinary typed `ByNode` polls ran at `2026-08-04T12:19:21Z`, `:26Z`,
`:31Z`, `:36Z`, `:41Z`, `:46Z`, and `:51Z`. Each complete reply was parsed as
DOTOS into an AST before inspection; no raw reply, closure, or proposal body
was retained. Each had a minimal typed generation row matching deployment ID
`4`, the exact rollback revision, `UserEnvironment`, `LiveActivation`, and
`Current`, but none contained the accepted marker `(53, 53)`. The same ID and
revision have historical rows, so the marker absence makes the row
uncorrelatable and it is not accepted as this rollback's `Current` receipt.

The bounded `lojix-daemon.service` user journal from `2026-08-04T14:17:00`
local time contained zero lines and therefore zero correlated terminal events.
It provides no terminal rollback witness.

Decision: **STOP — rollback admission is not durably correlated.** No target
POST validation, provider request, Spirit-corpus operation, source change,
direct activation, restart, extra deployment, bead update, or commit was run.

## Read-only runtime state after correlation failure

Captured: `2026-08-04T12:20:31Z`.

| Witness | Safe observation | Classification |
| --- | --- | --- |
| Spirit version | `0.26.0` | wired runtime; restored-base observation only |
| Spirit marker | `(25, 5374348791551424496)` | wired runtime; equals required base marker |
| Judge and daemon | active/running/success | wired |
| Dependency/order and listeners | judge in both `Requires` and `After`; exactly `3` sockets | wired |
| Kernel argv predicates | OpenAiCodex=true, Terra=true, Medium=true, Luna=false, XHigh=false | wired restored-base selection |
| Judge executable / argv witness | `spirit-judge`; SHA-256 `4a68e57370d6397bb3f481bead16edc396ee0317e3bf540f641d5956868890f3` | bounded non-content witness |

The Gate 0 snapshot recorded exact predicates but no argv hash. The later hash
is deliberately not attributed retroactively to that earlier process state;
the resulting race/evidence gap remains explicit.
