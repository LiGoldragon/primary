# Form-1 disposable rollback drill

Fixture: `form1-rollback-fixture.sh`, run only with `mktemp` state and mock
service control. It does not inspect or mutate a Home profile, systemd user
manager, service, socket, store, network, or Herdr session.

The fixture creates prior and candidate Home profile generations, an external
`flow-nexus` override, Flow and Message stores with rows and route placeholders,
and distinct copied rollback stores. It starts an old mock pair, stops it,
applies a candidate profile/override and corrupts both stores, then starts a
candidate mock pair. Cancellation is rejected until *both* network and remote
access witnesses are present. Candidate failure stops both mock services before
restoring the profile, exact override bytes, and both copied stores, then starts
the old pair.

Verified assertions:

- current profile points at generation 41 and its profile hash matches;
- external override hash matches the captured pre-switch hash;
- Flow and Message store hashes, row counts, and sorted route placeholders
  match their captured values;
- restore is rejected if either mock service is marked running; and
- cancellation returns status 42 before the two required witnesses.

The production-form timer definition is asserted as `OnActiveSec=300` with
rollback target generation 41 and a named cancellation authority. A real
five-minute elapsed wait is deliberately not witnessed: an accelerated
one-second expiry exercises the identical fixture rollback branch. Therefore
this proves the isolated procedure and timer definition, not a live systemd
timer, live Home generation switch, target-binary readability, native Start,
or remote-access witness.

Before the passing run, a disposable altered copy forced the captured Flow row
count to `999`; it failed with `ASSERTION FAILED: Flow row count`. The unaltered
fixture then passed with two Flow rows and two Message rows.
