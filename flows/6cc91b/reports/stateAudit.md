# State audit — the components against the living's vision

Flow 6cc91b, subflow, 2026-09-14. Read-only: no edit, no build, no test run, no web.

**Marking.** `[W]` witnessed — I or a delegated reader opened the code, config or
process listing named. `[C]` claimed — a document, log or report asserts it and
I did not re-derive it. Where a claim was checked and failed, it is marked `[C→W
false]`.

**Method.** Repository facts come from `jj log` / `git log` in each checkout under
`/git/github.com/LiGoldragon/`, `find`/`wc` over `*.rs` excluding `.git` and
`target`, `Cargo.toml`, `flake.nix` read but never evaluated. Deployment facts come
from `systemctl list-unit-files` and `list-units` on this host plus the NixOS and
home-manager modules in `CriomOS` / `CriomOS-home`. Vision citations are to
`Vision/<topic>.md`, `flows/*/vision/<topic>.md`, `vision-raw/`, and where no psyche
statement exists that absence is itself reported. Five parallel readers gathered the
per-component facts; every load-bearing number in the ranked list below I re-derived
myself.

## The deployment truth, first

Three of our daemons run on this host `[W]`, and only three unit files for the whole
estate exist here `[W]`:

```
system: lojix.service                 active running "Lojix Nexus"
user:   message-daemon.service        active running "Message (messenger) local messaging daemon"
user:   orchestrate-nexus.service     active running "Orchestrate Nexus path-reservation service"
```

`systemctl list-unit-files` matching `persona|spirit|criome|router` returns nothing at
all on this host `[W]` — the `criome.service` (`CriomOS/modules/nixos/criome.nix:190`),
`persona-router.service` (`CriomOS/modules/nixos/persona-router.nix:133`) and
`spirit.service` (`CriomOS/modules/nixos/spirit.nix:227`) modules exist `[W]` but are not
enabled on this machine. `CriomOS-home/modules/home/profiles/min/message.nix:41` says in
its own comment "No router daemon is deployed" `[W]`. Everything else in this audit —
nexus, signal, sema, protos, datom, ethos-zero, persona, forge, terminal-cell,
triad-runtime, harness — is library or tooling with no unit anywhere `[W]`.

## The table

