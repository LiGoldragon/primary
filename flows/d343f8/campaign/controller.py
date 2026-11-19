"""One-shot controller for the admitted December typed-call campaign.

This controller records worker observations. It never owns provider accounting;
the pinned worker and Research ledger remain authoritative for each reservation.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from decimal import Decimal, InvalidOperation
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid


ALLOWED_OUTCOMES = {"Answered", "Malformed", "ModelRefused", "Truncated"}


class CampaignError(RuntimeError):
    """A local guard failed; no subsequent slot may be attempted."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CampaignError(message)


def read_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CampaignError(f"cannot read JSON {path}: {error}") from error
    require(isinstance(value, dict), f"expected a JSON object: {path}")
    return value


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError as error:
        raise CampaignError(f"cannot hash {path}: {error}") from error


def decimal(value: object, field: str) -> Decimal:
    require(isinstance(value, (str, int, Decimal)), f"{field} must be a decimal string")
    try:
        result = Decimal(str(value))
    except InvalidOperation as error:
        raise CampaignError(f"{field} is not a decimal") from error
    require(result.is_finite() and result >= 0, f"{field} must be finite and nonnegative")
    return result


def resolve_campaign_path(campaign_root: Path, value: str) -> Path:
    path = Path(value)
    require(not path.is_absolute(), f"campaign input path must be relative: {value}")
    resolved = (campaign_root / path).resolve(strict=True)
    root = campaign_root.resolve(strict=True)
    require(resolved == root or root in resolved.parents, f"campaign input escapes campaign root: {value}")
    require(resolved.is_file(), f"campaign input is not a regular file: {value}")
    return resolved


def reservation_bound(model_policy: dict) -> Decimal:
    """Mirror the worker's reviewed maximum-input plus maximum-output formula."""
    return (
        Decimal(model_policy["maximum_input_tokens"])
        * Decimal(model_policy["reserve_input_rate_usd_per_million"])
        + Decimal(model_policy["maximum_output_tokens"])
        * Decimal(model_policy["output_rate_usd_per_million"])
    ) / Decimal(1_000_000)


def effective_model_bounds(policy: dict) -> dict:
    shared = policy["shared"]
    output: dict[str, dict] = {}
    for model, values in policy["models"].items():
        item = {
            "response_codec": values["codec"],
            "maximum_input_tokens": values["maximum_input_tokens"],
            "maximum_output_tokens": values["maximum_output_tokens"],
            "reserve_input_rate_usd_per_million": values["reserve_input_rate_usd_per_million"],
            "output_rate_usd_per_million": values["output_rate_usd_per_million"],
            "maximum_prompt_bytes": shared["maximum_prompt_bytes"],
            "reservation_bound_usd": str(reservation_bound(values)),
        }
        if values.get("input_admission"):
            item["input_admission"] = {
                "codec": values["input_admission"]["codec"],
                "system_utf8_bytes": len(shared["system_prompt"].encode("utf-8")),
                "framing_allowance": values["input_admission"]["framing_allowance"],
                "conservative_input_limit": values["maximum_input_tokens"],
            }
        output[model] = item
    return output


def require_file_digest(path: Path, expected: str, context: str) -> None:
    require(sha256_file(path) == expected, f"{context} drift: {path}")


def model_bounds(policy: dict) -> dict:
    return effective_model_bounds(policy)


def response_text(content: object, response_codec: str) -> str:
    """Match the pinned worker's text extraction without altering the answer."""
    require(isinstance(content, list) and content, "end_turn outcome lacks native answer content")
    adaptive = response_codec == "AdaptiveMedium"
    text: list[str] = []
    for block in content:
        require(isinstance(block, dict), "native response content block is malformed")
        block_type = block.get("type")
        if block_type == "text" and {"type", "text"} <= set(block) <= {"type", "text", "citations"} and \
                isinstance(block.get("text"), str) and \
                ("citations" not in block or block["citations"] is None or block["citations"] == []):
            text.append(block["text"])
        elif adaptive and block_type == "thinking" and set(block) == {"type", "thinking", "signature"} and \
                block.get("thinking") == "" and isinstance(block.get("signature"), str) and block["signature"]:
            continue
        elif adaptive and block_type == "redacted_thinking" and set(block) == {"type", "data"} and \
                isinstance(block.get("data"), str) and block["data"]:
            continue
        else:
            raise CampaignError("native response content violates the frozen worker codec")
    return "".join(text)


