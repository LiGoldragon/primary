# Skill — nix discipline

*Choosing flake-input forms, pinning, store-path hygiene, and
when to reach for `nix run` vs `cargo install`.*

---

## What this skill is for

When you're editing a `flake.nix`, choosing how to declare an
input, debugging a stale lock, or deciding how to invoke a
tool that isn't on `PATH`, this skill says what the workspace
does. The CLI reference for nix commands lives in lore (see
`lore/nix/basic-usage.md`, `lore/nix/flakes.md`,
`lore/nix/integration-tests.md`, `lore/rust/nix-packaging.md`);
this skill is about the *discipline* — which input form to
pick, which command shape, which test runner — and the why
behind each.

---

## Flake inputs — choosing the form

**Default: `github:<owner>/<repo>`.** The github form is what
should be committed to `flake.nix` for any sibling repo you
consume.

```nix
inputs.nota-codec.url = "github:LiGoldragon/nota-codec";
inputs.persona-wezterm.url = "github:LiGoldragon/persona-wezterm";
```

The github form is **portable** (any machine resolves it
identically), **reproducible** (the lock pins to a commit,
not a working-tree state), and **survives history** (if the
machine that committed the flake disappears, the input still
resolves).

### Don't use `git+file://`

Symptom: `inputs.foo.url = "git+file:///git/github.com/<owner>/<repo>"`.

`git+file://` points at a **local checkout** on the machine
that wrote the flake. The committed flake then references a
path that doesn't exist on any other machine, and behaves
silently differently depending on whether the local checkout
has uncommitted changes. Two consequences:

- The flake stops being reproducible across machines (the URL
  resolves to a different working tree on every host that has
  one, and to nothing on the rest).
- The flake's history loses its meaning — you can no longer
  tell what version of the dependency was used at any given
  commit, because `git+file://` doesn't pin the dep's commit
  in `flake.lock` the same way `github:` does.

**Don't commit `git+file://` inputs.** If you need to point at
a local clone for fast iteration, use the **CLI override**
pattern (below); leave the committed flake on `github:`.

### Iterating against a local clone — `--override-input`

Use `nix flake lock --override-input <name> path:<local-path>`
to temporarily point a `github:` input at a local clone:

```sh
nix flake lock --override-input nota-codec path:/git/github.com/LiGoldragon/nota-codec
```

This rewrites the `nota-codec` entry in `flake.lock` while the
committed `flake.nix` still says
`github:LiGoldragon/nota-codec`. Verify by inspecting
`flake.lock` (look at the `locked` block under the input).

When iteration is done, commit and push the dependency repo,
then run `nix flake update nota-codec` to re-pin the lock to
the new commit. The `flake.nix` never changes.

### `path:` is fine for sub-flakes inside one repo

If a repo contains a `subdir/flake.nix` and the parent's flake
consumes it, `path:` is the right form:

```nix
inputs.subflake.url = "path:./subdir";
```

`path:` here is a within-repo reference — it doesn't depend on
a particular machine's filesystem layout, only on the repo's
own structure.

### `flake = false` is for non-flake sources

```nix
inputs.some-source = {
  url = "github:<owner>/<repo>";
  flake = false;
};
```

Use this when consuming a repo that doesn't have a `flake.nix`
of its own — typically because you only need the source tree
(for `import` or for a build script). If the input *does* have
a `flake.nix`, leave `flake = false` off; you want its outputs.

### Summary table

| Form | When | Notes |
|---|---|---|
| `github:<owner>/<repo>` | **Default** for sibling-repo deps | Portable, reproducible, history-stable. |
| `github:<owner>/<repo>?ref=<branch>` | Track a non-default branch | Re-pinned by `nix flake update`. |
| `path:./subdir` | Sub-flake inside the same repo | Within-repo only. |
| `git+ssh://`, `git+https://` | Repos not on github | Same shape as `github:` but explicit transport. |
| `git+file:///...` | **Forbidden** in committed flakes | Use `--override-input path:...` for local iteration instead. |

---

## Lock-side pinning

Keep `flake.nix` generic; record the exact rev in
`flake.lock`. **Never write a hash into `flake.nix`.**

```nix
# flake.nix — generic, no hash
inputs.nixpkgs.url = "github:NixOS/nixpkgs?ref=nixos-unstable";
```

```sh
# flake.lock pinning happens via the CLI
nix flake lock --override-input nixpkgs github:<org>/nixpkgs/<rev>
```

The lock file is **machine-generated**; never hand-edit it.
`nix flake update` re-pins to upstream's latest; targeted
re-pinning happens through `--override-input`.

To reuse a rev another flake already pins, use
`--inputs-from`:

