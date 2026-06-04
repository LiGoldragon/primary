# 65/4 — The nota-codec entanglement: proper solution and ordered sequencing

The entanglement has one root and one correct fix, and they are the same move: chroma hand-rolled a NOTA parser (a 742-line byte-walking pre-lexer that rewrites bracket strings back into quoted strings, then reads the now-removed `Token::Str`), so when the bracket-only-strings discipline removed `Token::Str` from nota-codec at `f761421`, chroma froze below that rev behind a stale `Cargo.lock` pin. The fix is NOT a transitional nota-codec shim and NOT a version-pin juggle — it is forward-only migration of chroma's config parser onto the derive surface (`#[derive(NotaRecord)]` / `#[derive(NotaEnum)]`, decoded via `Decoder` + `T::decode`), deleting roughly 600 lines of bespoke parsing, after which chroma tracks `branch = "main"` for free. The ordered sequence is: (1) migrate chroma `config.rs` off the hand-rolled lexer and bump its nota-codec pin to current main (primary-n1ao); (2) THEN land the already-written sema-engine boundary fix (primary-y0ec), because adopting sema-engine is what pulls the schema chain — and thus current nota-codec — into chroma's graph in the first place. These are one migration done in two ordered steps, not two independent tasks. A correction worth stating up front: the prior reports and the brief say "NotaDecode derive," but the actual proc-macro derives are named `NotaRecord` and `NotaEnum` (they EMIT the `NotaDecode`/`NotaEncode` traits); citing them by their real names matters for the operator who has to write the code.

## 1. The right fix for the bespoke parser — derive surface, not a hand-rolled lexer

### What chroma does today (the forbidden shape, verified)

`src/config.rs` (742 lines, verified) parses `config.nota` through TWO hand-built layers, both forbidden by `skills/rust/parsers.md` and the bracket-only-strings discipline:

- **Layer 1 — a pre-lexer that un-does the discipline.** `config_text_with_bracket_strings_as_quoted` (`src/config.rs:119`) walks bytes by hand and rewrites every bracket string `[...]` / `[|...|]` BACK into a `"`-quoted string via `push_quoted_string` (`:255`), literally emitting the quotation marks the encoder structurally cannot emit.
- **Layer 2 — feeding the rewritten text through the codec lexer and reading the removed token.** `ConfigDocument::parse` (`:380`) drives `Lexer::new` / `lexer.next_token()` and matches the deleted variant at `src/config.rs:101`, `:402`, `:413` — `Token::Str(value)`. At nota-codec HEAD (`24e7823`) `Token` has no `Str`, so these three arms are hard compile errors. chroma compiles today ONLY because its lock pins `538555e`.

The entire file is also a free-function cascade (`config_text_with_bracket_strings_as_quoted`, `read_config_block_string`, `push_quoted_string`, `parse_theme_axis`, `parse_warmth_axis`, …), a third discipline violation (method-only). The intermediate `ConfigNode` enum (`:337`) is a hand-rolled re-implementation of exactly what `nota-codec`'s `Decoder` + value-shape layer already provides.

### The correct surface (verified against current nota-codec)

The intended parse surface is the derive + `Decoder`:

```rust
use nota_codec::{Decoder, NotaRecord, NotaEnum, NotaDecode};

#[derive(NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct Node {
    name: NotaName,
    edges: Vec<Edge>,
}

let mut decoder = Decoder::new(text);
let value = Node::decode(&mut decoder)?;
```

Verified facts about the surface chroma must adopt:

