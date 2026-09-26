"""What the scenarios observe: receipts on the wire, the recipient's pane,
and the recipient harness's own transcript (the target-side record of the
exact bytes that arrived)."""

import json
import pathlib
import re
import secrets
import time

from environment import CLAUDE_HOME, CODEX_HOME

RECEIPT = re.compile(r'\{ ([0-9a-f]{6}) (NotRequested|Observed|Unobserved) ([A-Za-z]+(?:\.[A-Za-z]+(?:\.\S+)?)?) \}')
MESSAGE_ID = re.compile(r'\b(m-[0-9a-f]+)\b')


def token(prefix):
    return f'{prefix}-{secrets.token_hex(3)}'


def receipts(reply):
    """{flow_id: (interrupt witness, grade)} from a Submitted/Receipts/ReceiptObserved line."""
    found = {}
    for flow_id, witness, grade in RECEIPT.findall(reply):
        found[flow_id] = (witness, grade)
    observed = re.match(r'ReceiptObserved\.\{ ([0-9a-f]{6}) (\S+) (.+) \}$', reply.strip())
    if observed:
        found[observed.group(1)] = (observed.group(2), observed.group(3))
    return found


def message_id(reply):
    match = MESSAGE_ID.search(reply)
    return match.group(1) if match else None


def unescape(text):
    return text.replace('\\»', '»')


class Transcripts:
    """User-role texts a harness recorded, found by a unique token."""

    def __init__(self, since):
        self.since = since

    def _files(self, harness):
        if harness == 'codex':
            roots = [CODEX_HOME / 'sessions']
            pattern = '**/*.jsonl'
        else:
            roots = [path for path in (CLAUDE_HOME / 'projects').glob('*flow-message-sandbox*')]
            pattern = '*.jsonl'
        for root in roots:
            for path in root.glob(pattern):
                try:
                    if path.stat().st_mtime >= self.since:
                        yield path
                except OSError:
                    continue

    @staticmethod
    def _user_text(harness, record):
        if harness == 'codex':
            payload = record.get('payload') or {}
            if record.get('type') == 'response_item' and payload.get('type') == 'message' \
                    and payload.get('role') == 'user':
                return ''.join(part.get('text', '') for part in payload.get('content', [])
                               if isinstance(part, dict))
            return None
        if record.get('type') != 'user':
            return None
        content = (record.get('message') or {}).get('content')
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return ''.join(part.get('text', '') for part in content
                           if isinstance(part, dict) and part.get('type') == 'text')
        return None

    def user_texts(self, harness, needle):
        texts = []
        for path in self._files(harness):
            try:
                with open(path, errors='replace') as handle:
                    for line in handle:
                        if needle not in line:
                            continue
                        try:
                            text = self._user_text(harness, json.loads(line))
                        except ValueError:
                            continue
                        if text and needle in text:
                            texts.append({'file': str(path), 'text': text})
            except OSError:
                continue
        return texts

    def session_user_texts(self, harness, path):
        """Every user-role text of one transcript, in order."""
        texts = []
        with open(path, errors='replace') as handle:
            for line in handle:
                try:
                    text = self._user_text(harness, json.loads(line))
                except ValueError:
                    continue
                if text:
                    texts.append(text[:300])
        return texts

    def wait_user_texts(self, harness, needle, timeout_seconds):
        deadline = time.monotonic() + timeout_seconds
        while True:
            texts = self.user_texts(harness, needle)
            if texts or time.monotonic() > deadline:
                return texts
            time.sleep(1)


def evidence_file(directory, name, text):
    path = pathlib.Path(directory) / name
    path.write_text(text)
    return str(path)
