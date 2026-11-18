"""Private bootstrap capability. Importing this module performs no action.

The caller must establish the reviewed production-before witness and the held
unit startup cut before entering Bootstrap. This module is not a run entrypoint.
"""
import contextlib
import ctypes
import hashlib
import json
import os
import re
from pathlib import Path
import selectors
import shlex
import signal
import stat
import subprocess
import time


class BootstrapError(Exception):
    pass


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def verify_inputs(manifest):
    """Bind each executable and admission record to its exact reviewed bytes."""
    names = ('flow', 'flow_meta', 'flow_daemon', 'flow_hook', 'curriculum',
             'curriculum_daemon', 'place_compiler', 'herdr', 'raw_codex',
             'git', 'tar', 'shell')
    entries = manifest['providers']
    if set(entries) != set(names):
        raise BootstrapError('provider set differs from reviewed bootstrap contract')
    for name in names:
        entry = entries[name]
        path, expected = entry['path'], entry['sha256']
        if not os.path.isabs(path) or len(expected) != 64 or any(c not in '0123456789abcdef' for c in expected):
            raise BootstrapError('invalid provider binding: ' + name)
        if not stat.S_ISREG(os.stat(path).st_mode) or not os.access(path, os.X_OK) or digest(path) != expected:
            raise BootstrapError('provider verification failed: ' + name)
    for name in ('admission',):
        record = manifest[name]
        if not os.path.isabs(record['path']) or digest(record['path']) != record['sha256']:
            raise BootstrapError('record verification failed: ' + name)
    root = manifest['root']
    if not os.path.isabs(root) or os.path.normpath(root) != root or root == '/' or any(c in root for c in '«»\\\n\r'):
        raise BootstrapError('root must be an absolute normalized private path')
    if not re.fullmatch(r'[A-Za-z0-9_-]+', manifest['session']):
        raise BootstrapError('invalid private session')


def check_membership(control_group):
    if not control_group.startswith('/user.slice/') or '..' in control_group.split('/'):
        raise BootstrapError('invalid owned cgroup')
    with open('/proc/self/cgroup', encoding='utf-8') as stream:
        lines = stream.read().splitlines()
    groups = [line[3:] for line in lines if line.startswith('0::')]
    if len(groups) != 1 or not (groups[0] == control_group or groups[0].startswith(control_group + '/')):
        raise BootstrapError('controller is outside owned cgroup')


def private_environment(manifest):
    root = manifest['root']
    return {'HOME': root + '/home', 'USER': manifest['user'], 'LOGNAME': manifest['user'],
            'LANG': 'C.UTF-8', 'PATH': root + '/bin:' + str(Path(manifest['providers']['flow']['path']).parent) + ':' + manifest['host_path'],
            'XDG_CONFIG_HOME': root + '/config', 'XDG_DATA_HOME': root + '/home/.local/share',
            'XDG_STATE_HOME': root + '/home/.local/state', 'XDG_CACHE_HOME': root + '/home/.cache',
            'XDG_RUNTIME_DIR': root + '/runtime', 'CODEX_HOME': root + '/codex',
            'CURRICULUM_CONTEXT_LAYOUT': '2',
            'CURRICULUM_CONTEXT_REFRESH_PROGRAM': root + '/bin/context-refresh',
            'CURRICULUM_PSYCHES_REPOSITORY_DIR': root + '/contexts/psyche-belief',
            'CURRICULUM_MIND_CONTEXT_DIR': root + '/contexts/mind-belief',
            'CURRICULUM_FIELD_CONTEXT_DIR': root + '/contexts/field-belief',
            'CURRICULUM_RECORDS_DIR': root + '/source/flows'}


def _write(path, data, mode=0o600):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        stream.write(data)


def _socket(path):
    try:
        return stat.S_ISSOCK(os.stat(path, follow_symlinks=False).st_mode)
    except FileNotFoundError:
        return False


