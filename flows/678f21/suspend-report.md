# Did the laptop really sleep? (Psyche core Sonnet c3c1a0, 2026-11-11, read-only; raw output in suspend/)

## Reading in short
The sleep itself cost about 3 points of battery over 4 h 52 min; most of the fall from 80-something to 63% happened before the lid closed, awake on battery. Suspend is working as designed (s2idle, then hibernate); s2idle reaches the deepest idle state only about a third of the time, and the firmware offers no S3 at all.

## 1. What the last sleep did (this boot: kernel 7.3.3, started 13:20:02)
| Time (11 Nov) | Event | Battery |
|---|---|---|
| 12:58 to 13:19 | awake on battery, 21 min | 77 -> 66% (0.55 point per minute, about 33% per hour) |
| 13:20:52 | lid closed, "Suspending, then hibernating" | 66% |
| 13:20:54 to 15:21:53 | s2idle (`PM: suspend entry (s2idle)`), woken after exactly 2 h 0 min 59 s | not sampled |
| 15:21:53 | hibernate entered (image 2.9G written, machine off) | |
| 18:13:25 | resumed from the hibernation image ("slept 4h52m32s") | 63% at 18:13:41 |
So the sleep phases together took 3 points (66 -> 63). Hibernate draws about nothing, so those 3 points are mostly the 2 h of s2idle: at most 1.5 points per hour. The earlier fall (80% at 16:36 on the 10th, 78% through the night on AC, 77% at 12:58) ran awake: 12 points in 21 minutes before the lid closed. That boot (kernel 7.1.8) had no GPE mask; the interrupt storm measured at 03:11 that day was running (0.55 of a core, irq/9-acpi).

## 2. GPE 6D and the wake
- The mask held: `acpi_mask_gpe=0x6D` is on the command line, the kernel logged "Masking GPE 0x6d", and `/sys/firmware/acpi/interrupts/gpe6D` reads 0, "masked". (Before the mask: 6.94M events in 11.5 h.)
- What woke the s2idle: the suspend-then-hibernate timer, 2 h after entry to the second (RTC alarm; "RTC can wake from S4"). No device wake is logged; bluetooth logged "wake event 0x0". The final wake at 18:13 was a boot from the hibernation image.

## 3. Deep sleep (S3)
The kernel reports `ACPI: PM: (supports S0 S4 S5)` and `/sys/power/mem_sleep` shows only `[s2idle]`: this firmware (BIOS 1.19) exposes no S3. I could not read the BIOS settings from Linux, so the name of the setting on this model is unconfirmed; the place to look is the BIOS menu Config > Power for a "Sleep State" or "Sleep Mode" entry (Lenovo has offered "Windows / Linux S3" on some models; whether the T14 Gen 5 Intel still has it is unknown to me).

## 4. Reading
- The drain you saw is not a suspend failure: sleep took 3 points; awake use on battery before the lid closed took 12.
- s2idle does reach hardware sleep but not for long: `suspend_stats/last_hw_sleep` 2463 s of the 7259 s suspended (34%); the cpuidle `low_power_idle_*_residency_us` files read 0 and the package C-state counters show only C2, so those counters are not a useful measure here. The PMC lists the Ethernet controller (GBE), the Wi-Fi/Bluetooth block (CNVI), audio DSPs and several fabrics as still On. Which one keeps the SoC out of its deepest state for the other 66% of the time is not determined (candidates: the Intel e1000e network controller, which also came up with link at 7686 s; USB; the Management Engine).
- Masking GPE 6D is a stopgap, as the brief says: the line is silenced inside Linux; the firmware cause stays. A fix is that line quiet with every feature working (the firmware book's route: a BIOS update or setting).
- Smaller finding: `spd5118` (the DDR5 temperature sensor) fails to resume on every wake with error -6; it looks harmless but is a resume error worth a look.
- Unknown: the battery level at 15:21:53 (no sample taken during sleep), so how the 3 points split between s2idle and hibernate is inferred.
