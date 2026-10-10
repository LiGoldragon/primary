import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("acceptance_check", HERE / "check.py")
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def valid(mode="Raw"):
    data = json.loads((HERE / "evidence.example.json").read_text())
    data["target"].update(host_key_verified=True, node_identity_verified=True)
    for key in module.GRAPH:
        data["graph"][key] = "a" * 40
    for key in module.RECEIPTS:
        data["receipts"][key] = key + "-receipt"
    for key in ("flow", "message"):
        data["artifacts"][key] = {
            "nix_output": "/nix/store/output-" + key,
            "guest_executable": "/nix/store/output-" + key + "/bin/nexus",
            "built_sha256": "b" * 64,
            "running_sha256": "b" * 64,
        }
    data["consumer_parity"] = {
        "flow_package": "/nix/store/flow",
        "message_package": "/nix/store/message",
        "effective_unit_digest": "c" * 64,
        "effective_config_digest": "d" * 64,
    }
    data["case"].update(
        recipient="disposable-one", source_event_id="event-one", mode=mode,
        cli_argv=["/nix/store/message/bin/message", "typed-request-from-Mind"],
        contract_revision="e" * 40,
        typed_request_digest="f" * 64, typed_response_digest="0" * 64,
        transport_receipt="transport-receipt", transport_state="Confirmed",
    )
    if mode == "Raw":
        data["case"]["authority"] = {"kind": "RawUid", "receipt": "uid-receipt", "bound_flow": None}
    else:
        data["case"].update(
            authority={"kind": "BoundFlow", "receipt": "binding-proof", "bound_flow": "sender"},
            binding={"id": "one-binding", "generation": 1}, permit="permit-one",
            raw_fallback=False, confirmed_release=True,
            target_delivery_receipt="one-target-delivery-proof",
        )
    data["rollback"].update(
        preimage_id="snapshot-one", schema_version="v1",
        preimage_state_digest="1" * 64, post_attempt_state_digest="2" * 64, recovered_state_digest="3" * 64,
        post_checkpoint_events=["event-one"], retained_events=["event-one"],
        ambiguous_attempts=["attempt-one"], retained_ambiguous_attempts=["attempt-one"],
        unit_stopped=True, qemu_gone=True, tap_gone=True, recovery_receipt="recovery-proof",
    )
    return data


class AcceptanceTests(unittest.TestCase):
    def test_template_refuses_without_graph_and_receipts(self):
        template = json.loads((HERE / "evidence.example.json").read_text())
        errors = module.check(template)
        self.assertTrue(any("graph.flow" in x for x in errors))
        self.assertTrue(any("field_parity" in x for x in errors))

    def test_raw_valid_but_cannot_claim_read_or_bound_sender(self):
        data = valid()
        self.assertEqual(module.check(data), [])
        data["case"]["read_state"] = "Read"
        data["case"]["authority"]["bound_flow"] = "forged-flow"
        errors = module.check(data)
        self.assertTrue(any("Raw cannot claim" in x for x in errors))
        self.assertTrue(any("Raw transport" in x for x in errors))

    def test_locked_ambiguous_attempt_stays_held(self):
        data = valid("FlowLocked")
        self.assertEqual(module.check(data), [])
        data["case"].update(transport_state="Ambiguous", confirmed_release=False, held_after_restart=True)
        self.assertEqual(module.check(data), [])
        data["case"]["confirmed_release"] = True
        self.assertTrue(any("ambiguous attempt" in x for x in module.check(data)))

    def test_locked_confirmed_requires_target_evidence(self):
        data = valid("FlowLocked")
        data["case"]["target_delivery_receipt"] = None
        self.assertTrue(any("target_delivery_receipt" in x for x in module.check(data)))

    def test_wrong_guest_extra_recipient_and_lost_post_snapshot_event_refuse(self):
        data = valid()
        data["target"]["host"] = "ouranos"
        data["case"]["recipient_count"] = 2
        data["rollback"]["retained_events"] = []
        errors = module.check(data)
        self.assertTrue(any("reserved Prometheus" in x for x in errors))
        self.assertTrue(any("exactly one" in x for x in errors))
        self.assertTrue(any("loses post-checkpoint" in x for x in errors))

    def test_build_runtime_hash_mismatch_refuses(self):
        data = copy.deepcopy(valid())
        data["artifacts"]["message"]["running_sha256"] = "c" * 64
        self.assertTrue(any("differs from immutable build" in x for x in module.check(data)))


if __name__ == "__main__":
    unittest.main()
