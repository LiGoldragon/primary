"""The run's own record: results.json (everything) and results.md (the table)."""

import json

TITLES = {
    '1': 'Soft to idle Haiku: Presented, reply',
    '2': 'Soft to working Luna: Parked, lands on rest',
    '3': 'MiddleAbrupt to working Codex (steer) and Claude',
    '4': 'HardAbrupt interrupt, Codex and Claude',
    '5': '/compact, ! shell, ESC, CR bodies refused, nothing typed',
    '6': 'Two senders, one pane: lease serializes',
    '7': 'Acknowledge by MessageId: Read',
    '8': 'Withdraw before delivery',
    '9': 'Message Nexus restart with a parked letter: resumes once',
    '10': 'Recipient pane closed mid-delivery: Exited, no successor',
    '11': 'Flow Start of a Claude Haiku seat continues into its brief',
    '12': 'Flow Start of a Codex seat (known BindingRefused)',
    '13': '64 KiB body and psyche letter arrive intact',
}


class Report:
    def __init__(self, sandbox):
        self.sandbox = sandbox

    def rows(self):
        results = self.sandbox.state.get('results', {})
        for number in sorted(results, key=int):
            result = results[number]
            failed = [check['check'] for check in result.get('checks', []) if not check['passed']]
            note = result.get('error') or ('; '.join(failed) if failed else '')
            yield number, TITLES.get(number, ''), result['verdict'], note

    def markdown(self):
        state = self.sandbox.state
        lines = [f'# Flow/Message sandbox run {state["run_id"]}', '',
                 f'Flow {state["pins"]["flow_revision"]}, Message {state["pins"]["message_revision"]}.',
                 '', '| # | Scenario | Verdict | Failed checks |', '|---|---|---|---|']
        for number, title, verdict, note in self.rows():
            lines.append(f'| {number} | {title} | {verdict} | {note} |')
        teardown = state.get('teardown', {})
        lines += ['', f'Teardown clean: {teardown.get("clean")}', '']
        for check, passed in teardown.get('checks', {}).items():
            lines.append(f'- {check}: {passed}')
        return '\n'.join(lines) + '\n'

    def write(self):
        root = self.sandbox.paths.root
        (root / 'results.json').write_text(json.dumps(self.sandbox.state, indent=1, default=str))
        (root / 'results.md').write_text(self.markdown())
        return root / 'results.md'
