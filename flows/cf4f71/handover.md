# Handover of cf4f71 ({ Psyche codexManager Tertiary }) to c57a2d

State at 18:0x, 4 Nov 2026. Beat 15 was the last sent (17:51); beat 16 due 18:02. Loop stopped by me on handover.

## Standing orders (from { Psyche core Secondary }, relaying the living)
- Hard beat every 10 min until the Flow Nexus fix is deployed: prompt every pane in `herdr --session default agent list` except the Psyche core Primary (wM1), the Secondary (wKZ), own pane, and book Quaternary idle by design (b4379a, wKR).
- Script: /tmp/claude-1001/-home-li-primary/cf4f71f0-c903-597f-937a-e9a581e2688c/scratchpad/beat.sh <n> (replies go to the pane that runs it; sed the reply pane `wK0:p1` to your own). Chain text inside is updated for step 2 dropped.
- After each beat, one Soft.Notice to { Psyche core Secondary } only when something changed or blocks. Use quoted single-quote args in zsh: flow 'Send.{ ... }'.
- Each beat also: /home/li/primary/tools/codex-usage. Codex 41% left at 17:51; soonest reset (6 Nov 17:32, about two days away, id RateLimitResetCredit_3962d176...) unused; { Psyche codexManager Secondary fb8093 } (wKE) is the keeper and decides redemption. I once mis-said the expiry was 13 minutes away and corrected it.

## The chain, as it now stands
1. Delivery fix built: DONE, flow main cfcbf5c (atomic receipt+queue; check 577/0/6, independent review clear), frozen; runtime built /nix/store/6yvx19bcpchpp0d4zz26y4ad1dfc1b4g-flow-configured-0.48.0.
2. CriomOS-home unit: DROPPED by the living (relayed by Psyche core Primary 15c0ce, wM1): 0.48 runs raw as flow-0.48, no unit, no wrapper change, flows launched through it with a brief saying so. I told Field core Primary.
3. A Send lands in a working seat on 0.48: not witnessed. The Secondary (wKZ:p1, 7a8991, Opus) will report when flows are up.
4. A refresh works: not witnessed. Feeders: beliefNexus (Mind, 20323c/9d3e07; same-image successor 748925f accepted, final default/all-features check pending, no deployed-refresh claim), Psyche core Tertiary b59322 (refreshes proven on 0.44; RecordMissing fix: handover records live under flows/<id>/vision).

## Panes seen at beat 15
Mind versionOne (fab3af, 177120), versionZero (0bf458, 84fdc5), beliefNexus, Mind core (70a111, 39b79d), Field core (2885c5, 3826cf), codexManager Secondary fb8093 (wKE), Psyche core Tertiary b59322 (wKB) and 3f4eec (wM2, has no brief, awaits one; I told the Secondary), book b4379a. versionOne/versionZero hold no step (next-version work).

## Pending
- Notice nothing since the step 2 drop except Field core Primary/Secondary still on step 2 work; Field core Secondary awaits approval for a focused reevaluation (moot).
- No flow has finished nothing two beats running.
