"""Source-only building blocks for the native matrix; not yet a complete run.

Subscriptions use the pinned Flow CLI stream; native read proof and graceful
Flow/pane closure must be assembled before a caller may enable Launch.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import selectors
import subprocess
import threading
import time


class MatrixError(Exception):
    pass


def strict_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise MatrixError('duplicate JSON field')
            result[key] = value
        return result
    def invalid_constant(value):
        raise MatrixError('invalid JSON constant')
    return json.loads(data, object_pairs_hook=unique, parse_constant=invalid_constant)


KINDS = {'O': 'Order', 'Q': 'Question', 'T': 'Task', 'N': 'Notice', 'L': 'Living',
         'K': 'Question', 'O2': 'Order', 'Q2': 'Question', 'T2': 'Task'}


def valid_id(value):
    return isinstance(value, str) and bool(re.fullmatch(r'[A-Za-z0-9_-]+', value))


def valid_request_id(value):
    return isinstance(value, str) and bool(re.fullmatch(r'[0-9a-z]{4}', value))


def typed_receipt(text, receipt_tokens):
    """Read all delimiters, retaining struct/vector and quoted-string distinctions."""
    tokens = receipt_tokens(text)
    def read(index, end):
        out = []
        while index < len(tokens) and tokens[index] != end:
            token = tokens[index]
            if token in ('{', '['):
                nested, index = read(index + 1, '}' if token == '{' else ']')
                out.append(('struct' if token == '{' else 'vector', nested))
            elif token in ('}', ']'):
                raise MatrixError('mismatched receipt delimiter')
            else:
                out.append(token)
                index += 1
        if end is not None:
            if index >= len(tokens): raise MatrixError('unterminated receipt')
            index += 1
        return out, index
    result, index = read(0, None)
    if index != len(tokens): raise MatrixError('trailing receipt input')
    return result


def enum(*names, **payloads):
    return ('enum', {**{name: None for name in names}, **payloads})


def struct(*fields):
    return ('struct', fields)


def option(schema):
    return enum('None', Some=schema)


def consume_typed(schema, items):
    if not items: raise MatrixError('missing typed payload')
    head, tail = items[0], items[1:]
    if schema == 'string':
        if isinstance(head, tuple) and len(head) == 2 and head[0] == 'quoted': return head[1], tail
        if isinstance(head, str) and head: return head, tail
        raise MatrixError('invalid string payload')
    if schema == 'integer':
        if not isinstance(head, str) or not re.fullmatch(r'-?(0|[1-9][0-9]*)', head) or not -(2**63) <= int(head) < 2**63:
            raise MatrixError('invalid integer payload')
        return head, tail
    kind, fields = schema
    if kind == 'struct':
        if not isinstance(head, tuple) or len(head) != 2 or head[0] != 'struct': raise MatrixError('expected struct payload')
        values, remaining = [], head[1]
        for field in fields:
            value, remaining = consume_typed(field, remaining)
            values.append(value)
        if remaining: raise MatrixError('extra struct payload')
        return values, tail
    if kind != 'enum' or not isinstance(head, str): raise MatrixError('invalid variant')
    for name, payload in fields.items():
        if payload is None and head == name: return name, tail
        prefix = name + '.'
        if payload is not None and head.startswith(prefix):
            suffix = head[len(prefix):]
            value, remaining = consume_typed(payload, ([suffix] if suffix else []) + tail)
            return (name, value), remaining
    raise MatrixError('unknown or malformed variant')


def delivery_state_schema():
    text, integer = 'string', 'integer'
    aspect = enum('Psyche', 'Mind', 'Field')
    model = enum('Fable', 'Opus', 'Sonnet', 'Haiku', 'Astra', 'Sol', 'Luna', 'Terra')
    address = struct(aspect, text, model)
    process = struct(integer, integer)
    lock = struct(address, address, integer)
    seat = struct(option(struct(text, text)), option(text), option(text), integer, process)
    minutes = enum('Zero', 'Negative', 'Unreachable')
    unknown = enum('Address', 'Flow', 'Key', Lock=lock)
    refusal = enum('Locked', 'Awake', 'Asleep', 'Lapsed', 'NotConfigured', 'NotMessage', 'Unresolved',
                   'RequestIdSpaceFull', 'RequestIdDrawsCollided', Held=lock, Unknown=unknown, Taken=address,
                   Unidentified=seat, Store=text, NotSendServer=process, Oversized=struct(integer, integer),
                   Direct=text, TopicRefused=text, MinutesRefused=minutes, PermaflowHeld=address)
    fault = enum('InvalidPredecessor', 'RootUnresolved', 'NotUtf8', Unreadable=text)
    composition = enum('InvalidLaunchRequestId', 'InvalidModelName', 'InvalidEffort', 'InvalidToolSet',
        'InvalidHerdrSessionName', 'InvalidSystemModules', 'InvalidPromptModules', 'InvalidRemembering',
        'InexactModel', 'Unconfigured', 'PresentationUnavailable', 'Unrecorded',
        HandoverUnreadable=struct(text, fault), RecoveryUnavailable=struct(address, text, text),
        RecoveryPredecessorMismatch=struct(address, address, text, text, text))
    flags = enum('UnclosedSingleQuote', 'UnclosedDoubleQuote', 'TrailingEscape')
    binding = enum('PaneMismatch', 'TerminalMismatch', 'HarnessMismatch', 'NotReady', 'ReservedIdentityMismatch',
                   'ClaimUnavailable', 'ObservationRefused', 'TransportRefused', 'Unclassified')
    native_target = enum('HerdrUnreadable', 'PaneMismatch', 'NoNativeSession', 'IdentityInexact')
    registration = enum('RouteUnverified', 'RoleConflict', 'RoleUnrecorded', 'PaneBindingForeign',
                        'AcknowledgementMismatch', 'PromptNotCanonical', 'TranscriptBoundary', 'ThreadNotNamed',
                        'Unclassified', NativeTarget=native_target)
    stage = enum('Open', 'CodexThread', 'Spawn', 'Bind', 'Naming', 'Receipt', 'Confirm', 'Unclassified')
    failure = enum('PaneTargetMismatch', 'NativeSessionMissing', 'NativeIdentityConflict', 'FlowClaimUnavailable',
        'HarnessMismatch', 'HerdrUnreadable', 'ForeignBinding', 'InvalidFlowId', 'NotReady', 'TranscriptUnreadable',
        'TitleReadbackDiffers', 'CodexNamingRefused', 'PaneLabelRefused', 'AdapterRefused', 'BoundaryMismatch',
        'ThreadNotNamed', 'PartDiffers', 'LeaveOutShown', 'ModelOrEffortDiffers', 'SessionUnrecorded',
        'Unclassified', 'SendToolUnsupported', 'WorkspaceLabelRefused')
    context = enum('ComposerUnavailable', 'MetaflowMismatch', 'PayloadMismatch', 'RecordMissing', 'SystemTooLarge',
                   'ModuleTooLarge', ComposerRejected=text, ModuleMissing=option(text))
    leave = enum('ClaudeAiConnectors', 'ConfiguredMcpServers', 'AgentTool', 'ExplorePlanAgents', 'FileTools',
        'WorkflowTool', 'ScheduleWakeupTool', 'ReportFindingsTool', 'ListAgentsTool', 'CronTools', 'WebTools',
        'DeferredTools', 'SkillTool', 'BundledSkills', 'ClaudeMd', 'GitInstructions', 'AttributionReminder',
        'UserSettings', 'ToolSearch', 'BashTool', 'CodexSkillListing', 'CodexAgentsMd', 'CodexCollaborationMode',
        'CodexEnvironmentContext', 'CodexPermissions', 'CodexDeveloperInstructions')
    leave_refusal = enum(Indispensable=leave, NeedsWorkflowLeftOut=leave, NotForHarness=leave)
    spawn_cause = enum('ControlCharacter', 'CommandTooLong', Herdr=struct(option(text), text))
    opened = struct(text, enum('Answered', 'InProgress', 'Unanswered', 'Unread'), enum('Archived', 'ArchiveRefused'))
    spawn = struct(spawn_cause, option(opened))
    start = enum('LaunchRequestConflict', 'LaunchPersistenceRefused', 'IntentPersistenceRefused',
        'OriginUnavailable', 'AddressAwake', 'Undeclared', CompositionRefused=composition,
        MalformedHarnessFlags=flags, NativeLaunchRefused=struct(stage, failure), BindingRefused=binding,
        RegistrationRefused=registration, ContextRefused=context, LeaveOutRefused=leave_refusal,
        HarnessSpawnRefused=spawn, ModelRefused=enum('Unconfigured', Differs=text), TopicRefused=text)
    retry = enum('HistoryAbsent', 'HandOverRefused', 'OwnerResolvedAbsent', WakeRefused=start)
    return enum('Queued', 'Attempting', 'Uncertain', 'Delivered', 'Read', 'Withdrawn', 'Archived',
                Retryable=retry, Failed=refusal)


def decode_visible_acceptance(value):
    if not isinstance(value, tuple) or value[0] != 'struct': raise MatrixError('invalid visible acceptance')
    fields = value[1]
    request_id, fields = consume_typed('string', fields)
    cursor, fields = consume_typed('integer', fields)
    state, fields = consume_typed(delivery_state_schema(), fields)
    if fields or not valid_request_id(request_id) or int(cursor) < 0:
        raise MatrixError('invalid acceptance identity, cursor or trailing payload')
    if isinstance(state, tuple) and state[0] in ('Failed', 'Retryable'):
        raise MatrixError('delivery is failed or retryable, not a completed admission')
    return request_id


def parse_visible_admission(text, receipt_tokens):
    parts = typed_receipt(text, receipt_tokens)
    if len(parts) == 1 and isinstance(parts[0], str) and parts[0].startswith('Sent.'):
        request_id = parts[0][len('Sent.'):]
        if valid_request_id(request_id): return request_id
    if len(parts) == 2 and parts[0] == 'Sent.':
        request_id, remaining = consume_typed('string', parts[1:])
        if not remaining and valid_request_id(request_id): return request_id
    if len(parts) == 2 and parts[0] == 'SendAccepted.':
        return decode_visible_acceptance(parts[1])
    raise MatrixError('not a typed visible admission')


def decode_native_acceptance(text, sender, target, receipt_tokens):
    parts = typed_receipt(text, receipt_tokens)
    if len(parts) != 2 or parts[0] != 'Accepted.' or not isinstance(parts[1], tuple) or parts[1][0] != 'struct':
        raise MatrixError('invalid native acceptance')
    fields = parts[1][1]
    address_schema = struct(enum('Mind'), 'string', enum('Luna'))
    sender_value, fields = consume_typed(enum(Sender=address_schema), fields)
    target_value, fields = consume_typed(address_schema, fields)
    if sender_value != ('Sender', ['Mind', sender, 'Luna']) or target_value != ['Mind', target, 'Luna']:
        raise MatrixError('native acceptance sender or target mismatch')
    if len(fields) != 1: raise MatrixError('native acceptance arity mismatch')
    return decode_visible_acceptance(fields[0])


def decode_cli_done_request(command, receipt_tokens):
    import shlex
    try:
        argv = shlex.split(command)
    except ValueError as exc:
        raise MatrixError('invalid CLI invocation') from exc
    if len(argv) != 3 or not argv[0].startswith('XDG_CONFIG_HOME=') or not os.path.isabs(argv[1]):
        raise MatrixError('invalid private CLI invocation')
    parts = typed_receipt(argv[2], receipt_tokens)
    if len(parts) != 2 or parts[0] != 'Send.':
        raise MatrixError('not a Send invocation')
    address = struct(enum('Mind'), 'string', enum('Luna'))
    value, remaining = consume_typed(struct(address, enum(Soft=enum(Done=struct('string', 'string')))), parts[1:])
    if remaining or value[0] != ['Mind', 'proposalTwoSender', 'Luna']:
        raise MatrixError('Done invocation target mismatch')
    request_id = value[1][1][1][0]
    if not valid_request_id(request_id): raise MatrixError('invalid Done request ID')
    return request_id


def quoted_content(text):
    return text.replace('\\', '\\\\').replace('«', '\\«').replace('»', '\\»')


def control_question(owner, side, prompt, ledger, private_call, receipt_tokens):
    if side not in ('sender', 'receiver') or not isinstance(prompt, str) or not prompt:
        raise MatrixError('invalid control question')
    ledger.instructed_turn(side)
    topic = 'proposalTwoSender' if side == 'sender' else 'proposalTwoReceiver'
    quoted = quoted_content(prompt)
    label = 'control-' + side + '-' + str(ledger.turns[side])
    request = 'Send.{ { Mind ' + topic + ' Luna } Soft.Question.«' + quoted + '» }'
    response = private_call(owner, label, 'flow', request)
    return parse_visible_admission(response, receipt_tokens)


def collect_phase_a_admissions(owner, channel, ledger, deadline, private_call, receipt_tokens):
    """Instruct the sender once, then collect the five separately admitted IDs."""
    task_cutoff = min(deadline, time.monotonic() + 15 * 60)
    control = control_question(owner, 'sender', render_phase_a_sender(owner.manifest), ledger, private_call, receipt_tokens)
    channel.register_control(control, 'sender')
    rows = (('O', 'Order', 'P2-order-before'), ('Q', 'Question', 'P2-question-before'),
            ('T', 'Task', 'P2-task-before'), ('N', 'Notice', 'P2-notice-before'),
            ('L', 'Living', 'P2-living-before'))
    for label, kind, marker in rows:
        event = channel.receive_admission(label, kind, marker, task_cutoff, receipt_tokens)
        ledger.request(label, event['request_id'], kind, event['minutes'])
        if kind == 'Task':
            ledger.task_cutoffs[label] = task_cutoff
        debug = private_call(owner, 'debug-' + label, 'flow_meta', 'DebugDelivery.' + event['request_id'])
        if not debug.strip().startswith('DeliveryDebugged.'):
            raise MatrixError('DebugDelivery refused for ' + label)
    return control


def collect_phase_b_admissions(owner, channel, ledger, deadline, private_call, receipt_tokens):
    task_cutoff = min(deadline, time.monotonic() + 15 * 60)
    control = control_question(owner, 'sender', render_phase_b_sender(owner.manifest), ledger, private_call, receipt_tokens)
    channel.register_control(control, 'sender')
    rows = (('O2', 'Order', 'P2-order-carry-excluded-7a97'),
            ('Q2', 'Question', 'P2-question-carry-required-7a97'),
            ('T2', 'Task', 'P2-task-carry-required-7a97'))
    for label, kind, marker in rows:
        event = channel.receive_admission(label, kind, marker, task_cutoff, receipt_tokens)
        ledger.request(label, event['request_id'], kind, event['minutes'])
        if kind == 'Task':
            ledger.task_cutoffs[label] = task_cutoff
        debug = private_call(owner, 'debug-' + label, 'flow_meta', 'DebugDelivery.' + event['request_id'])
        if not debug.strip().startswith('DeliveryDebugged.'):
            raise MatrixError('DebugDelivery refused for ' + label)
    return control


def collect_phase_a_consumption(owner, channel, ledger, deadline, private_call, receipt_tokens):
    ids = {name: ledger.requests[name]['id'] for name in ('O', 'Q', 'T')}
    unknown = ''.join(secrets.choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(4))
    if unknown in channel.requests.values() or unknown in channel.controls:
        raise MatrixError('unknown request ID collided')
    ids['unknown'] = unknown
    control = control_question(owner, 'receiver', render_phase_a_receiver(owner.manifest, ids), ledger, private_call, receipt_tokens)
    channel.register_control(control, 'receiver')
    for label, marker in (('O', 'P2-order-before'), ('Q', 'P2-question-before'), ('T', 'P2-task-before'),
                          ('N', 'P2-notice-before'), ('L', 'P2-living-before')):
        channel.receive_consumption(label, marker, deadline)
    return control, unknown


def collect_phase_b_consumption(owner, channel, ledger, deadline, private_call, receipt_tokens):
    ledger.instructed_turn('receiver')
    prompt = quoted_content(render_phase_b_receiver_notice())
    request = 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Notice.«' + prompt + '» }'
    reply = private_call(owner, 'phase-b-receiver-notice', 'flow', request)
    parse_visible_admission(reply, receipt_tokens)
    for label, marker in (('O2', 'P2-order-carry-excluded-7a97'),
                          ('Q2', 'P2-question-carry-required-7a97'),
                          ('T2', 'P2-task-carry-required-7a97')):
        channel.receive_consumption(label, marker, deadline)


def collect_phase_a_reply_outcomes(owner, channel, ledger, unknown, deadline, private_call, receipt_tokens):
    """Require each distinct receiver call's raw invocation and typed result."""
    ids = {name: ledger.requests[name]['id'] for name in ('O', 'Q', 'T')}
    if not valid_request_id(unknown) or unknown in ids.values():
        raise MatrixError('invalid unknown request identity')
    target = 'proposalTwoSender'
    result = native_send(target, 'Result', 'P2-result-before', ids['Q'])
    good_done = private_cli(owner.manifest, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ ' + ids['T'] + ' «P2-done-before» } }')
    rows = (
        ('result-order', 'native', native_send(target, 'Result', 'P2-result-order-refusal', ids['O']), 'unresolved'),
        ('result-task', 'native', native_send(target, 'Result', 'P2-result-task-refusal', ids['T']), 'unresolved'),
        ('done-question', 'cli', private_cli(owner.manifest, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ ' + ids['Q'] + ' «P2-done-question-refusal» } }'), 'unresolved'),
        ('result-unknown', 'native', native_send(target, 'Result', 'P2-result-unknown-refusal', unknown), 'unresolved'),
        ('result-question', 'native', result, 'accepted'),
        ('done-task', 'cli', good_done, 'accepted'),
        ('duplicate-result', 'native', result, 'unresolved'),
        ('duplicate-done', 'cli', good_done, 'unresolved'),
    )
    for label, surface, invocation, expected in rows:
        answered = ids['Q'] if label == 'result-question' else ids['T'] if label == 'done-task' else None
        channel.receive_reply_outcome(label, surface, invocation, expected, deadline, receipt_tokens, answered)
    prompt = ('Report that you read P2-result-before for Question ' + ids['Q'] +
              ' and P2-done-before for Task ' + ids['T'] +
              ', naming each original RequestId. Close this instruction Question with a Result.')
    control = control_question(owner, 'sender', prompt, ledger, private_call, receipt_tokens)
    channel.register_control(control, 'sender')
    channel.receive_routed_consumption('result-question', ids['Q'], 'P2-result-before', deadline)
    channel.receive_routed_consumption('done-task', ids['T'], 'P2-done-before', deadline)


