## fb1008c0-1 — 2026-08-14 — session-scoped ids; retrofit by origin hunt

> I see your C now; the agents knows his own counter. thats clever.
> and we could hunt for the origin of every existing record to
> retrofit them. I like that idea

— psyche, 2026-08-14T14:03+02:00 (Designer session fb1008c0),
typed, closing the id fork: a record's id is its originating
session's short id plus that session's own count. The flow knows
its own counter, so there is no global source of truth and no
cross-flow race; the id names the record, not its location, so it
survives topic merges and archiving. Date-based append-only
archive files stand unchanged. The retrofit is the psyche's
extension: hunt the origin session of every existing record and
assign its id retroactively. Supersedes the increasing-numerics id
mechanics above. This entry carries the first session-scoped id in
its header — Designer placement, veto open.

