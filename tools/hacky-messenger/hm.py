#!/usr/bin/env python3
"""Small, session-aware messaging through Herdr's existing CLI."""
import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys


class Failure(Exception):
    pass


def run(argv):
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise Failure(f'{argv[0]} failed or timed out; submission may be uncertain: {error}') from error
    if result.returncode:
        raise Failure((result.stderr or result.stdout).strip() or f'{argv[0]} failed')
    return result.stdout


def herdr(*args):
    try:
        reply = json.loads(run(['herdr', *args]))
    except ValueError as error:
        raise Failure('Herdr returned invalid JSON; do not blindly retry a send') from error
    if 'error' in reply:
        raise Failure(f"Herdr: {reply['error']}")
    return reply.get('result', reply)


def quote(value):
    return '«' + str(value).replace('\\', '\\\\').replace('»', '\\»') + '»'


# How each harness is hard-abrupted, witnessed live by flow 1ac573 on 2026-09-17
# against a Claude probe pane (interrupt confirmed by the harness's own
# "Interrupted" marker, with a 6000-item task stopping at 4393).
#
# codex:  one Escape interrupts, and `herdr agent prompt` submits by itself.
# claude: the FIRST Escape is eaten by the input editor when Claude's
#         editorMode is vim (it leaves INSERT for NORMAL); only the SECOND
#         reaches the harness as an interrupt. A redundant Escape on an
#         already-idle Claude is harmless. After an interrupt Claude leaves
#         prompted text sitting unsubmitted in the input box, so Enter is what
#         actually delivers it.
# KNOWN LIMITATION, observed in the same live run: the escapes interrupt the
# turn but do NOT clear whatever text is already sitting in the input box, so a
# residual unsubmitted line and the new message are concatenated on one line.
# The recipient still received and answered the message, but the delivered text
# was not clean. Clearing the input before prompting is the next fix here.
ABRUPT_KEYS = {
    'codex': {'interrupt': ('esc',), 'submit': ()},
    'claude': {'interrupt': ('esc', 'esc'), 'submit': ('enter',)},
}


