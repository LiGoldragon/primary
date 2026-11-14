# A persistent boot-event watchdog witness

Proposal for Order `1mhf`; nothing is implemented or deployed.

Declare one boot-triggered service that reads the watchdog identity and saved
`bootstatus` from sysfs and writes one structured journal record, after the
SP5100 driver appears. It opens no watchdog device, sends no ping and changes no
watchdog policy. The journal supplies the boot identity and timestamp.

For this driver, bit `WDIOF_CARDRESET` (`0x20`) records that SP5100's fired bit was
set at initialization. The driver saves it before clearing the hardware bit;
the saved sysfs value remains available. A set bit is a watchdog-fired witness,
not evidence of what stopped its pings. A zero is inconclusive. This exact
machine's flag retention remains unproved; an induced expiry test is outside
this proposal.

Keep the existing EFI-pstore panic/oops path and boot archive. Current kernel
configuration, `pstore_disable=N`, writable mount and systemd-pstore already
provide it; eight older firmware records show historical persistence. Merely
adding `efi_pstore.pstore_disable=0` would codify an existing behavior and add no
capture to the current boot, so that line alone is not the proposed improvement.

The active SP5100 driver has no pretimeout capability, so an expiry message
before reset is unavailable. Journald persists received records but samples no
sensors or memory; no existing minute event was found. A minute sampler would
need a separate Psyche ruling on its event source. None is added here.

The new boot-event record makes each retained watchdog reset witness survive a
later reboot. Panic/oops may leave EFI records; sudden power loss, firmware reset
and hangs outside those mechanisms can still remain unclassified. No software
capture can promise that the next ending names its cause.

Evidence and exact kernel/systemd source pointers:
`/home/li/primary/flows/d76b4c/abrupt-capture-research.md`.
