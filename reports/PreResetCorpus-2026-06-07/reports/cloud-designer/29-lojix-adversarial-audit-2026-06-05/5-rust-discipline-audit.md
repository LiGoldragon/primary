# Dimension 5 — Rust-discipline + abstractions audit (lojix triad-port)

Adversarial read of `schema_runtime.rs`, `lib.rs`, `daemon.rs`,
`client.rs` against the workspace hard overrides (AGENTS.md, intent
records 712 / 882 / 884) and `skills/rust/methods.md`. Posture: broken
until proven otherwise. Every claim cites `file:line` in the canonical
pushed copies under `/git/github.com/LiGoldragon/lojix/triad-port/`.

## Headline

The four audited files are mostly clean on the method-placement rule —
**no module-scope free functions and no ZST namespace holders exist in
any of them** (grep for `^(pub )?(const |async )?fn ` returns empty for
all four). `NixCommand` is a real data-bearing noun. `Error` is a typed
`thiserror` enum, no `anyhow`. The serious findings are about **typed
domain values lost to `String`** (the `attribute` / `target_attribute`
String channel, M1's new surface) and a **latent command-injection /
broken-activation defect in `NixCommand::activate_system`** that is both
a security smell AND a correctness bug: the literal `$CLOSURE` it ships
is never defined, so M1's activate path can never deploy the built
closure even once addressing lands. These are flaws to fix, not deferred
M2/M3 scope.

## Finding 5.1 (HIGH, security + correctness) — `activate_system` ships an undefined `$CLOSURE` and is the one stringly-built remote shell

`schema_runtime.rs:1273-1283`:

```rust
fn activate_system(node_name: &str) -> Self {
    Self::new(
        "ssh",
        vec![
            node_name.to_string(),
            "nix-env -p /nix/var/nix/profiles/system --set \"$CLOSURE\"".to_string(),
        ],
    )
}
```

Two distinct defects in one method:

1. **`$CLOSURE` is never defined.** `run_activate_generation`
   (`schema_runtime.rs:1153-1166`) calls
   `NixCommand::activate_system(&command.node_name)` and the
   `ActivateGenerationCommand` (`nexus.rs:106-113`) carries no
   `closure_path` at all — it only has generation/cluster/node/kind. The
   pipeline DID compute the realised closure
   (`set_closure_path`, `schema_runtime.rs:689-693`) and stores it on the
   `DeployPipeline`, but `activate_generation_command`
   (`schema_runtime.rs:274-281`) drops it. `NixCommand::run`
   (`schema_runtime.rs:1292-1308`) spawns `ssh` via
   `Command::new`/`.args` with **no `.env(...)`** for `CLOSURE` (grep
   confirms no `CLOSURE`/`.env(` anywhere in the file). So the remote
   shell expands `$CLOSURE` to the empty string and runs
   `nix-env -p /nix/var/nix/profiles/system --set ""` — which fails or
   sets nothing. The legacy production deployer interpolates the actual
   path (`lojix-cli/src/activate.rs:62` `--set {store}` and
   `:115` `CLOSURE='{store}'` set inside the script body). The port lost
   that binding. This is not deferred M2/M3 addressing work — even with
   correct addressing the activation is a no-op as written.

2. **Stringly-typed remote shell — the one injection-shaped seam.** The
   audit brief is right that `copy_closure`/`build_closure_remote`/
   `flake_metadata`/`eval_drv_path` are clean: they push each argument
   as its own `Vec<String>` element and `Command::args` never invokes a
   shell, so `ssh-ng://{node_name}` and `{closure_path}` cannot break out
   (`schema_runtime.rs:1247-1271`). But `activate_system` passes a
   **single remote-command string as one ssh argument**, and ssh hands
   that string to the **remote login shell**. The moment the fix to (1)
   interpolates a value into that string (the obvious patch is
   `format!("nix-env ... --set {closure}")` mirroring the legacy
   `--set {store}`), `closure_path` flows unescaped into a remote shell.
   A `closure_path` (or, once copy/activate address by horizon, a
   `node_name` used to build the ssh target) carrying shell metacharacters
   is then injection. The legacy code defends this exact seam with
   `ShellArgument::new(...).to_command_text()`
   (`lojix-cli/src/activate.rs:143`, `:286`) — a quoting type the port
   has no equivalent of.

**Fix:** add `closure_path` to `ActivateGenerationCommand` in
`nexus.schema` (regenerate `nexus.rs`), thread it through
`activate_generation_command`, and have `activate_system` take the
closure path. Then either (a) pass the closure via `Command::env("CLOSURE", path)`
so the remote shell variable is genuinely set (cleanest — keeps the
remote string constant and argument-free), or (b) introduce a
`RemoteShellArgument`/`ShellArgument` quoting noun (port the legacy one)
and interpolate through it. Do NOT land a bare
`format!("... --set {closure_path}")`: that is the injection. Until the
closure is threaded, the activate path is dead code that silently
"succeeds" — assert this is M2 scope explicitly in the schema, don't
leave a method that looks done but isn't.

## Finding 5.2 (MEDIUM, typed-domain-values) — the `attribute` / `target_attribute` String channel defeats the newtype rule

M1 added the attribute-resolution path, and it is stringly-typed end to
end:

- `NixEvalCommand.attribute: String` (`nexus.rs:80-86`) — a flake output
  attribute path is a domain value with identity
  (`nixosConfigurations.target.config.system.build.toplevel`,
  `homeConfigurations.<user>.activationPackage`), not free text.
- `DeployAction::target_attribute(&self) -> String`
  (`schema_runtime.rs:134-143`) and
  `DeployPipeline::target_attribute(&self) -> String`
  (`schema_runtime.rs:241-251`) both **return bare `String`**, violating
  `skills/rust/methods.md` §"Domain values are types, not primitives"
  ("A node name is not a `String`").
- The meta contract DID mint a newtype-shaped alias for the override:
  `FlakeAttribute = String` (`meta lib.schema:85`, `meta lib.rs:69`) — a
  schema-emitted alias, legitimate per the brief. But the production
  (non-override) branch produces a raw `String`
  (`schema_runtime.rs:136-142`), and `DeployPipeline::target_attribute`
  collapses `Option<FlakeAttribute>` and the action-derived `String` into
  one untyped `String` (`:247-250`). So the moment you leave the override
  branch, the type identity `FlakeAttribute` is thrown away.

This is the "don't hide typification in strings" smell
(`skills/rust/methods.md` §"Don't hide typification in strings"): the
String is then concatenated with `#` in `run_nix_eval`
(`schema_runtime.rs:1112` `format!("{}#{}", command.flake, command.attribute)`)
and `.drvPath`-suffixed in `eval_drv_path`
(`schema_runtime.rs:1230` `format!("{attribute}.drvPath")`) — three
string-format sites manipulating what should be a typed flake-attribute
value.

**Fix:** make `DeployAction::target_attribute` and
`DeployPipeline::target_attribute` return `meta::FlakeAttribute` (the
schema-emitted alias is the natural carrier; the production branch builds
a `FlakeAttribute` too, not a `String`). Better still, promote
`FlakeAttribute` from a `String` alias to a real newtype in the meta
schema (`FlakeAttribute(String)` with a private field per the
methods skill) and put the `#`-join and `.drvPath`-suffix logic on it as
methods (`fixture.to_flake_reference(flake)`, `attribute.eval_target()`),
so `run_nix_eval`/`eval_drv_path` stop hand-formatting. The verb
(`#`-join, `.drvPath`) belongs on the attribute noun, not in
free-`format!` inside the engine method.

## Finding 5.3 (LOW, abstractions) — `DeployAction` is well-formed; one residual `String` leak

The new `DeployAction` enum (`schema_runtime.rs:93-144`) is **good**:
it's a proper sum type (`System(SystemAction)` / `Home { mode, user }`),
its three predicate methods (`produces_closure`, `activates`,
`target_attribute`) are inherent methods on the data-bearing enum (not a
ZST), and it correctly replaces what the doc-comment says were "derived
booleans" — the action is asked rather than storing parallel bool flags
(`schema_runtime.rs:62-64` comment). This directly satisfies the
"no bool flag-soup" requirement. The one blemish is the `String` return
of `target_attribute` covered in 5.2. No flag-soup, no parallel mirror,
no ZST. Pass on structure; fix the return type.

## Finding 5.4 (LOW, abstractions) — `MetaOperation` mirror vs. schema sum types

`MetaOperation` (`schema_runtime.rs:35-41`, `enum {Deploy,Pin,Unpin,Retire}`)
is a hand-written 4-variant enum tracking which meta mutation is in
flight, so `reject_active_or_meta` (`schema_runtime.rs:544-570`) can route
a generic `WriteRejected` back to the typed rejection reply. This is
arguably a "parallel mirror" of the meta `Input` discriminant
(`meta lib.schema:57` `[Deploy Pin Unpin Retire]`) that
`skills/rust/methods.md` §"Schema-generated objects are the method
surface" warns against. It is *defensible* — it carries genuine runtime
state (which op is mid-flight, an engine concern not on the wire) and is
a `Copy` enum, not a ZST. But the cleaner shape is to carry the
classification on the engine as the schema-emitted discriminant
(`meta::InputRoute`-style) rather than a private re-enumeration that must
be kept in sync by hand: if the meta contract gains a fifth owner verb,
this enum and its four `*_reason` mapping methods
(`schema_runtime.rs:572-610`) silently fall out of sync with no compile
error. Not a hard violation; flag for the synthesizer as a sync-risk.
**Fix (optional):** derive the in-flight operation from a schema-emitted
route enum, or at minimum add a non-`_` exhaustiveness guard so adding a
verb breaks the build.

## Finding 5.5 (MEDIUM, correctness-adjacent to discipline) — `client.rs` contract disambiguation rests on a false premise

`client.rs:79-90` `decode_signal_file` decodes a signal-encoded file by
**trying the owner (meta) contract first, then ordinary**, with the
comment "its short headers are distinct" / "the rkyv frame's short header
self-identifies" (`client.rs:82-83`). That premise is **false**: the meta
and ordinary contracts use **identical short-header bytes** —
`meta INPUT_DEPLOY = 0x0000000000000000`
(`meta-signal-lojix/.../schema/lib.rs:633`) and
`ordinary INPUT_QUERY = 0x0000000000000000`
(`signal-lojix/.../schema/lib.rs:930`), and the whole `0x0000`–`0x0004`
input range overlaps between the two contracts. `decode_signal_frame`
validates the header against the decoded value's own header
(`nexus.rs:946-951` pattern, same in both contracts), so a bytewise
ordinary `Query` frame whose rkyv layout happens to deserialize as a meta
`Deploy` would be mis-claimed as Owner and sent to the owner socket. The
"header self-identifies" claim doesn't hold because the two contracts
**share the header namespace**. This isn't a methods/free-fn violation,
but it's a stringly/bytewise-discrimination-without-a-discriminant smell
in the dimension-5 family ("the type system should carry the
discrimination"): the file's tier (Ordinary vs Owner) is not encoded in
the bytes, so the client guesses. **Fix:** the `ComponentArgument` /
signal-file format needs a contract-tier tag (a leading discriminant byte
distinguishing the two triad legs), or the CLI must require the caller to
state the tier. The try-owner-then-ordinary heuristic should be replaced
with an explicit tier discriminant, and the misleading "headers are
distinct" comment removed. (Confirm with dimension-2/wire auditor whether
the rkyv layouts can actually collide; I confirmed the header bytes
collide from the two `short_header` modules, which is enough to falsify
the comment.)

## Finding 5.6 (LOW, errors) — `Error` enum is complete, but two ad-hoc string-typed members

`lib.rs:28-71` — the `Error` enum is a proper `#[derive(thiserror::Error)]`
typed per-crate enum, no `anyhow`, with `#[from]` conversions for the
real source errors (io, nota, config, runtime argument/frame). Good. Two
minor smells:

- `Error::FlagArgument(String)` (`lib.rs:54`) is **misused as a generic
  message channel**: `client.rs:73-76` returns
  `Error::FlagArgument("inline NOTA request decoding requires the
  nota-text feature")` — that's a *missing-feature* condition, not a
  flag-style argument. The String payload is a free-text message where a
  variant should exist. **Fix:** add a dedicated
  `Error::InlineNotaUnsupported` (no payload) variant; reserve
  `FlagArgument` for an actual flag token.
- `Error::EffectFailed { stage: String, detail: String }` (`lib.rs:69-70`)
  re-stringifies the typed `nexus::EffectStage` enum
  (`nexus.rs:180-187`) into a `String`. The wire/engine already has the
  typed stage; the crate `Error` throws the type away. **Fix:** carry
  `stage: nexus::EffectStage` (the typed enum), not `String`. (Note: grep
  shows `EffectFailed` is currently never constructed in the four files —
  the engine replies a typed meta rejection via `fail_pipeline`
  (`schema_runtime.rs:714-727`) instead — so this is a dead/typed-wrong
  variant; either type it or remove it.)

## Finding 5.7 (LOW, methods placement — adjacent file, out of strict scope) — `bin/lojix-daemon.rs` `run()` is a free function

Out of the strict 4-file scope but caught while verifying the
free-function grep: `src/bin/lojix-daemon.rs:16` defines
`fn run() -> lojix::Result<()>` as a **module-scope free function**
beside `fn main()`. `main` is exempt; `run` is not. Per intent 882 /
`skills/rust/methods.md` §"Methods on types, not free functions" the only
module-scope exemptions are `fn main()` and `#[cfg(test)]`. The body
(decode configuration, construct `Daemon`, run) should be an associated
function — e.g. `Daemon::from_argv() -> Result<Self>` then
`daemon.run()`, with `main` calling that. `bin/lojix.rs` correctly avoids
this (its `main` calls `Client::run_from_environment()`, an associated
function — `client.rs:55`). Flag for the operator; trivial fix.

## Clean (adversarially confirmed, no violation)

- **No module-scope free functions** in `schema_runtime.rs`, `lib.rs`,
  `daemon.rs`, `client.rs` (grep `^(pub )?(const |async )?fn ` empty for
  all four). Every helper is an inherent method on `SchemaRuntime`,
  `DeployPipeline`, `DeployAction`, `MetaOperation`, `NixCommand`,
  `Store`, `StoreState`, `Daemon`, `LojixRuntime`, `Client`, or a trait
  impl. The private-helpers-inside-impl discipline (intent 882) holds.
- **No ZST namespace holders.** `NixCommand` (`schema_runtime.rs:1197-1201`)
  carries `program: String` + `arguments: Vec<String>` — a real
  data-bearing noun whose constructors (`flake_metadata`, `eval_drv_path`,
  `build_closure`, …) and `run` read its fields. `Daemon`, `LojixRuntime`,
  `Client` all carry fields. `ListenerRole` (`daemon.rs:29-32`) is a
  `Copy` discriminant enum used as the `MultiListenerRuntime::Listener`
  tag, not a method-holder ZST.
- **`NixCommand` is a clean program+args noun, not a shell-builder.**
  `run` (`schema_runtime.rs:1292`) uses `Command::new(program).args(...)`
  — no `sh -c`, no shell — so `flake_metadata`/`eval_drv_path`/
  `build_closure`/`build_closure_remote`/`copy_closure`/`collect_garbage`
  are injection-safe (args are vector elements). The single exception is
  `activate_system` — see Finding 5.1.
- **`Error` is a typed per-crate `thiserror` enum, no `anyhow`** anywhere
  in the crate (modulo the two String-payload smells in 5.6).
- **Naming is full English words** — `deployment_identifier`,
  `generation_identifier`, `commit_sequence`, `subscription_token`,
  `activation_kind`, `closure_path` etc.; no abbreviations. `DeployAction`
  variant predicates (`produces_closure`, `activates`, `target_attribute`)
  read as full words.
- **`DeployStage` / `DeployAction` / `MetaOperation` are sum types, not
  bool soup** — the M1 doc-comment claim that the action replaces
  "derived booleans" is borne out (`schema_runtime.rs:62-64`).

## Summary table for the synthesizer

| # | Sev | Where | Flaw | Fix |
|---|-----|-------|------|-----|
| 5.1 | HIGH | `schema_runtime.rs:1273-1283` + `:274-281` + `nexus.rs:106-113` | `activate_system` ships literal `$CLOSURE` that is never defined (no `.env`, closure_path dropped from `ActivateGenerationCommand`) → activation is a no-op; AND it's the one single-string remote shell, so the obvious fix opens injection | thread `closure_path` into `ActivateGenerationCommand`; set it via `Command::env("CLOSURE", path)` OR port a `ShellArgument` quoting noun — never a bare `format!("--set {closure_path}")` |
| 5.2 | MED | `nexus.rs:80-86`; `schema_runtime.rs:134-143`,`:241-251`,`:1112`,`:1230` | flake attribute is `String` end-to-end; `target_attribute()×2` return bare `String`; production branch discards the `FlakeAttribute` identity; 3 `format!` sites hand-build it | return `meta::FlakeAttribute`; promote alias to a real newtype with `#`-join / `.drvPath` methods on it |
| 5.3 | LOW | `schema_runtime.rs:93-144` | `DeployAction` well-formed (sum type, real methods, replaces bool flags) — only blemish is the 5.2 String return | covered by 5.2 |
| 5.4 | LOW | `schema_runtime.rs:35-41`,`:572-610` | `MetaOperation` is a hand-kept mirror of the meta `Input` discriminant; `_`-arms in `*_reason` maps hide future sync breaks | derive from schema route enum, or add exhaustiveness guard |
| 5.5 | MED | `client.rs:79-90` + `meta lib.rs:633` / `ordinary lib.rs:930` | "headers are distinct" is false — meta `INPUT_DEPLOY` == ordinary `INPUT_QUERY` == `0x0000…`; try-owner-then-ordinary can mis-route a frame | add a contract-tier discriminant to the signal-file/argument format; drop the false comment |
| 5.6 | LOW | `lib.rs:54`,`:69-70`; `client.rs:73` | `FlagArgument(String)` reused as a missing-feature message; `EffectFailed{stage:String}` re-stringifies typed `EffectStage` (and is never constructed) | add `InlineNotaUnsupported` variant; carry `EffectStage` typed or delete the dead variant |
| 5.7 | LOW | `bin/lojix-daemon.rs:16` (out of strict scope) | `fn run()` is a module-scope free function beside `main` | make it `Daemon::from_argv()` + `daemon.run()` |
