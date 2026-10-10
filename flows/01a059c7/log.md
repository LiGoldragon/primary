# Disk space recovery

The flow is remembering prior disk-space work, cleaning all understood build directories across the configured local trees, deleting obsolete generations from every Nix profile (root SSH for the system profile), garbage-collecting Nix, surveying further reclaimable space, and proposing a reusable reclaiming skill.

Settled: current profile generations, the active system, and boot state remain while obsolete generations are removed.

Remembered: 019f9f38, 019fc976, 019fd886 — depth 1. Prior build, transcript, profile, and GC cleanups; active builds regenerated outputs, and the legacy chains have no flow directories. Their relevant last responses were read.

Remembered: 01a038c9, 1ebea3fb — depth 2. Measured repository cleanup preserved ambiguous managed state and separated apparent deletion size from filesystem free-space change. The parent last response was read; no standalone child transcript was found.

Settled: all validated Cargo and Vite build outputs found in repository, worktree, and temporary trees were removed while active processes and generated evidence trees were preserved. Obsolete system and Home Manager generations were removed; current generations remain. The proposal should revise the existing disk-hygiene skill rather than create an overlapping skill.

Settled: final verification passed. The flow removed 42 Cargo targets, two ignored JavaScript dist outputs, 74 Cargo output roots in temporary storage, and 21 Vite build outputs; it removed 19 obsolete system and 30 obsolete Home Manager generations and completed root Nix garbage collection. Current/booted system 177, Home Manager 989, and default profile 1996 remain. Free space rose from 118,865,735,680 bytes to 466,085,695,488 bytes.

Settled: the post-GC survey separates regenerable caches from durable transcripts, downloads, captures, application data, and operating-system images. It found 18,412,355,584 apparent bytes across 190 ambiguous temporary workspaces and did not classify them as safe. The proposed skill revision adds provenance, liveness, per-owner Nix cleanup, and post-cleanup verification to disk-hygiene without creating a competing skill.

Settled: system boot entries 159 and 162 remain usable rollback closures. Entries 158, 160–161, and 163–176 have missing init paths after GC and are cleanup candidates through supported bootloader regeneration, not direct deletion. No prior Home Manager rollback remains.

Open: none for the requested cleanup. Further cache, journal, personal-data, and application-data removal requires category-specific authorization or a retention decision.
