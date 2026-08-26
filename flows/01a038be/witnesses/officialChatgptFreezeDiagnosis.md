# Official ChatGPT freeze diagnosis witness

Method: strict BatchMode SSH as `li` to the established Ouranos endpoint;
read-only `/proc`, cgroup v2, PSI, journal, Niri IPC, and application-profile
metadata probes. The application was neither relaunched nor terminated. No
prompt, conversation, token, callback, credential, or application-log content
was read.

## Direct observations

The official ChatGPT launch created its primary process at `13:42:37`.
Kernel journal records show three Intel i915 GPU hangs in ChatGPT processes:

```text
13:42:55 GPU HANG … in .ChatGPT-wrappe [4082328]
13:42:55 … context reset due to GPU hang
13:43:03 GPU HANG … in .ChatGPT-wrappe [4083060]
13:43:03 … context reset due to GPU hang
13:43:34 GPU HANG … in .ChatGPT-wrappe [4083437]
13:43:34 … context reset due to GPU hang
```

The surviving GPU process was started at `13:43:33`, between the second and
third reset. It is an Electron GPU process with `--ozone-platform=x11` and
`--use-gl=disabled`. The renderer processes also explicitly pass
`--ozone-platform=x11`, although the user session exports both Wayland and X11
display endpoints. The session compositor is Niri, which owns the
GNOME-compatible display D-Bus interface; no relevant Mutter/Shell journal
message was recorded.

Niri reports one non-floating `Chatgpt` window using a logical
`1536 × 960` tile, exactly the logical size of the sole output at scale `1.25`.
Other ordinary tiled windows reported `1520 × 910.4`. This agrees with the
living's visual report that the application occupies full output height while
not in true fullscreen. The window record advertises PID `21333`, unlike the
new launch's primary PID, so this probe corroborates the geometry symptom but
does not by itself bind that particular Niri record to the new process tree.

At `13:48`, the ChatGPT cgroup held about `1.38 GiB` and had peaked at about
`2.12 GiB`. Its memory events showed zero `oom` and `oom_kill`, and its CPU,
memory, and I/O PSI values were all zero. The cgroup had cumulatively read
about `906 MB` and written about `497 MB`; the short sample showed no active
per-process writer over `1 MiB` in five seconds.

The host simultaneously had severe global I/O pressure: I/O `some` was about
`96%` and I/O `full` about `89%` over the preceding minute. This persisted
across a five-second sample, while NVMe traffic was modest and the ChatGPT
cgroup itself had zero I/O pressure. A kernel `i915_flip` worker was in D state
at the time of observation. There was no OOM kill, NVMe error, filesystem
error, renderer crash, or new GPU-hang line after `13:43:34` in the inspected
`13:40`–`13:52` journal window.

The application profile created cache/database log metadata at launch time;
only names, sizes, and timestamps were inspected. No profile-migration file
was observed and no log contents were read.

## Limits

The host does not provide `xprop`, `xwininfo`, or XRandR utilities, so direct
XWayland window-property inspection was unavailable. Niri IPC supplies the
safe geometry witness but not surface-buffer or damage history. The later
ordinary-interaction freeze has no separate matching post-`13:43:34` kernel
reset record, so its exact event-level mechanism remains unproven.
