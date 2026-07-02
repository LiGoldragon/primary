# MiniDox Layout Research Synthesis

## Task And Scope

Research scout synthesis for published MiniDox and similar compact split keyboard layouts/keymaps. Scope was design inspiration only: no firmware edits, no flashing, no commits, and no local runtime state changes beyond this report.

Current constraints carried from the brief and prior local reports:

- The target keyboard is MiniDox-compatible QMK, currently treated as `maple_computing/minidox/rev1`.
- The firmware should emit Colemak directly; do not depend on a host Colemak layout.
- Keep the QMK stack modern, reproducible, and low-risk to flash.
- Mouse/debug layers should be secondary, not the center of the layout.
- Feature redesign should follow a safe reflash checkpoint.

## Sources Consulted

- Spirit query: `spirit "(PublicTextSearch [MiniDox layout keyboard keymap])"` returned `(Error [no matching record])`.
- Local MiniDox context reports:
  - `agent-outputs/MiniDoxStackRecon/Scout-SituationalMap.md`
  - `agent-outputs/MiniDoxModernTooling/Scout-SituationalMap.md`
  - `agent-outputs/MiniDoxFlashReadiness/Scout-SituationalMap.md`
  - `agent-outputs/MiniDoxColemakCorrection/GeneralCodeImplementer-Evidence.md`
- Upstream QMK MiniDox:
  - `https://github.com/qmk/qmk_firmware/tree/master/keyboards/maple_computing/minidox/keymaps`
  - `https://raw.githubusercontent.com/qmk/qmk_firmware/master/keyboards/maple_computing/minidox/keymaps/default/keymap.c`
  - `https://raw.githubusercontent.com/qmk/qmk_firmware/master/keyboards/maple_computing/minidox/keymaps/bepo/keymap.c`
- Reusable small-layout systems:
  - Miryoku reference: `https://github.com/manna-harbour/miryoku/blob/master/docs/reference/readme.org`
  - Callum's current half-layer keymap: `https://github.com/callum-oakley/keymap` and `https://github.com/callum-oakley/vial-qmk/blob/r2g-callum/keyboards/mechboards/ferris/r2g/keymaps/callum/keymap.c`
  - Seniply: `https://github.com/stevep99/seniply` and `https://stevep99.github.io/seniply/`
- Combo/leader-heavy personal maps:
  - urob ZMK config: `https://github.com/urob/zmk-config`, especially `config/base.keymap`, `config/combos.dtsi`, `config/leader.dtsi`
  - Xavv1 Cantor Remix QMK: `https://github.com/malparty/xavv1-remix`, especially `keymap.c` and `features/combo.c`
  - GergoPlex combo gist: `https://gist.github.com/Merlin04/0541ca73bebdd3c5bd5807489bf2ec9f`
  - Andrew Rae Kyria keymap: `https://github.com/andrewjrae/kyria-keymap`
- Other compact hardware/source checks:
  - Cantor default QMK keymap: `https://raw.githubusercontent.com/qmk/qmk_firmware/master/keyboards/cantor/keymaps/default/keymap.c`
  - TOTEM source tree: `https://github.com/GEIGEIGEIST/TOTEM`
  - Architeuthis Dux family/source index: `https://github.com/tapioki/cephalopoda`
- QMK feature docs for context:
  - Combos and config options: `https://docs.qmk.fm/config_options`
  - Leader: `https://docs.qmk.fm/features/leader_key`
  - One-shot keys: `https://docs.qmk.fm/one_shot_keys`
  - Mouse keys: `https://docs.qmk.fm/features/mouse_keys`

## Observed Patterns

### Upstream MiniDox

QMK currently exposes only `default` and `bepo` MiniDox keymaps under `keyboards/maple_computing/minidox/keymaps`.

The `default` MiniDox keymap is conservative and useful as a baseline. It has four layers: base, lower, raise, adjust. The base uses plain QWERTY alphas with thumb keys for control, lower, space, backspace, raise, and one-shot shift. Raise contains unshifted numbers, arrows on the left home area, and common unshifted symbols. Lower contains shifted symbols and delete/enter. Adjust contains function keys, task-manager/control-alt-delete shortcuts, and `QK_BOOT`.