| Component | Meant to be (vision) | Code: path, size, head | Tests / Nix check | Deployed | Doc vs code | Gap |
|---|---|---|---|---|---|---|
| nexus | "the library that defines the core of a Nexus component"; every component is a Nexus (`Vision/nexus.md`) | `nexus`, 8 rs / 841 lines, v0.5.0, main `c495f2ac` 2026-09-12 "record the store as a file, not as a name" | 22 `#[test]`; `checks.test` = `cargoTest` covers | library only | agrees (configuration + SocketAuthority match) | Library exists; almost nothing is built on it |
| signal | binary rkyv, both sides know the schema, nothing self-labeling (`Vision/signal.md`) | `signal`, 18 rs / 1815 lines, v7.0.0, `bdf6a053` 2026-09-12 | 41 `#[test]`; 9 named checks incl. `test-datom`, `test-transport` | library only | ARCHITECTURE says "the protocol … is to be decided" while `src/exchange.rs` implements one | Protocol shipped ahead of its own doc |
| signal-* / meta-signal-* | exactly two contracts per component (`ARCHITECTURE.md` §0.6) | 39 `signal-*` + 25 `meta-signal-*` repos on disk | per-repo `checks.test` in the active ones | none | 14 `signal-*` have no `meta-signal-*` peer | The two-contract rule holds for 25 of 39 |
| sema | "the database engine of a Nexus, authored in Ethos" (`Vision/sema.md`) | `sema` 3 rs / 581 lines v0.1.1, last real commit 2026-08-13; `sema-engine` 22 rs / 10875 lines v0.16.0 2026-09-12 | sema 22 tests, sema-engine 146; both covered | not a unit; a store format used by other daemons | `sema` untouched a month while `sema-engine` carries the work | The named component is the small one |
| router | signals cross the network through a router (`Vision/nexus.md` §Routing) | `router`, 51 rs / 13725 lines, v0.11.0, `81ee01b1` 2026-09-11 | 54 `#[test]`; `checks.default` + 4 named socket checks | module fused into `persona-router.service`, not enabled here | doc agrees on skim | Substantial code, zero runtime |
| message | "whatever it is called, we should use that for the messaging" (`flows/6cc91b/vision/messenger.md`) | `message`, 28 rs / 2827 lines, v0.12.0, `6a52b9b8` 2026-09-12 | 20 `#[test]`; `checks.default` covers | **running**, user unit | `ARCHITECTURE` names `MessageEngine`/`MessengerTables`/`DeliveryRunner` and they exist | Live, but carries no prompt relay yet |
| signal-message / meta-signal-message | the two contracts for message | 5 rs / 556 and 5 rs / 242 lines, v3.0.0 / v0.6.0 | contract + datom checks | n/a | `signal-message/ARCHITECTURE.md` Code map lists 4 files that do not exist | Doc describes a crate that was replaced by generation |
| messenger-fixture-34d94e | the Codex-built relay fixture | branches in `message` (6 commits, +301/-13, new `src/relay.rs`, `tests/relay_fixture.rs`), `signal-message` (1), `meta-signal-message` (1) | fixture test green per Codex `[C]`; nix check never passed `[C]` | not merged to main in any of the three | n/a | The messenger work is entirely off main |
| criome | takes over the authentication layer of Lojix, root call on the host (`flows/024bc7/vision/criome.md`) | `criome`, 43 rs / 22280 lines, v0.9.1, `e644d251` 2026-09-12 | 102 `#[test]`; `checks.default` + `daemon-skeleton` + `test-dotos-text` | module exists, **not enabled here** | `CriomOS/ARCHITECTURE.md:8` still calls it "sema-ecosystem records validator"; criome's own doc retires that | Big daemon, no live authentication anywhere |
| CriomOS | the declarative system (`SKILL_VARIABLES.md`) | no Rust; flake + modules + ~33 Nix checks, `2985c813` 2026-09-12 | `checks = projectChecks` | is the system | stale criome description (above) | Modules exist for components the host never enables |
| lojix | "it should only be in OS" (`vision-raw/lojixOwnership.md`) | `lojix`, 42 rs / 24744 lines, v4.0.1, `0bb3d66c` 2026-09-11 | 152 `#[test]`; `checks.test` is bare `cargoTest`, `tools/` and `clients/*` tests have no named check `[C]` | **running**, system unit, pinned at `c4bba4fa` = local head | doc agrees on the 5-crate split | Possible untested-by-nix crates |
| orchestrate | "deployed unconditionally, in the home, for every user"; meta binary is part of it (`Vision/orchestrate.md`) | `orchestrate`, 37 rs / 6289 lines, v0.35.0, `9070cbb8` 2026-09-12 | 46 `#[test]`; `checks.test` with `--workspace --all-targets` | **running**, user unit; `orchestrate-meta` built | doc's "three process crates" matches | The one component that matches its vision |
| protos | the shared style, structure only (`Vision/protos.md`) | `protos`, 11 rs / 2438 lines, v0.31.0, `1febca78` 2026-09-12 | 49 `#[test]`; `checks.test` covers | library | **no ARCHITECTURE.md** | Healthy; undocumented and unlisted |
| datom | the notation, library `datom-codec` (`Vision/datom.md`) | `datom` is a symlink to `datom-codec`, 12 rs / 3467 lines, v0.31.0, `09e2a9d5` 2026-09-12 | 45 `#[test]`; `checks.test` covers | library | **no ARCHITECTURE.md** | 30 repos still name the rejected `dotos` |
| ethos | the schema language (`Vision/ethos.md`) | **no `ethos` repo exists**; `ethos-engine` 6 rs / 1601 lines v0.2.0, last commit 2026-08-13 | 3 `#[test]`; `checks.test` covers | none | its own doc self-labels as "wired legacy" | The language's engine is a month cold |
| ethos-zero | the Rust generator (`Vision/ethos.md` §Zero) | `ethos-zero`, 32 rs / 5455 lines, v10.0.0, `4bf73cae` 2026-09-12 | 49 `#[test]`; `test` + `dependency-ethos` + 2 lint checks | build-time only | **no ARCHITECTURE.md** | Rejects `signal-ethos-zero`'s own schema `[C]` |
| persona | the engine-manager, "the root orchestrator" (`ARCHITECTURE.md` §0.7; `flows/6cc91b/notion/persona.md`, a notion) | `persona`, 52 rs / 15455 lines, v0.5.0, `09ee526c` 2026-09-12 | 54 `#[test]`; `checks.default` + ~37 wire checks | fused module, **not enabled here** | 1811-line doc, path cross-check passed on a sample | No `meta-persona` binary despite `meta-signal-persona` |
| forge | no psyche statement found | `forge`, 9 rs / 199 lines, v0.1.0, `6629ce67` 2026-08-13 | **no tests, no `checks` block in flake.nix** | none | doc says "all bodies are `todo!()`" and they are | Honest skeleton; unbuilt, unnamed by the psyche |
| terminal-cell | no psyche statement found | `terminal-cell`, 31 rs / 8012 lines, v3.0.1, `9cab87cc` 2026-09-12 | 37 `#[test]`; `default`, `ownership`, `control-socket-mode` checks | **zero references in CriomOS or CriomOS-home** | doc sample agrees | 8000 lines with no deployment path |
| triad-runtime | the shared daemon concurrency primitive (`ARCHITECTURE.md` §0.6) | `triad-runtime`, 20 rs / 6360 lines, v0.10.1, `8dc6e30b` 2026-09-12 | 55 `#[test]`; `test` + `test-datom` | library, consumed by the daemons | Code map omits `async_runtime.rs` (1723 lines), `reaction.rs`, `workers.rs` | Its listener polls (see gap 2) |
| harness | the Flow Nexus decides system prompt and launch (`Vision/flowNexus.md`) | `harness`, 42 rs / ~11k lines, v0.5.0, 2026-09-12 | 17 test files; `checks` incl. named `flow-id-publication-race` | package only, no unit | doc agrees on `HarnessKind` | Vision wants a Nexus; this is a library plus CLIs |
| flow-id | the tool that names a flow | `/home/li/.nix-profile/bin/flow-id` resolves to `harness-0.3.4` in the store; repo is at v0.5.0 | covered by the harness check | installed in the profile | n/a | **The installed binary is two minor versions behind the source** |
| Curriculum skills | skills live outside the runtime repo so a change causes no rebuild (`Vision/flowNexus.md`) | `Curriculum/skills`, 44 authored `.md`, head 2026-09-13 | no flake in Curriculum; `curriculum-deploy/flake.nix:53` has `checks` | generated trees deployed into workspaces | `CLAUDE.md` names `manifests/*.dotos`; no `manifests/` in the Curriculum root `[W]` | Matches its vision better than most |
| agent-intercom (third party) | "why are you using these agent intercoms?" (`flows/6cc91b/vision/pairedFlows.md`) | `dataforxyz/agent-intercom-{claude,codex,orchestrator,pi}`, TypeScript, 74–123 files each, heads 2026-07-30 to 2026-08-23 | 27–35 `*.test.ts` each | **deployed**: MCP server in `~/.claude.json:2835`, plus an enabled `agent-intercom-fleet-cleanup.timer` | n/a | The living has told this flow to stop using it for Codex |
| paired-flow tools | a durable relay outside the flow directory, six-character match, Codex scripting (`flows/6cc91b/vision/relay.md`) | `flows/024bc7/tools/claude_inject.py` 31 lines, `codex_wake.py` 42 lines, `flows/6cc91b/tools/relay_last_prompt.py` 83 lines, **and `primary/tools/prompt-relay` 100 lines + `prompt-relay.test.mjs`** | prompt-relay has a test file; the Python three have none | run by hand | `flows/6cc91b/log.md` says `primary/tools` holds "all empty directories" — they are five executable files | The durable tool exists; the flow log has not caught up |