def expected_slot_contract(contract: dict) -> Counter:
    """Expand the frozen manifest's case/model/replicate data into exact slots."""
    require(isinstance(contract, dict), "slot contract is missing")
    models = contract.get("models")
    tasks = contract.get("task_kinds")
    require(isinstance(models, list) and models and all(isinstance(model, str) and model for model in models) and
            len(models) == len(set(models)),
            "slot contract models must be a nonempty unique list")
    require(isinstance(tasks, list) and tasks and all(isinstance(task, str) and task for task in tasks) and
            len(tasks) == len(set(tasks)),
            "slot contract task kinds must be a nonempty unique list")
    historical = contract.get("historical")
    derived = contract.get("derived")
    require(isinstance(historical, dict) and isinstance(derived, dict), "slot contract case groups are missing")
    historical_category = historical.get("category")
    historical_by_task = historical.get("cases_by_task")
    historical_replicates = historical.get("replicates")
    require(isinstance(historical_category, str) and isinstance(historical_by_task, dict),
            "historical contract is malformed")
    require(set(historical_by_task) == set(tasks), "historical task set differs from task contract")
    require(isinstance(historical_replicates, list) and historical_replicates and
            all(type(rep) is int and rep > 0 for rep in historical_replicates) and
            len(set(historical_replicates)) == len(historical_replicates), "historical replicates are malformed")

    expected = Counter()
    for task, cases in historical_by_task.items():
        require(isinstance(cases, list) and cases and all(isinstance(case, str) and case for case in cases) and
                len(cases) == len(set(cases)),
                f"historical {task} cases must be a nonempty unique list")
        for case in cases:
            for model in models:
                for replicate in historical_replicates:
                    expected[(historical_category, case, task, model, replicate)] += 1

    require(isinstance(derived, dict) and derived, "derived case contract must be nonempty")
    require(historical_category not in derived, "historical and derived categories must be distinct")
    for category, group in derived.items():
        require(isinstance(category, str) and isinstance(group, dict), "derived category is malformed")
        cases = group.get("cases")
        replicates = group.get("replicates")
        require(isinstance(cases, list) and cases, f"derived cases missing for {category}")
        require(isinstance(replicates, list) and replicates and
                all(type(rep) is int and rep > 0 for rep in replicates) and
                len(set(replicates)) == len(replicates), f"derived replicates malformed for {category}")
        case_ids = []
        for case in cases:
            require(isinstance(case, dict), f"derived case malformed for {category}")
            case_id = case.get("case_id")
            task = case.get("task_kind")
            source_case_id = case.get("source_case_id")
            require(isinstance(case_id, str) and case_id and isinstance(source_case_id, str) and source_case_id,
                    f"derived case identity malformed for {category}")
            require(task in tasks, f"derived task kind unknown for {category}")
            case_ids.append(case_id)
            if category == "missing_evidence":
                withheld = case.get("withheld_inputs")
                require(isinstance(withheld, list) and withheld and
                        all(isinstance(item, str) and item for item in withheld),
                        f"missing-evidence case lacks explicit withheld inputs: {case_id}")
            if category == "malformed_probe":
                perturbation = case.get("output_format_perturbation")
                require(isinstance(perturbation, dict) and
                        perturbation.get("decoder_expected_to_reject") is True and
                        perturbation.get("decoder_changed") is False,
                        f"malformed probe lacks declared unchanged-decoder perturbation: {case_id}")
            for model in models:
                for replicate in replicates:
                    expected[(category, case_id, task, model, replicate)] += 1
        require(len(case_ids) == len(set(case_ids)), f"duplicate derived case for {category}")

    excluded = contract.get("excluded_scoped_historical_cases")
    require(isinstance(excluded, list) and all(isinstance(case, str) and case for case in excluded) and
            len(excluded) == len(set(excluded)),
            "excluded scoped historical cases must be a unique list")
    all_historical = {case for cases in historical_by_task.values() for case in cases}
    require(all_historical.isdisjoint(excluded), "excluded scoped cases appear in the historical contract")
    require(contract.get("one_call_per_slot") is True, "slot contract must require one call per slot")
    return expected


