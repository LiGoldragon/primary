# Chroma resident projection — slice 2

Chroma main commit `d6cea6bcb41fb75d8a268cd46c66120eb694562c` implements the
approved inspection surface for the public `chroma-emacs` consumer.

It owns `io.github.LiGoldragon.Chroma` on the same-user session bus, exports
`/io/github/LiGoldragon/Chroma/Theme` and
`io.github.LiGoldragon.Chroma.Theme1`, and persists the desired theme plus its
revision atomically. A legacy theme-only archive migrates once at revision 0;
owner identity and applied status are deliberately transient and restart as
Unavailable. Registration is allowlisted to `emacs`, bound to the unique D-Bus
sender, and owner disappearance returns the projection to Unavailable.

The public calls are:

- `RegisterConsumer(string consumer) -> (string state, uint64 revision)`
- `DesiredStateChanged(string state, uint64 revision)`
- `ReportProjection(string consumer, uint64 revision, string result, string code, string summary)`
- `GetProjectionStatus(string consumer) -> (string status, uint64 revision)`

`result` is Applied or Failed. Applied sends empty `code` and `summary`; Failed
uses one of `configuration`, `load-failed`, `verification-failed`, or
`application-failed`, with summary at most 240 UTF-8 bytes. This is the
smallest typed correction to the slice-1 client: D-Bus method signatures are
fixed, so its earlier three-argument Applied call and five-argument Failed call
cannot both be served by one method name.

New reducer and persistence tests were first observed failing due to absent
public types, then passed. `dbus-run-session -- cargo test --test session_dbus`
proved an actual session-bus registration, full snapshot signal, and fixed
acknowledgement signature. Nix flake evaluation and remote-builder default
check/package builds passed separately. The remaining dependency is
CriomOS-home: pin/configure chroma-emacs, remove its old adapter configuration,
and provide the cross-process daemon check.
