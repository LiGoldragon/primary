# Ouranos deployment witness

Method: daemon-free Lojix 6 BuildOnly with `max-jobs = 0`, configured Prometheus builder, immutable public CriomOS source, externally composed regular Horizon definition, then matching Lojix 6 owner submission and ordinary terminal queries. Runtime checks were read-only after activation.

- BuildOnly: `(BootstrapTerminal.Succeeded)`; rooted closure `/nix/store/41cvi7l9rjy3n05jixzqdk937rg8gz27-nixos-system-ouranos-26.11.20260813.0e251e2`.
- Deployment 4: immutable `36653a125de8f14518af2dddf89333610891d140`, `CompleteHost`, `ActivateNow`, terminal `Completed ... Some.Succeeded`.
- `/run/current-system` and `/nix/var/nix/profiles/system` both resolve to the rooted closure.
- `lojix.service` is active/running; `/run/lojix/ordinary.sock` is 0660, `/run/lojix/meta.sock` is 0600; journal contains `(LojixNexusReady /run/lojix/ordinary.sock /run/lojix/meta.sock)`; `Query.ByNode` identifies deployment 4 as Current.
- GeoClue is active/running. `/etc/geoclue/geoclue.conf` has static source enabled. Root read of `/etc/geolocation` is exactly `16.736944`, `-92.637500`, `2121.000000`, `1000.000000` and the file is 0440 root:geoclue.
- Chroma 0.7.1 is active from `/nix/store/4rws7vjy4sf3zdi4c26vlqgyl8pbx34c-chroma-0.7.1`. `GetState` returned `State.{ Light 6500 85 }`; `GetSolarClock` returned `SolarClock.{ -22017 1789257600 }`.
- GammaRelay reported temperature `6500` and brightness `0.85`. Chroma's Emacs projection reported `Applied`, revision 44.
- li's Home profile resolves to `/nix/store/yqnl3980wa8ghjnislpsghs0879q88cz-home-manager-generation`.
- No reboot and no store reset occurred. The original Lojix archive, v5 source, and prior default-path store remain preserved in the private deployment evidence directory.