def kept_answer_case(owner, channel, ledger, deadline, private_call, receipt_tokens, receipt):
    """Ask an unbound Question, capture its native kept Result, then Answer it."""
    ledger.instructed_turn('receiver')
    question = 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Question.«P2-kept-question: wait for the next instruction.» }'
    response = private_call(owner, 'kept-question', 'flow', question)
    request_id = parse_visible_admission(response, receipt_tokens)
    if request_id in channel.requests.values() or request_id in channel.controls:
        raise MatrixError('kept Question ID reused')
    ledger.request('K', request_id, 'Question')
    channel.requests['K'] = request_id
    channel.minutes['K'] = None
    control = control_question(owner, 'receiver', render_kept_answer(request_id), ledger, private_call, receipt_tokens)
    channel.register_control(control, 'receiver')
    channel.receive_consumption('K', 'P2-kept-question', deadline)
    invocation = native_send('proposalTwoSender', 'Result', 'P2-kept-answer', request_id)
    channel.receive_reply_outcome('kept-result', 'native', invocation, 'kept', deadline, receipt_tokens)
    answered = private_call(owner, 'kept-answer', 'flow', 'Answer.' + request_id)
    receipt(answered, 'Answered.{ Sender.{ Mind proposalTwoReceiver Luna } Soft.Result.{ ' + request_id + ' «P2-kept-answer» } }')
    return request_id


