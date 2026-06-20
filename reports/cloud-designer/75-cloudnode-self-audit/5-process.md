# 75/5 — Process self-audit: reports 72/73/74, delivered vs. claimed

cloud-designer, 2026-06-20. Adversarial pass over the report+claim+process
surface of the CriomOS-on-DigitalOcean cloud-node work. Judged against the
evidence on disk: the cloud branch `cloud-designer-do-deploy-test` (HEAD
`9b41512`), the three target reports, and the git timeline. The verdict is
harsh on purpose. The headline: the work is real, but the reports stop one
commit short of the truth and never record the live mode-1 deploy that found a
real adapter bug and burned real DigitalOcean resources.

## The load-bearing finding — the reports end before the story does

The git timeline, from `cloud-designer-do-deploy-test`:

| Commit | Time | What |
|---|---|---|
| `783e23c` | 03:46 | "re-usable CriomOS-on-DO deploy harness + image-mint recipe" |
| `45056cba` (primary) | 11:44 | report 74/6 "built green, 1.1 GB" |
| `9b41512` | **12:13** | "custom images reject DO ipv6 + monitoring create flags" |

`9b41512`'s own commit body: *"Surfaced by the live MODE-1 deploy of the
CriomOS CloudNode image (id 233618631)."* So between 11:44 and 12:13 a live
**mode-1** deploy happened — the exact path reports 73 and 74 both insist is
**"Blocked on token"** / **"NEEDS-LIVE"**. It ran, it failed on a hardcoded
`ipv6:true,monitoring:true` in the adapter, and it was fixed. **No report in
`reports/cloud-designer/` records this.** The only record that the literal ask
("deploy CriomOS to DO with a pre-made image") was actually attempted live, and
what it cost, is a one-line git commit body. That is the single biggest
process hole here: the most important event in the whole arc — first real
mode-1 boot — is undocumented in the report surface that is supposed to be the
durable truth, while three sub-file-heavy report directories document the
*plan* for it in exhaustive detail.

This also retroactively falsifies report 74/6's "Next" section
(`6-built.md:57-64`), which frames upload+deploy as a clean future step gated
only on the token. By 12:13 the deploy had been *run* and had exposed a defect
the design reviews missed. The report was stale within 30 minutes and was never
amended.

## Over-claims — "proven live" / "green" beyond the evidence

### 73/6 "Ran it live and green" conflates two very different runs

`6-built-and-tested.md:18-20` TL;DR: *"Ran it live and green (mode 2, current
token): provision → Running → ssh reachable → destroyed."* That is true **for
mode 2 against a stock Ubuntu image**. But the report's title is *"the
re-usable CriomOS-on-DigitalOcean deploy harness"* and the whole framing is
CriomOS deployment. A reader skims "ran it live and green" and "CriomOS" in the
same breath. What actually ran green was: boot Ubuntu, ssh in, read Ubuntu's
`/etc/os-release`, find no CriomOS marker, honestly downgrade to
`ssh-reachable`, destroy. Zero CriomOS bytes touched DigitalOcean in that run.
The matrix at `:62-70` *is* honest (mode 1 = "Blocked on token"), but the TL;DR
and title oversell — the green run proves the *harness lifecycle*, not the
*product*. The gap between "image builds and boots" and "CriomOS is deployed"
is real and the prose blurs it.

### "ssh reachable" was not clean — the report admits a refused connection only in a footnote

`6-built-and-tested.md:66`: *"the retry loop absorbed an early 'connection
refused'."* So the very first ssh attempt **failed**; the harness retried. That
is normal (sshd isn't up at t=0) and the harness handles it correctly — but the
TL;DR's "ssh reachable → destroyed, ... 36.7s" presents a frictionless run. The
honest statement is "ssh became reachable after N retries," and that belongs in
the headline number, not buried in row 2 of a matrix. Minor, but it is the same
pattern as the bigger over-claim: the smooth-line summary hides the rough edge.

### 74/4 stamps `[VERIFIED]` on things that are inferred, not run

`4-end-to-end.md:10-11` defines `[VERIFIED]` as "source/code-confirmed this
session." Fine. But the end-to-end *sequence* it presents (build → release →
`POST /v2/images` → poll → deploy → confirm → destroy) was, as the git log
shows, partially **executed** later that day and broke at the deploy step. The
report's "Verified vs needs-live" summary (`:344-359`) lists the deploy harness
as "recognizes a numeric `CRIOMOS_IMAGE` as mode 1" — code-verified — but never
flags that the create payload it would send carries `ipv6:true,monitoring:true`,
which **rejects every custom image**. A code-confirmed read of `digitalocean.rs`
that session would have hit lines 439-440. The verification pass read field
*order* and *existence* and missed a live-breaking *value*. `[VERIFIED]` on the
harness leg was verifying the wrong axis.