class Messenger:
    def __init__(self, root=None):
        self.root = Path(root or os.environ.get('HM_REGISTRY',
            str(Path.home() / '.local/state/hacky-messenger'))).absolute()

    def path(self, flow):
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,95}', flow):
            raise Failure('Flow ID must contain only letters, digits, underscores, or hyphens')
        return self.root / (flow + '.json')

    @contextmanager
    def reservation(self, flow):
        # One short reservation serializes sends and registration in this registry.
        owner = os.environ.get('FLOW_ID', flow)
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,95}', owner):
            raise Failure('Invalid FLOW_ID')
        reply = run(['orchestrate', f'Lock.{{ HackyMessengerDelivery {owner} [ {quote(self.root)} ] «Register or submit through Herdr» }}'])
        match = re.match(r'Locked\.\{\s+(\d+)\b', reply)
        if not match:
            raise Failure(f'Reservation refused: {reply.strip()}')
        try:
            yield
        finally:
            released = run(['orchestrate', f'Release.{match[1]}'])
            if not released.startswith('Released.'):
                raise Failure(f'Release failed: {released.strip()}')

    def agents(self, session=None):
        sessions = ([{'name': session, 'running': True}] if session else
                    herdr('session', 'list', '--json')['sessions'])
        found = []
        for item in sessions:
            if item['running']:
                for agent in herdr('--session', item['name'], 'agent', 'list')['agents']:
                    found.append(dict(agent, session=item['name']))
        return found

    def readiness_probe(self, agent, marker):
        if not re.fullmatch(r'HM_READY_[A-Za-z0-9_-]{8,96}', marker):
            raise Failure('Readiness probe marker must be a unique HM_READY token')
        prompt = f'Reply exactly {marker} to confirm this explicit HM readiness probe.'
        result = run(['herdr', '--session', agent['session'], 'agent', 'prompt', agent['pane_id'], prompt])
        try:
            reply = json.loads(result)
        except ValueError as error:
            raise Failure('Herdr returned invalid readiness-probe JSON') from error
        error = reply.get('error')
        # Herdr 0.8.2 may return agent_prompt_stalled after injecting a prompt
        # into a resumed Codex terminal. It is usable only with the following
        # target-side read; every other error remains a hard refusal.
        if error and error.get('code') != 'agent_prompt_stalled':
            raise Failure(f'Herdr readiness probe failed: {error}')
        output = run(['herdr', '--session', agent['session'], 'agent', 'read', agent['pane_id'], '--lines', '30'])
        if marker not in output:
            raise Failure('Readiness probe was not observed in the exact target output')

    def register(self, flow, name, session=None, readiness_probe=None):
        path = self.path(flow)
        with self.reservation(flow):
            matches = [a for a in self.agents(session) if a.get('name') == name]
            if len(matches) != 1:
                raise Failure(f'Expected one live agent named {name}; found {len(matches)}. Use --session.')
            agent = matches[0]
            if not agent.get('agent'):
                raise Failure('Agent kind is unavailable')
            if not agent.get('interactive_ready'):
                if not readiness_probe:
                    raise Failure('Agent is not interactively ready')
                self.readiness_probe(agent, readiness_probe)
            record = {k: agent[k] for k in ('session', 'name', 'pane_id', 'terminal_id', 'agent')}
            if readiness_probe:
                record['readiness_probe'] = readiness_probe
            if path.exists() and self.read(flow) != {k: record[k] for k in ('session', 'name', 'pane_id', 'terminal_id', 'agent')}:
                raise Failure('Flow already registered to a different terminal; retire its registry file explicitly')
            self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
            temporary = path.with_suffix('.tmp')
            with temporary.open('w') as stream:
                json.dump(record, stream)
                stream.write('\n')
                stream.flush()
                os.fsync(stream.fileno())
            temporary.replace(path)
        return f'Registered {flow}: {name} ({record["session"]})'

    def read(self, flow):
        try:
            record = json.loads(self.path(flow).read_text())
            for key in ('session', 'name', 'pane_id', 'terminal_id', 'agent'):
                if not isinstance(record[key], str) or not record[key]:
                    raise ValueError(key)
            return record
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise Failure(f'No valid registration for {flow}: {error}') from error

    def deregister(self, flow, session, pane_id, terminal_id, name):
        path = self.path(flow)
        expected = {'session': session, 'pane_id': pane_id, 'terminal_id': terminal_id, 'name': name}
        with self.reservation(flow):
            actual = self.read(flow)
            if any(actual[key] != value for key, value in expected.items()):
                raise Failure('Registration differs from the explicitly revalidated stale route')
            path.unlink()
        return f'Deregistered stale {flow}: {name} ({session}/{pane_id}/{terminal_id})'

    @staticmethod
    def matches(record, agent):
        return all(record[k] == agent.get(k) for k in ('session', 'name', 'pane_id', 'terminal_id', 'agent'))

    def send(self, flow, message, abrupt=False):
        self.path(flow)
        if not message.strip() or any((ord(c) < 32 and c not in '\n\t') or 127 <= ord(c) <= 159 for c in message):
            raise Failure('Message must be nonempty and contain no terminal control characters')
        if len(message.encode()) > 65536:
            raise Failure('Message exceeds 64 KiB')
        if not os.environ.get('FLOW_ID'):
            raise Failure('Set FLOW_ID to your own flow ID before sending')
        with self.reservation(flow):
            record = self.read(flow)
            live = [a for a in self.agents(record['session']) if self.matches(record, a)]
            if len(live) != 1:
                raise Failure('Registration is stale or agent is not ready; nothing sent')
            if not live[0].get('interactive_ready'):
                if 'readiness_probe' not in record:
                    raise Failure('Registration is stale or agent is not ready; nothing sent')
                # A fresh marker prevents a stale terminal transcript from
                # standing in for present readiness on resumed Codex panes.
                self.readiness_probe(live[0], 'HM_READY_SEND_' + secrets.token_hex(16))
            if live[0].get('agent_status') == 'blocked':
                raise Failure('Agent is blocked; nothing sent')
            if abrupt and record['agent'] not in ABRUPT_KEYS:
                raise Failure(f'Hard-abrupt is not supported for {record["agent"]}; nothing sent')
            args = ['--session', record['session'], 'agent']
            # Herdr accepts pane targets; terminal identity was checked above.
            target = record['pane_id']
            if abrupt:
                for key in ABRUPT_KEYS[record['agent']]['interrupt']:
                    herdr(*args, 'send-keys', target, key)
            try:
                if live[0].get('interactive_ready'):
                    herdr(*args, 'prompt', target, message)
                else:
                    response = json.loads(run(['herdr', *args, 'prompt', target, message]))
                    if response.get('error'):
                        raise Failure('Prompt may have been delivered after readiness probe; inspect the exact target before retrying')
                if abrupt:
                    for key in ABRUPT_KEYS[record['agent']]['submit']:
                        herdr(*args, 'send-keys', target, key)
            except (Failure, ValueError) as error:
                prefix = 'Escape was sent; prompt failed or is uncertain' if abrupt else 'Prompt failed or is uncertain'
                raise Failure(f'{prefix}; do not retry automatically: {error}') from error
        return f'Submitted to {flow} via Herdr (not a read receipt)'

    def listing(self):
        records = {}
        for path in sorted(self.root.glob('*.json')):
            records[path.stem] = self.read(path.stem)
        rows = ['FLOW\tAGENT\tSESSION\tSTATE']
        seen = set()
        for agent in self.agents():
            flows = [f for f, r in records.items() if self.matches(r, agent)]
            seen.update(flows)
            rows.append('\t'.join([','.join(flows) or '-', agent.get('name') or '-',
                                   agent['session'], agent['agent_status']]))
        for flow in records.keys() - seen:
            record = records[flow]
            rows.append(f'{flow}\t{record["name"]}\t{record["session"]}\tSTALE')
        return '\n'.join(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='operation', required=True)
    register = sub.add_parser('register')
    register.add_argument('flow')
    register.add_argument('name')
    register.add_argument('--session')
    register.add_argument('--readiness-probe', help='unique HM_READY marker; required only for a Herdr endpoint that omits interactive_ready')
    deregister = sub.add_parser('deregister')
    deregister.add_argument('flow')
    deregister.add_argument('--session', required=True)
    deregister.add_argument('--pane-id', required=True)
    deregister.add_argument('--terminal-id', required=True)
    deregister.add_argument('--name', required=True)
    sub.add_parser('list')
    for name in ('send', 'send-abrupt'):
        send = sub.add_parser(name)
        send.add_argument('flow')
        send.add_argument('message')
    args = parser.parse_args()
    messenger = Messenger()
    try:
        if args.operation == 'register':
            result = messenger.register(args.flow, args.name, args.session, args.readiness_probe)
        elif args.operation == 'deregister':
            result = messenger.deregister(args.flow, args.session, args.pane_id, args.terminal_id, args.name)
        elif args.operation == 'list':
            result = messenger.listing()
        else:
            result = messenger.send(args.flow, args.message, args.operation == 'send-abrupt')
        print(result)
    except (Failure, OSError) as error:
        print(f'hm: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