def grouped_receipt(text, receipt_tokens):
    """Preserve typed heads and nested Datom structures for identity checks."""
    tokens = receipt_tokens(text)
    def group(index, end):
        result = []
        while index < len(tokens) and tokens[index] != end:
            token = tokens[index]
            if token in ('{', '['):
                value, index = group(index + 1, '}' if token == '{' else ']')
                result.append(value)
            elif token in ('}', ']'):
                raise MatrixError('unbalanced typed receipt')
            else:
                result.append(token[1] if isinstance(token, tuple) else token)
                index += 1
        if end is not None:
            if index >= len(tokens):
                raise MatrixError('unterminated typed receipt')
            index += 1
        return result, index
    result, index = group(0, None)
    if index != len(tokens):
        raise MatrixError('trailing typed receipt')
    return result


def close_control_questions(owner, channel, deadline, private_call, receipt_tokens):
    """Read kept answers for all control Questions before refreshing."""
    for request_id, side in channel.controls.items():
        if request_id in channel.closed_controls:
            continue
        channel.receive_control_completion(request_id, side, deadline, receipt_tokens)
        result = private_call(owner, 'control-answer-' + request_id, 'flow', 'Answer.' + request_id)
        parsed = grouped_receipt(result, receipt_tokens)
        topic = 'proposalTwoSender' if side == 'sender' else 'proposalTwoReceiver'
        if (len(parsed) != 2 or parsed[0] != 'Answered.' or not isinstance(parsed[1], list) or
            len(parsed[1]) != 4 or parsed[1][:3] != ['Sender.', ['Mind', topic, 'Luna'], 'Soft.Result.'] or
            not isinstance(parsed[1][3], list) or len(parsed[1][3]) != 2 or
            parsed[1][3][0] != request_id or not isinstance(parsed[1][3][1], str) or not parsed[1][3][1]):
            raise MatrixError('control Question has no matching kept Result')
        channel.closed_controls.add(request_id)


def verify_bound_inspect(text, binding, root, topic, receipt_tokens):
    parsed = grouped_receipt(text, receipt_tokens)
    try:
        if len(parsed) != 2 or parsed[0] != 'Inspected.' or len(parsed[1]) != 6:
            raise MatrixError('invalid Inspect receipt')
        metaflow, seat = parsed[1][:2]
        if topic not in ('proposalTwoSender', 'proposalTwoReceiver') or metaflow[0] != ['Mind', topic, 'Luna'] or metaflow[1] != 'Awake.' + binding['flow_id']:
            raise MatrixError('Inspect metaflow is not the bound synthetic flow')
        if len(seat) < 3 or seat[0] != 'Some.':
            raise MatrixError('Inspect has no bound FlowNode')
        node = seat[1]
        route = [binding['herdr_session'], binding['agent'], binding['pane'], binding['terminal']]
        if node[:3] != [binding['flow_id'], binding['native_session'], 'Codex']:
            raise MatrixError('Inspect FlowNode differs from bound native identity')
        if node[3] == 'Unavailable':
            tail = node[4:]
        elif node[3] == 'Available.' and node[4] == [root + '/runtime/codex/control.sock', 'Ready']:
            tail = node[5:]
        else:
            raise MatrixError('Inspect endpoint differs from private endpoint')
        if len(tail) != 4 or tail[:2] != ['Available.', route] or tail[3] != 'Active':
            raise MatrixError('Inspect FlowNode differs from bound Herdr route or lifecycle')
    except (IndexError, TypeError) as exc:
        raise MatrixError('incomplete Inspect receipt') from exc


def verify_successor_inspect(text, binding, root, receipt_tokens):
    verify_bound_inspect(text, binding, root, 'proposalTwoReceiver', receipt_tokens)


