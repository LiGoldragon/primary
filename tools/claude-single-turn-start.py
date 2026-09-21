#!/usr/bin/env python3
"""Freeze one complete native Claude first prompt; optionally start it through Herdr.

This records a structured first-user-message receipt. It does not claim that
Claude's slash Skill command ran or that the text entered developer role.
"""

import argparse
import hashlib
import json
import pathlib
import subprocess
import time
import uuid

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = pathlib.Path('/git/github.com/LiGoldragon/Curriculum/skills')
CHUNK_BYTES = 8_000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_pinned(path, expected):
    data = path.read_bytes()
    if digest(data) != expected:
        raise ValueError(f'changed source: {path}')
    return data.decode('utf-8')


def user_turns(transcript, lines):
    selected = {}
    with transcript.open() as stream:
        for number, line in enumerate(stream, 1):
            if number not in lines:
                continue
            entry = json.loads(line)
            payload = entry.get('payload', {})
            if entry.get('type') != 'response_item' or payload.get('type') != 'message' or payload.get('role') != 'user':
                raise ValueError(f'line {number} is not a native user message')
            blocks = payload.get('content', [])
            if len(blocks) != 1 or blocks[0].get('type') != 'input_text':
                raise ValueError(f'line {number} is not one plain user message')
            selected[number] = (entry.get('timestamp'), blocks[0]['text'])
    if set(selected) != set(lines):
        raise ValueError('native user turn missing')
    return selected


def assemble(profile, root=ROOT, skill_root=SKILLS):
    if profile['role'] != 'PsycheHigh' or profile['predecessor'] != 'f38926':
        raise ValueError('this path is scoped to the PsycheHigh successor')
    if len(profile['skills']) != len(set(profile['skills'])) or 'main-flow' not in profile['skills']:
        raise ValueError('duplicate or missing main-flow skill')
    sections = [
        '# PsycheHigh native first turn',
        'You are a fresh PsycheHigh successor to f38926. That predecessor has been reaped; do not resume or wake it. This is one assembled first user-role message. Each complete skill block below is applicable context. Claim no Flow identity or readiness until the native first-turn receipt has been checked. Reply only BOOTSTRAP_READY. Do not use tools in this first turn.',
    ]
    inputs = []
    for name in profile['skills']:
        path = skill_root / f'{name}.md'
        body = path.read_bytes()
        source_hash = digest(body)
        inputs.append({'kind': 'skill', 'name': name, 'path': str(path), 'sha256': source_hash})
        sections.append(f'<skill>\n<name>{name}</name>\n<path>{path}</path>\n{body.decode("utf-8").rstrip()}\n</skill>')
    for source in profile['sources']:
        relative = source['path']
        if pathlib.PurePath(relative).is_absolute() or '..' in pathlib.PurePath(relative).parts:
            raise ValueError('source path must be workspace-relative')
        path = root / relative
        body = read_pinned(path, source['sha256'])
        inputs.append({'kind': 'source', 'path': relative, 'sha256': source['sha256']})
        sections.append(f'<source path="{relative}">\n{body.rstrip()}\n</source>')
    transcript_spec = profile['native_user_turns']
    transcript = pathlib.Path(transcript_spec['path'])
    turns = user_turns(transcript, transcript_spec['lines'])
    for number in transcript_spec['lines']:
        timestamp, body = turns[number]
        turn_hash = digest(body.encode())
        inputs.append({'kind': 'native-user-turn', 'path': str(transcript), 'line': number, 'timestamp': timestamp, 'sha256': turn_hash})
        sections.append(f'<source kind="native-user-turn" path="{transcript}" line="{number}" timestamp="{timestamp}">\n{body}\n</source>')
    prefix = '\n\n'.join(sections) + '\n\n'
    payload_hash = digest(prefix.encode())
    prompt = prefix
    encoded = prompt.encode()
    return prompt, {'payload_sha256': payload_hash, 'prompt_sha256': digest(encoded), 'prompt_bytes': len(encoded), 'inputs': inputs, 'receipt_kind': 'first-user-message-structured-context'}


def herdr(session, *args):
    return subprocess.check_output(['herdr', '--session', session, *args], stdin=subprocess.DEVNULL, text=True)


def native_users(path):
    if not path.exists():
        return []
    entries = [json.loads(line) for line in path.read_text().splitlines()]
    return [entry['message']['content'] for entry in entries
            if entry.get('type') == 'user' and isinstance(entry.get('message', {}).get('content'), str)]