def verify_manifest(manifest_path: Path, manifest: dict | None = None) -> dict:
    """Verify the exact frozen inputs and the complete bounded slot contract."""
    manifest_path = manifest_path.resolve(strict=True)
    root = manifest_path.parent.resolve(strict=True)
    value = manifest if manifest is not None else read_json(manifest_path)

    seal = value.get("canonical_sha256")
    unsealed = dict(value)
    unsealed.pop("canonical_sha256", None)
    require(isinstance(seal, str) and seal == canonical_sha256(unsealed), "manifest canonical hash mismatch")
    limits = value.get("campaign_limits")
    require(isinstance(limits, dict), "campaign limits are missing")
    maximum_calls = limits.get("maximum_provider_calls")
    require(type(maximum_calls) is int and maximum_calls > 0, "maximum provider calls must be a positive integer")
    decimal(limits.get("maximum_campaign_retained_usd"), "maximum_campaign_retained_usd")
    contract = value.get("slot_contract")
    expected_slots = expected_slot_contract(contract)
    models_configured = set(contract["models"])
    tasks_configured = set(contract["task_kinds"])
    categories_configured = {key[0] for key in expected_slots}
    slots = value.get("slots")
    require(isinstance(slots, list), "manifest slots must be a list")
    require(len(slots) == maximum_calls, "manifest slot count differs from its frozen maximum")

    identifiers = [slot.get("identifier") for slot in slots]
    require(all(isinstance(identifier, str) and identifier for identifier in identifiers), "slot identifier missing")
    require(len(set(identifiers)) == len(identifiers), "duplicate slot identifier")
    models = {slot.get("model") for slot in slots}
    require(models == models_configured, "slot model set differs from the frozen contract")
    require(value.get("model_bounds", {}).keys() == models_configured, "model bounds do not name the configured models")
    policy_path_value = value.get("worker_policy_file")
    require(isinstance(policy_path_value, str), "worker policy path missing")
    policy_path = Path(policy_path_value).resolve(strict=True)
    policy = read_json(policy_path)
    require(set(policy.get("models", {})) == models_configured, "worker policy model set changed")
    require(effective_model_bounds(policy) == value["model_bounds"],
            "effective model reservation or output bounds changed")
    require(value.get("processor_timeout_seconds") == policy["shared"]["wrapper_timeout_seconds"] + 5,
            "processor timeout no longer follows the frozen worker wrapper bound")

    namespace = value.get("stage_uuid_namespace")
    try:
        namespace_uuid = uuid.UUID(namespace)
    except (TypeError, ValueError, AttributeError) as error:
        raise CampaignError("stage UUID namespace is invalid") from error
    require(str(namespace_uuid) == namespace.lower(), "stage UUID namespace is not canonical")

    tasks_by_category: dict[str, Counter] = {key: Counter() for key in categories_configured}
    historical_category = contract["historical"]["category"]
    historical_cases: dict[str, set[str]] = {task: set() for task in tasks_configured}
    actual_slots = Counter()
    per_model_counts = Counter()
    per_model_outputs = Counter()
    per_model_reservations: dict[str, Decimal] = {model: Decimal(0) for model in models_configured}
    category_counts = Counter()
    repeated_historical_prompts: dict[tuple[str, str], str] = {}
    derived_contract = {
        (category, case["case_id"]): case
        for category, group in contract["derived"].items()
        for case in group["cases"]
    }
    for slot in slots:
        require(slot.get("model") in models_configured, "unsupported model in slot")
        require(slot.get("task_kind") in tasks_configured, "unknown task kind in slot")
        require(slot.get("category") in categories_configured, "unknown slot category")
        require(type(slot.get("replicate")) is int and slot["replicate"] > 0, "invalid replicate")
        require(slot.get("one_call_only") is contract["one_call_per_slot"], "slot call cap differs from its contract")
        require(slot.get("stage_uuid") == str(uuid.uuid5(namespace_uuid, slot["identifier"])), "slot UUID does not match frozen namespace")
        actual_slots[(slot["category"], slot.get("case_id"), slot["task_kind"], slot["model"], slot["replicate"])] += 1
        tasks_by_category[slot["category"]][slot["task_kind"]] += 1
        category_counts[slot["category"]] += 1
        per_model_counts[slot["model"]] += 1

        call_path = resolve_campaign_path(root, slot["call_file"])
        prompt_path = resolve_campaign_path(root, slot["prompt_file"])
        require(sha256_file(call_path) == slot.get("call_sha256"), f"call drift for {slot['identifier']}")
        prompt_bytes = prompt_path.read_bytes()
        require(sha256_bytes(prompt_bytes) == slot.get("prompt_sha256"), f"prompt drift for {slot['identifier']}")
        call = read_json(call_path)
        require(call.get("model") == slot["model"], f"call model mismatch for {slot['identifier']}")
        require(Path(call.get("prompt_file", "")).resolve() == prompt_path, f"call prompt path mismatch for {slot['identifier']}")
        require(call.get("question", {}).get("kind") == slot["task_kind"], f"call task mismatch for {slot['identifier']}")
        require(call.get("question", {}).get("case") == slot["case_id"], f"call case mismatch for {slot['identifier']}")
        require(call.get("instruction") == slot.get("instruction"), f"instruction drift for {slot['identifier']}")

        bounds = value["model_bounds"][slot["model"]]
        require(len(prompt_bytes) <= bounds["maximum_prompt_bytes"], f"prompt exceeds worker byte bound: {slot['identifier']}")
        reservation = decimal(bounds["reservation_bound_usd"], "reservation_bound_usd")
        per_model_reservations[slot["model"]] += reservation
        per_model_outputs[slot["model"]] += bounds["maximum_output_tokens"]
        require(decimal(slot.get("reservation_bound_usd"), "slot reservation bound") == reservation,
                f"slot reservation mismatch for {slot['identifier']}")
        require(slot.get("maximum_output_tokens") == bounds["maximum_output_tokens"],
                f"slot output bound mismatch for {slot['identifier']}")
        admission = bounds.get("input_admission")
        if admission:
            total = len(prompt_bytes) + admission["system_utf8_bytes"] + admission["framing_allowance"]
            require(total <= admission["conservative_input_limit"],
                    f"default Opus input bound exceeded: {slot['identifier']}")
            require(slot.get("conservative_input_bytes") == total,
                    f"Opus input byte count changed: {slot['identifier']}")
        if slot["category"] == historical_category:
            require(slot.get("source_case_id") == slot.get("case_id"),
                    f"historical provenance case changed for {slot['identifier']}")
            prior_prompt = repeated_historical_prompts.setdefault((slot["case_id"], slot["model"]),
                                                                  slot["prompt_sha256"])
            require(prior_prompt == slot["prompt_sha256"],
                    f"historical variance prompt differs across replicates for {slot['identifier']}")
            require(set(slot.get("baseline_receipt_refs", {})) == models_configured,
                    f"historical baseline receipts incomplete for {slot['identifier']}")
            historical_cases[slot["task_kind"]].add(slot["case_id"])
        else:
            case_contract = derived_contract.get((slot["category"], slot["case_id"]))
            require(case_contract is not None, f"derived case is absent from contract: {slot['identifier']}")
            require(slot.get("source_case_id") == case_contract["source_case_id"],
                    f"derived provenance changed for {slot['identifier']}")
            require(slot.get("expected_semantic_label") is None,
                    f"derived case has an asserted semantic label: {slot['identifier']}")
            if slot["category"] == "missing_evidence":
                require(slot.get("withheld_inputs") == case_contract["withheld_inputs"],
                        f"withheld inputs changed for {slot['identifier']}")
            if slot["category"] == "malformed_probe":
                require(slot.get("output_format_perturbation") == case_contract["output_format_perturbation"],
                        f"output-format perturbation changed for {slot['identifier']}")

    require(actual_slots == expected_slots, "slot list differs from the exact frozen case/model/replicate contract")
    require(sum(per_model_counts.values()) == maximum_calls, "model slot totals differ from maximum call count")
    require(set(per_model_counts) == models_configured, "configured model has no provider slot")
    require(all(historical_cases[task] == set(contract["historical"]["cases_by_task"][task])
                for task in tasks_configured), "historical slot coverage differs from the frozen contract")
    require(category_counts == Counter(value.get("slot_category_counts", {})),
            "manifest category totals do not match its slots")
    require(dict(per_model_counts) == value.get("model_slot_counts"),
            "manifest model slot totals do not match its slots")
    output_totals = dict(per_model_outputs)
    output_totals["all_models"] = sum(per_model_outputs.values())
    require(output_totals == value.get("total_output_token_bounds"),
            "manifest total output-token bounds do not match its slots")
    reservation_totals = {model: str(amount) for model, amount in per_model_reservations.items()}
    reservation_totals["all_models"] = str(sum(per_model_reservations.values(), Decimal(0)))
    recorded_reservations = value.get("full_reservation_bounds_usd", {})
    require({model: str(decimal(amount, "full reservation total")) for model, amount in recorded_reservations.items()} ==
            reservation_totals, "manifest full-reservation totals do not match its slots")

    frozen_paths: dict[str, str] = {}
    for source in value.get("frozen_files", []):
        require(isinstance(source, dict) and isinstance(source.get("path"), str), "frozen file entry malformed")
        path_text = source["path"]
        path = resolve_campaign_path(root, path_text) if not Path(path_text).is_absolute() else Path(path_text).resolve(strict=True)
        require(path.is_file() and not path.is_symlink(), f"frozen file is absent or not regular: {path_text}")
        require_file_digest(path, source.get("sha256"), "frozen source")
        frozen_paths[str(path.resolve())] = source["sha256"]

    for slot in slots:
        for path_field, hash_field in (("source_call_path", "source_call_sha256"),
                                       ("source_prompt_path", "source_prompt_sha256")):
            source_path = str(Path(slot[path_field]).resolve(strict=True))
            require(frozen_paths.get(source_path) == slot[hash_field],
                    f"provenance source is not covered by the frozen source list: {source_path}")
        for baseline in slot.get("baseline_receipt_refs", {}).values():
            baseline_path = str(Path(baseline["path"]).resolve(strict=True))
            require(frozen_paths.get(baseline_path) == baseline["sha256"],
                    f"baseline receipt is not covered by the frozen source list: {baseline_path}")

    require(value.get("http_cap_per_slot") == 1, "per-slot worker cap must remain one")
    require(value.get("accounting_owner") == "pinned worker and Research ledger", "controller must not own accounting")
    require(frozen_paths.get(str(policy_path.resolve())) == sha256_file(policy_path), "worker policy is not frozen")
    require(value.get("result_directory") == str((root / "results" / namespace).resolve()), "result directory differs from frozen namespace")
    return value


