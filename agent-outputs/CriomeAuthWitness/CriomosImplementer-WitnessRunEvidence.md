# Two-VM criome-auth witness — prometheus run evidence

> SUPERSEDED. This file records the FIRST honest state (rev `98caa9f0`): auth
> chain green but L5 durable mirror landing was a documented router gap, and only
> the unregistered negative existed. The full chain (real head, L5 durable
> landing, BOTH negatives refused with reason) was closed at rev `fa449abf` and
> INDEPENDENTLY VERIFIED on real prometheus boots — see
> `CriomosImplementer-WitnessRunEvidence-v2.md` (the authoritative bundle, with
> the independent verification re-run in its section (9)). Keep this file for the
> gap-then-closed history.

Task: take the prior agent's launched two-VM criome-auth witness boot on
prometheus to completion and harvest the real per-link evidence bundle. Iterate
on genuine bugs the actual run reveals; do not rebuild the witness from scratch.
Method: `reports/capacityAdmissionSlice/6-Translation-criome-auth-witness-vm-test.md`.

Status: the witness now GENUINELY PASSES on real prometheus VM boots for the
criome AUTH chain (links L1-L4 + L6, incl. the negative control). One link —
the durable mirror Append landing (L5) — is blocked by a genuine router
inbound-delivery gap, diagnosed in depth below, and the witness no longer
asserts a false landing. All boots ran natively on prometheus (KVM); ouranos
never fired QEMU.

## (A) How the run was obtained

1. The prior agent's in-flight boot was found ALIVE on prometheus (driver +
   two QEMU guests, output to `/tmp/criome-auth-witness-boot-1782669688.log`).
   It was NOT completing: node-a's `spirit.service` was in a 190+ restart
   crash-loop (`spirit-write-configuration: expected ConfigurationWriterInput
   to hold 2 root objects, found 8`). The testScript was blocked in
   `wait_for_unit("spirit.service")` (a 3600s driver timeout away).
2. I diagnosed the spirit config bug, validated the fix natively against the
   exact pinned spirit binary on prometheus, fixed it, re-ran — and the real
   run surfaced three further genuine bugs in sequence (cross-node TCP timing;
   router runtime lazy-bind; the durable-delivery gap). Each was diagnosed
   natively (ephemeral user daemons in a tmpdir on prometheus, no production
   paths/network) before the next boot, to avoid burning ~6-min boots one bug
   at a time.
3. Final state: a clean committed revision boots both guests on prometheus and
   the witness reaches `WITNESS GREEN` for the auth chain.

Host safety: every boot was a hermetic `runNixOSTest` driver run on prometheus
(`system-features = ... kvm nixos-test`); no production `Switch`; no touching
prometheus live services/network; VMs are throwaway guests. Native grammar
probes used ephemeral `mktemp -d /tmp/...` daemons as user `li`, removed after.

## (B) Reproduce command + committed revision + forced-boot mechanism

From a clean checkout of CriomOS-test-cluster `criome-auth-witness`:

```sh
scripts/run-criome-auth-on-prometheus
# (or, raw, run ON prometheus:)
nix run github:LiGoldragon/CriomOS-test-cluster/<rev>#test-criome-auth-witness
```

Committed revision the witness runs at (clean tree, pushed):
`CriomOS-test-cluster criome-auth-witness @ 98caa9f05e55c94a0faf0440902dfb853995bd1d`.

How it forces a real boot EVERY run: the app's program is the `runNixOSTest`
DRIVER (`${check.driver}/bin/nixos-test-driver`). `nix run` builds/caches only
the driver package and the node closures; the QEMU boot happens when the driver
RUNS, every invocation — a cached `checks` realisation cannot satisfy it. The
run script refuses a dirty tree (`jj status` must report no changes), pushes the
witness branch, pins the committed `self` rev, ssh-es to prometheus, and runs
the driver there. The boot MUST run natively on prometheus: ouranos (laptop) is
forbidden QEMU, and prometheus's `/etc/nix/machines` lacks the `nixos-test`
feature so it cannot be remote-scheduled — prometheus's LOCAL nix runs it.

Forced-boot proven by distinct fresh QEMU guests on each invocation this
session: run 1 (19:23:19Z) booted QEMU pids 541668/541669 -> WITNESS GREEN;
run 2 (consecutive, same rev) booted fresh pids 541873/541874 -> WITNESS GREEN;
the earlier in-flight boot used 527882/527883. Two consecutive green runs with
DISTINCT fresh QEMU pairs each, at the same committed rev, prove the driver boots
on every invocation — a store-realized `checks` output never produces these.

## (C) Per-link evidence bundle — PROMETHEUS RUN (rev 98caa9f0, 2026-06-28T19:23:19Z)

All lines are durable-state / driver-introspection observations (not daemon
printlns of internal state); the testScript reads typed CLI replies and unit
states.

