# Energy on its Ethos, step two, joined with schedule-pace

Written as the work goes; each section is filled when its step is committed and gated.
Branches `ethos-565bc8` in signal-energy-nexus, meta-signal-energy-nexus and energy-nexus. Nothing live touched; no main moved.
Generator: ethos-zero 28.0.0 (970459d).

## Starting point

- signal-energy-nexus 5c1ff2f (0.6.0: Redeemed answers Redeem, Refused named), gate green (gate-energy2-signal-energy-nexus-5c1ff2f.log).
- meta-signal-energy-nexus fa3e3de (0.6.0), gate green (gate-energy2-meta-signal-energy-nexus-fa3e3de.log).
- energy-nexus 0b9e6b4 plus the interrupted agent's uncommitted edits: repin to 5c1ff2f/fa3e3de, `Refused_Data` to `Refused`, and the public socket answered through the generated `Answering` dispatch (`Public`); the daemon's own hand trait renamed `Acting`.

## Steps

### A. Operation generated, dispatch, stale library removed (energy-nexus 08fcb7f)

- Kept the interrupted agent's diff whole: it was sound (repin to 5c1ff2f/fa3e3de; `Refused`; the public socket answered by `call.input.answer(&Public { … })`, the contract's generated `Answerable`/`Answering`; the daemon's own hand trait renamed `Acting`).
- `ethos/operation.ethos` follows the running code (Q6): `Levelled.LevelChange`, `Failed.Refused` imported from signal_energy_nexus; `LevelChange.{ Old.Option<Level> Latest }` declared in its types section. Generated into `crates/core/src/generated/operation.rs` (core, because core's `remember` returns `LevelChange`); `crates/core/build.rs` regenerates and refuses a differing committed file. Hand `Operation`/`OperationOutcome` gone; `Operation::Reminding` carries `Reminding_Data { reminder, reading }`.
- `ethos/library.ethos` removed (Q3). The core's dev-dependency on ethos-zero 5a5daca moved to 970459d (cargo refuses one crate from two sources across build targets).
- Gate: exit 0, 73 tests, `nexus-dependency-boundary` green. Log gate-energy2-energy-nexus-08fcb7f.log.

### B. Memory generated; store proven (energy-nexus 5b519a9)

- `ethos/memory.ethos` declares the stored root `Memory.{ Vector<Latest> History Configuration }` (Q7); generated into `crates/core/src/generated/memory.rs`. Hand `Memory`, `Latest`, `Configuration` gone. `impl Default for Configuration`, `impl Default for Memory`, and the rules as `impl Validating for Configuration` (a core trait) on the generated types. `Answer` dropped from the Ethos: nothing used it.
- Hand-written still: the envelope and admission machinery (wire `memory.rs`), the frozen `unversioned` and `version1` layouts and their `From` upgrades.
- Proofs:
  - both ways: `crates/core/tests/memory_hand_and_generated.rs` freezes the 0b9e6b4 hand `Memory`/`Latest`/`Configuration` verbatim; a Memory with every field and variant set, and the default, archive to identical bytes through both, and each reads the other's bytes back equal.
  - e5722529 fixture: `memory_admission` still upgrades `fixtures/energy-e5722529.rkyv` and the four Layer archives, unchanged.
  - live copies (`crates/core/tests/live_store.rs`, ignored, run on the builder by a scratch flake against copies):
    - ouranos `~/.local/state/nexus/main/energy.rkyv` (daemon unit `ExecStart … main %t/nexus/main %S/nexus/main`), copied 2026-11-14 09:12, 600594 bytes, sha256 `58a9a369bb54b26d5afc17f5604ebe640fa028e25ba138e257b7219033dc1045`, envelope ENXMEMRY version 2: admitted as it is; 2 latest, 4642 readings (7252 windows), 3 thresholds, 0 reminders, 2 targets, 0 window targets; written back byte-identical.
    - zeus: no Energy store exists. Energy is not installed there (no energy units, no `energy-nexus` on PATH, `~/.local/state/nexus/main/` empty, no `energy*.rkyv` on its root filesystem). Nothing to copy.
- Gate: exit 0, 74 passed, 1 ignored (live_store), boundary green. Log gate-energy2-energy-nexus-5b519a9.log.

### C. The translator's Memory and the CLI configuration Library (energy-nexus 365100b)

- Q9: `ethos/programs.ethos`, a second Memory root, the translator's own: `Programs.{ CodexProgram.Option<String> FlowProgram.Option<String> ClaudeCredentials.Option<String> }` (field names `codex_program`, `flow_program`, `claude_credentials`; the code forced naming each position, plainest reading taken: what each holds). `impl Default for Programs` by hand. `energy-translator.rkyv` stays ENXTRNSL version 1.
- Q10: `ethos/cli.ethos`, a Library in energy-nexus: `CliConfiguration.{ PlaceName.String }`, `ConfigurationRefusal.[ Unlocated.String Missing.String Unreadable.RefusedFile Invalid.RefusedFile ]`, `RefusedFile.{ ConfigurationPath.String Reason.String }` (the two in-place `{ path reason }` payloads are one shape, so declared once and named). Its `Display` stays a trait impl in `cli.rs`.
- Both generated into `crates/translator/src/generated/`, checked by `crates/translator/build.rs`; translator gains a `datom` feature, default on.
- Proofs: `crates/translator/tests/hand_and_generated.rs` freezes the hand `Programs`, `CliConfiguration`, `ConfigurationRefusal`: Programs archives identical both ways; the configuration and every refusal print the same datom text, and `{ main }` reads. The e5722529 translator fixture (`tests/place.rs`) still opens. Live copy: ouranos `~/.local/state/nexus/main/energy-translator.rkyv`, 142 bytes, sha256 `7c2385a728f547c4e0d6cf966021b9eb9c89c70b91269abe84a2c2ba91fd5864`, version 1: admitted as it is, all three paths set, written back byte-identical. zeus: none (Energy not installed).
- Gate: exit 0, 76 passed, 2 ignored. Log gate-energy2-energy-nexus-365100b.log.

### D. The reminder typed (energy-nexus 96e5935)

- Q11: `send_reminder` builds `signal_flow::Input::Send(SendRequest { address: recipient.0, sendable_message: Soft(Notice("Energy <provider> is <level>.")) })` and passes `datomize().protosize().compact()`. `compact` (protos `Compactable`) keeps it on one line; `textualize` would print vertically. The fixture test now asserts the exact line, unchanged: `Send.{ { Mind energyNexus Sol } Soft.Notice.«Energy Codex is Low.» }`, and that it reads back as a signal-flow 63 Input.
- The notice sentence itself is still a `format!` in code (a message literal); left as is.
- Flake seen once on the builder: `flow_reminder_fixture_records_one_soft_notice` returned false from spawning its freshly written fixture script (the same tree passed on rerun, 76 green). Most likely ETXTBSY from a concurrent fork in the test process; the test is main's, unchanged in shape.
- Gate: exit 0, 76 passed. Log gate-energy2-energy-nexus-96e5935.log.

### E. Emission (energy-nexus ab5a520), Q8 plainest pending Fable

- `ethos/emission.ethos` is now an Emission root: emissions `CodexRateLimits CodexConsumeReset ClaudeUsage Send`, outcomes paired by position, one each: `CodexRateLimitsObserved.Observation`, `CodexResetConsumed.Consumption`, `ClaudeUsageObserved.Observation`, `ReminderSent.Delivery`; `Observation.[ Observed.Reading Down ]`, `Consumption.[ Reset NothingToReset NoCredit AlreadyRedeemed Down ]`, `Delivery.[ Sent Down ]`. The two reads share the outcome payload type `Observation` but each has its own outcome variant.
- **Emission carrying nothing:** ethos-zero 28 accepts a bare emission but binds `Emittable` only to an emission that carries a type ("an emission carrying nothing has no type to bear the trait and binds nothing"). So `CodexRateLimits.{}` and `ClaudeUsage.{}` are declared as empty records, which it generates as `pub struct CodexRateLimits {}` and binds (`impl Emitted for CodexRateLimits { type Outcome = Observation; }`). This is the form used; say so to Fable.
- `ethos/emission_signal.ethos` is the Signal over `energy-emission.sock`, importing `crate:[ Emission Outcome ]`: inputs `Emit.Emission`, `TurnEnds`; outputs `Emitted.Outcome`, `TurnEndsObserved.Vector<TurnEnd>`, then `TurnEnded.TurnEnd` and `Down` answering no input. `TurnEnd.{ Provider At }`, `At` the library's. TurnEnds stays a Signal subscription; the translator matches `Input::TurnEnds` and hands the stream to its relay (the generated one-answer `Answering` does not fit a stream, so neither end uses it here).
- Both generated into `crates/emission/src/generated/`, checked by `crates/emission/build.rs`; the hand `wire!` types, `Query`/`Response`, and the hand `Emittable` gone. The core's parse-only `ethos_declarations_check` and its ethos-zero dev-dependency are gone: every ethos file in the repository is generated at build now.
- Internal wire: the tags on `energy-emission.sock` moved. Both ends are in the one package.
- Check (path flake): 75 passed (one fewer: the parse-only test removed).
- Gate: exit 0, 75 passed, 2 ignored. Log gate-energy2-energy-nexus-ab5a520.log.

### F. schedule-pace carried onto the generated contracts

The original `schedule-pace` branches are untouched (signal-energy-nexus d7d9f8d, meta dd6ec2b, energy-nexus 8e91223); the joined line is on `ethos-565bc8`, its new shapes inside the unreleased 0.6.0.

**F1. signal-energy-nexus 8c861ec** (gate exit 0, log gate-energy2-signal-energy-nexus-8c861ec.log).
- Library gains `Hours`, `Hour`, `Weekday`, `Usefulness.Percent`, `Baseline.Percent`, `Span.{ Vector<Weekday> From.Hour To.Hour Usefulness }`, `Override.{ Since.Instant Until.Instant Usefulness }` (ruling 2), `TimeZone.String` (ruling 3). `Pace` drops `PerDay` and gains `HoursLeft.Hours UsefulLeft.FiniteDecimal PerUsefulHour.FiniteDecimal`; still per window with `Name` (ruling 6). `Target.[ Even SpendBy.{ Instant Percent } ]` (the tentative addition; Rust `SpendBy_Data { instant, percent }`, datom `SpendBy.{ 1762450320 80 }`).
- **Forced, not listed: `FiniteDecimal` stays hand-written** (`src/decimal.rs`, the schedule-pace branch's `Decimal` renamed), imported by the Library with `:crate:decimal:[ FiniteDecimal ]`. Ethos's intrinsic `Decimal` generates `datom_codec::Decimal`, which puts datom-codec and protos into the daemon, and energy-nexus's `nexus-dependency-boundary` check refuses exactly that. An import may not reuse the intrinsic's name, hence `FiniteDecimal`. Text `83.5`, `0.78`, `32.0` as before.
- Generated `Span.from` is a newtype named `From` (and `to: To`): it shadows `std::convert::From` wherever `signal_energy_nexus::*` is glob-imported. Kept, since the vision names them so; consumers import by name.
- Fixtures rewritten; only `Target.*`, `Pace`, `Read_Data`, `Response.Read` and the contract identity moved, plus a line per new type. Digest now `-8897529803879169300` (the `Read` line's comment says useful hours). `hand_and_generated` no longer proves Target/Pace against 0.5.0.

**F2. meta-signal-energy-nexus 24958c7** (on signal-energy-nexus 8c861ec).
- `Set` gains `Span`, `RemoveSpan.Span`, `Override`, `RemoveOverride.Override`, `Baseline`, `TimeZone`. Datom: `Configure.TimeZone.America/Mexico_City` reads as a bare atom.
- Every `Set` archive grows to `Span`'s size; every line holding a Set or a Target rewritten; digest `-7872982838352770340`. `hand_and_generated` keeps only Caller, Program, Program_Data, Path.
- Gate: exit 0, logs gate-energy2-meta-signal-energy-nexus-24958c7.log (2+2+1 tests).

**F3. energy-nexus 04f6dab** (gate exit 0, 95 passed, 2 ignored; log gate-energy2-energy-nexus-04f6dab.log).
- `usefulness.rs` carried (override, then the most specific span, then the baseline; percent-seconds), on the generated `From`/`To`/`Since`/`Until` newtypes and `FiniteDecimal`.
- Memory format version 3: `ethos/memory.ethos` adds `Schedule.Vector<Span> Vector<Override> Baseline Option<TimeZone>` to the generated Configuration. Version 2 is now a frozen hand layout (`version2`), with frozen `earlier::{Target, ProviderTarget, WindowTarget}` (SpendBy of an instant alone) shared by `unversioned`, `version1`, `version2`; version 1 and the unenveloped archive go through `version2`. An earlier `SpendBy(i)` becomes `SpendBy.{ i 100 }`. Defaults: schedule empty, baseline 100, zone none.
- Ruling 3: `Configure.TimeZone`; `OwnerZone::owner_zone` is the configured zone or `TimeZone::system()`. **Forced choice:** jiff's `tzdb-bundle-always` (zone database bundled) instead of the branch's `tzdb-zoneinfo`, so a configured name resolves alike on every host and in the build sandbox, and "the name resolves" can be a rule every memory read keeps (`Validating for TimeZone`). If that rule were ever broken, `owner_zone` would read the system zone.
- Ruling 5: `Configuring::configure(set, now)`; after a Span, RemoveSpan, Override, RemoveOverride, Baseline or TimeZone setting, every override with `until <= now` is removed. The daemon passes the wall clock. An override configured already past is accepted, answered `Configured`, and removed by the same change (plainest reading; listed).
- Tentative addition built: `SpendBy.{ instant percent }`: expected = percent x (useful time spent / useful time to the instant); per useful hour = (percent - used) / useful hours left. Percent outside 0..=100 refused (Configure and every read).
- `memory_hand_and_generated.rs` (step B's proof of byte identity at version 2) removed: at version 3 the generated layout differs by design; the version 2 layout is held by the frozen `version2` and proven on the live copy below and by `format_version_two_is_carried_whole_into_an_empty_schedule`.
- Flake fixed: the translator's two fixture-program tests take one lock (ETXTBSY when one execs a script the other's fork holds open). It failed twice in eight runs before.
- **Live copy, upgraded:** ouranos `energy.rkyv` (sha256 `58a9a369bb54b26d5afc17f5604ebe640fa028e25ba138e257b7219033dc1045`, 600594 bytes, version 2): upgraded from format version 2, 0 uncarried; read independently through the frozen `version2` layout and `Memory::from(version2)` equal to the upgrade; 4642 readings, 2 latest, 3 thresholds, 2 targets (Even, Even), 0 window targets carried; schedule empty, baseline 100, zone the system's; written as version 3, 600643 bytes, read back equal. The translator copy (version 1) admitted and written back byte-identical. zeus: none.

### Worked examples recomputed (for Fable, ruling 1)

Computed by `crates/core/tests/useful_hours.rs::the_vision_worked_examples_recomputed` at 04f6dab, under the module's schedule (`Configure.Baseline.20`, every day 8 to 22 at 100), owner zone UTC-6 (America/Mexico_City). The readings stand; these are the corrected pace lines. The vision's Pace has no window name; the implementation's line carries `Week` (ruling 6), and the vision's `SpendBy.1762450320` is now `SpendBy.{ 1762450320 100 }`.

1. Unchanged, holds: `{ Codex Week Even 25 35 Over 124 83.5 0.78 }`.
2. Vision `{ Codex SpendBy.1762450320 88 92 Over 48 32.0 0.25 }` → corrected:
   `Read.{ { Codex True [ { Week 92 1762235580 10080 } ] [ { rc_1 Available 1762450320 } ] 1762210000 } [ { Codex Week SpendBy.{ 1762450320 100 } 71 92 Over 67 42.8 0.19 } ] }`
3. Vision `{ Codex Even 23 92 Over 120 80.0 0.1 }` → corrected:
   `Read.{ { Codex True [ { Week 92 1762235580 10080 } ] [ { rc_1 Available 1762450320 } ] 1762210000 } [ { Codex Week Even 95 92 Under 7 5.6 1.43 } ] }` (the week resets 1762235580, about seven hours after the reading, so Even expects 95%).
- The dentist override example still reads `useful_left 81.5`, `per_useful_hour 0.8`, expected 26.

### G. Release revision: energy-nexus 0.4.0 (4012ed4)

- All five crates 0.4.0; UPGRADES `## 0.4.0` (the step entries above it folded under it); contracts stay 0.6.0, unreleased, with their own UPGRADES entries.
- Gate by revision: exit 0 (log gate-energy2-energy-nexus-4012ed4.log). nix-fast-build found both checks already built (`builds: 0`): the identical tree was built and tested by the path check just before (95 passed, 2 ignored). Both outputs are present on the builder: test `qxi8wlf6…-cargo-package-test-0.0.1`, boundary `cz0lflmb…-energy-nexus-dependency-boundary-0.1.0`, whose daemon tree holds jiff, jiff-core, jiff-tzdb and no datom-codec or protos.

## Revisions and gates

| repository | branch ethos-565bc8 head | gate |
|---|---|---|
| signal-energy-nexus 0.6.0 | **8c861ec2b52be29f13c616c3501557bc38708d22** | exit 0, gate-energy2-signal-energy-nexus-8c861ec.log |
| meta-signal-energy-nexus 0.6.0 | **24958c7417d251525c7823c3c0ca91ff51401b9c** | exit 0, gate-energy2-meta-signal-energy-nexus-24958c7.log |
| energy-nexus 0.4.0 | **4012ed4282871846233a95423c118225659c7368** | exit 0, gate-energy2-energy-nexus-4012ed4.log |

energy-nexus steps: 08fcb7f (Operation), 5b519a9 (Memory), 365100b (translator Memory, CLI Library), 96e5935 (typed reminder), ab5a520 (Emission), 04f6dab (schedule-pace joined), 4012ed4 (0.4.0); each gated green, logs gate-energy2-energy-nexus-<short>.log. Untouched: every `main`; `schedule-pace` at energy-nexus 8e91223, signal-energy-nexus d7d9f8d, meta dd6ec2b.

## What remains hand-written, and why

- `FiniteDecimal` (signal-energy-nexus `src/decimal.rs`): the intrinsic `Decimal` would put datom-codec and protos into the daemon (see F1).
- The memory envelope and admission machinery (wire `memory.rs`: Envelope, Earlier, Admission, Upgrade, MemoryRefusal, Persisted): runtime machinery holding `PathBuf` and `io::Error`; no Ethos root names an envelope or a version.
- The frozen earlier layouts: `unversioned`, `version1`, `version2`, `earlier::{Target, ProviderTarget, WindowTarget}` and their `From` upgrades. ethos-zero 28 cannot generate an upgrade from an earlier layout.
- Trait impls on generated types: `Default` (Configuration, Memory, Programs), `Validating`, `OwnerZone`, `ScheduleChecking`, `SpanReading`, the `Display` of `ConfigurationRefusal`.
- `RedeemDecision` (core): a decision between the Memory's rule and the Operation, in no root; kept.
- `UsefulTime` and the pace arithmetic: behaviour, not records.
- Runtime actors, handles and errors, as Flow left its own: Nexus, Daemon, Public, schedule Event/WallClock/Track, Translator, Listening, AppServer, the relay types, SubscriptionFailure, GreetingWait, Place and the socket types.
- The notice sentence of the reminder ("Energy <provider> is <level>.") is a `format!` (the Send around it is typed).
- The Codex app-server JSON-RPC and the Claude usage JSON readings: the translator's provider words (left open, as Flow's Codex family is, for Fable).
- Each crate's `build.rs` is the same 30 lines, three times (core, translator, emission): one check per crate that holds generated Rust.

## For Fable

- Q8 as built: `CodexRateLimits.{}` and `ClaudeUsage.{}` are empty records so that ethos-zero 28 binds them to `Emittable` (a bare emission binds nothing). TurnEnds is the emission Signal's subscription; neither end uses its generated one-answer `Answering`.
- The intrinsic `Decimal` against the Nexus dependency boundary: today Energy imports a hand `FiniteDecimal`. A generated finite decimal without datom-codec would end it.
- Ruling 1: the corrected example lines above.
- Tentative `SpendBy.{ Instant Percent }` built as described in F3.
- An override configured with its Until already passed is accepted and removed by the same change.

## Clients of the contracts outside energy-nexus

- **CriomOS-home** (main 39c86609): flake input `energy-nexus` (`modules/home/profiles/min/energy-nexus.nix` installs `energy-nexus-daemon`, `energy-translator`, `energy-nexus`, `energy-nexus-meta`, `energy-pace` and writes `nexus/energy-nexus.datom`). No contract code and no scripted `Configure` lines. Relock `energy-nexus` to 4012ed4 in the release; the units are unchanged. Energy is enabled on ouranos only; zeus has none.
- **energy-nexus-tests** (branch `energy-stage-one-a9a8d6`): legacy fixtures and scenarios naming both contracts. Not a live client; nothing to relock for this release. It needs this work carried over if stage one lands.
- Nothing else: zoekt (`~/.local/share/zoekt/index`) finds `signal_energy_nexus`, `meta_signal_energy_nexus`, `SpendBy`, `Configure.Target` and `energy-pace` only in the three repositories, energy-nexus-tests, CriomOS-home (the module above), psyche-belief (the vision), primary (flow reports), and the crate catalogue of build-base (`crate-versions.json`, `crate-features.json`, names only).

## Release prep

Branches only; no main moved, nothing switched. Logs and files are in `/home/li/primary/flows/565bc8/` (`gate-energy3-*`, `release-energy/`).

### The fault fix (energy-claude-down.md "Fix")

energy-nexus **aafd0ebdfae570614b61f6b62c547739c2a8bedf** on `ethos-565bc8` (0.4.0, one commit on 4012ed4; the fix is folded into the unreleased 0.4.0 and its UPGRADES entry). The contracts are unchanged: the reading's own `At` is its age, so no age is declared in signal-energy-nexus 0.6.0.

- **Declared and generated.** `ethos/emission.ethos`: `Observation.[ Observed.Reading Down.Failure ]`, `Failure.{ Cause Status.Option<HttpStatus> RetryAfter.Option<Seconds> }`, `Cause.[ Unconfigured CredentialsUnreadable Unreached Refused AnswerUnreadable ]`, `HttpStatus.Integer`, `Seconds.Integer`. Generated by ethos-zero 28.0.0 into `crates/emission/src/generated/emission.rs`; its `build.rs` freshness check is the existing one. `Failure::of(cause)` and `retry_after_seconds()` are two small hand methods in the emission crate. The translator now asks `energy-nexus-emission` for its `datom` feature (to print the failure).
- **Translator.** Claude is read with `http_status_as_error` off, so a non-2xx answer keeps its status and `retry-after` (seconds or HTTP date). Every failed reading of either provider is one journal line, for example `energy-translator: Claude reading failed: { Refused Some.429 Some.30 }`. The endpoint is a parameter of `claude_reading` (the URL constant stays one place), so the reading is tested against a local HTTP server.
- **Daemon.** When the fresh reading fails, `Acting::read` answers `Read` with the reading held and its pace; the reading's `At` is its age, and the daemon logs the age. `ProviderDown` stays only when no reading is held for that provider. A failure that carried a `retry-after` withholds that provider (`withheld: HashMap<Provider, Instant>` on the Nexus): until it has passed the daemon does not call the translator, and answers from memory; a reading taken clears the wait; a failure without a `retry-after` withholds nothing; the wait is per provider.
- **Schedule.** The schedule takes only a reading newer than the one it knows. Without this a held reading, answered by a failed read after its window had reset, would set its past alarm again and loop reads.
- **Tests (108 passed, 2 ignored on the builder; 13 new).** Translator: refused with status and retry-after in seconds; retry-after as an HTTP date; refused with none; answered reading; answered with no JSON (status kept); no credentials, tokenless, and unreached; the one-line journal text. Daemon: failed reading answered with the held reading (not `ProviderDown`, nothing levelled); `ProviderDown` when none held; not read at 1001, 1030, 1059 and read at 1060 with a retry-after of 60 (call count on a fake translator socket); no retry-after is read again; Claude's wait does not hold back Codex. Schedule: a read answered with the held reading moves no alarm and starts no read.
- **Left as is, say to Fable:** after a failed read the window-reset alarm is spent and is not re-armed until a fresh reading, a turn end or a question reads (those are the events that read; the retry-after passing is not itself an event that reads). The Codex failure causes are coarse (`Unconfigured`, `Unreached` for any app-server failure, `AnswerUnreadable`).

### Relock on build-base 1d75864

Nothing to move. energy-nexus and its contracts carry no build-base pin (rust-build, Cargo.lock; UPGRADES 0.3.2 says so). Every git pin they hold is in build-base's set: ethos-zero 28.0.0 `970459d`, datom-codec `09a0526`, protos `c93b598`, signal 11.0.0 `6d4eb74`, signal-flow 61.0.0 `4871bb8` (contracts) and 63.0.0 `4982eeb` (energy-nexus). The contracts' 0.6.0 is not in build-base's set (it holds 0.5.0 `7ca10eb` and `3264d6f`); it enters when released.

### Heads and gates (by revision, on the builder, `nix-fast-build --skip-cached`)

| repository | head | gate |
|---|---|---|
| signal-energy-nexus 0.6.0 | `8c861ec2b52be29f13c616c3501557bc38708d22` | exit 0, `gate-energy3-signal-energy-nexus-8c861ec.log` (outputs already built) |
| meta-signal-energy-nexus 0.6.0 | `24958c7417d251525c7823c3c0ca91ff51401b9c` | exit 0, `gate-energy3-meta-signal-energy-nexus-24958c7.log` (outputs already built) |
| energy-nexus 0.4.0 | `aafd0ebdfae570614b61f6b62c547739c2a8bedf` | exit 0, `gate-energy3-energy-nexus-aafd0eb.log`: test 108 passed, 2 ignored, and `nexus-dependency-boundary` green |

### Store proof on a fresh copy, at aafd0eb

Copies of ouranos's live stores, taken with `cp` at 2026-11-14 09:53 (the live files were never opened), in a scratch flake that runs the ignored `live_store` tests of core and translator on the builder (`gate-energy3-store-proof-aafd0eb.log`); zeus has no Energy store.

| file | bytes | sha256 of the copy | result |
|---|---|---|---|
| `energy.rkyv` | 611391 | `3d9a5c10d39c178ba2a29c96efe366f16ba75b1aec82f3b5c8a516d9ca3f020b` | format version 2 upgraded to 3, 0 uncarried, 2 latest, 4694 readings (7319 windows), 3 thresholds, 0 reminders, 2 targets, 0 window targets carried; written as version 3, 611440 bytes, read back equal; the version 2 layout read independently and carried whole |
| `energy-translator.rkyv` | 142 | `7c2385a728f547c4e0d6cf966021b9eb9c89c70b91269abe84a2c2ba91fd5864` | version 1 admitted as it is, three paths set, written back byte-identical (same digest as the 09:12 copy) |

### CriomOS-home

Branch `energy-565bc8` of CriomOS-home, **018691de31637646fa007b1798bd7ac98f4510e7**, pushed, from main 39c86609 (still main at 09:5x). One change: `flake.lock`, the `energy-nexus` node from `26239478` to `aafd0eb` (3 lines; `flake.nix` and the module untouched). Worktree `/git/worktrees/CriomOS-home-energy-565bc8`.

- Built on the builder with ouranos's live inputs (`release-energy/scripts/home-build-host.sh`, CriomOS main 949c4508): baseline Home 39c86609 gives `rpvdvc5sx49w4nmsy0n2fa7yghk4k5wp`, the live generation (`readlink ~/.local/state/nix/profiles/home-manager`). The new Home gives **`czmfd0pmdr6zh9alw4wx26hv2y52ymaa-home-manager-generation`**.
- Closure against live (`release-energy/closure-paths.txt`, `closure-diff.txt`): the only differing paths are the Energy package (`cargo-package-0.0.1`, the energy-nexus build: diff-closures shows `cargo-package: +890.1 KiB`), `energy-nexus-clients`, `energy-nexus.service`, `energy-translator.service`, and the home-manager aggregates that name them (`home-manager-files`, `home-manager-path`, `hm_hmfontconfigfonts.xml`, `hm-putter.json`, the generation). Nothing else differs.
- Not pushed to main, not switched. The switch is Field core Sol's to clear first (fnlv). The daemon and translator ship together; the first start upgrades `energy.rkyv` from version 2 to 3 (proven above).
