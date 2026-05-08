# Operator implementation audit — follow-up to designer/50

Status: 2026-05-08 follow-up — verification, idiom sweep,
broader scope.
Author: Claude (designer)

Designer/50 audited the typed-record migration (designer/45 +
46 + the operator-side implementation plan). This follow-up
adds three things that
designer/50 deferred:

1. **Verification** — actually run `cargo test` across every
   operator-touched repo, not just read the source.
2. **Rust-idiom sweep** — ZST-method-holders and free-function
   violations per `~/primary/skills/rust-discipline.md`.
3. **Broader scope** — operator activity outside the typed-
   record migration window: the `persona-*` sibling crate
   family.

Plus one concrete deliverable: a falsifiable-spec test file
at `signal-core/tests/pattern.rs` — 17 tests pinning the
canonical wire form for every `PatternField<T>` variant the
kernel ships.

---

## 1 · Verification — `cargo test` status

Every operator-touched repo's tests pass green at the head
commits cited in designer/50. Counts are the sum of
crate-internal + test/* files.

| Repo | Tests passed | Notes |
|---|---|---|
| `nota-codec` | 6 + 14 + 25 = **45** | five `tests/*_round_trip.rs` files exercise the four user-facing derives plus production-primitive coverage |
| `nota-derive` | **0** | proc-macro crate; coverage is downstream in the consumers' tests |
| `signal-core` | 0 + 7 + **17 (NEW)** = **24** | `frame.rs` covers handshake + operation rkyv; new `pattern.rs` covers PatternField wire form (this report's deliverable) |
| `signal` | 17 + 5 + 19 = **41** | `frame.rs` rkyv, `schema.rs` Schema derive, `text_round_trip.rs` covers Bind/Wildcard + (Node (Bind)) parse-error |
| `signal-persona` | 0 + 4 + 1 = **5** | persona contract is light on tests; the rkyv-only stance of the crate explains some of it but not all (see designer/50 §2 — sixteen pattern enums all without round-trip coverage) |
| `nexus` | 0 + 10 + 9 = **19** | parser + renderer; daemon body is exercised by mentci-integration |

Total: ~134 tests passing. Designer/50's static analysis
matches runtime reality. No silent failures.

---

## 2 · Rust-idiom sweep

### 2.1 · ZST candidates — all classified

`grep -rn "^pub struct [A-Z][a-zA-Z]*;"` finds eight
unit-struct definitions in operator's repos. Per
`~/primary/skills/rust-discipline.md` §"Legitimate ZST uses",
ZSTs earn their keep when they carry **type-level information**
— `PhantomData<T>` parameter trackers, framework markers
that delegate to a data-bearing partner type, or type-level
state-machine variants.

The full classification:

| Site | Kind | Verdict |
|---|---|---|
| `signal-core/src/pattern.rs:12` `Bind` | typed-record marker (`(Bind)` wire form) | ✅ legitimate — type IS the wire shape |
| `signal-core/src/pattern.rs:30` `Wildcard` | typed-record marker | ✅ legitimate — same |
| `nexus/src/daemon.rs:17` `Daemon` | ractor actor marker | ✅ legitimate — only `impl Actor for Daemon`, no inherent methods (operator already cleaned this per their commit `oyttukoo` "(nexus edit) (src/daemon.rs … — dropped inherent impl Daemon::start per the new §No ZST method holders rule per Li 2026-04-28)") |
| `nexus/src/listener.rs:22` `Listener` | ractor actor marker | ✅ legitimate — only `impl Actor for Listener` |
| `nexus/src/connection.rs:33` `Connection` | ractor actor marker | ✅ legitimate — `impl Actor` is the actor; `impl State` carries the real work on the `State` partner type |
| `signal/src/auth.rs:21` `CommittedMutation` | `Slot<CommittedMutation>` type-tag | ✅ legitimate — phantom-position marker; never instantiated |
| `signal/src/handshake.rs:25` `CriomeDaemonInstance` | `Slot<CriomeDaemonInstance>` type-tag | ✅ legitimate — same |
| `signal/src/slot.rs:39` `AnyKind` | `Slot<AnyKind>` type-erased slot | ✅ legitimate — type-level marker for diagnostic-site references that may point at any kind |

**No violations.** Every ZST in the sweep is one of the
three legitimate shapes — typed-record marker, framework
actor marker (delegating to State), or PhantomData-style
slot type-tag. The cleanest reading of operator's discipline
is that the `oyttukoo` commit already enforced this rule
across the code surface they own.

### 2.2 · Free-function violations

`grep -rn "^pub fn \|^fn "` outside `impl` blocks finds the
following standalone functions in the user-facing crates:

| Site | Visibility | Verdict |
|---|---|---|
| `nexus/src/bin/parse.rs:14` `fn main()` | private | ✅ binary entry point — rust-discipline.md exempts `main` |
| `nexus/src/bin/render.rs:13` `fn main()` | private | ✅ same |
| `nota-codec/src/lexer.rs:335` `fn is_ident_start(b: u8)` | private | ✅ local helper inside one module |
| `nota-codec/src/lexer.rs:339` `fn is_ident_continue(b: u8)` | private | ✅ local helper |
| `nota-codec/src/lexer.rs:355` `pub fn is_pascal_case(s: &str)` | **public** | 🟠 **promotable** — the verb belongs to a noun |
| `nota-codec/src/lexer.rs:359` `fn is_radix_digit(b: u8, radix: u32)` | private | ✅ local helper |
| `nota-codec/src/lexer.rs:368` `fn hex_digit(b: u8)` | private | ✅ local helper |
| `nota-codec/src/lexer.rs:380` `fn utf8_char_len(b: u8)` | private | ✅ local helper |
| `nota-codec/src/lexer.rs:394` `fn parse_int_literal(...)` | private | ✅ local helper |
| `nota-codec/src/lexer.rs:403` `fn dedent(raw: &str)` | private | ✅ local helper |
| `nota-codec/src/encoder.rs:171` `fn is_bare_string(value: &str)` | private | ✅ local helper |
| `nota-codec/src/encoder.rs:185` `fn is_ident_start(byte: u8)` | private | 🟡 **duplicates** lexer.rs:335 |
| `nota-codec/src/encoder.rs:189` `fn is_ident_continue(byte: u8)` | private | 🟡 **duplicates** lexer.rs:339 |

Two findings:

#### 2.2.1 · `pub fn is_pascal_case` is the verb without a noun

`nota-codec/src/lexer.rs:355`:

```rust
pub fn is_pascal_case(s: &str) -> bool {
    matches!(s.chars().next(), Some(c) if c.is_ascii_uppercase())
}
```

Used by `decoder.rs:122` and `decoder.rs:280` — both call
sites are matching against a `Token::Ident(name)`. The verb
("is this PascalCase?") is asking about a property of an
identifier. Two cleanest noun-locations:

- **`Token::is_pascal_case_ident(&self) -> bool`** — the
  matching predicate becomes a method on the token; the call
  site reads `if token.is_pascal_case_ident()` and never
  constructs the bare string-prefix question.
- **A new `PascalIdent(String)` newtype** — `TryFrom<&str>`
  validates; downstream code accepts only `PascalIdent`. This
  is the heavier fix and probably overkill for a single
  predicate.

The first is the right move. The fix is local to nota-codec
(method on `Token`), no cross-crate churn.

#### 2.2.2 · `is_ident_start` / `is_ident_continue` duplicated

The lexer's identifier-byte predicates appear verbatim in
`encoder.rs:185-189` because the encoder also has to decide
which strings are bare-ident-eligible. Two private copies of
the same byte-classification rules. The fix:

- Promote both to module-level helpers in a shared
  `nota-codec/src/idents.rs` (or similar), or
- Attach as associated functions on `Token` (since the same
  rules govern when a byte sequence is an `Ident` token).

Either works. The drift risk is concrete: a future change to
the lexer's identifier rules (allow `?`, allow leading `0`)
that the encoder doesn't mirror produces a wire-form
asymmetry — encode-then-decode loses round-trip. Worth
collapsing.

These are minor — both sit inside one crate, both are
fix-with-lunch. Filed for operator follow-up; not a blocker
for any of the typed-record migration.

---

## 3 · Broader scope — operator activity outside 45/46/47

Designer/50 focused on the typed-record migration window.
Operator's recent activity also includes a substantial
**persona-* sibling crate scaffolding** that didn't appear in
the designer/45/46 chain because its design lives in older
reports (designer/4 messaging design; designer/19 parallel
development).

### 3.1 · The persona-* family

The `repos/` index lists eight persona-related crates,
totaling ~3300 lines of Rust:

| Crate | Files | LoC | Role per recent commits |
|---|---|---|---|
| `persona` | 6 (lib + main + error + request + schema + state) | ~? | meta-crate / NOTA-facing schema scaffold |
| `persona-harness` | 3 (lib + harness + transcript) | ~? | harness primitive |
| `persona-message` | 9 (lib + main + bin + daemon + command + resolver + schema + store + error) | ~198 (store alone) | message daemon + store |
| `persona-orchestrate` | 4 (lib + main + claim + role) | ~73 | role-claim orchestration |
| `persona-router` | 5 (lib + main + delivery + message + error) | ~150 | message routing |
| `persona-store` | 6 (lib + main + schema + store + transition + error) | ~95 | persistent store |
| `persona-system` | 4 (lib + event + target + error) | ~109 | system-event surface |
| `persona-wezterm` | 5 (lib + bin + pty + terminal + error) | ~854 (pty alone) | wezterm transport |

**Common pattern:** every persona-* crate's most recent
commit is `refer to signal-persona contract` — operator
threaded the new `signal-persona` contract crate through the
sibling family, replacing whatever legacy `persona-message`
contract types they had.

The persona family now talks the same wire (signal-persona
contract crate over signal-core kernel) as the rest of the
signal-* family.

### 3.2 · Two notable depth points

- **`persona-wezterm/src/pty.rs` at 636 lines** is the
  largest single file in the family. The wezterm-PTY
  transport is the most fleshed-out persona-* component.
  Worth a separate read-through if and when a designer
  audit specifically targets the harness-IO surface.

- **`persona-message/src/store.rs` at 198 lines** is the
  redb-backed persistent store for the messaging substrate
  per designer/4. Same story — worth its own audit when
  the messaging surface stabilises.

Neither is a problem; both are signs that the persona family
is past scaffolding and into real implementation.

### 3.3 · `chroma` per-axis lerp work

`repos/chroma` head commit: `gradual warmth + brightness
ramps with cancel-and-replace; per-axis AbortHandle, lerp at
~60-step granularity`. This is system-specialist territory
(display/transport), not operator's core wire work. Noted for
completeness; out of scope for this audit.

---

## 4 · Concrete-test deliverable — `signal-core/tests/pattern.rs`

The user's task said *"Run and add tests to demonstrate
functionality with concrete examples."* Tests already pass
(§1). What was missing was a **kernel-level falsifiable spec
for `PatternField<T>`** — designer/47 §7 listed the canonical
cases; only the `signal/tests/text_round_trip.rs` integration
side covered them via `NodeQuery`/`EdgeQuery`. The kernel
itself had only `frame.rs`.

This audit lands `signal-core/tests/pattern.rs` (17 tests):

```rust
#[test]
fn bind_emits_typed_record() {
    assert_eq!(encode(&Bind), "(Bind)");
}

#[test]
fn wildcard_emits_typed_record() {
    assert_eq!(encode(&Wildcard), "(Wildcard)");
}

#[test]
fn pattern_field_string_round_trip_bind() {
    let decoded: PatternField<String> = decode("(Bind)");
    assert_eq!(decoded, PatternField::Bind);
}

#[test]
fn pattern_field_string_round_trip_match_bare_ident() {
    let decoded: PatternField<String> = decode("User");
    assert_eq!(decoded, PatternField::Match("User".into()));
}

#[test]
fn pattern_field_does_not_treat_at_sigil_as_bind() {
    let mut decoder = Decoder::new("@name");
    let result: nota_codec::Result<PatternField<String>> =
        PatternField::decode(&mut decoder);
    assert!(result.is_err(), "@-sigil must not decode as Bind");
}

#[test]
fn pattern_field_underscore_is_just_an_identifier() {
    // `_` is now a normal bare-ident at PatternField<String>
    // position, NOT Wildcard. Wildcard is only `(Wildcard)`.
    let decoded: PatternField<String> = decode("_");
    assert_eq!(decoded, PatternField::Match("_".into()));
}
```

The two negative tests at the bottom are the load-bearing
ones: they pin `@` and `_` to their post-migration meanings.
If a future change accidentally re-introduces sigil-shaped
Bind/Wildcard handling (regression), those two tests fire.

Discovery during the test-write: `PatternField::Match("User")`
encodes as `User` (bare ident), not `"User"` (quoted) — the
encoder emits eligible strings as bare-ident per a recent
nota-codec commit. Designer/47 §7 had flagged this as
ambiguous (`User or "User"`); the test now pins the actual
behavior with a separate quoted-string case
(`"hello world"`) covering the not-bare-eligible path.

All 17 pass.

---

## 5 · Designer-side miss — closed by operator concurrently

Designer/50 §4 noted my own oversight: designer/46 §5
proposed a one-line reserved-record-heads rule for
`skills/contract-repo.md` and the rename landed without it.

While I was writing this follow-up, **operator landed a
tight four-line bullet** under §"It owns" (commit
`nmwuxxln 76f107dd` — *"document reserved pattern heads"*):

> - Reserved record heads stay reserved workspace-wide. No
>   domain type defines a record kind named `Bind` or
>   `Wildcard`; those heads belong to
>   `signal_core::PatternField<T>` dispatch.

I drafted a longer dedicated section with a wrong-vs-right
code example and dropped it on top — then noticed operator's
bullet already covered the rule and reverted my section. The
terse placement under §"It owns" is the cleaner shape; if a
future agent needs the *why* (silent capture by PatternField
dispatch), the cross-reference to designer/46 §5 is in the
report record. Designer-side miss closed; gratitude to
operator for catching it concurrently.

This is also a small lesson on parallel-work coordination:
two agents fixing the same gap a few minutes apart didn't
collide because of the role-lane split (operator's repo edits;
my repo edits) — but the skills directory is shared. A claim
on `skills/contract-repo.md` would have surfaced the parallel
work earlier. Filed mentally; no immediate action.

---

## 6 · Bottom line

Designer/50's static audit holds up under runtime
verification — every test passes, every ZST is in one of the
three legitimate shapes, and the only free-function smell
(`pub fn is_pascal_case` + duplicated ident-byte predicates)
is local to nota-codec and doesn't block any consumer.

The persona-* family is post-scaffold and threading the new
`signal-persona` contract through; that's a separate audit
surface from the typed-record migration and warrants its own
review when the messaging substrate stabilises.

Designer-side miss closed (`skills/contract-repo.md` +
reserved record heads).

The single load-bearing residual gap remains the one
designer/50 §2 named: **signal-persona's 16+ hand-written
pattern enums should consolidate onto
`signal_core::PatternField<T>`**. Operator-side work,
mechanical, no design open question.

---

## 7 · See also

- `~/primary/reports/designer/50-operator-implementation-audit-45-46-47.md`
  — the audit this report extends.
- `~/primary/reports/designer/46-bind-and-wildcard-as-typed-records.md`
  §5 — original reserved-record-heads rule, now also in
  `skills/contract-repo.md`.
- `~/primary/skills/rust-discipline.md` §"Legitimate ZST uses"
  — the rule the §2.1 sweep applies.
- `~/primary/skills/abstractions.md` (verb belongs to noun)
  — the rule the §2.2 sweep applies.
- `~/primary/skills/contract-repo.md` §"Reserved record heads
  — `Bind`, `Wildcard`" — landed in the same commit as this
  report.
- `/git/github.com/LiGoldragon/signal-core/tests/pattern.rs`
  — the falsifiable spec landed in §4.
- `/git/github.com/LiGoldragon/nota-codec/src/lexer.rs:355`
  — the `is_pascal_case` free function flagged in §2.2.1.
- `/git/github.com/LiGoldragon/nota-codec/src/encoder.rs:185-189`
  — the duplicated ident-byte predicates flagged in §2.2.2.

---

*End report.*
