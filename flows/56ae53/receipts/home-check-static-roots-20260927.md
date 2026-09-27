# Home full-check static roots

Source examined: immutable CriomOS-home revision
`daf026f1e02bcd092f0ecc43b81207c96c6ec1b3`. The retained aggregate terminal
is `/var/tmp/flow-home-check-6fe957-20260926-2305/terminal.log`; it records
direct exit 1 for the three attributes at lines 572--587. No focused build,
Nix log retrieval, service operation, or source edit was performed for this
receipt.

## cluster-relay-package

`checks/cluster-relay-package/default.nix` unconditionally tests for
`${inputs.message.packages.${system}.default}/bin/relay`. The pinned Message
revision is `930c5169ffcf5fa3784b34b2751763009e926d1d`; its `Cargo.toml` has
`autobins = false` and declares no `relay` `[[bin]]`. Its unused
`src/bin/relay.rs` therefore does not place `relay` in the default package.
The check's `test -x` fails without output. Its fixture only substitutes a
fake relay while evaluating the Home module and does not change this separate
real-package assertion.

Owner: Messenger/Home integration. Remove or replace the retired relay check,
or explicitly package a relay only if that behavior remains required.

## session-variables

`checks/session-variables/default.nix` tests
`$activationPackage/etc/profile.d/hm-session-vars.sh`. The Home Manager
artifact that owns this script is `homeConfiguration.config.home.sessionVariablesPackage`;
the repository's `checks/default-opener/default.nix` already uses that artifact
at its line 32. An activation package is a generation wrapper and does not
promise that the session-vars file at its root. The initial `test -f` is
output-silent, matching the retained aggregate terminal's lack of builder
lines.

Owner: Home Nix checks. Bind and inspect `sessionVariablesPackage`, then retain
the rendering assertion only if its output format is part of the intended
contract.

## listener-level-widget

`checks/listener-level-widget/default.nix` line 47 requires the exact one-line
text `plugins.enabled = [ "criomos/listener-level" ];`. At the examined revision,
`modules/home/profiles/min/sfwbar.nix` has a multiline `plugins.enabled` list
containing both `criomos/wispr-status` and `criomos/listener-level`. The first
`grep -F` consequently exits 1 before producing output. This explains the
empty direct-check diagnostics without attributing a runtime widget failure.

Owner: the existing Listener desktop lane. Replace the serialization-sensitive
grep with a semantic membership assertion, or update the intended structural
expectation. No widget implementation work belongs to this receipt.

## Limit

These are static, source-grounded failure roots. A named focused check with
retained build output remains the acceptance proof after a repair.