## Per component

**nexus.** `Vision/nexus.md` is the most detailed vision document in the workspace and
the `nexus` crate is 841 lines `[W]`. It carries the Configure lifecycle and socket
authority `[W]`, which is the vision's core, but "everything built from now on is a
Nexus, and what was built in another shape is rewritten as one" is not visible in the
dependency graph: `criome`, `message`, `router` and `persona` each build their own
daemon shell on `triad-runtime` rather than on `nexus` `[W]`, and the prior bearing
report already noted nexus "depends on none of protos/datom/ethos" `[C]`.

**signal.** Solid and current `[W]`. The candidate disagreement is worth the psyche's
eye: the doc defers the protocol while the code has one. `Vision/signal.md` also
defers it ("The protocol is to be decided"), so the code is ahead of both.

**The contract family.** 64 contract repos on disk `[W]`. Two are entirely empty
(`signal-domain-criome`, `meta-signal-domain-criome`) `[W]`; five are stubs under 100
lines (`signal-psyche` at 4 lines, `meta-signal-psyche` 19, `signal-forge` 31,
`signal-logos` 82, `signal-ethos` 99) `[W]`; 28 of 63 were last touched between
2026-07-31 and 2026-08-29 `[C, from the family reader]`. Fourteen `signal-*` have no
`meta-signal-*` peer `[W]`: domain, ethos, forge, frame, logos, mind-judge, nomos,
orchestrator-judge, orchestrator-message, sema, sema-storage, sema-translator,
spirit-judge, standard. Four had dirty working copies `[C]`; `signal-sema` is mid
`nota`→`dotos` rename, uncommitted `[C]`.

