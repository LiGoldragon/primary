# Datom derive current-source check

At 2026-11-05T22:16:30Z, the prepared Datom source manifest identified `datom-codec-derive` as `0.32.0`; the current remote `datom-codec` main manifest at commit `f1796c798e9687e1a021a0c7630edb26b7266ecf` reports datom-codec `0.32.12` and its workspace members. No source/API/body comparison or generated-emission check was performed here. The approved conditional remains: retain derive `0.32.0` unless the source-ledger actual-emission check demonstrates changed generated implementations; no independent derive allocation follows from this check.
