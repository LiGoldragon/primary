# Horizon implementation report

Horizon now exposes the approved generated Datom contract. Separate authored
`HorizonConfiguration` and `ClusterDefinition` inputs compose deterministically
through `horizon-compose` into one public `horizon-definition.datom`; consumers
decode `HorizonDefinition`, resolve the requested `(cluster, node)`, and project
only that selected node. A generic definition being present in the catalogue
does not establish membership.

The producer is released on Horizon main at
`05879e7c1e5f637f78fbe26234b95213c77c59bc`, version **0.6.0**. Remote Nix
checks for the default test package, default package, and `horizon-compose`
package passed at that revision.

The contract splits generic definitions from cluster selection without dropping
the previous domain facts. `Installation` carries persistent disk/layout data;
`Live` retains ordinary keyboard, compressed-swap, network, key, user, domain,
trust, machine, and capability facts. `MachineSpecies::Pod` was source-proven
to mean a VM guest and is migrated to `VirtualMachine`; no Container variant
was introduced. Virtual machines distinguish a cluster host from an authored
external host, and preserve the source-faithful single-hop architecture
inheritance rule. Typed `VmTesting` is distinct from `TestVm`.

Projection behavior retains the audited cluster-qualified empty-domain fallback,
GitHub-ID-to-username fallback, derived builders/caches/keys/user groups and
editor defaults, and opaque secret references rather than public secret values.

CriomOS source consumers are in
`8bbc75d3f2d1ed9a42a5063304083665b03b7c33` on
`horizon-module-consumer-fix-542442`. They read the actual projection directly:
scalar magnitude, lower-camel capability tags, `Wifi4`/`Wifi6`/`Wifi7`,
`fs_type`, `maximum_guests`, and `guest_subnet`; they do not reconstruct the
old proposal shape.

The composition artifact used for materialization is the immutable canonical
child `/nix/store/q8wmy9z7yr0igrbm8kvn3i8icvm4jsdh-horizon-definition/horizon-definition.datom`.
With `(goldragon, ouranos)`, `BaseHost`, and `NoSecrets`, Lojix materialized the
four caller-owned Nix inputs `system`, `horizon`, `deployment`, and `secrets`
and successfully evaluated the resulting CriomOS target. The final coherent
consumer BuildOnly gate is recorded in the Lojix report.

The final paired Lojix consumer is 0.21.0 at
`59293764e02e0fb0ec9251f382e627787420f30d`. Its behavior-complete Datom/Signal
and materialization revision is `d4404aad0d9418e29ebbbc8042c1684276bb3dcd`;
the final child corrects only retained-v4 inspector and public type
documentation. Horizon's producer release and composed artifact contract are
unchanged.

## Recovered version from unlanded commit e9b10780a976 (2026-09-06 05:08 UTC)

#\1 Horizon implementation report

Horizon is released on main as **0.6.0** at
`05879e7c1e5f637f78fbe26234b95213c77c59bc`. It exposes the approved generated
Datom contract: separately authored `HorizonConfiguration` and
`ClusterDefinition` compose deterministically through `horizon-compose` into
one public `horizon-definition.datom`. Consumers decode `HorizonDefinition`,
resolve the requested `(cluster, node)`, and project only that selected node. A
generic catalogue definition does not establish cluster membership.

Goldragon `1f49f8dea50932cacc781d531c48b6d20805b439` owns the composed public
artifact and rendered current Synchronizer configuration. The renderer supplies
its canonical child to the current typed builder selection:
`ClusterRole.{ NixBuilder HorizonDefinition./absolute/horizon-definition.datom }`.
It retains dynamic online-capable NixBuilder selection rather than the temporary
fixed Prometheus host. The external composer remains cluster-neutral at
`7050afef14bcfe649c0d05bdaa681d1577cafc46`.

#\1 Contract and preserved projection behavior

The contract separates generic definitions from cluster selection without
dropping previous domain facts. `Installation` carries persistent disk/layout
data; `Live` retains keyboard, compressed-swap, network, key, user, domain,
trust, machine, and capability facts. Source evidence established that legacy
`MachineSpecies::Pod` meant a VM guest; it is now `VirtualMachine`, and no
Container variant was introduced. Virtual machines distinguish cluster-hosted
and authored external hosts while retaining the source-faithful single-hop
architecture inheritance rule. Typed `VmTesting` remains distinct from guest
identity `TestVm`.

Projection retains the audited cluster-qualified empty-domain fallback,
GitHub-ID-to-username fallback, builder/cache/key derivations, user groups and
editor defaults. Public projection carries opaque secret references only. The
composer and contract coverage include selected graphical and minimal Live
definitions, Installation disks, keyboard/compressed swap, router and backup
Wi-Fi references, VM host KVM availability, users/domains/trust, external and
cluster-hosted VMs, selection/collision rejection, and bounded VM architecture
validation.

