# Mind deployment proposal — 2026-07-28

## Decision

Deploy Mind as a `systemd --user` service in the active CriomOS-home minimal
profile. This is the smallest declarative lane that matches Mind's actual
process contract and the already-live Orchestrate and Messenger deployment
pattern. It needs no Ethos dependency, no NixOS system service, no Horizon
role addition, and no change to Mind source.

This is a proposal, not a deployment. No source, state, configuration,
service, deployment, or tracker record was changed while producing it.

## Evidence and scope classification

Wired facts:

- Mind `0.8.0`, main revision `042550a03083`, provides `mind`, `meta-mind`,
  `mind-daemon`, and `mind-write-configuration` from one flake package.
- The daemon takes one generated rkyv configuration-file path. Its writer
  accepts `(ConfigurationWriteRequest <working-socket> <meta-socket>
  <store> <output> [knowledge-judge])`; the daemon itself does not parse
  NOTA.
- The configuration binds working and meta sockets at mode `0600`, has a
  durable database path, and defaults the knowledge judge to `Fixture`.
- The ordinary CLI reads `MIND_SOCKET` and `MIND_ACTOR`; `meta-mind` reads
  `MIND_META_SOCKET`. Development `/tmp` defaults are not suitable as the
  deployed user contract.
- CriomOS-home already deploys Orchestrate and Messenger in profile `min` as
  `systemd --user` services, stores their data under `config.xdg.stateHome`,
  puts sockets under `%t`, packages profile wrappers, and starts them from
  `default.target`.
- The observed host has no `~/.local/state/mind`, Mind unit, Mind sockets, or
  profile executables. This is a fresh state introduction.

Compatibility facts:

- Mind's current store schema is v12. The code opens/migrates v8–v11 stores.
  The v8 test preserves graph rows. A v11 migration intentionally removes
  accepted-knowledge rows before registering the changed domain schema.
- Mind's committed `Cargo.lock`, rather than an Ethos implementation, pins the
  build closure. Relevant locked revisions include `schema-rust` main
  `0f306826f646`, `sema-engine` main `594802575f02`, `signal-mind`
  `1378d5f3c317`, `meta-signal-mind` main `bcb38ce275cb`, and `triad-runtime`
  main `b34df30c56fc`. `Cargo.toml` also carries the compatibility patches for
  `schema` and `schema-cc` revision `4a8aaf1de3aa`.
- The current migration audit explicitly says not to gate Mind or other
  generator consumers on Ethos: current Schema/schema-rust is the required
  compatibility compiler. Ethos remains a separate vertical witness.

## Minimal mutation set

Only `CriomOS-home` needs a source change.

| File | Change |
| --- | --- |
| `flake.nix` | Add a `mind` flake input pinned to Mind `042550a03083103227af1a273a61f9f543793012`; make its `nixpkgs` and `crane` inputs follow CriomOS-home's corresponding inputs. CriomOS-home has no top-level `fenix` input, so leave Mind's own Fenix pin intact. Do not broadly update the lock. |
| `flake.lock` | Add/lock only the new Mind input and its follows. |
| `modules/home/default.nix` | Explicitly import `./profiles/min/mind.nix`, as the sibling profile modules are not auto-imported. |
| `modules/home/profiles/min/mind.nix` | New owner-only user-service module described below. |
| `checks/mind-deployment/default.nix` | New evaluation contract for the module: package/wrapper, writer request, state/runtime locations, `0600` sockets, unit, restart policy, and `default.target` activation. |
| `flake.nix` | Register `mind-deployment` in the existing project checks map. |

There is no need to modify `/git/github.com/LiGoldragon/CriomOS`, Mind,
Schema, Signal, Meta-Signal, or a Horizon schema/release. A home service is
the correct ownership boundary: it belongs to the logged-in user, needs no
network listener or privileged resource, and the existing deployment uses the
same Home Manager surface.

### Proposed module shape

Use the same `size.min` plus boolean enable-option convention as Orchestrate
and Messenger:

```text
options.criomosHome.mind.enable = true

state directory:  ${config.xdg.stateHome}/mind
configuration:    ${config.xdg.stateHome}/mind/mind-daemon.rkyv
database:         ${config.xdg.stateHome}/mind/mind.sema
runtime directory: %t/mind (mode 0700)
working socket:   %t/mind/mind.sock
meta socket:      %t/mind/mind-owner.sock
```

`ExecStartPre` must create the state directory and invoke the package's
writer with exactly:

```text
(ConfigurationWriteRequest <working socket> <meta socket> <database> <configuration>)
```

The service then runs `mind-daemon <configuration>`, has bounded start-limit
settings matching the sibling daemons, `Restart=on-failure`, a short restart
delay, and `WantedBy=default.target`. Do not configure a Mind Judge in this
lane: omission deliberately selects the proven fixture boundary and avoids
turning this deployment into a Mind-Judge/LLM deployment.

