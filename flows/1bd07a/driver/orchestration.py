"""Reviewed-operator building blocks; no public command entrypoint.

External admission and an independently validated manifest are prerequisites.
The caller holds the terminal systemd-run handle and resource custody throughout.
"""
import json
import os
from pathlib import Path
import re
import secrets
import threading
import ctypes
import selectors
import signal
import stat
import subprocess
import time

import bootstrap


class CustodyError(Exception):
    pass


def write_once(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(data)


def retain_evidence(root, destination):
    """Copy bounded evidence and transcript files into a fresh outside directory."""
    root, destination = Path(root), Path(destination)
    if not root.is_absolute() or not destination.is_absolute():
        raise CustodyError('retention paths must be absolute')
    root_real = os.path.realpath(root, strict=True)
    parent_real = os.path.realpath(destination.parent, strict=True)
    target = os.path.join(parent_real, destination.name)
    if os.path.commonpath((root_real, target)) == root_real:
        raise CustodyError('retention directory must be outside workload root')
    os.mkdir(target, 0o700)
    for name in ('evidence', 'transcripts'):
        source = root / name
        if not source.exists():
            if name == 'evidence':
                raise CustodyError('evidence directory unavailable')
            continue
        st = source.lstat()
        if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.getuid():
            raise CustodyError('invalid retention source')
        for directory, dirs, files in os.walk(source, followlinks=False):
            relative = Path(directory).relative_to(root)
            output_dir = Path(target) / relative
            output_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
            for child in dirs:
                info = (Path(directory) / child).lstat()
                if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid():
                    raise CustodyError('unsafe directory in evidence')
            for child in files:
                path = Path(directory) / child
                info = path.lstat()
                if stat.S_ISFIFO(info.st_mode):
                    continue
                if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or info.st_nlink != 1:
                    raise CustodyError('unsafe file in evidence')
                fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC)
                try:
                    observed = os.fstat(fd)
                    if (observed.st_dev, observed.st_ino) != (info.st_dev, info.st_ino):
                        raise CustodyError('evidence changed during retention')
                    output = os.open(output_dir / child, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
                    try:
                        while True:
                            data = os.read(fd, 1048576)
                            if not data:
                                break
                            view = memoryview(data)
                            while view:
                                view = view[os.write(output, view):]
                    finally:
                        os.close(output)
                finally:
                    os.close(fd)
    return target


def provider(manifest, name):
    entry = manifest['operator_providers'][name]
    path, expected = entry['path'], entry['sha256']
    if not os.path.isabs(path) or not re.fullmatch('[0-9a-f]{64}', expected):
        raise CustodyError('invalid provider binding: ' + name)
    if not stat.S_ISREG(os.stat(path).st_mode) or not os.access(path, os.X_OK) or bootstrap.digest(path) != expected:
        raise CustodyError('provider differs from manifest: ' + name)
    return path


def parse_show(data):
    result = {}
    for line in data.decode('utf-8').splitlines():
        if '=' not in line:
            raise CustodyError('malformed systemd property')
        key, value = line.split('=', 1)
        if key in result:
            raise CustodyError('duplicate systemd property')
        result[key] = value
    return result


def unit_show(manifest):
    keys = ('Id', 'InvocationID', 'ControlGroup', 'MainPID',
            'ExecMainStartTimestampMonotonic', 'ExecStart')
    command = [provider(manifest, 'systemctl'), '--user', 'show', manifest['unit_name']]
    command += ['--property=' + key for key in keys]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            env=manifest['operator_environment'], check=True)
    values = parse_show(result.stdout)
    if set(values) != set(keys) or any(not values[key] for key in keys):
        raise CustodyError('incomplete unit identity')
    return values


def start_ticks(pid):
    # comm can contain spaces and parentheses; the final ')' ends field 2.
    data = Path('/proc/%d/stat' % pid).read_text()
    end = data.rfind(')')
    fields = data[end + 2:].split() if end >= 0 else []
    if len(fields) <= 19 or not fields[19].isdigit():
        raise CustodyError('process start ticks unavailable')
    return int(fields[19])


