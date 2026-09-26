# Prometheus

## We need to use Prometheus

Context: said to 88475f after hearing that ouranos builds locally because it cannot reach Prometheus (Field: tailscaled logged out, Headscale self-signed cert rejected). Relayed to da88cf by 88475f.

> Why was it working before? Would it help if I rebooted it? We need to use Prometheus.

-- psyche, STT, 2026-09-25 ~21:50, to 88475f.

## Here I'm rebooting him now

Context: said to 88475f two minutes after asking whether a reboot would help; "him" is Prometheus. Relayed to da88cf by 88475f.

> Here I'm rebooting him now.

-- psyche, STT, 2026-09-25 ~21:52, to 88475f.

## It wasn't even running

Context: correcting the reboot notice, to 88475f; the living went to the machine and found Prometheus powered off, then started it. Relayed to da88cf by 88475f.

> Well I haven't rebooted it. Should I? Do you have any way to talk to Prometheus? Is it turned off? Well there you go. That's the problem.

-- psyche, STT, 2026-09-25 ~21:55, to 88475f.

> So I started it. Now that should help. It wasn't even running. I guess we had a power outage or something.

-- psyche, STT, 2026-09-25 ~21:57, to 88475f.

## Move all the building to Prometheus

Context: to 88475f, after powering Prometheus on. Relayed to da88cf by 88475f.

> Give it, I don't know, 30 seconds. You should be able to test it. Make sure we move all the building to Prometheus and get all the fixes deployed to it.

-- psyche, STT, 2026-09-25 ~22:00, to 88475f.

## Move everything to Prometheus now

Context: to 88475f, before sleeping. Relayed to da88cf by 88475f. Full statement in vision/clusterData.md.

> ... I want you to stop doing [Nix] builds and [Nix] tests on [ouranos] and move everything to Prometheus now.

-- psyche, STT, 2026-09-25 ~22:05, to 88475f. Transcription corrected: "next" → "Nix", "Uranus" → "ouranos".

## Prometheus should be doing the builds

Context: to 88475f, refining the build-host order a few minutes after giving it. Relayed to da88cf by 88475f.

> You can't really write down literally the skills but we're moving back to remote builders. Of course you can fall back to local building but I guess you don't have a way to wake me up if something goes wrong. I'll hear the laptop running because it's next to me. Prometheus should be doing the builds and running the fan hard so I shouldn't hear my laptop run really hard most of the time.

-- psyche, STT, 2026-09-25 ~22:08, to 88475f.

## Prioritize Nix builds for everything

Context: to 88475f, ~2 minutes after the build-host refinement. Relayed to da88cf by 88475f. Transcription corrected by 88475f: "Nick's" → "Nix".

> We should prioritize using [Nix] builds for everything. That way we maximize the remote building aspect and maybe you can get a low-powered subflow to make sure Prometheus has lots of disk space by garbage collecting and cleaning up build directories and such like that. We had changed the models we wanted to have serve locally on the AI side but I'don't know what the status of that is. You can present that to me in the book in the morning.

-- psyche, STT, 2026-09-25 ~22:10, to 88475f. Transcription corrected: "Nick's" → "Nix".
