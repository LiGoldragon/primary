#!/usr/bin/env python3
"""Immutable prompt recovery archive.

Materialize exactly one unified diff against a known full prompt, store the
result under its SHA-256 address, and retain parent and diff provenance.  The
archive contains prompt bytes, never an interpreted or reconstructed prompt.
"""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import datetime, timezone


SCHEMA = "prompt-archive/v1"


def fail(message):
    raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).digest()


def atomic_write(path, data, mode=0o600):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".tmp-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def split_lines(data):
    # keepends prevents a patch from silently changing final-newline semantics.
    return data.decode("utf-8").splitlines(keepends=True)


def parse_range(value):
    fields = value.split(",", 1)
    try:
        start = int(fields[0])
        count = int(fields[1]) if len(fields) == 2 else 1
    except ValueError:
        fail("invalid unified-diff range")
    if start < 0 or count < 0:
        fail("negative unified-diff range")
    return start, count


def apply_unified_diff(base, diff):
    """Apply a deliberately narrow unified diff and reject every ambiguity."""
    source = split_lines(base)
    try:
        rows = diff.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        fail("diff must be UTF-8 unified diff")
    output, cursor, index, hunks = [], 0, 0, 0
    while index < len(rows):
        row = rows[index]
        if row.startswith(("--- ", "+++ ")):
            index += 1
            continue
        if not row.startswith("@@ "):
            fail("diff contains content outside a unified hunk")
        try:
            header = row.rstrip("\r\n").split(" @@", 1)[0].split()
            old_start, old_count = parse_range(header[1][1:])
            new_start, new_count = parse_range(header[2][1:])
        except (IndexError, ValueError):
            fail("invalid unified-diff hunk header")
        expected = old_start - 1 if old_start else 0
        if expected < cursor or expected > len(source):
            fail("unified-diff hunk order or source range is invalid")
        output.extend(source[cursor:expected])
        cursor = expected
        index += 1
        seen_old = seen_new = 0
        while index < len(rows) and not rows[index].startswith("@@ "):
            item = rows[index]
            if item.startswith("\\ No newline at end of file"):
                # The preceding actual line already carries the exact newline
                # from input text; accepting this marker would be misleading.
                fail("no-newline markers are unsupported; supply exact line endings")
            if not item or item[0] not in " +-":
                fail("invalid unified-diff hunk line")
            mark, body = item[0], item[1:]
            if mark in " -":
                if cursor >= len(source) or source[cursor] != body:
                    fail("unified-diff context does not match the supplied full prompt")
                cursor += 1
                seen_old += 1
            if mark in " +":
                output.append(body)
                seen_new += 1
            index += 1
        if (seen_old, seen_new) != (old_count, new_count):
            fail("unified-diff hunk line counts do not match its header")
        hunks += 1
    if not hunks:
        fail("diff has no unified hunks")
    output.extend(source[cursor:])
    result = "".join(output).encode("utf-8")
    if result == base:
        fail("diff is a no-op; refusing to create a duplicate version")
    return result


