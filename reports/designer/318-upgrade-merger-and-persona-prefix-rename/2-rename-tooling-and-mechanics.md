*Kind: Research · Topic: rename-tooling-and-mechanics · Date: 2026-05-24*

# 318/2 · Rename tooling + mechanics — Cargo, Nix, ghq, jj, source rewrite

Subagent B's slice of the 318 dispatch. Frame in
`0-frame-and-method.md`; inventory in
`1-rename-inventory-and-dependency-graph.md` (Subagent A);
upgrade triad design in `3-upgrade-triad-structural-design.md`
(Subagent C). This file answers the **mechanical how-to**
question: given the rename sweep ratified by spirit 371 plus the
upgrade-merger ratified by spirit 369, is each per-triad rename
mechanically feasible, and what is the operator's keystroke-level
recipe?

Bounded to read-only inspection. No `cargo build`, no `nix
build`, no jj commits authored from inside this dispatch.

## §1 Cargo rename mechanics

### §1.1 Three identifier slots per crate

Cargo resolves dependencies by **`[package].name`**, not by
directory name and not by `[lib].name`. Three distinct slots
interact. Verified against
`/git/github.com/LiGoldragon/persona-spirit/Cargo.toml:1-22`:

| Slot | Where set | Affects |
|---|---|---|
| Package name | `[package].name` | dependent declaration; `cargo` resolution by id |
| Lib name | `[lib].name` (defaults to package name with `-` → `_`) | Rust import token: `use <libname>::…` |
| Bin names | `[[bin]].name` (one per binary) | produced binary filenames under `target/release/` |

The repository on-disk directory name and source-file paths are
INDEPENDENT of the above; Cargo doesn't care. The git remote URL
and the flake input URL DO care (§2, §3).

For `signal-persona-spirit` → `signal-spirit`, three slots
update in the upstream manifest:

```toml
[package]
name         = "signal-spirit"
description  = "Signal contract for the ordinary spirit surface."
repository   = "https://github.com/LiGoldragon/signal-spirit"

[lib]
name = "signal_spirit"
```

The contract crate has no `[[bin]]` block (lib-only). For the
daemon repo `persona-spirit` → `spirit`, the `[[bin]]` block's
`spirit` CLI keeps its name; the daemon binary renames from
`persona-spirit-daemon` to `spirit-daemon` per
`skills/component-triad.md` §"Binary naming table".

### §1.2 Does Cargo fail for dependents that still spell the old name? Yes — immediately

Once `[package].name` changes upstream, any dependent whose
Cargo.toml still says `signal-persona-spirit = { git = "..." }`
fails at resolution time: Cargo consults the upstream's
manifest, finds `name = "signal-spirit"`, and reports no crate
named `signal-persona-spirit` is available at the resolved
revision. Verified against Cargo's documented behaviour in the
"manifest format" reference under `[dependencies]` (the spec
states the dependency key matches the upstream `[package].name`
unless `package = "…"` overrides it; see §1.3).

In our workspace, dependents are git-URL crates pinned to
`branch = "main"`. The break window opens on the dependent's
next `cargo update` after the rename pushes — not at the push
moment itself, because Cargo.lock keeps each dependent pinned to
the prior commit until refreshed. The §6 worked example pushes
the rename + every dependent's Cargo.toml update in lockstep.

### §1.3 The `package = "…"` bridge directive

Cargo's manifest reference documents that a dependency table can
rename the local key with a `package = "<actual-name>"` field.
This bridges old↔new during transition:

```toml
# In a dependent that still uses the old import token internally:
signal_persona_spirit = { git = "https://github.com/LiGoldragon/signal-spirit.git", package = "signal-spirit" }
```

Cargo resolves the upstream by `package = "signal-spirit"` while
the local table key (`signal_persona_spirit`) becomes the EXTERN
crate name visible to the dependent's source — the dependent can
keep writing `use signal_persona_spirit::…` even after the
upstream package renames. Witness in
`/git/github.com/LiGoldragon/lojix/Cargo.toml`:

```toml
horizon-lib  = { git = "...", branch = "...", package = "horizon-lib" }
horizon-nota-codec = { package = "nota-codec", git = "https://github.com/LiGoldragon/nota-codec.git" }
```

