# CriomOS live installer architecture review

The living requested a review of CriomOS, CriomOS-home, Horizon cluster data, and Lojix: module gating, minimal live installation images, externally supplied synthetic nodes, package organization, historical preOS support, and upstream Nix implementations. This flow investigates and develops a proposal in conversation; implementation has not been approved.

Setup witnesses located the relevant repositories and the primary embedded Beads store. Existing dirty work belongs to flow 4a8046. Its preservation lock was rejected because lock 771 owns that path; no change was made to that work. This flow writes only its separately reserved lane and index entry while the other flow retains ownership.

Raw vision was recorded before substantive investigation. The living corrected the speech-to-text names to CriomOS and Lojix.
