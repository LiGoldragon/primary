# Tooling and rename implementation plan

Planning only, 2026-09-14. This proposes a concrete write set for an
implementation agent. It does not authorize service/configuration changes,
manifest rewrite, or Cargo rename.

## Direction and current seams

The living asked the audit work to become operational: keep an evidence record
per target with source revision, deployed executable, active configuration,
bounded witness and last living review. Fable recorded the dispatch at
flows/6cc91b/log.md:71-73 and adopted the evidence-record proposal in
flows/6cc91b/reports/audit.md:46-51.

tools/engine-situation is not that record today. It is a Bash code-line/test
counter with five obsolete hard-coded default paths
(tools/engine-situation:1-11,34-97). It has no service, revision,
configuration, witness, or review model.

protocols/repos-manifest.dotos calls itself authoritative and defines positional
Repo records with semantic remote, family, kind, lifecycle, doctrine-home and
flags (protocols/repos-manifest.dotos:1-31). active-repositories says it wins
on membership/status (protocols/active-repositories.md:1-13). Disk cannot
reliably derive those semantic fields.

Authored direction rejects Dotos in favor of Datom, with legacy Dotos frozen
(Vision/datom.md:238-247). Nexus naming says component-nexus and component-meta
(Vision/nexus.md:3-5,41-49).

## Proposed exact write set

1. Add tools/component-evidence as the deterministic evidence generator; preserve tools/engine-situation unchanged as its existing code-shape counter.
2. Add tools/repo-inventory as the disk walker and semantic merge validator; it feeds component-evidence but never itself declares inventory truth.
3. Generate protocols/component-evidence.generated.md and protocols/repo-inventory.unknown.md.
4. Generate/rewrite protocols/repos-manifest.dotos only after validation.
5. Add protocols/repos-manifest.overrides.dotos (or equivalent typed companion) for declared semantic facts. The generator may infer only VCS checkout-root/revision facts and documented doctrine paths; every other missing metadata field remains Unknown in the generated sidecar.
6. Add fixture tests for both new tools, using fixture checkout trees and captured, non-secret systemctl-show output.

This excludes Cargo.toml, component source, unit files, Nix profiles, socket
configuration, private-repo content and generated skill trees. The generators
must be reviewed before any broad Datom/naming migration.

## Evidence record shape

One generated row per canonical manifest repository:

| Field | Acquisition | Output |
| --- | --- | --- |
| canonical repository | manifest plus validated checkout root | name and path |
| source revision | jj log at root | commit id and first line |
| deployed executable | exact named systemd unit, selected show properties | unit, LoadState, ActiveState, SubState, executable path |
| active configuration | selected declared path | path and optional SHA-256 only |
| bounded witness | explicit reviewed evidence reference | source line/date/result or Unknown |
| last living review | explicit override record | id/date/topic or Unknown |

Absent, aliased, masked, remotely owned, or unnamed units render Unknown or
NotObserved; they are never omitted or called undeployed. An active unit proves
only manager state and executable path, not matching source revision or working
behavior. Message demonstrates this distinction
(flows/34d94e/reports/auditMessaging.md:48,65-71).

## No-blind-regenerate rules

1. Enumerate only immediate LiGoldragon checkout entries; never recurse into
   worktrees as independent repositories.
2. Resolve symlinks before identity. datom currently resolves to datom-codec;
   do not emit both as independent repositories. Preserve an alias only when
   the override declares it.
3. Verify checkout root through VCS root discovery; nested crates and detached
   worktrees are not inventory members.
4. Never derive remote ownership, privacy, lifecycle, family or doctrine-home
   from directory names, remotes, README text or recency. Keep an override or
   fail with unresolved candidates.
5. Do not overwrite the manifest until every discovered candidate maps
   one-to-one to a validated semantic record. First emit a sorted candidate
   diff; unknowns fail closed.
6. A remote URL only corroborates an explicit remote override. It cannot create
   or rename an ownership fact.
7. Preserve comments, deprecated records and dispositions. Missing from disk is
   not Deprecated.
8. Read only selected systemd properties and hashed public config paths; never
   print Environment, environment files, config bodies, control keys,
   credentials or unredacted ExecStart arguments.

## Datom migration inventory

A literal `dotos` match occurs in **32 exact Cargo manifest paths**: **4
legacy-package-lineage manifests** and **28 distinct consumer-repository root
manifests**. “28” is a repository count; it is not a count of all exact paths,
and the nested `derive` manifests are included only in the legacy count.

**Legacy package lineage (4 exact paths; package identity/proc-macro identity,
not consumer dependencies):**

- `/git/github.com/LiGoldragon/dotos/Cargo.toml` — package `dotos`.
- `/git/github.com/LiGoldragon/dotos/derive/Cargo.toml` — package `dotos-derive`.
- `/git/github.com/LiGoldragon/nota/Cargo.toml` — also declares package `dotos`.
- `/git/github.com/LiGoldragon/nota/derive/Cargo.toml` — also declares package `dotos-derive`.

