# Two-VM criome-auth witness — full chain (L1–L6 incl. L5) prometheus run, v2

> INDEPENDENTLY VERIFIED (2026-06-29) by a fresh agent: the prior agent that
> produced this bundle died mid-response, so a fresh agent re-assessed the
> committed state and re-ran the witness on prometheus from scratch. Every claim
> below held. The full independent re-run evidence is section (9) at the end of
> this file. Verdict: the committed witness at `fa449abf` GENUINELY PASSES the
> full six-link chain (incl. L5 durable landing + BOTH negatives refused with
> reason) on real prometheus VM boots.

Supersedes `CriomosImplementer-WitnessRunEvidence.md` (rev `98caa9f0`, which had
an honest L5 durable-landing gap and only the unregistered negative). This v2
extends that witness so it (a) forwards the REAL seeded spirit head, (b) durably
LANDS the record in the mirror on node-b (L5), (c) proves signature verification
in the VM with a second negative (registered identity + foreign signature), and
re-ran it on prometheus to harvest the full per-link bundle. The full chain now
genuinely PASSES on real prometheus VM boots: all six links INCLUDING L5, plus
BOTH negatives, each refusing with the asserted reason. All boots ran natively on
prometheus (KVM); ouranos never fired QEMU. Nothing landed on any production main.

## (1) What changed + files

Base: `CriomOS-test-cluster criome-auth-witness @ 98caa9f0`, extended to
`@ fa449abf` (the clean committed rev the witness ran at).

### Real record head wiring (closes the synthetic-stand-in overclaim)
`lib/mkCriomeAuthWitnessTest.nix`: deleted the `sha256sum` synthetic-head block
and its false "content hash of the real record / provably tied" comments/prints.
The forwarded head is now read from the seeded daemon via the owner-only meta op
`meta-spirit '(ObserveHead)'`, extracting `\(Some ([0-9a-f]{64})\)`. That value
(`326640ace3…b85a`) is used as `HEAD_DIGEST_HEX` for every forward AND for the
mirror-landing assertion. It is `EntryDigest::to_string()` of the spirit store's
real versioned-log head, not a hash of literals.

### Mirror endpoint / grant / store wiring (L5 durable landing)
- `flake.nix`: re-pinned `router` input from the audited base `7dd747f9` to
  `221b5fb0` (carries the mirror `ComponentSocket` bootstrap endpoint + the
  `GrantDirectMessage` surface + the proven in-process L5 relay test), and
  re-pinned `spirit` from `a6d69b46` to branch `criome-auth-witness` `7d1b0697`
  (adds `ObserveHead`; re-pins its own meta-signal-spirit to `783cd502`).
  `flake.lock` updated accordingly (criome `4dc374f2`, mirror `d30cd180`
  unchanged — already at target).
- `lib/mkCriomeAuthWitnessTest.nix` `routerService`: added a `grantsNota`
  parameter and emit the 5th `BootstrapWriteRequest` list. node-b now passes the
  mirror actor-home `(mirror 0 None (Some (ComponentSocket <mirror-working>)))`
  AND the grant `(operator mirror)` (the forward's source actor is `operator`,
  not re-stamped). The `BootstrapWriteRequest` is now the 5-list form
  `(BootstrapWriteRequest <out> [ ] [ <home> ] [ <grant> ])` that 221b5fb0
  requires.
- testScript: the mirror store is REGISTERED FIRST via
  `meta-mirror '(RegisterStore spirit)'` (else an Append to an unregistered store
  is refused `UnknownStore`). After the positive accept, the mirror is read via
  `mirror '(ObserveHeads (Some spirit))'` and the landed head is asserted to
  EQUAL the real forwarded record head (non-degenerate, see (2)).

### Signature-verification proof (closes the negative-control scope limit)
testScript: added a SECOND negative — a REGISTERED identity (`Host(node-a)`)
presenting a FOREIGN signature → `InvalidSignature` → `ForwardRefused
AttestationInvalid`. It is built by attesting through node-b's criome while
claiming `NODE_IDENTITY=node-a` (a registered active identity on criome B): criome
signs with its OWN master key, so the presented key is node-b's — foreign to
node-a's registered key. criome B resolves `Host(node-a)` → registered key, sees
it differs from the presented key, and returns `InvalidSignature`
(verifier.rs:60). Both negatives now assert the specific refusal REASON
(`AttestationInvalid`), not merely that they refused. The previously-trivial
"mirror empty after refusal" assertions were re-scoped (see (2)).

