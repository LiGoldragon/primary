Summary

Chroma 0.2.5 and Noctalia 5.1.0 are implemented, remotely checked, pinned, and live through Lojix Home generation 971. Chroma is the sole appearance authority; Noctalia external mode, the portal, and GTK resolve Dark, and restart-safe warmth recovery is deployed. GeoClue still supplies only rejected 26 km fixes, so Chroma is explicitly unlocated and automatic solar scheduling remains unavailable. A generic local-only stateful location override has been explained but not authorized or implemented; no location value is in Nix or Git.

Findings and progress

- The live gamma relay is active on `eDP-1` at 2700 K, brightness 0.85, gamma 1. No competing redshift/gammastep/wlsunset process was observed.
- `wl-gammarelay-rs` failed twice before the Wayland environment existed, then recovered after Niri. Chroma initially could not reach the relay. This confirms a startup race that can preserve stale gamma state, but does not yet prove the setter of the current 2700 K value.
- Chroma is accepting GeoClue fixes with approximately 26 km accuracy. Current Chroma validates freshness and finiteness but does not reject poor accuracy. Its derived solar-clock offset differs by about 14.7 minutes from the caller-provided reference locality, more than a genuinely nearby 26 km uncertainty should normally produce. An unmerged Chroma branch rejects IP fallback and accuracy worse than 1 km; it is evidence, not the selected fix.
- Noctalia separately reports no usable automatic-location schedule and a location cache whose latitude/longitude fields are strings rather than numeric values. No coordinate values were persisted or reported.
- Chroma owns solar warmth plus GNOME/GTK theme application. Live state is partially inconsistent: Chroma says light and dconf says `prefer-light`, while GTK and icon themes remain dark.
- Chroma's configured 60-minute ramp begins 60 minutes before civil dusk and ends at civil dusk; for the reference locality on 2026-08-19 that is approximately 20:33–21:33 CEST. `Warmest` maps to 2700 K. The observed relay state is already 2700 K, but physical output and its last successful writer remain unwitnessed.
- Noctalia owns the status bar under Niri and selects its palette independently from wallpaper state. Its status-notifier host is registered but currently sees zero registered items. Chrome was not running, so live Chrome behavior remains unverified.
- The clarified symptom is theme state, not tray state. Chroma's live IPC reports Dark and Warmest/2700 K, while Noctalia independently resolves `auto` to light because it has no usable location. Noctalia writes `prefer-light` to the shared GNOME color-scheme key; dconf and the Settings portal both serve that light value to libadwaita/GTK and potentially Chrome, overwriting Chroma's dark color-scheme write while Chroma's separate GTK theme files remain dark.
- Chroma persists the final warmth target before starting interpolation. Startup recovery directly reapplies that stored target, and schedule reconciliation skips a transition whose target already equals stored state. A restart during the evening ramp can therefore apply 2700 K immediately and omit the remaining interpolation; the observed relay/Chroma D-Bus startup failures make this a strong explanation for a prematurely full-red screen.
- No written psyche ruling addresses these mechanisms. Existing Vision requires setup-independent general repositories and permits mutable Noctalia values to be overridden statefully through Helix. The caller's location and investigation-only constraint are task context, not new psyche rulings.

Open questions

- The exact last relay writer is not journaled, although Chroma's persistence/recovery semantics explain how it can retain and reapply 2700 K prematurely.
- Why Noctalia serialized its cached coordinates with the wrong type and whether that cache participates in the actual gamma command path.
- Chrome's exact system-theme consumption path remains unwitnessed; no authored Chroma/Chrome bridge exists.

No implementation, deployment, settings mutation, service restart, application launch, or committed location override is authorized in this investigation round.

Implementation authorization and design

- The psyche authorized implementation and redeployment of the user environment through Lojix if the way is clear, followed by live verification.
- The psyche ruled: “noctalia shouldnt be in charge of deciding the light/theme anywhere, it should be yielding to chroma's effects”. The ruling is recorded in `psyche/Vision/noctalia.md`.
- Recommended ownership: Chroma alone decides light/dark and publishes it through the standard Settings portal projection; a new Noctalia external/system mode subscribes to that projection, renders the wallpaper palette in the supplied variant, and never writes the global color-scheme or runs a solar decision.
- Recommended warmth repair: persist target separately from successfully applied/projected warmth; on restart derive the current schedule projection and remaining ramp before writing the relay. Target equality must not suppress an unfinished transition.
- No safe current stateful location override API exists. Location-quality rejection and fallback must remain Chroma-owned; no location enters authored or committed configuration.
- Implementation is tracked by claimed Chroma bead `chroma-zbf`. Source work has not begun.