The `nota` pair therefore needs identity/ownership review before any rename;
it is not evidence for a second consumer edit.

**Consumer root manifests (27 exact paths): 26 direct `dotos` dependencies plus one transitive named dependency:**

- `/git/github.com/LiGoldragon/agent/Cargo.toml`
- `/git/github.com/LiGoldragon/aggregator/Cargo.toml` — dependency on `dotos-text-query`, not a direct `dotos` dependency.
- `/git/github.com/LiGoldragon/chronos/Cargo.toml`
- `/git/github.com/LiGoldragon/criome/Cargo.toml`
- `/git/github.com/LiGoldragon/dotos-config/Cargo.toml`
- `/git/github.com/LiGoldragon/dotos-text-query/Cargo.toml`
- `/git/github.com/LiGoldragon/mentci-egui/Cargo.toml`
- `/git/github.com/LiGoldragon/meta-signal-agent/Cargo.toml`
- `/git/github.com/LiGoldragon/meta-signal-harness/Cargo.toml`
- `/git/github.com/LiGoldragon/meta-signal-mentci-client/Cargo.toml`
- `/git/github.com/LiGoldragon/meta-signal-mind/Cargo.toml`
- `/git/github.com/LiGoldragon/mind/Cargo.toml`
- `/git/github.com/LiGoldragon/mind-judge/Cargo.toml`
- `/git/github.com/LiGoldragon/relative-age-display/Cargo.toml`
- `/git/github.com/LiGoldragon/router/Cargo.toml`
- `/git/github.com/LiGoldragon/schema/Cargo.toml`
- `/git/github.com/LiGoldragon/schema-language/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-agent/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-frame/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-mentci-client/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-mind-judge/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-orchestrator-judge/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-orchestrator-message/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-sema/Cargo.toml`
- `/git/github.com/LiGoldragon/signal-version-handover/Cargo.toml`
- `/git/github.com/LiGoldragon/system/Cargo.toml`
- `/git/github.com/LiGoldragon/version-projection/Cargo.toml`

**Consumer root manifest with only feature/prose compatibility matches (1 exact
path):**

- `/git/github.com/LiGoldragon/mirror/Cargo.toml` — `dotos-text` feature and
  comments, with `datom-cli` as the dependency; classify separately from a
  direct dependency.

Classify each path further as direct dependency, transitive named dependency, optional feature, package/import compatibility, fixture, or prose before editing. A global
replacement is unsafe: legacy crates require a separate repository/package
transition and feature surfaces can be intentional compatibility boundaries.
The Datom consumer slice must be one locked batch per owning checkout, with
Cargo.lock only where tracked and changed.

## Daemon/meta rename inventory

Current declarations include message-daemon/meta-message, router-daemon/
meta-router, harness-daemon/meta-harness and terminal-daemon/meta-terminal;
orchestrate already has orchestrate-nexus/orchestrate-meta. Candidate manifests:

agent, aggregator, arca, chroma, chronos, cloud, criome, harness, introspect,
listener, lojix/clients/meta, lojix/nexus, message, mind, mirror, orchestrate,
persona, persona-spirit, repository-ledger, router, spirit, system, terminal,
upgrade.

This is inventory, not permission to rename every binary. Safe order:
map each binary to its ordinary/meta socket and signal contract; preserve a
compatibility alias only at an explicit published boundary; rename each paired
component atomically across package, Nix/module references, tests, docs and
callers; run focused checks; record the transition. Missing meta clients are
reported, never fabricated.

## Milestones

1. Lock the new `component-evidence` and `repo-inventory` paths only; retain
   `engine-situation` and create fixture-only generator tests plus candidate
   inventory output.
2. Give both new tools deterministic ordering, Unknown states, redaction,
   symlink canonicalization, and conflict failure.
3. Generate evidence from existing manifest plus overrides and review the diff.
4. Reconcile candidates manually, then regenerate only through the validated
   merge. Keep the dotos extension until the Datom grammar/consumer migration
   is separately approved.
5. Split the 28 consumer-repository transition and daemon/meta renames by
   owner repo, with separate locks, tests, and integration review.

## Sources

- flows/6cc91b/log.md:61-73
- flows/6cc91b/reports/audit.md:21-22,46-51,63
- tools/engine-situation:1-97
- protocols/repos-manifest.dotos:1-31
- protocols/active-repositories.md:1-13
- Vision/datom.md:238-247; Vision/nexus.md:3-5,41-49


## Latest Nexus terminology guard

The latest 2026-09-14 expression names Nexus, core and metaNexus explicitly and
asks the core library to prevent direct signal-actor to Sema-actor communication
(flows/6cc91b/vision/nexus.md:19-25). It is raw/latest direction, not a blanket
binary-renaming rule. Fable's anatomy review must settle how it relates to the
authored component-nexus/component-meta naming before any daemon/meta migration.
Therefore this plan inventories names only and does not mass-rename them.
