# 126 — `nota-config` crate scaffold (per designer/183)

Date: 2026-05-16
Role: operator-assistant
Scope: scaffold the `nota-config` library crate prescribed by
`reports/designer/183-typed-configuration-input-pattern.md` and
report the design deviation, the validation finding, and the
open question about the next slice.

## 0. What landed

- New repo: <https://github.com/LiGoldragon/nota-config>
  - License: License of Non-Authority (matches nota-codec).
  - `flake.nix`: crane + fenix minimal, matches `nota-codec`'s
    shape. `checks.default = cargoTest`.
  - `Cargo.toml`: edition 2024, rust-version 1.85, deps on
    `nota-codec` (git main), `rkyv` 0.8 (full canonical feature
    pin matching every other Persona-stack contract crate),
    `thiserror` 2. Dev-dep on `tempfile`.
  - Layout matches `ARCHITECTURE.md` §"Code map":
    - `src/lib.rs`, `src/error.rs`, `src/source.rs`,
      `src/configuration.rs`.
    - `tests/argv_detection.rs`, `tests/inline_nota.rs`,
      `tests/nota_file.rs`, `tests/rkyv_file.rs`,
      `tests/test_env_fallback.rs`.
- Local checkout: `/git/github.com/LiGoldragon/nota-config`.
- Initial commit on `main`: `d557fbf` — pushed and verified
  against the remote.
- Test count: **18 tests** through `nix flake check`, all green
  on `x86_64-linux`. Doc-tests on the two macros compile (marked
  `ignore` because the example types are illustrative).

## 1. The public surface (matches `designer/183` §3)

```rust
pub enum ConfigurationSource {
    InlineNota(String),
    NotaFile(PathBuf),
    RkyvFile(PathBuf),
}

impl ConfigurationSource {
    pub fn from_argv() -> Result<Self>;
    pub fn from_args<I, S>(args: I) -> Result<Self>
        where I: IntoIterator<Item = S>, S: AsRef<OsStr>;
    pub fn from_argv_nth(n: usize) -> Result<Self>;
    pub fn from_args_with_env_fallback<I, S>(args: I, env_value: Option<OsString>) -> Result<Self>
        where I: IntoIterator<Item = S>, S: AsRef<OsStr>;

    #[doc(hidden)]
    pub fn from_argv_with_test_env_fallback(env_var_name: &str) -> Result<Self>;

    pub fn decode<C: ConfigurationRecord>(self) -> Result<C>;
}

pub trait ConfigurationRecord: NotaDecode + Sized {
    fn from_rkyv_bytes(bytes: &[u8]) -> Result<Self>;
}

// Two macros — see §2 for why this deviates from /183 §3.1.
#[macro_export] macro_rules! impl_nota_only_configuration { … }
#[macro_export] macro_rules! impl_rkyv_configuration   { … }
```

Detection is extension-based per /183 §3.2:

1. First arg starts with `(` → `InlineNota`; concatenate all
   argv tokens with single spaces (shell may split a multi-word
   record).
2. First arg ends with `.nota` → `NotaFile`.
3. First arg ends with `.rkyv` → `RkyvFile`.
4. Anything else → `Error::UnknownExtension` or
   `Error::ExtensionRequired`.

## 2. Deviation: two macros, no blanket impl

`designer/183` §3.1 proposed:

```rust
pub trait ConfigurationRecord: NotaDecode + Sized {
    fn from_rkyv_bytes(bytes: &[u8]) -> Result<Self> {
        Err(Error::RkyvNotSupported(std::any::type_name::<Self>()))
    }
}

impl<T: NotaDecode> ConfigurationRecord for T { … }
```

…plus a per-type `impl_rkyv_configuration!(MessageDaemonConfiguration)`
macro that re-impls `ConfigurationRecord` for the specific type
to override `from_rkyv_bytes`.

**This won't compile.** Rust forbids overlapping impls: the
blanket already covers any `T: NotaDecode`, and the per-type
macro produces a second impl for the same type. Resolving the
overlap properly requires unstable `specialization`.

**What landed instead — two explicit macros, no blanket:**

```rust
pub trait ConfigurationRecord: NotaDecode + Sized {
    fn from_rkyv_bytes(bytes: &[u8]) -> Result<Self>;
}

#[macro_export]
macro_rules! impl_nota_only_configuration {
    ($t:ty) => {
        impl $crate::ConfigurationRecord for $t {
            fn from_rkyv_bytes(_bytes: &[u8]) -> $crate::Result<Self> {
                Err($crate::Error::RkyvNotSupported(std::any::type_name::<$t>()))
            }
        }
    };
}

#[macro_export]
macro_rules! impl_rkyv_configuration {
    ($t:ty) => {
        impl $crate::ConfigurationRecord for $t {
            fn from_rkyv_bytes(bytes: &[u8]) -> $crate::Result<Self> {
                rkyv::from_bytes::<$t, rkyv::rancor::Error>(bytes)
                    .map_err(|err| $crate::Error::Rkyv(err.to_string()))
            }
        }
    };
}
```

Every configuration record invokes **exactly one** of the two.
Call sites read symmetrically:

```rust
impl_nota_only_configuration!(SimpleConfig);
impl_rkyv_configuration!(MessageDaemonConfiguration);
```

**Cost**: one one-line macro invocation per type — same as
/183's design.
**Gain**: sound Rust without specialization.

