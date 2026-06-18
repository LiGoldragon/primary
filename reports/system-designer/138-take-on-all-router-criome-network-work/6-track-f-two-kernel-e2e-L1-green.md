# 138/6 — Track F: two-kernel cross-host transport e2e (L1 GREEN under real KVM)

*Build → adversarial verify (with mutation testing). Verdict: **sound, MERGE**.
The two-kernel test **actually executed under KVM** (exit 0, reproduced twice),
not merely built. This is report 136's ladder rung **L1**. The polish pass closed
all three P3s — **L1 now proves delivery-to-the-actor, not just receipt** (see the
"P3s — CLOSED" section).*

## Result

Branch **`transport-two-kernel-e2e-138`** (off `transport-p1-fixes-138`), polish
commit `453bc281` (initial L1 at `72db634d`), **pushed**. Home: the **router repo's flake** (co-located with the
transport + P1 fixes), as a `runNixOSTest` check
`router-two-kernel-cross-host-transport`.

What the test proves, verified independently by the reviewer:

- **Two separate kernels.** The driver booted two distinct `qemu-system-x86_64`
  guests (separate PIDs), each logging its own boot ("Detected virtualization
  kvm").
- **Real guest-to-guest network hop**, not loopback/in-process: nodeOuranos
  (192.168.1.1) → nodePrometheus (192.168.1.2) on eth1; the forward-probe binary
  runs *on* ouranos and dials prometheus over the VM L2.
- **Real minted slot + durable receipt:** `accept reply: (ForwardAccepted 1)`,
  `(ForwardAccepted 2)` — genuine pre-incremented persisted sequence, not a
  placeholder.
- **Loop guard bites cross-kernel:** `loop-guard reply: (ForwardRefused
  AlreadyForwarded)` — a `Forwarded`-stamped frame is refused before persisting.
- Final banner: `L1 GREEN: router cross-host transport delivered a real
  minted-slot durable receipt across two kernels over real VM networking, and the
  loop guard refused an already-forwarded frame.`

**Assertions are mutation-proven to bite:** the reviewer reverted the loop guard
(`router.rs:2281`) → a `Forwarded` frame returned `(ForwardAccepted 3)` and the
test FAILED the `AlreadyForwarded` assert; forcing the slot to 0
(`router.rs:395`) → FAILED the `slot != 0` assert. So the test genuinely guards
Track A's fixes.

## Engineering worth noting

- **Daemon discipline honored end-to-end.** Two new one-NOTA-arg deploy
  encoders (`router-encode-configuration`, `router-encode-bootstrap`) encode the
  typed `RouterDaemonConfiguration` / `RouterBootstrapDocument` to rkyv at deploy
  time; the new minimal `nix/modules/message-router.nix` runs them in
  `ExecStartPre`, then `ExecStart` launches `router-daemon <config.rkyv>` with
  **one argument, no flags**. The `default` nix package ships `router-daemon`
  built *without* `nota-text` (it cannot parse NOTA); encoders/probe live in the
  `text` package.
- **`router-forward-probe`** is the cross-host transport's first real client.
- **Eager tailnet bind:** a `RouterEngine::ensure_started` lifecycle hook binds a
  node's TCP ingress at startup (not lazily on first Unix-socket connection), so
  a receive-only node is listening the instant its unit is ready.
- A fast no-KVM witness (`two_process_transport_artifacts.rs`, two real
  daemon OS processes over loopback) exercises the same encoders/probe/asserts as
  a CI-cheap check.

## The three P3s — CLOSED (polish commit `453bc281`, re-run GREEN under KVM)

1. **Receipt → delivery.** A new one-NOTA-arg `router-harness-witness` binary (the
   cross-VM twin of L0's in-process `HarnessWitness`) binds the
   `EndpointKind::HarnessSocket` the daemon's `HarnessDelivery` connects to,
   decodes the inbound `MessageDelivery`, and emits `(WitnessedDelivery <harness>
   <sender> <body>)`. prometheus-responder is now homed on a real HarnessSocket;
   the test asserts on the **decoded delivery fields** read from the witness, not
   the accept slot. **Mutation-proven:** gating `deliver_to_harness_socket` to
   skip the connect makes the witness assertion time out and FAIL while the minted
   slot still passes — so the assertion fires precisely on broken delivery. The
   KVM log shows both `(WitnessedDelivery prometheus-responder message [relay
   across two kernels])` lines written on the far guest.
2. **Node IPs pinned.** `networking.interfaces.eth1.ipv4.addresses` set explicitly
   per node via `lib.mkForce` (verified one address each via `nix eval`), with a
   runtime `ip -4 addr` assert — a node rename now surfaces a wrong/unreachable
   address rather than silently retargeting the probe.
3. **Early-eof quieted.** A new `read_forward_frame` returns
   `IngressFrameRead::CleanClose` (no reply, no error log) on a clean close at the
   frame boundary; a truncated prefix or short body still surfaces a real
   `FrameError::Io`, so genuine mid-frame errors are not suppressed.

Three new P3s remain, all clarity-only and accepted (not worth a further KVM
pass): the report's nix store-path string isn't a stable identifier; `Accepted`
is deliberately decoupled from delivery success (a future author must not assert
delivery via the slot — the witness path is the correct one); and the nixosTest's
delivery check is line-presence rather than exact-count (the two-process witness
test asserts exact count/fields, covering this).

## Honest scope ceiling

L1 uses the **offline fixed-identity verifier** (`criome_socket_path` unset). It
does **not** exercise real criome BLS attestation, durable replay-across-kill,
clock-skew rejection, or impostor-key rejection — report 136 gates those on the
milestone-3 criome client (Decision 1, 138/2). The bridge is a virtual L2
(`runNixOSTest`), not Yggdrasil-routed peers — that is rung **L2**. Operator owns
the merge to router main.