## The minimality framing oversells (mildly)

`6-built.md:9-15` leads with **"1.1 GB ... ~55× smaller ... the directive met."**
The 55× is computed against the **60 GB** converted-droplet snapshot. But 60 GB
was never the *content* size — it was the droplet's *disk geometry*, mostly
empty. Comparing a content-sized image to a disk-geometry-sized snapshot and
reporting "55× smaller" flatters the result: the honest comparison is closure
vs. closure, and the real win is "content-sized and declarative," which the
report does also say. The "55×" is a true ratio of two real numbers that
nonetheless implies a 55× *content* reduction that didn't happen. Keep the
"content-sized, declarative, reproducible" claim; drop or caveat the "55×".

Separately, `6-built.md:9` reports **1.1 GB** as the headline; `5-plan.md:412`
and `1-image-build.md:374` predicted **~0.5–1 GB**. The built artifact came in
*above* the predicted band and the report does not note the miss — it just
restates the band elsewhere as if 1.1 GB confirmed it. A 10-30% overshoot on
the central deliverable's headline metric deserves a sentence, not silence.

## Report sprawl — 5,680 lines for a ~682-line diff plus three small additions

Reports 72, 73, 74 total **5,680 lines** across 19 files. The actual delivered
code on `cloud-designer-do-deploy-test` is a **682-line diff** (`flake.nix` +55,
mint script +105, `digitalocean.rs` +15, harness +509) plus three small
declarative additions in horizon-rs/CriomOS/goldragon (a species enum arm, a
`.nix` disk module, a node entry). That is roughly **8 lines of report per line
of delivered code**, and most of the delivered "code" is a single test harness.

The structural waste:
- **73 and 74 are the same investigation twice.** 73 chose the
  snapshot-mint path; 74 pivoted to the by-URL custom-image path and re-derived
  the *entire* end-to-end sequence (`74/4`), re-stating DO's BIOS-only
  constraint, the token blocker, the always-destroy pattern, the witness line —
  all already in 73. `74/4-end-to-end.md` is 375 lines that largely re-pollinate
  73's recipe with one genuinely new fact (custom-image-by-URL upload). One
  superseding section in 73, or a 74 that *only* documents the upload delta,
  would have carried the same information.
- **Five planning sub-files (`1`–`5`) precede each `6-built`.** 74 has
  `1-image-build`, `2-cluster-data`, `3-species`, `4-end-to-end`, `5-plan`
  (30 KB), then a 64-line `6-built`. The plan files are a lanes-A/B/C/D fan-out
  for a change that landed as three ~one-arm commits. The fan-out machinery
  outweighs the change by an order of magnitude.

The discipline (`AGENTS.md`: "Reports go in files; chat is for the user")
mandates files for substantive output — it does not mandate *five* of them per
landed enum arm. Sprawl this lopsided makes the durable record *harder* to
trust, not easier: the 11:44 "built green" report is buried under 30 KB of
superseded planning, and the one event that mattered (12:13 live deploy) is in
none of it.

## Process flaws worth recording

### P1 — bugs found at live-deploy time, not in review

