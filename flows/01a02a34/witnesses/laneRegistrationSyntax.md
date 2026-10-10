# Lane registration syntax

Method: subflow probe of the current `meta-orchestrate` and `orchestrate`
commands on `PATH`, resolving to the Nix `orchestrate-0.20.0-profile`, during
2026-08-22 flow `01a02a34`.

The registration form copied literally from `orchestrate/AGENTS.md:58` failed
before transport:

```text
meta-orchestrate: invalid meta orchestrate request Dotos: expected LaneRegistrationRequest to be a brace block
```

The corrected form passed parsing and reached transport:

```text
meta-orchestrate '(Register {{NewLanesDesign newLanesDesign {{[NewLanesDesign Designer]} Structural} (refresh coordination docs)} Fresh})'
transport error: ... No such file or directory (os error 2)
```

The documented Claim and Release forms failed because `RoleClaim` and
`RoleRelease` were expected to be brace blocks. Their corrected forms reached
the same missing-socket transport boundary:

```text
orchestrate '(Claim {laneName [Path./absolute/path] (why you are editing)})'
orchestrate '(Release {laneName})'
```

The documented Retire form failed because `Retirement` was expected to be a
unit-variant atom or `Variant.payload` application block. The corrected form
reached transport:

```text
meta-orchestrate '(Retire Lane.laneName)'
```

These probes witness parser acceptance by the current CLI only. No daemon
socket existed, so registration, claim, release, retirement, and reply records
were not exercised against a live daemon.

