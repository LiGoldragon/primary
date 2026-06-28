# Criome-auth integration base — implementation evidence

Task: the integration + trust-anchor step from
`reports/capacityAdmissionSlice/6-Translation-criome-auth-witness-vm-test.md`.
Produce one coherent, audit-gated integrated base (criome distinct identities +
persona-router real criome attestation + CriomOS modules) that BUILDS, ready for
the two-VM witness test (T4) to be written on top. Distinct criome identities
chosen by the psyche over a shared cluster key. Nothing landed on production
main; everything is on `criome-auth-integration` branches gated on the T6 audit.

## Branches + revisions (all pushed)

| Repo | Branch | Rev | What it carries |
|---|---|---|---|
| signal-criome | `criome-auth-integration` | `5976b2870e02` | 0.6.0: `node_identity.(Optional Identity)` added to `CriomeDaemonConfiguration` |
| meta-signal-criome | `criome-auth-integration` | `4e5f1af39a4b` | tracks signal-criome integration (wire-consistency cascade) |
| criome | `criome-auth-integration` | `4dc374f261db` | 0.4.3: configurable `node_identity`; working socket 0660; distinct-identity test |
| router | `criome-auth-integration` | `43572ce3ba96` | merge of T1 (`criome-forward-attestation`) + T3 (`persona-router-module`) + node-identity derivation |
| signal-router | `criome-forward-attestation` | `d212ea8a0a3b` | UNCHANGED — consumed from T1 (no new wire field needed) |
| CriomOS | `criome-auth-integration` | `bf30751f61c2` | merge of T2 (`criome-service-module`) + T3 (`persona-router-module`); nodeIdentity knob; socket-group access; pinned criome+router inputs |

Consistent wire generation verified across the whole router tree (one rev each,
no split-brain): signal-criome `5976b287` (0.6.0), signal-frame `b78c8077`
(0.3.0), criome `4dc374f2`, meta-signal-criome `4e5f1af3`, signal-router
`d212ea8a`.

## (1) Criome distinct-identity change — the trust anchor

The signing identity was hardcoded `Identity::host("criome")` in
`criome/src/actors/root.rs`. It is now configurable end to end, defaulting to
`Host("criome")` (single-node deployments unchanged).

Files changed:
- signal-criome `schema/lib.schema`: `CriomeDaemonConfiguration` gains
  `node_identity.(Optional Identity)` (appended last). `src/schema/lib.rs`
  regenerated (`SIGNAL_CRIOME_UPDATE_SCHEMA_ARTIFACTS=1 cargo build`). `src/lib.rs`:
  `new()` inits `node_identity: None`, plus `with_node_identity` / `node_identity()`
  accessors (the established `cluster_root` Optional idiom). Version 0.5.0→0.6.0.
- criome `src/actors/root.rs`: `Arguments.node_identity: Identity` +
  `Arguments::default_node_identity()` (= `Host("criome")`); `on_start` uses
  `arguments.node_identity` instead of the literal.
- criome `src/daemon.rs`: `CriomeDaemon.node_identity`; `from_configuration`
  reads `configuration.node_identity()` (default `Host("criome")`);
  `with_node_identity` builder; threaded into `RootArguments`.
- criome `src/deploy_encode.rs`: unchanged — it delegates to the schema-derived
  `NotaDecode` on `CriomeDaemonConfiguration`, which now handles the 6th field.

Required evidence — cross-identity ACCEPT + foreign/unregistered REFUSE, proven
at the criome level (two independent criome daemons, real `blst` BLS):

```
$ cargo test --test distinct_node_identities
running 1 test
test distinct_criome_identities_cross_verify_and_refuse_foreign_keys ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.23s
```

`criome/tests/distinct_node_identities.rs` proves, against the SAME verifying
criome B in one run:
- criome A (`Host("node-a")`, key Ka) `Sign` → criome B (which registered
  `node-a`→Ka) `VerifyAttestation` = `Valid`;
- a FOREIGN criome that also calls itself `Host("node-a")` but signs with key
  Kf → criome B = `InvalidSignature` (Kf ≠ the Ka B holds for node-a) — and this
  refusal bites EVEN THOUGH B's `cluster_root` is `None` (loose admission lets
  any key be registered, but the signature must still verify against the key B
  holds for that identity);
- an unregistered identity (a fresh criome B′ that never registered node-a) =
  `UnknownSigner`.

