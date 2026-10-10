# MiniDox Binary Recovery Situational Map

## Task And Scope

Read-only reverse-engineering scout for the user's lost MiniDox layout from compiled QMK `.hex` artifacts, especially `/git/github.com/LiGoldragon/qmkBinaries` commit `f6e2093debe57ee15acedc88b3dd772cf4071fb5` / jj change `pmkrlzxkwvlloonmyywoswuprsslpsms`, message `(version basicLeaderChords)`.

Boundaries followed: no source edits, no hardware reset, no flash, no commit, no push, and no `/nix/store` search. The only write was this report under `/home/li/primary/agent-outputs/MiniDoxBinaryRecovery/`.

## Commands And Sources Consulted

- Spirit query: `spirit "(PublicTextSearch [MiniDox QMK layout binary recovery leader chords])"` returned `(Error [no matching record])`.
- Workspace instructions: `/home/li/primary/AGENTS.md` was supplied in the prompt.
- Version-control discipline: `/home/li/primary/.agents/skills/version-control/SKILL.md`.
- Local searches: `find`, `rg --files`, and `rg` under `/git/github.com/LiGoldragon`, `/home/li/primary`, `/home/li/git-archive`, and scoped `/home/li` exclusions; no `/nix/store` search.
- `qmkBinaries` history: `jj status`, `jj log`, `jj show`, `jj file list`, `jj file show`, `jj file annotate`.
- Binary/tool probes: `command -v`, `objdump -i`, `objcopy --help`, `objdump -b ihex -m avr -D`, `objcopy -I ihex -O binary ... /dev/null`, `strings`, Python Intel HEX parsing.
- Upstream QMK source by `curl`: QMK commit `bc15c4f4ab81c1e2950dfc1c38cf86dc626573c9` for `keyboards/minidox/rev1/rev1.h`, `keyboards/minidox/rev1/info.json`, `keyboards/minidox/keymaps/default/keymap.c`, `quantum/quantum_keycodes.h`, `tmk_core/common/keycode.h`, and `tmk_core/common/action_code.h`; QMK commit `b1093e9da5f27253f3db692352daf5cf4ad5b98d` for current `maple_computing/minidox` default keymap context.
- Passive live-device check: `lsusb`, `/sys/bus/usb/devices`, and `usbhid-dump -d feed:3060 -e descriptor`; no matching MiniDox was attached during this scout.
- Prior local reports read for context: `MiniDoxResetChordRecon`, `MiniDoxFirmwareAudit`, `MiniDoxStackRecon`, and `MiniDoxModernTooling`.

## Findings By Confidence

1. The strongest artifact remains `qmkBinaries` commit `f6e2093debe57ee15acedc88b3dd772cf4071fb5` / change `pmkrlzxkwvlloonmyywoswuprsslpsms`, message `(version basicLeaderChords)`, changing only `minidox/right/maple_computing_minidox_rev1_LiGoldragon.hex`.
2. The `basicLeaderChords` right-half hex contains a credible QMK keymap table at byte offset `0x00ac`. The first coherent layer starts `KC_Q KC_W KC_F KC_P KC_G`, so that artifact appears to emit firmware Colemak on the base layer.
3. The recovered `basicLeaderChords` table has only two coherent 40-word MiniDox matrix layers before USB descriptor text begins. It does not look like the later four-layer reconstructed source in `/git/github.com/LiGoldragon/kibord`.
4. The keymap table itself does not contain an obvious `KC_LEAD`, `RESET`, or `QK_BOOT` entry. Whole-image scans found no contiguous `r e s e t` keycode sequence. The leader/reset behavior is therefore not proven from table extraction; it remains supported by the commit message and user memory, and would require AVR-aware disassembly or behavioral testing to prove.
5. Local tool availability is enough to parse Intel HEX and recover raw bytes, but not enough for AVR disassembly. `objcopy` supports `ihex` and can convert to raw binary; installed `objdump` cannot disassemble `-m avr`; `avr-objdump`, `avr-objcopy`, `llvm-objdump`, rizin/radare2, and Ghidra were not found on PATH. `avrdude` is installed, but it is not a disassembler and was not used against hardware.
6. VIA/dynamic keymap readout is not plausible from current binary evidence. No visible MiniDox hex variant contains `via`, `dynamic`, `raw`, or `hid` ASCII tokens, and no attached `feed:3060` device was present for passive descriptor readout. Dynamic readout would require firmware support that the artifacts do not advertise.

