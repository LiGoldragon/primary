# The observed ChatGPT freeze is an i915 GPU-reset failure, not an OOM

The strongest direct cause of the launch freeze is Intel i915 GPU hangs and
context resets in the ChatGPT Electron process tree. Three resets occurred
within 57 seconds of launch. The replacement GPU process and all observed
renderers force the Electron X11 backend, even though Niri is a Wayland
compositor. This makes the reported full-display-height, clipped non-fullscreen
window a credible XWayland/Niri geometry-path symptom rather than evidence of
a Home profile or MIME-registration fault.

Memory exhaustion is ruled out for the observed period: the ChatGPT cgroup
peaked near 2.12 GiB but recorded neither OOM nor memory pressure. There is a
separate severe host-wide I/O-stall condition, with I/O full pressure near 89%.
It can worsen responsiveness, but it is not attributable to the ChatGPT cgroup
from the available accounting and is weaker than the timestamped GPU-reset
evidence as an explanation of the launch freeze.

The later interaction freeze should not be described as a first-run migration:
it happened after the application was open. Its precise event is still unknown
because no later i915-reset, renderer-crash, or OOM journal line was observed.
The retained X11 GPU path remains the leading hypothesis for that recurrence,
with global I/O pressure as a concurrent risk factor.

No source, configuration, desktop state, or deployment was changed.

## Sources

- [Read-only diagnosis witness](../witnesses/officialChatgptFreezeDiagnosis.md)
- [Official ChatGPT correction deployment witness](officialChatgptCorrectionDeployment.md)