def cgroup_path(control_group):
    if not control_group.startswith('/user.slice/') or '..' in control_group.split('/'):
        raise CustodyError('invalid owned control group')
    return Path('/sys/fs/cgroup' + control_group)


def cgroup_identity(control_group):
    path = cgroup_path(control_group)
    st = path.stat(follow_symlinks=False)
    if not stat.S_ISDIR(st.st_mode):
        raise CustodyError('cgroup is not a directory')
    return {'device': st.st_dev, 'inode': st.st_ino,
            'events': (path / 'cgroup.events').read_text()}


def cgroup_empty(saved):
    path = cgroup_path(saved['unit']['ControlGroup'])
    try:
        st = path.stat(follow_symlinks=False)
    except FileNotFoundError:
        return {'state': 'absent'}
    if not stat.S_ISDIR(st.st_mode) or (st.st_dev, st.st_ino) != (saved['cgroup']['device'], saved['cgroup']['inode']):
        raise CustodyError('cgroup inode changed; retain custody')
    events = (path / 'cgroup.events').read_text()
    fields = dict(line.split() for line in events.splitlines())
    if fields.get('populated') != '0':
        raise CustodyError('cgroup populated or unobserved; retain custody')
    return {'state': 'empty', 'events': events, 'device': st.st_dev, 'inode': st.st_ino}


def compare_unit(saved, current):
    keys = ('Id', 'InvocationID', 'ControlGroup', 'MainPID',
            'ExecMainStartTimestampMonotonic', 'ExecStart')
    if any(not saved.get(key) or saved.get(key) != current.get(key) for key in keys):
        raise CustodyError('unit identity changed; retain custody')


def production_capture(manifest, side):
    """Capture whole typed responses, service properties and resolved wrappers."""
    if side not in ('before', 'after'):
        raise CustodyError('invalid witness side')
    evidence = Path(manifest['root']) / 'evidence'
    production = manifest['production']
    env = production['environment']
    flow = provider(manifest, 'production_flow')
    meta = provider(manifest, 'production_meta')
    systemctl = provider(manifest, 'systemctl')
    commands = {
        'configuration.datom': [meta, 'Configuration'],
        'fable-current.datom': [flow, 'Current.{ Psyche core Fable }'],
        'services': [systemctl, '--user', 'show', *production['units'],
                     '-p', 'Id', '-p', 'MainPID', '-p', 'ExecMainStartTimestampMonotonic',
                     '-p', 'ExecStart', '-p', 'FragmentPath', '-p', 'ActiveState', '-p', 'SubState'],
    }
    for name, command in commands.items():
        result = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        write_once(evidence / ('production-' + side + '.' + name), result.stdout)
        write_once(evidence / ('production-' + side + '.' + name + '.stderr'), result.stderr)
        if result.returncode:
            raise CustodyError('production witness command failed: ' + name)
        if name == 'configuration.datom' and not result.stdout.strip().startswith(b'Configuration.'):
            raise CustodyError('production Configuration unavailable')
        if name == 'fable-current.datom' and not result.stdout.strip().startswith(b'Current.'):
            raise CustodyError('production Fable Current unavailable')
    wrappers = production['wrappers']
    if set(wrappers) != {'flow', 'flow-meta', 'flow-hook'}:
        raise CustodyError('incomplete production wrapper witness')
    lines = []
    for name in sorted(wrappers):
        target = os.path.realpath(wrappers[name], strict=True)
        lines.append(name + ' ' + target + '\n')
    write_once(evidence / ('production-' + side + '.clients'), ''.join(lines).encode())


def production_compare(root):
    from controller import production_compare as compare, AdmissionError
    evidence = Path(root) / 'evidence'
    parts = ('configuration.datom', 'fable-current.datom', 'services', 'clients')
    before = {part: (evidence / ('production-before.' + part)).read_bytes() for part in parts}
    after = {part: (evidence / ('production-after.' + part)).read_bytes() for part in parts}
    try:
        compare(before, after)
    except AdmissionError as error:
        raise CustodyError(str(error)) from error