## (2) Encoding found + non-degenerate landing assertion

Resolved empirically against the running daemons (native probe on prometheus,
exact rev binaries) — the two prior upstream reports DISAGREED on the mirror head
encoding; this run settles it:

- `meta-spirit '(ObserveHead)'` renders the head as **64-char lowercase hex**:
  `(HeadObserved ((1 11590050586725752087) (Some 326640ace3…b85a)))`.
- `mirror '(ObserveHeads (Some spirit))'` ALSO renders the head as **64-char
  lowercase hex** (this rev's `signal-mirror` `EntryDigest`/`FixedBytes<32>` NOTA
  encoding is hex via `to_nota`, NOT 32 decimal bytes — the prior "32 DECIMAL
  bytes" warning does NOT apply at `d30cd180`). The landed form is
  `(HeadsObserved [(spirit (Some (1 326640ace3…b85a)))])` — `(<store> (Some
  (<sequence> <64-hex-digest>)))`.

So the witness compares **hex on both sides** — no conversion needed. The
landing assertion is non-degenerate by construction:

```python
landed_match = re.search(r"\(spirit \(Some \(\d+ ([0-9a-f]{64})\)\)\)", landed)
assert landed_match, "L5: the verified forward must durably land a head ..."   # rules out "nothing landed" (registered-empty prints (spirit None) -> no match)
assert landed_match.group(1) == head, "L5: landed head must EQUAL the real ..." # rules out "a different digest landed"
```

It distinguishes all three states: nothing-landed (`(spirit None)` → no match →
fail), a-different-digest (match but `!= head` → fail), the-real-record-landed
(match and `== head` → pass). The mirror stores the carried `EntryEnvelope.digest`
verbatim as its head (`mirror store.rs:179`), and `router-forward-witness` sets
that digest to `HEAD_DIGEST_HEX` (the real spirit head), so a real landing makes
the mirror head equal the real head. Before the accept the baseline is asserted
`(spirit None)` and `head not in baseline`, so the assertion cannot accidentally
always-pass.

## (3) Reproduce command + clean rev + forced-boot mechanism

Clean committed rev the witness ran at (pushed):
`CriomOS-test-cluster criome-auth-witness @ fa449abf97efe998473d715166cf7eb22ab056b9`.

Reproduce, from a clean checkout of the witness branch:

```sh
scripts/run-criome-auth-on-prometheus            # refuses a dirty tree; pushes; pins the committed rev; runs the driver on prometheus
# or, raw, the exact command run this session ON prometheus:
nix run github:LiGoldragon/CriomOS-test-cluster/fa449abf97efe998473d715166cf7eb22ab056b9#test-criome-auth-witness
```

How it forces a REAL boot every invocation: the app's program is the
`runNixOSTest` DRIVER (`${check.driver}/bin/nixos-test-driver`). `nix run`
builds/caches only the driver package + the two node closures; the QEMU boot
happens when the driver RUNS, every invocation — a cached `checks` realisation
cannot satisfy it. The boot MUST run natively on prometheus: ouranos (laptop) is
forbidden QEMU, and prometheus's `/etc/nix/machines` lacks the `nixos-test`
feature so the boot cannot be remote-scheduled — prometheus's LOCAL nix
(`system-features = … kvm nixos-test`) runs it.

Forced-boot PROVEN by distinct fresh QEMU guests on each invocation at the SAME
committed rev `fa449abf`:
- Run 1 (`2026-06-28T23:56:18Z`): QEMU `node-a pid 637620`, `node-b pid 637621`
  → `WITNESS GREEN`, `DRIVER_EXIT=0`.
- Run 2 (`2026-06-28T23:57:33Z`): QEMU `node-a pid 637833`, `node-b pid 637832`
  → `WITNESS GREEN`, `DRIVER_EXIT=0`.
Two consecutive green runs with DISTINCT fresh QEMU pairs at one committed rev — a
store-realized `checks` output never produces these.

## (4) Full six-link evidence bundle — PROMETHEUS RUN (rev fa449abf, run 1, 2026-06-28T23:56:18Z)

All lines are durable-state / driver-introspection observations (typed CLI
replies + unit states), not daemon printlns of internal state.

- **L1 — VM booted on prometheus.** `RUN_HOST=prometheus`, `RUN_KVM=present`,
  `RUN_SYSTEM_FEATURES=system-features = benchmark big-parallel kvm nixos-test`,
  `RUN_REVISION=fa449abf…`. Driver: `node-a: starting vm` / `node-b: starting vm`;
  `node-a: QEMU running (pid 637620)` / `node-b: QEMU running (pid 637621)`;
  `connected to guest root shell` on both.

- **L2 — all six daemons active, distinct identities.**
  `L2 OK: criome+router+spirit (node-a) and criome+router+mirror (node-b) active;
  distinct identities` — backed by criome `(LookupIdentity (Host node-a))` /
  `(Host node-b)` returning `Active` on the respective nodes.

- **L3 — real Spirit record seeded; fail-closed proven; REAL head read.**
  `L3 OK: meta Import receipt = (Imported (1 (1 11590050586725752087)))`.
  `L3 OK: ordinary working-socket Record refused fail-closed (guardian
  HarnessUnavailable) = (ReferentGuardianRejected (HarnessUnavailable [] [guardian
  is required but no guardian agent is configured]))` — the SAME daemon refuses an
  ordinary Record (real guardian refusal, not a parse error).
  `L3 OK: real spirit versioned-log head (ObserveHead) =
  326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a` — the store's
  own content-addressed head (NOT the old synthetic `cdc1c22f…`).

- **L5-prep — mirror store registered, head empty.**
  `L5-prep OK: mirror store 'spirit' registered, head empty = (HeadsObserved
  [(spirit None)])` (`meta-mirror '(RegisterStore spirit)' → (StoreRegistered
  spirit)`).

- **L6 pre — receiver ingress reachable.**
  `L6 pre: node-b router TCP ingress :7440 reachable from node-a`.

- **L6a (negative 1, UNREGISTERED signer) — refused with reason; mirror empty.**
  criome B `(LookupIdentity (Host node-a)) → (Rejection UnknownIdentity)` before
  the forward (so the decision is genuinely UnknownSigner).
  `WITNESS_PUBLIC_KEY=91b8777a…` (node-a's real BLS key) then `(ForwardRefused
  AttestationInvalid)`.
  `L6a mirror heads after negative-1: (HeadsObserved [(spirit None)])` — nothing
  landed.

- **L6b (negative 2, REGISTERED identity + FOREIGN signature) — refused with
  reason; mirror still empty.** After the handshake criome B holds `Host(node-a)
  Active` with key `91b8777a…`; this forward is attested through node-b's criome
  claiming `node-a`, so the presented key is node-b's
  `WITNESS_PUBLIC_KEY=8c5981a2…` — FOREIGN (`8c5981a2… != 91b8777a…`, asserted in
  the test). `(ForwardRefused AttestationInvalid)` (criome decision
  `InvalidSignature`: registered key != presented key).
  `L6b mirror heads after negative-2: (HeadsObserved [(spirit None)])` — nothing
  landed.

- **Trust handshake.** `(IdentityReceipt ((Host node-a) Active))` — node-a's REAL
  key registered on criome B; criome B `(LookupIdentity (Host node-a)) →
  (IdentityReceipt ((Host node-a) Active))`.

- **L4 (positive) — verified + accepted.**
  `WITNESS_PUBLIC_KEY=91b8777a…` (the SAME node-a key as negative-1, the registered
  matching key) then `(ForwardAccepted 0)`.

- **L5 (durable mirror landing) — REAL record LANDED.**
  `L5 mirror heads after accept: (HeadsObserved [(spirit (Some (1
  326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a)))])`.
  `L5 OK: real spirit head durably landed in the mirror; mirror head ==
  326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a` — the landed
  head EQUALS the real forwarded spirit head.

- `WITNESS GREEN (full chain): … node-b's criome REFUSED the unregistered signer
  (UnknownSigner → AttestationInvalid) and a registered identity bearing a FOREIGN
  signature (InvalidSignature → AttestationInvalid), leaving the mirror empty;
  after registering node-a's REAL key it ACCEPTED the matching-key forward and the
  carried Append durably LANDED in the mirror with head == the real spirit head.`

Driver finish: `test script finished in 12.58s`; `cleanup` clean; no `Traceback`,
no `RequestedAssertionFailed`. (Run 2 identical content with fresh pids,
`test script finished in 12.20s`.)

## (5) PASS / FAIL of every link

| Link | Claim | Result |
|---|---|---|
| L1 | VM boots natively on prometheus (KVM) | PASS (QEMU pids 637620/637621; 2nd run 637833/637832) |
| L2 | six daemons active, distinct identities | PASS |
| L3 | real Spirit record seeded; fail-closed; REAL head via ObserveHead | PASS (`Imported`; `HarnessUnavailable`; head `326640ace3…`) |
| L4 | registered matching-key forward verified + accepted | PASS (`ForwardAccepted 0`) |
| **L5** | **carried Append durably LANDS in the mirror; head == real record head** | **PASS** (`(spirit (Some (1 326640ace3…)))`) |
| L6a (neg 1) | unregistered signer refused with reason; mirror empty | PASS (`UnknownSigner → ForwardRefused AttestationInvalid`) |
| L6b (neg 2) | registered identity + foreign signature refused with reason; mirror empty | PASS (`InvalidSignature → ForwardRefused AttestationInvalid`; foreign key `8c5981a2… != 91b8777a…`) |

Two consecutive real boots at the clean rev, both `DRIVER_EXIT=0`.

## (6) Branches + revisions (all pushed; gated on the re-audit; NOT on any main)

| Repo | Branch | Rev | Role this run |
|---|---|---|---|
| CriomOS-test-cluster | `criome-auth-witness` | `fa449abf97efe998473d715166cf7eb22ab056b9` | the two-VM witness (real head, L5 landing, two negatives) + forced-boot app + run script — the clean rev it ran at |
| router | `criome-auth-witness` | `221b5fb04b838f3a5bbd2a6839d60aa2574902fd` | pinned: mirror ComponentSocket endpoint + `GrantDirectMessage` bootstrap + L5 relay test |
| spirit | `criome-auth-witness` | `7d1b069718a0ddede6e3928ecef272f25caaee6b` | pinned: owner-only meta `ObserveHead`; re-pins meta-signal-spirit `783cd502` |
| mirror | `criome-auth-witness` | `d30cd180507cd52d0369d2ec8b49136fdfca8458` | pinned (unchanged): signal-frame 0.3.0-aligned mirror |
| criome | `criome-auth-integration` | `4dc374f261db5d8d2bb62cb614f42a8592bca86f` | pinned (unchanged): configurable node_identity + distinct-identity trust |

Witness-resolved input revs (verified via `nix flake metadata` on the committed
rev): criome `4dc374f2`, router `221b5fb0`, mirror `d30cd180`, spirit `7d1b0697`
(its own lock re-pins meta-signal-spirit `783cd502`). Wire generation unchanged:
signal-frame 0.3.0 / signal-criome 0.6.0 (the wire was NOT split — each daemon is
built from its own pin and they all speak that one generation).

## (7) Remaining weaknesses (for the auditor / psyche)

1. **The two-VM negatives both surface at the router as `AttestationInvalid`.**
   criome maps both `UnknownSigner` and `InvalidSignature` to the single router
   refusal reason `AttestationInvalid`, so the router reply alone cannot
   distinguish the two. The witness distinguishes them by the SURROUNDING durable
   state, not by the router reply: negative-1 is run when criome B
   `(LookupIdentity (Host node-a)) = (Rejection UnknownIdentity)` (so the only
   possible decision is UnknownSigner); negative-2 is run after node-a is
   registered Active and asserts the presented key (`8c5981a2…`) differs from the
   registered key (`91b8777a…`) (so the only possible decision is
   InvalidSignature). The exact criome `VerificationDecision` is not read directly
   in the VM (no criome CLI verb forwards a constructed attestation); the
   distinction is structural. The per-decision branch is also unit-proven in
   `criome/tests/distinct_node_identities.rs`.

2. **Sender leg is `router-forward-witness` (a bin), not a router daemon outbound
   forward** — unchanged from v1; no router daemon ingress attaches a
   `RoutedContractObject` to an OUTBOUND message. The bin uses the router's OWN
   production `CriomeForwardAttestation`, so every signature/verification is real;
   the RECEIVER (node-b's persona-router daemon) is the full daemon doing
   verify/accept/refuse AND the L5 relay to the mirror socket.

3. **Daemons run as root in throwaway guests** (the mkCriomeClusterTest
   precedent) — proves the auth/verify/durable-landing logic, NOT production
   per-user socket isolation (carried by the hardened CriomOS modules,
   boot-proven separately by `criome-auth-integrated-test.nix`).

4. **Router lazy-runtime poke + TCP readiness gate** remain real receiver-side
   limitations the witness works around (the router should eagerly start its
   networked runtime and apply its bootstrap when a `tailnet_listen_address` is
   configured). Flagged, not fixed here.

5. **Benign log noise:** node-b's `router-daemon-tailnet: daemon frame error:
   frame IO error: early eof` is the router logging the forward-witness bin's
   one-shot TCP close after it reads the reply; it does not affect any link
   outcome (the test reads typed replies, not logs).

## (8) Host safety / boundaries

Every boot was a hermetic `runNixOSTest` driver run on prometheus
(`system-features = … kvm nixos-test`); no production `Switch`, no touching
prometheus live services/network; VMs are throwaway guests. Native grammar/chain
probes used an ephemeral `mktemp -d /tmp/…` set of daemons as user `li`, removed
after. ouranos never fired QEMU. No secrets in any output (the BLS public keys are
public material). Nothing landed on any production main; all branches pushed and
gated on the independent re-audit.

## (9) INDEPENDENT VERIFICATION RE-RUN (fresh agent, 2026-06-29)

The agent that produced sections (1)-(8) died mid-response (connection closed);
its chat findings were lost but its committed work (rev `fa449abf`) and these
evidence files survived. A fresh agent independently re-assessed and re-verified
the whole chain - it did NOT re-author the witness (the work was already complete
and committed), it confirmed the committed state and re-ran the boot from
scratch.

### Static verification (committed state, not the prose)

- `origin/CriomOS-test-cluster criome-auth-witness` == `fa449abf` (pushed; local
  branch matches origin). The local jj working copy is dirty with UNRELATED
  stale June-19 state on a different change (`9445ea2d` on `main`), which the
  reproduce ignores - the boot pulls the pinned GitHub ref `fa449abf`.
- The committed `flake.lock` at `fa449abf` pins exactly: router `221b5fb0`,
  spirit `7d1b0697`, mirror `d30cd180`, criome `4dc374f2`. All four dependency
  branch heads on GitHub match those revs (`git ls-remote`).
- The committed `lib/mkCriomeAuthWitnessTest.nix` testScript genuinely
  implements all four goals (read at `fa449abf`): real `ObserveHead` head
  (no `sha256sum`), `HEAD_DIGEST_HEX = head` for every forward; L5 RegisterStore
  + non-degenerate baseline (`(spirit None)` and `head not in baseline`) + the
  landing assertion `landed_head == head`; L6a (unregistered) asserts
  `UnknownIdentity` lookup then `ForwardRefused` + `AttestationInvalid`; L6b
  (registered + foreign sig) asserts `ForwardRefused` + `AttestationInvalid` AND
  `foreign_public_key != node_a_public_key`; both mirror-empty checks re-scoped to
  `"(Some" not in heads` and `head not in heads`.

### Live re-run on prometheus (two consecutive boots, same rev `fa449abf`)

Command (from ouranos; the driver runs natively on prometheus):
`ssh prometheus.goldragon.criome -- nix run github:LiGoldragon/CriomOS-test-cluster/fa449abf97efe998473d715166cf7eb22ab056b9#test-criome-auth-witness`

- Run A (`2026-06-29T00:05:22Z`): QEMU `node-a pid 638067` / `node-b pid 638066`;
  `connected to guest root shell` on both -> `WITNESS GREEN`, `test script
  finished in 14.72s`, `DRIVER_EXIT=0`.
- Run B (`2026-06-29T00:07:34Z`, consecutive, same rev): QEMU `node-a pid 638204`
  / `node-b pid 638205` -> `WITNESS GREEN`, `test script finished in 14.87s`,
  `DRIVER_EXIT=0`.

Forced-boot PROVEN: two consecutive invocations at one committed rev each booted a
DISTINCT fresh QEMU pair - a store-realized `checks` output never produces these.

Full six-link bundle observed in Run A (durable-state / driver-introspection):

| Link | Observed | Result |
|---|---|---|
| L1 | `node-a/node-b: starting vm`; `QEMU running (pid 638067/638066)`; `connected to guest root shell` (both); `RUN_HOST=prometheus`, `RUN_KVM=present`, `nixos-test` feature present | PASS |
| L2 | `L2 OK: criome+router+spirit (node-a) and criome+router+mirror (node-b) active; distinct identities` | PASS |
| L3 | `(Imported (1 (1 11590050586725752087)))`; ordinary Record `(ReferentGuardianRejected (HarnessUnavailable ...))`; `ObserveHead = 326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a` | PASS |
| L5-prep | `mirror store 'spirit' registered, head empty = (HeadsObserved [(spirit None)])` | PASS |
| L6a (neg 1, unregistered) | `WITNESS_PUBLIC_KEY=8d0f462d...`; `(ForwardRefused AttestationInvalid)`; mirror `(HeadsObserved [(spirit None)])` | PASS |
| L6b (neg 2, registered + foreign sig) | foreign `WITNESS_PUBLIC_KEY=b3c8cf79...` (!= node-a's `8d0f462d...`); `(ForwardRefused AttestationInvalid)`; mirror `(HeadsObserved [(spirit None)])` | PASS |
| Trust handshake | `(IdentityReceipt ((Host node-a) Active))` | - |
| L4 (positive) | `WITNESS_PUBLIC_KEY=8d0f462d...` (SAME registered matching key as L6a); `(ForwardAccepted 0)` | PASS |
| L5 (durable landing) | `L5 mirror heads after accept: (HeadsObserved [(spirit (Some (1 326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a)))])`; `mirror head == 326640ace3...b85a == real spirit head` | PASS |

Driver finish (Run A): `(finished: run the VM test script, in 14.64 seconds)`;
`cleanup` clean; no `Traceback`, no `RequestedAssertionFailed`, no
`AssertionError` (only benign kernel boot noise: `regulatory.db` firmware load
and `drm panic`-plane registration). `DRIVER_EXIT=0`.

### Encoding settled by the live re-run

Both `meta-spirit '(ObserveHead)'` and `mirror '(ObserveHeads (Some spirit))'`
render the head as 64-char lowercase hex (`326640ace3...b85a`) - the witness
compares hex on both sides, no conversion. The "32 decimal bytes" form does NOT
appear at mirror `d30cd180` (the debug trap does not apply here). The landing
assertion is non-degenerate by construction: the regex requires a
`(spirit (Some (... 64-hex)))` match (rules out "nothing landed", which prints
`(spirit None)`), then `landed_head == head` (rules out "a different digest
landed").

### Cross-run determinism (the un-fakeable part)

- The real head `326640ace3...b85a` is IDENTICAL across Run A, Run B, AND the
  prior agent's run - content-addressed from the seeded record, i.e. a REAL
  versioned-log head, not a per-run synthetic.
- The BLS public keys DIFFER per boot (Run A: node-a `8d0f462d...`, foreign
  `b3c8cf79...`; prior run: `91b8777a...` / `8c5981a2...`) - fresh per-boot
  criome identities prove genuine fresh boots, not a replayed cache. Within each
  run, node-a's key is the SAME in the negative-1 and the positive (registered
  matching key is the sole gate) and the foreign key differs (the
  `InvalidSignature` condition), exactly as asserted.

Verdict: the committed witness at `fa449abf` is genuinely complete and the full
chain PASSES on real prometheus boots. Nothing required finishing in code; the
fresh agent's contribution is this independent verification. Remaining weaknesses
are unchanged from section (7) and are the auditor's surface.