**sema.** `Vision/sema.md` is one paragraph and the code is split across `sema` (581
lines, cold since 2026-08-13), `sema-engine` (10875 lines, current), `sema-storage`
(905 lines, cold, its own doc calls itself "wired legacy") and `sema-translator` `[W]`.
The workspace `ARCHITECTURE.md` §0.5 draws the today/eventual line at `sema` versus
`Sema` but never explains `sema` versus `sema-engine`, which is the split that actually
exists `[W]`.

**router.** 13725 lines, current, well-checked, and deliberately not deployed `[W]` —
the home module says so in a comment `[W]`. This is the largest built-and-idle
component after criome.

**message.** The live one `[W]`. The living's ruling is that the messaging goes here
(`flows/6cc91b/vision/messenger.md`) `[W]`; the code that would do it sits on
`messenger-fixture-34d94e`, six commits off main, adding `src/relay.rs` and a fixture
test `[C, branch diff read]`. Nothing on main yet relays a prompt.

**criome.** 22280 lines and 102 tests `[W]`, the second-largest component, and no unit
enabled on this host `[W]`. The living's authentication vision
(`flows/6cc91b/vision/agentAuthentication.md`: "authenticated at multiple layers,
sandboxed, and controlled by more highly permissioned nexuses") has a candidate home
here and in `message`'s `provenance.rs` `[C, from the naming report]`, but the layer
between agents today is a Python pty injector `[W]`.

**CriomOS / lojix / orchestrate.** These three are the deployed reality. Lojix is
pinned at its own local head `[W]`, so deployment is not lagging source there.
Orchestrate is the only component whose vision file, code, binaries and running unit
all agree `[W]`.

**protos / datom / ethos-zero.** The healthiest crates in the estate by test density
and recency `[W]` and the least documented: none of the three has an `ARCHITECTURE.md`
`[W]` and none appears in `protocols/repos-manifest.dotos` `[W]`. `ethos` as a repo
does not exist; `ethos-engine` is the crate and it is a month cold `[W]`.

**persona / forge / terminal-cell.** Persona is 15455 lines with a 1811-line
architecture document and no live process `[W]`. Forge is an honest 199-line skeleton
whose doc says so `[W]` — but it has no tests and no `checks` block at all `[W]`.
Terminal-cell is 8012 lines that nothing in the operating system references `[W]`.

**triad-runtime / harness / flow-id.** The shared daemon primitive is real and used
`[W]`. Its `ARCHITECTURE.md` code map omits its own largest file `[W]`. The installed
`flow-id` is from `harness-0.3.4` while the repo is at 0.5.0 `[W]`; what that older
binary does differently is unknown.

**Curriculum, agent-intercom, the paired-flow tools.** Curriculum is 44 authored skills
with deployment through `curriculum-deploy` `[W]`. Agent-intercom is third-party,
genuinely deployed as an MCP server with an enabled cleanup timer `[W]`, and the living
asked on 2026-09-14 what it is doing `[W]`. The relay work has landed: Codex committed
`primary/tools/prompt-relay` (100 lines, Node, three subcommands, provenance
rejection) with a test file, at 07:16 today `[W]`, satisfying "put that tool somewhere
other than in the Flow ID directory" `[W]`.

## The ten largest gaps, ranked

1. **Almost nothing runs.** Three units for an estate of ~90000 lines of component
   Rust `[W]`. Router (13725 lines), criome (22280), persona (15455) and terminal-cell
   (8012) are built, tested and idle. `Vision/nexus.md` describes a graph of nexuses
   joined by contract edges; the deployed graph has three unconnected vertices.
2. **Polling is in the base layer.** `Vision/nexus.md`: "Polling is forbidden; a
   correct system goes quiet when nothing changes." `triad-runtime/src/daemon.rs:392`
   is `thread::sleep(self.listener_poll_interval.duration())` inside
   `serve_next_stream` `[W]` — in the primitive every triad daemon consumes.
   `harness/src/claude.rs:133` is `thread::sleep(self.poll_interval)` with a named
   `ClaudeObservationStrategy::PollingFallback` variant `[W]`.
3. **The messaging the living asked for is off main.** `messenger-fixture-34d94e` is
   unmerged in all three message repos `[C]`, its nix check never passed `[C]`, and no
   prompt-submit hook is configured in either harness `[C]`. The relay in production
   today is `prompt-relay` invoked by hand `[W]`.
4. **The rejected name is still in 30 repos.** `Vision/datom.md` names Dotos rejected
   and Datom the successor. Thirty `Cargo.toml` files still name `dotos` `[W]`,
   including `criome`, `router`, `mirror`, `system` and `mind` — several of which also
   depend on `datom-codec` `[W]`, so they are half-migrated, not merely stale.
5. **The meta tier is incomplete and double-named.** `Vision/nexus.md` says every
   Nexus has a meta socket and "the meta CLI is named component-meta". `orchestrate`
   ships `orchestrate-meta` `[W]`; `router`, `message`, `mind`, `mirror`, `spirit`,
   `system`, `introspect` and `harness` ship `meta-<component>` `[W]`, the form the
   workspace `ARCHITECTURE.md` §0.6 mandates instead. `criome`, `persona` and `upgrade`
   ship **no meta client at all** `[W]` despite each having a `meta-signal-*` repo.
6. **The authoritative repo inventory is not authoritative.** `ARCHITECTURE.md` §3
   calls `protocols/repos-manifest.dotos` "the single source of truth for what repos
   exist". It omits 67 on-disk repos `[W]` — `protos`, `datom`, `datom-codec`,
   `ethos-zero`, `ethos-engine`, `psyche`, `sema-storage`, `sema-translator`,
   `standards` and the whole logos/nomos family among them — and lists 8 that do not
   exist on disk: `schema-next`, `schema-rust-next`, `tree-sitter-schema`,
   `signal-derive`, `nexus-cli`, `persona-pi`, `WebPublish`, `AnaSeahawk-website` `[W]`.
7. **Nothing is written in Ethos yet where the vision says it must be.**
   `Vision/sema.md` requires the Sema root authored in Ethos; `Vision/ethos.md` says
   Ethos "will eventually replace everything". `ethos-engine` has not moved since
   2026-08-13 `[W]`, and the prior bearing report records that `signal-ethos-zero`'s own
   `signal.ethos` is rejected by the current generator `[C]`.
8. **Two very large components have no psyche statement at all.** No `Vision/`,
   `vision-raw/` or `flows/*/vision/` file names `terminal-cell` or `forge` as a subject
   `[W]`; `vision-raw/persona.md` and `vision-raw/hexis.md` are two-line empty shells
   `[W]`. 8211 lines of component code rest on agent-authored architecture documents
   only.
9. **The nexus library is not the base of the nexuses.** `Vision/nexus.md`: "Every
   component built from now on is a Nexus. The nexus repository is the library that
   defines the core." The three running daemons are built on `triad-runtime`, not on
   `nexus` `[W]`.
10. **Deployed tooling drifts from source.** The installed `flow-id` is
    `harness-0.3.4` against a 0.5.0 source `[W]`; `primary/tools/engine-situation`
    defaults to five repository paths of which four (`nota-next`, `schema-next`,
    `schema-rust-next`, `spirit-next`) do not exist `[W]`.

## Stale or contradictory documentation

- `primary/ARCHITECTURE.md` §0.6 mandates `<component>-daemon` for the daemon half,
  while `Vision/nexus.md` says "Nexus is its name; daemon is not" `[W]`. The code obeys
  both in different repos: `orchestrate-nexus` versus `message-daemon`,
  `criome-daemon`, `persona-daemon` `[W]`.
- `primary/ARCHITECTURE.md` §0.6 mandates `meta-<component>` CLIs while
  `Vision/nexus.md` mandates `<component>-meta` `[W]`.
- `primary/ARCHITECTURE.md` §0.6 names "separate repos for `dotos`, `schema-next`, and
  `schema-rust-next`" as the schema-derived stack; two of the three do not exist on
  disk `[W]`, and the estate's actual reader/writer is `protos` + `datom-codec` +
  `ethos-zero`, none of which the file mentions `[W]`.
- `primary/protocols/repos-manifest.dotos` — see gap 6 `[W]`.
- `CriomOS/ARCHITECTURE.md:8` describes criome as the "sema-ecosystem records
  validator"; criome's own `ARCHITECTURE.md` explicitly retires that description `[C]`.
- `signal-message/ARCHITECTURE.md` and `signal-persona/ARCHITECTURE.md` both carry Code
  map sections listing files that do not exist (`src/bootstrap_manifest.rs`,
  `src/schema/lib/behavior.rs`, `tests/interface_contract.rs` and others) `[C, both
  readers quoted the doc and the actual tree]`.
- `triad-runtime/ARCHITECTURE.md` code map omits `src/async_runtime.rs` (1723 lines),
  `src/reaction.rs`, `src/workers.rs`, `tests/reaction.rs` `[C]`.
- `signal/ARCHITECTURE.md` "Evolution": "the protocol … is to be decided" beside an
  implemented exchange protocol in the same file `[C]`.
- `protos`, `datom-codec`, `ethos-zero` have no `ARCHITECTURE.md` at all `[W]`, against
  `primary/ARCHITECTURE.md` §5's rule that permanent docs inline load-bearing claims.
- `primary/CLAUDE.md` refers to `manifests/*.dotos` as the identity/deployment source;
  no `manifests/` directory exists in the Curriculum root `[C]`.
- `flows/6cc91b/log.md` records `primary/tools` as holding "engine-situation,
  jj-branch-queue, nix-local-stack, all empty directories" — all three are executable
  files, and two more (`prompt-relay`, `prompt-relay.test.mjs`) have since landed
  `[C→W false]`.
- `flows/d1c570/reports/codeWitness.md` is accurate where I re-checked it: `protos`
  `1febca78`, `datom-codec` `09e2a9d5`, `ethos-zero` `4bf73cae`, `nexus` main
  `c495f2ac`, `orchestrate` `9070cbb8` all confirmed `[W]`. One of my readers reported
  nexus's head as `f477538d` dated 2026-08-13; I re-read the repo and the `main`
  bookmark is `c495f2ac`, 2026-09-12 `[W]` — the bearing report is right and that
  reading was wrong.

## Unknowns I could not settle

- Whether `lojix`'s `tools/` and `clients/*` tests are exercised by any nix check
  without evaluating the flake (builds forbidden here).
- What `flow-id` 0.3.4 does differently from the 0.5.0 source.
- Whether `persona-router.service` and `spirit.service` run on any other host in the
  estate; I can only witness this one.
- Whether the 14 `signal-*` repos without a `meta-signal-*` peer are the "genuinely
  ownerless components" §0.6 exempts, or a gap. Nothing on disk says which.
- Whether `signal-sema`'s uncommitted `nota`→`dotos` rename is abandoned or in flight.
- Whether the `messenger-fixture-34d94e` branches pass `nix flake check`; Codex reports
  its run was cut off by a 600 s timeout `[C]` and I may not build.
- `criome`'s and `persona`'s missing meta CLIs: whether a meta socket is served by the
  daemon without a client binary. I read the manifests, not the listener code.

## Sources

- `/home/li/primary/ARCHITECTURE.md`, `CLAUDE.md`, `NON_MANAGEMENT_AGENTS.md`,
  `SKILL_VARIABLES.md`, `protocols/repos-manifest.dotos`.
- `/home/li/primary/Vision/{nexus,signal,sema,protos,datom,ethos,orchestrate,flowNexus,highLevelView,remembering}.md`.
- `/home/li/primary/vision-raw/{lojixOwnership,persona,hexis,mentci}.md`.
- `/home/li/primary/flows/6cc91b/vision/*` (12 files), `flows/6cc91b/notion/*` (3 files),
  `flows/6cc91b/log.md`, `flows/024bc7/vision/criome.md`.
- `/home/li/primary/flows/d1c570/reports/{codeWitness,visionInventory}.md` — read as a
  claim and spot-checked, not taken as ground.
- Repository checkouts under `/git/github.com/LiGoldragon/` and
  `/git/github.com/dataforxyz/`: `jj log`, `git log`, `Cargo.toml`, `flake.nix`,
  `ARCHITECTURE.md`, `find`/`grep` over `*.rs`.
- `systemctl list-unit-files` and `list-units` (system and user) on this host.
- `/home/li/primary/tools/{prompt-relay,prompt-relay.test.mjs,engine-situation}`,
  `flows/024bc7/tools/*`, `flows/6cc91b/tools/relay_last_prompt.py`.
- Five parallel read-only readers dispatched from this subflow; their findings are
  marked `[C]` where I did not re-derive them.