- The derives are `#[proc_macro_derive(NotaRecord)]` and `#[proc_macro_derive(NotaEnum)]` in `nota-derive/src/lib.rs:27,37`, re-exported through `nota-codec` (`nota-codec/Cargo.toml:12` depends on `nota-derive`). They EMIT `NotaEncode` + `NotaDecode`; "NotaDecode derive" in the earlier reports is the trait, not the macro name.
- `NotaRecord` encodes/decodes as a POSITIONAL record `(field0 field1 ...)` — "The struct type is determined by the schema position, not by a type tag in the wire text" (`nota-derive/src/lib.rs` doc comment, verified). Decoding requires every declared field position; omitted optionals are an error, not a compatibility shape.
- The decode entry point is `Decoder::new(text)` then `T::decode(&mut decoder)` (`nota-codec/src/traits.rs:22`, `NotaDecode::decode(decoder: &mut Decoder<'_>) -> Result<Self>`; round-trip pattern in `nota-codec/tests/nota_transparent_round_trip.rs:25-29`).
- Bracket strings decode natively. `NotaString`'s only kind is `Block` (bracket-form only) — there is no quote path to re-introduce. chroma's color atoms `[#000000]` and path atoms `[/bin/dconf]` (verified in `tests/config.rs` `NATIVE_CONFIG`) decode straight into `String` / a `NotaName`-style newtype, deleting the entire pre-lexer.

### The non-trivial nuance the worked example must respect — named heads are enums, not positional records

chroma's `config.nota` is NOT a flat positional record. The verified fixture (`tests/config.rs` `NATIVE_CONFIG`) is head-keyed:

```
(Config
  (Theme
    (Concerns Terminal Desktop Ghostty)
    (Palettes (Dark (Base00 [#000000]) ...) (Light ...))
    (Adapters (Dconf [/bin/dconf]) (Emacsclient [/bin/emacsclient]))
    (FontPointSize 14)
    (GhosttyConfigTemplates (Dark [/tmp/chroma-test/dark.ghostty]) (Light ...))
    (Schedule (Waypoint (CivilDawn (SignedMinutes 0)) Light) (Default Dark)))
  (Warmth (Schedule (Manual Neutral)))
  (Brightness (Schedule (Manual Bright))))
```

Each inner form has a NAMED head (`Theme`, `Concerns`, `FontPointSize`, `Waypoint`). `NotaRecord` is positional and carries no head tag, so a head-keyed shape models as a `NotaEnum` (the head is the variant discriminant) whose variant payload is a `NotaRecord`. This is the actual migration: walk chroma's config grammar and assign each construct to either `NotaRecord` (positional payload) or `NotaEnum` (head-tagged choice). It is more than a one-line `#[derive]` slap, but it is entirely declarative — every node maps to one of the five derives, no byte-walking, no quote IR, no `Token` matching.

### chroma config.rs migration — the worked example

