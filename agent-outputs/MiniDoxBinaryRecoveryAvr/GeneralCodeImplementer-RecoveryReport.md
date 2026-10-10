# MiniDox Binary Recovery AVR Report

## Task And Scope

Make AVR-aware disassembly tooling available without hardware writes, then resume reverse-engineering the old MiniDox QMK binaries. Scope was limited to static analysis of existing HEX files. No flashing, resetting, or keyboard writes were performed.

Primary target from the brief:

`/git/github.com/LiGoldragon/qmkBinaries/minidox/right/maple_computing_minidox_rev1_LiGoldragon.hex`

Related artifact:

`/git/github.com/LiGoldragon/qmkBinaries/minidox/left/maple_computing_minidox_rev1_LiGoldragon.hex`

## Tooling Result

AVR binutils was made available without modifying repository tooling:

```sh
nix shell nixpkgs#pkgsCross.avr.buildPackages.binutils -c avr-objdump --version
```

Result: pass. The command provided GNU `avr-objdump` from AVR binutils 2.46. Nix fetched the needed package closure from the configured binary cache. No source repo edit was needed.

Useful invocations:

```sh
nix shell nixpkgs#pkgsCross.avr.buildPackages.binutils -c avr-objcopy -I ihex -O binary <hex> <bin>
nix shell nixpkgs#pkgsCross.avr.buildPackages.binutils -c avr-objdump -b ihex -m avr5 -D <hex> > <disasm>
```

`avr-size -C --mcu=atmega32u4` was not useful on these raw Intel HEX inputs; it reported zero section usage because the HEX has no ELF sections.

## Artifacts Produced

Derived files in this lane:

- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/right.bin`
- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/left.bin`
- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/right-avr5.disasm`
- `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/left-avr5.disasm`

Source artifact sizes and hashes:

| Half | HEX bytes | Binary bytes | SHA-256 of HEX |
| --- | ---: | ---: | --- |
| left | 54713 | 19446 | `f1dba6dd78ccda42f4c2d53f51c4b2cb8d76b99dee15fc214b7f0cf312d4a062` |
| right | 55347 | 19672 | `9807a636d70a0edead3696ab2a6f3fe5bbc1db332d9087c11d58458d77a8a915` |

## Key Observations

The right binary has a keymap-like little-endian `uint16_t` table at byte offset `0x00ac`. It runs to the USB string descriptor near `0x014c`, exactly 80 words, matching 2 layers x 40 matrix slots. This validates the prior worker's "two-layer" finding for the right artifact.

The left binary also has a table-like region starting at `0x00ac`, but it runs to the descriptor near `0x023c`, matching 5 layers x 40 matrix slots. It contains both an apparent QWERTY base layer and a firmware-Colemak base layer. Therefore both halves exist, but the right `basicLeaderChords` artifact alone is not a full recovery surface for all historical layers.

The current `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c` was consulted only as a comparison source. It is not treated as authoritative for the lived layout.

## Right Artifact Keymap

Decode assumptions:

- plain USB HID keycodes use QMK `KC_*` names;
- old QMK mod-tap encoding is decoded as `LCTL_T`, `LSFT_T`, `LALT_T`, `LGUI_T`, `RCTL_T`, `RSFT_T`, `RALT_T`, and `RGUI_T`;
- old QMK layer-tap encoding is decoded as `LT(layer,key)`;
- unidentified `0x7c58` is left raw.

Confidence: high for plain keys and mod/layer taps; low for raw special key `0x7c58`.

Layer 0, matrix order:

| Row | C0 | C1 | C2 | C3 | C4 |
| --- | --- | --- | --- | --- | --- |
| 0 | `KC_Q` | `KC_W` | `KC_F` | `KC_P` | `KC_G` |
| 1 | `KC_Z` | `LCTL_T(KC_R)` | `LALT_T(KC_S)` | `KC_T` | `KC_D` |
| 2 | `LSFT_T(KC_A)` | `KC_X` | `KC_C` | `KC_V` | `LGUI_T(KC_B)` |
| 3 | `KC_NO` | `KC_NO` | `KC_BSPC` | `0x7c58` | `LT(1,KC_SPC)` |
| 4 | `KC_SCLN` | `KC_Y` | `KC_U` | `KC_L` | `KC_J` |
| 5 | `KC_SLSH` | `RCTL_T(KC_I)` | `RALT_T(KC_E)` | `KC_N` | `KC_H` |
| 6 | `RSFT_T(KC_O)` | `KC_DOT` | `KC_COMM` | `KC_M` | `RGUI_T(KC_K)` |
| 7 | `KC_NO` | `KC_NO` | `LT(1,KC_ESC)` | `LALT(KC_SPC)` | `LT(1,KC_ENT)` |

Layer 1, matrix order:

| Row | C0 | C1 | C2 | C3 | C4 |
| --- | --- | --- | --- | --- | --- |
| 0 | `KC_GRV` | `_______` | `_______` | `KC_PGDN` | `KC_HOME` |
| 1 | `KC_CAPS` | `KC_8` | `KC_7` | `KC_6` | `KC_MINS` |
| 2 | `LSFT_T(KC_9)` | `KC_LEFT` | `KC_DOWN` | `KC_LBRC` | `LGUI_T(KC_0)` |
| 3 | `KC_NO` | `KC_NO` | `_______` | `_______` | `KC_TAB` |
| 4 | `KC_BSLS` | `_______` | `_______` | `KC_PGUP` | `KC_END` |
| 5 | `KC_QUOT` | `KC_3` | `KC_2` | `KC_1` | `KC_EQL` |
| 6 | `RSFT_T(KC_4)` | `KC_RGHT` | `KC_UP` | `KC_RBRC` | `RGUI_T(KC_5)` |
| 7 | `KC_NO` | `KC_NO` | `_______` | `_______` | `KC_ENT` |

Credible physical interpretation:

- Rows 0-3 are one half's 3x5 alpha bank plus thumb row, and rows 4-7 are the opposite half in reversed column order.
- Top-row physical reading is strong: base starts `Q W F P G` on one side and `J L U Y ;` on the other.
- Home/bottom-row physical reading is medium confidence because the MiniDox matrix/layout macro was not recovered from the exact build source, and the matrix order swaps some outside-column positions relative to a simple row-major physical sketch.

## Left Artifact Comparison

The left artifact has more keymap layers than the right artifact. Decoded layer identities:

| Layer | Interpretation | Confidence |
| --- | --- | --- |
| 0 | QWERTY-ish base layer with home-row mod taps | high |
| 1 | Firmware-Colemak base layer similar to the right artifact | high |
| 2 | shifted symbol/navigation/media layer | medium |
| 3 | number/navigation layer similar to right layer 1 | high |
| 4 | function/special layer containing raw `0x7c00`, `0x7e40`, `0x7e41` special keycodes | medium |

Notable layer 4 rows from left:

| Row | C0 | C1 | C2 | C3 | C4 |
| --- | --- | --- | --- | --- | --- |
| 0 | `KC_F1` | `KC_F2` | `KC_F3` | `KC_F4` | `KC_F5` |
| 1 | `KC_F11` | `0x7c00` | `_______` | `_______` | `_______` |
| 2 | `_______` | `0x7e40` | `0x7e41` | `_______` | `_______` |
| 4 | `KC_F10` | `KC_F9` | `KC_F8` | `KC_F7` | `KC_F6` |
| 5 | `KC_F12` | `0x0048` | `0x0047` | `0x0046` | `_______` |
| 6 | `_______` | `_______` | `_______` | `_______` | `0x7c00` |

Interpretation: `0x7c00` and `0x7e40`/`0x7e41` are likely old-QMK special keycodes, but exact names were not proven from the binary alone. They are candidates for leader/reset/layer-special behavior, but the code-level reset path below is stronger evidence than the table names.

## Leader And Reset Evidence

Right disassembly contains strong evidence for QMK leader/chord handling and a leader-triggered reset path.

In `/home/li/primary/agent-outputs/MiniDoxBinaryRecoveryAvr/right-avr5.disasm`, the function around `0x02ca` tests leader-buffer membership for individual keycodes and maps them to bit masks:

| Address | Keycode | Interpreted key | Mask loaded on match |
| --- | ---: | --- | ---: |
| `0x02ce` | `0x11` | `KC_N` | `0x80` |
| `0x02e0` | `0x08` | `KC_E` | `0x40` |
| `0x02f2` | `0x0c` | `KC_I` | `0x10` |
| `0x0304` | `0x12` | `KC_O` | `0x20` |
| `0x0316` | `0x17` | `KC_T` | `0x08` |
| `0x0328` | `0x16` | `KC_S` | `0x04` |
| `0x033a` | `0x15` | `KC_R` | `0x01` |
| `0x034c` | `0x04` | `KC_A` | `0x02` |

Interpretation: this is credible custom leader/chord logic over home-row-ish keys. Confidence: high that chord processing exists; medium on the exact source names because the ELF symbols are stripped.

The same function then loads five `uint16_t` arguments:

| Address | Register pair | Value | Interpreted key |
| --- | --- | ---: | --- |
| `0x036e` | `r25:r24` | `0x0015` | `KC_R` |
| `0x036a` | `r23:r22` | `0x0008` | `KC_E` |
| `0x0366` | `r21:r20` | `0x0016` | `KC_S` |
| `0x0362` | `r19:r18` | `0x0008` | `KC_E` |
| `0x035e` | `r17:r16` | `0x0017` | `KC_T` |

Then:

- `0x0372` calls `0x33c2`, consistent with a five-key leader-sequence predicate;
- `0x0376` conditionally skips only if the predicate result is zero;
- `0x0378` calls `0x04ac` if the predicate is nonzero.

`0x04ac` calls `0x0490` and then `0x393a`. `0x393a` writes `0x77 0x77` to SRAM addresses `0x0800` and `0x0801`, enables the watchdog through `0x0060`, and loops forever. That is consistent with the QMK Caterina bootloader reset path used on ATmega32u4-style boards.

Conclusion: the right artifact strongly supports `leader r e s e t` causing a bootloader/reset path. Exact original C spelling cannot be proven because the binary is stripped, but the keycode constants, call shape, and reset routine make the behavior high confidence.

## Both-Half Implications

Both left and right HEX artifacts exist in `qmkBinaries/minidox`. They are not redundant copies:

- right: 2-layer table, strong leader/chord/reset code evidence, likely the `basicLeaderChords` changed artifact from the provided commit context;
- left: 5-layer table, contains a QWERTY-ish base plus a firmware-Colemak base and a separate special/function layer.

Recovery should not reconstruct the lived layout from only the current `kibord` source or only the right HEX. The next reconstruction should treat the right artifact as authoritative for the `basicLeaderChords` leader/reset behavior, and use both HEX tables as historical evidence for layer/key placement.

## Checks Run

Commands and results:

- `nix shell nixpkgs#pkgsCross.avr.buildPackages.binutils -c avr-objdump --version`: pass, AVR objdump available.
- `nix shell nixpkgs#pkgsCross.avr.buildPackages.binutils -c avr-objcopy -I ihex -O binary ...`: pass for both HEX files.
- `nix shell nixpkgs#pkgsCross.avr.buildPackages.binutils -c avr-objdump -b ihex -m avr5 -D ...`: pass for both HEX files.
- `wc -c right.bin left.bin`: pass, `right.bin` is 19672 bytes and `left.bin` is 19446 bytes.
- static Python byte parsing of `0x00ac` table regions: pass, produced the decoded tables summarized above.
- hardware checks: not run by boundary; no hardware write/reset/flash action was performed.

## Recommended Next Reconstruction Step

Create a reconstruction keymap from the binary, not from current source:

1. Model the right artifact's two-layer keymap first, including the leader/chord function and `leader r e s e t` bootloader path.
2. Add a separate left-artifact historical comparison file or comments because the left artifact has five layers and may represent an earlier or different half build.
3. Before any hardware action, recover or verify the exact MiniDox matrix/layout macro from the QMK revision used to build these binaries; that is the remaining blocker for high-confidence physical placement of the outside columns and thumb special keys.
