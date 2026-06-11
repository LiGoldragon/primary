# Spirit deploy — system-operator handoff

The whole Spirit redesign is implemented and cargo-verified on `origin/main` (`9ed144d0`).
The design work is done; what remains is two **system-operator** steps to get the daemon
actually running it. This report names *what* must happen and the acceptance criteria;
*how* (the Nix/OS/CriomOS mechanics) is system-operator's lane. Designer does not touch
deploy files.

## Where things stand

- **Implemented:** universal vocabulary, the nested `Technology = Hardware + Software`
  taxonomy with equivalence relations, scopes, the guardian (gate + separate decision-log
  journal + live-tested judgment + equivalence-expanded retrieval), referent registry, and
  the store migration — all on `origin/main` `9ed144d0`, green across cargo feature sets and
  the live DeepSeek guardian suite.
- **Deployed (live) is far behind:** the user service `spirit-daemon.service` runs `9055609`
  (v0.8.1), on the **old 24-area vocabulary**, holding ~1398 records under
  `~/.local/state/spirit/`.

So this is a version upgrade of an existing deployed user-service, `9055609 → 9ed144d0`,
**plus a mandatory store migration** (the schema changed).

## Step 1 — get the Nix build green (current blocker)

`nix build .#default` failed twice on the remote builder (Prometheus) with an **external DNS
failure** — it could not resolve `github.com` while fetching `nota-next`. cargo is green
across every feature set; this is infra, not code.

- **Likely transient** — retry first.
- **If it persists:** the remote builder's DNS/network, or ensure the `nota-next` flake input
  is fetchable/substitutable on the builder.
- **Acceptance:** `nix build .#default` green **and** the flake checks green (the hermetic
  witnesses, incl. `nix_integration`). cargo-green ≠ Nix-green — the hermetic build is the
  real gate.

## Step 2 — deploy + store migration

### 2a. Pin and build

Bump the `spirit` input in the CriomOS-home flake to `9ed144d0` (and the toolchain inputs it
needs — `schema-next` `7c5f6880`, `schema-rust-next` `815124b2`, `nota-next` — to compatible
revisions), rebuild, activate the new `spirit-daemon`.

### 2b. The migration is mandatory — and touches the whole store

The `Domain` enum changed shape (Software branch added then nested under Technology, Craft
software-leaves evicted, `Technology(Intelligence)` removed). Because records are
**rkyv-archived with the Domain type**, the new daemon **cannot read the old `.sema` store
directly** — every one of the ~1398 records must pass through the version migration to be
re-encoded. (The *domain-value* re-tag is tiny — ~2 records change value — but the *re-encode*
is whole-store.) `production_migration.rs` is the tool (two-submodule historical→current
pattern); whether it runs automatically on daemon start or as a separate helper invocation is
in the packaging — confirm from the build.

- **Back up `~/.local/state/spirit/*.sema` before migrating.** This is the irreversible step.
- Run / trigger the store upgrade migration against the live store.
- **Acceptance:**
  - record count still **1398** (no loss),
  - `spirit Version` reports the new version,
  - a former `(Craft Architecture)` record now reads the nested path
    `(Technology Software Engineering SoftwareArchitecture)`,
  - ordinary `Observe`/`Lookup` works against the migrated store.

### 2c. Daemon mechanics (unchanged)

The daemon takes **one binary rkyv `SpiritDaemonConfiguration`** (built by the
`spirit-write-configuration` helper from typed NOTA — never inline NOTA/flags), requires a
meta socket, and **self-resumes from persisted SEMA on restart**.

## Consideration — the guardian needs the agent daemon

Guardian-gated writes (`Propose`/`Clarify`/`Supersede`/`Retire`/referent registration) call
the **agent daemon → DeepSeek**. For those to function, the agent daemon must be up with its
provider + key configured on its **meta socket** (`SecretSource::gopass
platform.deepseek.com/api-key`, the in-flight secrets thread). Without it, gated writes
**fail-closed**; raw `Record` writes bypass the guardian. Decide whether this deploy brings up
the configured agent daemon too, or ships spirit first with the guardian path dormant.

## Smoke test (post-deploy)

```
spirit Version                     # new version
spirit "(Count (Any Any Any Any None Any (AtLeastCertainty Minimum) Any))"   # ~1398
spirit "(Lookup <a former Craft-software record>)"   # nested Technology(...) domain
# if agent daemon configured: a gated Propose returns a GuardianVerdict
```

## Sequencing

Step 1 gates step 2 (no green build, no deploy). The agent-daemon/guardian config (the
secrets thread) can land in parallel or just after. Nothing here is designer-owned; this is
the system-operator (and, for the agent key config, operator/system-operator) pickup.
