# Spirit Topic Depth Query Implementation

System-operator report, 2026-06-01.

## Trigger

The psyche asked whether production Spirit could query several topics and return partial matches, then asked for a more ergonomic topic retrieval mechanism that emphasizes recency without making agents choose exact timestamps or counts. The follow-up instruction was to use a subagent to compare this operator lane's implementation plan with `reports/system-designer/56-spirit-verbal-depth-scopes-and-frequency-adaptive-search-2026-06-01.md`, take the best suggestions, implement, and report honestly on what exists.

Durable intent captured before implementation:

- Record 1315: Spirit should support intelligent topic retrieval that emphasizes recent intent by default while adapting historical depth to topic frequency.
- Record 1316: Spirit topic observation should support multi-topic partial and full matching.
- Record 1317: Spirit query ergonomics should support qualitative depth words instead of routine exact counts or absolute time windows.

## Subagent Comparison

Subagent `McClintock` compared the implementation against the system-designer report and found the right direction but several gaps:

- Keep the existing multi-topic `Partial` and `Full` topic selectors; they already satisfy the multi-topic shape.
- Add real `Shallow`, `Deep`, and `VeryDeep` verbal depth variants, not just `Recent`.
- Update `spirit.schema`, because otherwise the production contract documentation and generated shape drift from Rust.
- Update `persona-spirit/Cargo.lock`, because a stale lock would keep the daemon pinned to the older signal contract even if `signal-persona-spirit` was pushed.
- Return qualitative-depth results newest-first; old-to-new makes "recent" ergonomically wrong.
- Defer weighted / Nexus-based scoring and adaptive frequency statistics until there is a stronger substrate.

Those suggestions were incorporated.

## What Was Already Implemented Before This Work

Production Spirit already had:

- Multi-topic `Partial` matching: returns records matching one or more requested topics.
- Multi-topic `Full` matching: returns records matching every requested topic.
- Composable record queries across topic, optional kind, certainty, recorded-time selection, and observation mode.
- Time filters `Any`, `Between`, `Since`, and `Until`.

So the "several topics" part was not newly built here; it was verified and documented.

## What Is Implemented Now

### Signal contract

Repository: `/git/github.com/LiGoldragon/signal-persona-spirit`

Pushed commit: `4c7b51ff` (`signal-persona-spirit: add verbal recency depths`)

Implemented:

- Added `RecordedTimeSelection` variants:
  - `Shallow`
  - `Deep`
  - `VeryDeep`
- Kept existing `Recent`.
- Updated `spirit.schema` so the contract surface names all qualitative depths.
- Added canonical NOTA examples.
- Added round-trip tests for the new variants.
- Updated repo `ARCHITECTURE.md`, `INTENT.md`, and `skills.md`.

### Daemon behavior

Repository: `/git/github.com/LiGoldragon/persona-spirit`

Pushed commit: `df09280a` (`persona-spirit: add verbal recency depth queries`)

Implemented qualitative depth limits:

- `Shallow` returns up to 5 matching records.
- `Recent` returns up to 15 matching records.
- `Deep` returns up to 30 matching records.
- `VeryDeep` returns up to 100 matching records.

The query algorithm is:

1. Scan records.
2. Apply the existing filters first: topic selection, kind, certainty, and exact time window.
3. For qualitative depth selections, sort the matching records newest-first by recorded time and identifier.
4. Truncate to the qualitative depth limit.

That produces a simple frequency-adaptive behavior:

- On high-churn topics, the fixed result budget stays near the current working edge because enough recent records match.
- On quiet topics, the same budget reaches farther into history because fewer records match.

This is not a statistical adaptive-depth engine. It is a practical first implementation of the desired behavior using a bounded newest-matching-record selection.

### Home profile deployment

Repository: `/git/github.com/LiGoldragon/CriomOS-home`

Pushed commits:

- `7c74a083` (`home: pin spirit verbal recency query build`)
- `abffa839` (`home: use canonical rust analyzer toolchain`)

The first commit pins the production `persona-spirit-v0-3-0` Home input to the new `persona-spirit` revision.

The second commit fixes a deployment-blocking Home profile collision discovered during activation: `packages.rust-toolchain` already contains `rust-analyzer`, but Codium and Emacs were adding standalone `pkgs.rust-analyzer` too. The fix points Codium at `${rustToolchain}/bin/rust-analyzer` and removes the duplicate standalone editor-package entries.

Activation:

- Deployed via `lojix-cli` using Prometheus as builder.
- Home activation completed successfully.
- `persona-spirit-daemon-v0.3.0.service` and `persona-spirit-daemon-next.service` were restarted by activation and are active.

### Skill documentation

Workspace file: `skills/spirit-cli.md`

Updated to document:

- `TopicSelection` `Any`, `Partial`, and `Full`.
- `RecordedTimeSelection` `Any`, `Between`, `Since`, `Until`, `Shallow`, `Recent`, `Deep`, `VeryDeep`.
- Examples for qualitative topic searches.

## Verification

`signal-persona-spirit`:

- `cargo fmt --check` passed.
- `CARGO_BUILD_JOBS=2 cargo test` passed.

`persona-spirit`:

- `cargo fmt --check` passed.
- `CARGO_BUILD_JOBS=2 cargo test` passed.

`CriomOS-home`:

- `nix fmt -- --check` passed for the edited Home files.
- First activation attempt failed on the Rust analyzer package collision described above.
- After the Home fix, activation succeeded through `lojix-cli`.

Live production queries verified after activation:

```sh
spirit "(Observe (Records ((Partial [spirit query]) None Any Shallow SummaryOnly)))"
spirit "(Observe (Records ((Partial [spirit query]) None Any Deep SummaryOnly)))"
spirit "(Observe (Records ((Full [spirit query]) None Any Recent SummaryOnly)))"
```

All parsed and returned records. The `Shallow` query returned the newest five matching records. The `Deep` query returned a larger newest-first set.

## Honest Non-Implemented Surface

The following are not implemented:

- No Nexus / logic-language weighted query planning.
- No semantic keyword expansion.
- No per-topic observed-frequency statistics.
- No dynamic depth calculation from database density beyond the practical fixed-budget behavior.
- No result scoring or ranking beyond newest-first after filter matching.
- No weighted "topic A matters more than topic B" selector.
- No qualitative depth selectors on `RecordIdentifiers`; exact identifier and identifier-range queries still use their existing shape.
- No natural-language query parser. Agents still write NOTA.

## Architecture Reading

This implementation is deliberately small and production-shaped:

- The signal contract names the qualitative depth explicitly.
- The daemon owns the retrieval semantics.
- The CLI remains a text adapter to the daemon and does not interpret the query.
- The database schema does not need migration; all filtering is over existing record fields.

The larger design from `reports/system-designer/56-spirit-verbal-depth-scopes-and-frequency-adaptive-search-2026-06-01.md` remains valid as the next design frontier, but the production line now has an immediately usable version.

The next useful improvement would be a `TopicDepth` or `AdaptiveDepth` query mode that uses actual topic-density observations to choose a target budget/window, then reports the chosen depth in the reply for transparency. That should wait until the query language and reply vocabulary can carry the explanation cleanly.