def refresh_successor(owner, channel, ledger, old, deadline, private_call, receipt_tokens, receipt):
    """Refresh once and bind the actual changed FlowNode and first prompt."""
    if ledger.refresh_attempted or old != channel.identity.get('receiver'):
        raise MatrixError('invalid predecessor or repeated refresh')
    close_control_questions(owner, channel, deadline, private_call, receipt_tokens)
    ledger.refresh_attempted = True
    stream = Stream(owner, 'observe-metaflows', 'Observe.Metaflows', 'MetaflowsObserved')
    try:
        stream.opened(deadline)
        request = 'Refresh.{ Mind proposalTwoReceiver Luna }'
        response = private_call(owner, 'receiver-refresh', 'flow', request)
        expected = '{ { Mind proposalTwoReceiver Luna } ' + old['flow_id'] + ' }'
        if response.strip().startswith('RefreshQueued.'):
            receipt(response, 'RefreshQueued.' + expected)
        else:
            receipt(response, 'Refreshed.' + expected)
        successor_id = None
        while successor_id is None:
            event = grouped_receipt(stream.next_line(deadline), receipt_tokens)
            if len(event) != 2 or event[0] != 'MetaflowChanged.' or not isinstance(event[1], list):
                raise MatrixError('unexpected metaflow event')
            row = event[1]
            if len(row) >= 2 and row[0] == ['Mind', 'proposalTwoReceiver', 'Luna'] and isinstance(row[1], str) and row[1].startswith('Awake.'):
                candidate = row[1][len('Awake.'):]
                if candidate != old['flow_id']:
                    if not valid_id(candidate):
                        raise MatrixError('invalid successor FlowId')
                    successor_id = candidate
        current = private_call(owner, 'successor-current', 'flow', 'Current.{ Mind proposalTwoReceiver Luna }')
        receipt(current, 'Current.Awake.' + successor_id)
        binding, first_prompt = channel.receive_successor(successor_id, deadline)
        if binding['herdr_session'] != owner.manifest['session'] or binding['native_session'] == old['native_session']:
            raise MatrixError('successor native identity mismatch')
        inspected = private_call(owner, 'successor-inspect', 'flow_meta', 'Inspect.{ Mind proposalTwoReceiver Luna }')
        verify_successor_inspect(inspected, binding, owner.manifest['root'], receipt_tokens)
        snapshot_native(owner, 'receiver', binding, label='successor')
        panes = herdr_json(owner, 'predecessor-pane-inventory', ['pane', 'list'])
        try:
            if panes['id'] != 'cli:pane:list' or panes['result']['type'] != 'pane_list' or any(row['pane_id'] == old['pane'] for row in panes['result']['panes']):
                raise MatrixError('predecessor pane remains or inventory is invalid')
        except (KeyError, TypeError) as exc:
            raise MatrixError('predecessor pane inventory incomplete') from exc
        ledger.successor(first_prompt, old['flow_id'], successor_id, 15)
        channel.identity['receiver'] = binding
        return binding
    finally:
        stream.close_observer()


def complete_successor_carry(owner, channel, ledger, deadline, private_call, receipt_tokens):
    ids = {name: ledger.requests[name]['id'] for name in ('O2', 'Q2', 'T2')}
    if time.monotonic() >= ledger.task_cutoffs['T2']:
        raise MatrixError('conservative Task budget expired')
    control = control_question(owner, 'receiver', render_successor_inspect({'Q2': ids['Q2'], 'T2': ids['T2']}), ledger, private_call, receipt_tokens)
    channel.register_control(control, 'receiver')
    channel.receive_successor_report(ids['Q2'], ids['T2'], deadline)
    control = control_question(owner, 'receiver', render_successor(owner.manifest, ids), ledger, private_call, receipt_tokens)
    channel.register_control(control, 'receiver')
    target = 'proposalTwoSender'
    result = native_send(target, 'Result', 'P2-result-carry', ids['Q2'])
    done = private_cli(owner.manifest, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ ' + ids['T2'] + ' «P2-done-carry» } }')
    rows = (('carry-result', 'native', result, 'accepted'),
            ('carry-done', 'cli', done, 'accepted'),
            ('carry-duplicate-result', 'native', result, 'unresolved'),
            ('carry-duplicate-done', 'cli', done, 'unresolved'),
            ('carry-order-result', 'native', native_send(target, 'Result', 'P2-result-order-carry-refusal', ids['O2']), 'unresolved'))
    for label, surface, invocation, expected in rows:
        if time.monotonic() >= ledger.task_cutoffs['T2']:
            raise MatrixError('conservative Task budget expired')
        answered = ids['Q2'] if label == 'carry-result' else ids['T2'] if label == 'carry-done' else None
        channel.receive_reply_outcome(label, surface, invocation, expected, deadline, receipt_tokens, answered)
    prompt = ('Report that you read P2-result-carry for Question ' + ids['Q2'] +
              ' and P2-done-carry for Task ' + ids['T2'] +
              ', naming each original RequestId. Close this instruction Question with a Result.')
    control = control_question(owner, 'sender', prompt, ledger, private_call, receipt_tokens)
    channel.register_control(control, 'sender')
    channel.receive_routed_consumption('carry-result', ids['Q2'], 'P2-result-carry', deadline)
    channel.receive_routed_consumption('carry-done', ids['T2'], 'P2-done-carry', deadline)


def close_synthetic_flows(owner, channel, bindings, deadline, private_call, receipt_tokens, receipt):
    if set(bindings) != {'sender', 'receiver'} or any(channel.identity.get(side) != binding for side, binding in bindings.items()):
        raise MatrixError('closure identities do not match the owned pair')
    close_control_questions(owner, channel, deadline, private_call, receipt_tokens)
    failures = []
    for side in ('receiver', 'sender'):
        try:
            if side in channel.close_attempts:
                raise MatrixError('closure already attempted')
            topic = 'proposalTwoSender' if side == 'sender' else 'proposalTwoReceiver'
            inspected = private_call(owner, side + '-before-close-inspect', 'flow_meta', 'Inspect.{ Mind ' + topic + ' Luna }')
            if not inspected.strip().startswith('Inspected.'):
                raise MatrixError('pre-close Inspect refused')
            channel.close_attempts.add(side)
            close_bound_flow_and_pane(owner, side, bindings[side], private_call, receipt)
        except Exception as exc:
            failures.append(side + ': ' + str(exc))
    if failures:
        raise MatrixError('closure incomplete: ' + '; '.join(failures))


def await_initial_turns(turns, bindings, deadline, receipt_tokens):
    pending = {binding['flow_id']: side for side, binding in bindings.items()}
    while pending:
        event = grouped_receipt(turns.next_line(deadline), receipt_tokens)
        if len(event) != 2 or event[0] != 'TurnEnded.' or not isinstance(event[1], list) or len(event[1]) != 4:
            raise MatrixError('unexpected turn-end event')
        address, harness, flow_id, observed_at = event[1]
        if flow_id not in pending:
            continue
        side = pending[flow_id]
        topic = 'proposalTwoSender' if side == 'sender' else 'proposalTwoReceiver'
        if address != ['Mind', topic, 'Luna'] or harness != 'Codex' or not isinstance(observed_at, str):
            raise MatrixError('initial turn-end identity mismatch')
        del pending[flow_id]


