# Passive checkup bootstrap

This adapter reads `~/.local/state/field-census/latest.json` and a current
operator roster, then writes a three-aspect assessment to
`~/.local/state/field-checkup-shadow/latest.json`. It performs no Herdr,
Message, HM, Orchestrate, lifecycle, or wake call. It never creates a duty.
Without an authoritative duty source, each aspect is `DutyUnknown` while
coverage gaps are reported separately. The timer uses the shared census
snapshot and does not add another collector.

The passive `StructuralReport` maps distinct physical panes to the declared
Field/Mind/Psyche × high/medium/low/ultra-low grid. It reports unmatched cells
as gaps and unmatched panes as ghosts, including protected crossovers. Harness
health and role/model/effort evidence remain separate; terminal status alone
cannot prove native health. Every ghost has `removal_authorized:false`, and
every report has `launch_authorized:false`. A total of twelve panes cannot
pass when a cell is missing and another is duplicated.

`roster.json` is a temporary observation expectation, maintained after each
verified transfer by Field Low. A missing tier has `null`; a known tier has
`{"flow_id":"...","native_thread":"..."}`. Its schema is:

```json
{"version":1,"revision":"operator-receipt", "aspects":{"Field":{"high":null,"medium":null,"low":null,"ultra_low":null},"Mind":{"high":null,"medium":null,"low":null,"ultra_low":null},"Psyche":{"high":null,"medium":null,"low":null,"ultra_low":null}}}
```

This bootstrap does not implement the Mind-owned `checkup-nexus` contract.
Wake requires typed duty authority, exact current Flow and Message bindings,
pending-work evidence, durable episodes, and correlated acknowledgements.
The existing `core-checkup` and heartbeat units remain the deployed monitor.