Cross-checked through the deploy path (cargo binaries): the encoder accepts the
6-field NOTA and the daemon self-registers the configured identity:
```
$ criome-encode-configuration '(CriomeConfigurationArtifact (…/criome.sock …/criome.sema (Some …/criome.sock.meta) None Quorum (Some (Host node-a))) …/config.rkyv)'
(ArtifactWritten …/config.rkyv)
$ criome-daemon …/config.rkyv &   # then over the working socket:
$ criome '(LookupIdentity (Host node-a))'   → (IdentityReceipt ((Host node-a) Active))
$ criome '(LookupIdentity (Host criome))'   → (Rejection UnknownIdentity)
```

## (2) Router integration branch + named-check results

`router` `criome-auth-integration` @ `43572ce3ba96` merges T1 + T3 (additive
overlap only — `Cargo.toml [[bin]]`, `flake.nix` checks — auto-merged clean) and
repoints signal-criome/criome to the integration branches.

Load-bearing router change (`src/criome_attestation.rs`): the criome signer
identity is no longer the hardcoded `Host("criome")`. It is derived from the
NODE identity on both sides — the sender derives the `SignRequest` gate identity
from its own `router_identity`; the receiver derives the reconstructed
`Attestation.signer` from the wire-carried origin router identity (already bound
into the digest). No new signal-router wire field: distinct identities flow as
the origin already on the wire. T1's tests were updated to configure each criome
fixture with the sender's node identity (`router-a`), proving the router carries
a NON-default configured identity.

The four named checks, built from the pushed ref on the prometheus remote
builder (`nix build github:LiGoldragon/router?ref=criome-auth-integration#checks.x86_64-linux.<name>`):

```
router-test> test router_accepts_forward_under_real_criome_bls_attestation ... ok
router-test> test router_refuses_forwards_without_a_valid_criome_attestation ... ok
router-test> test router_configuration_carries_listen_identity_and_criome_socket ... ok
router-test> test router_bootstrap_carries_hardwired_peers_and_actor_homes ... ok
   (copied from ssh-ng://nix-ssh@prometheus.goldragon.criome)
```

Full router cargo suite green (lib 5, actor_runtime_truth 32,
authorized_object_fanout 3, criome_forward_attestation 2,
configuration_text_edges 2, end_to_end_remote_forward 1, no_shared_locks_truth 1,
observation_truth 12, process_boundary 3, schema_generated 2, smoke 16, …).

## (3) Persona-router module socket-access change

For the milestone-3 criome dial to work at runtime, the persona-router service
user must reach criome's working socket. Two coupled changes:

- criome `src/daemon.rs`: the WORKING socket is now bound 0660 (group-accessible
  IPC) via `bind_socket(path, mode)`; the META socket stays 0600. The 0700 state
  dir and 0600 master key are untouched, so group membership never exposes the
  key. Test `criome_daemon_socket_modes_split_shared_working_from_private_meta`
  asserts working=0660, meta=0600.
- CriomOS `modules/nixos/persona-router.nix`: `serviceConfig.SupplementaryGroups
  = [ criomeSocketGroup ]` (default `"criome"`, the criome daemon group). The
  persona-router daemon thus joins criome's group and can connect to
  `criomeSocketPath`. criome must be co-resident (it creates the group).

## (4) CriomOS integration branch + pinned inputs

