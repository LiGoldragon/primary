"""Unpaid synthetic checks; no processor or provider is invoked."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import controller


CAMPAIGN_ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = CAMPAIGN_ROOT / "proposal-manifest.json"


def synthetic_admission(path: Path, global_unreserved: str = "30") -> Path:
    manifest = controller.verify_manifest(MANIFEST_PATH)
    admission = {
        "authority": "Research",
        "status": "Admitted",
        "admission_id": "synthetic-fixture-only",
        "manifest_sha256": controller.sha256_file(MANIFEST_PATH),
        "slot_count": manifest["campaign_limits"]["maximum_provider_calls"],
        "campaign_limit_usd": manifest["campaign_limits"]["maximum_campaign_retained_usd"],
        "global_unreserved_usd": global_unreserved,
        "synthetic_fixture": True,
    }
    path.write_text(json.dumps(admission), encoding="utf-8")
    return path


def valid_answer_for_task(slot: dict) -> dict:
    if slot["task_kind"] == "Admission":
        return {"kind": "Admission", "judgment": {"kind": "Admitted", "wording": "fixture"}}
    return {"kind": "Queue", "judgment": {"kind": "KeepQueued", "reason": "fixture"}}


def synthetic_observation(slot: dict, bound: str, kind: str = "Answered", stop_reason: str = "end_turn",
                          receipt_override: dict | None = None, artifact_parent: Path | None = None,
                          task_answer: dict | None = None, raw_answer: str | None = None,
                          native_text_blocks: list[str] | None = None,
                          native_thinking: bool = False) -> dict:
    artifact = Path(tempfile.mkdtemp(prefix="typed-call-local-receipt-", dir=artifact_parent))
    native = {"model": slot["model"], "stop_reason": stop_reason}
    if task_answer is not None:
        answer_text = json.dumps(task_answer, separators=(",", ":"))
    elif raw_answer is not None:
        answer_text = raw_answer
    else:
        answer_text = None
    if answer_text is not None:
        content = []
        if native_thinking:
            content.append({"type": "thinking", "thinking": "", "signature": "fixture-signature"})
        for part in native_text_blocks or [answer_text]:
            content.append({"type": "text", "text": part})
        native["content"] = content
        answer_text = "".join(native_text_blocks or [answer_text])
    (artifact / "response.json").write_text(json.dumps(native), encoding="utf-8")
    receipt = {
        "artifact_directory": str(artifact),
        "result": {
            "state": "Succeeded",
            "settlement_appended": True,
            "job": "fixture-job-001",
            "usage": {"input_tokens": 1, "output_tokens": 1},
            "estimated_cost_usd": "0.001",
            "answer": answer_text,
        },
        "ledger": {
            "job": "fixture-job-001",
            "reservation_usd": bound,
            "retained_usd": "0.001",
            "unreserved_usd": "29.999",
        },
    }
    if receipt_override is not None:
        receipt = receipt_override
    return {
        "elapsed_milliseconds": 1,
        "processor_exit": 0,
        "receipt": receipt,
        "outcome": {"kind": kind, **({"reason": task_answer["reason"]} if kind == "ModelRefused" and task_answer else {})},
    }


class FrozenCampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = controller.verify_manifest(MANIFEST_PATH)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="december-controller-fixture-")
        self.root = Path(self.temporary.name)
        self.output = self.root / "results"
        self.admission = synthetic_admission(self.root / "admission.json")

    def tearDown(self):
        self.temporary.cleanup()

    def test_fixed_count_task_mix_and_model_counts(self):
        slots = self.manifest["slots"]
        self.assertEqual(len(slots), self.manifest["campaign_limits"]["maximum_provider_calls"])
        self.assertEqual(self.manifest["slot_category_counts"], {
            "historical_variance": 312,
            "malformed_probe": 12,
            "missing_evidence": 12,
        })
        self.assertEqual(self.manifest["model_slot_counts"], {
            "claude-haiku-5-5": 112,
            "claude-opus-5-5": 112,
            "claude-sonnet-5-5": 112,
        })
        cases = self.manifest["slot_contract"]["historical"]["cases_by_task"]
        self.assertEqual(len(cases["Admission"]), 22)
        self.assertEqual(len(cases["Queue"]), 30)
        all_cases = {case for group in cases.values() for case in group}
        self.assertTrue(all_cases.isdisjoint(self.manifest["slot_contract"]["excluded_scoped_historical_cases"]))

    def test_installed_execution_closure_is_frozen_and_ledger_is_separate(self):
        closure = self.manifest["execution_closure"]
        frozen = {item["path"] for item in self.manifest["frozen_files"]}
        guards = set(self.manifest["runtime_guard_files"])
        closure_paths = {
            item["path"]
            for group in ("worker_python_sources", "static_inputs", "executables")
            for item in closure[group]
        }
        self.assertTrue(closure_paths <= frozen)
        self.assertTrue(closure_paths <= guards)
        module_names = {Path(item["path"]).name for item in closure["worker_python_sources"]}
        self.assertTrue({"general_adapter.py", "raw_adapter.py", "raw_ledger.py", "ledger.py",
                         "policy.py", "model_policy.py", "settlement_evidence.py", "producer_guard.py"}
                        <= module_names)
        static_roles = {item["role"] for item in closure["static_inputs"]}
        self.assertEqual(static_roles, {"general_worker_policy", "native_worker_policy", "settlement_policy",
                                        "historical_evidence_manifest", "transport_ca_bundle"})
        executable_roles = {item["role"] for item in closure["executables"]}
        self.assertEqual(executable_roles, {"controller_interpreter", "processor_interpreter",
                                            "producer_guard_interpreter", "curl", "bubblewrap",
                                            "credential_producer"})
        ledger_path = closure["mutable_accounting_input"]["ledger_path"]
        self.assertNotIn(ledger_path, frozen)
        self.assertEqual(closure["mutable_accounting_input"]["validation_owner"],
                         "pinned worker and Research ledger; ledger content is not frozen here")

    def test_controller_interpreter_identity_accepts_equivalent_symlink_spelling(self):
        target = Path(sys.executable).resolve(strict=True)
        alias = self.root / "controller-python-alias"
        alias.symlink_to(target)
        alias_identity = controller.executable_identity("controller_interpreter", alias)
        target_identity = controller.executable_identity("controller_interpreter", target)
        self.assertEqual(alias_identity, target_identity)
        self.assertEqual(alias_identity["configured_path"], str(target))

    def test_manifest_cannot_omit_a_runtime_execution_source(self):
        changed = deepcopy(self.manifest)
        changed["execution_closure"]["worker_python_sources"].pop()
        changed["canonical_sha256"] = controller.canonical_sha256(
            {key: value for key, value in changed.items() if key != "canonical_sha256"})
        with self.assertRaisesRegex(controller.CampaignError, "closure differs"):
            controller.verify_manifest(MANIFEST_PATH, changed)

    def test_extra_slot_injection_fails_hard_count(self):
        changed = deepcopy(self.manifest)
        changed["slots"].append(deepcopy(changed["slots"][0]))
        changed["canonical_sha256"] = controller.canonical_sha256({k: v for k, v in changed.items()
                                                                    if k != "canonical_sha256"})
        with self.assertRaisesRegex(controller.CampaignError, "slot count differs"):
            controller.verify_manifest(MANIFEST_PATH, changed)

    def test_worker_reservation_formula_matches_each_model_bound(self):
        expected = {
            "claude-haiku-5-5": "0.6656",
            "claude-sonnet-5-5": "2.138112",
            "claude-opus-5-5": "0.10048",
        }
        for model, bound in expected.items():
            profile = self.manifest["model_bounds"][model]
            self.assertEqual(profile["reservation_bound_usd"], bound)
            self.assertEqual(str(controller.reservation_bound(profile)), bound)

    def test_effective_model_bound_drift_is_detected(self):
        changed = deepcopy(self.manifest)
        changed["model_bounds"]["claude-haiku-5-5"]["maximum_output_tokens"] += 1
        changed["canonical_sha256"] = controller.canonical_sha256({k: v for k, v in changed.items()
                                                                    if k != "canonical_sha256"})
        with self.assertRaisesRegex(controller.CampaignError, "effective model reservation"):
            controller.verify_manifest(MANIFEST_PATH, changed)

    def test_prompt_and_policy_file_hash_drift_helpers_fail_closed(self):
        drift = self.root / "drift.txt"
        drift.write_text("changed", encoding="utf-8")
        with self.assertRaisesRegex(controller.CampaignError, "prompt drift"):
            controller.require_file_digest(drift, "0" * 64, "prompt")
        with self.assertRaisesRegex(controller.CampaignError, "policy drift"):
            controller.require_file_digest(drift, "0" * 64, "policy")

    def test_runtime_prompt_policy_and_manifest_drift_fails_before_call(self):
        root = self.root / "runtime-fixture"
        root.mkdir()
        manifest_path = root / "manifest.json"
        call_path = root / "call.json"
        prompt_path = root / "prompt.txt"
        policy_path = root / "policy.json"
        call_path.write_text("{}", encoding="utf-8")
        prompt_path.write_bytes(b"prompt")
        policy_path.write_text("{\"policy\":1}", encoding="utf-8")
        manifest_path.write_text("frozen manifest", encoding="utf-8")
        manifest_hash = controller.sha256_file(manifest_path)
        slot = {
            "identifier": "fixture-slot",
            "call_file": "call.json",
            "call_sha256": controller.sha256_file(call_path),
            "prompt_file": "prompt.txt",
            "prompt_sha256": controller.sha256_file(prompt_path),
        }
        frozen = {str(policy_path.resolve()): controller.sha256_file(policy_path)}
        manifest = {
            "frozen_files": [{"path": str(policy_path), "sha256": frozen[str(policy_path.resolve())]}],
            "runtime_guard_files": [str(policy_path)],
            "execution_closure": self.manifest["execution_closure"],
            "worker_policy_file": self.manifest["worker_policy_file"],
            "processor_configuration": self.manifest["processor_configuration"],
        }
        self.assertEqual(controller.verify_runtime_slot(manifest_path, manifest, slot, manifest_hash), call_path)

        prompt_path.write_bytes(b"changed prompt")
        with self.assertRaisesRegex(controller.CampaignError, "call input|prompt input drift"):
            controller.verify_runtime_slot(manifest_path, manifest, slot, manifest_hash)
        slot["call_sha256"] = controller.sha256_file(call_path)
        with self.assertRaisesRegex(controller.CampaignError, "prompt input drift"):
            controller.verify_runtime_slot(manifest_path, manifest, slot, manifest_hash)
        prompt_path.write_bytes(b"prompt")

        manifest["frozen_files"] = [{"path": str(policy_path), "sha256": frozen[str(policy_path.resolve())]}]
        policy_path.write_text("{\"policy\":2}", encoding="utf-8")
        with self.assertRaisesRegex(controller.CampaignError, "runtime source drift"):
            controller.verify_runtime_slot(manifest_path, manifest, slot, manifest_hash)
        manifest_path.write_text("changed manifest", encoding="utf-8")
        with self.assertRaisesRegex(controller.CampaignError, "manifest drift"):
            controller.verify_runtime_slot(manifest_path, manifest, slot, manifest_hash)

    def test_all_opus_prompts_fit_default_byte_system_frame_limit(self):
        profile = self.manifest["model_bounds"]["claude-opus-5-5"]["input_admission"]
        self.assertEqual(profile["system_utf8_bytes"], 150)
        self.assertEqual(profile["framing_allowance"], 1024)
        self.assertEqual(profile["conservative_input_limit"], 20000)
        for slot in self.manifest["slots"]:
            if slot["model"] == "claude-opus-5-5":
                self.assertLessEqual(slot["conservative_input_bytes"], 20000)

    def test_variance_replicates_reuse_exact_prompt_hash_and_reference_baseline(self):
        slots = [slot for slot in self.manifest["slots"] if slot["category"] == "historical_variance"]
        by_case_model = {}
        for slot in slots:
            key = (slot["case_id"], slot["model"])
            by_case_model.setdefault(key, {})[slot["replicate"]] = slot
        self.assertEqual(len(by_case_model), 52 * 3)
        for replicate_map in by_case_model.values():
            self.assertEqual(set(replicate_map), {1, 2})
            self.assertEqual(replicate_map[1]["prompt_sha256"], replicate_map[2]["prompt_sha256"])
            self.assertEqual(set(replicate_map[1]["baseline_receipt_refs"]), set(self.manifest["slot_contract"]["models"]))

    def test_missing_evidence_is_explicit_and_has_no_asserted_answer(self):
        slots = [slot for slot in self.manifest["slots"] if slot["category"] == "missing_evidence"]
        self.assertEqual(len(slots), 12)
        self.assertTrue(all(slot["expected_semantic_label"] is None for slot in slots))
        for slot in slots:
            self.assertTrue(slot["withheld_inputs"])
            self.assertIn("withheld", slot["instruction"].lower())

    def test_malformed_probe_uses_declared_incompatible_output_shape(self):
        slots = [slot for slot in self.manifest["slots"] if slot["category"] == "malformed_probe"]
        self.assertEqual(len(slots), 12)
        self.assertTrue(all(slot["output_format_perturbation"]["decoder_changed"] is False for slot in slots))
        self.assertTrue(all(slot["output_format_perturbation"]["decoder_expected_to_reject"] is True for slot in slots))

    def test_campaign_dry_budget_guard_runs_before_child(self):
        first_bound = self.manifest["slots"][0]["reservation_bound_usd"]
        synthetic_admission(self.admission, str(controller.decimal(first_bound, "bound") / 2))
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout=b"{}")

        with self.assertRaisesRegex(controller.CampaignError, "GlobalReservationDoesNotFit"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(calls, [])
        self.assertTrue((self.output / "stopped.json").is_file())

    def test_each_next_full_reservation_must_fit_campaign_retained_envelope(self):
        calls = []
        remaining_global = [controller.decimal(self.manifest["campaign_limits"]["maximum_campaign_retained_usd"], "limit") + 10]

        def runner(args, **kwargs):
            slot = self.manifest["slots"][len(calls)]
            bound = controller.decimal(slot["reservation_bound_usd"], "bound")
            calls.append(args)
            observation = synthetic_observation(slot, slot["reservation_bound_usd"], "Answered", "end_turn",
                                                artifact_parent=self.root, task_answer=valid_answer_for_task(slot))
            remaining_global[0] -= bound
            observation["receipt"]["ledger"]["retained_usd"] = str(bound)
            observation["receipt"]["ledger"]["unreserved_usd"] = str(remaining_global[0])
            return SimpleNamespace(returncode=0, stdout=json.dumps(observation).encode())

        with self.assertRaisesRegex(controller.CampaignError, "CampaignReservationDoesNotFit"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        stopped = json.loads((self.output / "stopped.json").read_text())
        self.assertGreater(len(calls), 0)
        self.assertLess(len(calls), self.manifest["campaign_limits"]["maximum_provider_calls"])
        self.assertEqual(stopped["completed_slots"], len(calls))
        self.assertTrue(stopped["no_call_for_next_slot"])

    def test_research_admission_bounds_must_equal_manifest(self):
        admission = json.loads(self.admission.read_text())
        admission["campaign_limit_usd"] = "19.99"
        self.admission.write_text(json.dumps(admission))
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout=b"{}")

        with self.assertRaisesRegex(controller.CampaignError, "campaign envelope differs"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(calls, [])
        self.assertFalse(self.output.exists())

    def test_production_api_cannot_redirect_admission_to_a_fresh_marker_directory(self):
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout=b"{}")

        with self.assertRaises(TypeError):
            controller.run_campaign(MANIFEST_PATH, self.admission,
                                    output_directory=self.output, process_runner=runner)
        self.assertEqual(calls, [])
        self.assertFalse(self.output.exists())

    def test_concurrent_launch_refuses_before_child(self):
        self.output.mkdir()
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout=b"{}")

        with controller.exclusive_launch_lock(controller.launch_lock_path(self.output)):
            with self.assertRaisesRegex(controller.CampaignError, "exclusive lock"):
                controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(calls, [])

    def test_namespace_and_slot_intent_directories_are_durable_before_child(self):
        first_slot = self.manifest["slots"][0]
        first_bound = controller.decimal(first_slot["reservation_bound_usd"], "first bound")
        synthetic_admission(self.admission, str(first_bound))
        events = []
        original_fsync = controller.fsync_directory
        original_durable_json = controller.durable_json
        calls = []

        def tracked_fsync(path):
            resolved = Path(path).resolve(strict=True)
            events.append(("fsync", resolved))
            original_fsync(path)

        def tracked_json(path, value, exclusive=True):
            result = original_durable_json(path, value, exclusive)
            events.append(("json", Path(path).name, Path(path).parent.resolve()))
            return result

        def runner(args, **kwargs):
            calls.append(args)
            slot_directory = self.output / first_slot["identifier"]
            self.assertTrue((self.output / "run-started.json").is_file())
            self.assertTrue((slot_directory / "started.json").is_file())
            synced = {item[1] for item in events if item[0] == "fsync"}
            ancestor = slot_directory.resolve(strict=True)
            while True:
                self.assertIn(ancestor, synced, f"directory ancestor was not synced before child: {ancestor}")
                if ancestor.parent == ancestor:
                    break
                ancestor = ancestor.parent
            run_marker = events.index(("json", "run-started.json", self.output.resolve()))
            slot_marker = events.index(("json", "started.json", slot_directory.resolve()))
            self.assertLess(run_marker, slot_marker)
            events.append(("child",))
            observation = synthetic_observation(first_slot, first_slot["reservation_bound_usd"], "Answered",
                                                "end_turn", artifact_parent=self.root,
                                                task_answer=valid_answer_for_task(first_slot))
            retained = controller.decimal(observation["receipt"]["ledger"]["retained_usd"], "retained")
            observation["receipt"]["ledger"]["unreserved_usd"] = str(first_bound - retained)
            return SimpleNamespace(returncode=0, stdout=json.dumps(observation).encode())

        with patch.object(controller, "fsync_directory", tracked_fsync), \
                patch.object(controller, "durable_json", tracked_json):
            with self.assertRaisesRegex(controller.CampaignError, "GlobalReservationDoesNotFit"):
                controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(len(calls), 1)
        self.assertLess(events.index(("json", "started.json", (self.output / first_slot["identifier"]).resolve())),
                        events.index(("child",)))

    def test_directory_fsync_fault_prevents_child_and_slot_intent(self):
        first_slot = self.manifest["slots"][0]
        first_bound = controller.decimal(first_slot["reservation_bound_usd"], "first bound")
        synthetic_admission(self.admission, str(first_bound))
        slot_directory = self.output / first_slot["identifier"]
        original_fsync = controller.fsync_directory
        calls = []

        def fail_slot_directory(path):
            if Path(path).resolve() == slot_directory.resolve():
                raise controller.CampaignError("injected directory fsync failure")
            original_fsync(path)

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout=b"{}")

        with patch.object(controller, "fsync_directory", fail_slot_directory):
            with self.assertRaisesRegex(controller.CampaignError, "injected directory fsync failure"):
                controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(calls, [])
        self.assertTrue((self.output / "run-started.json").is_file())
        self.assertTrue(slot_directory.is_dir())
        self.assertFalse((slot_directory / "started.json").exists())

    def test_restart_after_started_marker_refuses_before_child(self):
        self.output.mkdir()
        controller.durable_json(self.output / "run-started.json", {"started_once": True})
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout=b"{}")

        with self.assertRaisesRegex(controller.CampaignError, "no restart or replay"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(calls, [])

    def test_timeout_holds_full_bound_and_restart_cannot_retry(self):
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            raise subprocess.TimeoutExpired(args[0], kwargs["timeout"])

        with self.assertRaisesRegex(controller.CampaignError, "full bound held"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(len(calls), 1)
        bound = self.manifest["slots"][0]["reservation_bound_usd"]
        uncertainty = json.loads((self.output / "uncertain.json").read_text(encoding="utf-8"))
        self.assertEqual(uncertainty["full_reservation_held_usd"], bound)
        with self.assertRaisesRegex(controller.CampaignError, "already started|uncertain attempt"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(len(calls), 1)

    def test_nonzero_processor_exit_is_uncertain_and_not_retried(self):
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=2, stdout=b"")

        with self.assertRaisesRegex(controller.CampaignError, "processor failed"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(len(calls), 1)
        self.assertTrue((self.output / "uncertain.json").is_file())

    def test_invalid_and_missing_receipts_hold_full_reservation(self):
        for stdout in (b"not-json", json.dumps({"processor_exit": 0, "receipt": None, "outcome": {"kind": "ProviderFailed"}}).encode()):
            with self.subTest(stdout=stdout):
                output = self.root / ("results-" + str(len(list(self.root.glob("results-*")))))

                def runner(*args, **kwargs):
                    return SimpleNamespace(returncode=0, stdout=stdout)

                with self.assertRaises(controller.CampaignError):
                    controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, output, runner)
                self.assertTrue((output / "uncertain.json").is_file())
                held = json.loads((output / "uncertain.json").read_text(encoding="utf-8"))
                self.assertEqual(held["full_reservation_held_usd"], self.manifest["slots"][0]["reservation_bound_usd"])

    def test_native_refusal_and_decoder_error_are_known_results(self):
        slot = self.manifest["slots"][0]
        bound = slot["reservation_bound_usd"]
        refusal = synthetic_observation(slot, bound, "ModelRefused", "refusal", artifact_parent=self.root)
        response_codec = self.manifest["model_bounds"][slot["model"]]["response_codec"]
        retained, unreserved, kind = controller.authoritative_receipt(
            refusal, slot, controller.decimal(bound, "bound"), response_codec)
        self.assertEqual(kind, "NativeRefusal")
        self.assertEqual(str(retained), "0.001")
        self.assertGreater(unreserved, 0)

        task_answer = {"kind": "Refused", "reason": "The controlled packet withholds essential evidence."}
        task_refusal = synthetic_observation(slot, bound, "ModelRefused", "end_turn", artifact_parent=self.root,
                                             task_answer=task_answer)
        _, _, kind = controller.authoritative_receipt(task_refusal, slot, controller.decimal(bound, "bound"), response_codec)
        self.assertEqual(kind, "TaskRefusal")

        invalid_task_refusal = synthetic_observation(slot, bound, "ModelRefused", "end_turn", artifact_parent=self.root,
                                                     raw_answer='{"kind":"Admission","judgment":{"kind":"Admitted","wording":"answer"}}')
        with self.assertRaisesRegex(controller.CampaignError, "valid task-level refusal"):
            controller.authoritative_receipt(invalid_task_refusal, slot, controller.decimal(bound, "bound"), response_codec)

        malformed = synthetic_observation(slot, bound, "Malformed", "end_turn", artifact_parent=self.root,
                                          raw_answer="{malformed json")
        _, _, kind = controller.authoritative_receipt(malformed, slot, controller.decimal(bound, "bound"), response_codec)
        self.assertEqual(kind, "Malformed")

        transport = {"processor_exit": 2, "receipt": None, "outcome": {"kind": "ProviderFailed"}}
        with self.assertRaisesRegex(controller.CampaignError, "processor exit"):
            controller.authoritative_receipt(transport, slot, controller.decimal(bound, "bound"), response_codec)

    def test_worker_answer_joining_handles_two_text_blocks_and_hidden_thinking(self):
        slot = next(slot for slot in self.manifest["slots"] if slot["model"] == "claude-opus-5-5")
        bound = slot["reservation_bound_usd"]
        codec = self.manifest["model_bounds"][slot["model"]]["response_codec"]
        refusal_answer = {"kind": "Refused", "reason": "The evidence was withheld."}
        refusal_text = json.dumps(refusal_answer, separators=(",", ":"))
        refusal_parts = [refusal_text[:17], refusal_text[17:]]
        task_refusal = synthetic_observation(slot, bound, "ModelRefused", "end_turn", artifact_parent=self.root,
                                             task_answer=refusal_answer, native_text_blocks=refusal_parts,
                                             native_thinking=True)
        _, _, kind = controller.authoritative_receipt(task_refusal, slot, controller.decimal(bound, "bound"), codec)
        self.assertEqual(kind, "TaskRefusal")

        answer = valid_answer_for_task(slot)
        answer_text = json.dumps(answer, separators=(",", ":"))
        answered = synthetic_observation(slot, bound, "Answered", "end_turn", artifact_parent=self.root,
                                         task_answer=answer, native_text_blocks=[answer_text[:12], answer_text[12:]],
                                         native_thinking=True)
        _, _, kind = controller.authoritative_receipt(answered, slot, controller.decimal(bound, "bound"), codec)
        self.assertEqual(kind, "Answered")

    def test_settled_task_refusal_is_distinct_and_campaign_can_continue(self):
        calls = []
        first = self.manifest["slots"][0]
        task_answer = {"kind": "Refused", "reason": "The controlled packet withholds essential evidence."}

        def runner(args, **kwargs):
            calls.append(args)
            if len(calls) == 1:
                observation = synthetic_observation(first, first["reservation_bound_usd"], "ModelRefused",
                                                    "end_turn", artifact_parent=self.root, task_answer=task_answer)
                return SimpleNamespace(returncode=0, stdout=json.dumps(observation).encode())
            return SimpleNamespace(returncode=2, stdout=b"native refusal or worker failure")

        with self.assertRaisesRegex(controller.CampaignError, "processor failed"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(len(calls), 2)
        first_measurement = json.loads((self.output / first["identifier"] / "measurement.json").read_text())
        self.assertEqual(first_measurement["outcome_kind"], "TaskRefusal")
        second = self.manifest["slots"][1]
        second_uncertainty = json.loads((self.output / second["identifier"] / "uncertain.json").read_text())
        self.assertEqual(second_uncertainty["full_reservation_held_usd"], second["reservation_bound_usd"])

    def test_native_refusal_worker_failure_holds_full_bound(self):
        calls = []

        def runner(args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=2, stdout=b"provider refusal did not settle")

        with self.assertRaisesRegex(controller.CampaignError, "processor failed"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(len(calls), 1)
        uncertainty = json.loads((self.output / "uncertain.json").read_text())
        self.assertEqual(uncertainty["full_reservation_held_usd"], self.manifest["slots"][0]["reservation_bound_usd"])

    def test_max_token_completion_is_recorded_as_truncation_then_stops(self):
        slot = self.manifest["slots"][0]
        bound = slot["reservation_bound_usd"]
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout=json.dumps(
                synthetic_observation(slot, bound, "Truncated", "max_tokens", artifact_parent=self.root)).encode())

        with self.assertRaisesRegex(controller.CampaignError, "max-token completion"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, self.admission, self.output, runner)
        self.assertEqual(len(calls), 1)
        record = json.loads((self.output / slot["identifier"] / "measurement.json").read_text(encoding="utf-8"))
        self.assertEqual(record["outcome_kind"], "Truncated")
        self.assertTrue((self.output / "stopped.json").is_file())

    def test_no_call_without_exact_research_manifest_hash(self):
        limits = self.manifest["campaign_limits"]
        wrong = self.root / "wrong-admission.json"
        wrong.write_text(json.dumps({
            "authority": "Research", "status": "Admitted", "admission_id": "fixture",
            "manifest_sha256": "0" * 64, "slot_count": limits["maximum_provider_calls"],
            "campaign_limit_usd": limits["maximum_campaign_retained_usd"], "global_unreserved_usd": "30",
        }), encoding="utf-8")
        calls = []

        def runner(*args, **kwargs):
            calls.append(args)
            return SimpleNamespace(returncode=0, stdout=b"{}")

        with self.assertRaisesRegex(controller.CampaignError, "different manifest hash"):
            controller._run_campaign_with_test_harness(MANIFEST_PATH, wrong, self.output, runner)
        self.assertEqual(calls, [])
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
