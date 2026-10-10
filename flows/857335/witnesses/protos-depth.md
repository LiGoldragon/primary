# Protos depth witness

Method: added a process-isolated Rust integration probe that gives the public
reader a 100,001-level braced input and a 100,002-node budget. The child runs
under a 256 MiB address-space cap and a 30-second timeout. The probe was run
once against the recursive reader before the repair, then through the complete
configured remote-builder Nix check after the repair.

Before the repair, the child reported a Rust stack overflow and exited with
SIGABRT; the parent test reported that failure without crashing. After the
repair, the reader stopped at its independent 256-structure depth boundary,
and the child succeeded. A separate 10,000-child bracketed input succeeded
with a 10,001-node budget, showing width remains governed by the public node
budget rather than the depth boundary. A separately constructed 100,001-link
headed `Protos` printed as the expected 200,005-byte text without recursive
printing. The remote check evaluated and built all nine configured checks on
`prometheus.goldragon.criome` successfully.

The subsequent qualified-head witness first failed because the reader treated
the angled constraints as a second top-level form. The landed four-form shape
keeps `Headed` anatomical: its `Symbol` head has an optional angled `Enclosed`
constraint node, and its body is unchanged. It parses nested mixed constraints
and prints `Processable<[ Clonable Sendable ] Serializable>.[ Vector <String> ]`
canonically. A standalone `Vector<String>` remains adjacent bare and angled
forms for its conceptual reader.
