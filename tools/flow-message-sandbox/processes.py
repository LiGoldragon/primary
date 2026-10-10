"""The run's long-lived processes and the process facts a binding names.

Each Nexus and the private Codex app-server runs in its own transient user
scope with a memory cap, started from this run and stopped by the PID this
run holds, never by a name pattern: a production Nexus shares the pattern.
"""

import os
import pathlib
import queue
import signal
import subprocess
import threading
import time


class ProcessIdentity:
    """A process as Flow names it: pid, uid, and kernel start time."""

    def __init__(self, pid):
        self.pid = int(pid)
        stat = pathlib.Path(f'/proc/{self.pid}/stat').read_text()
        fields = stat[stat.rindex(')') + 2:].split()
        self.start_token = fields[19]
        self.uid = pathlib.Path(f'/proc/{self.pid}').stat().st_uid
        self.cwd = os.readlink(f'/proc/{self.pid}/cwd')

    def datom(self):
        return f'{{ {self.pid} {self.uid} {self.start_token} }}'

    @staticmethod
    def environ(pid):
        try:
            raw = pathlib.Path(f'/proc/{pid}/environ').read_bytes()
        except OSError:
            return {}
        pairs = (item.split(b'=', 1) for item in raw.split(b'\0') if b'=' in item)
        return {key.decode(errors='replace'): value.decode(errors='replace') for key, value in pairs}

    @staticmethod
    def executable(pid):
        try:
            return os.readlink(f'/proc/{pid}/exe')
        except OSError:
            return ''

    @classmethod
    def all_pids(cls):
        return [int(entry) for entry in os.listdir('/proc') if entry.isdigit()]

    @classmethod
    def harness_in_pane(cls, session, pane, harness):
        """The oldest process of the harness running in the pane."""
        found = []
        for pid in cls.all_pids():
            environment = cls.environ(pid)
            if environment.get('HERDR_SESSION') != session or environment.get('HERDR_PANE_ID') != pane:
                continue
            if harness not in os.path.basename(cls.executable(pid)):
                continue
            try:
                found.append(cls(pid))
            except OSError:
                continue
        if not found:
            return None
        return min(found, key=lambda identity: int(identity.start_token))

    @classmethod
    def herdr_server(cls, session):
        """The Herdr server of the session: the herdr process that carries the
        session mark but belongs to no pane."""
        for pid in cls.all_pids():
            environment = cls.environ(pid)
            if environment.get('HERDR_SESSION') != session or 'HERDR_PANE_ID' in environment:
                continue
            if os.path.basename(cls.executable(pid)) == 'herdr':
                return cls(pid)
        return None

    @classmethod
    def in_session(cls, session):
        return [pid for pid in cls.all_pids()
                if cls.environ(pid).get('HERDR_SESSION') == session]


class ScopedProcess:
    """One long-lived process of the run, in its own capped user scope.

    Held by PID, so a later invocation of the suite can stop what an earlier
    one started."""

    def __init__(self, unit, arguments, environment, log_path, memory='1G', pid=None):
        self.unit = unit
        self.arguments = arguments
        self.environment = environment
        self.log_path = log_path
        self.memory = memory
        self.pid = pid
        self.process = None

    def start(self):
        log = open(self.log_path, 'a')
        # The Nexus's own XDG_RUNTIME_DIR is the run's; systemd-run reaches
        # the user manager through the real one, then `env` hands the run's
        # to the Nexus in the same process (every step execs).
        real_runtime = f'/run/user/{os.getuid()}'
        environment = dict(self.environment)
        own_runtime = environment.get('XDG_RUNTIME_DIR', real_runtime)
        environment['XDG_RUNTIME_DIR'] = real_runtime
        self.process = subprocess.Popen(
            ['systemd-run', '--user', '--scope', '--quiet', f'--unit={self.unit}',
             '-p', f'MemoryMax={self.memory}', '--',
             'env', f'XDG_RUNTIME_DIR={own_runtime}', *self.arguments],
            env=environment, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
            start_new_session=True)
        self.pid = self.process.pid
        return self.pid

    def running(self):
        if self.process is not None:
            return self.process.poll() is None
        return process_alive(self.pid)

    def stop(self):
        """Ends the process by its PID, then anything it left in its own scope
        (the unit name is this run's alone)."""
        if self.pid and self.running():
            os.kill(self.pid, signal.SIGTERM)
            if not self._ended(15):
                os.kill(self.pid, signal.SIGKILL)
                self._ended(15)
        if self.unit_active(self.unit):
            subprocess.run(['systemctl', '--user', 'stop', f'{self.unit}.scope'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _ended(self, timeout_seconds):
        if self.process is not None:
            try:
                self.process.wait(timeout=timeout_seconds)
                return True
            except subprocess.TimeoutExpired:
                return False
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            if not process_alive(self.pid):
                return True
            time.sleep(0.2)
        return False

    @staticmethod
    def unit_active(unit):
        result = subprocess.run(['systemctl', '--user', 'is-active', f'{unit}.scope'],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        return result.stdout.strip() in ('active', 'activating', 'deactivating')


def process_alive(pid):
    """Alive and not a zombie."""
    try:
        stat = pathlib.Path(f'/proc/{pid}/stat').read_text()
    except OSError:
        return False
    return stat[stat.rindex(')') + 2] != 'Z'


def wait_for_path(path, timeout_seconds):
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        if pathlib.Path(path).exists():
            return True
        time.sleep(0.1)
    return False


class Client:
    """One sandbox CLI call: exactly one inline datom, as every Nexus CLI takes."""

    def __init__(self, environment):
        self.environment = environment

    def call(self, executable, datom, environment=None, timeout=120):
        result = subprocess.run([executable, datom], env=environment or self.environment,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                timeout=timeout)
        return result.stdout.strip()

    def spawn(self, executable, datom, environment=None):
        return subprocess.Popen([executable, datom], env=environment or self.environment,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


class Stream:
    """A subscription (Observe) read line by line until a wanted line or a bound."""

    def __init__(self, process):
        self.process = process
        self.lines = []
        self._queue = queue.Queue()
        threading.Thread(target=self._pump, daemon=True).start()

    def _pump(self):
        for line in self.process.stdout:
            self._queue.put(line.rstrip('\n'))
        self._queue.put(None)

    def until(self, predicate, timeout_seconds):
        deadline = time.monotonic() + timeout_seconds
        for line in self.lines:
            if predicate(line):
                return line
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None
            try:
                line = self._queue.get(timeout=remaining)
            except queue.Empty:
                return None
            if line is None:
                return None
            self.lines.append(line)
            if predicate(line):
                return line

    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