def run_matrix(owner, channel, deadline, private_call, receipt_tokens, receipt):
    """Run the finite, sequential private pair; missing evidence fails closed."""
    import bootstrap
    ledger = Evidence()
    bindings = {}
    sends = turns = None
    drain_fd = None
    drain_watched = False
    completed = False
    try:
        sends, turns = observe_before_launch(owner, deadline)
        drain_fd = sends.start_drain(deadline)
        channel.watch_observer_failure(drain_fd)
        drain_watched = True
        for side, topic in (('sender', 'proposalTwoSender'), ('receiver', 'proposalTwoReceiver')):
            if time.monotonic() >= deadline:
                raise MatrixError('whole-run deadline expired')
            ledger.instructed_turn(side)
            binding = launch_once(owner, side, private_call, receipt_tokens, receipt)
            bindings[side] = binding
            inspected = private_call(owner, side + '-initial-inspect', 'flow_meta', 'Inspect.{ Mind ' + topic + ' Luna }')
            verify_bound_inspect(inspected, binding, owner.manifest['root'], topic, receipt_tokens)
            snapshot_native(owner, side, binding, label=side + '-initial')
            channel.identity[side] = binding
        await_initial_turns(turns, bindings, deadline, receipt_tokens)
        collect_phase_a_admissions(owner, channel, ledger, deadline, private_call, receipt_tokens)
        phase_a_deadline = min(deadline, ledger.task_cutoffs['T'])
        _, unknown = collect_phase_a_consumption(owner, channel, ledger, phase_a_deadline, private_call, receipt_tokens)
        collect_phase_a_reply_outcomes(owner, channel, ledger, unknown, phase_a_deadline, private_call, receipt_tokens)
        kept_answer_case(owner, channel, ledger, deadline, private_call, receipt_tokens, receipt)
        collect_phase_b_admissions(owner, channel, ledger, deadline, private_call, receipt_tokens)
        phase_b_deadline = min(deadline, ledger.task_cutoffs['T2'])
        collect_phase_b_consumption(owner, channel, ledger, phase_b_deadline, private_call, receipt_tokens)
        bindings['receiver'] = refresh_successor(owner, channel, ledger, bindings['receiver'], phase_b_deadline, private_call, receipt_tokens, receipt)
        complete_successor_carry(owner, channel, ledger, phase_b_deadline, private_call, receipt_tokens)
        close_synthetic_flows(owner, channel, bindings, deadline, private_call, receipt_tokens, receipt)
        completed = True
    finally:
        failures = []
        if not completed:
            for side in ('receiver', 'sender'):
                if side not in bindings or side in channel.close_attempts:
                    continue
                channel.close_attempts.add(side)
                try:
                    close_bound_flow_and_pane(owner, side, bindings[side], private_call, receipt)
                except Exception as exc:
                    failures.append(side + ': ' + str(exc))
        if drain_watched:
            try:
                channel.unwatch_observer_failure(drain_fd)
            except Exception as exc:
                failures.append('observer watch: ' + str(exc))
        for stream in (turns, sends):
            if stream is not None:
                try:
                    stream.close_observer(owner.manifest['control_timeout_seconds'])
                except Exception as exc:
                    failures.append('observer: ' + str(exc))
        evidence = Path(owner.manifest['root']) / 'evidence' / 'matrix-custody.json'
        bootstrap._write(evidence, json.dumps({'completed': completed, 'close_attempts': sorted(channel.close_attempts), 'failures': failures}, sort_keys=True) + '\n')
        if completed and failures:
            raise MatrixError('observer cleanup incomplete')


class Evidence:
    def __init__(self):
        self.requests = {}
        self.turns = {'sender': 0, 'receiver': 0}
        self.refreshes = 0
        self.refresh_attempted = False
        self.task_cutoffs = {}

    def instructed_turn(self, address):
        if address not in self.turns:
            raise MatrixError('address outside synthetic pair')
        self.turns[address] += 1
        if self.turns[address] > 12:
            raise MatrixError('instructed turn budget exceeded')

    def request(self, label, request_id, kind, minutes=None):
        if KINDS.get(label) != kind or not valid_request_id(request_id):
            raise MatrixError('request kind or ID mismatch')
        if label in self.requests or any(row['id'] == request_id for row in self.requests.values()):
            raise MatrixError('duplicate label or request ID')
        if kind == 'Task' and (not isinstance(minutes, int) or isinstance(minutes, bool) or minutes <= 0):
            raise MatrixError('Task Minutes missing')
        self.requests[label] = {'id': request_id, 'kind': kind, 'minutes': minutes}

    def successor(self, first_prompt, old_id, new_id, minutes):
        self.refreshes += 1
        if self.refreshes != 1 or not valid_id(old_id) or not valid_id(new_id) or old_id == new_id:
            raise MatrixError('successor identity or refresh count invalid')
        try:
            order, question, task = (self.requests[k] for k in ('O2', 'Q2', 'T2'))
        except KeyError as exc:
            raise MatrixError('carry requests not all observed') from exc
        if task['minutes'] != minutes:
            raise MatrixError('original Task Minutes changed')
        if 'T2' in self.task_cutoffs and time.monotonic() >= self.task_cutoffs['T2']:
            raise MatrixError('conservative Task budget expired')
        carry = (question['id'], task['id'], str(minutes), 'P2-question-carry-required-7a97', 'P2-task-carry-required-7a97')
        if any(not re.search(r'(?<![A-Za-z0-9_-])' + re.escape(value) + r'(?![A-Za-z0-9_-])', first_prompt) for value in carry):
            raise MatrixError('successor first prompt omits original carry')
        if re.search(r'(?<![A-Za-z0-9_-])' + re.escape(order['id']) + r'(?![A-Za-z0-9_-])', first_prompt) or 'P2-order-carry-excluded-7a97' in first_prompt:
            raise MatrixError('successor prompt carries excluded Order')


def native_send(target, kind, body, request_id=None):
    if target not in ('proposalTwoSender', 'proposalTwoReceiver'):
        raise MatrixError('target outside synthetic pair')
    if kind not in ('Order', 'Question', 'Result', 'Notice') or not isinstance(body, str) or not body:
        raise MatrixError('invalid native send shape')
    result = {'target': {'aspect': 'Mind', 'topic': target, 'model': 'Luna'},
              'priority': 'Soft', 'kind': kind, 'body': body}
    if kind == 'Result':
        if not valid_request_id(request_id):
            raise MatrixError('Result requires captured request ID')
        result['request'] = request_id
    elif request_id is not None:
        raise MatrixError('request belongs only to Result')
    return result


def private_cli(manifest, request):
    import shlex
    return 'XDG_CONFIG_HOME=' + shlex.quote(manifest['root'] + '/config') + ' ' + \
           shlex.quote(manifest['providers']['flow']['path']) + ' ' + shlex.quote(request)


def bound_agent_matches(item, binding):
    reported = item.get('agent_session')
    return (item.get('name') == binding['agent'] and item.get('pane_id') == binding['pane'] and
            item.get('terminal_id') == binding['terminal'] and
            (reported is None or (isinstance(reported, dict) and reported.get('value') == binding['native_session'])))


