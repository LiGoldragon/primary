# codex-quota-reset audit

Subject: primary `proposal/f55ec8-codex-quota-reset` at c518a99f17496accebe1278c3b8352930a92f02b, `tools/codex-quota-reset/`, read in the clone `/tmp/f55ec8-reset` (HEAD is that branch at that commit). Read-only Fable audit, 2026-09-16. No live socket opened, no credit consumed, nothing edited outside `flows/f55ec8/reports/`. Mutations were run on a scratch copy under `/tmp/f55ec8-audit/m`, never on the clone.

## Verdict: must change

The program does what the seven claims say on the happy path and never double-spends. It must change before the secondary installs it under a timer, for one reason of substance and two of proof:

1. The crash window is handled by refusing forever, not by the safe retry the living asked for. Once `ResetAttempted` is logged (`codex-quota-reset:98`) and the consume call dies, times out (10 s, `app-server.mjs:55-58`), or errors before `ResetConsumed` is logged (`:104`), every later run for that window says `ResetHeld.{ alreadySpentThisWindow }` (`:97`, `state.mjs:47-48`) and never calls again. Nothing was necessarily spent. The protocol's own remedy is the one the living named: resend with the same `idempotencyKey` and the backend answers `reset` or `alreadyRedeemed` (schema: "reuse the same value when retrying that attempt"; `alreadyRedeemed` = "The same idempotency key already completed a reset successfully"). The tool forbids exactly that retry, so a slow backend on one tick silently forfeits the window's reset, and the log then lies about it.
2. The crash-safety claim is stated in source but not witnessed by any test. Two mutations that break it pass green: dropping `ResetAttempted` from `alreadySpent`, and moving the `ResetAttempted` write to after the consume call.
3. The two-day floor is witnessed at 3 days (spend) and 1 day (hold) but not at the boundary; `<` mutated to `<=` passes green. README says "more than the minimum days" (`README.md:46`), code and policy comment say at least (`codex-quota-reset:89`, `policy.useReset.datom:2`).

Everything else claimed is witnessed. Five of my eight mutations went red; the three survivors are the items above.

## Claims

Command for every "green" below: `cd /tmp/f55ec8-reset && timeout 300 node tools/codex-quota-reset/tests/codex-quota-reset.test.mjs` printed `codex-quota-reset fixtures passed`, exit 0, 0.5 s. Mutation runs: `bash /tmp/f55ec8-audit-mut.sh` (copies the tool to `/tmp/f55ec8-audit/m`, applies one `sed`, runs the same test file).

### 1. One-datom CLI, no flags. Witnessed.

`codex-quota-reset:48-49`: `process.argv.slice(2)` must be exactly one value or the run is refused `malformedRequest`. `:29-44` parse `Check.{ policy socket clock }`. No flag parsing anywhere (`grep -n -- "--" tools/codex-quota-reset/*.mjs codex-quota-reset` finds none). Policy path must be absolute (`:34`).

### 2. `account/rateLimits/read` with `capabilities.experimentalApi: true`, binding window. Witnessed.

`app-server.mjs:131-134` sends `initialize` with `capabilities: { experimentalApi: true }`; test asserts it from the fake's recorded requests (`tests/codex-quota-reset.test.mjs:51-52`); mutation `experimentalApi: false` went red (actual false, expected true). `codex-quota-reset:68` calls `account/rateLimits/read`. Binding = the window with the greater `usedPercent` (`observe.mjs:26-28`); mutation inverting it went red (`QuotaObserved.{ 80 2026-09-26... }` against expected `60 2026-09-20`). The protocol schema (`codex app-server generate-json-schema`, codex-cli 0.153.4, offline) confirms the field shapes read: `RateLimitWindow.usedPercent` int32 required, `resetsAt` int64 nullable; `RateLimitResetCreditsSummary.availableCount` required, `credits` array-or-null, "the backend may cap this list". The tool handles null credits as `creditDetailUnknown` (`:91`) and a capped list by spending from what it sees; acceptable.

### 3. Soonest non-null `expiresAt`, `creditId` never omitted. Witnessed.

`observe.mjs:56-67`: filter `status === 'available'`, sort by `expiresAt` with null last, then `grantedAt`, then id. `codex-quota-reset:100` passes `{ creditId, idempotencyKey }`. Test `:59-72` asserts `credit-soon` named from a fixture that lists `credit-late` first and a `redeemed` credit. Mutation dropping `creditId` went red (actual undefined, expected `credit-soon`); mutation reversing the expiry order went red (`credit-late`). Schema confirms `creditId` is optional to the backend ("When omitted, the backend selects the next available credit") and `idempotencyKey` required, so naming it is the tool's own discipline and it holds.

### 4. Idempotency key from `resetsAt`; `ResetAttempted` before the call. Witnessed in source, half-witnessed in test.

