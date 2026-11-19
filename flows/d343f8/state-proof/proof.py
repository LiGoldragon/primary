#!/usr/bin/env python3
"""A frozen, one-shot, three-model system-state proof controller.

The collector only reads approved local sources. The run command has no path,
model, count, or budget overrides and cannot be used before Research admission.
"""
from __future__ import annotations

import ast
import fcntl
import hashlib
import json
import os
import re
import signal
import stat
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable, Iterable

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "configuration.json"
MANIFEST_PATH = ROOT / "manifest.json"
INPUTS_PATH = ROOT / "inputs"
SNAPSHOT_PATH = INPUTS_PATH / "snapshot.json"


class ProofError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class Emission:
    """Typed, single adapter invocation; hard_http_cap is always one."""
    slot_id: str
    model: str
    prompt_path: Path
    prompt_sha256: str
    maximum_usd: str
    hard_http_cap: int


@dataclass(frozen=True)
class Datom:
    kind: str
    value: str | None = None
    children: tuple["Datom", ...] = ()


@dataclass(frozen=True)
class Token:
    kind: str
    value: str = ""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: Any, *, pretty: bool = False) -> bytes:
    if pretty:
        rendered = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)
    else:
        rendered = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (rendered + "\n").encode("utf-8")


def json_load_strict(data: bytes | str) -> Any:
    def reject_constant(_: str) -> None:
        raise ValueError("non-finite JSON number")
    def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON object key")
            result[key] = value
        return result
    return json.loads(data, parse_constant=reject_constant, object_pairs_hook=reject_duplicate_keys)


def read_json(path: Path) -> Any:
    try:
        return json_load_strict(path.read_bytes())
    except Exception as error:
        raise ProofError("JsonInputInvalid") from error


def load_configuration() -> dict[str, Any]:
    value = read_json(CONFIG_PATH)
    if not isinstance(value, dict) or value.get("format") != "SystemStateProofConfiguration.v1":
        raise ProofError("ConfigurationInvalid")
    return value


def digest_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_identity(path_text: str, *, optional: bool = False) -> dict[str, Any]:
    path = Path(path_text)
    try:
        resolved = path.resolve(strict=True)
        info = resolved.stat()
        if not stat.S_ISREG(info.st_mode):
            raise ProofError("ClosurePathNotFile")
        return {
            "configured_path": str(path),
            "resolved_path": str(resolved),
            "sha256": digest_file(resolved),
            "size_bytes": info.st_size,
        }
    except FileNotFoundError:
        if optional:
            return {"configured_path": str(path), "state": "Missing"}
        raise ProofError("ClosureFileMissing")
    except ProofError:
        raise
    except Exception as error:
        raise ProofError("ClosureReadFailed") from error


def hash_closure(configuration: dict[str, Any]) -> dict[str, Any]:
    """Freeze the installed worker's recursive imports and policy-derived closure."""
    runtime = configuration["runtime"]
    worker_root = Path(runtime["worker_root"]).resolve(strict=True)
    entrypoint = Path(runtime["adapter_executable"]).resolve(strict=True)
    if entrypoint.parent != worker_root or not entrypoint.is_file():
        raise ProofError("WorkerEntrypointInvalid")
    policy_path = worker_root / "general-policy.json"
    native_policy_path = worker_root / "policy.json"
    settlement_policy_path = worker_root / "settlement-policy.json"
    for path in (policy_path, native_policy_path, settlement_policy_path):
        if path.is_symlink() or not path.is_file():
            raise ProofError("WorkerStaticPolicyMissing")
    try:
        general = read_json(policy_path)
        native = read_json(native_policy_path)
        settlement = read_json(settlement_policy_path)
        shared = general["shared"]
    except Exception as error:
        raise ProofError("WorkerPolicyInvalid") from error

    # Walk only local imports from the real adapter entrypoint. Built-in and
    # standard-library imports are supplied by the pinned interpreter.
    pending = [entrypoint]
    source_paths: set[Path] = set()
    while pending:
        source = pending.pop().resolve(strict=True)
        if source in source_paths:
            continue
        if source.parent != worker_root:
            raise ProofError("WorkerImportEscapesRoot")
        source_paths.add(source)
        try:
            tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        except Exception as error:
            raise ProofError("WorkerSourceParseFailed") from error
        local_modules: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                local_modules.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                local_modules.add(node.module.split(".", 1)[0])
            elif isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value.endswith(".py"):
                candidate = (worker_root / node.value).resolve()
                if candidate.parent == worker_root and candidate.is_file():
                    local_modules.add(candidate.stem)
        for module in local_modules:
            candidate = worker_root / f"{module}.py"
            if candidate.is_file():
                pending.append(candidate)

    historical_path = Path(settlement.get("historical_manifest_path", "")).resolve(strict=True)
    ca_path = Path(shared.get("ca_file", "")).resolve(strict=True)
    if not historical_path.is_file() or not ca_path.is_file():
        raise ProofError("WorkerStaticEvidenceMissing")
    if digest_file(historical_path) != settlement.get("historical_manifest_sha256"):
        raise ProofError("WorkerHistoricalManifestDrift")
    ledger_config = configuration["closure"]["mutable_ledger"]
    if (shared.get("authoritative_ledger_path") != ledger_config["path_from_worker_policy"]
            or shared.get("authoritative_ledger_identity") != ledger_config["identity_from_worker_policy"]
            or shared.get("baseline_sha256") != ledger_config["baseline_sha256_from_worker_policy"]
            or shared.get("baseline_sha256") != native.get("baseline_sha256")
            or shared.get("authoritative_ledger_path") != native.get("authoritative_ledger_path")
            or shared.get("authoritative_ledger_identity") != native.get("authoritative_ledger_identity")):
        raise ProofError("WorkerMutableLedgerMetadataDrift")
    native_digest = sha256_bytes(json.dumps(native, sort_keys=True, separators=(",", ":")).encode())
    if native_digest != shared.get("native_policy_sha256"):
        raise ProofError("WorkerNativePolicyDigestMismatch")
    if shared.get("artifact_directory_root") != runtime["worker_artifact_root"]:
        raise ProofError("WorkerArtifactRootDrift")

    files: dict[str, Any] = {
        "worker/general-policy.json": file_identity(str(policy_path)),
        "worker/policy.json": file_identity(str(native_policy_path)),
        "worker/settlement-policy.json": file_identity(str(settlement_policy_path)),
        "settlement/historical-evidence-manifest": file_identity(str(historical_path)),
        "transport/ca-bundle": file_identity(str(ca_path)),
        "controller/proof.py": file_identity(str(ROOT / "proof.py")),
        "controller/tests.py": file_identity(str(ROOT / "tests.py")),
        "controller/configuration.json": file_identity(str(CONFIG_PATH)),
    }
    for source in sorted(source_paths, key=str):
        files[f"worker-source/{source.name}"] = file_identity(str(source))
    python_path = Path(runtime["python_executable"]).resolve(strict=True)
    if not python_path.is_file():
        raise ProofError("WorkerInterpreterMissing")
    if Path(sys.executable).resolve(strict=True) != python_path:
        raise ProofError("ControllerInterpreterMismatch")
    producer_command = shared.get("producer_command")
    if not isinstance(producer_command, list) or not producer_command or not isinstance(producer_command[0], str):
        raise ProofError("WorkerProducerExecutableMissing")
    executable_paths = {
        "python_controller_worker_and_guard": str(python_path),
        "curl": shared.get("curl"),
        "bubblewrap": shared.get("bubblewrap"),
        "credential_producer": producer_command[0],
    }
    if any(not isinstance(path, str) or not path for path in executable_paths.values()):
        raise ProofError("WorkerExecutableConfigurationInvalid")
    executables = {name: file_identity(path) for name, path in sorted(executable_paths.items())}
    return {
        "worker_entrypoint": str(entrypoint),
        "files": files,
        "executables_from_installed_policy": executables,
        "mutable_accounting_input": {
            "ledger_path": shared["authoritative_ledger_path"],
            "device": shared["authoritative_ledger_identity"]["device"],
            "inode": shared["authoritative_ledger_identity"]["inode"],
            "baseline_sha256": shared["baseline_sha256"],
            "validation_owner": "unchanged worker; ledger content remains mutable",
        },
    }


