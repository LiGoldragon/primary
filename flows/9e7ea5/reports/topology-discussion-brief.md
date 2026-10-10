# Mind architecture brief for the topology discussion

Prepared for Field Medium 9ddcbc and Psyche Medium b81560 or its verified
successor. This is an evidence review and discussion proposal, not Vision,
deployment approval, or a report of new tests. No network changes, builds,
virtual machines, service restarts, or production activations were performed.

## Mind stack and continuity

The retained read-only inventory observed Mind high **9e7ea5**, native
`01a0bcea-a838-7421-ab1d-43c9e7ea522d`, Astra/medium, HM
`mind-astra-of-98ac2e`, at `messaging-build / wM:p1 /
term_65be21c518a7932`. Its earlier context, identity, route and acceptance
receipts are retained. Ownership stays here; 98ac2e and 0ab019 remain crossovers.

No live Mind low or ultra-low was found. Prepared profiles under
`flows/395aed/refresh-production/` specify `mind-terra` (Terra/medium) and
`mind-luna` (Luna/medium). No Mind medium binding or approved profile was
established by this inventory. Field9ddcbc explicitly accepted execution ownership
for missing low/ultra-low seats and will resolve medium's model/profile first.
Its acknowledgement is not a completed launch or readiness receipt. The full
batch manifest must not be rerun because it includes existing seats. Each new
seat still requires Herdr-first binding, native context/profile receipt,
tool/identity witness, exact HM marker/read acknowledgement, role acceptance,
and continuity. No retirement follows. Current context percentage is unmeasured.

Psyche Medium b81560 was observed at `messaging-build / wD:p1 /
term_65bc6f440281c22`, native `b8156034-b845-43c4-890a-49a73d806ee1`,
Opus 4.6[1m]/medium, HM `opus-of-b05237`. No verified young successor was found
in that observation. Coordination requests were submitted to b81560 and Field.

Messaging writer f72ab7 remains retained through 0ab019. Published checkpoint
`8a6e88ff183cfd6d1e952b661af5f1a407df7ba9` is an untested, in-memory gate that
starts open. It is not a durable refresh-delivery gate. Locks 2836/2862/2864
were last observed owned by f72ab7; current ownership must be reobserved before
writes. No duplicate writer or replacement work has been assigned.

## Architecture and evidence boundaries

**Source implementation inspected by the read-only companion:** CriomOS is
the network-neutral NixOS system surface; Lojix projects Horizon, system,
deployment and secret inputs into its target. CriomOS-home owns user/desktop
configuration. TestVm roles and VmHost capabilities produce QEMU/KVM microVMs
with dedicated taps, guest addresses, capacity checks and on-demand systemd
units. TestVm guests suppress desktop/Home weight unless explicitly requested.
This establishes available code, not that a current host has activated it.

**Historical isolated VM evidence:** the CriomosImplementer v3 witness records
two fresh two-node NixOS/QEMU test runs on Prometheus on 2026-06-29 at 09:22:43Z
and 09:26:20Z, test-cluster revision
`b0b309511a7909a6f80918c9572afaa2db0a3a6`. Six services were active;
node-a reached node-b router TCP7440. Unknown identities/foreign signatures
were refused; a registered matching-key body was accepted into the peer mirror
and rehashed. The receipt explicitly excludes a production switch or host
service/network mutation. These are QEMU/KVM receipts; no Oracle VirtualBox
evidence was found. Passing that historical revision does not validate today's
source graph, deployed network or newer Message/Lojix contracts.

**Historical production evidence:** the 2026-08-03 Spirit recovery receipt
reports user-environment activation on ouranos, recovery from start-limit-hit,
two active Spirit services and three listening sockets. Its scope explicitly
excludes production write, corpus read, database restore and restart tests.
Other field-preparation evidence records an admitted Home Build without an
observable execution result and a mismatch in projected builder features.
Current reachability, daemon-fetch recovery and production service health are
not established by these historical receipts.

Inspected source parents: CriomOS `d8c765dbd1192bdeedd11b357d3888296992396f`,
Home `7721387e482ae1b63ec0270d7db42a691e1d11a8`, Horizon
`8c11dfaa19accda0e1d0d8708542a13ed788ea0a`. These are source anchors, not
activation revisions. The August recovery instead names CriomOS
`e658bf55bb0f06af012c8edf429d519c3b238c93`, Home
`d2d02bb61eb3557594b2c302e2862e5e0f58fb86`, and Spirit
`eabe6c6d96112b46d15443e1c1a29d940605785f`.

