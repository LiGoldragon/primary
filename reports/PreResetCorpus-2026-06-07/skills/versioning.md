# Skill — versioning

*Keep component versions truthful when code behavior changes.*

## What this skill is for

Use this skill whenever an agent changes code, generated code,
wire contracts, storage schemas, package metadata, deployment
wrappers, or logic that affects a running component.

The purpose is traceability. A running binary that still says
`0.3.0` after a week of behavioral changes is lying to every
agent, report, test, and deployment wrapper that tries to reason
about it.

## The rule

Every code or logic change that changes component behavior bumps
that component's version in the same change set.

Do not leave version bumps as a later cleanup. The version bump is
part of the implementation.

## Semver discipline before 1.0

Use `major.minor.patch`.

- **Patch bump** (`0.3.0` -> `0.3.1`) for compatible bug fixes,
  internal logic changes, behavior corrections, and non-breaking
  implementation improvements.
- **Minor bump** (`0.3.x` -> `0.4.0`) for new operation roots, new
  public behavior, new wire fields with compatibility decoding, new
  deploy slots, or storage migrations that remain forward-managed.
- **Major bump** only when a component has crossed the 1.0 line.
  Before 1.0, breaking public changes bump the minor version at
  minimum and get called out explicitly in the commit/report.
- **A major bump requires explicit psyche authorization.** Crossing
  to `1.0`, and every later first-digit bump, is the psyche's call.
  An agent may *propose* a major bump in a report or commit message
  with the reasoning, but must get the psyche's go before making it.
  Patch and minor bumps an agent makes on its own as part of the
  change; major is reserved.

If a change only edits reports, skills, comments, or prose docs,
do not bump a component version unless that prose is packaged as
the component's runtime-visible help or public documentation
surface.

## Distinguish the version surfaces

Do not blur these into one word:

- **Component release version** — the package/binary version
  users and wrappers see.
- **Wire contract version** — the signal contract crate's semver
  and any protocol handshake value.
- **Storage schema version** — the redb/rkyv schema guard and
  migration ladder.
- **Deployment slot version** — the versioned wrapper or Home/Nix
  profile slot the unsuffixed command points at.

When one surface changes, bump that surface. When a daemon consumes
a changed signal contract, bump the daemon too.

## Where to bump

For Rust components, start with `Cargo.toml` package versions in
the changed daemon/CLI crate and every changed signal contract
crate. If the crate exposes `--version` or a versioned binary name,
make sure that surface reads from the bumped version.

For Nix-packaged tools, update any Nix package version, flake input
name, versioned wrapper, or slot mapping that intentionally names
the old version. Update downstream `flake.lock` files when the
component is consumed through a flake input.

For storage changes, update the schema-version guard and add the
migration step in the same change.

## Commit and report discipline

The commit message names the version move:

```text
persona-spirit: bump to 0.3.1 for privacy-filter fixes
```

If the version bump spans repos, the report or final status lists
each repo and each old -> new version.

Never report branch work as deployed. A version is:

- **implemented** when source and tests are on the branch;
- **landed** when it is on main;
- **available** when the package can be built from the pin;
- **deployed** only when the running profile or service points at
  the new version.

## Final check

Before finishing a code change:

- inspect the package metadata that carries the component version;
- run the relevant tests;
- if a binary exists, verify the built or live version surface;
- update downstream locks when the changed component is consumed by
  another repo;
- say clearly whether the version is only landed or also deployed.

If version semantics are unclear, ask the psyche. Do not silently
choose between patch, minor, wire, storage, or deploy-slot versions.

## See also

- this workspace's `skills/operator.md` — implementation ownership.
- this workspace's `skills/system-operator.md` — deploy and profile
  activation.
- this workspace's `skills/contract-repo.md` — wire-contract semver.
- this workspace's `skills/rust/storage-and-wire.md` — storage schema
  guards and migrations.
- this workspace's `skills/nix-discipline.md` — flake and lock hygiene.