def _read_bytes_bounded(path: Path, maximum: int) -> bytes:
    with path.open("rb") as stream:
        value = stream.read(maximum + 1)
    if len(value) > maximum:
        raise ProofError("InputTooLarge")
    return value


def verify_digest(data: bytes, expected: str, reason_code: str) -> None:
    if sha256_bytes(data) != expected:
        raise ProofError(reason_code)


def enforce_closure_match(expected: Any, current: Any) -> None:
    if expected != current:
        raise ProofError("ExecutionClosureDrift")


def lex_datom(text: str, maximum_tokens: int, maximum_depth: int) -> list[Token]:
    """Small Datom tokenizer: escaped closing guillemets remain string content."""
    tokens: list[Token] = []
    index = 0
    delimiters = "{}[]«»;"
    while index < len(text):
        char = text[index]
        if char.isspace():
            index += 1
            continue
        if char == ";":
            newline = text.find("\n", index)
            index = len(text) if newline < 0 else newline + 1
            continue
        if char in "{}[]":
            tokens.append(Token(char))
            index += 1
        elif char == ".":
            tokens.append(Token("dot"))
            index += 1
        elif char == "«":
            index += 1
            value: list[str] = []
            while index < len(text):
                if text[index] == "\\" and index + 1 < len(text) and text[index + 1] == "»":
                    value.append("»")
                    index += 2
                    continue
                if text[index] == "»":
                    index += 1
                    break
                value.append(text[index])
                index += 1
            else:
                raise ProofError("DatomUnterminatedString")
            tokens.append(Token("string", "".join(value)))
        else:
            start = index
            while index < len(text):
                current = text[index]
                if current.isspace() or current in delimiters:
                    break
                if current == ".":
                    decimal_dot = (
                        index > start and index + 1 < len(text)
                        and text[index - 1].isdigit() and text[index + 1].isdigit()
                    )
                    if not decimal_dot:
                        break
                index += 1
            if index == start:
                raise ProofError("DatomUnrecognizedGlyph")
            tokens.append(Token("atom", text[start:index]))
        if len(tokens) > maximum_tokens:
            raise ProofError("DatomTokenLimit")
    # Limit nesting before recursive parsing. The exact parse checks matching forms.
    depth = 0
    for token in tokens:
        if token.kind in ("{", "["):
            depth += 1
            if depth > maximum_depth:
                raise ProofError("DatomDepthLimit")
        elif token.kind in ("}", "]"):
            depth -= 1
            if depth < 0:
                raise ProofError("DatomUnbalanced")
    if depth:
        raise ProofError("DatomUnbalanced")
    return tokens


def parse_datom(text: str, maximum_tokens: int, maximum_depth: int) -> Datom:
    tokens = lex_datom(text, maximum_tokens, maximum_depth)
    position = 0

    def form(depth: int = 0) -> Datom:
        nonlocal position
        if depth > maximum_depth or position >= len(tokens):
            raise ProofError("DatomUnexpectedEnd")
        token = tokens[position]
        position += 1
        if token.kind in ("{", "["):
            close = "}" if token.kind == "{" else "]"
            members: list[Datom] = []
            while position < len(tokens) and tokens[position].kind != close:
                if tokens[position].kind in ("}", "]", "dot"):
                    raise ProofError("DatomUnexpectedDelimiter")
                members.append(form(depth + 1))
            if position >= len(tokens):
                raise ProofError("DatomUnbalanced")
            position += 1
            return Datom("struct" if token.kind == "{" else "vector", children=tuple(members))
        if token.kind == "string":
            return Datom("string", token.value)
        if token.kind != "atom":
            raise ProofError("DatomUnexpectedDelimiter")
        if position < len(tokens) and tokens[position].kind == "dot":
            position += 1
            return Datom("variant", token.value, (form(depth + 1),))
        return Datom("bare", token.value)

    root = form()
    if position != len(tokens):
        raise ProofError("DatomTrailingForms")
    return root


def _bare(value: Datom) -> str:
    if value.kind != "bare" or value.value is None:
        raise ProofError("DatomExpectedBare")
    return value.value


def _string_field(value: Any) -> str | None:
    return value if isinstance(value, str) and value else None


def _unknown_source(name: str, captured_at: str, reason: str, *, raw_sha256: str | None = None,
                    command_identity: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "source": name,
        "state": "Unknown",
        "captured_at_utc": captured_at,
        "reason_code": reason,
        "raw_sha256": raw_sha256,
        "command_identity": command_identity,
        "facts": None,
    }


def _available_source(name: str, captured_at: str, facts: Any, raw: bytes,
                      command_identity: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": name,
        "state": "Available",
        "captured_at_utc": captured_at,
        "reason_code": None,
        "raw_sha256": sha256_bytes(raw),
        "command_identity": command_identity,
        "facts": facts,
    }


def _command_identity(command: list[str]) -> dict[str, Any]:
    if not command or not isinstance(command[0], str):
        raise ProofError("CommandConfigurationInvalid")
    return file_identity(command[0])


def collect_one(name: str, command: list[str], configuration: dict[str, Any],
                parser: Callable[[bytes], Any], runner: Callable[..., Any] | None = None) -> dict[str, Any]:
    if runner is None:
        runner = subprocess.run
    start = utc_now()
    try:
        before = _command_identity(command)
    except ProofError as error:
        return _unknown_source(name, start, error.code)
    if not isinstance(command, list) or any(not isinstance(arg, str) for arg in command):
        return _unknown_source(name, start, "CommandConfigurationInvalid", command_identity=before)
    try:
        result = runner(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        timeout=configuration["timeout_seconds"], check=False)
    except subprocess.TimeoutExpired:
        return _unknown_source(name, start, "SourceTimeout", command_identity=before)
    except Exception:
        return _unknown_source(name, start, "SourceUnavailable", command_identity=before)
    finished = utc_now()
    output = result.stdout if isinstance(result.stdout, bytes) else str(result.stdout or "").encode()
    if len(output) > configuration["maximum_output_bytes"]:
        return _unknown_source(name, finished, "SourceOutputTooLarge", command_identity=before)
    if result.returncode != 0:
        return _unknown_source(name, finished, "SourceExitNonzero", raw_sha256=sha256_bytes(output),
                               command_identity=before)
    try:
        after = _command_identity(command)
    except ProofError as error:
        return _unknown_source(name, finished, error.code, raw_sha256=sha256_bytes(output),
                               command_identity=before)
    if before != after:
        return _unknown_source(name, finished, "SourceDriftDuringRead", raw_sha256=sha256_bytes(output),
                               command_identity=before)
    try:
        facts = parser(output)
    except ProofError as error:
        return _unknown_source(name, finished, error.code, raw_sha256=sha256_bytes(output),
                               command_identity=before)
    except Exception:
        return _unknown_source(name, finished, "SourceParseFailed", raw_sha256=sha256_bytes(output),
                               command_identity=before)
    return _available_source(name, finished, facts, output, before)


def _parse_flow_identity(text: str, config: dict[str, Any]) -> list[str] | None:
    try:
        root = parse_datom(text, config["maximum_output_bytes"], config["datom_maximum_depth"])
        if root.kind != "struct" or len(root.children) != 4:
            return None
        fields = [_bare(item) for item in root.children]
        if any(not field or len(field) > 80 for field in fields):
            return None
        return fields
    except ProofError:
        return None


def parse_herdr(output: bytes, config: dict[str, Any]) -> dict[str, Any]:
    try:
        document = json_load_strict(output)
        rows = document["result"]["agents"]
        if not isinstance(rows, list):
            raise ProofError("HerdrShapeUnknown")
    except ProofError:
        raise
    except Exception as error:
        raise ProofError("HerdrShapeUnknown") from error
    allowed_statuses = config["ui_status_values"]
    status_counts: dict[str, int] = {status: 0 for status in allowed_statuses}
    status_counts["Unknown"] = 0
    flows: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            status = "Unknown"
            identity = None
        else:
            observed_status = row.get("agent_status")
            status = observed_status if observed_status in allowed_statuses else "Unknown"
            display = row.get("display_agent")
            stripped = row.get("terminal_title_stripped")
            identity = _parse_flow_identity(display, config) if isinstance(display, str) else None
            other = _parse_flow_identity(stripped, config) if isinstance(stripped, str) else None
            if identity is None or (other is not None and other != identity):
                identity = None
        status_counts[status] += 1
        flows.append({"identity": identity, "ui_status": status})
    flows.sort(key=lambda row: tuple(row["identity"] or ("", "", "", "")))
    return {"flow_count": len(rows), "ui_status_counts": status_counts, "flows": flows,
            "status_semantics": "UI working/done values only; they do not establish task health."}


