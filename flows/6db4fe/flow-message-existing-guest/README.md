# Existing Prometheus guest: Flow/Message parity preparation

This fixture targets only Prometheus's already declared `microvm@vm-testing.service`. Field `6db4fe` holds guest process reservation `4373`; the retained Field `9ddcbc` owns consumer rollout. The older `../flow-message-vm/` NixOS test creates a different VM and must remain unbuilt and unbooted for this trial.

`guest_preflight.py plan` validates the manifest locally and lists missing immutable graph/receipt inputs. The example manifest intentionally leaves all candidate revisions and acceptance receipts unset. `guest_preflight.py inspect` is a **read-only** remote preflight: strict known-host-key SSH first asks the endpoint for `hostname --short`, requires exactly `prometheus`, and only then reads the one guest unit and its current/toplevel links and image/runner existence. It has no start, stop, build, login, test, or local-host fallback action. A wrong-host response, failed SSH, or timeout refuses before every unit/image read. The earlier Ouranos-local unit observation is discarded and must never be treated as Prometheus readiness.

The guest trial may be implemented and run only after owners publish one immutable, generated-and-tested Flow/Message/Signal/meta graph, an accepted Field parity receipt and real CLI syntax for both delivery modes. The manifest's case list is a **test contract**, not an executed result. It requires one exact recipient and a real typed CLI → Nexus → target receipt → Flow confirmed-release sequence; Raw remains explicitly unattributed and unlocked, whereas FlowLocked requires exact binding/generation/permit and may refuse unavailable without falling back to Raw. Negative cases cover stale/unknown binding, busy/refresh hold, forged identity claims, ambiguity and crash-before-release. Guest sockets and stores must stay under the manifest's guest-only `/run` and `/var/lib` paths; no host production socket/store is reused.

Before any authorized start, the executor must snapshot the *Prometheus* unit, `current` and `toplevel` links, image presence, QEMU/tap state and guest directory. The only eventual lifecycle interface is `systemctl start/stop microvm@vm-testing.service` on the verified remote host; rollback stops only that guest's process, verifies its tap/process gone, and preserves evidence. No second controller or `runNixOSTest` VM is allowed. Guest SSH uses strict host-key checking and existing identity without agent forwarding or copying a host home, token or key. SSH into the guest is not native Haiku/Luna login: process-only Luna remains an untested guest-local app-server proposal, and Haiku has no accepted process-memory-only login route. Neither model subject may run until its own login gate is accepted.

Focused local fixture check: `python -m unittest test_guest_preflight.py`. It uses a fake transport and does not contact Prometheus.

## Sources

- `flows/9ddcbc/reports/flow-message-vm-trial-2026-09-21.md` for the existing guest, rollout division and sequencing gate.
- `flows/6db4fe/reports/flow-message-vm-experiment.md` and `vm-native-login-interface.md` for prior guest preimage and process-only login boundaries.
- `flows/4b0f60/reports/message-delivery-modes.md` for Raw/FlowLocked and attribution semantics. These are design/acceptance inputs, not an installed paired runtime receipt.
