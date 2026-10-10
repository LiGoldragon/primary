# Chroma–Emacs adapter audit

## Outcome

At public repository revision
`0b502607e7a20e08e33f675c6ac3e77696c755fa`, the Emacs-side projection shape
is substantially implemented and the repository-local checks pass. It is not
fully proven against the approved contract: the purported isolated-D-Bus tests
are Emacs-daemon tests over function stubs, and one malformed stale snapshot
can regress the remembered revision.

The checkout's `main` and `origin/main` point at the requested revision. The
working copy was clean before and after the audit. No product repository,
GitHub state, or deployment/runtime state was changed.

## Contract audit

### Implemented client behavior

- Feature/configuration surface: `defcustom`
  `chroma-theme-light-theme` and `chroma-theme-dark-theme` are defined at
  `lisp/chroma-theme.el:22-30`; global `chroma-theme-mode` is defined and
  autoloaded at `lisp/chroma-theme.el:252-261`. Configuration is documented at
  `README.md:7-18`.
- Subscribe-before-register: `chroma-theme--reconnect` installs state and
  owner subscriptions before calling registration at
  `lisp/chroma-theme.el:228-245`. The late-startup test deliberately invokes a
  signal callback from registration at `test/chroma-theme-test.el:80-97`.
- Owner-change reconnect: owner signal registration and reconnect are present
  at `lisp/chroma-theme.el:60-67,235-250`; the behavior test is at
  `test/chroma-theme-test.el:99-115`.
- Snapshot reconciliation: registration replies accept a two-element list or
  vector and flow through the same snapshot handler at
  `lisp/chroma-theme.el:104-118,228-233`.
- Valid stale and duplicate revisions: the handler ignores a valid lower
  revision and reapplies an equal revision to converge drift at
  `lisp/chroma-theme.el:195-217`; the test is at
  `test/chroma-theme-test.el:117-132`.
- Scoped theme application: configured Light/Dark symbols must be distinct at
  `lisp/chroma-theme.el:120-129`; only the target/opposite Chroma themes are
  changed or restored at `lisp/chroma-theme.el:131-164`. Overlay membership is
  exercised at `test/chroma-theme-test.el:56-78`.
- Load-failure preservation: the target is loaded before disabling the previous
  Chroma theme at `lisp/chroma-theme.el:145-155`; best-effort restoration is at
  `lisp/chroma-theme.el:161-164`. The missing-target test is at
  `test/chroma-theme-test.el:134-154`.
- Postcondition and acknowledgement ordering: enabled-theme membership is
  checked at `lisp/chroma-theme.el:156-160`, and `Applied` is sent only after
  application returns at `lisp/chroma-theme.el:195-210`.
- Bounded typed failure reporting: full diagnostics stay in
  `chroma-theme--last-diagnostic` while stable codes and a 240-byte UTF-8
  summary cross the transport at `lisp/chroma-theme.el:166-193`. The bound is
  tested at `test/chroma-theme-test.el:156-175`.

### Nix and durable checks

The flake exposes `lib.mkChromaTheme`, `packages.<system>.default`, and the
named package for x86_64 and aarch64 at `flake.nix:6-27`. The package is an
Emacs trivial build at `nix/package.nix:3-8`. The default check invokes the
isolated daemon runner at `nix/checks.nix:3-11`.

The direct batch ERT witness ran 6/6 tests with zero unexpected results. The
daemon runner exited 0. `nix flake check --no-update-lock-file` passed on
x86_64; Nix explicitly omitted aarch64 as incompatible on this host.

## Critical proof gap: no real D-Bus peer

`test/run-isolated-daemon.sh:14-16` starts only an Emacs daemon. It does not
start `dbus-run-session`, `dbus-daemon`, or any fake D-Bus service. The test
macro at `test/chroma-theme-test.el:27-47` replaces every transport operation,
including subscriptions, registration, unregistration, and reports, with
callbacks. Consequently the tests do not exercise the production
`dbus-register-signal` or `dbus-call-method` paths, D-Bus argument signatures,
owner-change delivery, sender binding, or an isolated session bus.

This is a proof gap rather than a claim that the client control flow is absent.
The repository documentation calls this a fake peer (`README.md:33-35` and
`ARCHITECTURE.md:13-15`), but the actual witness is a transport seam with
function stubs. Chroma has no corresponding peer in this revision;
`README.md:20-31` explicitly calls the wire surface an inspection slice and
says the Chroma peer is not yet implemented.

## Concrete stale-revision defect

`chroma-theme--handle-snapshot` normalizes state before applying the stale
revision gate (`lisp/chroma-theme.el:200-205`). For a malformed stale snapshot,
normalization signals first; the error handler then stores the received
revision and reports failure (`lisp/chroma-theme.el:212-217`).

With remembered revision 5, the probe
`chroma-theme--handle-snapshot "NotAState" 4` produced:

    last=4 reports=((4 failed "configuration" "Invalid Chroma theme configuration: \"Unknown desired state: \\\"NotAState\\\"\""))

Thus revision 4 was not ignored and the monotonic remembered revision regressed.
A later valid revision 4 would no longer satisfy the `< last-revision` stale
test and could be applied. The stale comparison should precede state
normalization, or malformed stale messages should leave the remembered
revision untouched.

## Remaining proof and authority limits

The tests do not force a postcondition failure, inspect a representative
rendered face, assert that full diagnostics remain intact, or exercise failure
of rollback itself. The implementation has explicit code for the first two
checks and bounded reporting, but those paths are not fully witnessed.

Registration failure is caught and logged at `lisp/chroma-theme.el:242-245`;
there is no test for a service-owner race where the owner appears before its
object is ready and registration fails after the one owner-change event.

Persisted monotonic revisions, sender-bound consumer authority, and Chroma's
`Pending`/`Applied`/`Unavailable`/`Failed` status transitions cannot be
verified from this repository. They belong to the absent Chroma peer and
remain unresolved under the provisional ruling in
`flows/01a02b4b/vision/emacsPlugin.md:3-10`.

## Sources

- `flows/01a0238b/reports/emacsAdapterDesign.md`
- `flows/01a02b4b/vision/emacsPlugin.md`
- `flows/01a02b4b/log.md`
- `flows/01a02b97/witnesses/chromaEmacsAudit.md`
- `/git/github.com/LiGoldragon/chroma-emacs/README.md`
- `/git/github.com/LiGoldragon/chroma-emacs/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/chroma-theme-test.el`
- `/git/github.com/LiGoldragon/chroma-emacs/test/run-isolated-daemon.sh`
- `/git/github.com/LiGoldragon/chroma-emacs/flake.nix`
- `/git/github.com/LiGoldragon/chroma-emacs/nix/package.nix`
- `/git/github.com/LiGoldragon/chroma-emacs/nix/checks.nix`
