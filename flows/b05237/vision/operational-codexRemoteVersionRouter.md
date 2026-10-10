# Operational: the codex-remote executable checks which version is latest and routes to the right side

## The executable checks: if next has a newer version than stable, you use stable. If next has a different version than stable, you use next. Flows naturally move to the side we want

Context: spoken by the living to primary Psyche opus (Claude, medium, flow
b05237) on 2026-09-18, refining the stable/next Codex remote design from
Fable's proposal. The living names a version-routing executable: the plain
`codex-remote` command inspects both services and routes to the right one.
The rule: if next is newer than stable, use stable (because next is untested);
if next has a different version than stable (meaning stable was updated and
next hasn't caught up), use next. This creates a natural flow: new versions
land on next first, flows stay on stable until next is promoted, then flows
move to the promoted side without manual switching. Logged by the main flow
before acting.

> Yeah, and the Codex remote executable that's currently in the profile could, or we can make one that checks to see which version is the latest. If next has a newer version than stable, then you use stable. If next has a different version than stable, then you use next. That way, the flows will naturally move to the side that we want them to move on.

-- psyche, direct to primary Psyche opus b05237.
