# Live stock ChatGPT Desktop activation witness

Captured on 2026-09-02 on Ouranos. This witness records the continuity-gated
activation of the reviewed stock ChatGPT Desktop revision and a bounded,
privacy-preserving Desktop launch observation.

## Method

I read the required non-management, flow-evidence, behavior, testing, Nix,
operating-system, Lojix, edit-coordination, and secrets instructions; read the
existing rollback and deployment witnesses; and read the relevant written
psyche records without creating a psyche record. I then resolved the exact
immutable output with separate Nix evaluation and build steps in one persistent
terminal session, with local builds disabled and only `/etc/nix/machines`
configured as builders. After comparing the exact candidate with deployment
145 and the active unit, I queried Lojix, submitted the authorized activation,
and queried it through terminal completion.

After completion, I used only metadata/process/socket/profile observations. I
launched the active Desktop package through the active Wayland session with a
transient `setsid` process, did not create a service, and did not delete,
migrate, or inspect Desktop data, caches, configuration, or conversation
contents. I did not connect to the ChatGPT IPC or to the Codex control socket.

The only authored file is this parent-reserved witness.

## Exact candidate resolution

The immutable CriomOS consumer revision was
`663fefb70f9962c6751fd0d87b07f8cfef01ef9e`; its locked CriomOS-home input is
the reviewed `c025a681df31d55b9035364c01e2f6c8d7b59c1c`.

The captured persistent-session command used the materialized Ouranos `system`
and `horizon` inputs, the immutable source, `--option max-jobs 0`,
`--option fallback false`, and `--builders '@/etc/nix/machines'`:

```sh
nix eval --raw --option max-jobs 0 --option fallback false \
  --builders '@/etc/nix/machines' \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon \
  'github:LiGoldragon/CriomOS/663fefb70f9962c6751fd0d87b07f8cfef01ef9e#homeConfigurations.li.activationPackage.drvPath'

nix build --refresh --no-link --print-out-paths --print-build-logs \
  --option max-jobs 0 --option fallback false --builders '@/etc/nix/machines' \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon \
  'github:LiGoldragon/CriomOS/663fefb70f9962c6751fd0d87b07f8cfef01ef9e#homeConfigurations.li.activationPackage'
```

Evaluation completed with exit `0` and produced
`/nix/store/3f1x5fqdbn4sq29ga2jka99wri98342j-home-manager-generation.drv`.
The separate build completed with exit `0` and produced the exact candidate
generation:

```text
/nix/store/hli4cf0csmxsh3364aq0qdh8klvbalzi-home-manager-generation
```

Nix warned that the transient materialized `system` and `horizon` overrides
differed from the source stubs and did not write a lock file; it also emitted
existing package deprecation/problem warnings. Neither phase wrote product
source or a lock file.

## Persistent-owner continuity gate

The pre-activation active deployment was 145 at
`/nix/store/1rc1hq9b64kf34b9frkprh9i1s86p997-home-manager-generation`.
The candidate and current generations resolve their `home-files` links to
different Home Manager file trees, but each
`codex-remote-control.service` symlink resolves to exactly the same immutable
unit file:

```text
/nix/store/wz1lzdy0szhpwis2cjn68ak8dw4q7bhx-codex-remote-control.service/codex-remote-control.service
```

Candidate/current/active unit SHA-256 is
`720c73a7a11b170e770374cd2580728e2af0adbebe44ef52769f47bc728c034e`.
Both byte comparisons exited `0`: candidate versus 145, and candidate versus
the live `~/.config/systemd/user` link. The complete relevant unit is:

```ini
[Install]
WantedBy=default.target

[Service]
ExecStart=/nix/store/vp307a51wwncdl5cd7a8mm3d1w1x5qj6-codex-0.152.1/bin/codex app-server --remote-control --listen unix://
Restart=always
RestartSec=2s
UMask=0077
WorkingDirectory=/home/li/primary

[Unit]
Description=Codex Remote Control app-server
```

Thus all unit executable/store-path references, including `ExecStart`, are
unchanged. The candidate and current profile `bin/codex` targets also both
resolve to `/nix/store/j7xbc7wppa4zrzb5d50s3jw05fvqgns3-codex/bin/codex`,
with identical bytes (`cmp` exit `0`). The generated activation scripts use
the same Home Manager `sd-switch` reconciliation mechanism; no direct
`codex-remote-control` activation-script reference was present. This exact
unit identity is the safety gate: it rules out a unit-driven owner replacement
or restart by this activation.

Immediately before activation, the user unit was `active/running`, with
`MainPID=1664375`, and Unix socket
`/home/li/.codex/app-server-control/app-server-control.sock` was listening
under that PID.

## Target re-check and Lojix activation

Fresh ordinary-socket query established logical node `goldragon/ouranos`,
deployment 145 as current at the stated generation/revision, and deployment
146 as `UserEnvironment.Realize`, source `663fef…`,
`Completed/Succeeded`. `ssh -G li@ouranos.goldragon.criome` resolved user
`li`, hostname `ouranos.goldragon.criome`, port `22`. The canonical proposal
`/git/github.com/LiGoldragon/goldragon/proposal.datom` was an absolute regular
non-symlink file (mode `0644`, 5163 bytes, SHA-256
`933c07afb507b3b9d64bce08cf40e8f4f06b55350d12178c5d7b911582c8f614`).