The `bepo` MiniDox keymap is more interesting. It uses a direct BEPO base, layer-tap thumbs `LT(_LOWER, KC_TAB)` and `LT(_RAISE, KC_ENTER)`, bottom-row mod-taps on both hands, navigation and mouse wheel on lower, symbols on raise, and function/numbers on adjust. This proves a MiniDox-specific published layout has already combined direct firmware-level non-QWERTY output, layer-tap thumbs, and home-ish mod access.

MiniDox takeaway: the hardware fits the modern 36-key design vocabulary exactly, but the upstream MiniDox examples are mostly baseline/recovery references, not polished chord-heavy designs.

### Miryoku

Miryoku is the cleanest complete 36-key source system. Its declared physical model is 5 columns, 3 rows, 3 thumb keys, 2 hands, which matches MiniDox. It defaults to Colemak-DH, uses home-row dual-function modifiers, uses thumb layer-taps, and divides layers by purpose: Nav, Mouse, Button, Media, Num, Sym, and Fun. Its key design rule is opposite-hand access: hold a thumb key on one hand, press keys on the other hand, and keep movement within one key unit from home.

Specific patterns worth stealing:

- Number layer as a numpad, not a top-row copy.
- Symbol layer as shifted companions, reducing Shift chording for common symbols.
- Navigation on the home cluster, with line/page movement nearby.
- Mouse and media exist but are separate sublayers, not prominent on the base path.
- Bootloader lives on a same-hand sublayer behind a thumb hold and pinky key, not on base.
- Additional risky features require double-tap activation in Miryoku's reference design.

Tradeoff: Miryoku's home-row mods are elegant but can misfire for fast rolling typists. It is also a full system; partially copying it can be worse than adopting its layer logic deliberately.

### Seniply

Seniply is a 34-key, six-layer Colemak-DH layout built around thumb layer selection and one-shot/sticky modifiers instead of mod-tap home-row modifiers. It uses an Extend layer for navigation, editing, and one-shot home-row modifiers; a dedicated Function layer; a Symbols layer; and a Numbers layer. Numbers use a numpad arrangement, while symbols keep brackets, shifted-number symbols, and mathematical symbols in memorable positions.

Specific pattern: use one-shot mods on a nav/extend layer to avoid home-row mod timing risk. This maps well to MiniDox because the current layout already has three thumbs per side, enough to support Base, Shift, Nav/Extend, Sym, Num, and Fun without making every alpha a dual-role key.

Tradeoff: one-shot modifiers are usually less fluid for repeated modifier use than well-tuned home-row mods. They are also conceptually different from "hold a key and chord"; the user must like sticky sequencing.

### Callum Half-Layer Mods

Callum's current keymap moves away from both mod-tap and classic Callum one-shot mods. The new idea is "half-layer mods": each side has its own symbol half-layer. Holding the opposite half exposes modifiers on the side that is not being typed, so shortcuts like Command-C can be made without obscuring the `C` key and without tap-hold timing on alpha keys. The Ferris keymap source shows base, nav, left-symbol, right-symbol, and function layers, with boot on Nav.

Specific pattern: split symbols/mods by keyboard half. For MiniDox, this could mean left thumb exposes right-side symbol/mod half, right thumb exposes left-side symbol/mod half, and pressing both produces the full symbol surface.

Tradeoff: some symbols become multi-key motions. The benefit is deterministic behavior: fewer timing races than home-row mods or dense combos.

### urob ZMK Config

urob's 34-key ZMK config is the richest source for modern chord vocabulary. It is not directly portable to stock MiniDox QMK, but the ideas are strong.

Observed patterns:

