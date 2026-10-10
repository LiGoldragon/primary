# Sole-guest Flow/Message evidence check

Field 9ddcbc owns this **offline checker** and CriomOS-home consumer reservation 3776. Field 6db4fe holds Prometheus guest lock 4373 and its retained Terra worker alone controls `microvm@vm-testing.service`. This checker has no network, build, start, stop, login, or Message-send operation. It reads one evidence JSON from the existing-guest controller and checks parity, one-recipient selection, mode/authority separation, and lossless rollback. A pass is an evidence-consistency result, not proof that a CLI response or receipt was genuine; source owners and the controller must witness those inputs independently.

Run now, without touching the guest:

```sh
python flows/9ddcbc/flow-message-acceptance/check.py plan flows/9ddcbc/flow-message-acceptance/evidence.example.json
```

After Mind publishes one generated-and-tested immutable graph and its **actual compiled CLI syntax**, Terra's sole-guest run records an evidence file outside Git and Field supplies installed-pair parity. Then run `check` with that file. The checker never executes `case.cli_argv`; it records the real invocation Terra witnessed. Do not fill a template field from a proposal or synthetic output. Raw is explicit UID-authorized and unattributed; FlowLocked requires separate BoundFlow authority, exact binding/generation and permit, with no Raw fallback. Transport confirmation does not imply target read or application completion. The example intentionally fails closed.

The separate `flows/6db4fe/flow-message-vm/` flake starts another guest and remains out of scope. The supported existing-guest preflight lives in `flows/6db4fe/flow-message-existing-guest/`; it is read-only. No base boot occurs before coherent graph and Field parity. The acceptance owner must preserve post-checkpoint queued and ambiguous records when stopping or recovering the guest. Do not put login material, a device code, account identity, raw model response or unredacted typed payload in this evidence file.