class Archive:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.objects = self.root / "objects" / "sha256"
        self.records = self.root / "records"

    def content_path(self, hex_digest):
        return self.objects / hex_digest[:2] / hex_digest / "content"

    def digest_path(self, hex_digest):
        return self.objects / hex_digest[:2] / hex_digest / "sha256"

    def record_path(self, short_id):
        return self.records / f"{short_id}.json"

    def store_object(self, data):
        raw = digest(data)
        hex_digest = raw.hex()
        content, stored_digest = self.content_path(hex_digest), self.digest_path(hex_digest)
        if content.exists() or stored_digest.exists():
            if not (content.is_file() and stored_digest.is_file() and content.read_bytes() == data and stored_digest.read_bytes() == raw):
                fail("content-addressed object collision or archive corruption")
        else:
            atomic_write(content, data)
            atomic_write(stored_digest, raw)
        return raw

    def unique_id(self, raw):
        full = raw.hex()
        for length in range(12, 65):
            candidate = full[:length]
            existing = [path for path in self.records.glob("*.json") if path.stem.startswith(candidate)]
            if not existing:
                return candidate
            if any(json.loads(path.read_text()).get("prompt_sha256") == full for path in existing):
                fail("version already exists; use its ID rather than resnapshotting")
        fail("unable to choose a collision-free short ID")

    def resolve(self, value):
        if not value or any(char not in "0123456789abcdef" for char in value):
            fail("ID must be a lowercase hexadecimal prefix")
        matches = [path for path in self.records.glob("*.json") if path.stem.startswith(value)]
        if len(matches) != 1:
            fail("ID resolves to zero or multiple archived versions")
        return json.loads(matches[0].read_text()), matches[0]

    def seed(self, base):
        """Archive a known-good full prompt once, as the root of a chain."""
        raw = self.store_object(base)
        existing = [path for path in self.records.glob("*.json")
                    if json.loads(path.read_text()).get("prompt_sha256") == raw.hex()]
        if existing:
            return json.loads(existing[0].read_text())
        short_id = self.unique_id(raw)
        record = {
            "schema": SCHEMA, "id": short_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "prompt_sha256": raw.hex(),
            "prompt_sha256_binary_base64": base64.b64encode(raw).decode(),
            "parent_id": None, "parent_prompt_sha256": None,
            "diff_sha256": None, "diff_sha256_binary_base64": None,
            "materialization": "known-good-full-prompt-v1",
        }
        atomic_write(self.record_path(short_id), (json.dumps(record, sort_keys=True, indent=2) + "\n").encode())
        return record

    def snapshot(self, base, patch, parent):
        result = apply_unified_diff(base, patch)
        parent_raw = digest(base)
        if parent:
            parent_record, _ = self.resolve(parent)
            if parent_record["prompt_sha256"] != parent_raw.hex():
                fail("declared parent does not match the supplied known-good full prompt")
        else:
            parent_record = self.seed(base)
            parent = parent_record["id"]
        prompt_raw = self.store_object(result)
        diff_raw = self.store_object(patch)
        short_id = self.unique_id(prompt_raw)
        record = {
            "schema": SCHEMA,
            "id": short_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "prompt_sha256": prompt_raw.hex(),
            "prompt_sha256_binary_base64": base64.b64encode(prompt_raw).decode(),
            "parent_id": parent or None,
            "parent_prompt_sha256": parent_raw.hex(),
            "diff_sha256": diff_raw.hex(),
            "diff_sha256_binary_base64": base64.b64encode(diff_raw).decode(),
            "materialization": "strict-unified-diff-v1",
        }
        atomic_write(self.record_path(short_id), (json.dumps(record, sort_keys=True, indent=2) + "\n").encode())
        return record

    def get(self, value):
        record, _ = self.resolve(value)
        raw = bytes.fromhex(record["prompt_sha256"])
        content, stored_digest = self.content_path(raw.hex()), self.digest_path(raw.hex())
        if not content.is_file() or not stored_digest.is_file() or stored_digest.read_bytes() != raw:
            fail("prompt object or its binary SHA-256 digest is absent or corrupt")
        data = content.read_bytes()
        if digest(data) != raw:
            fail("prompt object SHA-256 does not match its address")
        return record, data

    def verify(self, value):
        record, data = self.get(value)
        checked = [record["id"]]
        while record["parent_id"]:
            parent, parent_data = self.get(record["parent_id"])
            if record["parent_prompt_sha256"] != digest(parent_data).hex():
                fail(f"parent provenance digest mismatch at {record['id']}")
            patch_raw = bytes.fromhex(record["diff_sha256"])
            patch_path, patch_digest_path = self.content_path(patch_raw.hex()), self.digest_path(patch_raw.hex())
            if not patch_path.is_file() or not patch_digest_path.is_file() or patch_digest_path.read_bytes() != patch_raw or digest(patch_path.read_bytes()) != patch_raw:
                fail(f"diff object is absent or corrupt at {record['id']}")
            if apply_unified_diff(parent_data, patch_path.read_bytes()) != data:
                fail(f"diff does not reproduce prompt at {record['id']}")
            record, data = parent, parent_data
            checked.append(record["id"])
        if record["materialization"] != "known-good-full-prompt-v1" or record["diff_sha256"] is not None:
            fail("chain root is not a known-good full-prompt snapshot")
        return {"schema": SCHEMA, "id": value, "verified": True, "chain": checked}


def read_file(name):
    return Path(name).read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, help="archive directory")
    commands = parser.add_subparsers(dest="command", required=True)
    materialize = commands.add_parser("materialize", help="apply strict diff and snapshot the resulting full prompt")
    materialize.add_argument("--base", required=True, help="known-good full prompt file")
    materialize.add_argument("--diff", required=True, help="caller-supplied UTF-8 unified diff")
    materialize.add_argument("--parent", help="archived parent ID; required when base is an archived version")
    get = commands.add_parser("get", help="write the exact refreshable full prompt")
    get.add_argument("--id", required=True)
    get.add_argument("--output", help="file to write; default is stdout")
    info = commands.add_parser("info", help="print version provenance")
    info.add_argument("--id", required=True)
    verify = commands.add_parser("verify", help="verify objects and full parent/diff chain")
    verify.add_argument("--id", required=True)
    args = parser.parse_args()
    archive = Archive(args.archive)
    try:
        if args.command == "materialize":
            print(json.dumps(archive.snapshot(read_file(args.base), read_file(args.diff), args.parent), sort_keys=True))
        elif args.command == "get":
            _, data = archive.get(args.id)
            if args.output:
                atomic_write(Path(args.output), data)
            else:
                sys.stdout.buffer.write(data)
        elif args.command == "info":
            record, _ = archive.resolve(args.id)
            print(json.dumps(record, sort_keys=True, indent=2))
        else:
            print(json.dumps(archive.verify(args.id), sort_keys=True))
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
