from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

lane = Path('/home/li/primary/flows/857335')
authority = [
    'Vision/protos.md', 'Vision/datom.md', 'Vision/ethos.md',
    'Vision/signal.md', 'Vision/sema.md', 'Vision/nexus.md',
    'Intent/anatomy.md', 'Intent/conversion.md', 'Intent/context.md',
    'Intent/mandatoryTraits.md',
]

if sys.argv[1] == 'prepare':
    manifest = []
    documents = []
    for relative in authority:
        path = Path('/home/li/primary') / relative
        content = path.read_bytes()
        manifest.append({'path': str(path), 'sha256': hashlib.sha256(content).hexdigest()})
        documents.append('\n===== ' + str(path) + ' =====\n' + content.decode())
    common = '''You are an independent skeptical audit subflow. The living explicitly requests this audit.
FLOW_ID: 564f55
FLOW_DIRECTORY: /home/li/primary/flows/564f55
Delegating execution lane and report destination: /home/li/primary/flows/857335

Do not create a flow lane or log. Record your harness thread/session ID as evidence provenance if available. Read NON_MANAGEMENT_AGENTS.md and the subflow and flow-evidence skills applicable to your work. The supplied FLOW_ID and FLOW_DIRECTORY are intentional and must remain unchanged.

Task: try to DISCONFIRM that the realized stack satisfies the full landed Vision and Intent below. Seek concrete counterexamples, missing requirements, semantic collapses, incomplete boundaries, and tests that falsely appear to prove compliance. This is not a request to praise or confirm the implementation. Equally, do not invent defects: explain rejected hypotheses and distinguish demonstrated failures, direct source findings, inferences and untested risks.

Audit these clean realized repositories and identify exact revisions inspected:
/git/github.com/LiGoldragon/protos main b543678cfc8609529cea7174eb4af8a64daa54ad (0.29.1)
/git/github.com/LiGoldragon/datom-codec main f2cc06858d38a4028c928d33323a6d682e7c222f (0.25.6), including crates/datom-codec-derive
/git/github.com/LiGoldragon/ethos-zero main 4695ee0c1f5d00dcf5cceba08f5fa00412b92184 (6.1.6)
Trace actual dependency/consumer boundaries where necessary, especially generated types and binary-versus-text compilation, but distinguish this released stack from unfinished consumer WIP.

The full ten documents appended below are the standard, with no unstated deferrals. Inspect architecture and actual executable behavior as well as API naming. Check both ascent and descent, context ownership, type-driven composition, arbitrary Rust derives and containers, syntax edge cases, errors and budgets, generated Ethos structures/kinds/imports, and all applicable Signal/Nexus requirements. Do not substitute green builds for design compliance. Do not read the other skeptical auditor's report or existing implementation/audit summaries before completing your independent report.

Read-only audit: do not edit repository sources, manifests, bookmarks, live configuration or services. Do not acquire write locks or deploy anything. Do not launch Nix builds, remote builders, or broad expensive test matrices; existing source/tests and focused lightweight reproductions are sufficient. Temporary scratch evidence may be written only in your own dedicated witness directory below. No nested auditors are required. No messages to external people.

Deliver a self-contained Markdown report. For each finding give severity, exact violated authority passage, source file/line/revision, minimal counterexample or evidence, why it matters, confidence and the smallest principled correction. State what you tested and actual outcomes, unresolved limitations, requirements inspected without findings, and rejected hypotheses. Finish with a Sources section. Do not say the stack is compliant if an applicable requirement is missing. Do not fix source code: the main flow reconciles the two independent reports before further Orchestrate work.

The latest living instruction explicitly authorizes the Codex audit on gpt-5.6-sol at medium effort, superseding an older temporary user-level no-Sol restriction for this audit. The Claude audit is explicitly claude-opus-5 at medium. Do not substitute another model or effort silently.
'''
    (lane / 'witnesses/skeptical-audit-authority.json').write_text(json.dumps(manifest, indent=2) + '\n')
    for auditor in ('opus', 'sol'):
        report = lane / f'reports/skeptical-{auditor}.md'
        scratch = lane / f'witnesses/skeptical-{auditor}'
        scratch.mkdir(exist_ok=True)
        prompt = common + f'\nYour report: {report}\nYour scratch evidence directory: {scratch}\nWrite the complete report as your final response; the launcher will preserve it at the report path. You may also write that report directly if supported.\n' + ''.join(documents)
        (lane / f'witnesses/skeptical-{auditor}-brief.md').write_text(prompt)
    sys.exit(0)

auditor = sys.argv[1]
brief = lane / f'witnesses/skeptical-{auditor}-brief.md'
report = lane / f'reports/skeptical-{auditor}.md'
stdout_path = lane / f'witnesses/skeptical-{auditor}.stdout'
stderr_path = lane / f'witnesses/skeptical-{auditor}.stderr'
if auditor == 'opus':
    command = ['/home/li/.nix-profile/bin/claude', '--model', 'claude-opus-5', '--effort', 'medium', '-p', '--output-format', 'json', '--allowedTools', 'Read,Glob,Grep,Bash,Write']
else:
    command = ['/home/li/.nix-profile/bin/codex', 'exec', '-m', 'gpt-5.6-sol', '-c', 'model_reasoning_effort=medium', '--sandbox', 'read-only', '--json', '--output-last-message', str(report), '-']
with brief.open('rb') as incoming, stdout_path.open('wb') as outgoing, stderr_path.open('wb') as errors:
    result = subprocess.run(command, stdin=incoming, stdout=outgoing, stderr=errors, cwd='/home/li/primary')
(lane / f'witnesses/skeptical-{auditor}.exit').write_text(str(result.returncode) + '\n')
if auditor == 'opus' and result.returncode == 0:
    try:
        payload = json.loads(stdout_path.read_text())
        if payload.get('result'):
            report.write_text(payload['result'] + '\n')
        (lane / 'witnesses/skeptical-opus-result.json').write_text(json.dumps(payload, indent=2) + '\n')
    except (ValueError, TypeError):
        pass
sys.exit(result.returncode)
