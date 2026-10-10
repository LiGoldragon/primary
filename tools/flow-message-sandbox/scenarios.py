"""The scenarios. Each returns a verdict with what was expected, what was
observed, and the evidence behind it.

Verdicts: pass, fail, expected-fail (a known fault reproduced), error (the
harness itself failed; recorded by the runner).

Seats: haiku (Claude recipient), luna-a and luna-b (Codex recipients),
sender-a and sender-b (idle Codex seats whose panes the senders speak from).
Model use is kept to one short turn per step.
"""

import time

from observation import Transcripts, evidence_file, message_id, receipts, token

REST = ('idle', 'done')
TURN_SECONDS = 150


class Step:
    """One scenario's record: checks with their observations."""

    def __init__(self, expected):
        self.expected = expected
        self.checks = []
        self.evidence = []

    def check(self, name, passed, observed):
        self.checks.append({'check': name, 'passed': bool(passed), 'observed': observed})
        return passed

    def verdict(self, expected_fail=False):
        passed = all(check['passed'] for check in self.checks)
        if expected_fail:
            verdict = 'expected-fail' if not passed else 'pass'
        else:
            verdict = 'pass' if passed else 'fail'
        return {'verdict': verdict, 'expected': self.expected, 'checks': self.checks,
                'evidence': self.evidence}