The first owner request used slash-revision shorthand and was rejected during
admission, without activation:

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS/663fefb70f9962c6751fd0d87b07f8cfef01ef9e (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

Its reply was deployment 147 `Rejected.FlakeReferenceMalformed`. Existing
successful immutable Lojix witnesses establish the configured parser form
`github:LiGoldragon/<repo>?rev=<40-hex>`. The corrected, explicit request was:

```sh
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/proposal.datom github:LiGoldragon/CriomOS?rev=663fefb70f9962c6751fd0d87b07f8cfef01ef9e (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'
```

It returned `DeployAccepted.(148 (3768 3768))`. Ordinary
`Query.ByDeployment.(148)` observed `Building` and then terminal:

```text
(148 148 (UserEnvironment.li goldragon ouranos UserEnvironment UserEnvironment.ActivateNow LiveActivation RequireImmutable Some.663fefb70f9962c6751fd0d87b07f8cfef01ef9e) Some.(3768 3768) Completed Some.(3801 3801) Some.Succeeded)
```

The final node query makes deployment 148 current at the exact candidate
generation and source revision. The active profile is now
`home-manager-997-link`, resolving to that same candidate output.

## Post-activation continuity

After activation, `codex-remote-control.service` remained
`active/running`; `MainPID` and `ExecMainPID` remained `1664375`, equal to the
pre-activation PID. Its command remains the exact unchanged `ExecStart` above
and the original control socket remains listening under PID 1664375. A final
exact process query finds one remote-control owner process. The user manager
lists one Codex unit only: `codex-remote-control.service`. No listener exists
on TCP port 18080.

The launched ChatGPT process has application-local Unix IPC sockets
(`.codex/ipc/ipc.sock` and a temporary `codex-browser-use` socket) while it is
alive; they are owned by the ChatGPT wrapper process, not by the Codex app
server, and were not connected to. No additional process has the remote-control
app-server command line, no custom service was introduced, and the owner
continued independently of Desktop launches.

## Stock package and Desktop GUI witness

The active profile wrapper is
`/nix/store/a2nvjsivkzqq957c8wjr3i260v6d0721-chatgpt-26.831.21537/bin/chatgpt`.
It executes only
`/nix/store/p3vjdpavgmgqv92wga4palispkbyw17j-chatgpt-unwrapped-26.831.21537/bin/chatgpt`
and passes the configured Wayland flags. It contains no
`CODEX_APP_SERVER_USE_LOCAL_DAEMON`, CLI-path, force-CLI, or App Tools pipe
environment forcing.

The unwrapped package has a regular, read-only vendor ASAR at
`lib/chatgpt/resources/app.asar`, size `292435829`, SHA-256
`9745ec1195897c019533d08e8415ab81a3c4e59e845403fdfea42ce1272fe954`, which
matches the independently recorded vendor archive hash. Its bundled
`resources/codex` is a regular executable, mode `0555`, size `255505120`, not
a Nix symlink. These observations verify the active packaged wrapper/ASAR/Core
boundary without invoking the Core protocol.

The active graphical session is Wayland (`wayland-1`). I launched the active
profile wrapper three times with transient `setsid`, `XDG_RUNTIME_DIR`, the
user session D-Bus address, and `WAYLAND_DISPLAY`; each launcher command
returned exit `0` and no durable service was created.

- The first launch registered a ChatGPT wrapper PID `2035255` visible through
  its local IPC sockets; it was no longer present at a later probe.
- The second registered PID `2036372` on the AT-SPI bus and local IPC; it too
  was absent by the later probe. These observations do not establish a crash
  cause.
- The third, bounded health witness observed main Electron wrapper PID
  `2037054` from the stock unwrapped package for more than five seconds, with
  zygote, GPU, network/storage utility, and renderer children. This is a real
  Electron process tree, separate from PID 1664375. At the final count, all
  ChatGPT wrapper processes had self-exited and the count was zero; no duplicate
  Desktop process remains. No process was killed or cleaned up by this work.

The user AT-SPI D-Bus service is active and its direct bus has
`org.a11y.atspi.Registry`; while the second launch lived, it registered a
unique `.ChatGPT-wrappe` name with its PID. However, `gdbus` is not installed,
Python GI/pyatspi is unavailable (`ModuleNotFoundError: gi`), and raw `busctl`
could not provide a safe high-level application/window/action tree. I did not
traverse accessible children, inspect window/conversation text, invoke an
accessibility action, or inject input.

Consequently a real GUI process launch and stock package boundary are
witnessed, but a new thread/start and a resume of that thread are not. No safe
automation surface exists in this environment for those actions without
inventing proof or reading/interacting with private UI state. Initialization,
thread/start, and thread/resume remain distinct: only the application's normal
launch initialization was observed.

## Remaining unknowns

- The immediate exit cause of the first two short ChatGPT launches is unknown;
  no application logs or private state were read. The third launch proves a
  bounded healthy Electron process tree but not long-lived GUI stability.
- New-chat creation and thread-resume behavior remain unverified because the
  available AT-SPI route is discovery-only and no safe GUI controller is
  installed or exposed.
- This witness does not read or claim the content, authentication state, or
  server outcome of any Desktop conversation.

## Sources

- `/home/li/primary/NON_MANAGEMENT_AGENTS.md`
- `/home/li/primary/.agents/skills/{child-flow,flow-evidence,behavior,testing,nix-workflow,operating-system,lojix,file-editing,edit-coordination,secrets,spirit,psyche}/SKILL.md`
- `/home/li/primary/flows/4ad49f/reports/system-integration.md`
- `/home/li/primary/flows/4ad49f/witnesses/{deployment-boundary,home-rollback-review,pristine-stock-boundary}.md`
- Immutable CriomOS `663fefb70f9962c6751fd0d87b07f8cfef01ef9e` and
  CriomOS-home `c025a681df31d55b9035364c01e2f6c8d7b59c1c`
- Fresh Nix, Lojix, profile, systemd, socket, package, Wayland, and AT-SPI
  observations described above.
