#!/usr/bin/env python3
"""Proposal 2 finite admission boundary. No runtime action occurs without a complete manifest."""
import json
import pathlib
import sys
import os, re, hashlib, subprocess, shlex, stat, time

EXPECTED_COMMIT = "fe5a6930871707a7086c9a647867a519734220ef"

class AdmissionError(Exception):
    pass

def receipt_tokens(text):
    """Consume the complete lexical input; malformed delimiters cannot disappear."""
    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch.isspace():
            i += 1
        elif ch in "{}[]":
            result.append(ch)
            i += 1
        elif ch == "«":
            i += 1
            value = []
            while i < len(text) and text[i] != "»":
                if text[i] == "«":
                    raise AdmissionError("unescaped opening guillemet")
                if text[i] == "\\":
                    i += 1
                    if i >= len(text) or text[i] not in ("\\", "«", "»"):
                        raise AdmissionError("invalid quoted escape")
                value.append(text[i])
                i += 1
            if i == len(text):
                raise AdmissionError("unterminated quoted string")
            result.append(("quoted", "".join(value)))
            i += 1
        elif ch == "»":
            raise AdmissionError("unmatched closing guillemet")
        else:
            start = i
            while i < len(text) and not text[i].isspace() and text[i] not in "{}[]«»":
                i += 1
            result.append(text[start:i])
    return result

def canonical_expected_tokens(text):
    """Render expected String tokens using the pinned codec's bare-string rule."""
    canonical = []
    for token in receipt_tokens(text):
        if isinstance(token, tuple) and token[0] == 'quoted':
            value = token[1]
            if value and not any(ch.isspace() or ch in '{}[]<>«»();' for ch in value):
                if canonical and isinstance(canonical[-1], str) and canonical[-1].endswith('.'):
                    canonical[-1] += value
                else:
                    canonical.append(value)
                continue
        canonical.append(token)
    return canonical


def receipt(actual, expected):
    actual_tokens = receipt_tokens(actual)
    if not actual_tokens or actual_tokens != canonical_expected_tokens(expected):
        raise AdmissionError("typed receipt mismatch")

def render_prompts(root, flow, task_id):
    if not re.fullmatch(r"[0-9a-z]{4}", task_id):
        raise AdmissionError("invalid captured Task ID")
    cli = shlex.quote(os.path.join(flow,"bin/flow")); xdg=shlex.quote(os.path.join(root,"config"))
    env=f"XDG_CONFIG_HOME={xdg} {cli}"
    return [
      f"Task: {env} 'Send.{{ {{ Mind proposalTwoReceiver Luna }} Soft.Task.{{ 15 «P2-task-before: hold until phase A authorization.» }} }}'",
      f"Living: {env} 'Send.{{ {{ Mind proposalTwoReceiver Luna }} Soft.Living.{{ «Proposal 2 isolated matrix» «P2-living-before: record this statement.» }} }}'",
      f"Done: {env} 'Send.{{ {{ Mind proposalTwoSender Luna }} Soft.Done.{{ {task_id} «P2-done-before» }} }}'",
      f"PhaseB Task: {env} 'Send.{{ {{ Mind proposalTwoReceiver Luna }} Soft.Task.{{ 15 «P2-task-carry-required-7a97» }} }}'",
    ]

def unit_guard(saved, observed):
    keys=("Id","InvocationID","ControlGroup","MainPID","ExecMainStartTimestampMonotonic","ExecStart")
    if any(not saved.get(k) or saved.get(k)!=observed.get(k) for k in keys): raise AdmissionError("unit identity mismatch: refuse stop")

def cgroup_guard(expected, observed):
    raise AdmissionError("cgroup inode and kernel population witness unavailable; retain custody")

