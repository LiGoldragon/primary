# Witness — an isolated 0.32.0 Nexus over a 0.30.0-written store

Method. A `git clone --shared` of `/git/github.com/LiGoldragon/orchestrate` into
session scratch, checked out at `054ce581` (0.32.0), built with `cargo build`.
The deployed 0.30.0 executable
(`/nix/store/hnzql8g1ybpbxk1gqfrdmjfji6winm7x-orchestrate-0.30.0/bin/`) was run
against an isolated `XDG_STATE_HOME` under session scratch and an isolated
`XDG_RUNTIME_DIR` of `/tmp/o6d` (short, because a socket path must fit
`SUN_LEN`), to produce a genuine 0.30.0 store; the 0.32.0 Nexus was then started
on that same store. All drives used the released client binaries built from the
clone. No live socket under `/run/user/1001/orchestrate-nexus/` was bound by any
scratch process. The scratch runtime directory and the scratch build tree were
removed afterwards; the scratch store remains under the session scratchpad.

Every block below is verbatim output.

## Live service interruption, disclosed

At 21:35:48 a `pkill -f` written to stop the scratch 0.30.0 instance matched the
live systemd user service as well, because both run the same `/nix/store` path.
The live Nexus was down 21:35:48 → 21:36:09 (21 seconds) and was restarted with
`systemctl --user start orchestrate-nexus`. No store was written by the kill; the
lock set was intact afterwards (38 locks, and 39 at the end of this review as
other flows acquired). Nothing else was touched.

## 0.30.0 writes the store

    $ orchestrate-0.30.0/bin/orchestrate-nexus   # XDG redirected to scratch
    orchestrate-nexus ready
    $ ls -la /tmp/o6d/orchestrate-nexus/
    srwxr-xr-x 1 li users 0 meta-orchestrate.sock
    srwxr-xr-x 1 li users 0 orchestrate.sock

    $ orchestrate-0.30.0/bin/orchestrate 'Lock.{ CarriedOne f6db8d [ /carried/one ] “carried across the cutover” }'
    Locked.{ 1 CarriedOne f6db8d [ /carried/one ] “carried across the cutover” }
    $ orchestrate-0.30.0/bin/orchestrate 'Lock.{ CarriedTwo f6db8d [ /carried/two ] second }'
    Locked.{ 2 CarriedTwo f6db8d [ /carried/two ] second }

Note the 0.30.0 client accepts and emits U+201C/U+201D curly quotes.

## Both wire directions refuse across the endianness change

    $ ORCHESTRATE_SOCKET=/tmp/o6d/... orchestrate-0.32.0 'Observe.Locks'   # 0.32 client -> 0.30 Nexus
    Unreachable.{ /tmp/o6d/orchestrate-nexus/orchestrate.sock «Signal frame: Signal frame I/O failed: failed to fill whole buffer» }

    $ orchestrate-0.30.0/bin/orchestrate 'Observe.Locks'                   # 0.30 client -> 0.32 Nexus
    orchestrate: bound Signal frame validation failed: UnboundHeader

## 0.32.0 opens the 0.30.0 store and cuts over

    $ orchestrate-0.32.0/bin/orchestrate-nexus   # same XDG, same store
    orchestrate-nexus ready
    $ ls -la /tmp/o6d/orchestrate-nexus/
    srw------- 1 li users 0 meta-orchestrate.sock
    srw-rw---- 1 li users 0 orchestrate.sock

    $ orchestrate 'Observe.Locks'
    Observed.Locks.[ { 1 CarriedOne f6db8d [ /carried/one ] «carried across the cutover» } { 2 CarriedTwo f6db8d [ /carried/two ] second } ]