def identity_binding(agent_list, agent_get, process_info, binding):
    """Bind supported Herdr fields to the already verified Flow/native route."""
    try:
        pane = binding['pane']
        rows = agent_list['result']['agents']
        matches = [r for r in rows if r.get('pane_id') == pane]
        item = agent_get['result']['agent']
        info = process_info['result']['process_info']
        if (agent_list['id'] != 'cli:agent:list' or agent_list['result']['type'] != 'agent_list' or
            agent_get['id'] != 'cli:agent:get' or agent_get['result']['type'] != 'agent_info' or
            process_info['id'] != 'cli:pane:process_info' or process_info['result']['type'] != 'pane_process_info' or
            len(matches) != 1 or item != matches[0] or info['pane_id'] != pane or
            not bound_agent_matches(item, binding)):
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
        self.drain_thread = None
        self.drain_failure = None
        self.stop_read = self.stop_write = self.failure_read = self.failure_write = None

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

    def start_drain(self, deadline):
        """Retain every later frame until the event-driven stop or failure."""
        if self.drain_thread is not None:
            raise MatrixError('observer drain already started')
        self.stop_read, self.stop_write = os.pipe2(os.O_CLOEXEC | os.O_NONBLOCK)
        self.failure_read, self.failure_write = os.pipe2(os.O_CLOEXEC | os.O_NONBLOCK)
        self.selector.register(self.stop_read, selectors.EVENT_READ, 'stop')
        def drain():
            try:
                while True:
                    if time.monotonic() >= deadline:
                        raise MatrixError(self.name + ' observer deadline')
                    events = self.selector.select(max(0, deadline - time.monotonic()))
                    if not events:
                        raise MatrixError(self.name + ' observer deadline')
                    if any(key.data == 'stop' for key, _ in events):
                        while True:
                            if time.monotonic() >= self.stop_deadline:
                                raise MatrixError(self.name + ' final drain deadline')
                            try:
                                chunk = os.read(self.fd, 65536)
                            except BlockingIOError:
                                break
                            if not chunk:
                                break
                            self.output.write(chunk)
                        return
                    if any(key.data == 'exit' for key, _ in events):
                        raise MatrixError(self.name + ' observer exited')
                    for key, _ in events:
                        if key.data == 'output':
                            try:
                                chunk = os.read(self.fd, 65536)
                            except BlockingIOError:
                                continue
                            if not chunk:
                                raise MatrixError(self.name + ' observer closed')
                            self.output.write(chunk)
            except BaseException as exc:
                self.drain_failure = str(exc) or 'observer drain failed'
                try:
                    os.write(self.failure_write, self.drain_failure.encode('utf-8', 'replace')[:4096])
                except OSError:
                    pass
        self.drain_thread = threading.Thread(target=drain, name=self.name + '-drain', daemon=True)
        self.drain_thread.start()
        return self.failure_read

    def stop_drain(self, timeout):
        if self.drain_thread is None:
            return
        self.stop_deadline = time.monotonic() + timeout
        os.write(self.stop_write, b'x')
        self.drain_thread.join(timeout=timeout)
        if self.drain_thread.is_alive():
            raise MatrixError(self.name + ' drain did not terminate')
        failure = self.drain_failure
        self.selector.unregister(self.stop_read)
        for fd in (self.stop_read, self.stop_write, self.failure_read, self.failure_write):
            os.close(fd)
        self.drain_thread = None
        if failure:
            raise MatrixError(failure)

    def close_observer(self, timeout=None):
        failure = None
        if self.drain_thread is not None:
            if timeout is None:
                raise MatrixError('observer drain timeout required')
            try:
                self.stop_drain(timeout)
            except MatrixError as exc:
                if self.drain_thread is not None:
                    raise
                failure = exc
        self.output.close()
        self.selector.close()
        os.close(self.pidfd)
        self.process.stdout.close()
        if failure is not None:
            raise failure


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

    Field supplies the recipient's own native-session reply naming the delivered
    RequestId. The caller binds that session to the observed private pane first.
    This is the accepted consumption witness for this release.
    """
    MAX_FRAME = 131072

    def __init__(self, root, peer_pidfd, identity, providers):
        self.root = Path(root)
        self.providers = providers
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
        self.consumed = set()
        self.minutes = {}
        self.invocations = set()
        self.closed_controls = set()
        self.close_attempts = set()

    def watch_observer_failure(self, fd):
        self.selector.register(fd, selectors.EVENT_READ, 'observer-failure')

    def unwatch_observer_failure(self, fd):
        self.selector.unregister(fd)

    def register_control(self, control_id, side):
        if not valid_request_id(control_id) or side not in ('sender', 'receiver') or control_id in self.controls or control_id in self.requests.values():
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
            if any(key.data == 'observer-failure' for key, _ in events):
                raise MatrixError('send observer drain failed')
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

    def review_rehearsals(self, hashes, deadline):
        """Retain an operator review of the two actual, dynamic receipts."""
        if set(hashes) != {'sender', 'receiver'} or any(
                not isinstance(value, str) or not re.fullmatch(r'[0-9a-f]{64}', value)
                for value in hashes.values()):
            raise MatrixError('invalid rehearsal receipt hashes')
        request = {'cut': 'rehearsal-review', 'sha256': hashes}
        self._retain('rehearsal-review-request.json', (json.dumps(request, sort_keys=True) + '\n').encode())
        frame = self._next_frame(deadline)
        self._retain('rehearsal-review-response.json', frame + b'\n')
        try:
            response = strict_json(frame)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('invalid rehearsal review') from exc
        if response != {'cut': 'rehearsal-review', 'sha256': hashes, 'decision': 'approved'}:
            raise MatrixError('exact rehearsal review not approved')

    def receive_admission(self, label, kind, marker, deadline, receipt_tokens):
        """Retain a sender receipt before asking the receiver to acknowledge it."""
        if KINDS.get(label) != kind or label in self.requests or not marker:
            raise MatrixError('invalid admission cut')
        frame = self._next_frame(deadline)
        index = self.counter
        self.counter += 1
        self._retain('%04d.admission.json' % index, frame + b'\n')
        try:
            event = strict_json(frame)
            if set(event) != {'cut', 'label', 'kind', 'marker', 'request_id', 'minutes', 'invocation', 'receipt', 'identity'} or event['cut'] != 'admission' or event['label'] != label or event['kind'] != kind or event['marker'] != marker or event['identity'] != self.identity['sender']:
                raise MatrixError('admission cut identity mismatch')
            request_id = event['request_id']
            if not valid_request_id(request_id) or request_id in self.requests.values() or request_id in self.controls:
                raise MatrixError('invalid or reused admission request')
            if kind == 'Task':
                if event['minutes'] != 15 or isinstance(event['minutes'], bool):
                    raise MatrixError('Task Minutes mismatch')
            elif event['minutes'] is not None:
                raise MatrixError('unexpected Minutes')
            call_bytes = self._source(event['invocation'])
            call = strict_json(call_bytes)
            native_bodies = {'O': 'P2-order-before: record this marker and its request id; give no Result.',
                             'Q': 'P2-question-before: keep unanswered until explicitly authorized in phase A.',
                             'N': 'P2-notice-before: record marker; no answer.',
                             'O2': 'P2-order-carry-excluded-7a97', 'Q2': 'P2-question-carry-required-7a97'}
            cli_requests = {'T': 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Task.{ 15 «P2-task-before: hold until phase A authorization.» } }',
                            'L': 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Living.{ «Proposal 2 isolated matrix» «P2-living-before: record this statement.» } }',
                            'T2': 'Send.{ { Mind proposalTwoReceiver Luna } Soft.Task.{ 15 «P2-task-carry-required-7a97» } }'}
            field = 'arguments' if label in native_bodies else 'command'
            expected_call = native_send('proposalTwoReceiver', kind, native_bodies[label]) if label in native_bodies else private_cli({'root': str(self.root), 'providers': self.providers}, cli_requests[label])
            if set(call) != {'call_id', field} or not valid_id(call['call_id']) or call['call_id'] in self.invocations or call[field] != expected_call:
                raise MatrixError('wrong or reused sender invocation')
            content = self._source(event['receipt'])
            text = content.decode('utf-8')
            if label in ('O', 'Q', 'N', 'O2', 'Q2'):
                payload = strict_json(text)
                items = payload['contentItems']
                if payload['success'] is not True or len(items) != 1 or items[0]['type'] != 'inputText':
                    raise MatrixError('invalid native tool admission')
                text = items[0]['text']
                if decode_native_acceptance(text, 'proposalTwoSender', 'proposalTwoReceiver', receipt_tokens) != request_id:
                    raise MatrixError('native send not accepted')
            elif parse_visible_admission(text, receipt_tokens) != request_id:
                raise MatrixError('CLI send request mismatch')
            boundary = r'(?<![A-Za-z0-9_-])' + re.escape(request_id) + r'(?![A-Za-z0-9_-])'
            if len(re.findall(boundary, text)) != 1:
                raise MatrixError('receipt does not bind request identity')
        except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('malformed admission evidence') from exc
        self._retain('%04d.admission.receipt' % index, content)
        self._retain('%04d.admission.invocation' % index, call_bytes)
        self.invocations.add(call['call_id'])
        self.requests[label] = request_id
        self.minutes[label] = event['minutes']
        return event

    def receive_consumption(self, label, marker, deadline):
        """Retain Field's captured own-session recipient reply naming this ID."""
        if label not in self.requests or label in self.consumed or not marker:
            raise MatrixError('consumption without an admission')
        frame = self._next_frame(deadline)
        index = self.counter
        self.counter += 1
        self._retain('%04d.consumption.json' % index, frame + b'\n')
        try:
            event = strict_json(frame)
            expected = {'cut', 'label', 'request_id', 'marker', 'identity', 'reply', 'transcript'}
            if set(event) != expected or event['cut'] != 'consumption' or event['label'] != label or event['request_id'] != self.requests[label] or event['marker'] != marker or event['identity'] != self.identity['receiver']:
                raise MatrixError('consumption cut identity mismatch')
            content = self._source(event['transcript'])
            lines = content.decode('utf-8').splitlines()
            reply = event['reply']
            boundary = r'(?<![A-Za-z0-9_-])' + re.escape(event['request_id']) + r'(?![A-Za-z0-9_-])'
            if not isinstance(reply, str) or reply not in lines or marker not in reply or not re.search(boundary, reply):
                raise MatrixError('recipient reply does not name marker and ID')
            if self.minutes[label] is not None and str(self.minutes[label]) not in reply:
                raise MatrixError('recipient reply does not attest Task Minutes')
        except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('malformed consumption evidence') from exc
        self._retain('%04d.consumption.transcript' % index, content)
        self.consumed.add(label)
        return event

    def receive_reply_outcome(self, label, surface, invocation, expected, deadline, receipt_tokens, answered_id=None):
        """Read Field-captured native/CLI invocation and its corresponding reply."""
        if surface not in ('native', 'cli') or expected not in ('unresolved', 'accepted', 'kept'):
            raise MatrixError('invalid reply outcome specification')
        frame = self._next_frame(deadline)
        index = self.counter
        self.counter += 1
        self._retain('%04d.outcome.json' % index, frame + b'\n')
        try:
            event = strict_json(frame)
            if set(event) != {'cut', 'label', 'surface', 'identity', 'invocation', 'response'} or event['cut'] != 'reply-outcome' or event['label'] != label or event['surface'] != surface or event['identity'] != self.identity['receiver']:
                raise MatrixError('reply outcome identity mismatch')
            call_bytes = self._source(event['invocation'])
            response_bytes = self._source(event['response'])
            call = strict_json(call_bytes)
            field = 'arguments' if surface == 'native' else 'command'
            if set(call) != {'call_id', field} or not valid_id(call['call_id']) or call['call_id'] in self.invocations or call[field] != invocation:
                raise MatrixError('wrong or reused invocation')
            response = response_bytes.decode('utf-8')
            if surface == 'native':
                payload = strict_json(response)
                items = payload['contentItems']
                if len(items) != 1 or items[0]['type'] != 'inputText' or payload['success'] is not (expected != 'unresolved'):
                    raise MatrixError('native outcome wrapper mismatch')
                response = items[0]['text']
            tokens = receipt_tokens(response)
            if expected == 'unresolved':
                wanted = 'Refused.Unresolved' if surface == 'native' else 'SendRefused.Unresolved'
                if tokens != [wanted]:
                    raise MatrixError('unresolved response mismatch')
            elif expected == 'accepted':
                if not valid_request_id(answered_id):
                    raise MatrixError('answered request ID missing')
                if surface == 'native':
                    if invocation.get('request') != answered_id:
                        raise MatrixError('native invocation answers another request')
                    admitted = decode_native_acceptance(response, 'proposalTwoReceiver', 'proposalTwoSender', receipt_tokens)
                else:
                    if decode_cli_done_request(invocation, receipt_tokens) != answered_id:
                        raise MatrixError('CLI invocation answers another request')
                    admitted = parse_visible_admission(response, receipt_tokens)
                if admitted != answered_id:
                    raise MatrixError('admitted reply answers another request')
            else:
                wanted = ['Kept.', '{', 'Sender.', '{', 'Mind', 'proposalTwoReceiver', 'Luna', '}', invocation['request'], '}'] if surface == 'native' else []
                values = [t[1] if isinstance(t, tuple) else t for t in tokens]
                if values != wanted:
                    raise MatrixError('kept response mismatch')
        except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('invalid reply outcome evidence') from exc
        self.invocations.add(call['call_id'])
        self._retain('%04d.outcome.invocation' % index, call_bytes)
        self._retain('%04d.outcome.response' % index, response_bytes)
        return response

    def receive_routed_consumption(self, label, request_id, marker, deadline):
        if label in self.consumed or not valid_request_id(request_id):
            raise MatrixError('invalid routed consumption cut')
        frame = self._next_frame(deadline)
        index = self.counter
        self.counter += 1
        self._retain('%04d.routed.json' % index, frame + b'\n')
        try:
            event = strict_json(frame)
            if set(event) != {'cut', 'label', 'request_id', 'marker', 'identity', 'reply', 'transcript'} or event['cut'] != 'routed-consumption' or event['label'] != label or event['request_id'] != request_id or event['marker'] != marker or event['identity'] != self.identity['sender']:
                raise MatrixError('routed consumption identity mismatch')
            content = self._source(event['transcript'])
            reply = event['reply']
            boundary = r'(?<![A-Za-z0-9_-])' + re.escape(request_id) + r'(?![A-Za-z0-9_-])'
            if not isinstance(reply, str) or reply not in content.decode('utf-8').splitlines() or marker not in reply or not re.search(boundary, reply):
                raise MatrixError('sender reply does not name routed request')
        except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('malformed routed consumption evidence') from exc
        self._retain('%04d.routed.transcript' % index, content)
        self.consumed.add(label)

    def receive_successor(self, flow_id, deadline):
        """Retain Field's first-prompt source and proposed private route."""
        frame = self._next_frame(deadline)
        index = self.counter
        self.counter += 1
        self._retain('%04d.successor.json' % index, frame + b'\n')
        try:
            event = strict_json(frame)
            if set(event) != {'cut', 'binding', 'first_prompt'} or event['cut'] != 'successor':
                raise MatrixError('invalid successor evidence cut')
            binding = event['binding']
            if set(binding) != {'flow_id', 'native_session', 'herdr_session', 'agent', 'pane', 'terminal'} or binding['flow_id'] != flow_id or any(not isinstance(v, str) or not v for v in binding.values()):
                raise MatrixError('invalid successor route')
            content = self._source(event['first_prompt'])
            prompt = content.decode('utf-8')
        except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('malformed successor evidence') from exc
        self._retain('%04d.first-prompt' % index, content)
        return binding, prompt

    def receive_successor_report(self, question_id, task_id, deadline):
        frame = self._next_frame(deadline)
        index = self.counter
        self.counter += 1
        self._retain('%04d.successor-report.json' % index, frame + b'\n')
        try:
            event = strict_json(frame)
            if set(event) != {'cut', 'identity', 'reply', 'transcript'} or event['cut'] != 'successor-report' or event['identity'] != self.identity['receiver']:
                raise MatrixError('wrong successor report identity')
            content = self._source(event['transcript'])
            reply = event['reply']
            if not isinstance(reply, str) or reply not in content.decode('utf-8').splitlines():
                raise MatrixError('successor report absent from transcript')
            for value in (question_id, task_id, 'P2-task-carry-required-7a97', '15'):
                if not re.search(r'(?<![A-Za-z0-9_-])' + re.escape(value) + r'(?![A-Za-z0-9_-])', reply):
                    raise MatrixError('successor report omits carry')
        except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('malformed successor report') from exc
        self._retain('%04d.successor-report.transcript' % index, content)

    def receive_control_completion(self, request_id, side, deadline, receipt_tokens):
        """Require the actual native Kept result before reading Answer once."""
        if self.controls.get(request_id) != side or request_id in self.closed_controls:
            raise MatrixError('invalid control completion cut')
        frame = self._next_frame(deadline)
        index = self.counter
        self.counter += 1
        self._retain('%04d.control-completion.json' % index, frame + b'\n')
        try:
            event = strict_json(frame)
            if set(event) != {'cut', 'request_id', 'side', 'identity', 'invocation', 'response'} or event['cut'] != 'control-completion' or event['request_id'] != request_id or event['side'] != side or event['identity'] != self.identity[side]:
                raise MatrixError('wrong control completion identity')
            call_bytes = self._source(event['invocation'])
            response_bytes = self._source(event['response'])
            call = strict_json(call_bytes)
            args = call['arguments']
            if set(call) != {'call_id', 'arguments'} or not valid_id(call['call_id']) or call['call_id'] in self.invocations or args.get('kind') != 'Result' or args.get('request') != request_id:
                raise MatrixError('wrong or reused control Result invocation')
            payload = strict_json(response_bytes)
            items = payload['contentItems']
            if payload['success'] is not True or len(items) != 1 or items[0]['type'] != 'inputText':
                raise MatrixError('control Result not kept')
            topic = 'proposalTwoSender' if side == 'sender' else 'proposalTwoReceiver'
            tokens = [t[1] if isinstance(t, tuple) else t for t in receipt_tokens(items[0]['text'])]
            if tokens != ['Kept.', '{', 'Sender.', '{', 'Mind', topic, 'Luna', '}', request_id, '}']:
                raise MatrixError('control Kept sender or ID mismatch')
        except (KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise MatrixError('invalid control completion evidence') from exc
        self.invocations.add(call['call_id'])
        self._retain('%04d.control-completion.invocation' % index, call_bytes)
        self._retain('%04d.control-completion.response' % index, response_bytes)

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
                'minutes', 'receipt', 'transcript', 'acknowledgement', 'identity',
                'reader_side', 'reader_identity'}
        if not isinstance(event, dict) or set(event) != keys:
            raise MatrixError('evidence event has wrong fields')
        expected = self.expected[0]
        if any(event[key] != value for key, value in expected.items()):
            raise MatrixError('out-of-order, wrong-side or wrong-kind evidence')
        request_id = event['request_id']
        if not valid_request_id(request_id) or request_id in self.requests.values() or request_id in self.controls:
            raise MatrixError('invalid or previously used request ID')
        if event['identity'] != self.identity.get(event['side']):
            raise MatrixError('pane/session/process identity does not match observed cut')
        if event['reader_side'] != 'receiver' or event['reader_identity'] != self.identity.get('receiver'):
            raise MatrixError('acknowledgement is not bound to receiver identity')
        minutes_value = event['minutes']
        if event['kind'] == 'Task':
            if minutes_value != 15 or isinstance(minutes_value, bool):
                raise MatrixError('Task Minutes mismatch')
        elif minutes_value is not None:
            raise MatrixError('unexpected Minutes on non-Task')
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
                payload = strict_json(receipt_text)
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
        if event['kind'] == 'Task' and str(minutes_value) not in transcript_text:
            raise MatrixError('Task Minutes absent from retained transcript')
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
    if set(ids) != set(required) or any(not valid_request_id(ids[k]) for k in required) or len(set(ids.values())) != len(ids):
        raise MatrixError('distinct captured phase A IDs and reviewed unknown ID required')
    target = 'proposalTwoSender'
    wrong_order = native_send(target, 'Result', 'P2-result-order-refusal', ids['O'])
    wrong_task = native_send(target, 'Result', 'P2-result-task-refusal', ids['T'])
    unknown = native_send(target, 'Result', 'P2-result-unknown-refusal', ids['unknown'])
    result = native_send(target, 'Result', 'P2-result-before', ids['Q'])
    bad_done = private_cli(manifest, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ ' + ids['Q'] + ' «P2-done-question-refusal» } }')
    good_done = private_cli(manifest, 'Send.{ { Mind proposalTwoSender Luna } Soft.Done.{ ' + ids['T'] + ' «P2-done-before» } }')
    return ('Use only Mind/proposalTwoSender/Luna and Mind/proposalTwoReceiver/Luna. '
            'Report the exact marker and original ID for each O, Q, T, N and L you read, and the Task Minutes. '
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
            '. Return all actual receipts and IDs. '
            'Close this instruction Question with a Result.')


