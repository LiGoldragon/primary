"""Talk to `codex app-server` over stdio JSON-RPC, using the ~/.codex login.

Shared by codex-usage and codex-redeem-reset. The Codex binary is
CODEX_BIN if set, else `codex` on PATH, falling back to the newest
/nix/store/*-codex-0.1*/bin/codex; it must speak account/rateLimits/read with
rateLimitResetCredits (codex-cli 0.161 and later carry it).
"""

import datetime
import glob
import json
import os
import re
import subprocess
import tempfile

def _version(path):
    match = re.search(r"-codex-(\d+(?:\.\d+)*)", path)
    return tuple(int(part) for part in match.group(1).split(".")) if match else ()


def codex_candidates():
    """CODEX_BIN alone if set; else `codex` on PATH, then the newest store codex.

    The `codex` on PATH may be a wrapper that adds --remote, which app-server
    rejects; the store binaries run directly.
    """
    if os.environ.get("CODEX_BIN"):
        return [os.environ["CODEX_BIN"]]
    stored = sorted(glob.glob("/nix/store/*-codex-0.1*/bin/codex"), key=_version, reverse=True)
    return ["codex"] + stored[:1]


CODEX_BIN = codex_candidates()[0]
TIMEOUT_SECONDS = float(os.environ.get("CODEX_APP_SERVER_TIMEOUT", "30"))


def call(method, params):
    """Try each candidate codex binary until one answers."""
    failure = None
    for binary in codex_candidates():
        try:
            return call_with(binary, method, params)
        except (RuntimeError, OSError) as error:
            failure = error
    raise failure


def call_with(binary, method, params):
    """Start one app-server, initialize it, make one request, return its result."""
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"clientInfo": {"name": "codex-usage", "title": "codex-usage", "version": "0"}}},
        {"jsonrpc": "2.0", "method": "initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": method, "params": params},
    ]
    with tempfile.TemporaryDirectory() as cwd:
        process = subprocess.Popen(
            [binary, "app-server"], cwd=cwd, text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            for request in requests:
                process.stdin.write(json.dumps(request) + "\n")
            process.stdin.flush()
            for line in process.stdout:
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if message.get("id") != 2:
                    continue
                if "error" in message:
                    raise RuntimeError(f"{method}: {message['error']}")
                return message["result"]
            raise RuntimeError(f"{method}: app-server closed without a reply: "
                               + process.stderr.read()[-500:])
        finally:
            process.kill()
            process.wait(timeout=TIMEOUT_SECONDS)


def read_usage():
    return call("account/rateLimits/read", {})


def available_credits(usage):
    """Available reset credits, soonest expiry first (the TUI's order)."""
    summary = usage.get("rateLimitResetCredits")
    if summary is None:
        raise RuntimeError("no rateLimitResetCredits in the reply; "
                           "the codex used is too old, set CODEX_BIN to a newer codex")
    credits = [c for c in summary.get("credits") or [] if c["status"] == "available"]
    return sorted(credits, key=lambda c: c["expiresAt"] or float("inf"))


def local_time(timestamp):
    if timestamp is None:
        return "never"
    return datetime.datetime.fromtimestamp(timestamp).astimezone().strftime("%a %d %b %Y %H:%M %Z")


def report(usage):
    lines = [f"ordinary usage allowed: {usage.get('ordinaryUsageAllowed')}"]
    for limit_id, limit in (usage.get("rateLimitsByLimitId") or
                            {"codex": usage["rateLimits"]}).items():
        for window_name in ("primary", "secondary"):
            window = limit.get(window_name)
            if window is None:
                continue
            minutes = window.get("windowDurationMins")
            lines.append(f"{limit_id} {window_name} ({minutes} min window): "
                         f"{100 - window['usedPercent']}% left, "
                         f"resets {local_time(window.get('resetsAt'))}")
        if limit.get("rateLimitReachedType"):
            lines.append(f"{limit_id} limit reached: {limit['rateLimitReachedType']}")
    summary = usage.get("rateLimitResetCredits") or {}
    credits = available_credits(usage)
    lines.append(f"resets available: {summary.get('availableCount')} "
                 f"(details listed: {len(credits)})")
    for credit in credits:
        lines.append(f"  {credit['id']}  {credit['status']}  {credit.get('title')}  "
                     f"expires {local_time(credit['expiresAt'])}  "
                     f"granted {local_time(credit['grantedAt'])}")
    return "\n".join(lines)
