# CriomOS-home Chroma–Emacs slices 3 and 4

## Result

The Home-side work is structurally localized, but it cannot be completed
against the current inputs. The accepted design requires a public
`chroma-emacs` repository and a Chroma D-Bus/status implementation that do not
exist at the inspected revisions. Current Home still has the legacy direct
projection path:

```text
Home generates Ignis theme files
  ├─ Emacs reads Darkman current-mode once at startup
  └─ Chroma launches emacsclient --eval and forgets the result
```

The target shape is:

```text
Home generates Ignis files + supplies symbols/load path + enables resident mode
  └─ Emacs daemon runs chroma-theme-mode
       ├─ subscribes/registers with Chroma's session D-Bus service
       ├─ applies and verifies only the Chroma-owned theme
       └─ acknowledges Applied or typed bounded failure
Chroma owns desired Light/Dark state, revision, and consumer status
```

No product source, build, activation, deployment, or external state was
changed in this reconnaissance.

## Settled ownership

The accepted design settles these points:

- `chroma-emacs` is a new public focused repository. The existing
  `CriomOS-emacs` whole-distribution scaffold is not its substitute.
- Chroma is the semantic authority and owns desired state, persisted monotonic
  revision, D-Bus publication, and per-consumer status.
- `chroma-emacs` is the only Emacs projection. It subscribes before
  registration, reconciles the registration snapshot, handles owner changes,
  ignores stale revisions, verifies the postcondition, and reports an
  acknowledgement or typed bounded failure.
- Home owns the plugin pin, package/native compilation, theme symbols/load
  path, mode enablement, and Ignis theme generation. It does not schedule
  themes, generate palettes, embed setup paths in the plugin, or disable
  unrelated overlay themes.
- Home owns the real end-to-end Nix witness; plugin ERT/isolated-daemon tests
  own the protocol matrix against a fake D-Bus peer; Chroma owns protocol and
  persistence tests.

## Exact current code sites

### Pin and package

`/git/github.com/LiGoldragon/CriomOS-home/flake.nix:437-439` contains only
commented planned `criomos-emacs` input lines. Add one exact pinned
`chroma-emacs` input there, following Home's `nixpkgs` input when that is part
of the new flake's contract. The lock update belongs in `flake.lock`; do not
pin a moving branch. Current active component inputs use exact GitHub
revisions, and package consumers conventionally read
`inputs.<component>.packages.${system}.default`.

The plugin's package attribute and any helper for native compilation are not
known: the public repository returned 404 and has no local checkout. That
output contract must be established by the plugin implementation before this
file can be made evaluation-correct.

### Emacs package, init, and service

`modules/home/profiles/med/emacs.nix:13-125` defines the package set from
`pkgs.emacs-pgtk`; `inputs` is not currently an argument. Add it only to
consume the pinned plugin package. The plugin must enter the same
`emacsPackagesFor emacsBase` package set so its dependencies and load path are
visible to the exact package used by both `programs.emacs` and
`services.emacs`.

Replace the startup-only block at `:310-323` with Home-authored configuration
that:

1. adds the generated theme directory to `custom-theme-load-path`;
2. supplies the semantic Light/Dark mapping to the plugin as the exact
   symbols `ignis-light` and `ignis-dark`;
3. loads `chroma-theme`; and
4. enables global `chroma-theme-mode` in the resident daemon.

The precise plugin variables/entry points are intentionally not invented
here. The accepted design names the feature and mode but does not define the
Lisp customization variable names. The plugin repository must publish this
small configuration contract.

Preserve `services.emacs` at `:804-808`, the shared `emacsWithPackages`, the
editor MIME/default-editor behavior, and existing Nix build-time native
compilation. The current `initElCompiled` derivation at `:663-722` byte-
compiles `init.el` and synchronously native-compiles it into a store
`eln-cache`; `early-init.el` at `:724-747` prepends that cache at runtime.
Slice 3 must extend this same reproducible path to the plugin's Elisp, either
by consuming a plugin package that already ships `.eln` artifacts for this
exact Emacs build or by compiling the plugin source alongside `init.el` in
this derivation. Do not enable runtime JIT native compilation. Which side
owns the plugin `.eln` build is an unresolved package-shape question, not a
reason to add a second compatibility package.

### Home-owned Ignis assets

`modules/home/base.nix:21-110` creates the two Base16-derived theme files and
provides `ignis-dark` / `ignis-light`. `:143-156` installs them at
`.config/emacs-ignis-themes`. Keep this generator and path in Home. The plugin
must receive the path from declarative init and must not generate or own these
files. The path is already setup-independent at the source level when
constructed with `expand-file-name`; the old Chroma adapter's literal
`"$HOME/.config/..."` is not a valid Lisp expansion and disappears with the
direct adapter.