def render_successor_inspect(ids):
    if set(ids) != {'Q2', 'T2'} or any(not valid_request_id(v) for v in ids.values()):
        raise MatrixError('captured carry IDs required')
    return ('Report the original carried Question and Task IDs, Task Minutes and Task text. '
            'Keep both unanswered and finish this instruction Question with a Result.')


def render_successor(manifest, ids):
    required = ('O2', 'Q2', 'T2')
    if set(ids) != set(required) or any(not valid_request_id(ids[k]) for k in required) or len(set(ids.values())) != len(ids):
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
            'and report the Task Minutes. Keep the Question and Task unanswered. '
            'This is a Notice and requires no Result.')


def render_kept_answer(request_id):
    if not valid_request_id(request_id):
        raise MatrixError('captured unbound Question ID required')
    reply = native_send('proposalTwoSender', 'Result', 'P2-kept-answer', request_id)
    return ('First report that you read P2-kept-question with RequestId ' + request_id + '. '
            'Answer the unbound operator Question by invoking your native send tool exactly once with '
            + json.dumps(reply) + '. Return the actual typed response, then close this instruction Question with a Result.')


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


def herdr_json(owner, label, arguments):
    """Retain one exact private-session Herdr reply before decoding it."""
    evidence = Path(owner.manifest['root']) / 'evidence'
    command = [owner.manifest['providers']['herdr']['path'], '--session', owner.manifest['session'], *arguments]
    process = owner.command(label, command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    for suffix, data in (('.command.json', (json.dumps(command) + '\n').encode()),
                         ('.stdout', output), ('.stderr', error)):
        fd = os.open(evidence / (label + suffix), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
    if process.returncode:
        raise MatrixError(label + ' Herdr command failed')
    try:
        return strict_json(output)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MatrixError(label + ' invalid Herdr JSON') from exc


def snapshot_native(owner, side, binding, label=None):
    if side not in ('sender', 'receiver') or not all(binding.get(k) for k in ('pane', 'terminal', 'native_session')):
        raise MatrixError('incomplete native binding')
    pane = binding['pane']
    label = label or side
    if not valid_id(label):
        raise MatrixError('invalid snapshot label')
    listed = herdr_json(owner, label + '-agent-list', ['agent', 'list'])
    selected = herdr_json(owner, label + '-agent-get', ['agent', 'get', pane])
    processes = herdr_json(owner, label + '-process-info', ['pane', 'process-info', '--pane', pane])
    info = identity_binding(listed, selected, processes, binding)
    if selected['result']['agent']['terminal_id'] != binding['terminal']:
        raise MatrixError('terminal identity differs from captured launch')
    return info


def close_bound_flow_and_pane(owner, side, binding, private_call, receipt):
    """Capture the pane, close Flow, then reconcile the private pane inventory."""
    snapshot_native(owner, side, binding, label=side + '-before-close')
    close_flow(owner, binding['flow_id'], private_call, receipt)
    listed = herdr_json(owner, side + '-post-close-list', ['pane', 'list'])
    try:
        if listed['id'] != 'cli:pane:list' or listed['result']['type'] != 'pane_list':
            raise MatrixError('invalid post-close inventory')
        remaining = [row for row in listed['result']['panes'] if row.get('pane_id') == binding['pane']]
    except (KeyError, TypeError) as exc:
        raise MatrixError('incomplete post-close inventory') from exc
    if not remaining:
        return
    if len(remaining) != 1 or remaining[0].get('terminal_id') != binding['terminal']:
        raise MatrixError('post-close pane no longer has the captured identity')
    current = herdr_json(owner, side + '-post-close-agent', ['agent', 'get', binding['pane']])
    try:
        if current['id'] != 'cli:agent:get' or current['result']['type'] != 'agent_info' or not bound_agent_matches(current['result']['agent'], binding):
            raise MatrixError('post-close native session changed')
    except (KeyError, TypeError) as exc:
        raise MatrixError('post-close native session unavailable') from exc
    reply = herdr_json(owner, side + '-pane-close', ['pane', 'close', binding['pane']])
    if reply != {'id': 'cli:pane:close', 'result': {'type': 'ok'}}:
        raise MatrixError('pane close did not return typed success')