The migration replaces the hand-rolled tree with derived types. Sketch (illustrative; exact field-by-field mapping is the operator's job):

```rust
// BEFORE: hand-rolled ConfigNode + free-function parse cascade (~600 lines)
//   config_text_with_bracket_strings_as_quoted -> push_quoted_string -> Lexer -> Token::Str
//   parse_theme_axis / parse_warmth_axis / parse_brightness_axis / parse_schedule / ...

// AFTER: declarative derives; head-tagged forms are NotaEnum, positional forms NotaRecord.

#[derive(NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct Config {            // (Config <theme> <warmth> <brightness>)
    theme: ThemeAxis,
    warmth: WarmthAxis,
    brightness: BrightnessAxis,
}

#[derive(NotaRecord, Debug, Clone, PartialEq, Eq)]
pub struct ThemeAxis {         // positional payload under the (Theme ...) head
    concerns: Concerns,
    palettes: ThemePalettes,
    adapters: ThemeAdapters,
    font_point_size: FontPointSize,
    ghostty_config_templates: Option<GhosttyConfigTemplates>,
    schedule: ThemeSchedule,
}

#[derive(NotaEnum, Debug, Clone, PartialEq, Eq)]
pub enum ThemeMode {           // bare-atom choice: Light / Dark
    Light,
    Dark,
}

#[derive(NotaEnum, Debug, Clone, PartialEq, Eq)]
pub enum ThemeSchedule {       // head-tagged: (Manual <mode>) | (Scheduled <waypoints...>)
    Manual(ThemeMode),
    Scheduled { waypoints: Vec<ThemeWaypoint>, default: ThemeMode },
}
```

`ConfigFile::theme_axis` collapses to:

```rust
pub fn theme_axis(&self) -> Result<ThemeAxis> {
    let text = std::fs::read_to_string(&self.path)?;
    let mut decoder = Decoder::new(&text);
    Ok(Config::decode(&mut decoder)?.theme)
}
```

What this deletes (verified line ranges in current `src/config.rs`): the import `use nota_codec::{Lexer, Token}` (`:17`), `config_text_with_bracket_strings_as_quoted` + helpers (`:119-268`), the `ConfigNode` enum + impls (`:337-373`), `ConfigDocument::parse`/`parse_node`/`parse_record` (`:380-428`), and every free-function `parse_*` axis builder (`:430-742`). That is the ~600-line deletion both prior reports cite, confirmed against the actual file. What remains: the derived type definitions (most of which mirror the existing structs in `theme.rs` / `warmth.rs` / `brightness.rs`, already present) plus thin `decode` entry points. Crucially, deleting `push_quoted_string` removes the only place in chroma that emits a `"` — the discipline is satisfied structurally, not by convention.

One real edge to watch: chroma's `reject_removed_or_non_nota_inputs` (`:96`) rejects removed theme-apply command records. With the derive, "removed record" handling becomes either an absent `NotaEnum` variant (decode errors naturally on an unknown head — verified: `nota-codec/tests/nota_mixed_enum_round_trip.rs` shows `(Mystery 42)` producing `Error::UnknownVariant`) or an explicit rejected-variant arm. The rejection semantics survive without a hand-rolled scanner.

## 2. Compat-shim vs pure migration — forward-only is the only discipline-correct path

A transitional nota-codec shim (re-adding a `Token::Str` behind a feature flag, or a `read_legacy_quote_string` compatibility build) is NOT warranted, for reasons that are structural, not stylistic:

- **Backward-compat is explicitly not a constraint here.** The bracket-only-strings discipline (`skills/nota-design.md` §"Strings come EXCLUSIVELY from bracket forms"; AGENTS.md hard override) states the encoder structurally cannot emit a quote and that legacy quoted input was migration-only with removal AUTHORISED once emitters migrate. `f761421` IS that authorised removal executed. Re-introducing a shim would un-authorise a decision the psyche already made and re-open the format ambiguity (is `"` content or delimiter?) the discipline exists to close. The embedding-safety property (NOTA embeds escape-free in any double-quote host) only holds if NO quote path exists anywhere.
- **A shim perpetuates the actual defect.** The entanglement is not a missing API — it is a hand-rolled parser frozen at an old contract. A shim keeps the hand-rolled parser alive and merely moves the freeze point forward; chroma would still be the only consumer reaching into `Lexer`/`Token` low-level primitives, still violating `skills/rust/parsers.md`, still the carrier of the next contract change's break. The shim treats the symptom (compile error) and protects the disease (bespoke parser).
- **The migration is bounded and the deletion is net-negative LOC.** ~600 lines deleted, replaced by declarative derives that mostly already exist as plain structs. There is no large surface to migrate incrementally; a shim's only value — buying time for a big migration — does not apply.
- **No deployment forces a slow path.** chroma is a single component (a config parser for a desktop theming daemon), not a wire contract with many deployed peers. There is no fleet of running chroma instances whose on-disk configs change format — the `config.nota` text is identical (it was already bracket-form; only chroma's INTERNAL pre-lexer manufactured quotes). The migration is invisible to users' config files.

The two-deploy-stacks discipline is the relevant containment model (report 65/3 §6): it says a straddling component must be PLACED decisively, not held by a stale pin. chroma's placement is "port to current" — it is the forward stack's neighborhood (it wants current sema-engine). Forward-only migration IS placing it. A shim is the opposite — it institutionalizes the straddle.

Verdict: pure forward migration. No shim.

## 3. The ordered sequence — n1ao before y0ec, and whether to sweep the cohort

### Why config-migration strictly precedes sema-engine adoption

The dependency edge that creates the collision is sema-engine adoption itself. chroma does not currently sit in a cargo graph with the schema chain; pulling sema-engine in (`sema-engine -> signal-sema -> signal-frame -> schema-rust -> schema -> nota-codec`) is what forces chroma's nota-codec to resolve to `branch = "main"` HEAD, which is exactly the rev `config.rs` cannot compile against. So the sema-engine boundary fix (primary-y0ec) STRUCTURALLY cannot land until `config.rs` is off `Token::Str` (primary-n1ao). The bead notes confirm this is already the lived sequence: the boundary fix was "written + verified to compile (state.rs/error.rs 0 errors) before clean revert per no-broken-code rule" and "chroma is sequenced behind n1ao."

### One unification event, not two

A subtlety from report 65/1 and 65/3, verified: sema-engine's OWN lock still pins old `538555e`, and the schema legs pin the bridge `d00fbf5`. So bumping chroma to current nota-codec, bumping sema-engine forward, and moving the schema legs past the bridge are a SINGLE unification onto HEAD `24e7823`, not three separate bumps. The schema chain is already HEAD-clean (it uses the shape layer and bracket forms; the quote removal is a no-op for it — verified in 65/1). The only code that cannot survive the unification is chroma's `config.rs`. Fix that one file and the whole graph unifies.

### The operator-actionable ordered plan

1. **n1ao step A — migrate chroma `config.rs` to the derive surface.** On a chroma feature branch (designer authors in `~/wt`, operator owns main per AGENTS.md): replace `ConfigNode` + the free-function parse cascade with `#[derive(NotaRecord)]` / `#[derive(NotaEnum)]` types per §1; delete the pre-lexer, `push_quoted_string`, and all `Token::Str` matches; route through `Decoder::new` + `Config::decode`. Keep the `config.nota` text fixtures unchanged (they are already bracket-form) — the existing `tests/config.rs` assertions are the regression guard that the migration preserves behavior. While in the file, fold the surviving logic into methods on owning types (`Config`, `ConfigFile`) per the method-only rule, retiring the free functions.
2. **n1ao step B — bump chroma's nota-codec pin to current main and unify.** With `config.rs` no longer touching `Token::Str`, run the lock bump to `24e7823`. chroma now tracks `branch = "main"` like every other family member; the stale pin is gone. Verify `cargo build` + `cargo test` green against current nota-codec.
3. **y0ec — land the sema-engine boundary fix.** Re-apply the already-written, already-compile-verified state.rs/error.rs change that adopts sema-engine and retires raw redb 2.x (`.redb -> .sema`). Because step B already unified nota-codec to HEAD, pulling sema-engine + the schema chain in now resolves cleanly — there is no second nota-codec collision to resolve. Verify green; operator integrates the branch into main.
4. **Close the loop.** Mark n1ao done when steps A+B are green; mark y0ec's chroma leg done when step 3 integrates. The `.sema` extension convention (Spirit 2564) lands with the boundary fix.

### Per-component, not a coordinated cohort sweep

The right granularity is per-component, sequenced, NOT a big-bang cohort sweep, because the cohort is heterogeneous in severity (verified across reports 65/1-65/3):

- **chroma is the unique STRONG-form instance** — the only repo that consumes the REMOVED `Token::Str` behind a stale pin, so it is the only one that breaks on a bump. It needs real source migration and must go first and alone.
- **The WEAK-form instances (nexus `src/parser.rs`, signal-core `src/request.rs`/`pattern.rs`) survive the bump** — they hand-roll Token dispatch but only on STRUCTURAL tokens (`LParen`, `LBracket`) that `f761421` did not remove. They are parser-discipline debt, not version blockers. They do NOT need to move to unblock chroma or sema-engine; bundling them into the chroma sequence would couple unrelated risk to a blocking task. Track them separately (signal-core is high-leverage as a foundational signal dependency, but it is not on the critical path).
- **The ~23 pure stale-pin repos need only a `cargo update`** — no source change. They are not on the critical path either; they bump opportunistically when each is next touched.

A coordinated sweep would be warranted only if multiple repos shared the strong-form break and had to land atomically in one graph. They do not: chroma is the single chokepoint. Forcing the weak-form and stale-pin repos through a synchronized sweep adds coordination cost and broadens the blast radius of any one failure, for zero unblocking benefit. Fix the chokepoint per-component; let the rest follow their own touch cadence. A standing mechanical check (grep every repo for direct use of `Lexer` / `Token` / `Decoder` / `Database::open` / `begin_write` — the low-level-primitive signature) is the right ongoing instrument, and is exactly the auditor-role work AGENTS.md flags as a candidate.

## 4. Relationship to primary-y0ec (sema-engine boundary) and primary-n1ao (chroma blocker)

Verified from the bead store: y0ec ("Peripheral sema-engine boundary strays") DISCOVERED n1ao ("Migrate chroma config.rs off removed nota-codec lexer, then adopt sema-engine"). The relationship, stated precisely:

- **n1ao is a hard prerequisite of y0ec's chroma leg.** y0ec cannot complete for chroma until n1ao is done, because adopting sema-engine is the exact action that pulls current nota-codec into chroma's graph and trips the `Token::Str` break. The bead OUTCOMES note records this: the boundary fix was "REVERTED (blocked): adopting sema-engine forces nota-codec forward and chroma's stale hand-rolled config.rs (old Token::Str lexer) breaks -> must migrate config.rs first."
- **They are the two faces of one identity (report 65/3 §5).** chroma is the same component failing the same way on two contracts: it hand-rolled raw redb (storage, y0ec axis — chroma is redb 2.6.3 vs sema-engine 4.1.0) AND hand-rolled a NOTA lexer (parse, n1ao axis). Both are "pinned to an old contract, hand-built what the contract now provides." The remediation shape is identical on both axes — delete the hand-rolled layer, adopt the typed surface (derive for parse, sema-engine for storage). n1ao removes the parse-axis hand-rolled layer; y0ec removes the storage-axis one. Done in order, they resolve chroma completely.
- **y0ec's OTHER legs are independent of n1ao.** orchestrator is LEGACY (retire, tracked as primary-mt02), not port. schema-next's redb store is an AsschemaStore lowering cache — owner decides adopt-vs-exempt. Neither depends on the nota-codec migration. n1ao is specifically and only the chroma chokepoint.

Net: the operator's path is n1ao (config migration + lock bump) → y0ec chroma leg (boundary fix re-apply + integrate), with y0ec's orchestrator/schema-next legs proceeding on their own tracks. The chroma blocker is fully sequenced; nothing else in the entanglement is on its critical path.

## See also

- `reports/system-designer/65-nota-codec-entanglement-meta-investigation-2026-06-04/1-version-delta-and-dependency-graph.md` — the rev lattice and why one source unifies to one rev.
- `reports/system-designer/65-nota-codec-entanglement-meta-investigation-2026-06-04/3-conceptual-root-and-related.md` — the conceptual root and the parse/storage twin identity.
- `reports/system-designer/63-sema-engine-boundary-conformance-audit-2026-06-04.md` — the storage-axis twin (y0ec).
- `skills/rust/parsers.md` — no-hand-rolled-parsers; the derive is the intended surface.
- `skills/nota-design.md` §"Strings come EXCLUSIVELY from bracket forms" — the discipline that removed `Token::Str`; the only legitimate hand-written-codec carve-out (symbol-shaped newtypes) is nowhere near chroma's byte-walking pre-lexer.
- `/git/github.com/LiGoldragon/chroma/src/config.rs` — the seed: `Token::Str` at `:101`/`:402`/`:413`, pre-lexer at `:119-268`.
- `/git/github.com/LiGoldragon/nota-derive/src/lib.rs:27,37` — the real derive names `NotaRecord` / `NotaEnum`.
- `/git/github.com/LiGoldragon/nota-codec/src/traits.rs:22` — `NotaDecode::decode(decoder: &mut Decoder<'_>)`, the decode entry point.
- Beads: `primary-n1ao` (chroma config migration blocker), `primary-y0ec` (sema-engine boundary strays).