### Chroma configuration

`modules/home/profiles/min/chroma.nix:107-140` currently emits:

```text
(Concerns Terminal Desktop Ghostty Emacs Pi)
(Adapters
  (Dconf <path>)
  (Emacsclient <path>))
```

After the Chroma protocol/status work is pinned, remove `Emacs` from the
concern list and remove `Emacsclient` from adapters. Chroma's D-Bus service is
not a configured imperative adapter; no Home shell command or direct
`emacsclient --eval` should replace it. The existing Chroma user service and
activation seed can remain, subject to whatever exact D-Bus service is
specified by Chroma's implementation.

`checks/chroma-dotos-config/default.nix:45-90` currently positively asserts
the old Emacsclient path and Emacs concern. Replace those expected generated
output assertions with the new no-direct-adapter shape while retaining the
already-proven absence of the `current-mode` sidecar. This is a generated
DOTOS output check; it does not replace the runtime witness.

## File-level implementation plan

1. **Upstream prerequisites, outside this Home slice.** Create and prove the
   public `chroma-emacs` repository. Publish its Nix package output, exact
   Emacs package name, required dependencies, feature/mode configuration
   contract, and isolated-daemon/fake-peer tests. Implement Chroma's session
   D-Bus desired-theme, registration snapshot, change signal, revision
   persistence, acknowledgement/failure, status query/signal, and service
   owner-reconnect contract. Remove Chroma's `Emacsclient` concern/adapter in
   that implementation. Until these exist, Home cannot lock a usable input.

2. **`CriomOS-home/flake.nix` and `flake.lock`.** Add the exact
   `chroma-emacs` input and lock it. Keep the existing Chroma pin only if it
   has the accepted D-Bus contract; otherwise repin to the reviewed Chroma
   revision. Do not add or wire `CriomOS-emacs`; its unfinished `emacs-plb`
   conversion is unrelated.

3. **`modules/home/profiles/med/emacs.nix`.** Add `inputs`, consume the
   plugin package through its published output, include it in the one
   `emacsWithPackages` set, remove the Darkman startup read, install the
   plugin feature and global mode in generated init, and provide
   `ignis-light`/`ignis-dark` plus the Home-owned load path. Extend the existing
   build-time `.elc`/`.eln` derivation to cover plugin code through the chosen
   upstream package contract. Keep the daemon service and all unrelated Emacs
   behavior unchanged.

4. **`modules/home/base.nix`.** Retain the existing Ignis generator and
   `.config/emacs-ignis-themes` materialization. Only adjust it if the plugin's
   published load-path contract requires an explicit generated path export;
   do not move theme generation into `chroma-emacs` or Chroma.

5. **`modules/home/profiles/min/chroma.nix`.** Delete the direct Emacs concern
   and `Emacsclient` adapter from generated DOTOS. Keep the Chroma daemon's
   other native concerns and schedules. Do not add a second one-shot adapter.

6. **`checks/chroma-dotos-config/default.nix`.** Update the generated-output
   contract to prove no direct Emacs adapter/concern remains and no
   `current-mode` sidecar is restored.

7. **New `checks/chroma-emacs-isolated-daemon/default.nix` (or an equivalent
   explicitly named check).** Evaluate the relevant Home module with the exact
   plugin and Chroma inputs. Materialize the generated theme files and init
   into a temporary HOME, create private XDG config/state/runtime directories,
   and run `dbus-run-session` with no host bus. Launch the real built Chroma
   daemon and an isolated Emacs daemon; use the existing Chroma fake gamma /
   Ghostty peer pattern only for native prerequisites. Start Emacs after
   Chroma to exercise late registration. For each Light/Dark transition, wait
   on the Chroma `Applied` acknowledgement/status event for the corresponding
   revision, then query Emacs for `custom-enabled-themes` and a representative
   face (the generated foreground). Load a temporary unrelated overlay theme
   and assert it survives while exactly the opposite Chroma-owned theme is
   disabled. Restart or replace the Chroma bus owner and assert Emacs
   re-registers and converges to the latest desired revision. Use event-driven
   readiness/acknowledgement, not sleeps or source-text greps.

8. **`flake.nix` check registration.** Register the new check in the same
   `projectChecks` map as the existing Home checks. Resolve its supported
   systems explicitly; current design does not settle whether the plugin's
   native compilation and Emacs PGTK daemon witness are required on both
   `x86_64-linux` and `aarch64-linux`.