The deviation is recorded in `nota-config/ARCHITECTURE.md`
§"Two macros, no blanket impl" with the same rationale.

## 3. Empirical finding: rkyv validation isn't "obvious garbage"

The first draft of `tests/rkyv_file.rs` included a
`corrupt_rkyv_file_returns_typed_error` test that wrote the
literal bytes `"not a valid rkyv archive"` (24 bytes) to a
`.rkyv` tempfile and expected `Error::Rkyv`. It **failed** —
`rkyv::from_bytes` interpreted those bytes as a valid
`DualConfig`:

```
DualConfig { name: "lid rkyv", port: 7311146942148534560 }
```

Lesson: rkyv with `bytecheck + unaligned + little_endian +
pointer_width_32` validates pointer offsets and string lengths
against the buffer, but happens to allow value-shaped garbage
through for simple record types whose archived layout fits
within the buffer.

The honest test is **"buffer too short to hold the archive,"**
not **"buffer looks weird."** Updated to a 1-byte file
(`truncated_rkyv_file_returns_typed_error`), which `bytecheck`
correctly rejects.

This is not a wrapper bug; it's rkyv's validator being
value-content-permissive. Worth knowing for future test
authoring: a malformed `.rkyv` file may decode to surprising
values; rely on length-based or type-mismatch tests for
negative cases.

## 4. Coordination state

- Operator-assistant lock: claimed
  `/git/github.com/LiGoldragon/nota-config` for the scaffold;
  to release after this report lands.
- Operator lock: actively on
  `/git/github.com/LiGoldragon/persona`,
  `/git/github.com/LiGoldragon/terminal-cell`,
  `[primary-31jt]`, `[primary-8n8]` —
  durable dev-stack router store + terminal-cell socket mode
  witness (the OA/121 §2.3 / DA/76 follow-ups). No conflict
  with this nota-config work.
- System-assistant lock: actively on the `horizon-re-engineering`
  worktree across 4 CriomOS repos — no overlap.

## 5. Open question — next slice

`designer/183` §10 names the next step after the scaffold:

> **Operator migrates `persona-message-daemon` first** (heaviest
> env-var user, simplest delivery boundary).

This is a three-repo cross-cutting change:

1. **`signal-persona-message`** — add
   `MessageDaemonConfiguration` typed record (per `designer/183`
   §8 Q4: per-component contract crate owns its config record),
   with NotaRecord + Archive + RkyvSerialize + RkyvDeserialize
   derives, plus `nota_config::impl_rkyv_configuration!`.
2. **`persona-message`** — replace the env-var-reading `main` in
   `src/daemon.rs:131–169` with
   `ConfigurationSource::from_argv()?.decode()?` per `designer/183`
   §7.2. Drop `SocketMode::from_environment`,
   `MessageOriginStamper::from_environment`,
   `SignalMessageSocket::from_environment`, and the supervision
   socket env-var reads in favour of fields on the typed config.
3. **`persona`** — update `src/direct_process.rs` to:
   - mint a `MessageDaemonConfiguration`,
   - write it to a state-dir path (default `.rkyv`, `.nota` for
     debug),
   - pass that path as argv to the spawned daemon,
   - drop the env-var sets it currently performs for the
     message daemon.

This is **production-touching, multi-commit, multi-repo work**
— per `skills/feature-development.md` it belongs on a feature
branch in a separate worktree, not on `main` of the canonical
checkouts. Each repo would get a parallel branch + worktree at
`~/wt/github.com/LiGoldragon/<repo>/<branch>/`.

Branch-name proposal: `typed-daemon-configuration`. Same name
across all three repos that the migration touches. The bead
that wraps this would carry the branch name explicitly per
`skills/beads.md`.

The user's call to make. The two clean choices:

- **Now, this session.** Spawn the worktrees, migrate the three
  repos, get the `persona-message-daemon`-with-typed-config
  story green via the dev-stack smoke. The work is bounded
  (one daemon's surface), the test surface already exists
  (`persona-dev-stack-smoke`).
- **Later, separate session.** This report stands as the
  handover; the next operator-assistant (or operator) picks up
  the bead, branches, and migrates.

There's no in-between worth picking. Half-migrating a daemon
across repos leaves a broken-supervisor problem until the
manager-side write lands.

A secondary user-attention item: the rkyv-test finding above
(§3) might motivate updating `designer/183`'s "Why prefer
rkyv" pitch with a one-line caveat — rkyv's validator catches
length and pointer violations but is value-content-permissive,
so production daemons should still treat a fresh decode as
"validated layout, not validated business semantics."

## 6. See also

- `reports/designer/183-typed-configuration-input-pattern.md`
  — the originating design.
- `reports/designer-assistant/76-review-operator-assistant-125-persona-engine-audit.md`
  §2.2 + Q1 — names `designer/183`'s typed-config approach as
  the right destination for stateful-daemon launch paths,
  superseding more env-var spawn args.
- `reports/designer/181-persona-engine-analysis-2026-05-15.md`
  §7 Q2 — already updated 2026-05-16 to point at `designer/183`
  as the structural successor to owner-uid-in-spawn-envelope.
- `https://github.com/LiGoldragon/nota-config` — the live
  scaffold.
- `~/primary/skills/feature-development.md` — the worktree
  discipline for the next slice.
- `~/primary/skills/jj.md` — version-control discipline for the
  next slice.
