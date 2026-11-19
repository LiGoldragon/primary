"""Prepare the frozen December campaign from admitted historical trial packets.

Only the local Rust ``prepare`` operation is used here. This module has no
provider invocation path.
"""

from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid

import controller


PRIMARY_ROOT = Path(__file__).resolve().parents[3]
CAMPAIGN_ROOT = Path(__file__).resolve().parent
TRIAL_ROOT = PRIMARY_ROOT / "flows/250509/trial"
WORKER_ROOT = PRIMARY_ROOT / "flows/082e0f/claude-api-evidence/api-worker"
AUTHORITY_FILE = PRIMARY_ROOT / "flows/d343f8/december-campaign-proposal.md"
MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
MAXIMUM_PROVIDER_CALLS = 336
MAXIMUM_CAMPAIGN_RETAINED_USD = "20"
HISTORICAL_CASES = ["belief-04", *[f"belief-balanced-{index:02d}" for index in range(2, 31)],
                    *[f"queue-{index:02d}" for index in range(1, 31)]]
SCOPED_OPUS_CASES = {
    "belief-balanced-19", "belief-balanced-20", "belief-balanced-22", "belief-balanced-24",
    "belief-balanced-27", "belief-balanced-28", "belief-balanced-29", "belief-balanced-30",
}
MISSING_CASES = {
    "Admission": ["belief-balanced-02", "belief-balanced-03"],
    "Queue": ["queue-01", "queue-02"],
}
FORMAT_CASES = {
    "Admission": ["belief-balanced-04", "belief-balanced-05"],
    "Queue": ["queue-03", "queue-04"],
}