```sh
nix flake lock --inputs-from path:/path/to/sibling-flake
```

This resolves any matching inputs using the sibling's locked
entries — no hash typed by hand.

---

## Don't reference raw `/nix/store/<hash>-<name>` paths

Store hashes change on every rebuild. Any recorded path
becomes stale within minutes. They're long, noisy, and
silently wrong by tomorrow.

In commands and output:

- When naming a binary, use the plain name (`dolt`, `bd`, `jq`)
  or the profile path
  (`~/.nix-profile/bin/dolt`, `/etc/profiles/per-user/li/bin/...`)
  — **never** the resolved `/nix/store/...` path.
- When tool output (`ps`, `env`, `ls`) contains store paths,
  don't quote them back in text. Refer to the thing by package
  name.
- If a store path is genuinely load-bearing for the point being
  made ("two different `dolt` versions are coexisting"), say so
  explicitly — don't paste the hash and call it documentation.

In commit messages, prose docs, and reports:

- Same rule. A `/nix/store/abc123...-foo` literal in a commit
  message freezes one build's hash into the history forever;
  the next build's hash drifts and the commit message reads as
  archaeological junk.
- Capture in shell variables when a store path is needed for
  a one-shot operation:

```sh
result=$(nix build .#some-output --print-out-paths --no-link)
echo "$result"          # use the variable
ls "$result"/bin
# the value is local to this shell; nothing freezes into
# git history or chat logs.
```

---

## Use `nix run nixpkgs#<pkg>` for missing tools

When a tool isn't on `PATH` (`rustfmt`, `clippy`, `jq`,
`ripgrep`, etc.), invoke it via Nix:

```sh
nix run nixpkgs#<package> -- <args>
```

**Don't reach for** `cargo install`, `pip install`,
`npm install -g`, distro package managers, or hand-written
shell substitutes. The setup is Nix-managed end-to-end;
out-of-Nix installs pollute the environment, are
non-reproducible, and bypass the system's invariants.

- First call to a missing tool: `nix run nixpkgs#<pkg> -- <args>`.
- Repeat use in a session: the same command works fine — Nix
  caches the build.
- Reserve writing a script substitute for cases where no
  upstream tool exists.
- Don't fall back to a bespoke Python/sed/awk substitute "for
  speed" while you wait for nix to fetch — it's almost always
  faster than the rebuild + debug cycle of a hand-rolled
  substitute.

For one-shot invocations of a Nix-built tool from this
workspace's flake outputs, prefer `nix run .#<attr> -- <args>`.
Reach for `nix build` only when the store path itself is
load-bearing (closure introspection, `nix copy`, etc.) — and
even then, capture the path in a shell variable.

---

## `nix flake check` is the canonical pre-commit runner

Every Rust crate (and ideally every flake) exposes its test
suite as `checks.default`. **Always use `nix flake check` as
the canonical pre-commit test runner**, not bare `cargo test`.

Why:

- Pins the toolchain to the flake's `fenix` component — no
  host-rustc drift.
- Resolves dependencies from the committed `Cargo.lock` /
  `flake.lock` — no "works on my machine" gaps.
- Makes the test invocation self-documenting: any Nix checkout
  reproduces the exact suite.

`cargo test` alone skips the reproducibility guarantees. Use
it during a tight inner loop if you must, but treat
`nix flake check` as the gate before pushing.

For the canonical flake layout (crane + fenix + layered
cargo-deps caching), see lore's `rust/nix-packaging.md`.

---

## Don't hand-edit `flake.lock`

`flake.lock` is machine-generated. Hand edits drift silently;
the next `nix flake lock` overwrites them.

If a lock entry is wrong:

- `nix flake update` — re-resolve all inputs.
- `nix flake update <input>` — re-resolve one input.
- `nix flake lock --override-input <name> <url>` — pin one
  input to a specific URL/rev.

Commit `flake.lock` after any of these. The commit message
should name what changed
(`update nota-codec to <short-sha>`).

---

## See also

- lore's `nix/basic-usage.md` — Nix CLI reference (commands,
  flags, blueprint folder map).
- lore's `nix/flakes.md` — inputs and locks reference.
- lore's `nix/integration-tests.md` — chained-derivation
  patterns for daemon-stack tests.
- lore's `rust/nix-packaging.md` — canonical crane + fenix
  flake layout for Rust crates.
- lore's `rust/testing.md` — `nix flake check` as the test
  runner; `CARGO_BIN_EXE_*` for two-process integration tests.
- this workspace's `skills/jj.md` — push before
  building (so the input is reachable from the lock).
- this workspace's `skills/skill-editor.md` — how skills are
  written and cross-referenced.