#\1 Final Home and OS integration receipts

Home `e71729ec6ebccce9d853227aea549712344a743c` retains the deliberate Codex
membership assertion while evaluating package outpaths one candidate at a time.
It rejects an absent Codex entry and does not turn unrelated unevaluable package
metadata into a false failure. The focused remote assertion derivation
`xpfawyzfb7ji9xpvq89rvi76jcnssf3f-ai-agent-launch-orchestration.drv` completed
with exit code 0.

CriomOS `82f6bf5958f999c97c4d81f985d4ac91bdbc2340` pins that Home revision and
makes its ownership fixture a possible current Horizon projection: local-key
users carry `hasPublicKey`, `publicKeys`, `sshPublicKeys`, and `sshPublicKey`.
The exact resolved graph uses the real four Lojix-generated inputs and the
Home legacy package set selected by that graph. Its isolated ownership
derivation `hbh54ji2adw2r6dfkjs77mhawsbs4kh2-lojix-ownership.drv` completed
remotely with exit code 0 and output
`z7wd79vknmdmyjk2ybrik78lq21i54j4-lojix-ownership`.

A fresh normal Lojix 0.21 BuildOnly request used the canonical public
HorizonDefinition, `(goldragon, ouranos)`, `CompleteHost`, `NoSecrets`, and
CriomOS `82f6…`. Attached session 35743 completed with exit code 0 and
`BootstrapTerminal.Succeeded`; it performed no activation. Its four generated
caller inputs have mode 0700, terminal evidence mode 0600, and its GC root
resolves to
`37gs894wby7b61aj8pq2svq8zgki7lnx-nixos-system-ouranos-26.11.20260813.0e251e2`.
That output derives from
`iwhcfrb2hkqg67s6l28lv560l4aja6cj-nixos-system-ouranos-26.11.20260813.0e251e2.drv`.

The aggregate CriomOS flake check is deliberately not claimed as passing: its
strict unrelated MS2130 kernel-policy stop is tracked by root as
`primary-5pq`. The focused migration checks above ran independently and did not
disable that assertion.

#\1 Remaining combined acceptance

The final C6 VM gate is external-owned and remains pending as of this report
revision. Its latest 4 GiB run passed replay, readiness, and admission but
ended at a durable Eval failure; external is diagnosing the captured VM stderr.
Home and CriomOS main movement remains held until that combined acceptance is
green.

## Recovered from unlanded commits (fe945a stray merge, 2026-10-01)

The final C6 VM gate is external-owned and remains pending as of this report
revision. Its latest 4 GiB run passed replay, readiness, and admission but
ended at a durable Eval failure; external is diagnosing the captured VM stderr.
The source audit attributes that failure to C6's custom daemon service PATH:
it omitted `gitMinimal`, which the production CriomOS Lojix service already
provides. The selected Clavifaber package has the exact locked Kameo Git
dependency, so the fixture correction is limited to that missing tool and a
hash-verified replay of the corresponding pinned Git transport. No Lojix or
production CriomOS runtime contract changes are needed.
Home and CriomOS main movement remains held until that combined acceptance is
green.

## Recovered version from unlanded commit 5245222d8067 (2026-09-06 12:33 UTC)

#\1 Horizon implementation report

Horizon is main **0.6.0** at `05879e7c1e5f637f78fbe26234b95213c77c59bc`.
Its generated Datom contract composes authored `HorizonConfiguration` and
`ClusterDefinition` into one public `horizon-definition.datom`. A consumer
receives that artifact, resolves its requested `(cluster, node)`, and projects
only the selected node.

Goldragon `1f49f8dea50932cacc781d531c48b6d20805b439` owns the composed public
artifact and current Synchronizer configuration. Its builder source is the
current typed form:

```text
ClusterRole.{ NixBuilder HorizonDefinition./absolute/horizon-definition.datom }
```

This keeps dynamic online, capable NixBuilder selection rather than pinning a
specific host. The cluster-neutral composer is
`7050afef14bcfe649c0d05bdaa681d1577cafc46`.

#\1 Contract and behavior retained

The contract separates generic definitions from cluster selection without
losing legacy facts. `Installation` owns persistent disk and layout data;
`Live` retains keyboard, compressed swap, network, key, user, domain, trust,
machine, and capability facts. VM guests are `VirtualMachine`; externally
hosted VMs have an authored external location; cluster-hosted VMs retain the
single-hop architecture inheritance rule. Host capability `VmTesting` remains
distinct from guest capability `TestVm`.

