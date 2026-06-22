# Schema IR integration — merge-ready handoff to schema-operator

*schema-designer · report 12 · the psyche asked schema-designer to land the
schema-IR unification to `main` across the four repos "along with"
schema-operator. Live coordination check shows schema-operator already holds
all four repos and is mid-integration on the identical work, so this is a
**handoff**, not a solo land. The `schema-ir` reference is verified green and
merge-ready; this report is the exact recipe operator needs to land it on each
repo's `main`.*

## Coordination outcome: HANDED OFF (operator owns main, integration in flight)

Live daemon observation (`orchestrate "(Observe Roles)"`, re-checked) shows
`schema-operator` (Codex) actively claiming all four repos with this exact work:

| Repo claimed by schema-operator | Reason on the claim |
|---|---|
| `/git/github.com/LiGoldragon/nota-next` | producer integration for schema-ir Help collapse before signal-spirit main |
| `/git/github.com/LiGoldragon/schema-next` | collapse Help onto schema IR on mainline with schema-designer schema-ir branches |
| `/git/github.com/LiGoldragon/schema-rust-next` | producer integration for schema-ir Help collapse before signal-spirit main |
| `/git/github.com/LiGoldragon/signal-spirit` | collapse Help onto schema IR on mainline with schema-designer schema-ir branches |

Per the integration discipline (`skills/main-feature-integration.md`) and the
psyche's "do it along with him": operator owns code-repo `main`. I did NOT claim
any repo, did NOT touch any `main`, and did NOT race. schema-designer's
contribution is the tested reference cut plus this handoff. The `schema-ir`
branches are all pushed to their remotes — operator integrates from there.

## Reference tips (pushed to remote, verified)

| repo | `schema-ir` tip | based on its current `main`? |
|---|---|---|
| nota-next | `4642807` | yes — base == `main` HEAD (`f94b546`) |
| schema-next | `1bfeb9c` | yes — base == `main` HEAD (`4b7e830`) |
| schema-rust-next | `b744e1d` | yes — base == `main` HEAD (`90d853c`) |
| signal-spirit | `39b1506` | **NO — base `7ae038e`; `main` advanced 2 commits** |

Three of four `schema-ir` branches are already based directly on current `main`
and rebase trivially. **signal-spirit is the only one needing a real rebase**,
and it carries a substantive reconciliation (see §"signal-spirit reconciliation").

## Green confirmation (run on the path-patched integration build)

All run in the `~/wt/.../schema-ir` worktrees (the integration build with local
`[patch]` path redirects, i.e. one IR flowing end to end):

- **signal-spirit `--features nota-text`** — lib 0, daemon_configuration 2,
  dependency_boundary 2, generated_contract 16,
  help_instance_schema_convergence **3**, instance_schema 10, validation 3 — all
  ok.
- **convergence test** (`tests/help_instance_schema_convergence.rs`) — 3 passed:
  `(Help Domains) -> (Domains (Vector Domain))`; Help `SourceReference` ==
  instance-schema's; Help decl == instance-schema expanded view.
- **signal-spirit daemon-default** (`cargo build` / `cargo test`, no features) —
  clean, no warnings; the `dependency_boundary` gate passes (runtime tree
  excludes nota-next / schema-next).
- **schema-next/schema-ir** full suite — green (all result lines ok, incl. 6
  instance render + help source_codec families).

## Land order and exact per-repo recipe

Land producers before consumers; after each producer lands, repin the next
consumer to that `main` and re-fetch. Every `schema-ir` branch's git deps
currently pin `branch = "schema-ir"`; for `main` they flip to `branch = "main"`,
and signal-spirit's cross-repo `[patch]` block is removed entirely.

### 1. nota-next (`schema-ir` `4642807`) — first

No cross-repo deps (only the internal `nota-next-derive = { path = "derive" }`).
Already based on `main`. Land as-is.

```
cd /git/github.com/LiGoldragon/nota-next
jj git fetch
jj rebase -d main -b schema-ir        # no-op / fast-forward; base already == main
jj bookmark set main -r <schema-ir tip>
jj git push --bookmark main
```

### 2. schema-next (`schema-ir` `1bfeb9c`) — after nota-next

Repin nota-next `schema-ir` → `main` in `Cargo.toml` (two sites):
`[dependencies]` line and `[dev-dependencies]` line, both
`nota-next = { git = "...nota-next.git", branch = "schema-ir" }` →
`branch = "main"`. Then green (`cargo test`), then land.

### 3. schema-rust-next (`schema-ir` `b744e1d`) — after schema-next

Repin in `Cargo.toml`:
- `[dependencies]` `schema-next` `branch = "schema-ir"` → `"main"` (line 19)
- `[dev-dependencies]` `nota-next` `branch = "schema-ir"` → `"main"` (line 35)
- **KEEP** `[patch.crates-io] kameo = { git = "...kameo.git", branch = "main" }`
  (line 47) — that is a legitimate upstream fork patch, NOT a worktree pin; it is
  on every branch including `main`. Do not remove it.

Then green, then land.

### 4. signal-spirit (`schema-ir` `39b1506`) — last; see reconciliation below

