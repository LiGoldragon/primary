# Chroma–Emacs adapter audit witnesses

Method: code read `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
at revision `0b502607e7a20e08e33f675c6ac3e77696c755fa`. The source defines the
two theme configuration variables, global mode, native D-Bus transport seams,
snapshot parsing, owner reconnect, scoped theme application, postcondition
checking, rollback, and bounded typed reporting.

Method: code read `/git/github.com/LiGoldragon/chroma-emacs/test/chroma-theme-test.el`.
The test macro replaces `chroma-theme--transport-subscribe-state`,
`chroma-theme--transport-subscribe-owner`,
`chroma-theme--transport-unsubscribe`,
`chroma-theme--transport-register`, and
`chroma-theme--transport-report` with callbacks. The six tests therefore do
not call the production `dbus-register-signal` or `dbus-call-method` paths.

Method: code read `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-daemon.sh`.
The runner starts an Emacs daemon on a temporary socket and loads ERT. It does
not start `dbus-run-session`, `dbus-daemon`, or a fake D-Bus service.

Method: probe `cd /git/github.com/LiGoldragon/chroma-emacs && emacs -Q --batch -L lisp -L test -l test/chroma-theme-test.el -f ert-run-tests-batch-and-exit`.
Observed: six tests ran, six passed, zero unexpected.

Method: probe `cd /git/github.com/LiGoldragon/chroma-emacs && timeout 90s bash test/run-isolated-daemon.sh .`.
Observed: exit status 0; this is the daemon runner around the same transport
stubs, not a D-Bus integration witness.

Method: probe `cd /git/github.com/LiGoldragon/chroma-emacs && nix flake check --no-update-lock-file`.
Observed: all checks passed for `x86_64-linux`; Nix reported that
`aarch64-linux` was omitted as incompatible on this host.

Method: probe a batch Emacs evaluation with `chroma-theme--last-revision` set
to 5, then `chroma-theme--handle-snapshot "NotAState" 4` under the test peer.
Observed output:

    last=4 reports=((4 failed "configuration" "Invalid Chroma theme configuration: \"Unknown desired state: \\\"NotAState\\\"\""))

This demonstrates that malformed revision 4 is not ignored as stale and
regresses the remembered revision from 5 to 4.

## Sources

- `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/chroma-theme-test.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-daemon.sh`
- `/git/github.com/LiGoldragon/chroma-emacs/nix/package.nix`
- `/git/github.com/LiGoldragon/chroma-emacs/nix/checks.nix`
- `/git/github.com/LiGoldragon/chroma-emacs/flake.nix`