`CriomOS` `criome-auth-integration` @ `bf30751f61c2`:
- `flake.nix`: `router.url = github:LiGoldragon/router?ref=criome-auth-integration`
  (repinned from T3's rev) and a new `criome.url =
  github:LiGoldragon/criome?ref=criome-auth-integration`. `flake.lock` pins
  criome @ `4dc374f261db` and router @ `43572ce3ba96`.
- `modules/nixos/criome.nix`: new `nodeIdentity` option (the per-node `Host`
  name; null keeps `Host("criome")`); emits the 6-field NOTA
  `(socket store (Some meta) clusterRoot authMode nodeIdentityField)`. Peer-key
  seed (`peerIdentitySeeds`) already existed from T2.
- `modules/nixos/criome-node-test.nix`: socket-mode assertion updated
  (working 0660 / meta 0600).
- `modules/nixos/criome-auth-integrated-test.nix` (new): a single-node
  runNixOSTest carrying BOTH modules on the consistent wire generation — the T4
  starting harness.

## (5) Integrated system closure builds

```
$ nix build --no-link --print-out-paths -L --expr '
  let criomos = builtins.getFlake "github:LiGoldragon/CriomOS/bf30751f61c2…";
      system = "x86_64-linux"; inputs = criomos.inputs;
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      integrated = import "${criomos}/modules/nixos/criome-auth-integrated-test.nix" {
        inherit pkgs inputs;
        criomePackage = inputs.criome.packages.${system}.default;
        criomeModule = "${criomos}/modules/nixos/criome.nix";
        routerModule = "${criomos}/modules/nixos/persona-router.nix"; };
  in integrated.driver'
…
/nix/store/xs8n2b53qb5m9606v83gaijmxd243304-nixos-test-driver-criome_auth_integrated_node_builds
EXIT=0
```
Built on the prometheus remote builder (criome 0.4.3 + router-text + the NixOS
node toplevel). Composition confirmed by eval of the integrated nixosSystem:
```
services_present            = ["criome","persona-router"]
persona_router_supp_groups  = ["criome"]
criome emitted config NOTA  = (CriomeConfigurationArtifact (/run/criome/criome.sock
  /var/lib/criome/criome.sema (Some /run/criome/criome.sock.meta) None Quorum
  (Some (Host node-a))) /run/criome/criome-config.rkyv)
```

NOTE on scope vs. the brief's "no-guardian spirit module": no spirit NixOS
module exists anywhere (the spirit flake exposes `packages.daemon`
guardian-compiled + `packages.configuration-writer`, but no `nixosModule`). The
integrated closure carries the load-bearing auth pair (criome + persona-router).
Authoring the guardian-no-agent spirit service module is the source-node
assembly the T4 card already owns; its wire is compatible (see item 7).

## (6) Exact recipe for T4 — two distinct identities + cross-node key

Per node N (∈ {node-a, node-b}), set the SAME identity string on both the criome
and the persona-router (the node-identity unification — see item 7):

criome module (`services.criome`):
```nix
services.criome = {
  enable = true;
  package = inputs.criome.packages.${system}.default;   # criome-auth-integration
  nodeIdentity = "node-a";          # this node's Host identity; criome signs as Host("node-a")
  peerIdentitySeeds = [ {           # seed the OTHER node's criome key (cross-trust)
    name = "node-b";                # the peer's Host identity
    publicKey = "<node-b criome BLS public key, hex bare atom>";
    fingerprint = "<peer fingerprint, bare atom>";
    purpose = "CriomeRoot";
  } ];
};
```
This emits, and the encoder seals, the 6-field config NOTA:
`(CriomeConfigurationArtifact (/run/criome/criome.sock /var/lib/criome/criome.sema (Some /run/criome/criome.sock.meta) None Quorum (Some (Host node-a))) /run/criome/criome-config.rkyv)`
and the seed runs at ExecStartPost over the working socket:
`(RegisterIdentity ((Host node-b) <pubkey> <fingerprint> CriomeRoot None))`.

persona-router (the `PersonaRouter` node service payload):
```nix
horizon.node.services = [ { PersonaRouter = {
  identity = "node-a";                       # MUST equal services.criome.nodeIdentity
  listenPort = 7440;
  criomeSocketPath = "/run/criome/criome.sock";   # criome working socket (0660)
  criomeSocketGroup = "criome";              # default; grants the dial
  peers = [ { identity = "node-b"; address = "192.168.1.20:7440"; } ];
  actorHomes = [ { actor = "mirror"; process = 0; home = "node-b"; } ];
}; } ];
```

Socket paths: criome working `/run/criome/criome.sock` (0660, group `criome`),
criome meta `/run/criome/criome.sock.meta` (0600), persona-router TCP
`0.0.0.0:7440`. To obtain each node's criome public key for the peer seed: boot
the node, `CRIOME_SOCKET=/run/criome/criome.sock criome '(LookupIdentity (Host node-a))'`
returns the `IdentityReceipt`; read the registered key from criome's snapshot /
the first attestation envelope. The forward path then is: criome A signs the head
as `Host("node-a")` → router A forwards (origin `node-a` on the wire) → router B
reconstructs `Host("node-a")`, criome B resolves the seeded key → `Valid`. The
negative control: drop the peer seed (or seed a wrong key) on the receiver →
`UnknownSigner`/`InvalidSignature` → `ForwardRefused(AttestationInvalid)`, no
mirror append.

## (7) Surprises / what T4 and the auditor MUST know

1. **Node-identity unification (the load-bearing integration invariant).** The
   router no longer hardcodes `Host("criome")`; it derives the criome signer
   identity from the node's router identity. Therefore on each node
   `services.criome.nodeIdentity` MUST equal the persona-router `identity`. If
   they differ, the sender's `SignRequest` gate identity is not Active in the
   local criome → sign rejected → unsigned attestation → receiver refuses
   fail-closed (a misconfiguration fails safe, never silently wrong). This is
   why item 6 sets one node name on both modules.

2. **No new signal-router wire field.** Distinct identities flow as the origin
   router identity already on `RouterPeerAttestation.signer` (bound into the
   signed digest, so cryptographically vouched). signal-router is consumed
   unchanged at T1's `criome-forward-attestation` rev.

3. **signal-criome 0.6.0 cascaded to meta-signal-criome.** Adding the config
   field bumped signal-criome and forced a `links="signal-criome"` conflict
   (criome also pulls signal-criome transitively via meta-signal-criome). Fix:
   a meta-signal-criome integration branch repointed at signal-criome
   `criome-auth-integration`, so the whole tree resolves to ONE signal-criome.
   Any future consumer of this stack must pin meta-signal-criome to the
   integration branch too.

4. **criome working socket is now 0660 (was 0600).** Required for the
   persona-router co-resident dial. Meta socket stays 0600; state dir 0700; key
   0600 — group membership exposes only the socket, never the key. The
   single-node criome witness assertions were updated accordingly.

5. **Wire generation is consistent (no split-brain).** criome + router +
   meta-signal-criome all resolve signal-frame `b78c8077` (0.3.0) and
   signal-criome `5976b287` (0.6.0). The Sign/VerifyAttestation/Attestation wire
   types are byte-identical between signal-criome 0.5 and 0.6 (only the deploy
   config record changed).

6. **SPIRIT — the one place scoped down from item 5's literal wording.** No
   spirit NixOS module exists; the integrated closure carries criome +
   persona-router only. Authoring the guardian-compiled-no-agent spirit service
   module is the T4 source-node assembly (the T4 card already specifies it).
   Wire compatibility for that assembly: spirit's lock is signal-frame `b78c8077`
   (0.3.0 — the SAME frame as this integration) and signal-criome 0.5.0; because
   the Sign/Verify socket wire is unchanged 0.5→0.6, spirit's mirror-shipper
   criome gate (`gate_and_ship_head`) will interoperate with a criome 0.6.0
   daemon over the socket. T4/the auditor should VERIFY this empirically
   (spirit→criome Sign succeeds in the boot), and MAY repin spirit to the
   integration signal-criome for strict version consistency (not required for
   correctness, since the wire is identical).

7. **What is proven vs. what the boot still owes.** Proven here: the criome
   trust anchor (cross-identity accept + foreign/unregistered refuse, real BLS);
   the router carries a configured non-default identity (four named checks on
   prometheus); the integrated criome+persona-router system closure builds on
   prometheus with both services, socket-group access, and the 6-field
   node-identity config. Still owed by T4 (needs a boot on an authorized
   VM-testing host): the live two-node forward — criome A attests, router A→B
   forwards, criome B verifies the seeded peer, mirror appends; and the negative
   control fail-closed with no mirror append. The integrated single-node test
   `criome-auth-integrated-test.nix` is the harness to extend; its `testScript`
   already asserts both units active, the distinct identity self-registered, the
   0660 socket, and the persona-router holding criome's group.

## Checks run (summary)

- criome `cargo test --all-features`: all green (incl. distinct-identity test +
  updated socket-mode test). criome encoder + daemon exercised over the working
  socket (configured identity self-registers; default Host("criome") preserved).
- router 4 named checks on prometheus: all `ok` (T1 accept/refuse + T3
  config/bootstrap). Full router cargo suite green.
- signal-criome `cargo test --all-features`: 23 green. meta-signal-criome builds
  against signal-criome 0.6.0.
- Integrated NixOS node closure: `nix build … integrated.driver` on prometheus =
  EXIT 0; eval confirms both services + socket group + 6-field NOTA.

## Claims / boundaries

orchestrate claim `criomos-implementer` accepted on the four integration
worktree paths. Nothing landed on any production main; all six branches pushed
and gated on the T6 audit. No secrets in any output. The in-VM boot was not run
(no QEMU on this host; prometheus is the authorized VM-testing host) — that is
T4/T5's forced-boot path.