Projection preserves the cluster-qualified empty-domain fallback,
GitHub-ID-to-username fallback, builder/cache and key derivations, user groups,
and editor defaults. The public view carries opaque secret references only.
Producer coverage exercises graphical and minimal Live definitions,
Installation disks, keyboard/compressed swap, router and backup Wi-Fi
references, KVM availability, users/domains/trust, external and cluster-hosted
VMs, generic selection, and invalid host/architecture relationships.

#\1 Final consumer candidate

CriomOS feature `de02ef17a47fd92ae7f38b1c32330a42b6066330` pins Clavifaber
`2203f677d3448d99269d66386d35683cd10a05ef`, the remote-gated current Datom
producer. The OS module writes only `publication.datom` through
`PublicKeyPublicationWriting`; it does not read or rewrite the retired
`publication.dotos`. Its focused remote consumer gate built
`frx1mijxcaj78v7nm7vkiz043ahfypah-clavifaber-publication-request.drv` with
exit code 0, producing
`0ag910lhs9x551a9yyx08nkflqfh36kl-clavifaber-publication-request`. It verified
the generated direct publication record, typed success reply, atomic 0644
file, absent legacy basename, and unchanged second-write hash.

The same candidate adds `gitMinimal` to the production `nix-daemon` service.
The final Ouranos output resolves its generated service unit and includes
`git-minimal-2.55.0/bin` and `sbin` in the effective daemon `PATH`. This fixes
the real cold-Git prerequisite discovered by C6 without changing its admission
or replay policy.

The exact four-input ownership graph evaluates to the already remote-passed
`hbh54ji2adw2r6dfkjs77mhawsbs4kh2-lojix-ownership.drv`; exact derivation
identity transfers its exit-0 result and output
`z7wd79vknmdmyjk2ybrik78lq21i54j4-lojix-ownership`.

Both fresh materializations invoke immutable Lojix
`7e29c37f51092e5a20abf88c670aabd2acee6e52#lojix-bootstrap`, rather than the
host's separately installed 0.20.3 binary. They use BuildOnly, NoSecrets, new
caller-owned private journal parents, fresh GC roots, and fresh terminal paths;
there is no activation.

| Target | Shape | Public definition | Result derivation | Output |
| --- | --- | --- | --- | --- |
| `(fieldlab, mercury)` | `BaseHost` | `/nix/store/rc2g6rxn05qi92x42s1sjdppbpsl01r0-horizon-definition/horizon-definition.datom` (SHA-256 `ed4ff2d23b87cf4f07bf928a7c7734d478e8a38cd709be59db972a6e3ccacd22`) | `/nix/store/bix0y5slnhh16ggc6gp9qlyb5xlln9gp-nixos-system-mercury-26.11.20260813.0e251e2.drv` | `/nix/store/yjbywpb126djjpq8h56hbax58f3gi55l-nixos-system-mercury-26.11.20260813.0e251e2` |
| `(goldragon, ouranos)` | `CompleteHost` | `/nix/store/0in67wflv4rxnylf4hbpdmni3m5as4sl-horizon-definition/horizon-definition.datom` (SHA-256 `eac13fa803fa8db358dfd03fc9a7c1a74bca27970b37008be4eccc9873322947`) | `/nix/store/9fdvm7zkyqkqmawas11lxyksyz6fnjg0-nixos-system-ouranos-26.11.20260813.0e251e2.drv` | `/nix/store/z5hhwav5zw1ia8k9ajhpmqmqbdzd9ly3-nixos-system-ouranos-26.11.20260813.0e251e2` |

Both commands returned exit code 0 and `BootstrapTerminal.Succeeded`. Their
four generated `system`, `horizon`, `deployment`, and `secrets` directories are
mode 0700; terminal evidence is mode 0600. The Mercury journal and terminal
SHA-256 values are `37d87cd51a62c4794e7d0bec1ba17b65554669f9eee524103240764ecf729d54`
and `57a54338cbe8b5f8d384111138d1ccc0d0b2ba35b7021e9841464f055004e2e9`.
The Ouranos values are
`c1a53a76c1985850082b7a3fc3df10b6e7714790995eb05223bb1f791847072b` and
`8c87499d4e79bf8df8cc74a3c7560d43d6fb731e35c97397c45a06d1e6c6cdaf`.

CriomOS source metadata for C6 is `de02ef17a47fd92ae7f38b1c32330a42b6066330`,
`lastModified=1788675700`, and
`narHash=sha256-H4TR3gal5vXxLy9vdmyuS580I8liV9uccTU570WRb1Q=`.

#\1 Gate boundary

The aggregate CriomOS check is not claimed passed. Its unrelated strict MS2130
kernel-review assertion remains tracked as `primary-5pq`; focused migration
checks were run independently without disabling that assertion.

C6 is external-owned and remains pending at this record revision. Home and
CriomOS main movement remains held until its final combined VM acceptance is
green. No source change, activation, or live-store action is implied by this
record.
