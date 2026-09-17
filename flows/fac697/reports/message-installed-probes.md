# Installed Message 0.11.1 live probes

These probes exercised the live ordinary Message socket at
`/run/user/1001/message/message.sock` with the exact installed client:

```text
/nix/store/2yspp3zdfymnml9ff1msdzrdi3bs0q6j-message-0.11.1/bin/message
```

Its derivation source is
`/nix/store/93bgbzas5klix318pknjgb84g1kvp0qs-source`. That source pins
`signal-message` 0.8.1 at
`dff3fbf3f9e2cd018f06bcf96a06c8367d3e7f31` and accepts these nine ordinary
inputs: `Submit`, `SubmitStamped`, `QueryInbox`, `AssignAgentIdentity`,
`BindAgentEndpoint`, `QueryAgentRegistry`, `QueryThread`, `SubscribeThread`,
and `QueryThreads`.

Set the common command boundary as follows:

```sh
MESSAGE_BIN=/nix/store/2yspp3zdfymnml9ff1msdzrdi3bs0q6j-message-0.11.1/bin/message
export MESSAGE_SOCKET=/run/user/1001/message/message.sock
```

## Successful stateful probe

The endpoint probe used only the deliberately seated
`fac697-input-probe` identity. A temporary Unix listener existed at the named
path. PID `3261659` was live, and `/proc/3261659/stat` field 22 was
`62002006`, when the binding request ran:

```sh
"$MESSAGE_BIN" 'BindAgentEndpoint.(fac697-input-probe (HarnessSocket /tmp/fac697-input-probe.sock) 3261659 62002006)'
# AgentEndpointBound.fac697-input-probe

"$MESSAGE_BIN" 'QueryAgentRegistry.ByAgent.fac697-input-probe'
# AgentRegistryListing.([(fac697-input-probe Bound.(HarnessSocket /tmp/fac697-input-probe.sock) None NotDead Pinned.(3261659 62002006))])
```

The listener was then killed, its socket removed, and the probe identity
reseated to clear its stale endpoint:

```sh
"$MESSAGE_BIN" 'AssignAgentIdentity.(fac697-input-probe None None)'
# AgentIdentityAssigned.(fac697-input-probe Reseated)

"$MESSAGE_BIN" 'QueryAgentRegistry.ByAgent.fac697-input-probe'
# AgentRegistryListing.([(fac697-input-probe None None NotDead None)])
```

The numeric PID and start ticks above are a completed witness, not reusable
values. A future binding probe must start a fresh listener and read that
process's current PID and `/proc/<pid>/stat` field 22.

The earlier successful thread subscription made the thread query a positive
read rather than an intentional absence:

```sh
"$MESSAGE_BIN" 'QueryThread.fac697-input-thread'
# ThreadListing.(fac697-input-thread None [fac697-input-probe] [])

"$MESSAGE_BIN" 'QueryThreads.All'
# ThreadIndexListing.([(fac697-input-thread None [fac697-input-probe] 0) (thread None [participant] 0)])
```

## Complete installed input surface

The remaining commands and their live typed outcomes are:

```sh
"$MESSAGE_BIN" 'Submit.(fac697-input-probe Send (variant probe) None)'
# SubmissionRejected.StoreRejected

"$MESSAGE_BIN" 'SubmitStamped.((fac697-input-probe Send (variant probe stamped) None) External.Owner 1)'
# MessageRequestUnimplemented.(SubmitStamped NotInPrototypeScope)

"$MESSAGE_BIN" 'QueryInbox.fac697-input-probe'
# InboxListing.([])

"$MESSAGE_BIN" 'AssignAgentIdentity.(fac697-input-probe None None)'
# AgentIdentityAssigned.(fac697-input-probe Seated)

"$MESSAGE_BIN" 'QueryAgentRegistry.ByAgent.fac697-input-probe'
# AgentRegistryListing.([(fac697-input-probe None None NotDead None)])

"$MESSAGE_BIN" 'SubscribeThread.(fac697-input-thread fac697-input-probe None)'
# ThreadSubscribed.(fac697-input-thread fac697-input-probe)
```

`QueryAgentRegistry.ByAgent.fac697-input-probe` now consistently returns the
seated row; the earlier empty keyed listing did not reproduce. In contrast,
the registry-wide query currently refuses:

```sh
"$MESSAGE_BIN" 'QueryAgentRegistry.All'
# AgentRegistryRejected.StoreRejected
```

The installed source maps any failure while scanning all registry records to
this reply, while the keyed read succeeds. An incompatible or otherwise
unreadable legacy row is one plausible explanation, but this probe did not
inspect or mutate unrelated registry rows and does not establish that cause.

`Submit` remains a live store rejection and `SubmitStamped` remains explicitly
outside prototype scope. They are wire/parser witnesses, not successful
message submissions. The successful functional examples are inbox read,
identity assignment/reseat, live endpoint binding, keyed registry read,
thread subscription, existing-thread read, and thread-index read.
