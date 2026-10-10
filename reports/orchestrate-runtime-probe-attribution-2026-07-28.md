# Orchestrate runtime probe attribution — 2026-07-28

Exact package: Orchestrate `0.18.0`, revision `0f7c1570896e`.

## Attribution

| Probe | Cause | Removal status |
| --- | --- | --- |
| `/proc/self/maps` | glibc `pthread_getattr_np`, called by Rust `std::rt::lang_start_internal` before `main` | No ordinary feature switch found; not caused by Orchestrate, Tokio, Sema, redb, or telemetry. |
| `/proc/self/cgroup` | Rust `available_parallelism`, called by Tokio `Runtime::new()` to choose the worker count | Avoidable with one explicit Tokio worker. |
| `/sys/devices/system/cpu/online`, `/proc/stat` | glibc allocator CPU discovery while Tokio worker threads start | Absent with one Tokio worker; independently avoidable with `MALLOC_ARENA_MAX=1`. |
| `/etc/ld-nix.so.preload`, Nix glibc `etc/ld.so.cache` | glibc dynamic loader before Rust `_start` | Present for the dynamically linked ELF; static packaging is unproven. |

`strace -k` supplied the named call stacks. The exact source and lock contain
no custom allocator, telemetry exporter, or direct use of these host paths.
Sema/redb cannot cause the probes because Tokio runtime construction occurs
before daemon binding and store opening.

## One-worker witness

Running the exact package with one Tokio worker inside an empty-root sandbox
removed the cgroup, sysfs CPU, and `/proc/stat` probes. The daemon reached all
three socket-ready paths and served `Observe Roles`.

`MALLOC_ARENA_MAX=1` alone removed the allocator CPU probes but retained the
Tokio cgroup probe. It is therefore not the preferred primary correction.

## Remaining boundary question

Use an explicit one-worker Tokio runtime and repeat the complete isolated
state-only witness. The remaining `/proc/self/maps` and dynamic-loader `/etc`
probes are pre-main platform startup behavior. Removing them would require a
proven static/runtime packaging change or an explicit ruling that pre-main
loader/runtime startup lies outside Orchestrate's component-owned behavior.