class Bootstrap:
    """Lifetime owner for private children; service cgroup owns termination.

    finally records unresolved child custody. The caller must complete the
    independently guarded unit stop and terminal/empty cgroup witness.
    """
    def __init__(self, manifest, unit_identity):
        self.manifest = manifest
        self.identity = unit_identity
        self.children = []
        self.old_handlers = {}
        self.entered = False

    def __enter__(self):
        verify_inputs(self.manifest)
        if self.identity['Id'] != self.manifest['unit_name'] or not self.identity.get('InvocationID'):
            raise BootstrapError('unit identity does not match manifest')
        check_membership(self.identity['ControlGroup'])
        def interrupted(signum, frame):
            raise BootstrapError('interrupted by signal ' + str(signum))
        try:
            for sig in (signal.SIGINT, signal.SIGTERM):
                self.old_handlers[sig] = signal.signal(sig, interrupted)
        except BaseException:
            for sig, handler in self.old_handlers.items():
                signal.signal(sig, handler)
            raise
        self.entered = True
        return self

    def __exit__(self, kind, value, traceback):
        try:
            if self.children:
                evidence = Path(self.manifest['root']) / 'evidence'
                if evidence.is_dir():
                    _write(evidence / 'bootstrap-custody.json', json.dumps({
                        'unit': self.identity, 'child_pids_observation_only': [p.pid for p in self.children],
                        'status': 'unit terminal and cgroup reconciliation required'}, sort_keys=True) + '\n')
        finally:
            for sig, handler in self.old_handlers.items():
                signal.signal(sig, handler)
            self.entered = False
        return False

    def _require_owner(self):
        if not self.entered:
            raise BootstrapError('bootstrap lifetime owner is not installed')
        check_membership(self.identity['ControlGroup'])

    def stage(self):
        self._require_owner()
        m = self.manifest
        root = Path(m['root'])
        st = root.lstat()
        if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid() or stat.S_IMODE(st.st_mode) != 0o700:
            raise BootstrapError('staged root is not the owned private directory')
        if set(os.listdir(root)) != {'evidence', 'ready.fifo', 'go.fifo'}:
            raise BootstrapError('staged root contains unexpected entries')
        for part in ('home', 'config/nexus/proposalTwo', 'config/herdr/sessions/' + m['session'],
                     'runtime/nexus/proposalTwo', 'runtime/curriculum', 'runtime/codex',
                     'state', 'codex/sessions', 'source/flows', 'contexts', 'bin', 'evidence'):
            (root / part).mkdir(mode=0o700, parents=True, exist_ok=True)
        _write(root / 'config/nexus/flow-nexus.datom', '{ proposalTwo }\n')
        _write(root / 'place.datom', '{ proposalTwo «%s/runtime/nexus/proposalTwo» «%s/state» }\n' % (root, root))
        providers = m['providers']
        shell = providers['shell']['path']
        for name, body in (('herdr', 'exec ' + shlex.quote(providers['herdr']['path']) + ' "$@"'),
                           ('codex-private', 'export CODEX_HOME=' + shlex.quote(str(root / 'codex')) + '\nexec ' + shlex.quote(providers['raw_codex']['path']) + ' "$@"'),
                           ('context-refresh', 'exit 0')):
            _write(root / 'bin' / name, '#!' + shell + '\n' + body + '\n', 0o700)
        _write(root / 'config/herdr/config.toml', '[agents]\ncodex_executables = [' + json.dumps(str(root / 'bin/codex-private')) + ']\n')
        _write(root / 'codex/config.toml', 'approval_policy = "never"\nsandbox_mode = "danger-full-access"\ncli_auth_credentials_store = "file"\nmodel = "gpt-6-luna"\nmodel_reasoning_effort = "medium"\n')
        return root

    def command(self, name, argv, *, stdin=None, stdout=None, stderr=subprocess.DEVNULL):
        self._require_owner()
        process = subprocess.Popen(argv, env=private_environment(self.manifest), stdin=stdin, stdout=stdout,
                                   stderr=stderr, close_fds=True)
        self.children.append(process)
        return process

    def archive_context(self, name, repository, revision):
        self._require_owner()
        approved = self.manifest['contexts'].get(name)
        if not approved or approved != {'repository': repository, 'revision': revision}:
            raise BootstrapError('context is not manifest-bound')
        if name not in ('psyche-belief', 'mind-belief', 'field-belief') or not os.path.isabs(repository) or not re.fullmatch(r'[0-9a-f]{40}', revision):
            raise BootstrapError('invalid context')
        destination = Path(self.manifest['root']) / 'contexts' / name
        destination.mkdir(mode=0o700)
        git = self.manifest['providers']['git']['path']
        tar = self.manifest['providers']['tar']['path']
        archive = self.command('git-archive', [git, '-C', repository, 'archive', revision], stdout=subprocess.PIPE)
        extract = self.command('tar-extract', [tar, '-x', '-C', str(destination)], stdin=archive.stdout)
        archive.stdout.close()
        _, extract_error = extract.communicate()
        _, archive_error = archive.communicate()
        if extract.returncode or archive.returncode:
            raise BootstrapError('context archive failed: ' + repr((archive_error, extract_error)))
        (destination / '.git').mkdir(mode=0o700)
        _write(destination / '.git/HEAD', revision + '\n')

    def compile_place(self, expect_receipt):
        self._require_owner()
        root = Path(self.manifest['root'])
        target = root / 'config/nexus/proposalTwo/flow-nexus.signal'
        request = 'Compile.{ «%s» «%s» }' % (root / 'place.datom', target)
        process = self.command('place-compile', [self.manifest['providers']['place_compiler']['path'], request], stdout=subprocess.PIPE)
        output, error = process.communicate()
        _write(root / 'evidence/place.input.datom', request + '\n')
        _write(root / 'evidence/place.receipt', output.decode('utf-8'))
        if process.returncode:
            raise BootstrapError('place compiler failed: ' + repr(error))
        expect_receipt(output.decode('utf-8'), 'Compiled.«%s»' % target)

    def start_ready(self, name, argv, paths, timeout):
        """Watch socket-creation events and child pidfd; never timer-poll."""
        self._require_owner()
        if not re.fullmatch(r'[a-z][a-z0-9-]*', name):
            raise BootstrapError('invalid readiness name')
        if not paths or timeout <= 0 or any(not str(p).startswith(self.manifest['root'] + '/') for p in paths):
            raise BootstrapError('invalid readiness paths or deadline')
        libc = ctypes.CDLL(None, use_errno=True)
        fd = libc.inotify_init1(os.O_CLOEXEC | os.O_NONBLOCK)
        if fd < 0:
            raise OSError(ctypes.get_errno(), 'inotify_init1')
        selector = selectors.DefaultSelector()
        pidfd = None
        try:
            for parent in sorted({str(Path(p).parent) for p in paths}):
                if libc.inotify_add_watch(fd, os.fsencode(parent), 0x100 | 0x80 | 0x4) < 0:
                    raise OSError(ctypes.get_errno(), parent)
            if any(os.path.lexists(p) for p in paths):
                raise BootstrapError('readiness path already exists')
            log = Path(self.manifest['root']) / 'evidence' / (name + '.log')
            with open(log, 'xb') as output:
                child = self.command(name, argv, stdout=output, stderr=output)
            pidfd = os.pidfd_open(child.pid)
            selector.register(fd, selectors.EVENT_READ, 'filesystem')
            selector.register(pidfd, selectors.EVENT_READ, 'exit')
            deadline = time.monotonic() + timeout
            while True:
                if all(_socket(p) for p in paths):
                    if any(key.data == 'exit' for key, _ in selector.select(0)):
                        raise BootstrapError(name + ' exited at readiness cut')
                    pid = child.pid
                    proc = Path('/proc') / str(pid)
                    fields = (proc / 'stat').read_text().rsplit(')', 1)[1].split()
                    group = (proc / 'cgroup').read_text().splitlines()
                    expected_group = self.identity['ControlGroup']
                    if len(fields) <= 19 or not any(x == '0::' + expected_group or x.startswith('0::' + expected_group + '/') for x in group):
                        raise BootstrapError(name + ' process outside owned cgroup')
                    observed = {'pid': pid, 'start_ticks': int(fields[19]), 'executable': os.readlink(proc / 'exe'),
                                'cgroup': group, 'sockets': list(map(str, paths))}
                    _write(Path(self.manifest['root']) / 'evidence' / (name + '.ready.json'), json.dumps(observed) + '\n')
                    return child
                events = selector.select(max(0, deadline - time.monotonic()))
                if not events:
                    raise BootstrapError(name + ' readiness deadline expired')
                if any(key.data == 'exit' for key, _ in events):
                    raise BootstrapError(name + ' exited before readiness')
                try:
                    os.read(fd, 65536)
                except BlockingIOError:
                    pass
        finally:
            selector.close()
            if pidfd is not None:
                os.close(pidfd)
            os.close(fd)

    def start_services(self):
        """Start only the four reviewed services, in dependency order."""
        self._require_owner()
        root = self.manifest['root']
        p = self.manifest['providers']
        session = self.manifest['session']
        deadline = self.manifest['startup_timeout_seconds']
        if not isinstance(deadline, (int, float)) or isinstance(deadline, bool) or deadline <= 0:
            raise BootstrapError('invalid startup timeout')
        specs = (
            ('herdr', [p['herdr']['path'], '--session', session, 'server'],
             [root + '/config/herdr/sessions/' + session + '/herdr.sock']),
            ('curriculum', [p['curriculum_daemon']['path']], [root + '/runtime/curriculum/curriculum.sock']),
            ('codex', [p['raw_codex']['path'], 'app-server', '--remote-control', '--listen',
                       'unix://' + root + '/runtime/codex/control.sock'], [root + '/runtime/codex/control.sock']),
            ('flow', [p['flow_daemon']['path'], 'proposalTwo'],
             [root + '/runtime/nexus/proposalTwo/flow.sock', root + '/runtime/nexus/proposalTwo/flow-meta.sock']),
        )
        for name, argv, sockets in specs:
            self.start_ready(name, argv, sockets, deadline)
