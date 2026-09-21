import unittest
import importlib.util
from pathlib import Path

module_path = Path(__file__).with_name("field-refresh-control.py")
spec = importlib.util.spec_from_file_location("field_refresh_control", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
validate = module.validate
probe_envelope = module.probe_envelope
# The control module already imported the installed Datom parser; use that
# exact parser to inspect the generated machine envelope.
relay = module.relay


class FieldRefreshControlTest(unittest.TestCase):
    def test_exact_probe_and_ack(self):
        marker = "6db4fe-03e825-probe1"
        validate(f"Probe.{{ «{marker}» }}", "Probe", marker)
        validate(f"Ack.{{ «{marker}» }}", "Ack", marker)

    def test_rejects_wrong_variant_arity_kind_and_marker(self):
        marker = "6db4fe-03e825-probe1"
        for value in [
            f"Ack.{{ «{marker}» }}",
            f"Probe.{{ «{marker}» «extra» }}",
            f"Probe.[ «{marker}» ]",
            "Probe.{ wrong-marker }",
            "Probe.{ «wrong-marker» }",
            "ordinary prose",
        ]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate(value, "Probe", marker)

    def test_probe_envelope_carries_declared_type_and_exact_reply_instruction(self):
        marker = "6db4fe-753e69-probe1"
        envelope = probe_envelope("flow-6db4fe", "field-sol", "flow-753e69", marker)
        parsed = relay(envelope)
        self.assertEqual(parsed["mode"], "typed")
        self.assertEqual(parsed["recipients"], ["flow-753e69"])
        validate(parsed["quote"], "Probe", marker)
        self.assertIn("refresh-control.ethos", parsed["context"])
        self.assertIn(f"Ack.{{ «{marker}» }}", parsed["context"])

    def test_offer_and_accept_are_exactly_typed(self):
        marker = "6db4fe-03e825-handoff"
        validate(f"Offer.{{ «{marker}» «flows/6db4fe/reports/refresh-handoff-current.md» }}", "Offer", marker)
        validate(f"Accept.{{ «{marker}» }}", "Accept", marker)
        for value in [
            f"Offer.{{ «{marker}» }}",
            f"Offer.{{ «{marker}» wrong }}",
            f"Accept.{{ «{marker}» «extra» }}",
        ]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate(value, "Offer" if value.startswith("Offer") else "Accept", marker)


if __name__ == "__main__":
    unittest.main()
