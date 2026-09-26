"""Disposable seats: a light harness started in its own pane and bound in
the sandbox Flow Nexus by MetaBindExisting, as an imported live seat is.

A seat's cwd is chosen so neither harness stops on a trust dialog without
the living having answered it before: Codex seats run in the home directory
the living already trusts, and Claude seats in the run's own work directory,
where the installed claude's skip-permissions flag applies.
"""

import json
import secrets
import time
import uuid

from environment import (CLAUDE_EFFORT, CLAUDE_MODEL, CODEX_EFFORT, CODEX_MODEL, USER_HOME)
from herdr import HerdrError
from processes import ProcessIdentity
from sandbox import CLAUDE_FLAG_SETTINGS


class SeatError(RuntimeError):
    pass


# Every seat is told what it is before any letter reaches it; an unprimed
# recipient takes a datom letter for a prompt injection and refuses it.
SEAT_PRIMER = (
    'This session is a disposable recipient seat in an isolated test of the Flow and '
    'Message delivery system, run by the owner of this machine. Text typed into your '
    'input arrives as a letter: Soft.{ m-<id> <Sender> Text.<body> } (or MiddleAbrupt. '
    'or HardAbrupt. in place of Soft.), where the first token after the brace is the '
    "letter's MessageId and the body is a genuine, authorized request from the test "
    'operator. Carry out what the body asks exactly and briefly, and do nothing else: '
    'run no command a letter does not ask for, and keep every reply to the words the '
    'letter asks for.')


class SeatLauncher:
    # Screens a fresh harness can open on, and the keys that pass each one
    # without changing any saved setting.
    CODEX_SCREENS = (
        ('Hooks need review', ('down', 'down', 'enter')),
        ('Do you trust the contents of this directory', ('enter',)),
    )
    CLAUDE_SCREENS = (
        # The default choice is "No, exit"; the seat directory is the run's own.
        ('Yes, I trust this folder', ('down', 'enter')),
    )

    def __init__(self, sandbox):
        self.sandbox = sandbox
        self.herdr = sandbox.herdr

    def launch(self, name, harness):
        if harness == 'codex':
            cwd = USER_HOME
            arguments = ['-m', CODEX_MODEL, '-c', f'model_reasoning_effort={CODEX_EFFORT}',
                         '-c', f'developer_instructions={json.dumps(SEAT_PRIMER)}',
                         '-a', 'never', '-s', 'read-only']
            screens, model = self.CODEX_SCREENS, CODEX_MODEL
        else:
            cwd = self.sandbox.paths.work
            arguments = ['--model', CLAUDE_MODEL, '--effort', CLAUDE_EFFORT,
                         '--settings', CLAUDE_FLAG_SETTINGS,
                         '--append-system-prompt', SEAT_PRIMER]
            screens, model = self.CLAUDE_SCREENS, CLAUDE_MODEL
        flow_id = secrets.token_hex(3)
        agent_name = f'{name}-{flow_id}'
        place = self.herdr.create_workspace(agent_name, cwd)
        deadline = time.monotonic() + 30
        while True:
            try:
                self.herdr.start_agent(agent_name, harness, place['pane'], arguments)
                break
            except HerdrError as error:
                # A start-up screen holds the agent "blocked"; it is passed below.
                if 'agent_not_ready' in str(error):
                    break
                # A new workspace's shell may not be up yet.
                if 'agent_pane_busy' not in str(error) or time.monotonic() > deadline:
                    raise
                time.sleep(1)
        passed = self._pass_screens(place['pane'], screens)
        pane = self.herdr.pane(place['pane'])
        record = {'name': name, 'flow_id': flow_id, 'harness': harness, 'model': model,
                  'agent_name': agent_name, 'cwd': str(cwd), 'pane': place['pane'],
                  'workspace': place['workspace'], 'terminal': place['terminal'],
                  'tab': pane['tab_id'], 'screens_passed': passed}
        self.sandbox.state['seats'][name] = record
        self.sandbox.save()
        return record

    def _pass_screens(self, pane, screens, timeout_seconds=90):
        """Answers start-up screens until the harness rests at its composer."""
        passed = []
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            visible = self.herdr.read(pane, source='visible', lines=60)
            screen = next((entry for entry in screens
                           if entry[0] in visible and entry[0] not in passed), None)
            if screen:
                self.herdr.send_keys(pane, *screen[1])
                passed.append(screen[0])
                time.sleep(2)
                continue
            status = self.herdr.agent_status(pane)
            if status in ('idle', 'done'):
                return passed
            time.sleep(1)
        raise SeatError(f'seat in {pane} never came to rest; passed {passed}')

    def claim(self, record):
        """Writes the flow-id claim marker Flow checks on every route read.

        The identity is the native session Herdr reports for the pane when it
        reports one (Claude), else a fresh UUID: the marker grammar takes 32
        lower-case hex digits, a Claude one in UUID v4 form."""
        agent = self.herdr.agent(record['pane']) or {}
        session = (agent.get('agent_session') or {}).get('value')
        identity = session.replace('-', '') if session else uuid.uuid4().hex
        record['native_session'] = identity
        marker = self.sandbox.paths.flows_root / f'.{record["flow_id"]}.flow-id'
        marker.write_text(f'version=1\nharness={record["harness"]}\n'
                          f'identity={identity}\nalias={record["flow_id"]}\n')

    def bind(self, names):
        """Binds the named seats in the sandbox Flow Nexus, in one request."""
        server = self.sandbox.state['herdr_server']
        container = (f'{{ {self.sandbox.session} {self.herdr.socket_path()} '
                     f'{{ {server["pid"]} {server["uid"]} {server["start_token"]} }} '
                     f'{self.sandbox.owner_id} }}')
        bindings = []
        for name in names:
            record = self.sandbox.state['seats'][name]
            self.claim(record)
            identity = ProcessIdentity.harness_in_pane(self.sandbox.session, record['pane'],
                                                       record['harness'])
            if identity is None:
                raise SeatError(f'no {record["harness"]} process found in {record["pane"]}')
            record['process'] = {'pid': identity.pid, 'uid': identity.uid,
                                 'start_token': identity.start_token, 'cwd': identity.cwd}
            harness = 'Codex' if record['harness'] == 'codex' else 'Claude'
            bindings.append(
                f'{{ {record["flow_id"]} Field Low {record["model"]} {harness} '
                f'{record["native_session"]} {record["workspace"]} {record["pane"]} '
                f'{record["tab"]} {record["terminal"]} {record["agent_name"]} '
                f'{identity.datom()} {identity.cwd} }}')
        reply = self.sandbox.flow_meta(
            f'MetaBindExisting.{{ {container} [ {" ".join(bindings)} ] }}')
        self.sandbox.state.setdefault('bindings', []).append(reply)
        self.sandbox.save()
        for name in names:
            flow_id = self.sandbox.state['seats'][name]['flow_id']
            if f'Bound.{{ {flow_id} ' not in reply:
                raise SeatError(f'{name} ({flow_id}) was not bound: {reply}')
        return reply