class GenerationError(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def write_exclusive(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    directory_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    path.chmod(0o444)


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GenerationError(f"expected object in {path}")
    return value


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def source_slot_maps() -> tuple[dict[str, dict], dict[str, dict]]:
    opus_plan = load_json(TRIAL_ROOT / "opus-plan.json")
    suite_plan = load_json(TRIAL_ROOT / "suite-plan.json")
    opus = {slot["case"]: slot for slot in opus_plan["slots"]}
    suite = {(slot["model"], slot["case"]): slot for slot in suite_plan["slots"]}
    return opus, suite


def source_call_path(slot: dict) -> Path:
    return Path(slot["call_file"]).resolve(strict=True)


def source_prompt_path(slot: dict) -> Path:
    return Path(slot["prompt_file"]).resolve(strict=True)


def source_baseline(model: str, case_id: str) -> Path:
    if model == "claude-opus-5-5":
        return TRIAL_ROOT / "results/opus-matrix" / f"{model}--{case_id}" / "measurement.json"
    return TRIAL_ROOT / "results/supported-matrix" / f"{model}--{case_id}" / "measurement.json"


def task_for_case(case_id: str) -> str:
    return "Admission" if case_id.startswith("belief") else "Queue"


def append_instruction(call: dict, text: str) -> None:
    call["instruction"] = call["instruction"].rstrip() + "\n\n" + text.strip()


def make_case_variants(opus_slots: dict[str, dict]) -> list[dict]:
    variants = []
    for case_id in HISTORICAL_CASES:
        if case_id in SCOPED_OPUS_CASES:
            continue
        variants.append({
            "category": "historical_variance",
            "case_id": case_id,
            "task_kind": task_for_case(case_id),
            "replicates": [1, 2],
            "base_call": load_json(source_call_path(opus_slots[case_id])),
            "source_slot": opus_slots[case_id],
            "provenance": {
                "source_case_id": case_id,
                "source_call": str(source_call_path(opus_slots[case_id])),
                "source_call_sha256": hash_file(source_call_path(opus_slots[case_id])),
                "source_prompt": str(source_prompt_path(opus_slots[case_id])),
                "source_prompt_sha256": hash_file(source_prompt_path(opus_slots[case_id])),
                "baseline_receipt_refs": {},
                "withheld_inputs": [],
                "output_format_perturbation": None,
                "expected_semantic_label": None,
            },
        })

    for task_kind, source_cases in MISSING_CASES.items():
        for source_case in source_cases:
            source_slot = opus_slots[source_case]
            base_call = load_json(source_call_path(source_slot))
            derived_id = "missing-" + source_case
            base_call["question"]["case"] = derived_id
            if task_kind == "Admission":
                base_call["question"]["snapshot"]["lines"] = []
                base_call["question"]["snapshot"]["modules"] = []
                withheld = ["question.snapshot.lines", "question.snapshot.modules"]
                instruction = (
                    "Controlled missing-evidence derivation: question.snapshot.lines and "
                    "question.snapshot.modules were withheld from the identified historical packet. "
                    "Their empty arrays mark withheld evidence; they do not establish that no lines "
                    "or modules exist. Use only supplied evidence and refuse when essential evidence "
                    "is missing. This tests task-level evidence sufficiency."
                )
            else:
                base_call["question"]["pending_work"] = []
                withheld = ["question.pending_work"]
                instruction = (
                    "Controlled missing-evidence derivation: question.pending_work was withheld from "
                    "the identified historical packet. Its empty array marks withheld evidence; it "
                    "does not establish that no pending work exists. Use only supplied evidence and "
                    "refuse when essential evidence is missing. This tests task-level evidence sufficiency."
                )
            append_instruction(base_call, instruction)
            variants.append({
                "category": "missing_evidence",
                "case_id": derived_id,
                "task_kind": task_kind,
                "replicates": [1],
                "base_call": base_call,
                "source_slot": source_slot,
                "provenance": {
                    "source_case_id": source_case,
                    "source_call": str(source_call_path(source_slot)),
                    "source_call_sha256": hash_file(source_call_path(source_slot)),
                    "source_prompt": str(source_prompt_path(source_slot)),
                    "source_prompt_sha256": hash_file(source_prompt_path(source_slot)),
                    "baseline_receipt_refs": {},
                    "withheld_inputs": withheld,
                    "withheld_encoding": "schema-required empty arrays plus an explicit instruction that emptiness marks withheld data",
                    "output_format_perturbation": None,
                    "expected_semantic_label": None,
                },
            })

    for task_kind, source_cases in FORMAT_CASES.items():
        for source_case in source_cases:
            source_slot = opus_slots[source_case]
            base_call = load_json(source_call_path(source_slot))
            derived_id = "format-probe-" + source_case
            base_call["question"]["case"] = derived_id
            wrong_shape = {"kind": "WrongFormatProbe", "reason": "declared incompatible shape"}
            perturbation = {
                "declared_output_shape": wrong_shape,
                "decoder_expected_to_reject": True,
                "decoder_changed": False,
            }
            append_instruction(base_call,
                "Controlled output-format perturbation: use the supplied packet as evidence, but "
                "return exactly the JSON object {\"kind\":\"WrongFormatProbe\",\"reason\":\"declared incompatible shape\"}. "
                "This shape is deliberately incompatible with the task's strict decoder. The decoder "
                "remains unchanged; record whatever response occurs.")
            variants.append({
                "category": "malformed_probe",
                "case_id": derived_id,
                "task_kind": task_kind,
                "replicates": [1],
                "base_call": base_call,
                "source_slot": source_slot,
                "provenance": {
                    "source_case_id": source_case,
                    "source_call": str(source_call_path(source_slot)),
                    "source_call_sha256": hash_file(source_call_path(source_slot)),
                    "source_prompt": str(source_prompt_path(source_slot)),
                    "source_prompt_sha256": hash_file(source_prompt_path(source_slot)),
                    "baseline_receipt_refs": {},
                    "withheld_inputs": [],
                    "output_format_perturbation": perturbation,
                    "expected_semantic_label": None,
                },
            })
    return variants


def verify_baseline_packets(variants: list[dict], suite_slots: dict[tuple[str, str], dict]) -> None:
    for variant in variants:
        for model in MODELS:
            case_id = variant["provenance"]["source_case_id"]
            if model == "claude-opus-5-5":
                model_slot = variant["source_slot"]
            else:
                model_slot = suite_slots.get((model, case_id))
                if model_slot is None:
                    raise GenerationError(f"historical source call missing for {model} {case_id}")
            source_call = load_json(source_call_path(model_slot))
            opus_call = load_json(source_call_path(variant["source_slot"]))
            if source_call["question"] != opus_call["question"] or source_call["instruction"] != opus_call["instruction"]:
                raise GenerationError(f"historical typed packet differs by model for {case_id}")
            baseline_prompt = source_prompt_path(model_slot).read_bytes()
            reference_prompt = source_prompt_path(variant["source_slot"]).read_bytes()
            if baseline_prompt != reference_prompt:
                raise GenerationError(f"models have different historical prompt bytes for {case_id}")
            receipt = source_baseline(model, case_id)
            if not receipt.is_file():
                raise GenerationError(f"historical baseline receipt missing: {receipt}")
            variant["provenance"]["baseline_receipt_refs"][model] = {
                "path": str(receipt.resolve()),
                "sha256": hash_file(receipt),
            }


def source_file_list(variants: list[dict], binary: Path, execution_closure: dict) -> list[dict]:
    paths = {
        AUTHORITY_FILE,
        TRIAL_ROOT / "opus-plan.json",
        TRIAL_ROOT / "suite-plan.json",
        TRIAL_ROOT / "processor.json",
        TRIAL_ROOT / "src/lib.rs",
        TRIAL_ROOT / "src/main.rs",
        TRIAL_ROOT / "tests/decoding.rs",
        PRIMARY_ROOT / "flows/250509/typed-call-report.md",
        WORKER_ROOT / "general-policy.json",
        WORKER_ROOT / "general_adapter.py",
        WORKER_ROOT / "model_policy.py",
        Path(__file__).resolve(),
        Path(controller.__file__).resolve(),
        Path(__file__).with_name("tests.py").resolve(),
        binary,
    }
    for variant in variants:
        paths.add(Path(variant["provenance"]["source_call"]))
        paths.add(Path(variant["provenance"]["source_prompt"]))
        for receipt in variant["provenance"]["baseline_receipt_refs"].values():
            paths.add(Path(receipt["path"]))
    for group in ("worker_python_sources", "static_inputs", "executables"):
        paths.update(Path(item["path"]) for item in execution_closure[group])
    return [{"path": str(path.resolve(strict=True)), "sha256": hash_file(path.resolve(strict=True))}
            for path in sorted(paths, key=lambda item: str(item))]


def build(output_root: Path = CAMPAIGN_ROOT, prepare_timeout: int = 30,
          refresh_existing_inputs: bool = False) -> dict:
    output_root = output_root.resolve()
    if output_root != CAMPAIGN_ROOT.resolve():
        output_root.mkdir(parents=True, exist_ok=True)
    inputs_root = output_root / "inputs"
    manifest_path = output_root / "proposal-manifest.json"
    if refresh_existing_inputs:
        if not inputs_root.is_dir() or inputs_root.is_symlink():
            raise GenerationError("manifest refresh requires the existing immutable input directory")
    elif inputs_root.exists() or manifest_path.exists():
        raise GenerationError("frozen campaign inputs already exist; generator will not overwrite them")

    opus_plan = load_json(TRIAL_ROOT / "opus-plan.json")
    suite_plan = load_json(TRIAL_ROOT / "suite-plan.json")
    opus_slots = {slot["case"]: slot for slot in opus_plan["slots"]}
    suite_slots = {(slot["model"], slot["case"]): slot for slot in suite_plan["slots"]}
    policy_path = WORKER_ROOT / "general-policy.json"
    policy = load_json(policy_path)
    binary = Path(opus_plan["binary"]).resolve(strict=True)
    processor_configuration = Path(opus_plan["processor_configuration"]).resolve(strict=True)
    variants = make_case_variants(opus_slots)
    expected_history = set(HISTORICAL_CASES) - SCOPED_OPUS_CASES
    actual_history = {v["case_id"] for v in variants if v["category"] == "historical_variance"}
    if actual_history != expected_history or len(actual_history) != 52:
        raise GenerationError("historical default-bound set does not contain the exact authorized 52 cases")
    if len(variants) != 60:
        raise GenerationError("expected 52 historical and eight derived packets")

    for variant in variants:
        if variant["category"] == "historical_variance":
            variant["base_call"] = load_json(source_call_path(variant["source_slot"]))
            variant["base_call"]["question"]["case"] = variant["case_id"]
    verify_baseline_packets(variants, suite_slots)

    profile = controller.model_bounds(policy)
    opus_bound = profile["claude-opus-5-5"]["input_admission"]
    for case_id in expected_history:
        prompt_path = source_prompt_path(opus_slots[case_id])
        total = prompt_path.stat().st_size + opus_bound["system_utf8_bytes"] + opus_bound["framing_allowance"]
        if total > opus_bound["conservative_input_limit"]:
            raise GenerationError(f"historical prompt is outside the default Opus input bound: {case_id}")

    namespace = uuid.uuid5(uuid.NAMESPACE_URL, "https://primary.goldragon.criome/campaign/december-20usd-336/0cb1dfea2")
    order = []
    for variant in variants:
        for replicate in variant["replicates"]:
            for model in MODELS:
                identifier = f"{variant['category']}__{variant['case_id']}__{model}__r{replicate}"
                order.append((variant, replicate, model, identifier))
    if len(order) != MAXIMUM_PROVIDER_CALLS:
        raise GenerationError(f"slot plan has {len(order)} entries instead of configured maximum {MAXIMUM_PROVIDER_CALLS}")

    derived_cases = {}
    for variant in variants:
        if variant["category"] == "historical_variance":
            continue
        case = {
            "case_id": variant["case_id"],
            "source_case_id": variant["provenance"]["source_case_id"],
            "task_kind": variant["task_kind"],
        }
        if variant["category"] == "missing_evidence":
            case["withheld_inputs"] = variant["provenance"]["withheld_inputs"]
            case["withheld_encoding"] = variant["provenance"]["withheld_encoding"]
        if variant["category"] == "malformed_probe":
            case["output_format_perturbation"] = variant["provenance"]["output_format_perturbation"]
        derived_cases.setdefault(variant["category"], []).append(case)
    slot_contract = {
        "models": MODELS,
        "task_kinds": ["Admission", "Queue"],
        "one_call_per_slot": True,
        "historical": {
            "category": "historical_variance",
            "cases_by_task": {
                task: sorted(case for case in expected_history if task_for_case(case) == task)
                for task in ("Admission", "Queue")
            },
            "replicates": [1, 2],
        },
        "derived": {
            category: {"cases": cases, "replicates": [1]}
            for category, cases in sorted(derived_cases.items())
        },
        "excluded_scoped_historical_cases": sorted(SCOPED_OPUS_CASES),
    }
    campaign_limits = {
        "maximum_provider_calls": MAXIMUM_PROVIDER_CALLS,
        "maximum_campaign_retained_usd": MAXIMUM_CAMPAIGN_RETAINED_USD,
    }

    scratch_temp = tempfile.TemporaryDirectory(prefix="december-campaign-generator-")
    try:
        scratch = Path(scratch_temp.name)
        rendered_by_variant: dict[str, bytes] = {}
        representative_call = {}
        representative_prompt = {}
        for variant in variants:
            scratch_call_path = scratch / (variant["category"] + "__" + variant["case_id"] + ".call.json")
            scratch_prompt_path = scratch / (variant["category"] + "__" + variant["case_id"] + ".prompt.txt")
            call = deepcopy(variant["base_call"])
            call["model"] = "claude-opus-5-5"
            call["prompt_file"] = str(scratch_prompt_path)
            scratch_call_path.write_bytes(json_bytes(call))
            subprocess.run([str(binary), "prepare", str(scratch_call_path), str(scratch_prompt_path)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=prepare_timeout, check=True)
            rendered = scratch_prompt_path.read_bytes()
            if variant["category"] == "historical_variance":
                original = source_prompt_path(variant["source_slot"]).read_bytes()
                if rendered != original:
                    raise GenerationError(f"Rust prepare changed historical prompt bytes for {variant['case_id']}")
            total = len(rendered) + opus_bound["system_utf8_bytes"] + opus_bound["framing_allowance"]
            if total > opus_bound["conservative_input_limit"]:
                raise GenerationError(f"prepared Opus prompt exceeds the default bound: {variant['case_id']}")
            rendered_by_variant[variant["category"] + "/" + variant["case_id"]] = rendered
            representative_call[variant["category"] + "/" + variant["case_id"]] = scratch_call_path
            representative_prompt[variant["category"] + "/" + variant["case_id"]] = scratch_prompt_path

        profile_counts = Counter()
        categories = Counter()
        total_output_bound = Counter()
        total_reservation_bound = {model: Decimal(0) for model in MODELS}
        slot_records = []
        generated: dict[Path, bytes] = {}
        for variant, replicate, model, identifier in order:
            variant_key = variant["category"] + "/" + variant["case_id"]
            prompt_relative = Path("inputs") / f"{identifier}.prompt.txt"
            call_relative = Path("inputs") / f"{identifier}.call.json"
            absolute_prompt = (output_root / prompt_relative).resolve()
            call = deepcopy(variant["base_call"])
            call["model"] = model
            call["prompt_file"] = str(absolute_prompt)
            call_bytes = json_bytes(call)
            prompt_bytes = rendered_by_variant[variant_key]
            bound = Decimal(profile[model]["reservation_bound_usd"])
            prompt_count = len(prompt_bytes)
            conservative = None
            admission = profile[model].get("input_admission")
            if admission:
                conservative = prompt_count + admission["system_utf8_bytes"] + admission["framing_allowance"]
                if conservative > admission["conservative_input_limit"]:
                    raise GenerationError(f"Opus prompt bound fails for {identifier}")
            provenance = deepcopy(variant["provenance"])
            slot = {
                "identifier": identifier,
                "stage_uuid": str(uuid.uuid5(namespace, identifier)),
                "category": variant["category"],
                "case_id": variant["case_id"],
                "task_kind": variant["task_kind"],
                "model": model,
                "replicate": replicate,
                "one_call_only": slot_contract["one_call_per_slot"],
                "call_file": str(call_relative),
                "call_sha256": sha256_bytes(call_bytes),
                "prompt_file": str(prompt_relative),
                "prompt_sha256": sha256_bytes(prompt_bytes),
                "prompt_utf8_bytes": prompt_count,
                "maximum_output_tokens": profile[model]["maximum_output_tokens"],
                "reservation_bound_usd": str(bound),
                "conservative_input_bytes": conservative,
                "source_case_id": provenance["source_case_id"],
                "source_call_path": provenance["source_call"],
                "source_call_sha256": provenance["source_call_sha256"],
                "source_prompt_path": provenance["source_prompt"],
                "source_prompt_sha256": provenance["source_prompt_sha256"],
                "baseline_receipt_refs": provenance["baseline_receipt_refs"],
                "withheld_inputs": provenance["withheld_inputs"],
                "withheld_encoding": provenance.get("withheld_encoding"),
                "output_format_perturbation": provenance["output_format_perturbation"],
                "expected_semantic_label": provenance["expected_semantic_label"],
                "instruction": call["instruction"],
            }
            if variant["category"] != "historical_variance":
                slot["derived_packet"] = True
            generated[output_root / prompt_relative] = prompt_bytes
            generated[output_root / call_relative] = call_bytes
            slot_records.append(slot)
            profile_counts[model] += 1
            categories[variant["category"]] += 1
            total_output_bound[model] += profile[model]["maximum_output_tokens"]
            total_reservation_bound[model] += bound

        execution_closure = controller.derive_execution_closure(policy_path, processor_configuration)
        frozen_files = source_file_list(variants, binary, execution_closure)
        result_directory = output_root / "results" / str(namespace)
        runtime_guard_paths = {
            Path(__file__).resolve(), Path(controller.__file__).resolve(),
            Path(__file__).with_name("tests.py").resolve(), binary, processor_configuration,
        }
        for group in ("worker_python_sources", "static_inputs", "executables"):
            runtime_guard_paths.update(Path(item["path"]) for item in execution_closure[group])
        manifest = {
            "schema_version": 1,
            "campaign": "December typed-call campaign",
            "authority": {
                "proposal_path": str(AUTHORITY_FILE),
                "proposal_sha256": hash_file(AUTHORITY_FILE),
                "admission_owner": "Research",
                "calls_authorized_before_admission": False,
            },
            "campaign_limits": campaign_limits,
            "slot_contract": slot_contract,
            "http_cap_per_slot": 1,
            "accounting_owner": "pinned worker and Research ledger",
            "controller_accounting": "worker observations only; no second ledger",
            "stage_uuid_namespace": str(namespace),
            "binary": str(binary),
            "processor_configuration": str(processor_configuration),
            "worker_policy_file": str(policy_path.resolve()),
            "execution_closure": execution_closure,
            "runtime_guard_files": [str(path.resolve(strict=True))
                                    for path in sorted(runtime_guard_paths, key=str)],
            "processor_timeout_seconds": policy["shared"]["wrapper_timeout_seconds"] + 5,
            "result_directory": str(result_directory.resolve()),
            "model_bounds": profile,
            "model_slot_counts": dict(sorted(profile_counts.items())),
            "total_output_token_bounds": {
                **{model: total_output_bound[model] for model in MODELS},
                "all_models": sum(total_output_bound.values()),
            },
            "full_reservation_bounds_usd": {
                **{model: str(total_reservation_bound[model]) for model in MODELS},
                "all_models": str(sum(total_reservation_bound.values(), Decimal(0))),
            },
            "slot_category_counts": dict(sorted(categories.items())),
            "failure_injection": {
                "provider_invoked_for_fixtures": False,
                "fixture_scope": "local synthetic subprocess and receipt evidence only",
                "cases": ["timeout", "native_refusal", "malformed_answer", "max_tokens", "nonzero_exit",
                          "missing_receipt", "invalid_receipt", "prompt_drift", "policy_drift",
                          "extra_slot", "concurrent_launch", "restart_after_start", "reservation_guard"],
            },
            "frozen_files": frozen_files,
            "slots": slot_records,
        }
        manifest["canonical_sha256"] = controller.canonical_sha256(manifest)

        if refresh_existing_inputs:
            expected_files = {path.resolve() for path in generated}
            actual_files = {path.resolve() for path in inputs_root.rglob("*") if path.is_file()}
            if actual_files != expected_files:
                raise GenerationError("existing immutable input set differs from regenerated slots")
            for path, data in generated.items():
                if path.read_bytes() != data:
                    raise GenerationError(f"existing immutable input bytes differ: {path}")
        else:
            inputs_root.mkdir(parents=True, exist_ok=False)
            for path, data in generated.items():
                write_exclusive(path, data)
        manifest_bytes = json_bytes(manifest)
        if refresh_existing_inputs and manifest_path.exists():
            manifest_path.unlink()
        write_exclusive(manifest_path, manifest_bytes)
        controller.verify_manifest(manifest_path)
        return manifest
    finally:
        scratch_temp.cleanup()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-timeout", type=int, default=30)
    parser.add_argument("--refresh-existing-inputs", action="store_true",
                        help="rebuild the manifest only after exact input bytes are verified")
    args = parser.parse_args()
    if args.prepare_timeout <= 0:
        raise SystemExit("prepare timeout must be positive")
    try:
        manifest = build(prepare_timeout=args.prepare_timeout,
                         refresh_existing_inputs=args.refresh_existing_inputs)
    except (GenerationError, controller.CampaignError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f"generation failed: {error}", file=__import__("sys").stderr)
        return 2
    print(json.dumps({
        "manifest": str(CAMPAIGN_ROOT / "proposal-manifest.json"),
        "slots": len(manifest["slots"]),
        "stage_uuid_namespace": manifest["stage_uuid_namespace"],
        "provider_calls": 0,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