Open ruling before implementation

- In Noctalia external mode, behavior before the first portal value: retain the last observed external mode when available, with a first-run fallback still to be ruled.
- Chroma location quality: whether to reject fixes worse than a threshold such as 1 km, retaining a last good fix and remaining explicitly unlocated when none exists.

Addendum — integrate_deploy, 2026-08-20

Implemented and deployed

- The psyche approved the proposed fallbacks. Chroma 0.2.5 landed at `eea85f4aae5a`: fixes worse than 1 km are rejected, last-good/unlocated authority is explicit, and warmth persistence separates desired, confirmed-applied, projected, and transitioning state. Legacy warmth state is never replayed; restart and failed-relay regressions are tested.
- Noctalia 5.1.0 landed at fork commit `9778437e8bd326d6d82340fff6b0400eee2caf6f`: `external` mode consumes the portal appearance signal, keeps the wallpaper palette, retains last observed external mode with first-run Dark, and does not write the global color-scheme.
- CriomOS-home `ad0958adbd65892daa69af94829d8c0b982cb305` pins both producers, selects external/wallpaper/m3-rainbow, and uses Hexis to reconcile only mutable `/theme/mode` to `external` with `always`. CriomOS `9b8b06438f0e955390f57f71e937f63b70752ed6` pins that Home commit.
- Remote producer and focused consumer checks passed. The broad Noctalia suite ran 79/81; its new external-appearance test passed, while two unrelated pre-existing/non-hermetic tests failed. A dedicated remote `external-appearance` Nix check passed 1/1.
- Lojix activation request 22 completed by journal witness. Home generation 971 is active. Live Noctalia is 5.1.0 and resolves Dark; dconf and portal report dark; GTK3/4 request dark. Live Chroma is 0.2.5 and reports Dark/2700 K/85%; the gamma relay is active. Chrome was not running and remains unverified.
- The first activation exposed a stale mutable `auto` override. Hexis corrected only that leaf, Chroma republished Dark through its supported reapply path, and the durable Home reconciliation was then deployed. No manual dconf theme write or committed location occurred.

Residual location boundary

- GeoClue 2.8.1, NetworkManager, wpa_supplicant, and the declared BeaconDB Wi-Fi endpoint are active, but every fix is approximately 26 km. Chroma correctly rejects them and remains explicitly unlocated.
- The GeoClue IP-source `(null)` warning is optional-backend noise; suppressing it would not improve accuracy. Safe evidence cannot establish nearby BeaconDB coverage or inspect Wi-Fi scan payloads. No declarative service change is justified without a provider/privacy/hardware decision.
- Automatic solar scheduling is therefore unavailable. A generic Chroma-owned stateful location-override interface does not currently exist; adding and using one is an open product/authority decision. No location value is committed or persisted.
- Bead `chroma-zbf` remains open because live automatic transition/recovery is not fully proved while Chroma is unlocated. Ordinary Lojix Query remains broken by its known wire-shape panic; request admission, terminal journal, and active profile are the deployment witnesses.

Latest handoff — integrate_deploy, 2026-08-20

- The psyche asked for an explanation of the proposed temporary stateful location override; this did not authorize implementation.
- Proposed anatomy: Chroma exposes privileged `SetLocationOverride` and `ClearLocationOverride` operations; the override is stored only in Chroma's mutable local state, survives daemon restart, takes precedence while set, recomputes solar schedules immediately, and yields back to GeoClue only when cleared. The stored value should be municipality-level rather than a personal address and must never enter logs, Nix, Git, or deployment requests.
- The interface does not yet exist and no location override is currently stored. Chroma remains explicitly unlocated. Live theme state remains Dark; Chrome itself was not running during verification.

External `01a020ff` Emacs investigation and its correction are recorded in
`annotations.md`.
