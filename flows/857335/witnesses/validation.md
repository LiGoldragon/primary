# Validation witness

Method: configured remote Nix builder (`prometheus.goldragon.criome`) ran the
Protos test, formatting, clippy, documentation, and structural-policy checks.

The Protos test gate passed after a real failure witness: an ordinary
backslash inside guillemets was dropped on round-trip. The correction preserves
it while retaining `\\»` as the escaped close form.

Datom and Ethos Zero have not passed their durable gates yet; this witness does
not claim them green.