`Cargo.toml` changes for `main`:
- `[dependencies]` `nota-next` (l28) + `schema-next` (l29): `schema-ir` → `main`
- `[build-dependencies]` `schema-rust-next` (l35): `schema-ir` → `main`
- `[dev-dependencies]` `nota-next` (l38) + `schema-next` (l39): `schema-ir` → `main`
- **Remove the entire cross-repo `[patch]` block (lines 46-61)** — the three
  `[patch."https://github.com/LiGoldragon/{nota-next,schema-next,schema-rust-next}.git"]`
  entries pinning `../../<repo>/schema-ir` worktrees. `main` resolves these
  upstreams through their `main` branches, not worktree paths.

## signal-spirit reconciliation — REAL, operator must handle

signal-spirit `main` advanced 2 commits past the `schema-ir` base (`7ae038e`):
`54dff5f` (add daemon authorization mode) and `1de570e` (document authorization
mode). These add an `AuthorizationMode [Gating Observing]` enum and an
`AuthorizationMode` field on `SpiritDaemonConfiguration`. They touch the SAME
files the schema-ir branch rewrote:

| file | main's change | schema-ir's change | reconcile by |
|---|---|---|---|
| `schema/signal.schema` | +`AuthorizationMode` enum + field (2 sites, ~line 162) | Vec→Vector migration (30 lines, scattered) | text-merge — mostly disjoint sites; keep BOTH the AuthorizationMode additions and the (Vector T) spellings |
| `src/schema/signal.rs` | hand-added AuthorizationMode type + field (+18 lines) | **regenerated** (980 lines) from schema-rust-next | **regenerate, don't text-merge** — after the schema source carries both AuthorizationMode and (Vector T), the generated `signal.rs` is the build product; let the build/codegen produce it |
| `src/lib.rs` | +`with_authorization_mode` / `authorization_mode()` methods + field in constructor | +4 lines (Help wiring) | text-merge — both add to `impl SpiritDaemonConfiguration`; keep both |
| `tests/daemon_configuration.rs` | +33 lines (AuthorizationMode round-trip tests; main has more assertions) | unchanged (2 tests) | **take main's version** — it's the superset; the schema-ir branch never touched this file |
| `ARCHITECTURE.md`, `INTENT.md` | doc additions | INTENT +9 (schema-ir) | text-merge — disjoint |

The cleanest operator path for signal-spirit: rebase `schema-ir` onto current
`main`, resolve the `signal.schema` / `lib.rs` / docs conflicts by keeping both
sides, **take main's `daemon_configuration.rs`**, then **regenerate
`src/schema/signal.rs`** from the merged schema rather than hand-merging the
generated file. After regeneration, the AuthorizationMode field must round-trip
through the new Help/instance-schema codec (it's a plain enum + field, so it
should fall out for free; the convergence test does not cover it, so add or
extend a daemon_configuration assertion if operator wants belt-and-suspenders).

## Green gate before each push

The convergence test, instance-schema tests, signal-spirit `--features
nota-text` suite, daemon-default build + `dependency_boundary` gate — all green
before pushing each repo's `main`. After signal-spirit's regeneration, re-run the
full `--features nota-text` suite (daemon_configuration must now show main's
larger count, not 2).

## Divergence note for the psyche

The two cuts (designer's `schema-ir` and operator's in-flight integration) are
designed to converge on the same unified `SourceReference` IR. The only
divergence found is operational, not semantic: signal-spirit `main` gained the
`AuthorizationMode` feature after the `schema-ir` branch forked, so the landing
must fold AuthorizationMode into the regenerated contract. No conflict in the IR
design itself; nota-next / schema-next / schema-rust-next have zero divergence
(their `schema-ir` is already main-based).

## What landed vs what is staged

### Update — operator landed the three producers while this handoff was written

A re-fetch at hand-off time shows schema-operator already landed the producers,
as **repinned per-concern cuts** (not my raw `schema-ir` tips as ancestors —
operator owns main and split the merge cleanly, which is correct):

| repo | landed `main` | content |
|---|---|---|
| nota-next | `4642807` (== schema-ir tip) | instance-schema decoder base |
| schema-next | `9219e32` "land schema IR source codec on main pins" (+ `aca86ff`, `a8fa3a6`) | unified IR source codec, repinned to main |
| schema-rust-next | `e4ac3ba` "land instance schema emitter on main pins" (+ `37e2904`) | NotaDecodeTraced emitter, repinned to main |
| **signal-spirit** | **NOT landed — still `1de570e`** | the consumer, last in order, carries the AuthorizationMode reconciliation |

The producer IR content matches this unified-IR design (same SourceReference
codec + instance-schema emitter); operator's commit structure differs from my
branch's, which is operator's prerogative. **No semantic divergence.**

### Remaining: signal-spirit (operator's, the one with the reconciliation)

- repin nota-next/schema-next/schema-rust-next `schema-ir` → `main`
- remove the cross-repo `[patch]` block (lines 46-61)
- fold in AuthorizationMode (take main's `daemon_configuration.rs`; **regenerate**
  `src/schema/signal.rs`; keep both sides in `signal.schema` / `lib.rs` / docs)
- green the full `--features nota-text` suite + daemon-default boundary, then land

### schema-designer contribution

- **Landed on any `main` by schema-designer: nothing** (correct — operator owns
  code-repo main; racing was forbidden).
- **Delivered:** the four tested `schema-ir` reference branches (pushed, verified
  green) + this exact merge recipe + the AuthorizationMode reconciliation
  operator needs for the final signal-spirit land.