The second line aliases `nota-codec` → `horizon-nota-codec`
locally; the first is a redundant-but-valid form. Two dependents
in different workspaces CAN point at the same upstream under
different local keys — each dependent's Cargo.toml is
independent.

**Recommendation for this sweep:** do NOT use the bridge form.
Update each dependent in lockstep with the upstream rename and
land the chain together per triad. The bridge costs one extra
line and adds indirection that hurts readability; it's only
useful when a dependent's owner is unavailable, and in this
solo-author workspace there is no unavailable owner.

### §1.4 Multi-crate Cargo workspaces

Most LiGoldragon repos are single-crate (one Cargo.toml, one
`[package]`, no `[workspace]`). Workspace exceptions today:
`horizon-rs`, `kameo`, `signal-frame`, `signal-core`,
`WebPublish`. **None intersect the 318 rename sweep** — the
affected repos (persona-*, signal-persona-*,
owner-signal-persona-*, sema-upgrade, version-handover,
version-projection) are all single-crate.

If a member SUBDIRECTORY of a workspace repo were renamed, the
workspace root's `members = […]` array would need updating. Not
load-bearing here.

### §1.5 `cargo add --rename` and `cargo remove`

Cargo 1.95.0 (verified locally) has built-in dependency-table
helpers (stable since Rust 1.62):

```sh
cargo add signal-spirit --git https://github.com/LiGoldragon/signal-spirit --branch main
cargo add signal-spirit --git ... --branch main --rename signal_persona_spirit
cargo remove signal-persona-spirit
```

`--rename` writes the `package = …` bridge from §1.3. No
external `cargo-edit` install needed. The upstream's OWN
Cargo.toml edits (renaming `[package].name`, `[lib].name`,
`description`, `repository`) are all MANUAL — `cargo add` only
edits dependency tables.

### §1.6 Shell-command count for one rename