`state.mjs:38-45`: UUIDv5-shaped digest of `codex-quota-reset/window/<resetsAt>`. Test `:88-96` asserts the same key from a fresh state directory (derived, not random); mutation making it random went red (the rerun then consumed again instead of holding). Note that test's expected key comes from the previous run through the tested path, not from outside; a fixed literal key for `resetsAt` 1789840800 would be the stronger witness.

`codex-quota-reset:98` appends `ResetAttempted` before `:100` calls consume, and `state.mjs:47-48` counts `ResetAttempted` as spent. But no test exercises the path where the attempt is written and the consume does not complete: mutation `attemptedIgnored` (only `ResetConsumed` blocks) passed green; mutation `attemptedAfterCall` (write moved after the call) passed green. The fake's `consumeOutcome` parameter (`fake-app-server.mjs:45`) is never set by any test; no test sees `alreadyRedeemed`, `nothingToReset`, `noCredit`, an RPC error, or a hung consume.

### 5. No token or account id printed or logged. Witnessed, one soft edge.

`observe.mjs` returns only percentages, window kind, instants and credit rows (`:46-52`); `accountId` is never read. The fixture carries the sentinel `fixture-account-not-printed` and the test asserts it is absent from both the ndjson log and stdout (`tests:55-56`). No auth material reaches the client at all: the app-server holds it. Soft edge: the refuse path prints `appServer: ${error.message}` (`codex-quota-reset:106`) where `message` is the backend's JSON-RPC error object stringified verbatim (`app-server.mjs:82`); whatever the backend puts in an error lands in the journal. Not a token path today; worth trimming to the error code.

### 6. Nine fixture cases with real payload files, five mutations red. Partly witnessed.

Fixtures are files: five JSON payloads and two policy datoms under `tests/fixtures/`, read from disk by the fake per request (`fake-app-server.mjs:66`) and by the program through the absolute path in the datom. No inline payload strings. No test asserts source text: the test file reads only the ndjson log and the child's stdout (`grep readFileSync` in the test hits only `log.ndjson`). Count: eight test blocks, nine program runs (block two runs twice for the rerun), 10 `spawn`/`run(` sites counting the helper. "Nine" is fair as runs. Their "five mutations red" I cannot reproduce as theirs; of my eight, five red (noCreditId, latestExpiryFirst, noExperimentalApi, bindingWrongWindow, randomKey) and three green (attemptedIgnored, daysBoundaryLE, attemptedAfterCall). The clock is injected (`At.<unixSeconds>`, `NOW = 1789581600`), each run gets its own tmpdir socket and `XDG_STATE_HOME` (`tests:14-17`), tests share no state, and no test waits on the clock.

### 7. Nix check `codex-quota-reset-fixtures`. Wiring witnessed; the build is the reported one.

`flake.nix:118-123` `runCommand "primary-codex-quota-reset-fixtures"` with `pkgs.nodejs`, running `${self}/tools/codex-quota-reset/tests/codex-quota-reset.test.mjs`; exposed at `flake.nix:131`. Same file I ran green locally; fixtures ship in `${self}`. Not rebuilt here (nix build is not offline-cheap in this sandbox); the green reported from Prometheus is taken as ground.

## The living's rule: at least two days, never one

`codex-quota-reset:88-89`: `daysLeft = (resetsAt - now) / 86400; if (daysLeft < minimumDaysLeft) hold('windowEndsSooner')`, with `2` in `policy.useReset.datom`. At the test clock the fixtures sit at 3 days (spend), 1 day (hold, `tests:98-108`), 4 and 10 days (above threshold anyway). So "never for one day" is witnessed; exactly 2.0 days spends and 1.999 holds, which reads as at least two, but no fixture sits at the boundary and the README says "more than". Because the primary window is a 5-hour window, whenever it is the binding one `daysLeft` is under a day and the tool holds; only a binding weekly window can ever be reset. That matches the living's week framing but means a primary-window exhaustion never triggers a reset, whatever the policy says. Worth saying in the README.

## Crash-window trace

Setting: policy `UseReset 15 2`, binding weekly window at 5 percent with 3 days left, one available credit.

Run one, up to the send:

1. `:68` read; `:74-82` `QuotaObserved` printed and logged.
2. `:84-94` all gates pass; `soonestCredit` picks the credit.
3. `:96` key = digest(resetsAt). `:97` `alreadySpent` scans the log: false.
4. `:98` `appendFileSync` writes `{kind: ResetAttempted, creditId, idempotencyKey, resetsAt}`. Synchronous: the record is in the file before line 100 runs. Not fsynced, so a power loss can lose it; a process death cannot.
5. `:100` `call(...)` builds the frame and `socket.write`s it (`app-server.mjs:52-61`). The bytes may or may not have left the process when death arrives.