The `ipv6/monitoring` defect (hardcoded `true` in `DropletPayload::from_spec`,
`digitalocean.rs:457,463` post-fix) is a **values bug on the only create path**.
It was discoverable by reading the adapter — the same adapter the adversarial
verification pass (72/5) and the 74/4 "VERIFIED" pass both claim to have read.
It was found instead by burning a live droplet + custom image. The lesson:
"code-confirmed this session" verification was confirming structure (field
order, existence) and not *values that the live API rejects*. A review that
actually traced one create call end-to-end against DO's custom-image
constraints (which 74/4 itself documents at `:48` — "UEFI forbidden",
"BIOS only") would have asked "does DO honor `ipv6`/`monitoring` on custom
images?" and caught it dry. Adding it as a noted-but-unfixed `ServerSpec` field
(commit body: "Both should become desired-state fields ... rather than
hardcoded") is the right call but is itself residual debt the reports never
surfaced.

### P2 — possible live-resource leak, undocumented

The live mode-1 deploy created custom image **233618631** and (implicitly) a
droplet from it. Reports 73/74 only ever cite the clean mode-2 teardown
(droplet `578965503`, "account empty afterward"). There is **no record** of
whether image 233618631 and its droplet were destroyed. The harness's
`DeployCleanup` Drop guard destroys *droplets and ssh keys* but explicitly
**does not destroy the custom image** (`74/4:261`: "The custom image itself is
**not** destroyed by the harness — it is the reusable artifact"). So a failed
mode-1 run that aborts at create-rejection may leave the image *and* — if the
create partially succeeded before the reject — a droplet. The account state
after the 12:13 deploy is unverified in any report. This is exactly the
"timeout-kill droplet leak" risk: a billable resource whose teardown is
unconfirmed. **Action: verify image 233618631 and any sibling droplet are
destroyed; record account-empty-after for the mode-1 run, not just mode-2.**

### P3 — the 60 GB snapshot was the hack that triggered the rework

The whole 72→74 arc exists because an earlier path produced a 60 GB
converted-droplet snapshot (`6-built.md:11`, `74/4:21`). That snapshot was the
quick-hack baseline — boot a droplet, infect it, snapshot the whole disk
geometry. It is correctly *retired* by the declarative image, and the reports
are honest that it was the wrong shape. The process note: the hack shipped (or
nearly shipped) before the minimal design existed, and the minimal design was
reverse-justified against it ("55× smaller"). Healthier order is design the
content-sized image first; the snapshot path should have been recognized as a
geometry-bloat trap at design time, not after producing 60 GB.

### P4 — repeated long background waits and timeout-kills

The harness lifecycle is provision → poll-to-Running → ssh-retry-loop
(`DEPLOY_SSH_ATTEMPTS=30`, ~2.5 min) → confirm → destroy, and the flake wrapper
adds a `trap … EXIT` sweep specifically *because* the Rust `Drop` guard does
not run on `kill -9` (`73/6:38`, `74/4:259`). The presence of two
always-destroy layers is good engineering — but the *reason* it is needed is
that these runs were long enough, and interrupted often enough (timeout-kills,
`kill -9` during iteration), that a single Drop guard was judged insufficient.
That is a tell that the live-iteration loop was slow and lossy: minutes per
attempt, multiple attempts, resources at risk on every interruption. The
mitigation is sound; the underlying cost (slow live loops, kill-driven
iteration) is real and should be acknowledged rather than presented purely as a
robustness feature.

## Where the reports are honest (credit where due, briefly)

- `73/6:62-70` deploy-level matrix correctly separates "Proven live" (mode 2),
  "Blocked on token" (mode 1), "Wired, not yet exercised" (`nixos-rebuild`
  push). The honesty *mechanism* (`DeployLevel::as_witness_field` emitting
  `ssh-reachable` not `criomos-confirmed` when no marker matched) is real and in
  the code (`digitalocean_deploy_live.rs:361,372`). The harness genuinely
  refuses to over-claim its own confirm level.
- 72/5's adversarial-verification pass is the right instinct (refute each
  finding, correct four framings, reverse one harmful fix). The irony is that
  the *same rigor* applied to the deploy adapter's create payload would have
  caught the ipv6/monitoring bug before the live run.

## The asks

1. **Write the missing live-deploy record.** A short report (or an amendment to
   74/6) documenting the 12:13 mode-1 deploy: image 233618631, the ipv6/monitoring
   rejection, the fix `9b41512`, and the *account-empty-after* state. The most
   important event currently lives only in a git commit body.
2. **Verify no leaked resources.** Confirm image 233618631 and any droplet
   created from it are destroyed; if the harness can't tear down a
   create-rejected mode-1 attempt, that is a harness gap to file.
3. **Promote `ipv6`/`monitoring` to `ServerSpec` desired-state.** The hardcoded
   `false` is the mirror of the hardcoded `true` bug — both are wrong-by-default
   for *some* image. The commit body already concedes this; it is open debt.
4. **Caveat the "55×" and the 1.1 GB-vs-predicted-band miss** in 74/6, or drop
   the ratio for the honest "content-sized, declarative" claim.
5. **For the next arc, collapse the planning fan-out.** A superseding-delta
   report, not a second full end-to-end re-derivation, when a path pivots.