The profile package should preserve the package's binaries but wrap:

```text
mind       -> MIND_SOCKET=${XDG_RUNTIME_DIR}/mind/mind.sock
meta-mind  -> MIND_META_SOCKET=${XDG_RUNTIME_DIR}/mind/mind-owner.sock
```

`MIND_ACTOR` should remain caller-selected; hard-coding it in the wrapper
would collapse client identities. The daemon and configuration writer remain
unwrapped and use their generated paths. Both runtime sockets are owner-only
at the component contract and the systemd runtime directory must be `0700`.

## Data, state, and release risks

The greatest risk is not a fresh install: it is a later redeploy against an
unknown old Mind store. There is no Mind state on this host today, so the first
activation creates a new v12 `mind.sema`. If a nonempty state file appears
before activation, stop and require an explicit backup/restore decision:
Mind supports v8–v11, but upgrading v11 intentionally deletes old
accepted-knowledge rows. Never point Mind at Orchestrate's or Messenger's
stores.

Other constraints:

- Pin Mind to the audited `0.8.0` source revision, not an unreviewed moving
  branch. Let its committed Cargo lock preserve the current Schema/Signal/
  Meta-Signal/Sema closure; do not use a broad `flake update` or a Cargo lock
  refresh in this lane.
- A deployment-only addition changes the active home profile's public behavior
  but has no independent CriomOS-home release version surface to bump. Mind's
  own `0.8.0` version does not change.
- The fixture judge makes ordinary work-item and typed-graph operations usable,
  but it is not evidence that live knowledge adjudication is configured. That
  is intentionally out of scope.
- Runtime `%t` sockets disappear with the user session; durable state does
  not. `RuntimeDirectory` avoids stale socket ownership after a restart.

## Required validation and acceptance witness

Before activation, independently evaluate the new CriomOS-home check and the
target home/full-OS configuration with the lojix-materialized inputs. Build
Mind's owner tests at the exact pin, at least `cli-binary`, `daemon-wire`,
`mind-cli-opens-and-queries-work-item-through-daemon`,
`mind-store-survives-process-restart`, and
`mind-meta-cli-reaches-owner-policy-socket`. Evaluation and build are separate
witnesses; neither proves activation.

After an authorized declarative deployment, the live witness is:

1. `mind-daemon.service` is active and the profile resolves `mind`,
   `meta-mind`, and `mind-write-configuration` from the pinned package.
2. `%t/mind/mind.sock` and `%t/mind/mind-owner.sock` exist, are owned by the
   user, and are mode `0600`; no `/tmp` socket is relied upon.
3. With the wrapper and a stated test actor, issue one non-sensitive
   `(Opening Task High [Mind deployment witness] [created by live acceptance])`
   and verify its `OpeningReceipt`; then query `(Query (Open) 10)` and verify
   that exact title.
4. Restart only `mind-daemon.service`, repeat the query, and verify the same
   work item remains. This is the activation-level state-survival witness.
5. Make one owner-socket `meta-mind` request and record the typed reply, which
   distinguishes a live owner endpoint from an unbound socket. Do not claim a
   semantic management feature beyond the reply currently implemented.

Rollback is declarative: remove/disable `criomosHome.mind`, rebuild the prior
home generation, and stop the user service. This removes profile wrappers and
runtime sockets but intentionally leaves `~/.local/state/mind/mind.sema`
untouched. For a bad fresh deployment, preserve that path under a timestamped
backup before any retry; deletion needs separate explicit authorization.

## Coordination and existing work

The implementation touches a shared CriomOS-home checkout. Before editing,
claim the exact five/six paths above through Orchestrate; if any are owned,
request an isolated CriomOS-home worktree rather than editing the shared
checkout. The existing primary rule is to land on main with Jujutsu; no raw
Git workflow is needed. Check the CriomOS-home bead list again immediately
before implementation. This design pass found no Mind deployment bead, no
Mind input/module in the current home flake, and no matching Mind deployment
branch or resumable worktree. The visible Mind worktrees concern judge prompt
work, not deployment; do not resume them for this lane.

## Approval text

> I authorize a narrow, declarative CriomOS-home deployment of Mind 0.8.0 at
> audited revision 042550a03083103227af1a273a61f9f543793012: add only the pinned Mind input, a minimal
> profile-min user service/configuration writer/state path/owner-only socket
> wrappers, and an evaluation check; build and run the stated local live
> acceptance witness, including one disposable Mind record and a service
> restart. Do not alter Mind, Schema/Ethos, Signal/Meta-Signal, Horizon,
> system services, LLM/Mind-Judge configuration, existing data, or unrelated
> lock inputs; if pre-existing Mind state is found, stop for a separate
> backup/migration approval.
