import unittest
import importlib.util
from pathlib import Path

module_path = Path(__file__).with_name("field-refresh-control.py")
spec = importlib.util.spec_from_file_location("field_refresh_control", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
validate = module.validate


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


if __name__ == "__main__":
    unittest.main()