def read_fifo(fd, deadline, abort_fds=()):
    selector = selectors.DefaultSelector()
    selector.register(fd, selectors.EVENT_READ, 'fifo')
    try:
        for abort_fd in abort_fds:
            selector.register(abort_fd, selectors.EVENT_READ, 'abort')
        events = selector.select(max(0, deadline - time.monotonic()))
        if not events:
            raise CustodyError('startup handshake deadline expired')
        if any(key.data == 'abort' for key, _ in events):
            raise CustodyError('startup peer or forwarding failure')
        data = os.read(fd, 65536)
        if not data.endswith(b'\n') or b'\n' in data[:-1]:
            raise CustodyError('malformed handshake')
        return json.loads(data)
    finally:
        selector.close()


def auth_link(manifest):
    """Link the sole approved target; inspect metadata only, never its bytes."""
    root, target = Path(manifest['root']), manifest['auth_target']
    if not os.path.isabs(target):
        raise CustodyError('auth target must be absolute')
    st = os.stat(target, follow_symlinks=False)
    if not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid():
        raise CustodyError('auth target must be an owned regular file')
    metadata = {'uid': st.st_uid, 'mode': stat.S_IMODE(st.st_mode), 'device': st.st_dev,
                'inode': st.st_ino, 'size': st.st_size, 'mtime_ns': st.st_mtime_ns}
    write_once(root / 'evidence/auth-target-before.json', (json.dumps(metadata) + '\n').encode())
    link = root / 'codex/auth.json'
    os.symlink(target, link)
    lst = link.lstat()
    write_once(root / 'evidence/auth-link.json', (json.dumps({'target': os.readlink(link),
               'uid': lst.st_uid, 'inode': lst.st_ino, 'device': lst.st_dev}) + '\n').encode())


def before_digest(root):
    import hashlib
    h = hashlib.sha256()
    for part in ('configuration.datom', 'fable-current.datom', 'services', 'clients'):
        data = (Path(root) / 'evidence' / ('production-before.' + part)).read_bytes()
        h.update(len(data).to_bytes(8, 'big'))
        h.update(data)
    return h.hexdigest()


def unlink_auth_after_terminal(manifest):
    root = Path(manifest['root'])
    evidence = root / 'evidence'
    link = root / 'codex/auth.json'
    if not os.path.lexists(link):
        return
    record = json.loads((evidence / 'auth-link.json').read_text())
    st = link.lstat()
    if not stat.S_ISLNK(st.st_mode) or (st.st_dev, st.st_ino) != (record['device'], record['inode']) or os.readlink(link) != manifest['auth_target']:
        raise CustodyError('auth link identity changed; retain custody')
    link.unlink()
    target = os.stat(manifest['auth_target'], follow_symlinks=False)
    metadata = {'uid': target.st_uid, 'mode': stat.S_IMODE(target.st_mode), 'device': target.st_dev,
                'inode': target.st_ino, 'regular': stat.S_ISREG(target.st_mode),
                'size': target.st_size, 'mtime_ns': target.st_mtime_ns}
    write_once(evidence / 'auth-target-after.json', (json.dumps(metadata) + '\n').encode())