## Relevant MiniDox Artifacts

Visible worktree paths in `/git/github.com/LiGoldragon/qmkBinaries`:

- `/git/github.com/LiGoldragon/qmkBinaries/minidox/left/maple_computing_minidox_rev1_LiGoldragon.hex`
- `/git/github.com/LiGoldragon/qmkBinaries/minidox/right/maple_computing_minidox_rev1_LiGoldragon.hex`

Visible history:

| Change | Commit | Date | Message | MiniDox hex effect |
| --- | --- | --- | --- | --- |
| `yttwyxuvtxmswryvyssottomsvqnnuxq` | `15d50f4d94a3392ebd66dee8281ceb462a48c668` | 2023-11-11 | `(init qwertyVersion)` | Added left and right hex |
| `stmkwxzwvvonywlrwoowkywtzmyxlwnl` | `4d5ed80f73c748b06c8fcddc17c83d22c04cfb6e` | 2023-11-12 | `(added MdReadme)` | No hex change |
| `pkmtrsplylyssxnorzlksnztxltvmkry` | `66bb38dd81fb2674603ef701d34ee87875e16bf5` | 2023-11-13 | `(MdReadmeIdTypifying GitRev)` | No hex change |
| `pmkrlzxkwvlloonmyywoswuprsslpsms` | `f6e2093debe57ee15acedc88b3dd772cf4071fb5` | 2023-11-13 | `(version basicLeaderChords)` | Changed right hex only |
| `qmttrmoktwuxnlzxntoqzkvyxpmuqzrw` | `5f7fe00d62a920f1b5757b42eda4d479b5f26075` | 2026-05-30 | `qmkBinaries: refresh minidox firmware` | Changed right hex only |
| `txzyxkoxytvqmmytzyktkomrtqyypxus` | `e73817404f33060ba41efa6d0db22f57a9d526e7` | 2026-05-30 | empty working copy | No file change |

Content hashes and sizes observed by `jj file show`:

| Revision | Side | Lines | Text bytes | SHA-256 prefix |
| --- | --- | ---: | ---: | --- |
| init/readme/basic/refresh/current | left | 1217 | 54713 | `f1dba6dd78ccda42` |
| init/readme/id | right | 1217 | 54713 | `55df52f36cc2bc1a` |
| `basicLeaderChords` | right | 1245 | 55961 | `f5ad83fbe6be6478` |
| refresh/current | right | 1231 | 55347 | `9807a636d70a0ede` |

The left hex never changes in visible history. The right hex has three distinct variants: initial `qwertyVersion`, `basicLeaderChords`, and 2026 refresh.

Obvious prior repos/remotes checked:

- `/git/github.com/LiGoldragon/kibord` exists but is now known non-authoritative for the flashed layout. Its current MiniDox source is a modern scaffold only.
- `/home/li/git-archive/Mentci-AI/Sources/kibord` and `/home/li/git-archive/Mentci-AI/Sources/mentci-ai/inputs/flake/kibord` exist, but scoped search found only `ergodone/coleremak` keymap/config/rules files, not MiniDox source.
- Scoped `/home/li` search found `/home/li/Pictures/minidox` but no additional MiniDox/QMK source repo.

## HEX Conversion And Disassembly State

Observed tool facts:

- `objcopy -I ihex -O binary /git/github.com/LiGoldragon/qmkBinaries/minidox/right/maple_computing_minidox_rev1_LiGoldragon.hex /dev/null` exited `0`, proving the installed `objcopy` can parse the Intel HEX container and emit raw bytes.
- Python Intel HEX parsing of `basicLeaderChords` found contiguous byte ranges:
  - left hex: `19446` bytes, addresses `0x0000..0x4bf5`
  - right `basicLeaderChords` hex: `19888` bytes, addresses `0x0000..0x4daf`
- `objdump -b ihex -m avr -D ...` failed with `objdump: can't use supplied machine avr` and `objdump: can't disassemble for architecture UNKNOWN!`.
- `objdump -i` lists x86/IAMCU targets plus `ihex`, `srec`, and `binary` formats, but no AVR architecture.
- `avr-objdump`, `avr-objcopy`, `llvm-objdump`, `radare2`, `rizin`, and Ghidra were not found on PATH.
- `avrdude` version `8.1` is on PATH, but it is for programmer/device operations; it was not used against hardware.

Interpretation: raw binary extraction is locally available. Symbolic ELF recovery is not: Intel HEX does not carry C symbols, and the installed binutils cannot disassemble AVR. Meaningful code recovery needs AVR binutils or an AVR-aware reverse-engineering tool.

