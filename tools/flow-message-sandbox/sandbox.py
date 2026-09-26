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

    def configure_flow(self):
        runtime = self.paths
        client = self.paths.bin / 'codex-sandbox-client'
        client.write_text('#!/bin/sh\n'
                          f'export CODEX_HOME={CODEX_HOME}\n'
                          f'exec {USER_HOME}/.nix-profile/bin/codex "$@"\n')
        client.chmod(0o755)
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
        self.start_codex_app_server()

    def herdr_sessions(self):
        result = subprocess.run(['herdr', 'session', 'list'], env=self.environment.clients(),
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return sorted(line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip())