- L1 — VM booted on prometheus. `RUN_HOST=prometheus`, `RUN_KVM=present`,
  `RUN_SYSTEM_FEATURES=system-features = benchmark big-parallel kvm nixos-test`,
  `RUN_REVISION=98caa9f05e55...`, `RUN_TIMESTAMP=2026-06-28T19:23:19Z`. Driver:
  `node-a: starting vm` / `node-b: starting vm`; `QEMU running (pid 541669)` /
  `(pid 541668)`; `connected to guest root shell` on both.

- L2 — all six daemons active, distinct identities. Driver:
  `finished: waiting for unit criome.service` (node-a 10.96s, node-b 0.22s),
  `persona-router.service` (node-a, node-b), `spirit.service` (node-a),
  `mirror.service` (node-b). testScript:
  `L2 OK: criome+router+spirit (node-a) and criome+router+mirror (node-b)
  active; distinct identities` — backed by criome `(LookupIdentity (Host node-a))`
  / `(Host node-b)` returning `Active` on the respective nodes.

- L3 — real Spirit record seeded; fail-closed proven; head derived.
  `L3 OK: meta Import receipt = (Imported (1 (1 11590050586725752087)))`
  (owner-only meta Import on the guardian-compiled, no-agent spirit daemon).
  `L3 OK: ordinary working-socket Record refused fail-closed (guardian
  HarnessUnavailable) = (ReferentGuardianRejected (HarnessUnavailable [] [guardian
  is required but no guardian agent is configured]))` — the SAME daemon refuses
  an ordinary Record; this is a REAL guardian refusal, not a parse error (the
  assertion requires `HarnessUnavailable`).
  `L3 OK: forwarded head (content hash of the real record) =
  cdc1c22fea273efbade8385bfa0e5c73899bb66632b96949e0952fc77891b718`.

- L6 (negative, run first) — unregistered signer refused fail-closed.
  `L6 pre: node-b router TCP ingress :7440 reachable from node-a`.
  `L6 negative forward outcome: WITNESS_PUBLIC_KEY=b9b8dc36a52a8b12e8df72eea4835b5964abc0d5d0214e8352b09d7b7dd48b64bb413bbdd9c1b6856cb1d483862e3f14`
  then `(ForwardRefused AttestationInvalid)` — node-a's REAL criome BLS signature,
  refused by node-b's criome because node-a's key is NOT yet registered.
  `L6 mirror heads after refusal: (HeadsObserved [])` →
  `L6 OK: unauthorized forward refused fail-closed (ForwardRefused); mirror empty`.

- Trust handshake — distinct-identity cross-trust.
  `trust handshake (criome B registers node-a's key): (IdentityReceipt ((Host
  node-a) Active))` — node-a's real BLS public key registered on criome B. This
  is the SOLE change between the refused and accepted forward.

- L4 (positive) — registered signer verified + accepted.
  `L4 positive forward outcome: WITNESS_PUBLIC_KEY=b9b8dc36...` then
  `(ForwardAccepted 0)` — the SAME bytes/signer, now ACCEPTED because node-b's
  criome holds node-a's registered key. The criome verify gate is the witnessed,
  un-fakeable claim: refuse (unregistered) vs accept (registered), one variable.

- L5 (durable mirror landing) — DOCUMENTED GAP, not asserted.
  `L5 mirror heads after accept (durable-landing gap — see evidence):
  (HeadsObserved [])`. The verified forward is ForwardAccepted but the router
  does not deliver the carried signal-mirror Append to the mirror's
  ComponentSocket (see section E). The witness does NOT claim a false landing.

`WITNESS GREEN (auth chain): ... node-b's criome REFUSED the unregistered signer
(ForwardRefused) and, after registering node-a's real BLS key, ACCEPTED the same
forward (ForwardAccepted) — the registered key is the sole gate. Durable mirror
Append landing is a documented router inbound-delivery gap.`

## (D) Run transcript proving real VM boots on prometheus

Boot markers (rev 98caa9f0): `node-a: starting vm` / `node-b: starting vm`;
`node-b: QEMU running (pid 541668)`; `node-a: QEMU running (pid 541669)`;
`Guest shell says: Spawning backdoor root shell...`; `connected to guest root
shell` on both; per-unit `finished: waiting for unit ...` lines; `test script
finished in 12.75s`; `cleanup ... finished`. Test passed (no
`RequestedAssertionFailed`, no `Traceback`). Two consecutive invocations each
booted a fresh QEMU pair (distinct pids), confirming the driver boots on every
run rather than re-using a cached check.

## (E) PASS / FAIL + code fixed

PASS: the criome AUTH chain end to end on real boots — fail-closed spirit seed
(L3), criome A attestation (L4/L6 emitted real BLS key), router carry, criome B
REFUSE unregistered (L6, negative control, fail-closed, mirror empty) and ACCEPT
registered (L4) with the registered key as the sole gate.

