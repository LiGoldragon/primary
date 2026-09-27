# Witness: flow-0174 prerequisite witnesses not found

**Method**: direct filesystem read (`Read` tool) and search (`find` over
`/home/li/wt/primary/56ae53/flows` and over `/` to depth 8 for
`*flow-0174*` and `*witnesses*` paths), run before any Herdr or Flow
command was issued. No Herdr, Flow, or systemd command was run in the
course of this check.

## Finding

The brief for this subflow (from main flow 8904b1) instructed reading
two files before starting the nine numbered steps:

- `FLOW_DIRECTORY/witnesses/flow-0174-three-live-start-attempt.md`
- `FLOW_DIRECTORY/witnesses/flow-0174-fixture-and-baseline.md`

Neither exists. `flows/8904b1/` holds only `log.md` and `receipts/`;
it has no `witnesses/` directory at all (I created one, empty except
for this file, to hold this report). A recursive search of every
`flows/*/witnesses/` directory in this working copy, and a
filesystem-wide search to depth 8 for any path containing
`flow-0174`, found no file matching either name anywhere.

The search for `*flow-0174*` more broadly did surface four unrelated
paths from other work: `/var/tmp/flow-0174-home-validation-6fe957`,
`/tmp/flow-0174-test-target-407811`,
`/home/li/wt/flow-0174-independent-test-407811` (a git+jj checkout,
matching the brief's named clean tree for the tagged revision), and
this session's own scratchpad directory
`.../scratchpad/flow-0174-fixture-1790483601`. None of these is a
witness document; none was read further, since reading them was not
asked for and they are not the two named files.

`flows/8904b1/receipts/flow8904b1-to-9ac67c-chronology-check-20260926-233508.md`
(pre-existing, not written by this subflow) independently shows the
main flow already knew, as of 23:35 UTC, that this exact matter was
unresolved: it records a message to Field Sol about "two Herdr
fixture bring-up attempts" ending in
`Held.{ field-sol-9ac67c RepairRequired }`, consistent with
`flows/8904b1/log.md` currently being repaired by another worker (per
this subflow's own brief).

## Conclusion

The brief's premise — that the fixture stage and the three-live-start
attempt were already written up as witnesses to read — does not hold
in the working copy as found. This subflow stopped here, before
reading Field Sol's report or issuing any Herdr, Flow, or systemd
command, and before touching any live or scratch state.
