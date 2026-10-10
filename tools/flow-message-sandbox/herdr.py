"""The run's own Herdr session: started, driven, observed, and deleted.

The session is started by attaching a detached client under `script`, as a
terminal would; its server inherits the client environment, so every pane
the session opens sees the sandbox sockets and pinned binaries and none of
the caller's Herdr, Flow or Claude markers.
"""

import json
import os
import signal
import subprocess
import time

from environment import HERDR_SESSIONS


class HerdrError(RuntimeError):
    pass


class HerdrSession:
    def __init__(self, name, environment, logs):
        self.name = name
        self.environment = environment
        self.logs = logs
        self.client_pid = None

    # -- lifecycle -------------------------------------------------------

    def start(self):
        typescript = self.logs / 'herdr-client.typescript'
        client = subprocess.Popen(
            ['script', '-qfc', f'stty cols 220 rows 60; herdr session attach {self.name}',
             str(typescript)],
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            env=self.environment, start_new_session=True)
        self.client_pid = client.pid
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            reply = self.call(['pane', 'list'], check=False)
            if reply and 'result' in reply:
                return reply['result']['panes']
            time.sleep(0.5)
        raise HerdrError(f'Herdr session {self.name} never answered')

    def stop(self):
        self.call(['server', 'stop'], check=False)
        if self.client_pid:
            try:
                os.killpg(self.client_pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        subprocess.run(['herdr', 'session', 'delete', self.name], env=self.environment,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def listed(self):
        result = subprocess.run(['herdr', 'session', 'list'], env=self.environment,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return any(line.split()[:1] == [self.name] for line in result.stdout.splitlines())

    # -- calls -----------------------------------------------------------

    def run(self, arguments, timeout=120):
        return subprocess.run(['herdr', '--session', self.name, *arguments],
                              env=self.environment, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True, timeout=timeout)

    def call(self, arguments, check=True, timeout=120):
        result = self.run(arguments, timeout=timeout)
        for stream in (result.stdout, result.stderr):
            try:
                reply = json.loads(stream)
            except ValueError:
                continue
            if check and 'error' in reply:
                raise HerdrError(f'herdr {" ".join(arguments[:3])}: {reply["error"]}')
            return reply
        if check:
            raise HerdrError(f'herdr {" ".join(arguments[:3])}: {result.stderr.strip()}')
        return None

    def socket_path(self):
        return str(HERDR_SESSIONS / self.name / 'herdr.sock')

    # -- panes -----------------------------------------------------------

    def create_workspace(self, label, cwd):
        reply = self.call(['workspace', 'create', '--cwd', str(cwd), '--label', label,
                           '--no-focus'])['result']
        pane = reply['root_pane']
        return {'workspace': reply['workspace']['workspace_id'], 'pane': pane['pane_id'],
                'terminal': pane['terminal_id'], 'tab': pane.get('tab_id')}

    def pane(self, pane_id):
        for pane in self.call(['pane', 'list'])['result']['panes']:
            if pane['pane_id'] == pane_id:
                return pane
        return None

    def agent(self, pane_id):
        reply = self.call(['agent', 'get', pane_id], check=False)
        if not reply or 'result' not in reply:
            return None
        return reply['result']['agent']

    def agent_status(self, pane_id):
        agent = self.agent(pane_id)
        return agent.get('agent_status') if agent else None

    def wait_agent(self, pane_id, states, timeout_seconds):
        arguments = ['agent', 'wait', pane_id]
        for state in states:
            arguments += ['--until', state]
        arguments += ['--timeout', str(int(timeout_seconds * 1000))]
        reply = self.call(arguments, check=False, timeout=timeout_seconds + 30)
        if reply and 'result' in reply:
            return reply['result'].get('agent', {}).get('agent_status')
        return None

    def start_agent(self, name, kind, pane_id, arguments):
        return self.call(['agent', 'start', name, '--kind', kind, '--pane', pane_id,
                          '--timeout', '30000', '--', *arguments], timeout=90)

    def read(self, pane_id, source='recent', lines=400):
        result = self.run(['pane', 'read', pane_id, '--source', source, '--lines', str(lines)])
        return result.stdout

    def send_keys(self, pane_id, *keys):
        return self.run(['pane', 'send-keys', pane_id, *keys])

    def wait_output(self, pane_id, match, timeout_seconds, source='recent', lines=400):
        reply = self.call(['pane', 'wait-output', pane_id, '--match', match, '--source', source,
                           '--lines', str(lines), '--timeout', str(int(timeout_seconds * 1000))],
                          check=False, timeout=timeout_seconds + 30)
        return bool(reply and 'result' in reply)

    def close_pane(self, pane_id):
        return self.run(['pane', 'close', pane_id])

    def snapshot_agents(self):
        reply = self.call(['api', 'snapshot'], check=False)
        if not reply:
            return []
        return reply.get('result', {}).get('snapshot', {}).get('agents', [])