def protected_configuration(data):
    """Exclude only the three integers in ConfigurationSnapshot field 14."""
    text = data.decode('utf-8') if isinstance(data, bytes) else data
    tokens = list(re.finditer(r'«(?:\\.|[^»])*»|[{}\[\]]|[^\s{}\[\]«»]+', text))
    if len(tokens) < 3 or tokens[0].group() != 'Configuration.' or tokens[1].group() != '{':
        raise AdmissionError('invalid production Configuration')
    fields = []
    i = 2
    while i < len(tokens) and tokens[i].group() != '}':
        start = i
        if tokens[i].group().endswith('.'):
            i += 1
        if i >= len(tokens):
            raise AdmissionError('incomplete production Configuration')
        if tokens[i].group() in ('{', '['):
            depth = 1
            i += 1
            while i < len(tokens) and depth:
                depth += tokens[i].group() in ('{', '[')
                depth -= tokens[i].group() in ('}', ']')
                i += 1
            if depth:
                raise AdmissionError('incomplete production Configuration')
        else:
            i += 1
        fields.append((tokens[start].start(), tokens[i-1].end()))
    if len(fields) != 22 or i != len(tokens)-1:
        raise AdmissionError('unexpected production Configuration shape')
    start, end = fields[14]
    counter = text[start:end]
    if not re.fullmatch(r'{\s*[0-9]+\s+[0-9]+\s+[0-9]+\s*}', counter):
        raise AdmissionError('invalid production counter field')
    return (text[:start] + re.sub(r'[0-9]+', '<counter>', counter) + text[end:]).encode('utf-8')


def production_compare(before, after):
    required=("configuration.datom","fable-current.datom","services","clients")
    for name in required:
        left, right = before.get(name), after.get(name)
        if left is None or right is None:
            raise AdmissionError("production witness incomplete")
        if name == 'configuration.datom':
            left, right = protected_configuration(left), protected_configuration(right)
        if left != right:
            raise AdmissionError("production witness changed: " + name)

def unit_stop_command(saved, observed, unit, systemctl):
    unit_guard(saved, observed)
    if not re.fullmatch(r"proposal2-[A-Za-z0-9_.-]+\.service",unit): raise AdmissionError("unit name outside reserved namespace")
    if saved["Id"] != unit or not os.path.isabs(systemctl): raise AdmissionError("unit or systemctl mismatch")
    return [systemctl,"--user","stop","--job-mode=fail",unit]

def metadata_record(target, link):
    st=os.stat(target,follow_symlinks=False)
    if not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid(): raise AdmissionError("auth target must be owned regular file")
    if os.path.lexists(link): raise AdmissionError("private auth link already exists")
    return {"uid":st.st_uid,"mode":oct(st.st_mode & 0o777),"device":st.st_dev,"inode":st.st_ino,"size":st.st_size,"mtime_ns":st.st_mtime_ns}