9. **Documentation cleanup.** Update the Home roadmap/architecture comments
   that still say the next Emacs work is `criomos-emacs`/`home-tl6`, replacing
   that dependency with the focused `chroma-emacs` integration and keeping
   `CriomOS-emacs` marked as a separate unfinished scaffold. This is a durable
   documentation correction, not a compatibility path.

## Dependencies, unknowns, and risks

### Dependencies

- No public `chroma-emacs` repository or package exists at this observation.
- Current Chroma `eea85f4a` has no D-Bus service/revision/status contract and
  still has the direct Emacs concern.
- Home's current `CriomOS-emacs` roadmap item is open but is not a dependency
  of the accepted design; leaving it as an implicit dependency would revive a
  rejected repository boundary.

### Unknowns returned to the caller

- Exact public repository revision and Nix output attribute for
  `chroma-emacs`.
- Exact Lisp customization names for semantic theme symbols and load paths.
- Exact D-Bus bus name, object/interface, registration method, snapshot shape,
  change signal, acknowledgement/failure method, status signal/query, and
  owner-change semantics.
- Whether plugin `.eln` artifacts are built by the plugin flake or by Home's
  aggregate `initElCompiled` derivation.
- Supported systems and whether a headless Emacs PGTK daemon needs an X/Wayland
  test compositor in the Nix check.
- The exact event surface the Home check will use to await `Applied` without
  polling; this follows from Chroma's implementation.

### Risks

- Removing the old adapter before both upstream contracts are pinned creates a
  deliberate temporary loss of Emacs projection; sequence the Home change
  after upstream package/protocol proofs.
- The current Home and Chroma services are independently graphical-session
  aware. The plugin's subscribe-before-register/reconnect semantics must absorb
  startup ordering rather than adding a brittle systemd ordering edge.
- Loading a malformed or missing theme must preserve the prior Chroma-owned
  state and produce `Failed`, not silently acknowledge; Home's generated valid
  assets prove only the success path.
- Current direct projection disables every enabled theme. The new plugin must
  disable only the opposite Chroma-owned theme and retain overlays.
- Live Home activation can reload graphical-session services. Follow the Home
  activation-safety rule; use a full OS deployment for durable state and do not
  treat a Home-only overlay as reboot-persistent.

## Later deployment observations

These are follow-up witnesses, not performed here. After upstream pins and
Home checks pass:

1. Push and lock Home's exact main revision, then update CriomOS's
   `criomos-home` input/lock before any OS deployment. Build/evaluate through
   the deployment-provided materialized inputs and configured remote builder;
   keep evaluation, realized closure, and activation evidence separate.
2. Confirm the embedded target activation package, generated
   `.config/emacs-ignis-themes`, native `.eln` artifacts, Chroma user service,
   and Emacs daemon service in the selected generation.
3. In the running user session, observe Chroma desired mode/revision and
   consumer status, `chroma-theme-mode`, `custom-enabled-themes`, and the
   representative rendered face for both directions. Record the exact
   acknowledgement revision rather than inferring success from a process exit.
4. Restart Chroma while Emacs remains resident and observe a new registration,
   snapshot reconciliation, and `Applied` status. Separately restart Emacs and
   observe startup subscription/reconciliation from the persisted Chroma
   revision.
5. Report any mismatch between source revision, evaluated input, realized
   generation, active user services, live Emacs state, and reboot-persistent
   system generation. A standalone Home activation may be a live overlay; a
   full system generation carrying the same Home pin is required for durable
   reboot behavior.

## Sources

- `/home/li/primary/flows/01a0238b/reports/emacsAdapterDesign.md`
- `/home/li/primary/flows/01a0238b/vision/emacsPlugin.md`
- `/home/li/primary/flows/01a0238b/witnesses/sourceBoundaries.md`
- `/home/li/primary/flows/01a01b52/annotations.md`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-dotos-config/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-home/docs/ROADMAP.md`
- `/git/github.com/LiGoldragon/chroma/src/theme.rs`
- `/git/github.com/LiGoldragon/chroma/src/config.rs`
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`
- `/git/github.com/LiGoldragon/chroma/flake.nix`
- `/git/github.com/LiGoldragon/chroma/scripts/chroma-sandbox-terminal`
- `/git/github.com/LiGoldragon/CriomOS-emacs/README.md`
- `/git/github.com/LiGoldragon/CriomOS-emacs/docs/ROADMAP.md`
- `/git/github.com/LiGoldragon/CriomOS-emacs/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/userHomes.nix`
- `/git/github.com/LiGoldragon/CriomOS/reports/0038-lojix-local-config-and-home-deploy-design.md`
- Witnesses `flows/5ff8f889/witnesses/homeState.md`, `homeContracts.md`,
  `chromaAndScaffold.md`, and `testAndDeployment.md`
- Flow `5ff8f889`