def parse_queues(output: bytes, config: dict[str, Any]) -> dict[str, Any]:
    try:
        root = parse_datom(output.decode("utf-8"), config["maximum_output_bytes"], config["datom_maximum_depth"])
        if root.kind != "variant" or root.value != "Queues" or len(root.children) != 1:
            raise ProofError("QueuesShapeUnknown")
        vector = root.children[0]
        if vector.kind != "vector":
            raise ProofError("QueuesShapeUnknown")
        queues: list[dict[str, Any]] = []
        for item in vector.children:
            if item.kind != "struct" or len(item.children) != 2:
                raise ProofError("QueuesShapeUnknown")
            address, messages = item.children
            if address.kind != "struct" or len(address.children) != 3 or messages.kind != "vector":
                raise ProofError("QueuesShapeUnknown")
            identity = [_bare(value) for value in address.children]
            if any(not value or len(value) > 80 for value in identity):
                raise ProofError("QueuesShapeUnknown")
            queues.append({"address": identity, "pending_messages": len(messages.children)})
        queues.sort(key=lambda row: tuple(row["address"]))
        return {
            "queue_count": len(queues),
            "pending_message_count": sum(row["pending_messages"] for row in queues),
            "queues": queues,
            "content_policy": "All message payloads and text are withheld; only queue address and count are retained.",
        }
    except UnicodeDecodeError as error:
        raise ProofError("QueuesEncodingInvalid") from error


def _unwrap_variant(value: Datom, name: str) -> Datom:
    if value.kind != "variant" or value.value != name or len(value.children) != 1:
        raise ProofError("EnergyShapeUnknown")
    return value.children[0]


def _as_decimal(value: Datom) -> str:
    raw = _bare(value)
    try:
        number = Decimal(raw)
        if not number.is_finite():
            raise InvalidOperation
        return str(number)
    except Exception as error:
        raise ProofError("EnergyNumberInvalid") from error


def parse_energy(output: bytes, config: dict[str, Any]) -> dict[str, Any]:
    try:
        root = parse_datom(output.decode("utf-8"), config["maximum_output_bytes"], config["datom_maximum_depth"])
        read = _unwrap_variant(root, "Read")
        if read.kind != "struct" or len(read.children) != 3:
            raise ProofError("EnergyShapeUnknown")
        reading, paces, _held = read.children
        if reading.kind != "struct" or len(reading.children) != 5 or paces.kind != "vector":
            raise ProofError("EnergyShapeUnknown")
        provider = _bare(reading.children[0])
        allowed_raw = _bare(reading.children[1])
        if allowed_raw not in ("True", "False"):
            raise ProofError("EnergyShapeUnknown")
        windows_node = reading.children[2]
        if windows_node.kind != "vector":
            raise ProofError("EnergyShapeUnknown")
        windows: list[dict[str, Any]] = []
        for window in windows_node.children:
            if window.kind != "struct" or len(window.children) != 4:
                raise ProofError("EnergyShapeUnknown")
            windows.append({
                "name": _bare(window.children[0]),
                "used_percent": _as_decimal(window.children[1]),
                "reset_epoch": _bare(window.children[2]),
                "duration_minutes": _bare(window.children[3]),
            })
        observed_epoch = _bare(reading.children[4])
        pace_rows: list[dict[str, Any]] = []
        for pace in paces.children:
            if pace.kind != "struct" or len(pace.children) != 9:
                raise ProofError("EnergyShapeUnknown")
            target = pace.children[2]
            if target.kind != "variant" or len(target.children) != 1:
                raise ProofError("EnergyShapeUnknown")
            target_payload = target.children[0]
            if target_payload.kind == "struct":
                target_values = [_bare(value) for value in target_payload.children]
            elif target_payload.kind == "bare":
                target_values = [target_payload.value or ""]
            else:
                raise ProofError("EnergyShapeUnknown")
            pace_rows.append({
                "provider": _bare(pace.children[0]),
                "window": _bare(pace.children[1]),
                "target_kind": target.value,
                "target_payload": target_values,
                "expected_percent": _as_decimal(pace.children[3]),
                "used_percent": _as_decimal(pace.children[4]),
                "standing": _bare(pace.children[5]),
                "legacy_trailing_values": [_bare(value) for value in pace.children[6:]],
            })
        if provider not in config["energy_provider_names"]:
            raise ProofError("EnergyProviderUnknown")
        if any(item["provider"] != provider for item in pace_rows):
            raise ProofError("EnergyProviderMismatch")
        return {
            "provider": provider,
            "allowed": allowed_raw == "True",
            "observed_epoch": observed_epoch,
            "windows": windows,
            "pace": pace_rows,
            "interpretation": "Metrics and standings are copied from deployed Energy Nexus; target payload is retained opaque.",
        }
    except UnicodeDecodeError as error:
        raise ProofError("EnergyEncodingInvalid") from error


def parse_host(output: bytes, config: dict[str, Any]) -> dict[str, Any]:
    try:
        lines = output.decode("ascii").splitlines()
        if len(lines) != 2 or not lines[0].startswith("loadavg=") or not lines[1].startswith("cpu_count="):
            raise ProofError("HostShapeUnknown")
        load = lines[0][len("loadavg="):].split()
        if len(load) != 5:
            raise ProofError("HostShapeUnknown")
        cpu_count = int(lines[1][len("cpu_count="):])
        averages = [Decimal(value) for value in load[:3]]
        runnable = load[3].split("/")
        if cpu_count <= 0 or len(runnable) != 2 or any(value < 0 for value in averages):
            raise ProofError("HostShapeUnknown")
        ratio = (averages[0] / Decimal(cpu_count)).quantize(Decimal("0.001"))
        return {
            "host": config["host_name"],
            "load_average_1m_5m_15m": [str(value) for value in averages],
            "runnable_tasks": int(runnable[0]),
            "scheduler_entities": int(runnable[1]),
            "cpu_count": cpu_count,
            "one_minute_load_per_cpu": str(ratio),
            "metric_semantics": "Load average/runnable work, not current CPU utilization.",
        }
    except ProofError:
        raise
    except Exception as error:
        raise ProofError("HostShapeUnknown") from error


def collect_snapshot(configuration: dict[str, Any], runner: Callable[..., Any] | None = None) -> dict[str, Any]:
    collection = configuration["collection"]
    per_source = {
        "flow_list": lambda raw: parse_herdr(raw, collection),
        "queues": lambda raw: parse_queues(raw, collection),
        "energy_claude": lambda raw: parse_energy(raw, collection),
        "energy_codex": lambda raw: parse_energy(raw, collection),
        "host_load": lambda raw: parse_host(raw, collection),
    }
    commands = {
        "flow_list": collection["flow_list_command"],
        "queues": collection["queue_list_command"],
        "energy_claude": collection["energy_commands"]["Claude"],
        "energy_codex": collection["energy_commands"]["Codex"],
        "host_load": collection["host_command"],
    }
    sources = {
        name: collect_one(name, commands[name], collection, parser, runner)
        for name, parser in per_source.items()
    }
    sources["host_load"]["transport_identity_files"] = {
        Path(path).name: file_identity(path, optional=True)
        for path in collection["host_transport_identity_files"]
    }
    captured_epoch = int(time.time())
    for name in ("energy_claude", "energy_codex"):
        source = sources[name]
        if source["state"] == "Available":
            observed_epoch = int(source["facts"]["observed_epoch"])
            age = captured_epoch - observed_epoch
            source["observation_metadata"] = {
                "observed_epoch": observed_epoch,
                "age_seconds_at_snapshot": age,
                "maximum_age_seconds": collection["energy_observation_maximum_age_seconds"],
            }
            source["facts"]["age_seconds_at_snapshot"] = age
            if age < 0 or age > collection["energy_observation_maximum_age_seconds"]:
                source["state"] = "Unknown"
                source["reason_code"] = "EnergyObservationStale"
                source["facts"] = None
    return {
        "format": "SystemStateProofSnapshot.v1",
        "captured_at_utc": utc_now(),
        "captured_epoch": captured_epoch,
        "snapshot_capture_maximum_age_seconds": collection["snapshot_capture_maximum_age_seconds"],
        "energy_observation_maximum_age_seconds": collection["energy_observation_maximum_age_seconds"],
        "sources": sources,
    }


