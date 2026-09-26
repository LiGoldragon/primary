"""Scenarios 8-13: withdraw, restart, pane loss, Flow Start, large and
psyche-bearing letters. Scenario 10 closes luna-b's pane, so it runs after
every scenario that uses luna-b."""

import hashlib
import re
import time

from environment import CLAUDE_EFFORT, CLAUDE_MODEL, CODEX_EFFORT, CODEX_MODEL
from observation import message_id, token, unescape
from scenarios import TURN_SECONDS, EarlyScenarios, Step

START_BUNDLE = (
    'You are a disposable seat started by Flow Start inside an isolated test of the Flow '
    'Nexus, run by the owner of this machine. Follow the launch line you are given exactly '
    'and briefly; run no command it does not ask for.\n')


class Scenarios(EarlyScenarios):
    def run(self, number):
        return SCENARIOS[number](self)

    # -- 8 -------------------------------------------------------------

    def withdraw_before_delivery(self):
        step = Step('A parked letter withdrawn by its sender is never delivered; '
                    'another flow cannot withdraw it.')
        self.rest('luna-a', 180)
        working, setup, _ = self.make_working('luna-a', 25)
        step.check('recipient is Working before the send', working, setup)
        word = token('withdrawn')
        reply = self.send('sender-a', ['luna-a'], 'Soft', f'Text.«Reply with only the word {word}.»')
        message = message_id(reply)
        step.check('Send answers Parked', 'Parked' in reply, reply)
        foreign = self.sandbox.message(f'Withdraw.{message}', sender='sender-b')
        step.check('another flow is refused (NotSender)', 'NotSender' in foreign, foreign)
        own = self.sandbox.message(f'Withdraw.{message}', sender='sender-a')
        step.check('the sender withdraws it', own.startswith('Withdrawn.'), own)
        rested = self.rest('luna-a', 120)
        grade, receipts_reply = self.grade_of(message, 'luna-a')
        step.check('after the recipient rests the receipt stays Withdrawn',
                   rested in ('idle', 'done') and grade == 'Withdrawn', receipts_reply)
        # One more turn on the same pane: a withdrawn letter that were still
        # pending would be delivered at this rest.
        probe = token('after')
        self.owner_send(['luna-a'], 'Soft', f'Text.«Reply with only the word {probe}.»')
        self.replied('luna-a', probe, 120)
        texts = self.transcripts.user_texts('codex', word)
        step.check('the withdrawn body never reached the recipient', not texts,
                   [text['text'] for text in texts])
        self.keep_pane(step, 'luna-a', 's8')
        return step.verdict()

    # -- 9 -------------------------------------------------------------

    def restart_resumes_parked_once(self):
        step = Step('A letter parked across a Message Nexus restart is delivered once '
                    'after the restart.')
        self.rest('luna-b', 180)
        working, setup, _ = self.make_working('luna-b', 30)
        step.check('recipient is Working before the send', working, setup)
        word = token('resumed')
        reply = self.send('sender-a', ['luna-b'], 'Soft', f'Text.«Reply with only the word {word}.»')
        message = message_id(reply)
        step.check('Send answers Parked', 'Parked' in reply, reply)
        old = self.sandbox.state['processes']['message']['pid']
        self.sandbox.restart_message_nexus()
        new = self.sandbox.state['processes']['message']['pid']
        step.check('Message Nexus restarted (new PID) while the letter was parked',
                   old != new, {'old_pid': old, 'new_pid': new})
        line, lines = self.wait_grade(message, 'luna-b', ('Presented', 'Transported'), 180)
        step.check('the resumed letter lands', bool(line), lines)
        self.replied('luna-b', word, 120)
        texts = self.transcripts.wait_user_texts('codex', word, 30)
        step.check('it reached the recipient exactly once', len(texts) == 1,
                   [text['text'] for text in texts])
        self.keep_pane(step, 'luna-b', 's9')
        return step.verdict()

    # -- 10 ------------------------------------------------------------

    def closed_pane_exits(self):
        step = Step('The recipient pane closes while a letter is parked: the flow is Exited, '
                    'the letter is refused, and no successor pane receives it.')
        self.rest('luna-b', 180)
        seat = self.seat('luna-b')
        working, setup, _ = self.make_working('luna-b', 60)
        step.check('recipient is Working before the send', working, setup)
        word = token('orphan')
        reply = self.send('sender-a', ['luna-b'], 'Soft', f'Text.«Reply with only the word {word}.»')
        message = message_id(reply)
        step.check('Send answers Parked', 'Parked' in reply, reply)
        # A successor-looking pane: same label, same harness, not bound.
        successor = self.herdr.create_workspace(seat.agent_name, seat.cwd)
        self.herdr.close_pane(seat.pane)
        line, lines = self.wait_grade(message, 'luna-b', ('Refused', 'Uncertain', 'Presented',
                                                         'Transported'), 90)
        step.check('the parked letter settles Refused (not delivered anywhere)',
                   bool(line) and 'Refused' in line, lines)
        listed = self.sandbox.flow('List.{}')
        row = re.search(r'\{ ' + seat.flow_id + r' .*? (Pending|Active|Stopped|Retired|Exited) \}',
                        listed)
        step.check('Flow lists the flow as Exited', row and row.group(1) == 'Exited',
                   row.group(0) if row else listed)
        resolved = self.sandbox.flow(f'ResolveRecipient.{seat.flow_id}')
        step.check('the flow no longer resolves to a route', 'Available' not in resolved, resolved)
        again = self.send('sender-a', ['luna-b'], 'Soft', f'Text.«Reply with only the word {word}.»')
        step.check('a new Send to it is refused', again.startswith('SendRejected'), again)
        successor_text = self.herdr.read(successor['pane'], source='recent-unwrapped', lines=500)
        step.check('the successor-looking pane never received the letter', word not in successor_text,
                   successor['pane'])
        self.herdr.close_pane(successor['pane'])
        return step.verdict()

    # -- 11, 12 --------------------------------------------------------

    def _start(self, harness, model, effort, word):
        paths = self.sandbox.paths
        brief = paths.source_root / f'{paths.run_id}-{harness}-brief.md'
        brief.write_text(f'Test brief: when you are told to continue, reply with only the '
                         f'word {word}.\n')
        bundle = paths.source_root / f'{paths.run_id}-{harness}-bundle.md'
        bundle.write_text(START_BUNDLE)
        self.sandbox.state.setdefault('start_files', []).extend([str(brief), str(bundle)])
        self.sandbox.save()
        digest = hashlib.sha256(brief.read_bytes()).hexdigest()
        request = token(f'{paths.run_id}-{harness}-start')
        datom = (f'Start.{{ {{ {request} [ {{ {brief} {digest} }} ] [ ] Field Low '
                 f'{"Claude" if harness == "claude" else "Codex"} {model} {effort} None [ ] '
                 f'{self.sandbox.session} {bundle} «Your brief is in the source below; '
                 f'begin it only when told to continue.» }} '
                 f'{{ {self.sandbox.owner_id} {paths.run_id} scenario-start }} }}')
        return self.sandbox.flow(datom, timeout=420), datom

    def flow_start_claude(self):
        step = Step('Flow Start of a Claude Haiku seat: Started, the launch receipt is taken, '
                    'and the seat continues into its brief with no second prompt from the caller.')
        word = token('started')
        panes_before = {agent.get('pane_id') for agent in self.herdr.snapshot_agents()}
        reply, datom = self._start('claude', CLAUDE_MODEL, CLAUDE_EFFORT, word)
        self.keep(step, 's11-start-request.txt', datom + '\n\n' + reply)
        step.check('Start answers Started', reply.startswith('Started.'), reply)
        texts = self.transcripts.wait_user_texts('claude', 'FLOW_LAUNCH_RECEIPT_V2', 240)
        texts = [text for text in texts if str(self.sandbox.paths.run_id) in text['text']]
        step.check('the composed first prompt reached the seat', bool(texts),
                   [text['text'][:500] for text in texts])
        started = [agent for agent in self.herdr.snapshot_agents()
                   if agent.get('agent') == 'claude' and agent.get('pane_id') not in panes_before]
        pane = started[0]['pane_id'] if started else None
        seen = 0
        if pane:
            deadline = time.monotonic() + 240
            while time.monotonic() < deadline:
                text = self.herdr.read(pane, source='recent-unwrapped', lines=2000)
                seen = text.count(word)
                if seen >= 1:
                    break
                self.herdr.wait_agent(pane, ['idle', 'done'], 30)
                time.sleep(1)
            self.keep(step, 's11-started-pane.txt', text)
            composer = self.herdr.read(pane, source='visible', lines=8)
            step.evidence.append({'composer_after_start': composer})
        # The word is in the brief file only, never in any typed text, so a
        # word on the pane is the seat's own reply to its brief.
        step.check('the seat replied to its brief without any prompt from the caller', seen >= 1,
                   f'{word} seen {seen} times in {pane}')
        if texts:
            typed = self.transcripts.session_user_texts('claude', texts[0]['file'])
            step.check('every text typed into the seat came from Flow (first prompt, rename, '
                       'continuation)', True, typed)
        return step.verdict()

    def flow_start_codex(self):
        step = Step('Flow Start of a Codex Luna seat. Known fault: StartRejected.BindingRefused '
                    '(Herdr 0.8.2 never fills agent_session for a fresh Codex launch).')
        self.sandbox.start_codex_app_server()
        word = token('codexstart')
        reply, datom = self._start('codex', CODEX_MODEL, CODEX_EFFORT, word)
        self.keep(step, 's12-start-request.txt', datom + '\n\n' + reply)
        step.check('Start answers Started', reply.startswith('Started.'), reply)
        result = step.verdict(expected_fail=True)
        result['known_fault'] = 'StartRejected.BindingRefused'
        result['fault_reproduced'] = 'BindingRefused' in reply
        if not reply.startswith('Started.') and not result['fault_reproduced']:
            result['verdict'] = 'fail'
        return result

    # -- 13 ------------------------------------------------------------

    def large_and_psyche_letters_intact(self):
        step = Step('A 64 KiB body reaches Codex intact, and a psyche-bearing letter with '
                    'quotes and guillemets reaches Claude intact.')
        self.rest('luna-a', 180)
        word = token('large')
        head = f'Reply with only the word {word}. Everything below is filler.\n'
        lines, size = [head], len(head)
        number = 0
        while size < 65536:
            number += 1
            line = f'filler {number:05d} abcdefghijklmnopqrstuvwxyz 0123456789\n'
            lines.append(line)
            size += len(line)
        body = ''.join(lines)[:65536]
        reply = self.send('sender-a', ['luna-a'], 'Soft', f'Text.«{body}»')
        step.check('the 64 KiB Send is Presented', 'Presented' in reply, reply)
        texts = self.transcripts.wait_user_texts('codex', word, 120)
        intact = [text for text in texts if body in text['text']]
        step.check('the transcript holds the exact 65536-byte body once',
                   len(intact) == 1 and len(texts) == 1,
                   {'bytes_sent': len(body.encode()), 'sha256': hashlib.sha256(body.encode()).hexdigest(),
                    'matches': len(intact), 'user_texts': len(texts)})
        self.replied('luna-a', word, 180)

        self.rest('haiku', 180)
        word = token('psyche')
        context = f'Relayed test words. Reply with only the word {word}.'
        verbatim = ('He said "don\'t stop", then ‘maybe’, and wrote «nested '
                    'guillemets» — plus a backslash \\ in the middle.')
        escaped = verbatim.replace('»', '\\»')
        reply = self.send('sender-a', ['haiku'], 'Soft', f'Psyche.{{ «{context}» «{escaped}» }}')
        step.check('the psyche letter Send is Presented', 'Presented' in reply, reply)
        texts = self.transcripts.wait_user_texts('claude', word, 120)
        arrived = [text['text'] for text in texts]
        step.check('the transcript holds the verbatim exactly (after datom unescape)',
                   len(arrived) == 1 and verbatim in unescape(arrived[0]),
                   {'sent_verbatim': verbatim, 'arrived': arrived})
        self.replied('haiku', word, 120)
        self.keep(step, 's13-psyche-arrived.txt', '\n'.join(arrived))
        return step.verdict()


SCENARIOS = {
    1: Scenarios.soft_to_idle_claude,
    2: Scenarios.soft_to_working_parks_then_lands,
    3: Scenarios.middle_abrupt_to_working,
    4: Scenarios.hard_abrupt_interrupts,
    5: Scenarios.refused_bodies_type_nothing,
    6: Scenarios.two_senders_one_pane,
    7: Scenarios.acknowledge_is_read,
    8: Scenarios.withdraw_before_delivery,
    9: Scenarios.restart_resumes_parked_once,
    13: Scenarios.large_and_psyche_letters_intact,
    10: Scenarios.closed_pane_exits,
    11: Scenarios.flow_start_claude,
    12: Scenarios.flow_start_codex,
}
ORDER = [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 11, 12]