NOT PASSING (documented gap, link L5): the durable mirror Append landing. The
verified inbound forward is `ForwardAccepted`, but the persona-router daemon does
not relay the carried `signal-mirror::Append` to the co-resident mirror's
ComponentSocket, so no head lands.

Code I fixed (all on the witness branches, gated on audit — see section G):

1. spirit NOTA grammar to the witness-pinned spirit `a6d69b46` (`inputs.spirit`
   resolves to lock node `spirit_2`, NOT the `4fce1c5f` also in the lock — my
   first native validation hit the wrong rev and gave a coincidentally-similar
   error). Against `a6d69b46` the `spirit-write-configuration` input is an enum
   newtype variant whose 7-field struct is a NESTED record
   `(ConfigurationWriteRequest (<socket> (Some <meta>) <db> None <authMode> None
   <out>))` (authorization_mode `Observing`); the meta `Import` record id is a
   bare-eligible string with an EMPTY referent vector (owner-only Import bypasses
   the guardian but NOT the store's referent canonicalization, which rejects an
   unregistered referent); and an ordinary working-socket Record WITH a referent
   fails closed via the referent guardian `HarnessUnavailable`. File:
   `CriomOS-test-cluster/lib/mkCriomeAuthWitnessTest.nix` (spiritService config,
   `importNota`, L3 fail-closed probe + a strengthened `HarnessUnavailable`
   assertion). All three validated natively against the `a6d69b46` binary.

2. cross-node TCP readiness gate before the forwards: daemons reach `active`
   before the guest VLAN carrier/IP is up, so the first run hit
   `connect to node-b:7440: Connection refused`. Added
   `node_b.wait_for_open_port(7440)` + a node-a `</dev/tcp/node-b/7440` reach
   check. File: same witness `.nix`.

3. receiver router runtime poke: the router daemon starts its networked runtime
   (and binds the tailnet TCP ingress + applies its bootstrap actor-home table)
   LAZILY, on the first working-socket request (`RouterEngine::runtime()`
   `OnceCell`). A receiver that only ever gets inbound TCP never binds :7440.
   Added a `router '(Summary witness-poke)'` poke on node-b before the forwards.
   File: same witness `.nix`. Validated natively (port CLOSED before poke, OPEN
   after).

4. router deployable channel grant (router branch): a verified inbound forward
   is only DELIVERED to a locally-homed actor when a direct-message channel grant
   (sender->recipient) exists; otherwise it parks for adjudication. No deployable
   surface could install that grant (the bootstrap writer omitted grants; the
   meta-router grant vocabulary names only fixed components/connection classes,
   not the witness's `operator`/`mirror`). I extended `router-write-bootstrap` to
   emit `RouterBootstrapOperation::GrantDirectMessage` (a 5th `(source
   destination)` list) and updated its boundary test. Files (router
   `criome-auth-witness`): `src/bin/router_write_bootstrap.rs`,
   `tests/configuration_text_edges.rs`. NECESSARY BUT NOT SUFFICIENT — see (E)
   below: even with the grant applied, the native receiver chain still does not
   land the Append in the mirror, so the witness stays pinned to the audited
   router base `7dd747f9` and does not depend on this grant.

## (F) Where the witness is weaker than ideal (for the auditor + psyche)

1. **Durable mirror landing (L5) does not work — genuine router gap.**
   Diagnosed via a full native receiver chain on prometheus (criome A signer +
   criome B verifier + receiver router + mirror, real BLS, real TCP): the
   positive forward returns `(ForwardAccepted 0)` but the mirror stays
   `(HeadsObserved [])`; the mirror receives NO connection. In code,
   `router.rs::apply_forwarded` enqueues the `RoutedContractObject` and returns
   `ForwardApplied::Accepted` unconditionally after `retry_pending()`;
   `retry_pending` resolves the actor (`ReadHarnessDeliveryTarget`), runs
   `CheckChannel`, and on success calls `HarnessDelivery::deliver` →
   `deliver_to_component_socket`. The mirror never receives the Append even with
   the channel grant added, so the wall is at target-resolution or the
   channel/structural-channel gate, not the criome auth. The
   inbound-forward -> co-resident-component DURABLE delivery path was only ever
   exercised in `router/tests/end_to_end_remote_forward.rs` for a notice-only
   `NotifyObject` to a PASSIVE harness witness via in-process
   `RouterInput::GrantChannel` — never a durable `Append` to a real mirror daemon
   through the deployable bootstrap. Recommended next step: a router engineer
   with the router's own introspection (correct engine id for `MessageTrace`,
   or a tracing subscriber) to localize whether the forwarded message parks at
   target-miss vs channel-adjudication vs delivery, then wire the deployable
   grant + (likely) structural-channels into the bootstrap and confirm
   `deliver_to_component_socket` fires. `EntryDigest` is `(Bytes 32)`, so any
   future mirror-head assertion must compare the 32 decimal bytes
   (`205 193 194 47 ...` for this head), NOT the hex string — the original
   witness grepped the hex and would never have matched even if the head landed.

