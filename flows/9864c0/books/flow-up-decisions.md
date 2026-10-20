# Flow up: decisions as made (source; published by the book subflow)

1. "Main aspects" for Primaries and Tertiaries is read as Psyche, Mind and Field, each on topic core.
2. Psyche core Primary: wake Fable 39bd0c if its context is under the refresh threshold (15% or 100,000 tokens); otherwise start a fresh Fable successor.
3. Field core Secondary 42265e is kept if its pane is live; a successor is started only if it is dead.
4. A failed start is fixed in Flow or the messenger when the fix is small, committed in that repository, then retried.
5. Roster found complete: all nine core cells live (Psyche 9864c0/39bd0c/4201a3, Mind 41fa34/0c85a3/6f2dce, Field 42265e/44cda5/4a16cc). Psyche core Primary stays Fable 39bd0c (about 10% context, under threshold); a duplicate successor was started by mistake, failed registration and was closed.
6. Flow implementation goes to Mind core Secondary with the gap list; decisions inside it go to Fable 39bd0c.
7. A second stray 'nix profile remove' of the Flow and messenger packages (started 15:40) is stopped; services keep running from Home-unit store paths, not the profile.