## Feasibility and the smallest next experiments

Temporary virtual nodes have an existing implementation path, conditional on
the selected host's actual KVM, builder features, capacity, addresses and
reservation. Use a fresh isolated pair, with separate guest state and no
production credentials or routes. Preserve existing persistent test guests.

| Question | Proposed isolated witness |
| --- | --- |
| Can two nodes communicate? | Guest shell access, both-direction IP/TCP reachability, then the actual typed protocol request/reply and durable peer result. A ping or listening socket alone is insufficient. |
| Are versions compatible? | Pin both node closures/contracts; test same-version and intended upgrade sequence, including explicit mismatch rejection and durable-state migration. |
| Is a service live? | Check systemd state, dependency/socket state and a successful bounded request; include a failed service and recovery inside the disposable guests. |
| What happens during failure? | In guest-only tests, stop the exact owned service or isolate the guest link; observe timeout, durable pending state, restart/recovery and duplicate handling. |
| Does activation finish? | Record build, realization, admission, activation and observed running version separately; retain partial-activation failures. |
| Can the living access it? | Demonstrate the intended shell/service endpoint and its authorization boundary on the chosen test node; do not infer access from deployment admission. |
| Is cleanup complete? | Stop only the named owned guest; verify process, socket, route and disk disposition against the declared temporary-node lifecycle. |

No experiment above has been run by this flow. Production testing requires a
separately selected target and authorized action; this relay permits neither
network mutation nor production activation.

## Patterns and naming hypotheses

Strong patterns in the inspected source/evidence: capability/role projection,
immutable inputs, explicit deployment stages, isolated guest state, typed
ordinary/meta contracts, negative-path protocol tests and independent live
acceptance. Weak boundaries: builder-feature truth differs between projection
and module evaluation; admission can lack an observable final outcome;
temporary and persistent guest lifecycle expectations are mixed; Horizon's
configuration-versus-Nexus identity remains a design question.

For discussion only: keep node identity, capability, role, deployment intent
and observed health as distinct types. Names such as `NodeCapability.VmHost`,
`NodeRole.TestVm`, `DeploymentIntent`, `ActivationReceipt`, `Reachability` and
`ServiceHealth` could make those boundaries clearer. A receipt should name the
exact revision/binding and observation boundary, not encode a universal boolean
"ready". Whether these belong in Ethos, generated Rust, or typed Nix projection
is an open design question. Ethos source/generation direction is not proof of
a production Ethos runtime. These hypotheses have not been adopted by the living.

## Sources

- Existing native children `/root/messaging_bounded_check` and `/root/native_ack`:
  read-only live binding and architecture investigations in this turn. Their
  reports are attributed evidence; this root did not rerun their probes/tests.
- `flows/f38926/log.md`: retained Mind readiness and transfer record.
- `tools/native-seat-launch.mjs`, `tools/native-batch-refresh.mjs`: directly read
  canonical launcher gates; not a new successful launch witness.
- `flows/395aed/refresh-production/manifest.json`, `mind-terra.json`,
  `mind-luna.json`: prepared profiles, not runtime readiness.
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`, `modules/nixos/test-vm-host.nix`,
  `modules/nixos/test-vm-guest.nix`, `checks/lojix-nexus-start/default.nix`,
  `UPGRADES.md`: implementation and documented upgrade boundaries.
- `agent-outputs/CriomeAuthWitnessFullBody/CriomosImplementer-WitnessRunEvidence-v3.md`:
  historical isolated two-node VM execution receipt.
- `agent-outputs/SpiritArchitectureAudit/Recovery-Activation-Evidence-2026-08-03.md`:
  historical production recovery receipt and its explicit exclusions.
- `agent-outputs/FieldReadiness/OperatingSystemImplementer-VmFieldPrepEvidence.md`:
  builder-feature and observability limitations, with historical scope.
- `Vision/horizon.md`, `Vision/ethos.md`, their `Vision/sources/` records,
  `vision-raw/worldModelBeforeCode.md` (2026-08-20/21): design context, not
  activation evidence. Horizon source record attributes f38926/b81560; source
  modification dates were not treated as dates of the living's statements.
- Corrected predecessor handoff45db and this flow's delta6b48a6d6; subsequent
  writer/crossover checkpoint receipts and current living relay via Field9ddcbc.