For one signal-* rename across ~3 dependents (the persona-spirit
family's current count from `grep`): 1 upstream Cargo.toml edit
+ 3 dependent Cargo.toml edits + ~30 source-file edits + 3
`cargo update` + 3 `cargo check` ≈ 30 shell commands plus
per-file edits. Bounded by dependent set, not Cargo mechanics.

## §2 Nix flake mechanics

### §2.1 What a flake.nix carries

Three top-level fields. Verified against
`/git/github.com/LiGoldragon/signal-persona-spirit/flake.nix:1-15`:

```nix
{
  description = "signal-persona-spirit - Signal contract for the ordinary persona-spirit surface";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    ...
  };
  outputs = { self, nixpkgs, flake-utils, ... }: ...;
}
```

`description` is text-only, no semantic load. `inputs` names
other flakes (each input has a URL + the implicit input-name
from its attrset key). `outputs` takes `self` + resolved inputs
and returns build derivations.

What changes in the renamed flake's own `flake.nix`:

| Field | Change |
|---|---|
| `description` | substitute new name (cosmetic) |
| `inputs` | unchanged (only references upstream tooling, not the rename target itself) |
| `outputs` | function args unchanged; `devShells.default.name` updates; `packages.<name>` keys rename if keyed by old name |

For `persona-spirit/flake.nix:42-67` (a daemon flake), the
`packages` attrset is currently:

```nix
packages = {
  default = spiritPackage;
  spirit = spiritPackage;
  persona-spirit-daemon = daemonPackage;
  full = fullPackage;
};
```

After rename, `persona-spirit-daemon` becomes `spirit-daemon`
across packages + apps + the `mkApp` name field. Witness in
`sema-upgrade/flake.nix` which references
`persona-spirit.packages.${system}.persona-spirit-daemon` —
that attribute key must update on both sides.

### §2.2 Dependent flakes — input rename

A dependent's `inputs` declares the rename target. In
`persona/flake.nix`:

```nix
# Before:
persona-spirit.url = "github:LiGoldragon/persona-spirit";
signal-persona-spirit.url = "github:LiGoldragon/signal-persona-spirit";
# After:
spirit.url = "github:LiGoldragon/spirit";
signal-spirit.url = "github:LiGoldragon/signal-spirit";
```

Plus the `outputs` function parameter list updates to match,
plus every body reference to the old name (e.g.
`persona-spirit.packages.${system}.persona-spirit-daemon` →
`spirit.packages.${system}.spirit-daemon`).

### §2.3 flake.lock — keyed by input name, not URL

A `flake.lock` is a JSON object with a `nodes` map. Each input
becomes a node keyed by its input NAME. Verified via `jq
'.nodes."persona-spirit"'` against
`/git/github.com/LiGoldragon/persona/flake.lock`:

```json
{
  "inputs": { "crane": ["crane"], ... },
  "locked": {
    "ref": "refs/heads/main",
    "rev": "d396ad357cf7dfcd9cfcce26993c0e9119f5a93d",
    "type": "git",
    "url": "https://github.com/LiGoldragon/persona-spirit.git"
  },
  "original": { "owner": "LiGoldragon", "repo": "persona-spirit", "type": "github" }
}
```

Two URLs per entry: `original` (user-typed) and `locked`
(resolved revision). The node KEY is the input name from
`flake.nix`. Renaming the input requires the lock's node key to
change too — the lock doesn't auto-rename.

Operator workflow for relock:

```sh
cd /git/github.com/LiGoldragon/<dependent>
# After editing flake.nix to rename the input:
nix flake update spirit            # update one specific input
# or:
nix flake lock                     # rewrite the whole lock
```

For URL-only changes (GitHub repo rename without input-name
rename), `nix flake update <input-name>` re-resolves the URL and
refreshes the locked revision; node key stays.

### §2.4 `nix flake metadata` for audit

`nix flake metadata <flake-ref>` prints resolved + locked URL of
a flake and its inputs. After the rename + relock, the operator
verifies no input still resolves to a
`github:LiGoldragon/<old-name>` URL. There is **no built-in
"find all dependents of input X"** command — the audit is `grep
-l "persona-spirit" /git/.../*/flake.nix` plus per-dependent
`nix flake metadata` verification.

## §3 ghq + GitHub rename mechanics

### §3.1 ghq's storage model

ghq stores checkouts at `$(ghq root)/<host>/<owner>/<repo>`.
This workspace's `ghq root` is `/git/`, so checkouts land at
`/git/github.com/LiGoldragon/<repo>`. `/home/li/primary/repos/`
is a flat symlink index (e.g. `repos/persona →
/git/github.com/LiGoldragon/persona`). ghq has no `rename`
subcommand — the local-side rename is plain `mv` plus updating
the git remote URL.

### §3.2 GitHub's redirect behaviour

GitHub redirects renamed repos automatically. Per GitHub Docs ›
Repositories › Repository names and renames:

- The old URL (HTTPS + SSH + API) redirects to the new URL
  indefinitely.
- Redirect breaks ONLY if the old name is reused by another repo
  under the same owner.
- Covers `git fetch`, `git clone`, `git push`, REST/GraphQL APIs,
  and the web UI.

For our `github:LiGoldragon/<old-name>` flake inputs, Nix's
`github:` fetcher follows the redirect. **A flake input pointing
at the OLD name after a GitHub rename continues to fetch
successfully**, but the resolved URL in the lock entry reflects
the new canonical URL. The lock SHOULD still be refreshed to
point at the new URL explicitly — the redirect is
emergency-tolerance, not a substitute for naming hygiene.

### §3.3 Recommended order: local-first

Two paths:

**Local first** — operator renames the local directory, updates
all Cargo.toml + flake.nix locally, verifies the new shape
compiles, then performs the GitHub rename and refreshes remote
URLs + flake.locks.

**GitHub first** — operator renames the GitHub repo first, then
moves local directory, updates remote URL, continues with local
edits.

**Recommendation: local-first.** Rationale:

1. **Reversibility.** Local-first is recoverable by reverting
   the local edits (`jj undo`, no GitHub state to re-roll).
2. **Atomic verification.** With all manifests updated locally
   to the new names, the operator verifies the whole sweep
   compiles before any remote-side action.
3. **GitHub rename is cheap to perform last.** Once the local
   sweep is verified, the GitHub rename + remote-URL update is
   per-repo two-command:
   ```sh
   gh repo rename signal-spirit \
     --repo LiGoldragon/signal-persona-spirit
   git -C /git/github.com/LiGoldragon/signal-spirit \
     remote set-url origin git@github.com:LiGoldragon/signal-spirit.git
   ```
4. **Spirit pilot non-interference.** Pilot's deployed v0.1.0
   and v0.1.1 binaries continue to be reachable at the old
   GitHub repo names during local edits; no risk of breaking
   pilot-in-flight by an early GitHub rename.

## §4 jj patterns for the rename commits

### §4.1 Per-repo commit boundary

Each `/git/github.com/LiGoldragon/<repo>` is its own colocated
jj repository; a single commit cannot span multiple repos. Plus
`skills/jj.md` §"Per-logical-commit pushes — not batch" mandates
a push per logical commit. The triad rename naturally lands as
one commit per touched repo:

```sh
# In the renamed repo:
cd /git/github.com/LiGoldragon/signal-spirit
jj commit -m 'signal-spirit: rename from signal-persona-spirit'
jj bookmark set main -r @-
jj git push --bookmark main

# In each dependent:
cd /git/github.com/LiGoldragon/persona
jj commit -m 'persona: track signal-persona-spirit → signal-spirit'
jj bookmark set main -r @-
jj git push --bookmark main
```

Commit-message pattern: `<repo>: <verb> <scope>`. For the
renamed crate itself: `<new-name>: rename from <old-name>`. For
dependents: `<repo>: track <old-name> → <new-name>`.

### §4.2 Headless jj mandatory

Per `skills/jj.md` §"Never let jj open an editor": every commit
invocation uses `-m '<msg>'`. Verified that this workspace's jj
config has `ui.editor = "emacsclient -c"` (from `jj config
list`), which would spawn a graphical Emacs frame and hang an
agent session. The operator-bead description must restate the
inline-only rule.

### §4.3 Workspace VCS shape

Verified by `jj config list`: jj-on-git colocated repos. The
on-disk repo has both `.git/` and `.jj/`; `jj git push` is the
publish path. GPG signing is `signing.behavior = 'own'` with a
configured key; jj signs locally; GitHub accepts both signed and
unsigned (no enforced sign-required ruleset). No git-side
concerns beyond standard SSH push auth.

### §4.4 Scripting per-repo rename commits

The persona-prefix sweep spans ~25 repos. For the automated
pass:

```sh
for repo in <Subagent-A's-rename-list>; do
  cd "/git/github.com/LiGoldragon/$repo"
  # edits per §1, §2 above
  jj st                                      # working-tree check
  jj commit -m '<msg>'
  jj bookmark set main -r @-
  jj git push --bookmark main
done
```

**Do NOT** script the `jj st` inspection out — it's the
working-copy check from `skills/jj.md` §"Before you commit —
the working-copy check", and the rename sweep is exactly the
situation where the working tree might contain a peer agent's
stray edit. **Recommendation:** batch 3-5 repos per operator
session with human review of each batch's diffs before pushing.
Fully automated 25-repo runs are too easy to get wrong; batched
semi-automated is the right granularity.

`jj split` is NOT the shape for triad renames — split divides
ONE working-copy commit into multiple commits in the SAME repo.
The rename is naturally one-commit-per-repo; no splitting
needed.

## §5 Workspace-wide source rewrite tooling

### §5.1 `cargo add --rename` and `cargo remove`

Per §1.5, Cargo's built-in helpers cover dependent
`[dependencies]` table edits. They do NOT cover:

- Renaming `[package].name`, `[lib].name`, `description`,
  `repository`. Manual edit required.
- Renaming `[[bin]]` blocks. Manual.

The renamed crate's OWN Cargo.toml edits are manual; dependent
manifest edits can be scripted.

### §5.2 `rg --replace` — preview only, not file rewrite

ripgrep's `--replace` flag does **NOT modify files**. From `rg
--help`: *"Neither this flag nor any other ripgrep flag will
modify your files."* It's display-time substitution for
previewing a rewrite. Useful in preview mode:

```sh
rg 'signal_persona_spirit' --replace 'signal_spirit' \
  --type rust /git/github.com/LiGoldragon/
```

For actual file rewrites, pipe the rg-matched file list through
`sed -i`:

```sh
rg -l 'signal_persona_spirit' --type rust \
  /git/github.com/LiGoldragon/ \
  | xargs sed -i 's/signal_persona_spirit/signal_spirit/g'
```

### §5.3 `sed -i` — fragile, fast, scriptable

For the rename sweep, `sed -i` over a curated file list is the
default. Failure modes:

1. **Substring false positives.** `signal_persona_spirit_extra`
   matches. Use word-boundary: `s/signal_persona_spirit\b/.../`
   on GNU sed.
2. **Hyphen vs underscore.** Rust import tokens use
   `signal_persona_spirit`; Cargo.toml + flake.nix use
   `signal-persona-spirit`; binary names use
   `persona-spirit-daemon`. Each form is a distinct sed pass on
   the right file subset.
3. **Documentation drift.** ARCHITECTURE.md, AGENTS.md,
   README.md reference the old name in prose; default to
   programmatic rewrite with operator review.

Three sed passes per single rename, applied to disjoint file
sets:

| Pass | Pattern | Files |
|---|---|---|
| 1. Rust tokens | `s/signal_persona_spirit/signal_spirit/g` | `*.rs` |
| 2. Cargo/flake hyphen | `s/signal-persona-spirit/signal-spirit/g` | `Cargo.toml`, `flake.nix`, `flake.lock` |
| 3. Daemon binary name | `s/persona-spirit-daemon/spirit-daemon/g` | `flake.nix`, systemd unit files, scripts |

### §5.4 rust-analyzer rename — daemon-mode, batch-unfriendly

rust-analyzer supports cross-crate rename via LSP
`textDocument/rename` when running as a server. Editor
integrations drive it. There's no documented `rust-analyzer
rename <old> <new>` CLI shape for one-shot batch rewrites
(verified `rust-analyzer --help`).

This makes rust-analyzer mismatched to the 318 sweep: the sweep
touches MANY independent jj repos that are not opened as a
single rust-analyzer workspace; even within one repo,
rust-analyzer's rename targets a specific symbol at a specific
location, not a crate-wide identifier rename. Useful only for
cleanup sub-cases (renaming a specific type or function after
the main pass).

### §5.5 Recommended tool combination

Operator's tool stack for one per-triad rename:

| Step | Tool |
|---|---|
| 1. Locate file set | `rg -l` |
| 2. Preview rewrite | `rg --replace` |
| 3. Apply Rust token rewrite | `sed -i` over `*.rs` |
| 4. Apply Cargo dependent rewrite | `cargo remove` + `cargo add` or sed |
| 5. Apply hyphenated rewrite | `sed -i` over manifests + flakes |
| 6. Edit upstream Cargo.toml | editor (manual) |
| 7. Edit flake.nix | editor (manual) |
| 8. Refresh flake.lock | `nix flake lock` per dependent |
| 9. Verify | `cargo check` + `nix flake check` |
| 10. Commit per repo | `jj commit -m '<msg>'` |
| 11. Push per repo | `jj git push --bookmark main` |

The operator-bead description must restate steps 6-7 as MANUAL
(flake.nix and the upstream manifest are hand-shaped, not
regex-driven) and steps 3-5 as scripted with `jj st` review
between batches.

## §6 End-to-end worked example — `signal-persona-spirit` → `signal-spirit`

Walking every step from "before" to "after" with file:line
citations. The before state's dependents (sample from `grep`
today): `/git/.../persona/Cargo.toml`,
`/git/.../persona-spirit/Cargo.toml`,
`/git/.../sema-upgrade/Cargo.toml` (Cargo.toml deps);
`/git/.../persona/tests/daemon.rs:23`,
`/git/.../sema-upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:5`
(source `use` statements); `/git/.../persona/flake.nix` (flake
input).

### §6.1 Step 1 — Local directory rename + upstream manifest

```sh
mv /git/github.com/LiGoldragon/signal-persona-spirit \
   /git/github.com/LiGoldragon/signal-spirit
cd /git/github.com/LiGoldragon/signal-spirit
```

Edit `Cargo.toml`: `[package].name` → `signal-spirit`,
`[lib].name` → `signal_spirit`, `description` + `repository`
fields. Edit `flake.nix:1-2` description and the
`devShells.default.name` field. Edit `tests/round_trip.rs` if it
references `signal_persona_spirit` as its tested crate.

### §6.2 Step 2 — Dependent Cargo.toml updates

For each dependent identified by Subagent A:

```sh
cd /git/github.com/LiGoldragon/<dependent>
sed -i 's/signal-persona-spirit/signal-spirit/g' Cargo.toml
```

Sample diff in `persona-spirit/Cargo.toml`:

```toml
# Before:
signal-persona-spirit = { git = "https://github.com/LiGoldragon/signal-persona-spirit.git", branch = "main" }
# After:
signal-spirit = { git = "https://github.com/LiGoldragon/signal-spirit.git", branch = "main" }
```

The `.git` URL suffix updates from the same sed pattern because
the URL contains the hyphenated old name.

### §6.3 Step 3 — Dependent source `use` rewrites

```sh
rg -l 'signal_persona_spirit' --type rust /git/github.com/LiGoldragon/ \
  | xargs sed -i 's/\bsignal_persona_spirit\b/signal_spirit/g'
```

`\b` boundary keeps `owner_signal_persona_spirit` safe (its own
rename is a separate operator bead). Sample diffs:

```rust
// /git/.../persona/tests/daemon.rs:23
// Before:  use signal_persona_spirit::{…};
// After:   use signal_spirit::{…};

// /git/.../sema-upgrade/src/migrations/persona_spirit/version_0_1_0_to_0_1_1.rs:5
// Before:  use signal_persona_spirit as current;
// After:   use signal_spirit as current;
```

### §6.4 Step 4 — GitHub rename (deferred until local commits land)

Per §3.3 local-first, the local edits + commits land first. The
GitHub rename happens after, via one CLI call per repo:

```sh
gh repo rename signal-spirit --repo LiGoldragon/signal-persona-spirit
git -C /git/github.com/LiGoldragon/signal-spirit \
  remote set-url origin git@github.com:LiGoldragon/signal-spirit.git
```

GitHub auto-creates the redirect indefinitely (per §3.2).

### §6.5 Step 5 — Flake input rename + lock refresh in each dependent

After the GitHub rename, each dependent's flake.nix edits + lock
refresh:

```sh
sed -i 's/signal-persona-spirit/signal-spirit/g' \
  /git/github.com/LiGoldragon/<dependent>/flake.nix
cd /git/github.com/LiGoldragon/<dependent>
nix flake lock
```

The sed pass updates the `inputs` attrset key, the URL, the
`outputs` parameter, and body references. Operator opens the
diff to verify the outputs parameter list updated correctly.

The flake-side edits are deferred until AFTER the GitHub rename
to avoid the transition window where flake.nix points at
`github:LiGoldragon/signal-spirit` while GitHub still has it as
`signal-persona-spirit` (which would break `nix flake lock`).

### §6.6 Step 6 — Cargo + nix verification per dependent (operator session)

```sh
cd /git/github.com/LiGoldragon/<dependent>
cargo update -p signal-spirit
cargo check
```

`cargo check` is the gate that proves the source-rewrite was
correct. If it fails, the operator diagnoses + iterates before
moving to the next repo. This step is OPERATOR SESSION ONLY —
deferred from this research.

### §6.7 Step 7 — Witness tests (operator session)

`tests/round_trip.rs` in the renamed crate stays green (rkyv +
NOTA round-trips are name-agnostic). Dependents' boundary +
integration tests must compile cleanly. Per
`skills/architectural-truth-tests.md`, the rename should not
break any invariant test — invariants test the SHAPE, not the
NAME.

### §6.8 Step 8 — Per-repo commits

In each touched repo (upstream first, then each dependent):

```sh
cd /git/github.com/LiGoldragon/signal-spirit
jj st                         # confirm scope per §4.4
jj commit -m 'signal-spirit: rename from signal-persona-spirit'
jj bookmark set main -r @-
jj git push --bookmark main
```

```sh
cd /git/github.com/LiGoldragon/persona
jj st
jj commit -m 'persona: track signal-persona-spirit → signal-spirit'
jj bookmark set main -r @-
jj git push --bookmark main
```

(Repeat per dependent.)

### §6.9 Tally

For ONE signal-* rename, persona-spirit family's current
dependent count:

| Slot | Count |
|---|---|
| Local manifest edits | 1 upstream + ~3 dependents |
| Local source edits | ~30 .rs files |
| Flake edits | 1 upstream + ~3 dependents |
| Flake.lock refreshes | ~3 dependents |
| GitHub rename | 1 `gh repo rename` |
| jj commits | ~7 across ~4 repos |
| Operator verification | `cargo check` × 3, `cargo test` × 3 |

Approximate operator-session effort: 30 minutes mechanical edits
+ ~1 hour verification + per-repo commits. Per-triad cost is
bounded by dependent count, not by mechanics.

## §7 Feasibility verdict

### §7.1 Per-concern verdict table

| Sub-concern | Verdict | Blocker (if any) |
|---|---|---|
| Cargo `[package].name` rename | feasible | none; `package = …` bridge available as fallback |
| Cargo dependent updates | feasible | none; `cargo remove` + `cargo add` or sed |
| Cargo workspace member rename | not load-bearing | no member repos in the rename set |
| Nix flake input rename | feasible | requires coordinated flake.nix + flake.lock refresh per dependent |
| Nix flake.lock node-key change | feasible | `nix flake lock` regenerates cleanly; old node disappears |
| GitHub repo rename | feasible | `gh repo rename` one-call; auto-redirect indefinitely |
| ghq local rename | feasible | plain `mv` + `git remote set-url`; no ghq helper but none needed |
| jj headless commits | feasible | inline `-m '<msg>'` mandatory; verified `ui.editor = "emacsclient -c"` would hang otherwise |
| jj-on-git push to renamed GitHub | feasible | no enforced sign-required ruleset; signing continues to work |
| Source-rewrite tooling | feasible-with-prep | sed/rg combination works but needs care around hyphen vs underscore + substring matches |
| Spirit pilot collision risk | feasible-with-coordination | recommend local-first AND defer signal-persona-spirit rename until after pilot deploy stabilises |

### §7.2 Bottom line

**Feasible-with-prep.** Every mechanical layer (Cargo, Nix,
GitHub, ghq, jj, sed/rg) has a clean path. No tool has a
blocking limitation. The complexity is in the **coordination**,
not in any individual tool. Three recommendations for the
operator-bead epic:

1. **One per-triad rename per bead.** Don't batch multi-triad
   renames; the per-repo commit count alone justifies the
   granularity. Subagent A's topological order names the
   sequence.
2. **Local-first per triad.** Edit + verify locally before
   touching GitHub. The GitHub redirect handles the transition
   window for any external consumer.
3. **Lean post-pilot.** Per the frame's §5 constraint,
   `primary-wdl6` + `primary-x3ci` are deploy-gated; rename work
   that touches signal-persona-spirit should land AFTER the
   pilot stabilises. Other triad renames (e.g.
   signal-persona-orchestrate, signal-persona-router) can land
   in parallel with the pilot since they don't intersect the
   in-flight upgrade flow.

The persona-prefix sweep is mechanically a SEQUENCE of ~25
independent per-triad renames. With local-first + per-bead
granularity + pilot-aware sequencing, none of the ~25 renames
needs special tooling beyond what's verified above.

## See also

- `/home/li/primary/reports/designer/318-upgrade-merger-and-persona-prefix-rename/0-frame-and-method.md` — orchestrator frame for this dispatch.
- `/home/li/primary/reports/designer/317-sema-upgrade-and-macro-convergence-audit/1-sema-upgrade-path-audit.md` — sema-upgrade path audit (input to the upgrade-merger).
- `/home/li/primary/reports/designer/317-sema-upgrade-and-macro-convergence-audit/2-macro-current-state-audit.md` — macro audit (companion sweep).
- `/home/li/primary/skills/jj.md` — jj discipline, headless-commit rule, push cadence, working-copy check.
- `/home/li/primary/skills/component-triad.md` — triad shape, binary-naming table that names the rename targets.