def write_durable_new(path: Path, data: bytes) -> None:
    """Create a new file and sync its contents and parent directory entry."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        view = memoryview(data)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise ProofError("DurableWriteFailed")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    parent_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
    try:
        os.fsync(parent_fd)
    finally:
        os.close(parent_fd)


def durable_mkdir(path: Path, *, must_be_new: bool) -> None:
    """Sync every directory entry from the root through this path."""
    target = Path(os.path.abspath(path))
    parts = target.parts
    if not parts or parts[0] != os.sep:
        raise ProofError("ResultPathInvalid")
    flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
    current_fd = os.open(os.sep, flags)
    try:
        for index, component in enumerate(parts[1:]):
            final = index == len(parts[1:]) - 1
            try:
                child_fd = os.open(component, flags, dir_fd=current_fd)
                existed = True
            except FileNotFoundError:
                os.mkdir(component, mode=0o700, dir_fd=current_fd)
                os.fsync(current_fd)
                child_fd = os.open(component, flags, dir_fd=current_fd)
                os.fsync(child_fd)
                existed = False
            except OSError as error:
                raise ProofError("ResultPathUnsafe") from error
            if final and must_be_new and existed:
                os.close(child_fd)
                raise ProofError("RunNamespaceAlreadyExists")
            if existed:
                os.fsync(current_fd)
                os.fsync(child_fd)
            os.close(current_fd)
            current_fd = child_fd
    finally:
        os.close(current_fd)


def _lock_file(path: Path) -> int:
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags, 0o600)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            os.close(descriptor)
            raise ProofError("LaunchLockUnsafe")
        os.fsync(descriptor)
        parent_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
        try:
            os.fsync(parent_fd)
        finally:
            os.close(parent_fd)
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return descriptor
    except BlockingIOError as error:
        raise ProofError("LaunchAlreadyActive") from error
    except ProofError:
        raise
    except Exception as error:
        raise ProofError("LaunchLockFailed") from error


def _read_existing_snapshot(configuration: dict[str, Any]) -> dict[str, Any]:
    snapshot = read_json(SNAPSHOT_PATH)
    if not isinstance(snapshot, dict) or snapshot.get("format") != "SystemStateProofSnapshot.v1":
        raise ProofError("SnapshotInvalid")
    age = int(time.time()) - int(snapshot.get("captured_epoch", 0))
    if age < 0 or age > configuration["collection"]["snapshot_capture_maximum_age_seconds"]:
        raise ProofError("SnapshotStale")
    for name in ("energy_claude", "energy_codex"):
        source = snapshot.get("sources", {}).get(name, {})
        if source.get("state") == "Available":
            observed = int(source.get("facts", {}).get("observed_epoch", 0))
            source_age = int(time.time()) - observed
            if source_age < 0 or source_age > configuration["collection"]["energy_observation_maximum_age_seconds"]:
                raise ProofError("SnapshotSourceStale")
    return snapshot


def render_prompt(configuration: dict[str, Any], snapshot: dict[str, Any]) -> bytes:
    snapshot_text = json.dumps(snapshot, ensure_ascii=False, sort_keys=True, indent=2)
    template = configuration["task"]["prompt_template"]
    prompt = template.replace("{{snapshot_json}}", snapshot_text)
    return prompt.encode("utf-8")


def _decimal(value: Any) -> Decimal:
    try:
        result = Decimal(str(value))
        if not result.is_finite() or result < 0:
            raise InvalidOperation
        return result
    except Exception as error:
        raise ProofError("BudgetValueInvalid") from error


def _effective_profile(policy: dict[str, Any], model: str) -> dict[str, Any]:
    try:
        p = policy["models"][model]
        maximum_input = p["maximum_input_tokens"]
        maximum_output = p["maximum_output_tokens"]
        input_rate = str(p["reserve_input_rate_usd_per_million"])
        output_rate = str(p["output_rate_usd_per_million"])
        if type(maximum_input) is not int or type(maximum_output) is not int:
            raise ProofError("WorkerModelPolicyInvalid")
        maximum_usd = (
            Decimal(maximum_input) * _decimal(input_rate)
            + Decimal(maximum_output) * _decimal(output_rate)
        ) / Decimal(1_000_000)
        return {
            "maximum_input_tokens": maximum_input,
            "maximum_output_tokens": maximum_output,
            "reserve_input_rate_usd_per_million": input_rate,
            "output_rate_usd_per_million": output_rate,
            "maximum_usd": str(maximum_usd),
            "codec": p.get("codec"),
            "thinking": p.get("thinking"),
            "tools": p.get("tools"),
            "service_tier": p.get("service_tier"),
            "inference_geo": p.get("inference_geo"),
            "stream": p.get("stream"),
            "output_config": p.get("output_config"),
            "input_admission": p.get("input_admission"),
        }
    except ProofError:
        raise
    except Exception as error:
        raise ProofError("WorkerModelPolicyInvalid") from error


def _validate_policy_bounds(configuration: dict[str, Any], prompt: bytes) -> dict[str, Any]:
    worker_root = Path(configuration["runtime"]["worker_root"])
    try:
        general_policy = read_json(worker_root / "general-policy.json")
    except ProofError:
        raise ProofError("WorkerPolicyInvalid")
    shared = general_policy["shared"]
    if shared.get("artifact_directory_root") != configuration["runtime"]["worker_artifact_root"]:
        raise ProofError("WorkerArtifactRootDrift")
    if configuration["task"].get("system_prompt") != shared.get("system_prompt"):
        raise ProofError("WorkerSystemPromptMismatch")
    ledger = configuration["closure"]["mutable_ledger"]
    if (shared.get("authoritative_ledger_path") != ledger["path_from_worker_policy"]
            or shared.get("authoritative_ledger_identity") != ledger["identity_from_worker_policy"]
            or shared.get("baseline_sha256") != ledger["baseline_sha256_from_worker_policy"]):
        raise ProofError("WorkerLedgerPolicyDrift")
    if len(prompt) > shared.get("maximum_prompt_bytes", 0):
        raise ProofError("PromptExceedsWorkerBound")
    profiles: dict[str, Any] = {}
    bounds: dict[str, Decimal] = {}
    for model in configuration["budget"]["model_order"]:
        profile = _effective_profile(general_policy, model)
        configured = configuration["budget"]["model_bounds"][model]
        for key in ("maximum_input_tokens", "maximum_output_tokens"):
            if profile[key] != configured[key]:
                raise ProofError("ModelTokenBoundDrift")
        for key in ("reserve_input_rate_usd_per_million", "output_rate_usd_per_million"):
            if Decimal(profile[key]) != Decimal(configured[key]):
                raise ProofError("ModelRateDrift")
        if Decimal(profile["maximum_usd"]) != Decimal(configured["maximum_usd"]):
            raise ProofError("ModelReservationDrift")
        if profile["input_admission"]:
            max_input = profile["maximum_input_tokens"]
            system_bytes = len(shared["system_prompt"].encode("utf-8"))
            framing = profile["input_admission"]["framing_allowance"]
            if len(prompt) + system_bytes + framing > max_input:
                raise ProofError("PromptExceedsModelBound")
        elif len(prompt) > shared["maximum_prompt_bytes"]:
            raise ProofError("PromptExceedsWorkerBound")
        profiles[model] = profile
        bounds[model] = Decimal(profile["maximum_usd"])
    total = sum(bounds.values(), Decimal(0))
    if total != Decimal(configuration["budget"]["maximum_total_reservation_usd"]):
        raise ProofError("TotalReservationDrift")
    if total > Decimal(configuration["budget"]["maximum_usd"]):
        raise ProofError("CampaignEnvelopeTooSmall")
    return {"shared_system_prompt": shared["system_prompt"],
            "shared_worker_bounds": {"maximum_prompt_bytes": shared["maximum_prompt_bytes"],
                                     "maximum_response_bytes": shared["maximum_response_bytes"],
                                     "system_prompt_sha256": sha256_bytes(shared["system_prompt"].encode("utf-8"))},
            "model_profiles": profiles,
            "maximum_total_reservation_usd": str(total)}


def _relative_input_path(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError as error:
        raise ProofError("InputPathInvalid") from error


def validate_slot_contract(slots: Any, configuration: dict[str, Any]) -> None:
    expected_models = configuration["budget"]["model_order"]
    if not isinstance(slots, list) or len(slots) != configuration["budget"]["maximum_provider_calls"]:
        raise ProofError("FrozenSlotCountInvalid")
    if [slot.get("model") for slot in slots if isinstance(slot, dict)] != expected_models:
        raise ProofError("FrozenModelSequenceInvalid")
    if [slot.get("slot_id") for slot in slots if isinstance(slot, dict)] != [
        f"slot-{index:02d}" for index in range(1, len(expected_models) + 1)
    ]:
        raise ProofError("FrozenSlotIdentityInvalid")


def preflight_budget(emissions: Iterable[Emission], campaign_limit: str, global_headroom: str) -> None:
    total = sum((Decimal(item.maximum_usd) for item in emissions), Decimal(0))
    if total > Decimal(campaign_limit):
        raise ProofError("CampaignEnvelopeTooSmall")
    if total > Decimal(global_headroom):
        raise ProofError("ResearchGlobalHeadroomInsufficient")


def freeze_packet(configuration: dict[str, Any]) -> dict[str, Any]:
    if MANIFEST_PATH.exists():
        raise ProofError("ManifestAlreadyFrozen")
    snapshot = _read_existing_snapshot(configuration)
    prompt_bytes = render_prompt(configuration, snapshot)
    effective = _validate_policy_bounds(configuration, prompt_bytes)
    slots: list[dict[str, Any]] = []
    total = Decimal(0)
    for index, model in enumerate(configuration["budget"]["model_order"], start=1):
        slot_id = f"slot-{index:02d}"
        prompt_path = INPUTS_PATH / f"{slot_id}.prompt.txt"
        call_path = INPUTS_PATH / f"{slot_id}.call.json"
        prompt_sha = sha256_bytes(prompt_bytes)
        model_bound = configuration["budget"]["model_bounds"][model]
        call = {
            "format": "SystemStateProofCall.v1",
            "task": configuration["task"]["name"],
            "slot_id": slot_id,
            "model": model,
            "hard_http_cap": 1,
            "prompt_relative_path": _relative_input_path(prompt_path),
            "prompt_sha256": prompt_sha,
            "maximum_usd": model_bound["maximum_usd"],
            "maximum_input_tokens": model_bound["maximum_input_tokens"],
            "maximum_output_tokens": model_bound["maximum_output_tokens"],
        }
        call_bytes = canonical_json(call, pretty=True)
        write_durable_new(prompt_path, prompt_bytes)
        write_durable_new(call_path, call_bytes)
        slots.append({
            "slot_id": slot_id,
            "model": model,
            "call_relative_path": _relative_input_path(call_path),
            "call_sha256": sha256_bytes(call_bytes),
            "prompt_relative_path": _relative_input_path(prompt_path),
            "prompt_sha256": prompt_sha,
            "hard_http_cap": 1,
            "maximum_input_tokens": model_bound["maximum_input_tokens"],
            "maximum_output_tokens": model_bound["maximum_output_tokens"],
            "maximum_usd": model_bound["maximum_usd"],
        })
        total += Decimal(model_bound["maximum_usd"])
    if len(slots) != configuration["budget"]["maximum_provider_calls"]:
        raise ProofError("SlotCountMismatch")
    validate_slot_contract(slots, configuration)
    if total != Decimal(configuration["budget"]["maximum_total_reservation_usd"]):
        raise ProofError("ReservationSumMismatch")
    for path in INPUTS_PATH.glob("*.prompt.txt"):
        path.chmod(0o444)
    for path in INPUTS_PATH.glob("*.call.json"):
        path.chmod(0o444)
    frozen_at = utc_now()
    policy = _validate_policy_bounds(configuration, prompt_bytes)
    closure_hashes = hash_closure(configuration)
    manifest = {
        "format": "SystemStateProofManifest.v1",
        "project": configuration["project"],
        "frozen_at_utc": frozen_at,
        "configuration_sha256": sha256_bytes(CONFIG_PATH.read_bytes()),
        "controller_sha256": sha256_bytes((ROOT / "proof.py").read_bytes()),
        "tests_sha256": sha256_bytes((ROOT / "tests.py").read_bytes()),
        "snapshot_relative_path": _relative_input_path(SNAPSHOT_PATH),
        "snapshot_sha256": sha256_bytes(SNAPSHOT_PATH.read_bytes()),
        "source_and_runtime_closure": closure_hashes,
        "worker_effective_policy": policy,
        "slots": slots,
        "maximum_provider_calls": configuration["budget"]["maximum_provider_calls"],
        "maximum_usd": configuration["budget"]["maximum_usd"],
        "maximum_total_reservation_usd": str(total),
        "mutable_ledger": configuration["closure"]["mutable_ledger"],
        "replay_policy": "One admitted namespace, one slot intent per invocation, no retry or restart; an existing namespace is terminal.",
        "accounting_policy": "The unchanged API worker is the sole ledger writer. This controller persists response observations and receipt references only.",
    }
    manifest_bytes = canonical_json(manifest, pretty=True)
    write_durable_new(MANIFEST_PATH, manifest_bytes)
    MANIFEST_PATH.chmod(0o444)
    return {"manifest_sha256": sha256_bytes(manifest_bytes), "slots": slots,
            "maximum_total_reservation_usd": str(total), "maximum_usd": configuration["budget"]["maximum_usd"]}


def _validate_frozen_inputs(configuration: dict[str, Any], manifest: dict[str, Any], manifest_sha: str) -> list[Emission]:
    if manifest.get("format") != "SystemStateProofManifest.v1":
        raise ProofError("ManifestInvalid")
    if manifest.get("configuration_sha256") != sha256_bytes(CONFIG_PATH.read_bytes()):
        raise ProofError("ConfigurationDrift")
    if manifest.get("controller_sha256") != sha256_bytes((ROOT / "proof.py").read_bytes()):
        raise ProofError("ControllerDrift")
    if manifest.get("tests_sha256") != sha256_bytes((ROOT / "tests.py").read_bytes()):
        raise ProofError("TestsDrift")
    enforce_closure_match(manifest.get("source_and_runtime_closure"), hash_closure(configuration))
    slots = manifest.get("slots")
    validate_slot_contract(slots, configuration)
    if manifest.get("maximum_provider_calls") != len(slots):
        raise ProofError("FrozenCallCapInvalid")
    if manifest.get("maximum_usd") != configuration["budget"]["maximum_usd"]:
        raise ProofError("FrozenCampaignBoundInvalid")
    if manifest.get("maximum_total_reservation_usd") != configuration["budget"]["maximum_total_reservation_usd"]:
        raise ProofError("FrozenTotalBoundInvalid")
    verify_digest(SNAPSHOT_PATH.read_bytes(), manifest.get("snapshot_sha256", ""), "SnapshotDrift")
    snapshot = _read_existing_snapshot(configuration)
    if snapshot.get("captured_epoch") != read_json(SNAPSHOT_PATH).get("captured_epoch"):
        raise ProofError("SnapshotDrift")
    prompt_template = render_prompt(configuration, snapshot)
    policy = _validate_policy_bounds(configuration, prompt_template)
    if manifest.get("worker_effective_policy") != policy:
        raise ProofError("WorkerEffectivePolicyDrift")
    emissions: list[Emission] = []
    seen_slots: set[str] = set()
    for index, slot in enumerate(slots, start=1):
        slot_id = f"slot-{index:02d}"
        if slot.get("slot_id") != slot_id or slot_id in seen_slots:
            raise ProofError("FrozenSlotIdentityInvalid")
        seen_slots.add(slot_id)
        model = slot["model"]
        expected = configuration["budget"]["model_bounds"][model]
        call_path = ROOT / slot["call_relative_path"]
        prompt_path = ROOT / slot["prompt_relative_path"]
        if call_path.resolve().parent != INPUTS_PATH.resolve() or prompt_path.resolve().parent != INPUTS_PATH.resolve():
            raise ProofError("FrozenInputPathUnsafe")
        call_bytes = _read_bytes_bounded(call_path, configuration["collection"]["maximum_output_bytes"])
        prompt_bytes = _read_bytes_bounded(prompt_path, configuration["runtime"]["maximum_stdout_bytes"])
        verify_digest(call_bytes, slot.get("call_sha256", ""), "FrozenCallDrift")
        verify_digest(prompt_bytes, slot.get("prompt_sha256", ""), "FrozenPromptDrift")
        if prompt_bytes != prompt_template:
            raise ProofError("PromptFactsMismatch")
        call = json_load_strict(call_bytes)
        expected_call = {
            "format": "SystemStateProofCall.v1",
            "task": configuration["task"]["name"],
            "slot_id": slot_id,
            "model": model,
            "hard_http_cap": 1,
            "prompt_relative_path": slot["prompt_relative_path"],
            "prompt_sha256": slot["prompt_sha256"],
            "maximum_usd": expected["maximum_usd"],
            "maximum_input_tokens": expected["maximum_input_tokens"],
            "maximum_output_tokens": expected["maximum_output_tokens"],
        }
        if call != expected_call or slot.get("hard_http_cap") != 1:
            raise ProofError("FrozenCallDrift")
        emissions.append(Emission(slot_id, model, prompt_path, slot["prompt_sha256"],
                                  expected["maximum_usd"], 1))
    if Decimal(sum((Decimal(item.maximum_usd) for item in emissions), Decimal(0))) != Decimal(manifest["maximum_total_reservation_usd"]):
        raise ProofError("FrozenReservationSumInvalid")
    return emissions


def _parse_admission(configuration: dict[str, Any], manifest_sha: str) -> dict[str, Any]:
    path = Path(configuration["runtime"]["research_admission_path"])
    admission = read_json(path)
    required = {
        "format", "authority", "decision", "manifest_sha256", "maximum_provider_calls",
        "maximum_usd", "global_unreserved_usd", "run_namespace", "admitted_at_utc", "expires_at_utc",
    }
    if not isinstance(admission, dict) or set(admission) != required:
        raise ProofError("ResearchAdmissionShapeInvalid")
    if admission["format"] != "ResearchSystemStateAdmission.v1" or admission["authority"] != "Research" or admission["decision"] != "Admitted":
        raise ProofError("ResearchAdmissionAbsent")
    if admission["manifest_sha256"] != manifest_sha:
        raise ProofError("ResearchManifestMismatch")
    if admission["maximum_provider_calls"] != configuration["budget"]["maximum_provider_calls"]:
        raise ProofError("ResearchCallCapMismatch")
    if Decimal(admission["maximum_usd"]) != Decimal(configuration["budget"]["maximum_usd"]):
        raise ProofError("ResearchEnvelopeMismatch")
    total = Decimal(configuration["budget"]["maximum_total_reservation_usd"])
    if _decimal(admission["global_unreserved_usd"]) < total:
        raise ProofError("ResearchGlobalHeadroomInsufficient")
    run_namespace = admission["run_namespace"]
    try:
        parsed_uuid = uuid.UUID(run_namespace)
    except Exception as error:
        raise ProofError("ResearchRunNamespaceInvalid") from error
    if str(parsed_uuid) != run_namespace:
        raise ProofError("ResearchRunNamespaceInvalid")
    try:
        now = datetime.now(timezone.utc)
        starts = datetime.fromisoformat(admission["admitted_at_utc"].replace("Z", "+00:00"))
        expires = datetime.fromisoformat(admission["expires_at_utc"].replace("Z", "+00:00"))
        if starts.tzinfo is None or expires.tzinfo is None or now < starts or now >= expires:
            raise ProofError("ResearchAdmissionExpired")
    except ProofError:
        raise
    except Exception as error:
        raise ProofError("ResearchAdmissionTimeInvalid") from error
    return admission


def _safe_result_path(root: Path, artifact_directory: Any, job: Any, job_prefix: str) -> Path:
    if not isinstance(artifact_directory, str) or not isinstance(job, str):
        raise ProofError("WorkerReceiptPathInvalid")
    worker_root = root.resolve(strict=True)
    candidate = Path(artifact_directory).resolve(strict=True)
    try:
        relative = candidate.relative_to(worker_root)
    except ValueError as error:
        raise ProofError("WorkerReceiptPathInvalid") from error
    if relative.name != job or not job.startswith(job_prefix):
        raise ProofError("WorkerReceiptPathInvalid")
    return candidate


def _read_worker_receipt(stdout: bytes, exit_code: int, emission: Emission,
                         configuration: dict[str, Any]) -> dict[str, Any]:
    try:
        report = json_load_strict(stdout)
        if not isinstance(report, dict) or not isinstance(report.get("result"), dict) or not isinstance(report.get("ledger"), dict):
            raise ProofError("WorkerReceiptMissing")
        result = report["result"]
        ledger_fields = report["ledger"]
        worker_policy = read_json(Path(configuration["runtime"]["worker_root"]) / "general-policy.json")
        job_prefix = worker_policy["shared"]["job_prefix"]
        directory = _safe_result_path(Path(configuration["runtime"]["worker_artifact_root"]),
                                      report.get("artifact_directory"), result.get("job"), job_prefix)
        disk_result = read_json(directory / "result.json")
        disk_ledger = read_json(directory / "ledger-fields.json")
        if disk_result != result or disk_ledger != ledger_fields:
            raise ProofError("WorkerReceiptMismatch")
        if result.get("job") != ledger_fields.get("job"):
            raise ProofError("WorkerReceiptMismatch")
        if result.get("policy_sha256") != ledger_fields.get("policy_sha256"):
            raise ProofError("WorkerReceiptMismatch")
        if not isinstance(ledger_fields.get("reservation_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", ledger_fields["reservation_sha256"]):
            raise ProofError("WorkerReservationReceiptInvalid")
        configured_ledger = configuration["closure"]["mutable_ledger"]["path_from_worker_policy"]
        if ledger_fields.get("path") != configured_ledger:
            raise ProofError("WorkerLedgerPathMismatch")
        if type(ledger_fields.get("ordinal")) is not int or ledger_fields["ordinal"] <= 0:
            raise ProofError("WorkerOrdinalInvalid")
        if Decimal(ledger_fields.get("reservation_usd", "-1")) != Decimal(emission.maximum_usd):
            raise ProofError("WorkerReservationBoundMismatch")
        retained = Decimal(ledger_fields.get("retained_usd", "-1"))
        unreserved = Decimal(ledger_fields.get("unreserved_usd", "-1"))
        if retained < 0 or retained > Decimal(emission.maximum_usd) or unreserved < 0:
            raise ProofError("WorkerAccountingFieldsInvalid")
        if exit_code == 0 and not (result.get("state") == "Succeeded"
                and result.get("outcome_appended") is True
                and result.get("http_status") == 200
                and isinstance(result.get("usage"), dict)
                and result.get("settlement_appended") is True):
            raise ProofError("WorkerSuccessReceiptInvalid")
        if result.get("state") == "Succeeded" and exit_code != 0:
            raise ProofError("WorkerExitReceiptMismatch")
        if result.get("outcome_appended") is True and result.get("settlement_appended") is True:
            accounting_state = "Settled"
        else:
            accounting_state = "Uncertain"
        if result.get("state") == "Succeeded" and result.get("stop_reason") != "end_turn":
            raise ProofError("WorkerStopReasonMismatch")
        return {
            "report": report,
            "result": result,
            "ledger": ledger_fields,
            "directory": directory,
            "accounting_state": accounting_state,
            "retained_usd": str(retained),
            "unreserved_usd": str(unreserved),
            "receipt_sha256": sha256_bytes(canonical_json({"result": result, "ledger": ledger_fields})),
        }
    except ProofError:
        raise
    except Exception as error:
        raise ProofError("WorkerReceiptInvalid") from error


def _provider_refusal_in_response(directory: Path, configuration: dict[str, Any]) -> bool:
    try:
        response = _read_bytes_bounded(directory / "response.json", configuration["runtime"]["maximum_stdout_bytes"])
        raw = json_load_strict(response)
        if isinstance(raw, dict) and raw.get("type") == "message":
            if raw.get("stop_reason") == "refusal":
                return True
            content = raw.get("content")
            return isinstance(content, list) and any(isinstance(block, dict) and block.get("type") == "refusal" for block in content)
    except Exception:
        return False
    return False


def decode_task_answer(answer: Any, configuration: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(answer, str) or not answer.strip():
        return {"kind": "MalformedAnswer", "reason_code": "AnswerMissing"}
    try:
        decoded = json_load_strict(answer)
    except Exception:
        return {"kind": "MalformedAnswer", "reason_code": "JsonInvalid"}
    if not isinstance(decoded, dict):
        return {"kind": "MalformedAnswer", "reason_code": "TopLevelSchemaInvalid"}
    if decoded.get("kind") == "Refused":
        if set(decoded) != {"kind", "reason"}:
            return {"kind": "MalformedAnswer", "reason_code": "TaskRefusalSchemaInvalid"}
        reason = decoded.get("reason")
        if not isinstance(reason, str) or not reason.strip() or len(reason) > configuration["task"]["maximum_reason_characters"]:
            return {"kind": "MalformedAnswer", "reason_code": "TaskRefusalSchemaInvalid"}
        return {"kind": "TaskRefused", "reason": reason}
    if decoded.get("kind") != "Answered" or set(decoded) != {"kind", "answer"}:
        return {"kind": "MalformedAnswer", "reason_code": "AnswerKindInvalid"}
    body = decoded.get("answer")
    if not isinstance(body, dict) or set(body) != {"flow_load", "energy_use", "reason"}:
        return {"kind": "MalformedAnswer", "reason_code": "AnswerSchemaInvalid"}
    schema = configuration["task"]["answer_schema"]["answer"]
    for field in ("flow_load", "energy_use"):
        if not isinstance(body.get(field), str) or body[field] not in schema[field]:
            return {"kind": "MalformedAnswer", "reason_code": f"{field}Invalid"}
    reason = body.get("reason")
    if not isinstance(reason, str) or not reason.strip() or len(reason) > configuration["task"]["maximum_reason_characters"]:
        return {"kind": "MalformedAnswer", "reason_code": "ReasonInvalid"}
    return {"kind": "Answered", "answer": {"flow_load": body["flow_load"], "energy_use": body["energy_use"], "reason": reason}}


def _run_adapter(emission: Emission, configuration: dict[str, Any]) -> tuple[int | None, bytes, bytes, bool]:
    executable = configuration["runtime"]["python_executable"]
    adapter = configuration["runtime"]["adapter_executable"]
    command = [executable, "-B", adapter, emission.model, str(emission.hard_http_cap), str(emission.prompt_path)]
    environment = os.environ.copy()
    for name in ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONINSPECT"):
        environment.pop(name, None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            close_fds=True, start_new_session=True, env=environment)
    try:
        stdout, stderr = child.communicate(timeout=configuration["runtime"]["adapter_timeout_seconds"])
        maximum_stdout = configuration["runtime"]["maximum_stdout_bytes"]
        maximum_stderr = configuration["runtime"]["maximum_stderr_bytes"]
        if len(stdout) > maximum_stdout or len(stderr) > maximum_stderr:
            return child.returncode, b"", b"", True
        return child.returncode, stdout, stderr, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        try:
            child.communicate(timeout=5)
        except Exception:
            pass
        return None, b"", b"", True


def _receipt_observation(exit_code: int | None, stdout: bytes, stderr: bytes, overflow: bool,
                         emission: Emission, configuration: dict[str, Any]) -> dict[str, Any]:
    if overflow or exit_code is None:
        return {"kind": "TransportOrAccountingUncertain", "accounting_state": "Uncertain",
                "held_bound_usd": emission.maximum_usd, "reason_code": "AdapterOutputOrTimeout"}
    try:
        receipt = _read_worker_receipt(stdout, exit_code, emission, configuration)
    except ProofError as error:
        return {"kind": "TransportOrAccountingUncertain", "accounting_state": "Uncertain",
                "held_bound_usd": emission.maximum_usd, "reason_code": error.code,
                "stdout_sha256": sha256_bytes(stdout), "stderr_sha256": sha256_bytes(stderr)}
    result = receipt["result"]
    if _provider_refusal_in_response(receipt["directory"], configuration):
        kind = "ProviderNativeRefusal" if receipt["accounting_state"] == "Settled" else "ProviderNativeRefusalUncertain"
        return {"kind": kind, "accounting_state": receipt["accounting_state"],
                "held_bound_usd": emission.maximum_usd if receipt["accounting_state"] != "Settled" else receipt["retained_usd"],
                "stop_reason": "refusal", "worker_receipt_sha256": receipt["receipt_sha256"],
                "unreserved_usd": receipt["unreserved_usd"], "job": result.get("job"),
                "ordinal": receipt["ledger"].get("ordinal"),
                "artifact_directory": str(receipt["directory"]),
                "usage": result.get("usage"), "estimated_cost_usd": result.get("estimated_cost_usd")}
    if receipt["accounting_state"] != "Settled":
        return {"kind": "TransportOrAccountingUncertain", "accounting_state": "Uncertain",
                "held_bound_usd": emission.maximum_usd, "reason_code": result.get("cause", "SettlementMissing"),
                "worker_receipt_sha256": receipt["receipt_sha256"], "job": result.get("job"),
                "ordinal": receipt["ledger"].get("ordinal"),
                "artifact_directory": str(receipt["directory"]),
                "usage": result.get("usage"), "estimated_cost_usd": result.get("estimated_cost_usd")}
    if result.get("stop_reason") == "refusal":
        return {"kind": "ProviderNativeRefusal", "accounting_state": "Settled",
                "held_bound_usd": receipt["retained_usd"], "stop_reason": "refusal",
                "worker_receipt_sha256": receipt["receipt_sha256"],
                "unreserved_usd": receipt["unreserved_usd"], "job": result.get("job"),
                "ordinal": receipt["ledger"].get("ordinal"),
                "artifact_directory": str(receipt["directory"]),
                "usage": result.get("usage"), "estimated_cost_usd": result.get("estimated_cost_usd")}
    if result.get("state") == "Truncated" or result.get("stop_reason") in (
            "max_tokens", "model_context_window_exceeded"):
        partial = result.get("answer")
        partial_sha = sha256_bytes(partial.encode("utf-8")) if isinstance(partial, str) else None
        return {"kind": "TruncatedOutput", "accounting_state": "Settled",
                "held_bound_usd": receipt["retained_usd"], "stop_reason": result.get("stop_reason"),
                "partial_answer_sha256": partial_sha, "worker_receipt_sha256": receipt["receipt_sha256"],
                "unreserved_usd": receipt["unreserved_usd"], "job": result.get("job"),
                "ordinal": receipt["ledger"].get("ordinal"),
                "artifact_directory": str(receipt["directory"]),
                "usage": result.get("usage"), "estimated_cost_usd": result.get("estimated_cost_usd")}
    if result.get("stop_reason") != "end_turn":
        return {"kind": "IncompleteOutput", "accounting_state": "Settled",
                "held_bound_usd": receipt["retained_usd"], "stop_reason": result.get("stop_reason"),
                "worker_receipt_sha256": receipt["receipt_sha256"],
                "unreserved_usd": receipt["unreserved_usd"], "job": result.get("job"),
                "ordinal": receipt["ledger"].get("ordinal"),
                "artifact_directory": str(receipt["directory"]),
                "usage": result.get("usage"), "estimated_cost_usd": result.get("estimated_cost_usd")}
    decoded = decode_task_answer(result.get("answer"), configuration)
    return {**decoded, "accounting_state": "Settled", "held_bound_usd": receipt["retained_usd"],
            "worker_receipt_sha256": receipt["receipt_sha256"], "unreserved_usd": receipt["unreserved_usd"],
            "job": result.get("job"), "ordinal": receipt["ledger"].get("ordinal"),
            "artifact_directory": str(receipt["directory"]),
            "usage": result.get("usage"), "estimated_cost_usd": result.get("estimated_cost_usd")}


def _make_emission_intent(emission: Emission) -> dict[str, Any]:
    return {
        "format": "SystemStateProofSlotIntent.v1",
        "slot_id": emission.slot_id,
        "model": emission.model,
        "prompt_sha256": emission.prompt_sha256,
        "maximum_usd": emission.maximum_usd,
        "hard_http_cap": emission.hard_http_cap,
        "state": "IntentDurableBeforeAdapterBoundary",
        "created_at_utc": utc_now(),
        "retry": "forbidden",
    }


def _execute_one(emission: Emission, configuration: dict[str, Any]) -> dict[str, Any]:
    exit_code, stdout, stderr, overflow = _run_adapter(emission, configuration)
    return _receipt_observation(exit_code, stdout, stderr, overflow, emission, configuration)


def _verify_frozen_slot_before_child(configuration: dict[str, Any], manifest_sha: str,
                                     original_emissions: list[Emission], emission: Emission) -> None:
    """Recheck the complete frozen execution/input closure at each paid boundary."""
    manifest_bytes = MANIFEST_PATH.read_bytes()
    verify_digest(manifest_bytes, manifest_sha, "ManifestDriftBeforeChild")
    manifest = json_load_strict(manifest_bytes)
    current_emissions = _validate_frozen_inputs(configuration, manifest, manifest_sha)
    if current_emissions != original_emissions:
        raise ProofError("FrozenEmissionSetDrift")
    slot_index = next((index for index, item in enumerate(original_emissions)
                       if item.slot_id == emission.slot_id), None)
    if slot_index is None or original_emissions[slot_index] != emission:
        raise ProofError("FrozenEmissionDrift")


def _validate_admission_and_snapshot(configuration: dict[str, Any], manifest_sha: str) -> dict[str, Any]:
    admission = _parse_admission(configuration, manifest_sha)
    snapshot = _read_existing_snapshot(configuration)
    return {"admission": admission, "snapshot": snapshot}


def _run_admitted_once(configuration: dict[str, Any], manifest: dict[str, Any], manifest_sha: str,
                       admission: dict[str, Any], emissions: list[Emission], *,
                       invoke: Callable[[Emission, dict[str, Any]], dict[str, Any]] | None = None,
                       validate_before_child: Callable[[Emission], None] | None = None,
                       results_root: Path | None = None) -> dict[str, Any]:
    """Private transition core. Production supplies only real worker and fixed root."""
    if invoke is None:
        invoke = _execute_one
    if validate_before_child is None:
        validate_before_child = lambda emission: _verify_frozen_slot_before_child(
            configuration, manifest_sha, emissions, emission)
    if results_root is None:
        results_root = Path(configuration["runtime"]["results_root"])
    namespace = admission["run_namespace"]
    namespace_path = results_root / namespace
    durable_mkdir(results_root, must_be_new=False)
    durable_mkdir(namespace_path, must_be_new=True)
    run_intent = {
        "format": "SystemStateProofRunIntent.v1",
        "manifest_sha256": manifest_sha,
        "run_namespace": namespace,
        "maximum_provider_calls": configuration["budget"]["maximum_provider_calls"],
        "maximum_total_reservation_usd": configuration["budget"]["maximum_total_reservation_usd"],
        "state": "RunIntentDurableBeforeAnyAdapterBoundary",
        "created_at_utc": utc_now(),
    }
    write_durable_new(namespace_path / "run-intent.json", canonical_json(run_intent, pretty=True))
    report: dict[str, Any] = {
        "format": "SystemStateProofObservation.v1",
        "manifest_sha256": manifest_sha,
        "run_namespace": namespace,
        "started_at_utc": utc_now(),
        "maximum_provider_calls": configuration["budget"]["maximum_provider_calls"],
        "maximum_total_reservation_usd": configuration["budget"]["maximum_total_reservation_usd"],
        "slots": [],
        "state": "Running",
    }
    campaign_reserved = Decimal(0)
    global_unreserved = Decimal(admission["global_unreserved_usd"])
    for emission in emissions:
        bound = Decimal(emission.maximum_usd)
        campaign_remaining = Decimal(configuration["budget"]["maximum_usd"]) - campaign_reserved
        if bound > campaign_remaining or bound > global_unreserved:
            report["state"] = "StoppedBudgetAdmission"
            report["stopped_before_slot"] = emission.slot_id
            report["slots"].append({"slot_id": emission.slot_id, "kind": "NotInvokedBudgetBound", "maximum_usd": emission.maximum_usd})
            break
        slot_path = namespace_path / emission.slot_id
        durable_mkdir(slot_path, must_be_new=True)
        write_durable_new(slot_path / "intent.json", canonical_json(_make_emission_intent(emission), pretty=True))
        try:
            validate_before_child(emission)
        except ProofError as error:
            report["state"] = "StoppedFrozenInputDrift"
            report["stopped_before_slot"] = emission.slot_id
            report["slots"].append({"slot_id": emission.slot_id, "kind": "NotInvokedFrozenInputDrift",
                                    "reason_code": error.code, "maximum_usd": emission.maximum_usd})
            break
        observation = invoke(emission, configuration)
        slot_record = {
            "slot_id": emission.slot_id,
            "model": emission.model,
            "maximum_usd": emission.maximum_usd,
            "observation": observation,
            "observed_at_utc": utc_now(),
        }
        write_durable_new(slot_path / "observation.json", canonical_json(slot_record, pretty=True))
        report["slots"].append(slot_record)
        if observation.get("accounting_state") != "Settled":
            report["state"] = "StoppedTransportOrAccountingUncertain"
            report["held_bound_usd"] = emission.maximum_usd
            break
        campaign_reserved += bound
        global_unreserved = Decimal(observation["unreserved_usd"])
        if observation.get("kind") in ("ProviderNativeRefusal", "ProviderNativeRefusalUncertain"):
            report["state"] = "StoppedProviderNativeRefusal"
            break
        if observation.get("kind") in ("TruncatedOutput", "IncompleteOutput"):
            report["state"] = "StoppedTruncatedOrIncompleteOutput"
            break
    else:
        report["state"] = "Complete"
    report["finished_at_utc"] = utc_now()
    write_durable_new(namespace_path / "report.json", canonical_json(report, pretty=True))
    return report


def collect_mode() -> dict[str, Any]:
    configuration = load_configuration()
    if MANIFEST_PATH.exists() or SNAPSHOT_PATH.exists():
        raise ProofError("CollectionAlreadyFrozenOrPresent")
    snapshot = collect_snapshot(configuration)
    snapshot_bytes = canonical_json(snapshot, pretty=True)
    write_durable_new(SNAPSHOT_PATH, snapshot_bytes)
    SNAPSHOT_PATH.chmod(0o444)
    return {"snapshot_sha256": sha256_bytes(snapshot_bytes),
            "source_states": {name: source["state"] for name, source in snapshot["sources"].items()},
            "captured_at_utc": snapshot["captured_at_utc"]}


def freeze_mode() -> dict[str, Any]:
    configuration = load_configuration()
    return freeze_packet(configuration)


def run_campaign() -> dict[str, Any]:
    """Production entry point; fixed manifest, admission, lock, result root, and real worker."""
    configuration = load_configuration()
    lock = _lock_file(Path(configuration["runtime"]["launch_lock_path"]))
    try:
        manifest_bytes = MANIFEST_PATH.read_bytes()
        manifest_sha = sha256_bytes(manifest_bytes)
        manifest = json_load_strict(manifest_bytes)
        emissions = _validate_frozen_inputs(configuration, manifest, manifest_sha)
        admission = _parse_admission(configuration, manifest_sha)
        _read_existing_snapshot(configuration)
        # Admission must cover the full conservative sum before the first child boundary.
        preflight_budget(emissions, configuration["budget"]["maximum_usd"], admission["global_unreserved_usd"])
        return _run_admitted_once(configuration, manifest, manifest_sha, admission, emissions)
    finally:
        os.close(lock)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1 or args[0] not in ("collect", "freeze", "run"):
        print(json.dumps({"state": "Refused", "reason_code": "Usage"}, sort_keys=True))
        return 2
    try:
        if args[0] == "collect":
            result = collect_mode()
        elif args[0] == "freeze":
            result = freeze_mode()
        else:
            result = run_campaign()
        print(json.dumps({"state": "Succeeded", **result}, ensure_ascii=False, sort_keys=True))
        return 0
    except ProofError as error:
        print(json.dumps({"state": "Refused", "reason_code": error.code}, sort_keys=True))
        return 2
    except Exception:
        print(json.dumps({"state": "Refused", "reason_code": "InternalError"}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