def in_unit(manifest, workload, envelope_path, envelope_hash):
    """Called by the reviewed service entrypoint, not enabled as a CLI."""
    deadline = time.monotonic() + 1200
    root = Path(manifest['root'])
    envelope_bytes = Path(envelope_path).read_bytes()
    if bootstrap.hashlib.sha256(envelope_bytes).hexdigest() != envelope_hash:
        raise CustodyError('startup envelope hash mismatch')
    envelope = json.loads(envelope_bytes)
    if set(envelope) != {'pid', 'uid', 'start_ticks', 'nonce'} or envelope['uid'] != os.getuid():
        raise CustodyError('invalid outer operator envelope')
    proc = Path('/proc') / str(envelope['pid'])
    before = proc.stat().st_uid
    if before != envelope['uid'] or start_ticks(envelope['pid']) != envelope['start_ticks']:
        raise CustodyError('outer operator identity mismatch')
    peer_fd = os.pidfd_open(envelope['pid'])
    if proc.stat().st_uid != before or start_ticks(envelope['pid']) != envelope['start_ticks']:
        os.close(peer_fd)
        raise CustodyError('outer operator changed during pidfd open')
    ready = os.open(root / 'ready.fifo', os.O_WRONLY)
    go = os.open(root / 'go.fifo', os.O_RDONLY | os.O_NONBLOCK)
    try:
        os.write(ready, (json.dumps({'pid': os.getpid(), 'start_ticks': start_ticks(os.getpid()),
                                     'invocation_id': os.environ.get('INVOCATION_ID')}) + '\n').encode())
        saved = read_fifo(go, time.monotonic() + manifest['handshake_timeout_seconds'], (peer_fd,))
        identity = saved['unit']
        if before_digest(root) != saved['production_before_sha256']:
            raise CustodyError('production-before handshake mismatch')
        if identity['Id'] != manifest['unit_name'] or identity['InvocationID'] != os.environ.get('INVOCATION_ID') or int(identity['MainPID']) != os.getpid() or saved['start_ticks'] != start_ticks(os.getpid()):
            raise CustodyError('go identity mismatch')
        bootstrap.check_membership(identity['ControlGroup'])
        if cgroup_identity(identity['ControlGroup'])['inode'] != saved['cgroup']['inode']:
            raise CustodyError('go cgroup inode mismatch')
        with bootstrap.Bootstrap(manifest, identity) as owner:
            workload(owner, peer_fd, envelope['nonce'], deadline)
    finally:
        os.close(peer_fd)
        os.close(ready)
        os.close(go)


