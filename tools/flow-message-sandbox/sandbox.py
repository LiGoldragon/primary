"""One disposable Flow + Message sandbox: stand it up, seat it, tear it down.

State lives in the run's state.json so a later invocation can run more
scenarios against the same sandbox or tear it down.
"""

import json
import os
import pathlib
import shutil
import subprocess
import time
import tomllib

from environment import (CLAUDE_EFFORT, CLAUDE_MODEL, CODEX_EFFORT, CODEX_HOME, CODEX_MODEL,
                         USER_HOME, Environment, Pins, RunPaths)
from herdr import HerdrSession
from processes import Client, ProcessIdentity, ScopedProcess, process_alive, wait_for_path

CLAUDE_FLAG_SETTINGS = '{"permissions":{"defaultMode":"bypassPermissions"}}'
HARNESS_PROFILES = '[ { Claude [ / «!» # ] [ esc esc ] [ enter ] } { Codex [ / «!» ] [ esc ] [] } ]'


class Seat:
    """A disposable recipient or sender: one harness in one pane of the run."""

    def __init__(self, record):
        self.record = record

    def __getattr__(self, name):
        try:
            return self.record[name]
        except KeyError as error:
            raise AttributeError(name) from error


class Sandbox:
    def __init__(self, paths, pins, state=None):
        self.paths = paths
        self.pins = pins
        self.environment = Environment(paths, pins)
        self.state = state or {'run_id': paths.run_id, 'pins': pins.record(), 'seats': {},
                               'processes': {}, 'units': []}
        self.herdr = HerdrSession(paths.run_id, self.environment.clients(), paths.logs)
        self.herdr.client_pid = self.state.get('herdr_client_pid')
        self.client = Client(self.environment.clients())

    # -- persistence -----------------------------------------------------

    @classmethod
    def resume(cls, run_id):
        paths = RunPaths(run_id)
        state = paths.load_state()
        pins = Pins(state['pins']['flow'], state['pins']['message'])
        return cls(paths, pins, state)

    def save(self):
        self.paths.save_state(self.state)

    @property
    def session(self):
        return self.paths.run_id

    @property
    def owner_id(self):
        return self.paths.run_id.split('-')[-1]

    def seat(self, name):
        return Seat(self.state['seats'][name])

    # -- long-lived processes --------------------------------------------

    def _process(self, key):
        record = self.state['processes'].get(key)
        if not record:
            return None
        return ScopedProcess(record['unit'], [], {}, None, pid=record['pid'])

    def _start(self, key, arguments, environment, socket=None):
        count = sum(1 for unit in self.state['units'] if unit.startswith(f'{self.session}-{key}'))
        unit = f'{self.session}-{key}-{count}'
        process = ScopedProcess(unit, arguments, environment, self.paths.logs / f'{key}.log')
        pid = process.start()
        self.state['processes'][key] = {'unit': unit, 'pid': pid}
        self.state['units'].append(unit)
        self.save()
        if socket and not wait_for_path(socket, 30):
            raise RuntimeError(f'{key} never opened {socket}; see {self.paths.logs}/{key}.log')
        return process

    def stop_process(self, key):
        process = self._process(key)
        if process:
            process.stop()
            self.state['processes'].pop(key)
            self.save()

    def start_flow_nexus(self):
        return self._start('flow', [str(self.pins.flow / 'bin' / 'flow-nexus')],
                           self.environment.flow_nexus(), self.paths.flow_meta_socket)

    def start_message_nexus(self):
        return self._start('message', [str(self.pins.message / 'bin' / 'message-nexus')],
                           self.environment.message_nexus(), self.paths.message_meta_socket)

    def restart_message_nexus(self):
        self.stop_process('message')
        for socket in (self.paths.message_socket, self.paths.message_meta_socket):
            if socket.exists():
                socket.unlink()
        return self.start_message_nexus()

    def start_codex_app_server(self):
        running = self._process('codex')
        if running and running.running():
            return running
        return self._start('codex', [str(USER_HOME / '.nix-profile' / 'bin' / 'codex'),
                                     'app-server', '--listen', f'unix://{self.paths.codex_socket}'],
                           self.environment.codex_app_server(), self.paths.codex_socket)

    # -- clients ---------------------------------------------------------

    def flow(self, datom, **keywords):
        return self.client.call('flow', datom, **keywords)

    def flow_meta(self, datom, **keywords):
        return self.client.call('flow-meta', datom, **keywords)

    def message(self, datom, sender=None, **keywords):
        environment = self.environment.in_pane(self.session, self.seat(sender).pane) if sender else None
        return self.client.call('message', datom, environment=environment, **keywords)

    def message_meta(self, datom, **keywords):
        return self.client.call('message-meta', datom, **keywords)

    def spawn_message(self, datom, sender=None):
        environment = self.environment.in_pane(self.session, self.seat(sender).pane) if sender else None
        return self.client.spawn('message', datom, environment=environment)

    # -- stand up --------------------------------------------------------

    @staticmethod
    def herdr_codex_client():
        """The Codex client Herdr lets `agent start --executable` run: Herdr
        refuses any executable its own config does not list for the kind.
        The stable Flow client only sets CODEX_HOME and execs codex; the
        launch's --remote names the run's private app-server."""
        config = tomllib.loads((USER_HOME / '.config' / 'herdr' / 'config.toml').read_text())
        clients = config.get('agents', {}).get('codex_executables', [])
        stable = [client for client in clients if 'stable' in client]
        if not stable:
            raise RuntimeError('Herdr config lists no stable Codex client')
        return stable[0]

    def configure_flow(self):
        runtime = self.paths
        client = self.herdr_codex_client()
        absent = self.paths.root / 'absent'
        datom = ' '.join([
            'Configure.{', str(runtime.flow_socket), str(runtime.flow_meta_socket),
            str(runtime.source_root),
            f'{{ {client} {CODEX_HOME} {runtime.codex_socket} [ {CODEX_MODEL} ] }}',
            f'{{ {absent}/codex-next-client {absent}/codex-next {absent}/next.sock [] }}',
            HARNESS_PROFILES, '[ Psyche ]', self.pins.message_nexus_executable(), '}'])
        reply = self.flow_meta(datom)
        self.state['flow_configured'] = reply
        self.save()
        if not reply.startswith('Configured.'):
            raise RuntimeError(f'Flow refused its configuration: {reply}')
        return reply

    def up(self):
        self.paths.create()
        self.state['started_at'] = time.time()
        self.state['flows_root_before'] = sorted(os.listdir(self.paths.flows_root))
        self.state['herdr_sessions_before'] = self.herdr_sessions()
        self.save()
        self.herdr.start()
        self.state['herdr_client_pid'] = self.herdr.client_pid
        server = ProcessIdentity.herdr_server(self.session)
        self.state['herdr_server'] = {'pid': server.pid, 'uid': server.uid,
                                      'start_token': server.start_token}
        self.save()
        self.start_flow_nexus()
        self.configure_flow()
        # Configure answers NexusRestartRequired: the Nexus reads it on open.
        self.stop_process('flow')
        for socket in (self.paths.flow_socket, self.paths.flow_meta_socket):
            if socket.exists():
                socket.unlink()
        self.start_flow_nexus()
        self.start_message_nexus()

    def herdr_sessions(self):
        result = subprocess.run(['herdr', 'session', 'list'], env=self.environment.clients(),
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return sorted(line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip())

    # -- tear down -------------------------------------------------------

    def down(self, purge=False):
        """Stops everything this run started, by PID and by its own session."""
        for key in ('message', 'flow', 'codex'):
            self.stop_process(key)
        # Any earlier scope of this run (a restarted Nexus, a second
        # app-server) is stopped by its own run-unique unit name.
        for unit in self.state['units']:
            if ScopedProcess.unit_active(unit):
                ScopedProcess(unit, [], {}, None).stop()
        self.herdr.stop()
        leftovers = ProcessIdentity.in_session(self.session)
        for pid in leftovers:
            try:
                os.kill(pid, 15)
            except ProcessLookupError:
                pass
        if self.paths.runtime.exists():
            shutil.rmtree(self.paths.runtime)
        # Seat claim markers, and whatever Flow Start's flow-id claims wrote.
        for entry in self.flows_root_added():
            path = self.paths.flows_root / entry
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
        for written in self.state.get('start_files', []):
            if os.path.exists(written):
                os.unlink(written)
        for directory in (self.paths.flow_home, self.paths.message_home, self.paths.bin):
            if directory.exists():
                shutil.rmtree(directory)
        if purge and self.paths.root.exists():
            shutil.rmtree(self.paths.root)
        return self.verify_clean(leftovers)

    def flows_root_added(self):
        if not self.paths.flows_root.exists():
            return []
        before = set(self.state.get('flows_root_before', []))
        return sorted(set(os.listdir(self.paths.flows_root)) - before)

    def verify_clean(self, killed_leftovers=()):
        """What the run leaves behind, checked rather than assumed."""
        time.sleep(1)
        checks = {
            'no process carries the run session mark':
                not [pid for pid in ProcessIdentity.in_session(self.session) if process_alive(pid)],
            'no sandbox scope unit is active':
                not [unit for unit in self.state['units'] if ScopedProcess.unit_active(unit)],
            'no sandbox Nexus or app-server PID is alive':
                not [record for record in self.state['processes'].values()
                     if process_alive(record['pid'])],
            'Herdr no longer lists the run session': not self.herdr.listed(),
            'the run Herdr session directory is gone':
                not self.paths.herdr_session_directory.exists(),
            'the run socket directory is gone': not self.paths.runtime.exists(),
            'the run stores and homes are gone':
                not self.paths.flow_home.exists() and not self.paths.message_home.exists(),
            'the flows root holds only what it held before the run': not self.flows_root_added(),
            'every Herdr session present before the run is still present':
                set(self.state.get('herdr_sessions_before', [])) <= set(self.herdr_sessions()),
        }
        result = {'clean': all(checks.values()), 'checks': checks,
                  'leftover_session_processes_stopped': list(killed_leftovers)}
        if self.paths.root.exists():
            self.state['teardown'] = result
            self.save()
        return result