2. **Sender leg is `router-forward-witness` (a bin), not a router daemon
   outbound forward** — unchanged from the prior evidence; no router daemon
   ingress attaches a `RoutedContractObject` to an OUTBOUND message. The bin uses
   the router's OWN production `CriomeForwardAttestation`, so every
   signature/verification is real. The RECEIVER (node-b's persona-router daemon)
   is the full daemon doing verify/accept/refuse — the witnessed claim.

3. **Negative control is the UNREGISTERED case (`UnknownSigner` ->
   `AttestationInvalid`).** Same bytes/signer forwarded before vs after
   registering node-a's key on criome B — fail-closed `ForwardRefused`, mirror
   empty. The FOREIGN-key-for-a-registered-identity case (`InvalidSignature`) is
   unit-proven separately in `criome/tests/distinct_node_identities.rs`.

4. **Daemons run as root in throwaway guests** (the mkCriomeClusterTest
   precedent) — proves the auth/verify logic, NOT production per-user socket
   isolation (carried by the hardened CriomOS modules, boot-proven by
   `criome-auth-integrated-test.nix`).

5. **My L3 fail-closed witness short-circuits at the REFERENT guardian**
   (`ReferentGuardianRejected HarnessUnavailable`) because the probe Record
   carries a referent that auto-registers through the guardian first. It is
   still a real guardian `HarnessUnavailable` fail-closed; an empty-referent
   Record instead trips an `EmptyReferents` validation (a6d69b46) before the
   record guardian, which is a weaker witness, so the referent path was chosen.

## (G) Branches + revisions (all pushed; gated on the T6 audit; NOT on any main)

| Repo | Branch | Rev | Carries |
|---|---|---|---|
| CriomOS-test-cluster | `criome-auth-witness` | `98caa9f05e55` | the two-VM witness (spirit-grammar fixes, TCP gate, router poke, honest L5) + forced-boot app + run script |
| router | `criome-auth-witness` | `9f4d3894fdfd` | forward-witness bin + bootstrap ComponentSocket endpoint + NEW deployable direct-message GrantDirectMessage in router-write-bootstrap (+ test). NOT pinned by the witness (necessary-not-sufficient for L5). |
| criome | `criome-auth-integration` | `4dc374f261db` | (consumed unchanged) configurable node_identity + distinct-identity trust |
| mirror | `criome-auth-witness` | `d30cd180` | (consumed unchanged) signal-frame 0.3.0 alignment |
| spirit | (main, lock node `spirit_2`) | `a6d69b46` | (consumed unchanged) guardian-compiled no-agent daemon + meta Import |

Witness-resolved input revs (verified via `nix flake metadata` on the committed
rev): criome `4dc374f2`, router `7dd747f9` (the audited base; the witness does
NOT pin my router grant rev `9f4d3894`), mirror `d30cd180`, spirit `a6d69b46`.

## (H) Checks run (summary)

- Spirit leg (config write, meta Import, fail-closed Record): validated natively
  against the witness-pinned spirit `a6d69b46` binary on prometheus —
  `(ConfigurationWritten ...)`, `(Imported (1 ...))` with `Lookup` ->
  `(RecordFound ...)`, ordinary Record -> `(ReferentGuardianRejected
  (HarnessUnavailable ...))`.
- Router runtime poke: native — TCP :7440 `CLOSED` before the `(Summary ...)`
  poke, `OPEN` after.
- Full receiver chain (criome A/B + router + mirror) native: `ForwardRefused`
  (unregistered) -> register -> `ForwardAccepted` (registered); mirror
  `(HeadsObserved [])` in both cases (the durable-landing gap).
- Router branch build (`packages.witness`) green after fixing the
  `router_bootstrap_carries_hardwired_peers_and_actor_homes` boundary test for
  the new 5th grants field.
- Two-VM witness boot on prometheus (rev 98caa9f0): `WITNESS GREEN`, `test script
  finished in 12.75s`, clean cleanup, no assertion failure; two consecutive runs
  each booted fresh QEMU guests.

## (I) Claims / boundaries

Nothing landed on any production main; all branches pushed and gated on the
independent (T6) audit. No secrets in any output. The boot ran natively on the
authorized VM-testing host (prometheus); ouranos never fired QEMU. The durable
mirror landing (L5) is reported as a genuine, in-depth-diagnosed router gap
rather than masked by a hollow green (intent `beaj` / `vcin`): the evidence is
the product.
