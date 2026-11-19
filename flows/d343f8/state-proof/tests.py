#!/nix/store/bya4ansy58az5133kryqp2cvrxbnz8qy-python3-3.14.10/bin/python3.14
"""Unpaid local fixtures for the frozen system-state proof."""
from __future__ import annotations

import json
import tempfile
import time
import unittest
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

import proof


class ParserFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.config = proof.load_configuration()["collection"]

    def test_datom_keeps_guillemet_escape_inside_string(self) -> None:
        parsed = proof.parse_datom("«q [ secret \\» still secret»", 100, 20)
        self.assertEqual(parsed.value, "q [ secret » still secret")

    def test_queue_parser_counts_without_retaining_payload(self) -> None:
        raw = 'Queues.[ { { Mind topic Haiku } [ «hidden {payload} \\» marker» «other» ] } ]'.encode()
        result = proof.parse_queues(raw, self.config)
        self.assertEqual(result["queue_count"], 1)
        self.assertEqual(result["pending_message_count"], 2)
        self.assertNotIn("hidden", json.dumps(result))
        self.assertEqual(result["queues"][0]["address"], ["Mind", "topic", "Haiku"])

    def test_queue_wrong_shape_is_unknown(self) -> None:
        with self.assertRaisesRegex(proof.ProofError, "QueuesShapeUnknown"):
            proof.parse_queues("Queues.[ { { Mind topic } [ «x» ] } ]".encode(), self.config)

    def test_queue_malformed_text_does_not_guess_with_braces(self) -> None:
        with self.assertRaises(proof.ProofError):
            proof.parse_queues("Queues.[ { not a real queue [ «x» ] } ]".encode(), self.config)

    def test_flow_identity_parser_retains_only_typed_identity_and_ui_status(self) -> None:
        raw = json.dumps({"result": {"agents": [{
            "agent_status": "working",
            "display_agent": "{ Mind psyche Sol id-1 }",
            "terminal_title_stripped": "{ Mind psyche Sol id-1 }",
            "transcript": "private text must not be retained",
        }]}}).encode()
        result = proof.parse_herdr(raw, self.config)
        self.assertEqual(result["ui_status_counts"]["working"], 1)
        self.assertEqual(result["flows"][0]["identity"], ["Mind", "psyche", "Sol", "id-1"])
        self.assertNotIn("private text", json.dumps(result))
        self.assertIn("not establish task health", result["status_semantics"])

    def test_energy_legacy_shape_keeps_pace_labels_and_opaque_trailing_values(self) -> None:
        raw = ("Read.{ { Claude True [ { Week 65 1795266000 10080 } ] [] 1795067528 } "
               "[ { Claude Week SpendBy.{24 92}72 65 Under 31 31.1 0.87 } ] Held }").encode()
        result = proof.parse_energy(raw, self.config)
        self.assertEqual(result["provider"], "Claude")
        self.assertEqual(result["windows"][0]["used_percent"], "65")
        self.assertEqual(result["pace"][0]["standing"], "Under")
        self.assertEqual(result["pace"][0]["legacy_trailing_values"], ["31", "31.1", "0.87"])
        self.assertNotIn("Held", json.dumps(result))

    def test_host_load_is_not_cpu_utilization(self) -> None:
        result = proof.parse_host(b"loadavg=0.13 0.12 0.04 1/824 123\ncpu_count=32\n",
                                  {"host_name": "fixture"})
        self.assertEqual(result["one_minute_load_per_cpu"], "0.004")
        self.assertIn("not current CPU utilization", result["metric_semantics"])


class AnswerAndBudgetFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.config = proof.load_configuration()

    def test_answered_typed_json_accepts_single_enum_values(self) -> None:
        raw = json.dumps({"kind": "Answered", "answer": {
            "flow_load": "Unknown", "energy_use": "Appropriate", "reason": "Snapshot has no baseline."}})
        decoded = proof.decode_task_answer(raw, self.config)
        self.assertEqual(decoded["kind"], "Answered")

    def test_task_refusal_is_distinct(self) -> None:
        raw = json.dumps({"kind": "Refused", "reason": "Evidence is insufficient."})
        self.assertEqual(proof.decode_task_answer(raw, self.config)["kind"], "TaskRefused")

    def test_combined_pipe_enum_is_malformed(self) -> None:
        raw = json.dumps({"kind": "Answered", "answer": {
            "flow_load": "TooMany|Appropriate|TooFew|Unknown",
            "energy_use": "Unknown", "reason": "No."}})
        self.assertEqual(proof.decode_task_answer(raw, self.config)["reason_code"], "flow_loadInvalid")

    def test_unknown_fields_and_empty_reason_are_malformed(self) -> None:
        extra = json.dumps({"kind": "Answered", "answer": {
            "flow_load": "Unknown", "energy_use": "Unknown", "reason": "ok", "extra": 1}})
        empty = json.dumps({"kind": "Refused", "reason": "   "})
        self.assertEqual(proof.decode_task_answer(extra, self.config)["kind"], "MalformedAnswer")
        self.assertEqual(proof.decode_task_answer(empty, self.config)["kind"], "MalformedAnswer")

    def test_non_json_and_nonfinite_numbers_are_malformed(self) -> None:
        self.assertEqual(proof.decode_task_answer("not-json", self.config)["kind"], "MalformedAnswer")
        self.assertEqual(proof.decode_task_answer('{"kind":"Answered","answer":NaN}', self.config)["kind"],
                         "MalformedAnswer")

    def test_duplicate_top_level_and_nested_keys_are_malformed(self) -> None:
        duplicate_kind = '{"kind":"Refused","kind":"Answered","answer":{}}'
        duplicate_field = ('{"kind":"Answered","answer":{"flow_load":"Unknown",'
                           '"flow_load":"TooMany","energy_use":"Unknown","reason":"x"}}')
        self.assertEqual(proof.decode_task_answer(duplicate_kind, self.config)["kind"], "MalformedAnswer")
        self.assertEqual(proof.decode_task_answer(duplicate_field, self.config)["kind"], "MalformedAnswer")

    def test_installed_policy_calculates_expected_per_model_bounds(self) -> None:
        profile = proof._validate_policy_bounds(self.config, b"short fixture prompt")
        self.assertEqual(profile["maximum_total_reservation_usd"], "2.904192")
        self.assertEqual(Decimal(profile["model_profiles"]["claude-haiku-5-5"]["maximum_usd"]), Decimal("0.66560"))
        self.assertEqual(Decimal(profile["model_profiles"]["claude-sonnet-5-5"]["maximum_usd"]), Decimal("2.138112"))
        self.assertEqual(Decimal(profile["model_profiles"]["claude-opus-5-5"]["maximum_usd"]), Decimal("0.10048"))

    def test_worker_system_prompt_is_exact_frozen_worker_prompt(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["task"]["system_prompt"] += " extra"
        with self.assertRaisesRegex(proof.ProofError, "WorkerSystemPromptMismatch"):
            proof._validate_policy_bounds(config, b"short")

    def test_model_token_drift_fails_closed(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["budget"]["model_bounds"]["claude-haiku-5-5"]["maximum_input_tokens"] -= 1
        with self.assertRaisesRegex(proof.ProofError, "ModelTokenBoundDrift"):
            proof._validate_policy_bounds(config, b"short")

    def test_exact_three_model_contract_rejects_injection_or_reorder(self) -> None:
        slots = [{"slot_id": f"slot-{i:02d}", "model": model}
                 for i, model in enumerate(self.config["budget"]["model_order"], 1)]
        proof.validate_slot_contract(slots, self.config)
        for altered in (slots + [{"slot_id": "slot-04", "model": "extra"}], list(reversed(slots))):
            with self.assertRaises(proof.ProofError):
                proof.validate_slot_contract(altered, self.config)

    def test_full_reservation_is_checked_before_any_child(self) -> None:
        emissions = [proof.Emission(f"slot-{i}", model, Path("prompt"), "0" * 64,
                                    self.config["budget"]["model_bounds"][model]["maximum_usd"], 1)
                     for i, model in enumerate(self.config["budget"]["model_order"], 1)]
        proof.preflight_budget(emissions, "10.00", "10.00")
        child_calls: list[str] = []
        with self.assertRaisesRegex(proof.ProofError, "ResearchGlobalHeadroomInsufficient"):
            proof.preflight_budget(emissions, "10.00", "2.904191")
        self.assertEqual(child_calls, [])

    def test_drift_guards_reject_changed_inputs_and_closure(self) -> None:
        with self.assertRaisesRegex(proof.ProofError, "InputDrift"):
            proof.verify_digest(b"changed", "0" * 64, "InputDrift")
        with self.assertRaisesRegex(proof.ProofError, "ExecutionClosureDrift"):
            proof.enforce_closure_match({"x": "a"}, {"x": "b"})


class OnceOnlyAndDurabilityFixtures(unittest.TestCase):
    def setUp(self) -> None:
        self.configuration = proof.load_configuration()

    def emissions(self) -> list[proof.Emission]:
        budget = self.configuration["budget"]
        return [proof.Emission(f"slot-{index:02d}", model, Path("fixture.prompt"), "a" * 64,
                               budget["model_bounds"][model]["maximum_usd"], 1)
                for index, model in enumerate(budget["model_order"], 1)]

    def admission(self, headroom: str = "10.00") -> dict[str, str]:
        return {"run_namespace": "00000000-0000-4000-8000-000000000001",
                "global_unreserved_usd": headroom}

    def test_launch_lock_rejects_concurrent_instance(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / "launch.lock"
            first = proof._lock_file(lock)
            try:
                with self.assertRaisesRegex(proof.ProofError, "LaunchAlreadyActive"):
                    proof._lock_file(lock)
            finally:
                import os
                os.close(first)

    def test_existing_namespace_is_a_terminal_restart_refusal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            namespace = Path(directory) / self.admission()["run_namespace"]
            namespace.mkdir()
            with self.assertRaisesRegex(proof.ProofError, "RunNamespaceAlreadyExists"):
                proof.durable_mkdir(namespace, must_be_new=True)

    def test_run_and_slot_intents_are_durable_before_child_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            event_log: list[str] = []
            original_mkdir = proof.durable_mkdir
            original_write = proof.write_durable_new

            def mkdir(path: Path, *, must_be_new: bool) -> None:
                original_mkdir(path, must_be_new=must_be_new)
                event_log.append(f"dir-durable:{path.name}")

            def write(path: Path, data: bytes) -> None:
                original_write(path, data)
                event_log.append(f"file-durable:{path.name}")

            def invoke(emission: proof.Emission, _config: dict[str, object]) -> dict[str, str]:
                event_log.append(f"child:{emission.slot_id}")
                return {"kind": "Answered", "accounting_state": "Settled", "unreserved_usd": "10.00"}

            with patch.object(proof, "durable_mkdir", side_effect=mkdir), \
                    patch.object(proof, "write_durable_new", side_effect=write):
                result = proof._run_admitted_once(self.configuration, {}, "b" * 64,
                                                   self.admission(), self.emissions()[:1],
                                                   invoke=invoke, validate_before_child=lambda _emission: None,
                                                   results_root=Path(directory) / "results")
            self.assertEqual(result["state"], "Complete")
            child_index = event_log.index("child:slot-01")
            self.assertEqual(event_log[:child_index], [
                "dir-durable:results", "dir-durable:00000000-0000-4000-8000-000000000001",
                "file-durable:run-intent.json", "dir-durable:slot-01", "file-durable:intent.json",
            ])

    def test_budget_failure_never_reaches_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            called: list[str] = []
            result = proof._run_admitted_once(self.configuration, {}, "c" * 64,
                self.admission("0.50"), self.emissions(),
                invoke=lambda emission, _config: called.append(emission.slot_id) or {},
                validate_before_child=lambda _emission: None,
                results_root=Path(directory) / "results")
            self.assertEqual(result["state"], "StoppedBudgetAdmission")
            self.assertEqual(called, [])

    def test_settled_slot_with_less_headroom_stops_before_next_full_bound(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            called: list[str] = []
            def settled(emission: proof.Emission, _config: dict[str, object]) -> dict[str, str]:
                called.append(emission.slot_id)
                return {"kind": "Answered", "accounting_state": "Settled", "unreserved_usd": "0.50"}
            result = proof._run_admitted_once(self.configuration, {}, "d" * 64,
                self.admission("10.00"), self.emissions(), invoke=settled,
                validate_before_child=lambda _emission: None,
                results_root=Path(directory) / "results")
            self.assertEqual(called, ["slot-01"])
            self.assertEqual(result["state"], "StoppedBudgetAdmission")
            self.assertEqual(result["stopped_before_slot"], "slot-02")

    def test_uncertain_transport_stops_without_retry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            called: list[str] = []
            def uncertain(emission: proof.Emission, _config: dict[str, object]) -> dict[str, str]:
                called.append(emission.slot_id)
                return {"kind": "TransportOrAccountingUncertain", "accounting_state": "Uncertain"}
            result = proof._run_admitted_once(self.configuration, {}, "e" * 64,
                self.admission(), self.emissions(), invoke=uncertain,
                validate_before_child=lambda _emission: None,
                results_root=Path(directory) / "results")
            self.assertEqual(called, ["slot-01"])
            self.assertEqual(result["state"], "StoppedTransportOrAccountingUncertain")

    def test_settled_truncation_stops_without_retry(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            called: list[str] = []
            def truncated(emission: proof.Emission, _config: dict[str, object]) -> dict[str, str]:
                called.append(emission.slot_id)
                return {"kind": "TruncatedOutput", "accounting_state": "Settled",
                        "unreserved_usd": "9.30"}
            result = proof._run_admitted_once(self.configuration, {}, "f" * 64,
                self.admission(), self.emissions(), invoke=truncated,
                validate_before_child=lambda _emission: None,
                results_root=Path(directory) / "results")
            self.assertEqual(called, ["slot-01"])
            self.assertEqual(result["state"], "StoppedTruncatedOrIncompleteOutput")

    def test_drift_between_slots_stops_before_second_child(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            called: list[str] = []
            def validate(emission: proof.Emission) -> None:
                if emission.slot_id == "slot-02":
                    raise proof.ProofError("FrozenPromptDrift")
            def settled(emission: proof.Emission, _config: dict[str, object]) -> dict[str, str]:
                called.append(emission.slot_id)
                return {"kind": "Answered", "accounting_state": "Settled", "unreserved_usd": "10.00"}
            result = proof._run_admitted_once(self.configuration, {}, "f" * 64,
                self.admission(), self.emissions(), invoke=settled,
                validate_before_child=validate, results_root=Path(directory) / "results")
            self.assertEqual(called, ["slot-01"])
            self.assertEqual(result["state"], "StoppedFrozenInputDrift")
            self.assertEqual(result["stopped_before_slot"], "slot-02")

    def test_native_and_task_refusal_are_distinct_receipt_outcomes(self) -> None:
        emission = self.emissions()[0]
        settled = {"result": {"stop_reason": "end_turn", "answer": '{"kind":"Refused","reason":"Missing facts"}'},
                   "accounting_state": "Settled", "retained_usd": "0.01", "unreserved_usd": "9.99",
                   "receipt_sha256": "a" * 64, "directory": Path("fixture"), "ledger": {"ordinal": 1}}
        with patch.object(proof, "_read_worker_receipt", return_value=settled), \
                patch.object(proof, "_provider_refusal_in_response", return_value=False):
            task = proof._receipt_observation(0, b"report", b"", False, emission, self.configuration)
        self.assertEqual(task["kind"], "TaskRefused")
        native = dict(settled)
        native["result"] = {"stop_reason": "refusal", "answer": None}
        with patch.object(proof, "_read_worker_receipt", return_value=native), \
                patch.object(proof, "_provider_refusal_in_response", return_value=False):
            refusal = proof._receipt_observation(0, b"report", b"", False, emission, self.configuration)
        self.assertEqual(refusal["kind"], "ProviderNativeRefusal")

    def test_malformed_answer_and_transport_uncertainty_are_distinct(self) -> None:
        emission = self.emissions()[0]
        settled = {"result": {"stop_reason": "end_turn", "answer": "not JSON"},
                   "accounting_state": "Settled", "retained_usd": "0.01", "unreserved_usd": "9.99",
                   "receipt_sha256": "a" * 64, "directory": Path("fixture"), "ledger": {"ordinal": 1}}
        with patch.object(proof, "_read_worker_receipt", return_value=settled), \
                patch.object(proof, "_provider_refusal_in_response", return_value=False):
            malformed = proof._receipt_observation(0, b"report", b"", False, emission, self.configuration)
        timeout = proof._receipt_observation(None, b"", b"", False, emission, self.configuration)
        self.assertEqual(malformed["kind"], "MalformedAnswer")
        self.assertEqual(timeout["kind"], "TransportOrAccountingUncertain")
        self.assertEqual(timeout["held_bound_usd"], emission.maximum_usd)

    def test_settled_max_tokens_partial_json_is_truncated_not_answered(self) -> None:
        emission = self.emissions()[0]
        partial = json.dumps({"kind": "Answered", "answer": {
            "flow_load": "Unknown", "energy_use": "Unknown", "reason": "complete-looking partial"}})
        receipt = {"result": {"state": "Truncated", "stop_reason": "max_tokens", "answer": partial,
                              "usage": {"input_tokens": 10, "output_tokens": 20},
                              "estimated_cost_usd": "0.001"},
                   "accounting_state": "Settled", "retained_usd": "0.001", "unreserved_usd": "9.999",
                   "receipt_sha256": "c" * 64, "directory": Path("fixture"), "ledger": {"ordinal": 1}}
        with patch.object(proof, "_read_worker_receipt", return_value=receipt), \
                patch.object(proof, "_provider_refusal_in_response", return_value=False):
            result = proof._receipt_observation(0, b"report", b"", False, emission, self.configuration)
        self.assertEqual(result["kind"], "TruncatedOutput")
        self.assertEqual(result["accounting_state"], "Settled")
        self.assertEqual(result["partial_answer_sha256"], proof.sha256_bytes(partial.encode()))

    def test_public_run_has_no_result_path_override_and_requires_admission(self) -> None:
        import inspect
        self.assertEqual(list(inspect.signature(proof.run_campaign).parameters), [])
        from contextlib import redirect_stdout
        import io
        output = io.StringIO()
        with redirect_stdout(output):
            result = proof.main(["run", "--results-root", "/tmp/redirect"])
        self.assertEqual(result, 2)
        self.assertIn('"reason_code": "Usage"', output.getvalue())

    def test_source_observation_must_remain_fresh_at_freeze_and_run(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            snapshot_path = Path(directory) / "snapshot.json"
            captured = int(time.time())
            snapshot = {"format": "SystemStateProofSnapshot.v1", "captured_epoch": captured,
                        "sources": {"energy_codex": {"state": "Available",
                            "facts": {"observed_epoch": captured - 3601}}}}
            snapshot_path.write_bytes(proof.canonical_json(snapshot))
            with patch.object(proof, "SNAPSHOT_PATH", snapshot_path):
                with self.assertRaisesRegex(proof.ProofError, "SnapshotSourceStale"):
                    proof._read_existing_snapshot(self.configuration)


if __name__ == "__main__":
    unittest.main(verbosity=2)