Death here (SIGKILL, OOM, node crash, or the 10 s RPC timeout at `app-server.mjs:55-58` which rejects, reaches `.catch` at `:105-106`, prints `ResetRefused.{ appServer: ... }`, logs `ResetRefused`, exits 2):

- stdout: `QuotaObserved` only (plus `ResetRefused` on the timeout path).
- log: `QuotaObserved`, `ResetAttempted` (plus `ResetRefused`).
- backend: one of two states, unknown to us: (a) the request never arrived, credit still `available`; (b) it arrived and was processed, credit `redeemed` (or transiently `redeeming`, a status the schema names), window reset.

Rerun (next timer tick):

- Case (b): `:68` reads ~100 percent remaining (and likely a new `resetsAt`); `:85` holds `aboveThreshold` before any key check. Correct outcome, by accident of the reading rather than by the key.
- Case (a): reading still 5 percent, 3 days, credit available; `:96` same key (same `resetsAt`); `:97` `alreadySpent` is true because `ResetAttempted` counts (`state.mjs:48`); `ResetHeld.{ alreadySpentThisWindow }`. No call is made. Every tick until `resetsAt` passes says the same. The credit is not spent for this window; the hold reason says it was.

So: no double spend in either case, which is the claim, and it holds. But the living's sentence was "we can call again and not double spend", and the tool cannot call again. The protocol was built for the call-again: same `idempotencyKey` is "one logical reset attempt", a completed one answers `alreadyRedeemed`, an unstarted one answers `reset`. The local `ResetAttempted` lock adds nothing the key does not already give, and subtracts the retry. In practice the timeout path is the likely one under a timer, not a process death, and it fires whenever the backend takes over ten seconds.

Also witnessed: neither the timeout nor the RPC-error path is under test; the fake always answers `reset` at once.

## What must change before the timer

1. Retry, do not lock. When the log holds a `ResetAttempted` for the key with no `ResetConsumed` after it, send the consume again with the same `creditId` and `idempotencyKey` and log the outcome; hold `alreadySpentThisWindow` only once a `ResetConsumed` exists for the key. Keep the pre-call `ResetAttempted` write (it is what makes the rerun know it is a retry). Log the outcome word: `alreadyRedeemed` on the retry is the backend confirming case (b).
2. Witness it. A fake mode whose consume never answers (or answers after the client timeout), a run that dies or times out, then a rerun against a fake answering `alreadyRedeemed` and one answering `reset`; assert exactly one consume before, one after, same key, and the log sequence. These kill mutations `attemptedIgnored` and `attemptedAfterCall`. Use the fake's existing `consumeOutcome` parameter for the other three outcome words too.
3. Boundary fixture at exactly two days (and one just under), and one README sentence choosing "at least" to match the code and the living.
4. Say in the README that only a binding weekly window can ever be reset under a two-day floor, so a primary-window exhaustion is never relieved by this tool.
5. Optional: trim `appServer:` refusals to the JSON-RPC error code; assert a literal expected key for one `resetsAt`.

Not blocking, for the secondary's unit: `Type=oneshot`, no `Restart=`, the same user that owns `~/.codex`, `XDG_STATE_HOME` set or the default `~/.local/state` writable; with change 1 in, a failed tick is completed by the next one, which is the README's own design.

## Sources

- `/tmp/f55ec8-reset` at c518a99f17496accebe1278c3b8352930a92f02b: `tools/codex-quota-reset/codex-quota-reset`, `app-server.mjs`, `observe.mjs`, `state.mjs`, `policy.mjs`, `datom.mjs`, `README.md`, `policy.datom`, `policy.useReset.datom`, `tests/codex-quota-reset.test.mjs`, `tests/fake-app-server.mjs`, `tests/fixtures/*`, `flake.nix:93-133`; `git show --stat HEAD`.
- Local run: `timeout 300 node tools/codex-quota-reset/tests/codex-quota-reset.test.mjs` green, exit 0.
- Mutation script `/tmp/f55ec8-audit-mut.sh` on a scratch copy `/tmp/f55ec8-audit/m`: eight mutations, five red, three green, as listed under claim 6.
- Protocol: `codex app-server generate-json-schema --out /tmp/f55ec8-audit/schema` (codex-cli 0.153.4, offline): `ConsumeAccountRateLimitResetCreditParams`, `ConsumeAccountRateLimitResetCreditOutcome`, `RateLimitResetCredit`, `RateLimitResetCreditStatus`, `RateLimitResetCreditsSummary`, `RateLimitWindow`, `InitializeCapabilities.experimentalApi`.
- `flows/f55ec8/vision/quota.md`, `flows/f55ec8/log.md` (2026-09-16 entries on the reset hook and the two-day floor), `flows/f55ec8/scripts/witness_requests.jsonl` (earlier read-only witness: `initialize`, `account/rateLimits/read` only; no consume was ever witnessed live).
- Node arithmetic on fixture instants against `NOW = 1789581600`: 3, 1, 4, 10, 3 days.