## Upstream MiniDox Matrix Evidence

QMK `bc15c4f4...` has the older MiniDox path `keyboards/minidox/rev1/rev1.h`, with:

```c
#define LAYOUT_split_3x5_3( \
  k01, k02, k03, k04, k05,    k45, k44, k43, k42, k41, \
  k11, k12, k13, k14, k15,    k55, k54, k53, k52, k51, \
  k21, k22, k23, k24, k25,    k65, k64, k63, k62, k61, \
            k33, k34, k35,    k75, k74, k73            \
  ) \
  { \
    { k01, k02, k03, k04, k05 }, \
    { k11, k12, k13, k14, k15 }, \
    { k21, k22, k23, k24, k25 }, \
    { ___, ___, k33, k34, k35 }, \
    { k41, k42, k43, k44, k45 }, \
    { k51, k52, k53, k54, k55 }, \
    { k61, k62, k63, k64, k65 }, \
    { ___, ___, k73, k74, k75 } \
  }
```

That macro is the basis for the draft visual projection below. It reverses right-hand visual keys in matrix storage.

## Recovered `basicLeaderChords` Keymap Table

Evidence:

- Right `basicLeaderChords` hex, parsed from commit `f6e2093debe57ee15acedc88b3dd772cf4071fb5`.
- Candidate table byte offset: `0x00ac`.
- Two coherent layers, each `8 * 5 = 40` 16-bit words.
- At byte offset `0x014c`, USB descriptor text begins (`MiniDox`, `That-Canadian`), so later words are not keymap layers.

Raw matrix words:

```text
Layer 0:
0014 001a 0009 0013 000a
001d 2115 2416 0017 0007
2204 001b 0006 0019 2805
0000 0000 002a 7c58 412c
0033 001c 0018 000f 000d
0038 310c 3408 0011 000b
3212 0037 0036 0010 380e
0000 0000 4129 042c 4128

Layer 1:
0035 0001 0001 004e 004a
0039 0025 0024 0023 002d
2226 0050 0051 002f 2827
0000 0000 0001 0001 002b
0031 0001 0001 004b 004d
0034 0020 001f 001e 002e
3221 004f 0052 0030 3822
0000 0000 0001 0001 0028
```

### Draft Visual Projection

Labels decode standard HID/QMK values directly. `*_T(...)` labels for `0x2xxx`/`0x3xxx` are interpreted through old TMK/QMK action-code form from `tmk_core/common/action_code.h`; those are credible but should be verified behaviorally.

Layer 0, likely base Colemak:

| Row | Left five | Right five |
| --- | --- | --- |
| Top | `Q` `W` `F` `P` `G` | `J` `L` `U` `Y` `;` |
| Stored row 2 | `Z` `LCTL_T(R)` `LALT_T(S)` `T` `D` | `H` `N` `RALT_T(E)` `RCTL_T(I)` `/` |
| Stored row 3 | `LSFT_T(A)` `X` `C` `V` `LGUI_T(B)` | `RGUI_T(K)` `M` `,` `.` `RSFT_T(O)` |
| Thumbs | `BSPC` `RALT+RGUI_T(KP_ENTER?)` `LT(1, Space)` | `LT(1, Enter)` `LALT(Space)` `LT(1, Esc)` |

Uncertainty: under the upstream 2020 MiniDox macro, this projection puts `Z` on the second physical row and `LSFT_T(A)` on the third physical row. That is unusual compared to later reconstructed source. It may be intentional, or it may mean the old source used row arguments differently than modern expectations. The raw matrix words are the safer evidence.

Layer 1, likely held by `LT(1, ...)` thumb keys:

| Row | Left five | Right five |
| --- | --- | --- |
| Top | `` ` `` `TRNS` `TRNS` `PGDN` `HOME` | `END` `PGUP` `TRNS` `TRNS` `\` |
| Stored row 2 | `CAPS` `8` `7` `6` `-` | `=` `1` `2` `3` `'` |
| Stored row 3 | `LSFT_T(9)` `LEFT` `DOWN` `[` `LGUI_T(0)` | `RGUI_T(5)` `]` `UP` `RIGHT` `RSFT_T(4)` |
| Thumbs | `TRNS` `TRNS` `TAB` | `ENTER` `TRNS` `TRNS` |