def canonical_manifest_hash(manifest):
    """Admission hashes the entire manifest except its own record pointer."""
    content = dict(manifest)
    content.pop('admission', None)
    return hashlib.sha256(json.dumps(content, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def validate(manifest):
    required = {'candidate_commit', 'root', 'retained_evidence', 'unit_name', 'session', 'user', 'host_path',
                'providers', 'operator_providers', 'operator_environment', 'production', 'contexts',
                'admission', 'driver', 'artifacts', 'auth_target',
                'expected_configuration', 'handshake_timeout_seconds',
                'control_timeout_seconds', 'terminal_timeout_seconds', 'startup_timeout_seconds'}
    if not isinstance(manifest, dict) or set(manifest) != required:
        raise AdmissionError('manifest must contain the exact schema')
    allowed_env = {'HOME', 'USER', 'LOGNAME', 'LANG', 'PATH', 'XDG_RUNTIME_DIR', 'DBUS_SESSION_BUS_ADDRESS'}
    for env in (manifest['operator_environment'], manifest['production']['environment']):
        if not isinstance(env, dict) or not set(env) <= allowed_env or any(not isinstance(v, str) for v in env.values()):
            raise AdmissionError('operator environment contains unreviewed fields')
    if manifest['candidate_commit'] != EXPECTED_COMMIT:
        raise AdmissionError('candidate commit differs from reviewed source')
    root, retained = manifest['root'], manifest['retained_evidence']
    if (not isinstance(root, str) or not isinstance(retained, str) or
        not os.path.isabs(root) or not os.path.isabs(retained) or
        os.path.normpath(root) != root or os.path.normpath(retained) != retained or
        os.path.commonpath((root, retained)) == root):
        raise AdmissionError('retention must be an absolute normalized path outside the workload root')
    if manifest['auth_target'] != '/home/li/.codex-next-5ck97j38j3sb/auth.json':
        raise AdmissionError('auth target differs from approved target')
    if not isinstance(manifest['expected_configuration'], str) or not manifest['expected_configuration'].startswith('Configuration.'):
        raise AdmissionError('exact reviewed Configuration required')
    for name in ('handshake_timeout_seconds', 'control_timeout_seconds', 'terminal_timeout_seconds', 'startup_timeout_seconds'):
        value = manifest[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 < value <= 1200:
            raise AdmissionError('invalid finite timeout: ' + name)
    if set(manifest['contexts']) != {'psyche-belief', 'mind-belief', 'field-belief'}:
        raise AdmissionError('exact private belief repositories required')
    pins = {'psyche-belief':'47384885438a86fe522b0baf68607ec3395864da',
            'mind-belief':'622f9104da1e677dbef3530249c3f2da89ca9be4',
            'field-belief':'ebeedf43f5a9df0969fae821fd2778572dd05004'}
    for name, revision in pins.items():
        if manifest['contexts'][name]['revision'] != revision:
            raise AdmissionError('context revision mismatch: ' + name)
    return manifest


def verify_admission(manifest):
    record = manifest['admission']
    if set(record) != {'path', 'sha256'} or not os.path.isabs(record['path']):
        raise AdmissionError('admission record binding missing')
    content = pathlib.Path(record['path']).read_bytes()
    if hashlib.sha256(content).hexdigest() != record['sha256']:
        raise AdmissionError('admission record bytes differ')
    review = json.loads(content)
    if set(review) != {'manifest_sha256', 'independent_review', 'field_admission'} or review['manifest_sha256'] != canonical_manifest_hash(manifest):
        raise AdmissionError('review does not bind the manifest')
    if review['independent_review'] != 'approved' or review['field_admission'] != 'approved':
        raise AdmissionError('independent review and Field admission required')


def verify_artifacts(manifest):
    sources = {}
    artifacts = manifest['artifacts']
    if set(artifacts) != {'controller', 'bootstrap', 'orchestration', 'matrix'}:
        raise AdmissionError('complete executable artifact set required')
    for name, entry in artifacts.items():
        path = pathlib.Path(entry['path'])
        source = path.read_bytes()
        if not path.is_absolute() or hashlib.sha256(source).hexdigest() != entry['sha256']:
            raise AdmissionError('artifact mismatch: ' + name)
        sources[name] = source
        if path.parent != pathlib.Path(__file__).resolve().parent or path.name != name + '.py':
            raise AdmissionError('artifact import path mismatch: ' + name)
    if pathlib.Path(manifest['driver']['path']).resolve() != pathlib.Path(__file__).resolve() or manifest['driver']['sha256'] != artifacts['controller']['sha256']:
        raise AdmissionError('driver binding mismatch')
    return sources


def private_call(owner, label, binary, request, expected=None):
    root = pathlib.Path(owner.manifest['root'])
    evidence = root / 'evidence'
    import bootstrap
    bootstrap._write(evidence / (label + '.input.datom'), request + '\n')
    process = owner.command(label, [owner.manifest['providers'][binary]['path'], request], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    bootstrap._write(evidence / (label + '.reply.datom'), output.decode('utf-8'))
    bootstrap._write(evidence / (label + '.stderr'), error.decode('utf-8', errors='replace'))
    if process.returncode:
        raise AdmissionError(label + ' command failed')
    text = output.decode('utf-8')
    if expected is not None:
        receipt(text, expected)
    return text


def configure_and_rehearse(owner):
    m = owner.manifest
    root = m['root']
    p = m['providers']
    session = m['session']
    private_call(owner, 'unconfigured', 'flow_meta', 'Configuration', 'Unconfigured')
    commands = [
        ('nexus', f'Configure.Nexus.{{ «{root}/source» {{ «{root}/bin/codex-private» «{root}/codex» «{root}/runtime/codex/control.sock» [ gpt-6-luna ] }} {{ «{root}/bin/codex-private» «{root}/codex-unused» «{root}/runtime/codex/unused.sock» [] }} [ {{ Codex [ / «!» ] [ esc ] [] }} ] [] None None «{root}/runtime/curriculum/curriculum.sock» 60 None {session} }}'),
        ('models', 'Configure.Models.[ { Luna gpt-6-luna } ]'),
        ('hook', f'Configure.HarnessHook.«{p["flow_hook"]["path"]}»'),
        ('metaflows', 'Configure.Metaflows.[ { { Mind proposalTwoSender Luna } None [] [ spirit:core:0 intent:main-flow:0 ] [] Regular Default Maintained «Send only the explicitly assigned synthetic test requests. Stop after the assigned request; perform no other task.» [] } { { Mind proposalTwoReceiver Luna } None [] [ spirit:core:0 intent:main-flow:0 ] [] Regular Default Maintained «Receive the assigned synthetic requests and answer only Questions by Result and Tasks by Done when instructed. Keep each assigned identifier exact.» [] } ]')]
    for label, request in commands:
        private_call(owner, 'configure-' + label, 'flow_meta', request, request.replace('Configure.', 'Configured.', 1))
    config = private_call(owner, 'configuration', 'flow_meta', 'Configuration', m['expected_configuration'])
    tokens = receipt_tokens(config)
    for topic in ('proposalTwoSender', 'proposalTwoReceiver'):
        if tokens.count(topic) != 1:
            raise AdmissionError('private Configuration does not have exactly two synthetic rows')
    if '/home/li/.local/bin' in config:
        raise AdmissionError('production wrapper in private Configuration')
    hashes = {}
    for side, topic in (('sender', 'proposalTwoSender'), ('receiver', 'proposalTwoReceiver')):
        request = f'Rehearse.{{ {{ Mind {topic} Luna }} Predecessors.0 «Report ready only.» }}'
        result = private_call(owner, side + '-rehearsed', 'flow', request)
        if not result.strip().startswith('Rehearsed.'):
            raise AdmissionError('rehearsal refused: ' + side)
        hashes[side] = hashlib.sha256(result.encode()).hexdigest()
    return hashes


def private_workload(owner, peer_fd, nonce, deadline):
    import orchestration
    import matrix
    owner.stage()
    for name, value in owner.manifest['contexts'].items():
        owner.archive_context(name, value['repository'], value['revision'])
    owner.compile_place(receipt)
    orchestration.auth_link(owner.manifest)
    owner.start_services()
    owner.bind_service_endpoint('flow', 'flow_daemon', owner.manifest['root'] + '/runtime/nexus/proposalTwo/flow.sock')
    owner.bind_service_endpoint('codex', 'raw_codex', owner.manifest['root'] + '/runtime/codex/control.sock')
    channel = matrix.EvidenceChannel(owner.manifest['root'], peer_fd, {}, owner.manifest['providers'])
    try:
        hashes = configure_and_rehearse(owner)
        channel.review_rehearsals(hashes, min(deadline, time.monotonic() + owner.manifest['control_timeout_seconds']))
        matrix.run_matrix(owner, channel, deadline, private_call, receipt_tokens, receipt)
    finally:
        channel.close()


def main(argv):
    try:
        if len(argv) not in (3, 6) or argv[1] not in ('run', 'in-unit'):
            raise AdmissionError('usage: controller.py {run|in-unit} MANIFEST [MANIFEST_SHA256]')
        path = pathlib.Path(argv[2]).resolve(strict=True)
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if argv[1] == 'in-unit' and (len(argv) != 6 or digest != argv[3]):
            raise AdmissionError('in-unit manifest hash mismatch')
        manifest = validate(json.loads(raw))
        verify_admission(manifest)
        sources = verify_artifacts(manifest)
        import types
        for name in ('bootstrap', 'orchestration', 'matrix'):
            module = types.ModuleType(name)
            module.__file__ = manifest['artifacts'][name]['path']
            sys.modules[name] = module
            exec(compile(sources[name], module.__file__, 'exec'), module.__dict__)
        import orchestration
        if argv[1] == 'run' and len(argv) == 3:
            orchestration.operator(manifest, str(path), digest, production_compare)
        elif argv[1] == 'in-unit':
            orchestration.in_unit(manifest, private_workload, argv[4], argv[5])
        else:
            raise AdmissionError('invalid command')
        return 0
    except Exception as exc:
        print('STOP: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