Locks, their ids and their reasons carried across untouched; the allocator
carried too (the next Lock took id 3, continuing 0.30.0's sequence).

## The Datom string delimiter changed

    $ orchestrate 'Lock.{ AfterCutover f6db8d [ /after/cutover ] “post-cutover lock” }'
    Unreadable.Error.{ Composition [ 1 ] Arity.{ 4 5 } }
    $ orchestrate 'Lock.{ AfterCutover f6db8d [ /after/cutover ] «post-cutover lock» }'
    Locked.{ 3 AfterCutover f6db8d [ /after/cutover ] «post-cutover lock» }
    $ orchestrate 'Lock.{ AfterCutover3 f6db8d [ /after/three ] bare }'
    Locked.{ 4 AfterCutover3 f6db8d [ /after/three ] bare }

## Lock refusals, release, empty observation

    $ orchestrate 'Lock.{ CarriedOne f6db8d [ /other ] again }'
    LockRejected.DuplicateName.{ 1 CarriedOne f6db8d [ /carried/one ] «carried across the cutover» }
    $ orchestrate 'Lock.{ Other f6db8d [ /carried/one/deeper ] overlap }'
    LockRejected.PathOverlap.{ /carried/one/deeper { 1 CarriedOne f6db8d [ /carried/one ] «carried across the cutover» } }
    $ orchestrate 'Release.1'
    Released.{ 1 CarriedOne f6db8d [ /carried/one ] «carried across the cutover» }
    $ orchestrate 'Release.9999'
    ReleaseRejected.UnknownLockId
    $ orchestrate 'Observe.Locks' | cat -A
    Observed.Locks.[]$

## The full configuration lifecycle, over both sockets

    $ orchestrate "Configure.{ <ordinary> <meta> }"
    ConfigurationAccepted.{ { <ordinary> <meta> } False }
    $ orchestrate 'Configure.{ relative.sock /abs/meta.sock }'
    ConfigurationRefused.{ InvalidConfiguration }
    $ orchestrate-meta "Configure.{ <ordinary> <meta> }"
    Configured.{ { <ordinary> <meta> } True }
    $ orchestrate "Configure.{ <ordinary> <meta> }"
    ConfigurationRefused.{ MetaConfigureOccurred }
    $ orchestrate-meta 'ReverseMetaConfiguration'
    OrdinaryConfigurationReopened.{ { <ordinary> <meta> } False }
    $ orchestrate "Configure.{ <ordinary> <meta> }"
    ConfigurationAccepted.{ { <ordinary> <meta> } False }
    $ orchestrate-meta 'Configure.{ nope /abs/meta.sock }'
    ConfigurationRejected.{ InvalidConfiguration }

## Configure repoints the sockets at the next start, and strands the old paths

    $ orchestrate "Configure.{ /tmp/o6d/alt-o.sock /tmp/o6d/alt-m.sock }"
    ConfigurationAccepted.{ { /tmp/o6d/alt-o.sock /tmp/o6d/alt-m.sock } False }
    # running instance keeps its bindings; restart:
    $ ls -la /tmp/o6d/
    srw------- 1 li users 0 alt-m.sock
    srw-rw---- 1 li users 0 alt-o.sock
    drwxr-xr-x 2 li users   orchestrate-nexus        # still holds both dead socket files

## Binding comes from the store, not from XDG

A copy of the real live store, placed under a scratch `XDG_STATE_HOME` with a
scratch `XDG_RUNTIME_DIR`, made the 0.32.0 Nexus attempt the production paths:

    $ XDG_STATE_HOME=<scratch> XDG_RUNTIME_DIR=<scratch> orchestrate-0.32.0/bin/orchestrate-nexus
    orchestrate-nexus: an Orchestrate Nexus already owns socket "/run/user/1001/orchestrate-nexus/orchestrate.sock"

It was refused only because the live Nexus held the socket. This also witnesses
that the cutover read the real deployed 0.30.0 store's configuration row.

## The peer refusal, end to end

`/etc/subuid` grants `li:100000:65536`, so an unprivileged user namespace yields
a genuinely different kernel uid. The scratch meta socket was chmod'ed 0666 for
this one exchange, because its 0600 mode otherwise refuses the `connect(2)`
before the check is reached; it was restored to 0600 afterwards.

    $ unshare --user --map-users=1000:100000:1 --map-groups=1000:100000:1 --setuid 1000 --setgid 1000 -- id
    uid=1000(bird) gid=1000 groups=1000
    # writes as this identity land as outer uid 100000; /tmp/o6d (0755, owned by li) refuses them.

    $ unshare ... -- socat -u UNIX-CONNECT:/tmp/o6d/orchestrate-nexus/meta-orchestrate.sock - | od -An -tx1
     00 00 00 12 03 a0 86 01 00 00 00 00 00 00 00 00
     00 00 00 00 00 00

Big-endian prefix 0x12 = 18 body bytes; discriminant `03` is `PeerRefused`, the
fourth `Response` variant; `a0 86 01 00` little-endian is 100000, the peer's uid.
No frame was sent by the peer — the refusal precedes the first read.

## The Datom-free Nexus, on the binary rather than on the resolution

    $ cargo build --package orchestrate-nexus --target-dir /tmp/o6-nexusonly
    $ strings -a /tmp/o6-nexusonly/debug/orchestrate-nexus | grep -c 'datom_codec\|datom-codec\|protos'
    0
    $ nm -C /tmp/o6-nexusonly/debug/orchestrate-nexus | grep -i 'datom\|protos'
    # 39 hits, every one a false positive on "Atomic" inside sema_engine symbol names

    $ strings -a <workspace-resolution build>/orchestrate-nexus | grep -c 'datom_codec\|datom-codec'
    1240

    $ cargo tree --package orchestrate-nexus --edges normal --locked --offline | grep -c 'datom-codec\|protos v'
    0
    $ cargo tree --package orchestrate --package orchestrate-meta --edges normal --locked --offline | grep -c 'datom-codec\|protos v'
    10

## The repository's own gate, run locally

`cargo test --workspace --all-targets` at `054ce581`: 23 tests, 0 failures,
including `store::cutover::tests::a_previous_generation_store_carries_its_
configuration_and_its_locks`, the three `configuration_authority` tests, and all
six `live_nexus` tests (`observe_delivers_the_state_on_open_and_every_later_
change`, `a_little_endian_prefix_is_not_the_shared_frame`,
`the_privileged_socket_is_bound_for_its_owner_alone`,
`malformed_archive_never_reaches_the_store`,
`nexus_serves_both_typed_sockets_and_resumes_state`,
`nexus_rejects_arguments_without_opening_state`).

## Deployment-check probes

    $ orchestrate-upgrade-preflight            # 0.32.0, fresh XDG
    active legacy PathLock rows: 0             # identical to 0.30.0, and creates no store