Number-ordering evidence: this artifact does not have a conventional `1 2 3 4 5 6 7 8 9 0` row. The obvious numeric layer places `8 7 6` on the left second row and `1 2 3` on the right second row, with `9/0` and `5/4` as mod-tap taps on the third row if the action-code decode is correct.

## Leader, Chord, And Reset Evidence

Credible positives:

- Commit message `(version basicLeaderChords)` strongly suggests the right hex was built for leader/chord behavior.
- The artifact is not just a renamed current source build: the recovered table shape differs from the later reconstructed four-layer `kibord` source.

Negative or inconclusive evidence:

- The recovered `basicLeaderChords` keymap table contains no obvious `KC_LEAD`, `RESET`, or `QK_BOOT` keycode.
- Whole-binary scans found no contiguous keycode sequence for `KC_R KC_E KC_S KC_E KC_T`, either as bytes `15 08 16 08 17` or as 16-bit little-endian words.
- Whole-binary scans found two `0x5cxx`-range 16-bit words in each right hex, but they occur in code/data-looking regions and are not credible keymap entries by themselves.
- No useful ASCII strings appear for `reset`, `leader`, `via`, `dynamic`, `MiniDox`, `QMK`, or `LiGoldragon`.

Interpretation: the table recovery supports base/layer keycodes. It does not prove `[leader r e s e t]`, `QK_BOOT`, or reset behavior. Proving that behavior from the binary now requires AVR-aware disassembly and control-flow analysis, or a non-flashing behavioral test on the physical keyboard.

## VIA And Dynamic Keymap Plausibility

Artifact evidence:

- Scoped binary string scans across all visible MiniDox variants found no hits for `via`, `dynamic`, `raw`, or `hid`.
- The recovered keymap table is a static compiled table, not an obvious VIA dynamic keymap storage area.
- No `feed:3060` MiniDox was currently attached, so passive `usbhid-dump -d feed:3060 -e descriptor` returned `No matching HID interfaces`.

Interpretation: VIA/dynamic readout is unlikely to help for these artifacts. It is only plausible if the currently flashed firmware differs from all visible artifacts and was built with VIA/Vial/dynamic support. Existing evidence does not point that way.

## Recommended Next Recovery Workflow

Use a hybrid workflow, but start behavioral before flashing anything:

1. Treat `qmkBinaries` as the artifact source of truth and keep `f6e2093d` right hex plus the unchanged left hex preserved by hash.
2. Seed a draft source layout from the recovered two-layer table above, not from current `/git/github.com/LiGoldragon/kibord`.
3. With the keyboard attached in normal mode and no reset/flash, record actual key outputs under a plain US host layout. Use `libinput debug-events`, `evtest` if available later, or another passive HID/event recorder. Press every physical key on base and the recovered `LT(1, ...)` layer. This will resolve the A/Z row-order uncertainty and the number ordering.
4. Do not test `[leader r e s e t]` casually: if it works, it may enter bootloader/reset mode. Test only when ready to observe USB changes and recover without flashing.
5. If binary proof of leader/chord behavior matters before behavioral testing, run the artifact through AVR-aware tooling. Needed tools: `avr-objdump`/AVR binutils or an AVR-capable reverse-engineering suite. The installed toolchain cannot disassemble AVR.
6. Do not use VIA/dynamic readout as the primary path unless a passive descriptor check on the attached keyboard shows a raw-HID/VIA-like interface or source/binary evidence later proves VIA support.

## Unknowns And Blockers

- Exact source for `basicLeaderChords` was not found in `/git/github.com/LiGoldragon`, `/home/li/git-archive`, or scoped `/home/li` searches.
- The currently flashed keyboard was not attached during this scout, so no live behavioral or descriptor evidence was collected.
- AVR disassembly was blocked by missing AVR-aware disassembly tools on PATH.
- The physical handedness/flashing strategy remains unresolved. The history has left/right hex artifacts, but only the right hex changed for `basicLeaderChords` and refresh.

## Verification Summary

- Every artifact and commit claim above is backed by `jj` output or file paths in `/git/github.com/LiGoldragon/qmkBinaries`.
- The keymap table claim is backed by Python Intel HEX parsing of `jj file show` output and by upstream QMK `keyboards/minidox/rev1/rev1.h` matrix layout.
- Tool availability claims are backed by `command -v`, `objdump -i`, `objcopy --help`, and the failed `objdump -b ihex -m avr -D` probe.
- Negative source-search claims are based on scoped `find`/`rg`; private/non-obvious locations outside those scopes were not exhaustively searched.