def verify_runtime_slot(manifest_path: Path, manifest: dict, slot: dict, manifest_file_sha256: str) -> Path:
    """Recheck exact inputs and critical source files immediately before a call."""
    require_file_digest(manifest_path, manifest_file_sha256, "manifest")
    input_path = resolve_campaign_path(manifest_path.parent, slot["call_file"])
    prompt_path = resolve_campaign_path(manifest_path.parent, slot["prompt_file"])
    require_file_digest(input_path, slot["call_sha256"], "call input")
    require_file_digest(prompt_path, slot["prompt_sha256"], "prompt input")
    frozen = {str(Path(item["path"]).resolve(strict=True)): item["sha256"] for item in manifest["frozen_files"]}
    for path_value in manifest["runtime_guard_files"]:
        path = Path(path_value).resolve(strict=True)
        require(frozen.get(str(path)) is not None, f"runtime guard source is not frozen: {path}")
        require_file_digest(path, frozen[str(path)], "runtime source")
    return input_path


def durable_json(path: Path, value: dict, exclusive: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        directory_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        raise


@contextmanager
def exclusive_launch_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as stream:
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise CampaignError("another campaign launcher holds the exclusive lock") from error
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def validate_admission(admission_path: Path, manifest_path: Path, manifest: dict) -> dict:
    admission = read_json(admission_path.resolve(strict=True))
    require(admission.get("authority") == "Research", "a Research admission record is required")
    require(admission.get("status") == "Admitted", "Research has not admitted this campaign")
    manifest_file_sha = sha256_file(manifest_path)
    require(admission.get("manifest_sha256") == manifest_file_sha, "Research admission names a different manifest hash")
    limits = manifest["campaign_limits"]
    require(admission.get("slot_count") == limits["maximum_provider_calls"],
            "Research admission must name the frozen maximum slot count")
    require(decimal(admission.get("campaign_limit_usd"), "campaign_limit_usd") ==
            decimal(limits["maximum_campaign_retained_usd"], "maximum_campaign_retained_usd"),
            "Research admission campaign envelope differs from the frozen manifest")
    require(admission.get("global_unreserved_usd") is not None, "Research admission lacks a current global reservation snapshot")
    decimal(admission["global_unreserved_usd"], "global_unreserved_usd")
    require(admission.get("admission_id"), "Research admission identifier is required")
    return admission


def authoritative_receipt(observation: dict, slot: dict, bound: Decimal,
                          response_codec: str) -> tuple[Decimal, Decimal, str]:
    """Return observed retention, remaining global commitment, and outcome kind.

    A missing or contradictory worker receipt is unresolved. The caller records
    the full slot reservation as held and stops without retry.
    """
    require(isinstance(observation, dict), "processor observation is not an object")
    require(observation.get("processor_exit") == 0, "processor exit is not a settled success")
    receipt = observation.get("receipt")
    require(isinstance(receipt, dict), "worker receipt missing")
    result = receipt.get("result")
    ledger = receipt.get("ledger")
    require(isinstance(result, dict) and isinstance(ledger, dict), "worker receipt fields missing")
    require(result.get("state") == "Succeeded" and result.get("settlement_appended") is True,
            "worker job is unsettled or uncertain; full bound remains held")
    require(result.get("job") and result.get("job") == ledger.get("job"), "worker job reference mismatch")
    require(result.get("usage") is not None, "worker usage missing")
    require(result.get("estimated_cost_usd") is not None, "worker cost estimate missing")
    require(decimal(ledger.get("reservation_usd"), "worker reservation") == bound,
            "worker reservation differs from the frozen full bound")
    retained = decimal(ledger.get("retained_usd"), "worker retained amount")
    require(retained <= bound, "worker retained amount exceeds the frozen full bound")
    global_unreserved = decimal(ledger.get("unreserved_usd"), "worker global unreserved")

    outcome = observation.get("outcome")
    require(isinstance(outcome, dict), "typed outcome missing")
    kind = outcome.get("kind")
    require(kind in ALLOWED_OUTCOMES, "provider/process outcome is unresolved")
    native_path_value = receipt.get("artifact_directory")
    require(isinstance(native_path_value, str) and native_path_value, "native response directory missing")
    native_path = Path(native_path_value) / "response.json"
    native = read_json(native_path)
    require(native.get("model") == slot["model"], "native model proof mismatch")
    stop_reason = native.get("stop_reason")
    require(stop_reason in {"end_turn", "refusal", "max_tokens"}, "native stop reason is unresolved")
    classified_kind = kind
    if stop_reason == "end_turn":
        answer_text = response_text(native.get("content"), response_codec)
        require(result.get("answer") == answer_text, "worker answer differs from native end_turn text")
    if kind == "ModelRefused":
        if stop_reason == "refusal":
            classified_kind = "NativeRefusal"
        elif stop_reason == "end_turn":
            try:
                answer = json.loads(answer_text)
            except json.JSONDecodeError as error:
                raise CampaignError("task refusal native answer is not valid JSON") from error
            require(isinstance(answer, dict) and answer.get("kind") == "Refused" and
                    isinstance(answer.get("reason"), str) and answer["reason"].strip(),
                    "end_turn ModelRefused is not a valid task-level refusal answer")
            require(outcome.get("reason") == answer["reason"], "typed task refusal differs from native answer")
            classified_kind = "TaskRefusal"
        else:
            raise CampaignError("model refusal lacks native or task-level refusal proof")
    elif kind == "Truncated":
        require(stop_reason == "max_tokens", "truncation lacks matching native proof")
    elif stop_reason == "refusal" or stop_reason == "max_tokens":
        raise CampaignError("typed outcome contradicts native stop reason")
    return retained, global_unreserved, classified_kind


def one_shot_markers(output: Path) -> None:
    require(not (output / "run-started.json").exists(), "campaign already started; no restart or replay")
    require(not (output / "done.json").exists(), "campaign already finished; no restart or replay")
    require(not (output / "stopped.json").exists(), "campaign already stopped; no restart or replay")
    require(not (output / "uncertain.json").exists(), "campaign has an uncertain attempt; no replay")


def _execute_admitted_campaign(manifest_path: Path, manifest: dict, admission: dict,
                               output: Path, runner) -> dict:
    """Execute after the caller has verified the manifest and Research record."""
    frozen_manifest_hash = sha256_file(manifest_path)
    with exclusive_launch_lock(output / ".controller.lock"):
        one_shot_markers(output)
        output.mkdir(parents=True, exist_ok=True)
        one_shot_markers(output)
        global_unreserved = decimal(admission["global_unreserved_usd"], "global_unreserved_usd")
        campaign_limit = decimal(admission["campaign_limit_usd"], "campaign_limit_usd")
        retained_in_campaign = Decimal(0)
        durable_json(output / "run-started.json", {
            "manifest_sha256": sha256_file(manifest_path),
            "admission_id": admission["admission_id"],
            "started_once": True,
            "provider_calls_made": 0,
        })
        completed = 0

        for slot in manifest["slots"]:
            bound = decimal(slot["reservation_bound_usd"], "slot reservation")
            campaign_remaining = campaign_limit - retained_in_campaign
            if bound > campaign_remaining or bound > global_unreserved:
                reason = "CampaignReservationDoesNotFit" if bound > campaign_remaining else "GlobalReservationDoesNotFit"
                durable_json(output / "stopped.json", {
                    "reason": reason,
                    "next_slot": slot["identifier"],
                    "next_full_reservation_usd": str(bound),
                    "campaign_remaining_usd": str(max(Decimal(0), campaign_remaining)),
                    "global_unreserved_usd": str(global_unreserved),
                    "completed_slots": completed,
                    "no_call_for_next_slot": True,
                })
                raise CampaignError(reason)

            call_file = verify_runtime_slot(manifest_path, manifest, slot, frozen_manifest_hash)

            slot_directory = output / slot["identifier"]
            slot_directory.mkdir()
            durable_json(slot_directory / "started.json", {
                "slot": slot["identifier"],
                "stage_uuid": slot["stage_uuid"],
                "manifest_sha256": sha256_file(manifest_path),
                "reservation_bound_usd": str(bound),
                "instruction": "One invocation only. A result failure never permits replay.",
            })
            try:
                process = runner(
                    [manifest["binary"], "invoke", str(call_file), manifest["processor_configuration"]],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    timeout=manifest["processor_timeout_seconds"],
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired) as error:
                durable_json(slot_directory / "uncertain.json", {
                    "kind": "TransportOrProcessUncertainty",
                    "reason": type(error).__name__,
                    "full_reservation_held_usd": str(bound),
                    "stop": True,
                    "retry": False,
                })
                durable_json(output / "uncertain.json", {"slot": slot["identifier"], "full_reservation_held_usd": str(bound)})
                raise CampaignError("provider/process result uncertain; full bound held, stop without retry") from error

            stdout = getattr(process, "stdout", None)
            if process.returncode != 0 or not isinstance(stdout, (bytes, bytearray)):
                durable_json(slot_directory / "uncertain.json", {
                    "kind": "TransportOrProcessUncertainty",
                    "process_returncode": process.returncode,
                    "full_reservation_held_usd": str(bound),
                    "stop": True,
                    "retry": False,
                })
                durable_json(output / "uncertain.json", {"slot": slot["identifier"], "full_reservation_held_usd": str(bound)})
                raise CampaignError("processor failed or returned no receipt; full bound held, stop without retry")
            try:
                observation = json.loads(stdout)
            except (json.JSONDecodeError, UnicodeDecodeError, TypeError) as error:
                durable_json(slot_directory / "uncertain.json", {
                    "kind": "InvalidReceipt",
                    "reason": type(error).__name__,
                    "full_reservation_held_usd": str(bound),
                    "stop": True,
                    "retry": False,
                })
                durable_json(output / "uncertain.json", {"slot": slot["identifier"], "full_reservation_held_usd": str(bound)})
                raise CampaignError("invalid receipt; full bound held, stop without retry") from error

            try:
                retained, global_unreserved, outcome_kind = authoritative_receipt(
                    observation, slot, bound, manifest["model_bounds"][slot["model"]]["response_codec"])
            except CampaignError as error:
                durable_json(slot_directory / "observation.json", observation)
                durable_json(slot_directory / "uncertain.json", {
                    "kind": "InvalidOrUnsettledWorkerReceipt",
                    "reason": str(error),
                    "full_reservation_held_usd": str(bound),
                    "stop": True,
                    "retry": False,
                })
                durable_json(output / "uncertain.json", {"slot": slot["identifier"], "full_reservation_held_usd": str(bound)})
                raise CampaignError("receipt unresolved; full bound held, stop without retry") from error

            durable_json(slot_directory / "observation.json", observation)
            retained_in_campaign += retained
            receipt = observation["receipt"]
            native = read_json(Path(receipt["artifact_directory"]) / "response.json")
            durable_json(slot_directory / "measurement.json", {
                "slot": slot["identifier"],
                "category": slot["category"],
                "case": slot["case_id"],
                "task_kind": slot["task_kind"],
                "model": slot["model"],
                "replicate": slot["replicate"],
                "prompt_sha256": slot["prompt_sha256"],
                "call_sha256": slot["call_sha256"],
                "job": receipt["result"]["job"],
                "usage": receipt["result"]["usage"],
                "raw_estimated_cost_usd": receipt["result"]["estimated_cost_usd"],
                "worker_retained_usd": str(retained),
                "global_unreserved_after_receipt_usd": str(global_unreserved),
                "elapsed_milliseconds": observation.get("elapsed_milliseconds"),
                "native_stop_reason": native["stop_reason"],
                "outcome_kind": outcome_kind,
                "outcome": observation["outcome"],
                "paid_call_slot": True,
            })
            completed += 1
            if outcome_kind == "Truncated":
                durable_json(output / "stopped.json", {
                    "reason": "TruncatedOutput",
                    "slot": slot["identifier"],
                    "completed_slots": completed,
                    "worker_retained_usd": str(retained),
                    "known_result": True,
                    "retry": False,
                })
                raise CampaignError("max-token completion is recorded; stop without retry")

        durable_json(output / "done.json", {
            "manifest_sha256": sha256_file(manifest_path),
            "completed_slots": completed,
            "provider_calls_at_most": manifest["campaign_limits"]["maximum_provider_calls"],
            "worker_observations_only": True,
        })
        return {"completed_slots": completed, "result_directory": str(output)}


def _run_campaign_with_test_harness(manifest_path: Path, admission_path: Path,
                                    output_directory: Path, process_runner) -> dict:
    """Synthetic-only seam; the CLI never accepts a result-path or runner override."""
    require(output_directory is not None and process_runner is not None,
            "test harness requires explicit output directory and mock runner")
    manifest_path = manifest_path.resolve(strict=True)
    manifest = verify_manifest(manifest_path)
    admission = validate_admission(admission_path, manifest_path, manifest)
    return _execute_admitted_campaign(manifest_path, manifest, admission,
                                      output_directory.resolve(), process_runner)


def run_campaign(manifest_path: Path, admission_path: Path) -> dict:
    """Run at the manifest's frozen result path with the pinned real subprocess boundary."""
    manifest_path = manifest_path.resolve(strict=True)
    manifest = verify_manifest(manifest_path)
    admission = validate_admission(admission_path, manifest_path, manifest)
    return _execute_admitted_campaign(manifest_path, manifest, admission,
                                      Path(manifest["result_directory"]).resolve(), subprocess.run)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("verify", "dry-run", "run"))
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("proposal-manifest.json"))
    parser.add_argument("--research-admission", type=Path)
    args = parser.parse_args(argv)
    try:
        manifest_path = args.manifest.resolve(strict=True)
        manifest = verify_manifest(manifest_path)
        if args.mode == "verify":
            print(json.dumps({"slots": len(manifest["slots"]), "provider_calls": 0, "manifest_sha256": sha256_file(manifest_path)}))
            return 0
        if args.mode == "dry-run":
            print(json.dumps({
                "slots": len(manifest["slots"]),
                "provider_calls": 0,
                "models": {model: sum(slot["model"] == model for slot in manifest["slots"])
                           for model in sorted(manifest["slot_contract"]["models"])},
                "maximum_provider_calls": manifest["campaign_limits"]["maximum_provider_calls"],
                "all_configured_calls_guaranteed": False,
                "result_directory": manifest["result_directory"],
            }))
            return 0
        require(args.research_admission is not None, "run requires a Research admission record")
        result = run_campaign(manifest_path, args.research_admission)
        print(json.dumps(result))
        return 0
    except CampaignError as error:
        print(json.dumps({"error": str(error), "provider_calls": "unknown if an attempt marker exists"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
