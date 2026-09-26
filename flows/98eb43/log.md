
Living, typed:
"No, I asked you what's missing for a future version of you to not miss out, and why have you not started logging now?"

Living, relayed via #msg from da88cf (Psyche Fable, heading tonight's integration), by the living's word at ~22:05:
"From now on no Nix builds and no Nix tests on ouranos by any flow — every Nix build and check runs on Prometheus, which is powered on and reachable again (the declared builder in /etc/nix/machines; ouranos max-jobs is 0). Do not raise max-jobs, do not pass --builders '' or --max-jobs N>0, do not run cargo/bb/clojure test suites as a substitute for a Nix check on ouranos. If a remote build fails, report the exact error to da88cf instead of building locally. Anything you hotfixed around Prometheus's absence (local builds, pins, overrides, drop-ins): send da88cf the list; tonight each is integrated as a declared feature or discarded. The Tailscale/Headscale repair is da88cf's by the living's word; do not act on it independently."

Living, relayed via da88cf, 2026-09-25 ~22:05, to 88475f, before sleeping; corrected "next"->"Nix", "Uranus"->"ouranos":
"Okay well, you can get that Tailscale problem figured out and fixed. Make sure you follow the topology of the cluster, data, and administrator roles and features in order to add data in order to know which host does what. I leave it to Fable's best judgment because I'm going to sleep and I want this to be done. You can present me with what has been done afterwards but I want you to stop doing [Nix] builds and [Nix] tests on [ouranos] and move everything to Prometheus now."
