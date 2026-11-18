"""Source-only building blocks for the native matrix; not yet a complete run.

Subscriptions use the pinned Flow CLI stream; native read proof and graceful
Flow/pane closure must be assembled before a caller may enable Launch.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import time


class MatrixError(Exception):
    pass


KINDS = {'O': 'Order', 'Q': 'Question', 'T': 'Task', 'N': 'Notice', 'L': 'Living',
         'K': 'Question', 'O2': 'Order', 'Q2': 'Question', 'T2': 'Task'}


def valid_id(value):
    return isinstance(value, str) and bool(re.fullmatch(r'[A-Za-z0-9_-]+', value))


class Evidence:
    def __init__(self):
        self.requests = {}
        self.turns = {'sender': 0, 'receiver': 0}
        self.refreshes = 0

    def instructed_turn(self, address):
        if address not in self.turns:
            raise MatrixError('address outside synthetic pair')
        self.turns[address] += 1
        if self.turns[address] > 12:
            raise MatrixError('instructed turn budget exceeded')

    def request(self, label, request_id, kind, deadline=None):
        if KINDS.get(label) != kind or not valid_id(request_id):
            raise MatrixError('request kind or ID mismatch')
        if label in self.requests or any(row['id'] == request_id for row in self.requests.values()):
            raise MatrixError('duplicate label or request ID')
        if kind == 'Task' and (not isinstance(deadline, int) or isinstance(deadline, bool) or deadline <= 0):
            raise MatrixError('actual Task deadline missing')
        self.requests[label] = {'id': request_id, 'kind': kind, 'deadline': deadline}

    def successor(self, first_prompt, old_id, new_id, actual_deadline):
        self.refreshes += 1
        if self.refreshes != 1 or not valid_id(old_id) or not valid_id(new_id) or old_id == new_id:
            raise MatrixError('successor identity or refresh count invalid')
        try:
            order, question, task = (self.requests[k] for k in ('O2', 'Q2', 'T2'))
        except KeyError as exc:
            raise MatrixError('carry requests not all observed') from exc
        if task['deadline'] != actual_deadline:
            raise MatrixError('original Task deadline was not carried')
        if any(s not in first_prompt for s in (question['id'], task['id'], str(actual_deadline))):
            raise MatrixError('successor first prompt omits original carry')
        if order['id'] in first_prompt or 'P2-order-carry-excluded-7a97' in first_prompt:
            raise MatrixError('successor prompt carries excluded Order')


def native_send(target, kind, body, request_id=None):
    if target not in ('proposalTwoSender', 'proposalTwoReceiver'):
        raise MatrixError('target outside synthetic pair')
    if kind not in ('Order', 'Question', 'Result', 'Notice') or not isinstance(body, str) or not body:
        raise MatrixError('invalid native send shape')
    result = {'target': {'aspect': 'Mind', 'topic': target, 'model': 'Luna'},
              'priority': 'Soft', 'kind': kind, 'body': body}
    if kind == 'Result':
        if not valid_id(request_id):
            raise MatrixError('Result requires captured request ID')
        result['request'] = request_id
    elif request_id is not None:
        raise MatrixError('request belongs only to Result')
    return result


def private_cli(manifest, request):
    import shlex
    return 'XDG_CONFIG_HOME=' + shlex.quote(manifest['root'] + '/config') + ' ' + \
           shlex.quote(manifest['providers']['flow']['path']) + ' ' + shlex.quote(request)


def identity_binding(agent_list, agent_get, process_info, pane, native_session):
    """Require one exact current pane; process metadata is not native-PID proof."""
    try:
        rows = agent_list['result']['agents']
        matches = [r for r in rows if r.get('pane_id') == pane]
        item = agent_get['result']['agent']
        info = process_info['result']['process_info']
        if (agent_list['id'] != 'cli:agent:list' or agent_list['result']['type'] != 'agent_list' or
            agent_get['id'] != 'cli:agent:get' or agent_get['result']['type'] != 'agent_info' or
            process_info['id'] != 'cli:pane:process_info' or process_info['result']['type'] != 'pane_process_info' or
            len(matches) != 1 or item != matches[0] or info['pane_id'] != pane or
            item['agent_session']['value'] != native_session):
            raise MatrixError('ambiguous pane/session association')
    except (KeyError, TypeError) as exc:
        raise MatrixError('incomplete pane/session association') from exc
    return info


class Stream:
    """A selector-driven CLI subscription; owns no signal or numeric-PID kill."""
    def __init__(self, owner, name, query, opened_head):
        self.name = name
        self.process = owner.command(name, [owner.manifest['providers']['flow']['path'], query],
                                     stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.fd = self.process.stdout.fileno()
        os.set_blocking(self.fd, False)
        self.pidfd = os.pidfd_open(self.process.pid)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.fd, selectors.EVENT_READ, 'output')
        self.selector.register(self.pidfd, selectors.EVENT_READ, 'exit')
        self.buffer = b''
        self.evidence = Path(owner.manifest['root']) / 'evidence' / (name + '.stream')
        self.output = open(self.evidence, 'xb', buffering=0)
        self.opened_head = opened_head

    def next_line(self, deadline):
        while b'\n' not in self.buffer:
            events = self.selector.select(max(0, deadline - time.monotonic()))
            if not events:
                raise MatrixError(self.name + ' stream deadline')
            if any(key.data == 'exit' for key, _ in events):
                raise MatrixError(self.name + ' observer exited')
            try:
                chunk = os.read(self.fd, 65536)
            except BlockingIOError:
                continue
            if not chunk:
                raise MatrixError(self.name + ' observer closed')
            self.output.write(chunk)
            self.buffer += chunk
            if len(self.buffer) > 1048576:
                raise MatrixError('oversized observation')
        line, self.buffer = self.buffer.split(b'\n', 1)
        return line.decode('utf-8')

    def opened(self, deadline):
        line = self.next_line(deadline)
        if not (line == self.opened_head or line.startswith(self.opened_head + '.') or line.startswith(self.opened_head + ' ')):
            raise MatrixError(self.name + ' opening receipt mismatch')
        return line

    def close_observer(self):
        self.output.close()
        self.selector.close()
        os.close(self.pidfd)
        self.process.stdout.close()


def observe_before_launch(owner, deadline):
    sends = Stream(owner, 'observe-sends', 'ObserveSends.None', 'SendsObserved')
    try:
        sends.opened(deadline)
        turns = Stream(owner, 'observe-turn-ends', 'Observe.TurnEnds', 'TurnEndsObserved')
        try:
            turns.opened(deadline)
        except BaseException:
            turns.close_observer()
            raise
        return sends, turns
    except BaseException:
        sends.close_observer()
        raise


class EvidenceChannel:
    """Finite newline-JSON channel; the caller supplies a live peer pidfd.

    An independent reviewer must establish the peer and native identity cut.
    This class checks the submitted source material and retains raw records; it
    does not turn a model submission into evidence of a provider read.
    """
    MAX_FRAME = 131072

    def __init__(self, root, peer_pidfd, identity):
        self.root = Path(root)
        self.directory = self.root / 'evidence' / 'operator-channel'
        self.directory.mkdir(mode=0o700, exist_ok=False)
        self.fifo = self.directory / 'events.fifo'
        os.mkfifo(self.fifo, 0o600)
        self.fd = os.open(self.fifo, os.O_RDWR | os.O_NONBLOCK | os.O_CLOEXEC)
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.fd, selectors.EVENT_READ, 'channel')
        self.selector.register(peer_pidfd, selectors.EVENT_READ, 'peer-exit')
        self.buffer = b''
        self.counter = 0
        self.identity = identity
        self.expected = []
        self.controls = {}
        self.requests = {}

    def register_control(self, control_id, side):
        if not valid_id(control_id) or side not in ('sender', 'receiver') or control_id in self.controls:
            raise MatrixError('invalid or reused control Question ID')
        self.controls[control_id] = side

    def expect(self, cut, label, side, kind, marker, control_id):
        if self.controls.get(control_id) != side or KINDS.get(label) != kind or not marker:
            raise MatrixError('invalid expected evidence cut')
        if any(row['label'] == label for row in self.expected) or label in self.requests:
            raise MatrixError('duplicate expected request')
        self.expected.append({'cut': cut, 'label': label, 'side': side, 'kind': kind,
                              'marker': marker, 'control_id': control_id})

    def _retain(self, name, content):
        path = self.directory / name
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(content)

    def _source(self, reference):
        if not isinstance(reference, dict) or set(reference) != {'path', 'sha256'}:
            raise MatrixError('source reference must bind path and hash')
        rel = Path(reference['path'])
        if rel.is_absolute() or len(rel.parts) < 2 or rel.parts[0] not in ('evidence', 'transcripts'):
            raise MatrixError('source must be in private evidence or transcripts')
        if any(part in ('', '.', '..') or 'auth' in part.lower() or 'credential' in part.lower() for part in rel.parts):
            raise MatrixError('invalid or credential-bearing source path')
        expected = reference['sha256']
        if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected):
            raise MatrixError('invalid source hash')
        fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            for index, part in enumerate(rel.parts):
                final = index == len(rel.parts) - 1
                flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC
                if not final:
                    flags |= os.O_DIRECTORY
                next_fd = os.open(part, flags, dir_fd=fd)
                os.close(fd)
                fd = next_fd
            import stat
            st = os.fstat(fd)
            if not stat.S_ISREG(st.st_mode) or st.st_uid != os.getuid() or st.st_nlink != 1 or st.st_size > 1048576:
                raise MatrixError('source must be a bounded regular file')
            chunks = []
            total = 0
            while True:
                chunk = os.read(fd, 65536)
                if not chunk:
                    break
                total += len(chunk)
                if total > 1048576:
                    raise MatrixError('source exceeds size limit')
                chunks.append(chunk)
            content = b''.join(chunks)
        finally:
            os.close(fd)
        if hashlib.sha256(content).hexdigest() != expected:
            raise MatrixError('source bytes differ from submitted hash')
        return content

    def _next_frame(self, deadline):
        while b'\n' not in self.buffer:
            events = self.selector.select(max(0, deadline - time.monotonic()))
            if not events:
                raise MatrixError('operator evidence deadline expired')
            if any(key.data == 'peer-exit' for key, _ in events):
                raise MatrixError('operator evidence peer exited')
            try:
                data = os.read(self.fd, 65536)
            except BlockingIOError:
                continue
            if not data:
                raise MatrixError('operator evidence channel closed')
            self.buffer += data
            if len(self.buffer) > self.MAX_FRAME:
                raise MatrixError('operator evidence frame exceeds limit')
        frame, self.buffer = self.buffer.split(b'\n', 1)
        if not frame:
            raise MatrixError('empty evidence frame')
        return frame

    def receive(self, deadline):
        if not self.expected:
            raise MatrixError('unexpected evidence with no active cut')
        frame = self._next_frame(deadline)
        index = self.counter
        self.counter += 1
        self._retain('%04d.raw.json' % index, frame + b'\n')
        def unique_object(pairs):
            value = {}
            for key, item in pairs:
                if key in value:
                    raise MatrixError('duplicate JSON field')
                value[key] = item
            return value
        try:
            event = json.loads(frame, object_pairs_hook=unique_object, parse_constant=lambda _: (_ for _ in ()).throw(MatrixError('invalid JSON constant')))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('malformed evidence JSON') from exc
        keys = {'cut', 'label', 'side', 'kind', 'marker', 'control_id', 'request_id',
                'deadline', 'receipt', 'transcript', 'acknowledgement', 'identity',
                'reader_side', 'reader_identity'}
        if not isinstance(event, dict) or set(event) != keys:
            raise MatrixError('evidence event has wrong fields')
        expected = self.expected[0]
        if any(event[key] != value for key, value in expected.items()):
            raise MatrixError('out-of-order, wrong-side or wrong-kind evidence')
        request_id = event['request_id']
        if not valid_id(request_id) or request_id in self.requests.values() or request_id in self.controls:
            raise MatrixError('invalid or previously used request ID')
        if event['identity'] != self.identity.get(event['side']):
            raise MatrixError('pane/session/process identity does not match observed cut')
        if event['reader_side'] != 'receiver' or event['reader_identity'] != self.identity.get('receiver'):
            raise MatrixError('acknowledgement is not bound to receiver identity')
        deadline_value = event['deadline']
        if event['kind'] == 'Task':
            if not isinstance(deadline_value, int) or isinstance(deadline_value, bool) or deadline_value <= 0:
                raise MatrixError('Task deadline missing')
        elif deadline_value is not None:
            raise MatrixError('unexpected deadline on non-Task')
        receipt = self._source(event['receipt'])
        transcript = self._source(event['transcript'])
        try:
            receipt_text = receipt.decode('utf-8')
            transcript_text = transcript.decode('utf-8')
        except UnicodeDecodeError as exc:
            raise MatrixError('evidence must be UTF-8') from exc
        # Exact boundary on the ID avoids matching a guessed ID as a substring.
        boundary = r'(?<![A-Za-z0-9_-])' + re.escape(request_id) + r'(?![A-Za-z0-9_-])'
        acknowledgement = event['acknowledgement']
        if not isinstance(acknowledgement, str) or not acknowledgement or '\n' in acknowledgement:
            raise MatrixError('one explicit acknowledgement line required')
        if event['label'] in ('O', 'Q', 'N', 'O2', 'Q2'):
            try:
                payload = json.loads(receipt_text)
                items = payload['contentItems']
                if payload['success'] is not True or len(items) != 1 or items[0]['type'] != 'inputText':
                    raise MatrixError('native tool response is not typed success')
                receipt_text = items[0]['text']
                if not receipt_text.startswith('Accepted.'):
                    raise MatrixError('native tool response is not Accepted')
            except (KeyError, TypeError, json.JSONDecodeError) as exc:
                raise MatrixError('invalid native tool response') from exc
        elif not receipt_text.strip().startswith('SendAccepted.'):
            raise MatrixError('ordinary CLI response is not SendAccepted')
        if len(re.findall(boundary, receipt_text)) != 1 or event['marker'] not in acknowledgement or not re.search(boundary, acknowledgement):
            raise MatrixError('receipt or explicit marker/ID acknowledgement missing')
        if acknowledgement not in transcript_text.splitlines():
            raise MatrixError('acknowledgement not present in actual transcript')
        if event['kind'] == 'Task' and str(deadline_value) not in transcript_text:
            raise MatrixError('Task deadline absent from retained transcript')
        self._retain('%04d.receipt' % index, receipt)
        self._retain('%04d.transcript' % index, transcript)
        self.requests[event['label']] = request_id
        self.expected.pop(0)
        return event

    def close(self):
        self.selector.close()
        os.close(self.fd)


def render_phase_a_sender(manifest):
    target = 'proposalTwoReceiver'
    order = native_send(target, 'Order', 'P2-order-before: record this marker and its request id; give no Result.')
    question = native_send(target, 'Question', 'P2-question-before: keep unanswered until explicitly authorized in phase A.')
    notice = native_send(target, 'Notice', 'P2-notice-before: record marker; no answer.')
    task = private_cli(manifest, 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Task.{ 15 «P2-task-before: hold until phase A authorization.» } }')
    living = private_cli(manifest, 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Living.{ «Proposal 2 isolated matrix» «P2-living-before: record this statement.» } }')
    return ('Use only the two synthetic addresses Mind/proposalTwoSender/Luna and Mind/proposalTwoReceiver/Luna. '
            'Perform the following in order, exactly once, and return each actual receipt and RequestId. '
            'Call your native send tool with ' + json.dumps(order) + '; then with ' + json.dumps(question) +
            '; run this exact command in your native terminal: ' + task + '; call native send with ' + json.dumps(notice) +
            '; run this exact command in your native terminal: ' + living +
            '. Close this instruction Question with a Result after those actions.')


def render_phase_a_receiver(manifest, ids):
    required = ('O', 'Q', 'T', 'unknown')
    if set(ids) != set(required) or any(not valid_id(ids[k]) for k in required) or len(set(ids.values())) != len(ids):
        raise MatrixError('distinct captured phase A IDs and reviewed unknown ID required')
    target = 'proposalTwoSender'
    wrong_order = native_send(target, 'Result', 'P2-result-order-refusal', ids['O'])
    wrong_task = native_send(target, 'Result', 'P2-result-task-refusal', ids['T'])
    unknown = native_send(target, 'Result', 'P2-result-unknown-refusal', ids['unknown'])
    result = native_send(target, 'Result', 'P2-result-before', ids['Q'])
    bad_done = private_cli(manifest, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ ' + ids['Q'] + ' «P2-done-question-refusal» } }')
    good_done = private_cli(manifest, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ ' + ids['T'] + ' «P2-done-before» } }')
    return ('Use only Mind/proposalTwoSender/Luna and Mind/proposalTwoReceiver/Luna. '
            'Report the exact marker and original ID for each O, Q, T, N and L you read. '
            'Then do the following in order, exactly once each: native send ' + json.dumps(wrong_order) +
            '; native send ' + json.dumps(wrong_task) + '; run ' + bad_done + '; native send ' + json.dumps(unknown) +
            '; native send ' + json.dumps(result) + '; run ' + good_done + '; make a new native send call ' +
            json.dumps(result) + '; run the same Done command again as a new call: ' + good_done +
            '. Return the actual receipts. Finish this instruction Question with a Result.')


def render_phase_b_sender(manifest):
    target = 'proposalTwoReceiver'
    order = native_send(target, 'Order', 'P2-order-carry-excluded-7a97')
    question = native_send(target, 'Question', 'P2-question-carry-required-7a97')
    task = private_cli(manifest, 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Task.{ 15 «P2-task-carry-required-7a97» } }')
    return ('Use only the two synthetic addresses. Once each, native send ' + json.dumps(order) +
            ', native send ' + json.dumps(question) + ', and run this exact command in your native terminal: ' + task +
            '. Return all actual receipts, IDs, and the admitted Task deadline. '
            'Close this instruction Question with a Result.')


def render_successor_inspect(ids):
    if set(ids) != {'Q2', 'T2'} or any(not valid_id(v) for v in ids.values()):
        raise MatrixError('captured carry IDs required')
    return ('Report the original carried Question and Task IDs and the Task deadline. '
            'Keep both unanswered and finish this instruction Question with a Result.')


def render_successor(manifest, ids):
    required = ('O2', 'Q2', 'T2')
    if set(ids) != set(required) or any(not valid_id(ids[k]) for k in required) or len(set(ids.values())) != len(ids):
        raise MatrixError('distinct captured carry IDs required')
    target = 'proposalTwoSender'
    answer = native_send(target, 'Result', 'P2-result-carry', ids['Q2'])
    unresolved = native_send(target, 'Result', 'P2-result-order-carry-refusal', ids['O2'])
    done = private_cli(manifest, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ ' + ids['T2'] + ' «P2-done-carry» } }')
    return ('Use only the two synthetic addresses. Now native send ' + json.dumps(answer) + '; run ' + done + '; make a new native send call ' +
            json.dumps(answer) + '; run the same Done command again as a new call: ' + done + '; native send ' +
            json.dumps(unresolved) + '. Return every actual receipt, then close this instruction Question with a Result.')


def render_phase_b_receiver_notice():
    return ('Read each of P2-order-carry-excluded-7a97, P2-question-carry-required-7a97 and '
            'P2-task-carry-required-7a97. Acknowledge each exact marker and original RequestId, '
            'and report the actual Task deadline. Keep the Question and Task unanswered. '
            'This is a Notice and requires no Result.')


def render_kept_answer(request_id):
    if not valid_id(request_id):
        raise MatrixError('captured unbound Question ID required')
    reply = native_send('proposalTwoSender', 'Result', 'P2-kept-answer', request_id)
    return ('Answer the unbound operator Question by invoking your native send tool exactly once with '
            + json.dumps(reply) + '. Return the actual typed response.')


def parse_started(text, session_name, receipt_tokens):
    """Decode only Started.Launched with private Herdr route and Unbound origin.

    Pinned signal-flow 319e3c3: Launched.{ FlowId SessionId
    HerdrRouteSelection Origin }; HerdrRoute is a four-string struct.
    """
    tokens = receipt_tokens(text)
    if len(tokens) != 13 or tokens[0:2] != ['Started.', '{'] or tokens[4:6] != ['Available.', '{'] or tokens[10:] != ['}', 'Unbound', '}']:
        raise MatrixError('launch receipt is not complete Started.Launched')
    def string(token):
        value = token[1] if isinstance(token, tuple) and len(token) == 2 and token[0] == 'quoted' else token
        if not isinstance(value, str) or not value or value in '{}[]':
            raise MatrixError('launch receipt contains an invalid string')
        return value
    flow_id, native_session, herdr_session, agent, pane, terminal = map(string, (tokens[2], tokens[3], tokens[6], tokens[7], tokens[8], tokens[9]))
    if not valid_id(flow_id) or herdr_session != session_name:
        raise MatrixError('launch flow or Herdr session mismatch')
    return {'flow_id': flow_id, 'native_session': native_session, 'herdr_session': herdr_session,
            'agent': agent, 'pane': pane, 'terminal': terminal}


def launch_once(owner, side, private_call, receipt_tokens, receipt):
    """One launch attempt; uncertain output is retained and never retried."""
    if side not in ('sender', 'receiver'):
        raise MatrixError('address outside synthetic pair')
    topic = 'proposalTwoSender' if side == 'sender' else 'proposalTwoReceiver'
    evidence = Path(owner.manifest['root']) / 'evidence'
    intent = evidence / (side + '.launch-intent')
    fd = os.open(intent, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    os.close(fd)
    request = 'Launch.{ { Mind ' + topic + ' Luna } Predecessors.0 «Report ready only.» }'
    reply = private_call(owner, side + '-launch', 'flow', request)
    binding = parse_started(reply, owner.manifest['session'], receipt_tokens)
    path = evidence / (side + '.launch-identity.json')
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        json.dump(binding, stream, sort_keys=True)
        stream.write('\n')
    current = private_call(owner, side + '-current', 'flow', 'Current.{ Mind ' + topic + ' Luna }')
    receipt(current, 'Current.Awake.' + binding['flow_id'])
    return binding


def close_flow(owner, flow_id, private_call, receipt):
    if not valid_id(flow_id):
        raise MatrixError('invalid captured FlowId')
    reply = private_call(owner, 'close-' + flow_id, 'flow_meta', 'Close.' + flow_id)
    receipt(reply, 'Closed.' + flow_id)
