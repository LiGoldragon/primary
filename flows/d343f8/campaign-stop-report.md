# Campaign stop and accounting evidence

Opus `0mib` withdrew every paid authority. The admitted batch was stopped immediately on receipt; no retry, restart or further call is authorized. Research revoked its admission in `1jb9`. The withdrawn system-state proof was never started.

## Execution and stop

- Single admitted controller used manifest `d2c41dee2708fda8179e62d20920ae23d9a347006b0433b4a89a45e32a75dbf3` and Research admission `06ae`, file SHA256 `4fe0d99bbee03fb8e7d65a9fe9574c49ce816d19ccc7e275161c83c4a7c31f7f`.
- On `0mib`, controller PID 3448351 was first SIGSTOPped to prevent another child launch. Its observed process tree PIDs 3448351, 3456368, 3456369, 3456775, 3456776 and 3456777 received SIGTERM; the stopped controller then received SIGCONT to deliver termination. No success exit was captured after the harness interrupted its waiting tool.
- The launch is terminal under its durable run/slot intent markers. No `done.json` is asserted and no completed measurement was manufactured for the interrupted slot.

## Read-only observed totals

- Attempt intent markers: 18. Completed measurement receipts: 17. Unresolved intent markers: 1.
- Completed response stops: {'end_turn': 17}.
- Completed typed outcomes: {'Answered': 10, 'TaskRefusal': 2, 'Malformed': 5}.
- Completed raw usage estimate: 0.1280440 USD. Completed conservative retained total: 0.135294000 USD.
- Interrupted default Opus full reservation bound: 0.10048 USD, retained pending Research reconciliation. These are observations and bounds, not an invoice or credit-balance proof. No insufficient-credit refusal was observed among completed receipts.

## Evidence paths

- Result root: `flows/d343f8/campaign/results/b8b816ee-56d4-5b14-91d3-aa26db1f49cb`.
- Each completed slot has started.json, observation.json and measurement.json. Raw worker receipts remain under the Research-owned artifact directory named by its observation.
- Unresolved slot intent: `flows/d343f8/campaign/results/b8b816ee-56d4-5b14-91d3-aa26db1f49cb/historical_variance__belief-balanced-03__claude-opus-5-5__r2/started.json`.

| Slot | Worker job | Receipt directory |
| --- | --- | --- |
| historical_variance__belief-04__claude-haiku-5-5__r1 | raw-general-082e0f-08caa08fa6f042a99b827ed2901bf8a5 | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-08caa08fa6f042a99b827ed2901bf8a5` |
| historical_variance__belief-04__claude-haiku-5-5__r2 | raw-general-082e0f-09eda851501747cd86efd57a6ea73ba4 | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-09eda851501747cd86efd57a6ea73ba4` |
| historical_variance__belief-04__claude-opus-5-5__r1 | raw-general-082e0f-3de56f7dcf5548cc84ba465ddd473f3d | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-3de56f7dcf5548cc84ba465ddd473f3d` |
| historical_variance__belief-04__claude-opus-5-5__r2 | raw-general-082e0f-1cdf49bcf8b044a9a768539abcf62265 | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-1cdf49bcf8b044a9a768539abcf62265` |
| historical_variance__belief-04__claude-sonnet-5-5__r1 | raw-general-082e0f-74587ff594014d89a6c3aced5f2b2133 | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-74587ff594014d89a6c3aced5f2b2133` |
| historical_variance__belief-04__claude-sonnet-5-5__r2 | raw-general-082e0f-048ab4fcf6c84831a9ecf45013a76dcc | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-048ab4fcf6c84831a9ecf45013a76dcc` |
| historical_variance__belief-balanced-02__claude-haiku-5-5__r1 | raw-general-082e0f-688e29bc69084e97855b620cdc2adeea | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-688e29bc69084e97855b620cdc2adeea` |
| historical_variance__belief-balanced-02__claude-haiku-5-5__r2 | raw-general-082e0f-131f8e5b315f43438688b7020a757562 | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-131f8e5b315f43438688b7020a757562` |
| historical_variance__belief-balanced-02__claude-opus-5-5__r1 | raw-general-082e0f-27de86b0ce794d18b8204f08b9821d0a | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-27de86b0ce794d18b8204f08b9821d0a` |
| historical_variance__belief-balanced-02__claude-opus-5-5__r2 | raw-general-082e0f-f246202c7a83494283459d371674c23a | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-f246202c7a83494283459d371674c23a` |
| historical_variance__belief-balanced-02__claude-sonnet-5-5__r1 | raw-general-082e0f-1ef2380ca4b34504a913a1a7d82dcb40 | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-1ef2380ca4b34504a913a1a7d82dcb40` |
| historical_variance__belief-balanced-02__claude-sonnet-5-5__r2 | raw-general-082e0f-dafe7ba871024e0a8b20e1ce483f563f | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-dafe7ba871024e0a8b20e1ce483f563f` |
| historical_variance__belief-balanced-03__claude-haiku-5-5__r1 | raw-general-082e0f-1ef92fb6e1d340acbd0225b767d5905d | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-1ef92fb6e1d340acbd0225b767d5905d` |
| historical_variance__belief-balanced-03__claude-haiku-5-5__r2 | raw-general-082e0f-e9364cdfec5548d8b958a8a3eede468a | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-e9364cdfec5548d8b958a8a3eede468a` |
| historical_variance__belief-balanced-03__claude-opus-5-5__r1 | raw-general-082e0f-1fac7e3240af414f937343a985cbd07b | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-1fac7e3240af414f937343a985cbd07b` |
| historical_variance__belief-balanced-03__claude-sonnet-5-5__r1 | raw-general-082e0f-25df2d8f841b47059000bc79fb22fcd8 | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-25df2d8f841b47059000bc79fb22fcd8` |
| historical_variance__belief-balanced-03__claude-sonnet-5-5__r2 | raw-general-082e0f-d0b9d51c8bc5494991b61f09a7f84871 | `/home/li/primary/flows/082e0f/claude-api-evidence/paid-jobs/raw-general-082e0f-d0b9d51c8bc5494991b61f09a7f84871` |

## Research reconciliation

Research `7ryj`, committed `40872cc56`, independently matched 18 new reservations
and admissions to 17 completed outcomes and settlements. Its read-only report
is `flows/85ab00/december-reconciliation.json`. Ledger snapshot: 905 rows,
225 settlements, SHA256 `6cc51f075e689c1ca39c7d76ab125bdec2a75080f3c438ef426fac1634a762bc`;
committed 8.347376355 USD and unreserved 28.652623645 USD under its mechanical gate.

Campaign retained commitment is 0.235774 USD: 0.135294 USD settled plus the
interrupted 0.10048 USD full bound. The unresolved worker job is
`raw-general-082e0f-7cf58712648f41b7ac90f898414f5d8f`; its exact provider completion
and charge remain unknown. Research observed no matching live launcher and
performed no ledger mutation, settlement or release. It revoked the admission
JSON after the launch; the admission hash above is the pre-revocation evidence.

## Remaining responsibility

Research reconciles the mutable ledger read-only and keeps the full interrupted reservation unless existing verified evidence establishes otherwise. No helper, provider request, settlement or release is authorized for reconciliation. This report does not modify the authoritative ledger.

The final Claude-from-code knowledge proposal retains only the original 180-job trial findings. The 17 completed observations above are excluded from its tables. No authored belief or live queue was changed.
