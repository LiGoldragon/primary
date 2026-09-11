# Chroma location and schema upgrade

Investigating the laptop location failure and realizing the requested San Cristóbal override and Chroma schema upgrade.

- The living requested Chroma history recovery, bearings on location/output failures, a San Cristóbal location hotfix, and current Ethos/Datom with redundant single-field structs removed.
- Dispatched `remember` for historical evidence, `location` for live location/output state, and `chroma_upgrade` for current schema/dependency scope.
- `remember` recovered historical Chroma/Emacs projection decisions and their later corrections; these are historical claims, not present-runtime witnesses. It committed and pushed preexisting primary changes unchanged as `283810db3ee1` before this flow wrote artifacts.
- `location` reported a live active Chroma 0.4.0, State.{ Light 6500 85 }, SolarClockUnavailable, and GeoClue fixes rejected at 3149 m and 26000 m against Chroma’s 1 km acceptance threshold. It identified an existing GeoClue static-source hotfix scoped to the laptop.
- `chroma_upgrade` read upstream Chroma 0.4.0 and identified 11 single-field schema wrappers, older pinned dependencies, a stale regeneration tool, and CLI/config consumers requiring coordinated migration.
- Dispatched implementation to `location` for the host-only static override and to `chroma_upgrade` for the Chroma/Home migration and validation.
