"""Where one sandbox run lives, and the environment its processes see.

Nothing here points at a production socket, store or Herdr session. Every
path is derived from the run id: the state tree under
~/.cache/flow-message-sandbox/<run>, the sockets under
/run/user/<uid>/<run> (short enough for SUN_LEN), and a Herdr session named
<run>. The harness logins are reused only by leaving HOME, ~/.claude and
~/.codex where the living keeps them; nothing is copied or read from them
except the harness transcripts, which the target-side checks read.
"""

import json
import os
import pathlib
import secrets
import subprocess

FLOW_REVISION = '908135684f27c4c912b9808e196fb82fe11f4ce6'
MESSAGE_REVISION = '481b579fcf72797ffa9ccf8ce4e2283a58cdff97'
FLOW_VERSION = '0.17.0'
MESSAGE_VERSION = '0.17.0'

CLAUDE_MODEL = 'claude-haiku-4-5-20251001'
CLAUDE_EFFORT = 'low'
CODEX_MODEL = 'gpt-5.6-luna'
CODEX_EFFORT = 'low'

USER_HOME = pathlib.Path.home()
STATE_PARENT = USER_HOME / '.cache' / 'flow-message-sandbox'
HERDR_SESSIONS = USER_HOME / '.config' / 'herdr' / 'sessions'
CLAUDE_HOME = USER_HOME / '.claude'
CODEX_HOME = USER_HOME / '.codex'

# Inherited markers that would bind a sandbox process to the caller's own
# pane, flow, or Claude job. Every sandbox process starts without them.
SCRUBBED_PREFIXES = ('HERDR_', 'FLOW_', 'MESSAGE_', 'CLAUDE', 'CODEX_', 'ORCHESTRATE_')
SCRUBBED_NAMES = ()


class Pins:
    """The two components under test, built from their exact revisions."""

    def __init__(self, flow_store_path, message_store_path):
        self.flow = pathlib.Path(flow_store_path)
        self.message = pathlib.Path(message_store_path)

    @classmethod
    def build(cls, log_directory):
        """Builds both revisions (remote builders do the work) and returns them."""
        paths = []
        for name, revision in (('flow', FLOW_REVISION), ('message', MESSAGE_REVISION)):
            log = pathlib.Path(log_directory) / f'nix-build-{name}.log'
            with open(log, 'w') as handle:
                result = subprocess.run(
                    ['nix', 'build', '--no-link', '--print-out-paths', '-L',
                     f'github:LiGoldragon/{name}/{revision}'],
                    stdout=subprocess.PIPE, stderr=handle, text=True, timeout=5400)
            if result.returncode != 0:
                raise RuntimeError(f'nix build of {name} {revision} failed; see {log}')
            paths.append(result.stdout.strip().splitlines()[-1])
        return cls(*paths)

    def record(self):
        return {'flow': str(self.flow), 'flow_revision': FLOW_REVISION,
                'message': str(self.message), 'message_revision': MESSAGE_REVISION}

    def message_nexus_executable(self):
        return os.path.realpath(self.message / 'bin' / 'message-nexus')


class RunPaths:
    """Every path one run owns."""

    def __init__(self, run_id):
        self.run_id = run_id
        self.root = STATE_PARENT / run_id
        self.runtime = pathlib.Path(f'/run/user/{os.getuid()}') / run_id
        self.flow_home = self.root / 'flow-home'
        self.message_home = self.root / 'message-home'
        # One stable directory is every run's Flow source root and Claude
        # seat cwd, so the Claude trust question is answered once, not per
        # run. A run removes what it added there. One run at a time.
        self.source_root = STATE_PARENT / 'seat'
        self.flows_root = self.source_root / 'flows'
        self.work = self.source_root
        self.bin = self.root / 'bin'
        self.logs = self.root / 'logs'
        self.evidence = self.root / 'evidence'
        self.state_file = self.root / 'state.json'
        self.herdr_session_directory = HERDR_SESSIONS / run_id
        self.flow_socket = self.runtime / 'flow' / 'flow.sock'
        self.flow_meta_socket = self.runtime / 'flow' / 'flow-meta.sock'
        self.message_socket = self.runtime / 'message' / 'message.sock'
        self.message_meta_socket = self.runtime / 'message' / 'message-owner.sock'
        self.codex_socket = self.runtime / 'codex' / 'app-server.sock'

    @staticmethod
    def new_run_id():
        return 'fms-' + secrets.token_hex(3)

    def create(self):
        for directory in (self.flow_home, self.message_home, self.flows_root,
                          self.work, self.bin, self.logs, self.evidence):
            directory.mkdir(parents=True, exist_ok=True)
        self.runtime.mkdir(mode=0o700, parents=False, exist_ok=False)
        (self.runtime / 'codex').mkdir(mode=0o700)

    def load_state(self):
        if self.state_file.exists():
            return json.loads(self.state_file.read_text())
        return {}

    def save_state(self, state):
        self.state_file.write_text(json.dumps(state, indent=1, sort_keys=True))


class Environment:
    """The environment of every process the sandbox starts."""

    def __init__(self, paths, pins):
        self.paths = paths
        self.pins = pins

    @staticmethod
    def scrubbed():
        return {name: value for name, value in os.environ.items()
                if not name.startswith(SCRUBBED_PREFIXES) and name not in SCRUBBED_NAMES}

    def search_path(self):
        return ':'.join([str(self.pins.flow / 'bin'), str(self.pins.message / 'bin'),
                         str(self.paths.bin), str(USER_HOME / '.nix-profile' / 'bin'),
                         '/run/current-system/sw/bin'])

    def clients(self):
        """What a sandbox CLI, a pane, or a recipient's own shell sees."""
        environment = self.scrubbed()
        environment.update({
            'PATH': self.search_path(),
            'FLOW_SOCKET': str(self.paths.flow_socket),
            'FLOW_META_SOCKET': str(self.paths.flow_meta_socket),
            'MESSAGE_SOCKET': str(self.paths.message_socket),
            'MESSAGE_META_SOCKET': str(self.paths.message_meta_socket),
        })
        return environment

    def in_pane(self, session, pane):
        """A client process carrying a pane's Herdr marks: the flow bound there."""
        environment = self.clients()
        environment.update({'HERDR_SESSION': session, 'HERDR_PANE_ID': pane})
        return environment

    def flow_nexus(self):
        environment = self.clients()
        environment.update({
            'HOME': str(self.paths.flow_home),
            'XDG_RUNTIME_DIR': str(self.paths.runtime),
            'XDG_CONFIG_HOME': str(USER_HOME / '.config'),
            'FLOW_SOURCE_ROOT': str(self.paths.source_root),
            'CODEX_HOME': str(CODEX_HOME),
            'CLAUDE_CONFIG_DIR': str(CLAUDE_HOME),
        })
        return environment

    def message_nexus(self):
        environment = self.clients()
        environment.update({
            'HOME': str(self.paths.message_home),
            'XDG_RUNTIME_DIR': str(self.paths.runtime),
        })
        return environment

    def codex_app_server(self):
        environment = self.clients()
        environment['CODEX_HOME'] = str(CODEX_HOME)
        return environment
