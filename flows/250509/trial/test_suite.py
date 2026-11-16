"""Synthetic driver checks; subprocess/network calls are not executed."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import suite


class SerialDriverTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="typed-call-driver-")
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        prompt = self.root / "prompt.txt"
        prompt.write_text("fixture")
        call = self.root / "call.json"
        call.write_text(json.dumps({"model": "fixture", "prompt_file": str(prompt)}))
        self.slot = {"identifier": "one", "model": "fixture", "case": "one", "call_file": str(call), "prompt_file": str(prompt), "prompt_sha256": suite.digest(prompt)}
        self.config = {"frozen_files": [], "slots": [self.slot], "reservation_bounds": {"fixture": "1"}, "maximum_slots_per_model": 60, "http_cap_per_slot": 1, "output_directory": str(self.root / "results"), "initial_retained_usd": "0.1", "maximum_retained_usd": "10"}

    def test_dry_verification_calls_no_process(self):
        with patch("subprocess.run") as process:
            self.assertEqual(suite.verify(self.config), {"fixture": 1})
            process.assert_not_called()

    def test_duplicate_slot_refused(self):
        self.config["slots"].append(copy.deepcopy(self.slot))
        with self.assertRaisesRegex(RuntimeError, "duplicate slot"):
            suite.verify(self.config)

    def test_sixty_one_slots_refused(self):
        self.config["slots"] = [dict(self.slot, identifier=str(i)) for i in range(61)]
        with self.assertRaisesRegex(RuntimeError, "slot cap"):
            suite.verify(self.config)

    def test_unknown_model_refused(self):
        self.slot["model"] = "unsupported"
        with self.assertRaisesRegex(RuntimeError, "unsupported model"):
            suite.verify(self.config)

    def test_changed_prompt_refused(self):
        Path(self.slot["prompt_file"]).write_text("changed")
        with self.assertRaisesRegex(RuntimeError, "prompt changed"):
            suite.verify(self.config)

    def test_changed_binary_or_producer_refused(self):
        self.config["frozen_files"] = [{"path": self.slot["prompt_file"], "sha256": "wrong"}]
        with self.assertRaisesRegex(RuntimeError, "frozen input"):
            suite.verify(self.config)

    def test_full_reservation_guard_before_call(self):
        self.config["initial_retained_usd"] = "9.5"
        with patch("suite.observe") as observe:
            with self.assertRaisesRegex(RuntimeError, "full reservation"):
                suite.run(self.config)
            observe.assert_not_called()

    def test_uncertainty_stops_chain_without_retry(self):
        self.config["slots"].append(dict(self.slot, identifier="two"))
        with patch("suite.observe", side_effect=RuntimeError("uncertain")) as observe:
            with self.assertRaisesRegex(RuntimeError, "uncertain"):
                suite.run(self.config)
            self.assertEqual(observe.call_count, 1)
        self.assertTrue((self.root / "results/one/started.json").exists())
        self.assertFalse((self.root / "results/two").exists())

    def test_existing_slot_never_repeated(self):
        (self.root / "results/one").mkdir(parents=True)
        with patch("suite.observe") as observe:
            with self.assertRaises(FileExistsError):
                suite.run(self.config)
            observe.assert_not_called()

    def test_unsuccessful_receipt_refused(self):
        with self.assertRaisesRegex(RuntimeError, "processor unsuccessful"):
            suite.valid_receipt({"processor_exit": 2, "receipt": None})

    def test_input_bound_refuses_locally_without_subprocess(self):
        self.config["input_admission"] = {"fixture": {"system_utf8_bytes": 2, "framing_allowance": 1, "maximum_input_tokens": 3}}
        with patch("suite.observe") as observe:
            suite.run(self.config)
            observe.assert_not_called()
        result = json.loads((self.root / "results/one/measurement.json").read_text())
        self.assertEqual(result["outcome"]["kind"], "RefusedBeforeCall")
        self.assertFalse(result["paid_call"])
        self.assertIsNone(result["job"])

    def test_conservative_count_is_bytes_not_observed_tokens(self):
        self.config["input_admission"] = {"fixture": {"system_utf8_bytes": 2, "framing_allowance": 1024, "maximum_input_tokens": 20000}}
        self.assertEqual(suite.admission_counts(self.config, self.slot)["conservative_local_total"], 1033)


if __name__ == "__main__":
    unittest.main()