- "Timeless" home-row mods: balanced hold-taps, `require-prior-idle-ms`, positional hold-tap, and delayed hold-trigger decisions to reduce rolling misfires.
- Combos instead of a symbol layer for many symbols. Vertical combos mirror the standard number-row symbols, while horizontal combos produce brackets and paired delimiters.
- Combo activation has idle gating and different fast/slow terms to reduce accidental triggers.
- `S` + `T` starts a leader key; leader sequences handle Unicode, output/Bluetooth toggles, reset, and bootloader.
- Smart Num starts a number layer that stays active while typing numbers and exits on non-number input.
- Smart Mouse is a combo-activated mouse layer that auto-deactivates on other keypresses.
- A "magic" thumb combines repeat, sticky shift, held shift, and caps-word.

Tradeoff: ZMK behavior modules are not drop-in QMK code. The source is best used as inspiration for feature shape, not as an implementation recipe for the AVR MiniDox.

### Xavv1 Cantor Remix

Xavv1 is a QMK Cantor keymap that explicitly blends Miryoku with a combo-optimized "Kombol" approach. Its QMK source has home-row mod-taps, separate Nav/Num/Sym/Game/SendString/RGB layers, tap dance for app shortcuts, mouse layers, and many combos. The combo file has concrete definitions for diacritics, quotes, brackets, parentheses, angle brackets, minus/equal/plus/underscore, semicolon/colon/tilde/pipe/backslash, and text macros such as "the" and "and".

Specific pattern: use combos for delimiter pairs and punctuation that are hard to memorize on a full symbol layer. Keep a normal Num layer and a normal Sym layer too; combos are an overlay, not the only path.

Tradeoff: this map includes personal send-string macros and prominent mouse/app layers. Those should not carry over to the MiniDox before the safe reflash checkpoint, and private macros should not be copied.

### GergoPlex Combo Gist

The GergoPlex gist is an extreme combo-first QMK example: one main layer plus a symbol layer, Colemak-style alphas, tap-dance tap/hold home-row modifiers, and combos for grave, tab, equals, minus, quote, escape, home/page/end navigation. It intentionally does not use the outermost thumb keys so it can port to 34-key boards.

Specific pattern: a compact combo overlay can add navigation and punctuation without adding layers. For MiniDox, this argues for starting with a small, memorable combo set rather than a huge chord table.

Tradeoff: the gist itself warns it relies on QMK behavior/fixes around tap dance and has a lot of custom code. Treat it as a design sketch, not a low-risk base.

### Andrew Rae Kyria

Andrew Rae's Kyria keymap has a custom userspace leader implementation that does not use QMK's timeout-based leader behavior, plus a display string for current leader state, combos, vim mode, and case modes such as caps word and x-case. This is innovative and source-backed, but too large for a first MiniDox redesign pass.

Specific pattern: leader sequences are better for rare, mnemonic commands than for common symbols. Good targets are layout switching, case modes, debug, bootloader/reset, and maybe a few text-editing modes.

Tradeoff: the custom leader and vim/case modes add maintenance surface. They should come after baseline keymap stability.

### Less Useful Baselines

Cantor's upstream default QMK keymap is a plain single-layer QWERTY map. TOTEM publishes Vial/QMK and ZMK firmware artifacts and source, but the top-level source sampled here was more useful as hardware context than as an elegant keymap source. Architeuthis Dux source indexes exist, but this scout did not find a richer, broadly documented keymap than the urob, Xavv1, Callum, Seniply, and Miryoku sources above.

## Tradeoffs For A MiniDox Redesign

- Direct firmware Colemak is compatible with Miryoku/Seniply style, but published Colemak-DH layouts should be adapted intentionally. Do not accidentally switch the user from settled Colemak to Colemak-DH unless asked.
- MiniDox's 36 keys make Miryoku a natural structural reference. The safest redesign path is not "add every clever feature"; it is "use a coherent 36-key layer grammar, then add a few chords."
- Home-row mods are the most controversial feature. Miryoku and urob show how powerful they can be; Callum and Seniply show serious alternatives when timing risk matters.
- Combos are strongest for paired delimiters, punctuation, escape/tab/backspace, and rare commands. They are weaker as the only way to type all numbers/symbols unless the user wants a chord-first layout.
- Leader sequences are best for rare mnemonic actions. They are a poor replacement for frequent punctuation.
- Mouse/debug should be present but hidden. Miryoku and urob both isolate mouse layers; upstream MiniDox hides boot on adjust. That fits the user's constraint.
- Anything requiring custom state machines, custom leader, smart layers, or dense combo timing should wait until a known-good firmware can be rebuilt and reflashed safely.