def launch(prepared, session, pane, name, model, effort):
    # This historical path sends `claude` into a Herdr shell without proving
    # that the shell has an isolated CLAUDE_JOB_DIR.  A shared job directory
    # makes /rename propagate to sibling native sessions.
    raise RuntimeError('historical Claude launch cannot prove isolated job state; use native-batch-refresh')
    prompt = pathlib.Path(prepared['prompt_path']).read_text()
    if digest(prompt.encode()) != prepared['prompt_sha256']:
        raise ValueError('frozen prompt changed')
    native_id = str(uuid.uuid4())
    transcript = pathlib.Path.home() / '.claude/projects' / ('-' + str(ROOT).strip('/').replace('/', '-')) / f'{native_id}.jsonl'
    if transcript.exists():
        raise RuntimeError('fresh native transcript already exists')
    # A blank native TUI makes no model turn. Herdr sends the complete prompt
    # in small literal chunks; only the final Enter submits the first turn.
    started = json.loads(herdr(session, 'agent', 'start', name, '--kind', 'claude', '--pane', pane,
                               '--timeout', '60000', '--', '--model', model, '--effort', effort,
                               '--dangerously-skip-permissions', '--session-id', native_id,
                               '--remote-control', 'PsycheHigh'))
    agent = started.get('result', {}).get('agent', {})
    if agent.get('name') != name or agent.get('pane_id') != pane or agent.get('agent') != 'claude' or agent.get('interactive_ready') is not True:
        raise RuntimeError('Herdr did not bind exact fresh Claude target')
    if native_users(transcript):
        raise RuntimeError('fresh native session already received a user turn')
    chunks = []
    current = ''
    for character in prompt:
        if len((current + character).encode()) > CHUNK_BYTES:
            chunks.append(current)
            current = ''
        current += character
    if current:
        chunks.append(current)
    for chunk in chunks:
        herdr(session, 'pane', 'send-text', pane, chunk)
    # Claude collapses large pasted chunks in the editor, so the payload tail
    # is not necessarily visible before submission. The native transcript hash
    # below is the acceptance boundary for the exact first message.
    visible = herdr(session, 'pane', 'read', pane, '--lines', '25')
    if '[Pasted text #' not in visible:
        raise RuntimeError('Herdr input did not show the assembled paste')
    time.sleep(1)
    if native_users(transcript):
        raise RuntimeError('model woke before final Enter')
    herdr(session, 'pane', 'send-keys', pane, 'Enter')
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        users = native_users(transcript)
        if users:
            if len(users) != 1 or digest(users[0].encode()) != prepared['prompt_sha256']:
                raise RuntimeError('native first user turn differs from frozen prompt')
            return {'native_session_id': native_id, 'transcript': str(transcript),
                    'herdr_session': session, 'herdr_agent': name, 'herdr_pane': pane,
                    'first_user_turn_sha256': prepared['prompt_sha256'],
                    'first_user_turn_exact': True, 'remote_list_visible': None}
        time.sleep(.25)
    raise RuntimeError('native first user turn was not observed')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--launch', action='store_true')
    parser.add_argument('--herdr-session')
    parser.add_argument('--herdr-pane')
    parser.add_argument('--herdr-agent')
    args = parser.parse_args()
    profile = json.loads(pathlib.Path(args.profile).read_text())
    prompt, record = assemble(profile)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    prompt_path = out / 'first-prompt.txt'
    prompt_path.write_text(prompt)
    record.update({'prompt_path': str(prompt_path), 'profile': str(pathlib.Path(args.profile).resolve()), 'model': profile['model'], 'effort': profile['effort'], 'role': profile['role']})
    (out / 'prepared.json').write_text(json.dumps(record, indent=2) + '\n')
    if args.launch:
        if not all((args.herdr_session, args.herdr_pane, args.herdr_agent)):
            raise ValueError('exact Herdr session, pane, and agent name are required')
        receipt = launch(record, args.herdr_session, args.herdr_pane, args.herdr_agent, profile['model'], profile['effort'])
        (out / 'native-first-turn.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({key: record[key] for key in ('prompt_sha256', 'prompt_bytes', 'receipt_kind', 'prompt_path')}))


if __name__ == '__main__':
    main()
