# Claude title isolation handoff

Flow `03e825`, read-only observation for the held Psyche Ultra Low launch. This report records current evidence, not an isolation acceptance receipt. No Claude session, pane, route, profile, transcript, launcher, or job directory was changed.

## Observed boundary

Herdr identified three distinct Claude agents for the existing Psyche Medium (`b80e55`), High (`1b8ac0`), and Low (`0625c3`) seats. Each had its own pane, terminal, shell process, and Claude foreground processes. For those three shells and six foreground processes, a filtered `/proc/<pid>/environ` read showed the same named `CLAUDE_JOB_DIR` value, `/home/li/.claude/jobs/108ab020`. The named `CLISESSIONID` key was unset in all nine observations. No other environment values were collected for this report.

The three exact native transcript files, located from each seat's existing Flow identity marker, each contained its own-session `custom-title` metadata event ending in `Psyche High 1b8ac0`. This independently establishes cross-session title fanout as a native metadata observation. Shared `CLAUDE_JOB_DIR` and fanout are correlated; these observations alone do not prove the directory is the cause. The asserted inherited `CLISESSIONID` was not observed in the inspected processes. The current `flows/6db4fe/reports/canonical-title-alignment-implementation.md` attributes propagation to shared job state after one targeted `/rename`; that is the title worker's reported causal conclusion, separate from this subflow's process/transcript observations.

## Ownership and hold

At observation, Orchestrate `Observe.Locks` showed no lock naming Claude launcher/environment isolation or reserving `tools/native-batch-refresh.mjs` or `tools/claude-native-seat-refresh.py`. Lock `3960` belonged to `6db4fe` for the separate canonical-title script, tests, and its implementation report. An isolation worker and its exact source/report/receipt paths were **not located** by this audit; this is not evidence that no worker exists. No isolation acceptance receipt was found in the inspected Primary report/source inventory. `tools/canonical-title-alignment.mjs` explicitly refuses live Claude native-title apply after observed sibling propagation and labels route-only title status `deferred-isolation-unproven`; fixture rollback tests are not an isolation witness.

Keep Psyche Ultra Low on hold until the responsible source owner supplies an exact per-session environment-isolation receipt and a supported same-session title/readback witness showing no sibling title change. That evidence must name the affected native sessions and compare the relevant named job/session environment keys without exposing unrelated environment. A source patch, fixture, or title-only transcript event is insufficient by itself. The existing title worker's report also requires preserving the same UUID/context while repairing existing titles.

Independent gates remain open. The unchanged canonical Ultra Low profile and one-seat manifest are under `flows/753e69/psyche-haiku-native/`; their current audited source validation fails because `flows/b80e55/vision/flashbookResponsiveDesign.md` is absent. A real Herdr-managed caller, native skill expansion and bootstrap receipts, own Flow identity, exact title readback, HM binding, and role acceptance each need separate evidence. Existing Psyche Low `0625c3` and every other worker/route remain untouched.

## Sources

- `herdr --session messaging-build agent list` and `herdr --session messaging-build pane process-info --pane <exact pane>`: read-only distinct Psyche agents, panes, terminals, and foreground process IDs.
- Filtered read-only `/proc/<shell-or-foreground-pid>/environ`: only `CLAUDE_JOB_DIR` and `CLISESSIONID` values/presence for the three existing Psyche sessions were considered; no environment dump was retained.
- `flows/.b80e55.flow-id`, `flows/.1b8ac0.flow-id`, `flows/.0625c3.flow-id`, and corresponding exact files under `/home/li/.claude/projects/-home-li-primary/`: session identity and `custom-title` metadata only; no transcript body or file mutation.
- `orchestrate 'Observe.Locks'`: point-in-time exact path/owner observation, including title lock `3960`; absence in one snapshot is not a permanent ownership conclusion.
- `tools/canonical-title-alignment.mjs` and `.test.mjs`: live Claude apply refusal and fixture-only rollback; `flows/6db4fe/reports/canonical-title-alignment-implementation.md`: title worker's reported targeted-rename observation and causal interpretation.
- `flows/753e69/psyche-haiku-native/profile.json`, `launch-manifest.json`, and the read-only source-existence check: canonical unchanged input and independently open audited-source gate.