def guarded_stop(manifest, saved):
    current = unit_show(manifest)
    compare_unit(saved['unit'], current)
    observed = cgroup_identity(current['ControlGroup'])
    if (observed['device'], observed['inode']) != (saved['cgroup']['device'], saved['cgroup']['inode']):
        raise CustodyError('cgroup inode changed before stop')
    result = subprocess.run([provider(manifest, 'systemctl'), '--user', 'stop', '--job-mode=fail', saved['unit']['Id']],
                            env=manifest['operator_environment'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            timeout=manifest['control_timeout_seconds'])
    if result.returncode:
        raise CustodyError('unit stop failed: ' + result.stderr.decode('utf-8', errors='replace'))
    return result.stdout


def _wait_process(process, deadline, failure_fd=None):
    fd = os.pidfd_open(process.pid)
    selector = selectors.DefaultSelector()
    try:
        selector.register(fd, selectors.EVENT_READ)
        if failure_fd is not None:
            selector.register(failure_fd, selectors.EVENT_READ)
        events = selector.select(max(0, deadline - time.monotonic()))
        if not events:
            raise CustodyError('unit terminal event not observed')
        if failure_fd is not None and any(key.fd == failure_fd for key, _ in events):
            raise CustodyError('operator forwarding failed: ' + os.read(failure_fd, 4096).decode('utf-8', 'replace'))
        return process.wait()
    finally:
        selector.close()
        os.close(fd)


def operator(manifest, manifest_path, expected_manifest_digest):
    """Run only from a later reviewed entrypoint after explicit admission.

    No retry. Any uncertain unit identity is retained and never name-killed.
    """
    if bootstrap.digest(manifest_path) != expected_manifest_digest:
        raise CustodyError('manifest bytes changed')
    if json.loads(Path(manifest_path).read_text()) != manifest:
        raise CustodyError('manifest object and bytes differ')
    bootstrap.verify_inputs(manifest)
    for name in ('systemd_run', 'systemctl', 'python', 'production_flow', 'production_meta'):
        provider(manifest, name)
    driver = manifest['driver']
    if not os.path.isabs(driver['path']) or bootstrap.digest(driver['path']) != driver['sha256']:
        raise CustodyError('immutable driver mismatch')
    if not re.fullmatch(r'proposal2-[A-Za-z0-9_.-]+\.service', manifest['unit_name']):
        raise CustodyError('invalid private unit')
    wrappers = {os.path.realpath(p) for p in manifest['production']['wrappers'].values()}
    for directory in manifest['host_path'].split(os.pathsep):
        if not os.path.isabs(directory):
            raise CustodyError('private PATH contains a nonabsolute component')
        for name in ('flow', 'flow-meta', 'flow-hook'):
            candidate = os.path.join(directory, name)
            if os.path.exists(candidate) and os.path.realpath(candidate) in wrappers:
                raise CustodyError('private PATH exposes a production wrapper')
    root = Path(manifest['root'])
    root.mkdir(mode=0o700, parents=False, exist_ok=False)
    (root / 'evidence').mkdir(mode=0o700)
    envelope = {'pid': os.getpid(), 'uid': os.getuid(), 'start_ticks': start_ticks(os.getpid()),
                'nonce': secrets.token_hex(32)}
    envelope_bytes = (json.dumps(envelope, sort_keys=True) + '\n').encode()
    envelope_path = root / 'evidence/startup-envelope.json'
    write_once(envelope_path, envelope_bytes)
    envelope_hash = bootstrap.hashlib.sha256(envelope_bytes).hexdigest()
    os.mkfifo(root / 'ready.fifo', 0o600)
    os.mkfifo(root / 'go.fifo', 0o600)
    read_fd = os.open(root / 'ready.fifo', os.O_RDWR | os.O_NONBLOCK)
    go_fd = os.open(root / 'go.fifo', os.O_RDWR | os.O_NONBLOCK)
    process = None
    saved = None
    terminal = False
    launch_pidfd = None
    status = {'custody': 'not-started'}
    old_handlers = {}
    forward_thread = None
    stop_read, stop_write = os.pipe2(os.O_CLOEXEC | os.O_NONBLOCK)
    failure_read, failure_write = os.pipe2(os.O_CLOEXEC | os.O_NONBLOCK)
    def interrupted(signum, frame):
        raise CustodyError('operator interrupted: ' + str(signum))
    try:
        for sig in (signal.SIGINT, signal.SIGTERM):
            old_handlers[sig] = signal.signal(sig, interrupted)
        production_capture(manifest, 'before')
        command = [provider(manifest, 'systemd_run'), '--user', '--unit=' + manifest['unit_name'],
                   '--service-type=exec', '--wait', '--pipe', '--property=KillMode=control-group',
                   '--property=SendSIGKILL=yes', '--property=TimeoutStopSec=15s',
                   '--property=RuntimeMaxSec=20m', provider(manifest, 'python'), '-I', '-B', driver['path'],
                   'in-unit', str(manifest_path), expected_manifest_digest, str(envelope_path), envelope_hash]
        write_once(root / 'evidence/systemd-run.command.json', (json.dumps(command) + '\n').encode())
        log = os.open(root / 'evidence/systemd-run.log', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            process = subprocess.Popen(command, env=manifest['operator_environment'], stdout=log, stderr=log,
                                       stdin=subprocess.DEVNULL, close_fds=True)
        finally:
            os.close(log)
        status['custody'] = 'launch-uncertain'
        launch_pidfd = os.pidfd_open(process.pid)
        def forward():
            try:
                forward_operator_input(root, envelope['nonce'], process, stop_read)
            except BaseException as exc:
                try:
                    os.write(failure_write, str(exc).encode('utf-8', 'replace')[:4096] or b'forwarding failed')
                except OSError:
                    pass
        forward_thread = threading.Thread(target=forward, name='operator-forward', daemon=True)
        forward_thread.start()
        ready = read_fifo(read_fd, time.monotonic() + manifest['handshake_timeout_seconds'], (failure_read, launch_pidfd))
        identity = unit_show(manifest)
        if identity['Id'] != manifest['unit_name'] or identity['InvocationID'] != ready['invocation_id'] or int(identity['MainPID']) != ready['pid']:
            raise CustodyError('startup unit identity mismatch')
        expected_argv = [provider(manifest, 'python'), '-I', '-B', driver['path'], 'in-unit', str(manifest_path), expected_manifest_digest, str(envelope_path), envelope_hash]
        observed_argv = Path('/proc/%d/cmdline' % ready['pid']).read_bytes().split(b'\0')[:-1]
        if observed_argv != [arg.encode() for arg in expected_argv]:
            raise CustodyError('startup process argv differs from admitted command')
        if os.path.realpath('/proc/%d/exe' % ready['pid']) != os.path.realpath(expected_argv[0]):
            raise CustodyError('startup process executable differs from admitted Python')
        if expected_argv[0] not in identity['ExecStart'] or driver['path'] not in identity['ExecStart']:
            raise CustodyError('startup ExecStart does not name admitted driver')
        if start_ticks(ready['pid']) != ready['start_ticks']:
            raise CustodyError('startup process identity mismatch')
        group = cgroup_identity(identity['ControlGroup'])
        saved = {'unit': identity, 'cgroup': group, 'start_ticks': ready['start_ticks'],
                 'production_before_sha256': before_digest(root)}
        write_once(root / 'evidence/unit-start.json', (json.dumps(saved, sort_keys=True) + '\n').encode())
        message = (json.dumps(saved, sort_keys=True) + '\n').encode()
        if len(message) > 4096 or os.write(go_fd, message) != len(message):
            raise CustodyError('startup go write incomplete')
        status['custody'] = 'owned'
        code = _wait_process(process, time.monotonic() + manifest['terminal_timeout_seconds'], failure_read)
        terminal = True
        status['systemd_run_exit'] = code
        if code:
            raise CustodyError('unit returned failure')
    except BaseException as exc:
        status['error'] = str(exc)
    finally:
        if forward_thread is not None:
            os.write(stop_write, b'x')
            forward_thread.join(timeout=manifest['control_timeout_seconds'])
            if forward_thread.is_alive():
                status['forward_error'] = 'forwarding thread did not terminate'
        if process is not None and not terminal and saved is not None:
            try:
                output = guarded_stop(manifest, saved)
                write_once(root / 'evidence/unit-stop.stdout', output)
                status['systemd_run_exit'] = _wait_process(process, time.monotonic() + manifest['control_timeout_seconds'])
                terminal = True
            except BaseException as exc:
                status['stop_error'] = str(exc)
        if terminal and saved is not None:
            try:
                empty = cgroup_empty(saved)
                write_once(root / 'evidence/cgroup-terminal.json', (json.dumps(empty, sort_keys=True) + '\n').encode())
                unlink_auth_after_terminal(manifest)
                production_capture(manifest, 'after')
                production_compare(root)
                status['custody'] = 'terminal-and-empty'
                status['production'] = 'equal'
            except BaseException as exc:
                status['reconciliation_error'] = str(exc)
                status['custody'] = 'uncertain'
        elif process is not None:
            status['custody'] = 'uncertain'
        for sig, handler in old_handlers.items():
            signal.signal(sig, handler)
        os.close(read_fd)
        os.close(go_fd)
        for fd in (stop_read, stop_write, failure_read, failure_write):
            os.close(fd)
        if launch_pidfd is not None:
            os.close(launch_pidfd)
        write_once(root / 'evidence/operator-status.json', (json.dumps(status, sort_keys=True) + '\n').encode())
        retain_evidence(root, manifest['retained_evidence'])
    if status.get('error') or status.get('stop_error') or status.get('reconciliation_error') or status.get('forward_error') or status['custody'] != 'terminal-and-empty':
        raise CustodyError('run incomplete; see retained operator status')
    return status


def forward_operator_input(root, nonce, unit_process, stop_fd):
    """Outer driver forwards Field's framed stdin to the in-unit FIFO.

    Same-UID process identity, nonce and byte consistency are custody checks,
    not an authentication claim. Invoked by the outer owner's thread only.
    """
    libc = ctypes.CDLL(None, use_errno=True)
    notify = libc.inotify_init1(os.O_CLOEXEC | os.O_NONBLOCK)
    if notify < 0:
        raise OSError(ctypes.get_errno(), 'inotify_init1')
    selector = selectors.DefaultSelector()
    unit_fd = os.pidfd_open(unit_process.pid)
    fifo_fd = None
    forward_registered = False
    queue = bytearray()
    stdin_buffer = bytearray()
    directory = Path(root) / 'evidence/operator-channel'
    fifo = directory / 'events.fifo'
    watched = False
    try:
        if libc.inotify_add_watch(notify, os.fsencode(Path(root) / 'evidence'), 0x100 | 0x80 | 0x20) < 0:
            raise OSError(ctypes.get_errno(), 'watch evidence')
        selector.register(notify, selectors.EVENT_READ, 'filesystem')
        selector.register(unit_fd, selectors.EVENT_READ, 'unit-exit')
        selector.register(stop_fd, selectors.EVENT_READ, 'stop')
        selector.register(0, selectors.EVENT_READ, 'field-input')
        while True:
            if directory.is_dir() and not watched:
                if libc.inotify_add_watch(notify, os.fsencode(directory), 0x100 | 0x80 | 0x20) < 0:
                    raise OSError(ctypes.get_errno(), 'watch operator channel')
                watched = True
            if watched and fifo_fd is None and fifo.exists():
                try:
                    fifo_fd = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK | os.O_NOFOLLOW | os.O_CLOEXEC)
                    if not stat.S_ISFIFO(os.fstat(fifo_fd).st_mode):
                        raise CustodyError('operator channel is not FIFO')
                    if queue:
                        selector.register(fifo_fd, selectors.EVENT_WRITE, 'forward')
                        forward_registered = True
                except OSError as exc:
                    import errno
                    if exc.errno != errno.ENXIO:
                        raise
            for key, _ in selector.select():
                if key.data in ('stop', 'unit-exit'):
                    return
                if key.data == 'filesystem':
                    try:
                        os.read(notify, 65536)
                    except BlockingIOError:
                        pass
                elif key.data == 'field-input':
                    data = os.read(0, 65536)
                    if not data:
                        raise CustodyError('Field operator input ended')
                    stdin_buffer.extend(data)
                    if len(stdin_buffer) > 131072:
                        raise CustodyError('Field input frame too large')
                    while b'\n' in stdin_buffer:
                        line, _, remaining = stdin_buffer.partition(b'\n')
                        stdin_buffer = bytearray(remaining)
                        try:
                            frame = json.loads(line)
                        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                            raise CustodyError('invalid Field input frame') from exc
                        if not isinstance(frame, dict) or frame.pop('nonce', None) != nonce:
                            raise CustodyError('Field input nonce mismatch')
                        output = (json.dumps(frame, separators=(',', ':')) + '\n').encode()
                        if len(queue) + len(output) > 131072:
                            raise CustodyError('Field forwarding queue full')
                        queue.extend(output)
                        if fifo_fd is not None and not forward_registered:
                            selector.register(fifo_fd, selectors.EVENT_WRITE, 'forward')
                            forward_registered = True
                elif key.data == 'forward' and queue:
                    try:
                        written = os.write(fifo_fd, queue)
                    except BlockingIOError:
                        continue
                    del queue[:written]
                    if not queue:
                        selector.unregister(fifo_fd)
                        forward_registered = False
    finally:
        selector.close()
        if fifo_fd is not None:
            os.close(fifo_fd)
        os.close(unit_fd)
        os.close(notify)