class EarlyScenarios:
    def __init__(self, sandbox):
        self.sandbox = sandbox
        self.herdr = sandbox.herdr
        self.transcripts = Transcripts(since=sandbox.state.get('started_at', time.time() - 3600))

    # -- helpers ---------------------------------------------------------

    def seat(self, name):
        return self.sandbox.seat(name)

    def send(self, sender, recipients, priority, content):
        ids = ' '.join(self.seat(name).flow_id for name in recipients)
        return self.sandbox.message(f'Send.{{ [ {ids} ] {priority} {content} }}', sender=sender)

    def owner_send(self, recipients, priority, content):
        ids = ' '.join(self.seat(name).flow_id for name in recipients)
        return self.sandbox.message_meta(f'Send.{{ [ {ids} ] {priority} {content} }}')

    def observe(self, message):
        from processes import Stream
        return Stream(self.sandbox.client.spawn('message', f'Observe.{message}'))

    def grade_of(self, message, recipient):
        reply = self.sandbox.message(f'QueryReceipts.{message}')
        return receipts(reply).get(self.seat(recipient).flow_id, (None, None))[1], reply

    def wait_grade(self, message, recipient, wanted, timeout_seconds=TURN_SECONDS):
        """Waits on the receipt subscription for one of the wanted grades."""
        flow_id = self.seat(recipient).flow_id
        stream = self.observe(message)
        try:
            line = stream.until(
                lambda line: receipts(line).get(flow_id, (None, ''))[1].split('.')[0] in wanted,
                timeout_seconds)
            return line, stream.lines
        finally:
            stream.close()

    def make_working(self, recipient, seconds):
        """The recipient starts a turn that stays Working for `seconds`."""
        marker = token('busy')
        # In the foreground: Claude otherwise moves a long command to the
        # background and ends its turn, and the recipient is no longer working.
        reply = self.owner_send([recipient], 'Soft', f'Text.«Run the shell command sleep {seconds} '
                                f'in the foreground (never in the background) and wait for it to '
                                f'finish, then reply with only the word {marker}.»')
        status = self.herdr.wait_agent(self.seat(recipient).pane, ['working'], 60)
        return status == 'working', reply, marker

    def rest(self, recipient, timeout_seconds=TURN_SECONDS):
        return self.herdr.wait_agent(self.seat(recipient).pane, list(REST), timeout_seconds)

    def pane(self, recipient):
        return self.herdr.read(self.seat(recipient).pane, source='recent-unwrapped', lines=3000)

    def replied(self, recipient, word, timeout_seconds=TURN_SECONDS):
        """The recipient's own reply carries the word (the letter carries it once)."""
        deadline = time.monotonic() + timeout_seconds
        while True:
            count = self.pane(recipient).count(word)
            if count >= 2 or time.monotonic() > deadline:
                return count
            self.herdr.wait_agent(self.seat(recipient).pane, list(REST), 20)
            time.sleep(1)

    def keep(self, step, name, text):
        step.evidence.append(evidence_file(self.sandbox.paths.evidence, name, text))

    def keep_pane(self, step, recipient, label):
        self.keep(step, f'{label}-{recipient}-pane.txt', self.pane(recipient))

    # -- 1 -------------------------------------------------------------

    def soft_to_idle_claude(self):
        step = Step('Soft to an idle Haiku is Presented and the recipient replies.')
        word = token('pong')
        self.rest('haiku', 60)
        reply = self.send('sender-a', ['haiku'], 'Soft', f'Text.«Reply with only the word {word}.»')
        grade = receipts(reply).get(self.seat('haiku').flow_id, (None, None))[1]
        step.check('Send answers Presented', grade == 'Presented', reply)
        count = self.replied('haiku', word)
        step.check('the recipient replies with the word', count >= 2, f'{word} seen {count} times')
        self.keep_pane(step, 'haiku', 's1')
        return step.verdict()

    # -- 2 -------------------------------------------------------------

    def soft_to_working_parks_then_lands(self):
        step = Step('Soft to a working Luna is Parked, then lands once it rests.')
        working, setup, _ = self.make_working('luna-a', 25)
        step.check('recipient is Working before the send', working, setup)
        word = token('parked')
        reply = self.send('sender-a', ['luna-a'], 'Soft', f'Text.«Reply with only the word {word}.»')
        message = message_id(reply)
        grade = receipts(reply).get(self.seat('luna-a').flow_id, (None, None))[1]
        step.check('Send answers Parked', grade == 'Parked', reply)
        line, lines = self.wait_grade(message, 'luna-a', ('Presented', 'Transported'))
        step.check('the parked letter lands on rest (Presented)', line and 'Presented' in line,
                   lines)
        count = self.replied('luna-a', word)
        step.check('the recipient replies with the word', count >= 2, f'{word} seen {count} times')
        texts = self.transcripts.wait_user_texts('codex', word, 30)
        step.check('the letter reached the recipient exactly once', len(texts) == 1,
                   [text['text'] for text in texts])
        self.keep_pane(step, 'luna-a', 's2')
        return step.verdict()

    # -- 3 -------------------------------------------------------------

    def middle_abrupt_to_working(self):
        step = Step('MiddleAbrupt reaches a working Codex (steer) and a working Claude '
                    'without parking, and each replies.')
        for recipient, harness in (('luna-a', 'codex'), ('haiku', 'claude')):
            self.rest(recipient, 90)
            working, setup, _ = self.make_working(recipient, 25)
            step.check(f'{recipient} is Working before the send', working, setup)
            word = token('steer')
            status = self.herdr.agent_status(self.seat(recipient).pane)
            step.check(f'{recipient} is still Working at the send', status == 'working', status)
            reply = self.send('sender-a', [recipient], 'MiddleAbrupt',
                              f'Text.«Reply with only the word {word}.»')
            grade = receipts(reply).get(self.seat(recipient).flow_id, (None, None))[1]
            step.check(f'{recipient}: Send answers Presented or Transported, not Parked',
                       grade in ('Presented', 'Transported'), reply)
            count = self.replied(recipient, word, 180)
            step.check(f'{recipient}: replies with the word', count >= 2,
                       f'{word} seen {count} times')
            self.keep_pane(step, recipient, 's3')
        return step.verdict()

    # -- 4 -------------------------------------------------------------

    def hard_abrupt_interrupts(self):
        step = Step('HardAbrupt interrupts a working Codex and a working Claude '
                    '(InterruptWitness Observed) and each replies.')
        for recipient in ('luna-a', 'haiku'):
            self.rest(recipient, 180)
            working, setup, busy = self.make_working(recipient, 90)
            step.check(f'{recipient} is Working before the send', working, setup)
            word = token('halt')
            status = self.herdr.agent_status(self.seat(recipient).pane)
            step.check(f'{recipient} is still Working at the send', status == 'working', status)
            started = time.monotonic()
            reply = self.owner_send([recipient], 'HardAbrupt',
                                    f'Text.«Stop what you are doing and reply with only the word {word}.»')
            witness, grade = receipts(reply).get(self.seat(recipient).flow_id, (None, None))
            step.check(f'{recipient}: interrupt witness Observed', witness == 'Observed', reply)
            step.check(f'{recipient}: delivered (Presented or Transported)',
                       grade in ('Presented', 'Transported'), reply)
            count = self.replied(recipient, word, 120)
            elapsed = time.monotonic() - started
            step.check(f'{recipient}: replies with the word before the 90 s sleep would end',
                       count >= 2 and elapsed < 85, f'{word} seen {count} times after {elapsed:.0f} s')
            self.keep_pane(step, recipient, 's4')
        return step.verdict()

    # -- 5 -------------------------------------------------------------

    def refused_bodies_type_nothing(self):
        step = Step('A /compact body, a ! shell body, and ESC and CR bytes are refused '
                    'at Send and nothing is typed.')
        self.rest('haiku', 90)
        before = self.pane('haiku')
        bodies = {
            'compact': ('/compact {}', 'HarnessCommand'),
            'shell': ('!echo {}', 'HarnessCommand'),
            'escape': ('echo {} \x1b[2J', 'ControlCharacter'),
            'carriage-return': ('first {}\rsecond', 'ControlCharacter'),
        }
        markers = []
        for name, (template, refusal) in bodies.items():
            marker = token(name)
            markers.append(marker)
            reply = self.send('sender-a', ['haiku'], 'Soft', f'Text.«{template.format(marker)}»')
            step.check(f'{name}: SendRejected.BodyRefused {refusal}',
                       reply.startswith('SendRejected.BodyRefused') and refusal in reply, reply)
        after = self.pane('haiku')
        typed = [marker for marker in markers if marker in after]
        step.check('no refused body reached the pane', not typed,
                   {'markers_in_pane': typed, 'pane_text_unchanged': before.strip() == after.strip()})
        vet = self.sandbox.flow_meta(
            f'Vet.{{ v-{token("vet")} {self.seat("haiku").flow_id} '
            f'Soft.{{ m-0 Owner Text.«/compact» }} }}')
        step.check("Flow's own Vet refuses the same body", 'HarnessCommand' in vet, vet)
        return step.verdict()

    # -- 6 -------------------------------------------------------------

    def two_senders_one_pane(self):
        step = Step('Two senders to one pane at once: the lease serializes; one is typed, '
                    'the other waits (Parked) and lands whole, never interleaved.')
        self.rest('luna-b', 90)
        words = {'sender-a': token('first'), 'sender-b': token('second')}
        processes = {sender: self.sandbox.spawn_message(
            f'Send.{{ [ {self.seat("luna-b").flow_id} ] Soft Text.«Reply with only the word {word}.» }}',
            sender=sender) for sender, word in words.items()}
        replies = {sender: process.communicate(timeout=120)[0].strip()
                   for sender, process in processes.items()}
        grades = {sender: receipts(reply).get(self.seat('luna-b').flow_id, (None, None))[1]
                  for sender, reply in replies.items()}
        step.check('both Sends were accepted', all(grades.values()), replies)
        step.check('at most one was typed at once; the other waited',
                   sorted(grades.values()) in (['Parked', 'Presented'], ['Parked', 'Transported'],
                                               ['Presented', 'Presented'], ['Presented', 'Transported']),
                   grades)
        for sender, reply in replies.items():
            if grades[sender] == 'Parked':
                line, lines = self.wait_grade(message_id(reply), 'luna-b', ('Presented', 'Transported'))
                step.check(f'{sender}: the waiting letter lands', bool(line), lines)
        for sender, word in words.items():
            texts = self.transcripts.wait_user_texts('codex', word, 90)
            other = words['sender-b' if sender == 'sender-a' else 'sender-a']
            whole = [text for text in texts
                     if f'Reply with only the word {word}.»' in text['text'] and other not in text['text']]
            step.check(f'{sender}: its letter arrived once, whole and alone', len(whole) == 1 and len(texts) == 1,
                       [text['text'] for text in texts])
        self.rest('luna-b', TURN_SECONDS)
        self.keep_pane(step, 'luna-b', 's6')
        return step.verdict()

    # -- 7 -------------------------------------------------------------

    def acknowledge_is_read(self):
        step = Step('The recipient acknowledges with the MessageId the letter carries; '
                    'the receipt becomes Read.')
        self.rest('haiku', 90)
        word = token('ack')
        reply = self.send('sender-a', ['haiku'], 'Soft',
                          "Text.«Run this shell command, with ID replaced by this letter's MessageId "
                          "(the m- token right after the opening brace): message 'Acknowledge.ID' "
                          f"-- then reply with only the word {word}.»")
        message = message_id(reply)
        step.check('Send answers Presented', 'Presented' in reply, reply)
        line, lines = self.wait_grade(message, 'haiku', ('Read',), 180)
        step.check('the receipt becomes Read', bool(line), lines)
        count = self.replied('haiku', word, 60)
        step.check('the recipient replies with the word', count >= 2, f'{word} seen {count} times')
        foreign = self.sandbox.message(f'Acknowledge.{message}', sender='sender-b')
        step.check('a flow that is not a recipient cannot acknowledge it', 'NotRecipient' in foreign, foreign)
        self.keep_pane(step, 'haiku', 's7')
        return step.verdict()
