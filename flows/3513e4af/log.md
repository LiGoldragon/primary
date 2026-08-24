# 3513e4af — Claude incident preservation evidence

Direct reconstruction of Claude sessions `2f6b1dc5-307c-400c-b339-8ec622e8fadc` and `aa4c7747-3b0c-43ea-a131-0fa65b17348e`, their primary working-copy transitions, surviving flow artifacts, and the preservation contract visible before and after `634ad0ed5672`.

Settled: both transcripts survive. 2f6’s flow files survive after a context-based restoration committed as `90575b46c066`; aa4’s vision files were absent from the stale checkout observed by its transcript, then restored from `e9dbab8c`. The direct loss mechanism is an external/stale working-copy state transition; the exact actor or operation that selected it is unknown. The current primary entry rule landed separately in `634ad0ed5672` and was not present at either incident.

Open: no independent byte copy of 2f6’s lost tail; no direct witness identifies the concurrent actor that advanced or selected the stale Git/jj state; lane registration and claims could not be exercised because the daemon socket is absent.

## Sources

- `witnesses/claudeIncidents.md`
- `witnesses/jjState.md`
- `witnesses/instructionContract.md`
- `reports/claudeIncidentPreservation.md`