## Candidate Ideas For Later MiniDox Design

1. Miryoku-shaped layer grammar: keep 5x3+3 as the mental model; use opposite-hand thumbs for Nav, Num, Sym, and Fun; keep mouse/media/debug as tertiary layers.

2. Direct Colemak base with MiniDox thumbs: left thumbs could be Escape, Tab, Space; right thumbs could be Backspace, Enter, Delete or Shift. This preserves Miryoku's thumb-value idea while honoring firmware-level Colemak.

3. Numpad number layer: place `7 8 9`, `4 5 6`, `1 2 3`, with `0` and dot on thumbs or bottom positions. This is common across Miryoku, Seniply, urob, and Xavv1.

4. Paired symbol layer plus paired combos: put brackets, braces, parentheses, angle brackets, quote/double quote, minus/plus/equal/underscore in symmetric positions. Add only 8-12 high-confidence combos first, inspired by urob and Xavv1.

5. Choose one modifier philosophy deliberately:
   - conservative: one-shot mods on an Extend/Nav layer, Seniply-style;
   - fluid: home-row mods with cross-hand/bilateral tuning, Miryoku/urob-style;
   - deterministic: Callum-style half-layer mods.

6. Combo-entered leader: use a mnemonic combo such as `S` + `T` or a thumb+home chord to enter leader mode, then reserve leader sequences for rare actions: `boot`, `reset`, `base`, `game`, maybe Unicode/compose later. Do not spend a physical key on leader.

7. Smart Shift thumb: evolve the current one-shot shift into a "magic thumb" concept only after baseline stability. Candidate behavior: tap sticky shift, hold shift, double-tap caps-word, optional repeat key. Keep it simpler than urob's full behavior at first.

8. Extend-style navigation layer: arrows on home positions, home/end/page nearby, cut/copy/paste/undo on the opposite side, and modifiers available on the layer. This is more useful than a standalone mouse layer for daily programming.

9. Hidden recovery/system layer: put `QK_BOOT`, `QK_RBT`, EEPROM/debug keys, and optional base/game switching behind Lower+Raise or an equivalent chorded layer. Require a deliberate two-step action for bootloader, matching Miryoku's "additional features require double tap" spirit.

10. Add a temporary QWERTY/game layer, not a host dependency. Since firmware emits Colemak directly, a QWERTY-position game layer can help games and shortcuts without changing the host layout.

## Unknowns And Follow-Up Requirements

- I did not clone or build any external keymap. All source inspection was via GitHub raw/API and web pages.
- I did not inspect every listed keyboard exhaustively. Corne/Kyria/Ferris/Sweep are represented through strong reusable personal keymaps; Lily58/Sofle/Gergo/GergoPlex/TOTEM/Cantor/Architeuthis Dux were sampled where they produced relevant source or context.
- I did not verify which QMK features are enabled or size-safe on the user's exact MiniDox firmware. Dense combos, tap dance, repeat/caps-word, mouse keys, and leader all have firmware-size and behavior risks on AVR.
- I did not attempt flashing, bootloader entry, or physical keyboard inspection.

## Scout Recommendation

For the future redesign, start with a Miryoku/Seniply-level layer architecture and only a small combo overlay. The best first experimental target is: direct Colemak base, numpad Num layer, paired Sym layer, Extend/Nav layer, hidden Adjust/System layer with bootloader, and either Seniply-style one-shot mods or Callum-style half-layer mods. Defer urob-style smart layers, custom leader engines, tap-dance-heavy home-row mods, and large combo dictionaries until after a safe reflash checkpoint and a measured typing trial.
