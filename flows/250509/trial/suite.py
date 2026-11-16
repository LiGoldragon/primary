"""Bounded serial experiment driver. Only the reviewed processor owns accounting.

The output files are task observations, never a second reservation/spend ledger.
An existing slot marker prevents a second invocation after an interrupted call.
"""
import argparse
import collections
from decimal import Decimal
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def write_once(path, value):
    with path.open("x") as output:
        json.dump(value, output, ensure_ascii=False, indent=2)
        output.write("\n")
        output.flush()
        os.fsync(output.fileno())


def verify(config):
    for item in config["frozen_files"]:
        require(digest(item["path"]) == item["sha256"], "frozen input changed: " + item["path"])
    slots = config["slots"]
    counts = collections.Counter(slot["model"] for slot in slots)
    require(all(model in config["reservation_bounds"] for model in counts), "unsupported model")
    require(all(count <= config["maximum_slots_per_model"] for count in counts.values()), "slot cap exceeded")
    require(len({slot["identifier"] for slot in slots}) == len(slots), "duplicate slot")
    require(config["http_cap_per_slot"] == 1, "processor contract requires cap one")
    for slot in slots:
        call = json.loads(Path(slot["call_file"]).read_text())
        require(call["model"] == slot["model"], "model mismatch")
        require(digest(slot["prompt_file"]) == slot["prompt_sha256"], "prompt changed")
        require(call["prompt_file"] == slot["prompt_file"], "prompt path mismatch")
    return counts


def observe(config, slot):
    if slot.get("reuse"):
        # Reuse only exact prior question/model/prompt bytes, not a similar case.
        prior = json.loads(Path(slot["reuse"]["call_file"]).read_text())
        current = json.loads(Path(slot["call_file"]).read_text())
        require(prior == current, "reused call differs")
        require(digest(prior["prompt_file"]) == slot["prompt_sha256"], "reused prompt differs")
        return json.loads(Path(slot["reuse"]["observation_file"]).read_text())
    process = subprocess.run(
        [config["binary"], "invoke", slot["call_file"], config["processor_configuration"]],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    require(process.returncode == 0, "Rust process failed; attempt uncertain, stop without retry")
    return json.loads(process.stdout)


def valid_receipt(observation):
    receipt = observation.get("receipt") or {}
    result = receipt.get("result") or {}
    require(observation["processor_exit"] == 0, "processor unsuccessful; no retry")
    require(result.get("state") == "Succeeded" and result.get("settlement_appended") is True,
            "receipt unsuccessful or uncertain; no retry")
    require(result.get("job") == (receipt.get("ledger") or {}).get("job"), "job reference mismatch")
    require(result.get("usage") is not None, "usage missing")
    require(observation["outcome"]["kind"] != "ProviderFailed", "provider/native proof failure")
    native = json.loads((Path(receipt["artifact_directory"]) / "response.json").read_text())
    require(native.get("stop_reason") in {"end_turn", "refusal", "max_tokens"}, "unrecognized stop reason")
    return Decimal(receipt["ledger"]["retained_usd"]), native["stop_reason"]


def run(config):
    output = Path(config["output_directory"])
    output.mkdir(exist_ok=True)
    with (output / "suite.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        spent = Decimal(config["initial_retained_usd"])
        limit = Decimal(config["maximum_retained_usd"])
        for slot in config["slots"]:
            verify(config)
            directory = output / slot["identifier"]
            directory.mkdir()  # Existing slot, successful or uncertain, is never repeated.
            if not slot.get("reuse"):
                require(spent + Decimal(config["reservation_bounds"][slot["model"]]) <= limit,
                        "next full reservation cannot fit the remaining trial envelope")
            write_once(directory / "started.json", {"slot": slot, "instruction": "No retry; inspect authoritative processor evidence after uncertainty."})
            observation = observe(config, slot)
            write_once(directory / "observation.json", observation)
            retained, stop_reason = valid_receipt(observation)
            if not slot.get("reuse"):
                spent += retained
            receipt = observation["receipt"]
            write_once(directory / "measurement.json", {
                "slot": slot["identifier"], "model": slot["model"], "case": slot["case"],
                "reused": bool(slot.get("reuse")), "prompt_sha256": slot["prompt_sha256"],
                "job": receipt["result"]["job"], "artifact_directory": receipt["artifact_directory"],
                "usage": receipt["result"]["usage"], "raw_estimated_cost_usd": receipt["result"]["estimated_cost_usd"],
                "retained_usd": str(retained), "stop_reason": stop_reason,
                "elapsed_milliseconds": observation["elapsed_milliseconds"], "outcome": observation["outcome"],
            })
            print(json.dumps({"slot": slot["identifier"], "outcome": observation["outcome"]["kind"], "observed_trial_retained_usd": str(spent)}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["dry", "run"])
    parser.add_argument("configuration", type=Path)
    args = parser.parse_args()
    config = json.loads(args.configuration.read_text())
    counts = verify(config)
    if args.mode == "dry":
        print(json.dumps({"slots_by_model": counts, "reused": sum(bool(slot.get("reuse")) for slot in config["slots"]), "http_cap": config["http_cap_per_slot"], "paid_calls": 0}))
    else:
        run(config)


if __name__ == "__main__":
    main()
