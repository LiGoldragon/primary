# MiniDox QMK Candidate Review

## Task And Scope

Scout review for choosing a modern QMK keymap/example style basis for porting the recovered MiniDox layout in `/git/github.com/LiGoldragon/kibord`.

Scope followed:

- Read-only source inspection plus this requested report.
- No firmware edits, no flashing, no hardware queries, no commits, no pushes.
- QMK-focused. ZMK-only patterns were treated as background inspiration, not shortlist bases.
- Prior report consulted: `/home/li/primary/agent-outputs/MiniDoxLayoutResearch/Scout-ResearchSynthesis.md`.

## Sources And Commands Consulted

Local repository:

- `/git/github.com/LiGoldragon/kibord/README.md`
- `/git/github.com/LiGoldragon/kibord/flake.nix`
- `/git/github.com/LiGoldragon/kibord/flake.lock`
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c`
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/config.h`
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/rules.mk`
- `jj status` in `/git/github.com/LiGoldragon/kibord`

Intent query:

- `spirit "(PublicTextSearch [QMK MiniDox layout style modern keymap])"` returned `(Error [no matching record])`.

Public source-level references:

- Pinned QMK MiniDox keymaps at `b1093e9da5f27253f3db692352daf5cf4ad5b98d`, ref `0.33.8`:
  - `https://github.com/qmk/qmk_firmware/tree/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/maple_computing/minidox/keymaps`
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/maple_computing/minidox/keymaps/default/keymap.c`
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/maple_computing/minidox/keymaps/bepo/keymap.c`
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/maple_computing/minidox/rev1/keyboard.json`
- Miryoku reference:
  - `https://github.com/manna-harbour/miryoku/blob/master/docs/reference/readme.org`
- Callum half-layer mods:
  - `https://github.com/callum-oakley/keymap/blob/main/README.md`
  - `https://github.com/callum-oakley/vial-qmk/blob/r2g-callum/keyboards/mechboards/ferris/r2g/keymaps/callum/keymap.c`
- Seniply:
  - `https://github.com/stevep99/seniply/blob/master/docs/index.html`
  - `https://stevep99.github.io/seniply/`
- Xavv1 Cantor Remix:
  - `https://github.com/malparty/xavv1-remix/blob/main/keymap.c`
  - `https://github.com/malparty/xavv1-remix/blob/main/features/combo.c`
- Pinned QMK compact split examples:
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/gboards/gergoplex/keymaps/colemak-dhm/keymap.c`
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/crkbd/keymaps/default/keymap.c`
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/splitkb/kyria/keymaps/default/keymap.c`
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/sofle/keymaps/default/keymap.c`
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/lily58/keymaps/default/keymap.c`
- QMK feature docs at the pinned revision:
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/docs/features/leader_key.md`
  - `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/docs/features/combo.md`
- Andrew Rae Kyria keymap, inspected as a non-shortlist advanced example:
  - `https://github.com/andrewjrae/kyria-keymap`

## Local Observed Facts

- `/git/github.com/LiGoldragon/kibord/flake.nix:6-8` pins `qmk_firmware` to `github:qmk/qmk_firmware/0.33.8`.
- `/git/github.com/LiGoldragon/kibord/flake.lock:131-145` locks QMK to revision `b1093e9da5f27253f3db692352daf5cf4ad5b98d`.
- `/git/github.com/LiGoldragon/kibord/flake.nix:268-275` builds MiniDox as QMK target `maple_computing/minidox/rev1`, with keymap source `./maple_computing/minidox/LiGoldragon`.
- `/git/github.com/LiGoldragon/kibord/README.md:3` says the MiniDox target is build-only and must not be flashed until review.
- `/git/github.com/LiGoldragon/kibord/README.md:16` says MiniDox emits Colemak directly and should not depend on host Colemak.
- `/git/github.com/LiGoldragon/kibord/README.md:35-41` documents `QK_LEAD`, leader sequence `r e s e t`, `QK_BOOT` fallbacks, and tri-layer `FUNCTIONS`.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c:28-32` has the recovered firmware-Colemak base.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c:42-46` currently places numbers in recovered/nonlinear positions on `NUMBERS`.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c:49-53` keeps direct `QK_BOOT` on `FUNCTIONS`.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c:64-70` activates `FUNCTIONS` from `SYMBOLS` + `NUMBERS` and preserves `leader r e s e t` calling `reset_keyboard()`.
- `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/rules.mk` enables Leader and disables Command/Bootmagic.
- `jj status` in `/git/github.com/LiGoldragon/kibord` reported no changes.
- No local `/git/github.com/.../qmk_firmware` checkout was found by scoped `find /git/github.com -maxdepth 4`.

## Candidate Shortlist

### 1. Miryoku Reference Architecture

Source: `https://github.com/manna-harbour/miryoku/blob/master/docs/reference/readme.org`

What it offers:

- The cleanest complete 36-key design grammar: 5 columns, 3 rows, 3 thumbs, two hands.
- Purpose-separated layers: Nav, Mouse, Button, Media, Num, Sym, Fun.
- Opposite-hand thumb layer access, home-row dual-function modifiers, thumb layer-taps, hidden bootloader/system features.
- Clear written principles and high-quality visual references.

Why the user might prefer it:

- It turns the recovered MiniDox layout into something recognizable as a modern compact split layout rather than a recovered table dump.
- MiniDox is exactly the physical shape Miryoku is designed around.
- It gives the follow-on worker a coherent answer for every key category instead of ad hoc layer fill.

Pros:

- Best match to MiniDox geometry.
- Strong layer organization.
- Mouse/debug/system features are naturally secondary.
- Direct firmware Colemak can be preserved by using the user's recovered `BASE` instead of Miryoku's default Colemak-DH.
- Good mental model for hiding `QK_BOOT` behind deliberate access.

Cons and risks:

- Full Miryoku adoption would switch several user behaviors at once.
- Home-row mods are timing-sensitive, and the recovered layout already has mod-taps in some uncertain physical positions.
- Miryoku is now mostly documentation/configurator data, not a simple local QMK `keymap.c` to copy line-for-line.

Portability effort:

- Medium. Use as architecture and comments, not as direct code. Keep the local MiniDox `LAYOUT_split_3x5_3` and map layers manually.

Sales pitch:

- Choose Miryoku if the goal is "make this a serious modern 36-key QMK MiniDox." It is the strongest primary pattern because it supplies a complete, teachable layer grammar while still allowing the recovered Colemak base to remain authoritative.

### 2. Upstream MiniDox `default` + `bepo`

Sources:

- `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/maple_computing/minidox/keymaps/default/keymap.c`
- `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/maple_computing/minidox/keymaps/bepo/keymap.c`

What it offers:

- Exact pinned-QMK MiniDox examples at the repo's active revision.
- Proven `LAYOUT_split_3x5_3` visual comments.
- `default` shows Lower/Raise/Adjust, standard number row left-to-right, and `QK_BOOT` on Adjust.
- `bepo` proves a direct firmware-level non-QWERTY base plus layer-tap thumbs and mod-tap bottom row are acceptable in an upstream MiniDox keymap.

Why the user might prefer it:

- Lowest risk for build compatibility.
- The visual comment convention is immediately understandable and already MiniDox-shaped.
- It keeps the follow-on change small and auditable.

Pros:

- Exact keyboard and exact pinned QMK.
- Very low firmware-size risk.
- Best source for physical diagram comments.
- Good fallback for implementing the user's requested number reorder: put `KC_1` through `KC_0` in the same left-to-right physical positions as the MiniDox default Raise row.

Cons and risks:

- Not modern enough by itself: no elegant compact-keyboard layer philosophy, no useful combo strategy, no strong docs beyond inline ASCII.
- `default` uses older custom layer keycodes and process handling; the local keymap already uses modern `LT()` and `update_tri_layer_state()`, which should be preserved.
- `bepo` uses BEPO keycodes and is a pattern only, not a layout source.

Portability effort:

- Low. Copy the diagram style and MiniDox-specific layer labels; do not copy keycodes wholesale.

Sales pitch:

- Choose upstream MiniDox as the "truthy visual shell." It is not the most elegant layout, but it is the safest way to make the port look like a real MiniDox QMK keymap.

### 3. Callum Half-Layer Mods

Sources:

- `https://github.com/callum-oakley/keymap/blob/main/README.md`
- `https://github.com/callum-oakley/vial-qmk/blob/r2g-callum/keyboards/mechboards/ferris/r2g/keymaps/callum/keymap.c`

What it offers:

- A modern 34-key QMK layout philosophy that avoids home-row mod and combo timing ambiguity.
- Left-symbol and right-symbol half layers, with modifiers on the opposite half so shortcuts do not obscure the target alpha key.
- Good explanatory docs and compact source.
- `QK_BOOT` is placed on the Nav layer in the inspected Ferris keymap.

Why the user might prefer it:

- It gives a deterministic alternative to Miryoku-style home-row mods.
- It is easier to trial on recovered firmware because it uses layers more than custom state machines.
- MiniDox has 36 keys, so it has enough thumbs to host the idea without contorting the base.

Pros:

- Strong low-risk modifier strategy.
- Clear modern sales pitch: fewer tap-hold races.
- Good source to copy for layer names and half-layer organization.
- QMK-native source exists.

Cons and risks:

- The implementation inspected targets Ferris/Vial, not MiniDox or pinned QMK directly.
- It is 34-key and `LAYOUT_split_3x5_2_enc`, so thumb mapping must be adapted.
- Some symbols can become multi-key motions; not everyone likes that.
- It is less widely standardized than Miryoku.

Portability effort:

- Medium. Translate the concept into MiniDox `SYMBOLS_LEFT`/`SYMBOLS_RIGHT` or similar layers only if the user wants a modifier philosophy change. Otherwise borrow only the organization and documentation style.

Sales pitch:

- Choose Callum if the user values predictable shortcuts over clever tap-hold behavior. It is the best fallback pattern when home-row mod risk is the main concern.

### 4. Seniply Extend / One-Shot Modifier Pattern

Sources:

- `https://github.com/stevep99/seniply/blob/master/docs/index.html`
- `https://stevep99.github.io/seniply/`

What it offers:

- A six-layer compact layout for at least 34 keys.
- Thumb-selected layers without dual-role alpha mod-taps as a requirement.
- Extend layer with navigation, editing, and sticky/one-shot modifiers.
- Symbols and numbers are explained with strong learning rationale.

Why the user might prefer it:

- It is the cleanest conservative pattern for reducing tap-hold timing risk while staying compact.
- Its Extend layer can modernize the MiniDox without losing the recovered base.
- It keeps mouse/debug secondary and makes ordinary editing more central.

Pros:

- Very good documentation and visual conventions.
- Good alternative to home-row mods.
- Directly compatible with the user's desire to keep firmware-level Colemak.
- Gives a practical route for one-shot modifiers and navigation without a large combo table.

Cons and risks:

- The repository is docs/downloads oriented, not a simple QMK source basis.
- It defaults to Colemak-DH; the user wants recovered firmware Colemak, not an unrequested alpha switch.
- It partly relies on host layout assumptions for symbols; the local MiniDox should stay explicit about keycodes.

Portability effort:

- Medium-low as an idea, higher if trying to reproduce it exactly. Best used to design the Nav/Extend layer and one-shot modifier behavior.

Sales pitch:

- Choose Seniply if the user wants a friendly, stable daily-driver feel more than advanced chord tricks. It is the best "boring in the right way" modifier/navigation pattern.

### 5. Xavv1 Cantor Remix

Sources:

- `https://github.com/malparty/xavv1-remix/blob/main/keymap.c`
- `https://github.com/malparty/xavv1-remix/blob/main/features/combo.c`

What it offers:

- QMK-native compact split source with Colemak-style base, layer-tap thumbs, Nav/Num/Sym layers, game layer, send-string layer, RGB layer, tap dance, mouse, and many combos.
- Concrete combo implementation for brackets, parentheses, angle brackets, quote variants, minus/equal/plus/underscore, semicolon/colon/tilde/pipe/backslash, and text macros.
- Good example of using combos as an overlay rather than the entire layout.

Why the user might prefer it:

- It shows what a modern QMK compact split can look like when combos are first-class.
- It is more directly copyable into QMK C than Miryoku or Seniply docs.
- The bracket/punctuation combo vocabulary is useful for programming on MiniDox.

Pros:

- QMK source is concrete and readable.
- Good source for a small, optional combo overlay.
- Shows boot/reset access on a hidden layer with `QK_BOOT` and `QK_RBT`.
- Shows numpad-ish numbers and paired symbols.

Cons and risks:

- Too personal to copy wholesale: email/name macros, app shortcuts, send strings, RGB, mouse layers, and tap dance add risk and clutter.
- Targets Cantor `LAYOUT_split_3x6_3`, not MiniDox `LAYOUT_split_3x5_3`.
- Dense combos plus mod-taps may raise misfire and firmware-size risk on AVR.

Portability effort:

- Medium-high if copied broadly. Low if borrowing only the combo file pattern for a tiny set of delimiter/punctuation combos.

Sales pitch:

- Choose Xavv1 as a spice rack, not as the meal. It is the best source for tasteful QMK combo examples after the base MiniDox port is stable.

### 6. Pinned QMK GergoPlex Colemak-DHm

Source: `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/gboards/gergoplex/keymaps/colemak-dhm/keymap.c`

What it offers:

- A compact QMK-in-tree `LAYOUT_split_3x5_3` keymap at the exact pinned QMK revision.
- Colemak-DHm alpha layer, three layers, thumb layer-taps, home/bottom mod-taps, combo map comment, mouse buttons on symbol layer, and numbers/function/navigation combined.
- Straightforward source with strong ASCII diagrams.

Why the user might prefer it:

- It is both modern-ish and inside the pinned QMK source, reducing version drift.
- It demonstrates a MiniDox-compatible physical macro directly.
- Its comments are compact and readable.

Pros:

- Exact `LAYOUT_split_3x5_3` shape.
- Pinned QMK version match.
- Good visual layer comments.
- Has a standard top-row number layer `1` through `0`, matching the requested number direction.

Cons and risks:

- GergoPlex is not MiniDox hardware.
- Alpha default is Colemak-DHm, not recovered Colemak.
- Numbers/functions/navigation are compressed into one layer, which may be less clean than Miryoku/Seniply.
- It includes `g/keymap_combo.h`, which may imply userspace or generated combo dependency not directly present in MiniDox.

Portability effort:

- Low-medium. It is the easiest non-MiniDox source to adapt mechanically because the layout macro matches.

Sales pitch:

- Choose GergoPlex if the follow-on worker needs a pinned-QMK, 3x5+3 code skeleton quickly. It is less conceptually polished than Miryoku, but far more directly translatable.

### 7. QMK Kyria / Sofle / Lily58 Visual Baselines

Sources:

- `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/splitkb/kyria/keymaps/default/keymap.c`
- `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/sofle/keymaps/default/keymap.c`
- `https://github.com/qmk/qmk_firmware/blob/b1093e9da5f27253f3db692352daf5cf4ad5b98d/keyboards/lily58/keymaps/default/keymap.c`

What they offer:

- Well-established split keyboard ASCII diagram conventions.
- Kyria gives a clearly documented multi-base setup including QWERTY, Dvorak, Colemak-DH, Nav, Sym, Function, Adjust, and a layer template.
- Sofle gives a common Lower/Raise/Adjust convention with Colemak layer and OS/word navigation helpers.
- Lily58 gives classic Lower/Raise/Tri-layer visual formatting.

Why the user might prefer it:

- These are familiar to QMK readers and reviewers.
- They are useful when making the recovered MiniDox source look like "normal QMK."

Pros:

- Strong visual comment style.
- Pinned QMK version match.
- Useful for docs and layer diagram polish.

Cons and risks:

- Larger boards with extra columns/keys; not layout bases for MiniDox.
- Their actual key placement is not portable without deleting many keys.
- Less useful than upstream MiniDox or GergoPlex for physical MiniDox geometry.

Portability effort:

- Low if borrowing comments/templates only. High and not recommended if adapting keymaps.

Sales pitch:

- Choose these only for presentation polish. They should not drive behavior.

## Non-Shortlist Notes

- Andrew Rae Kyria (`https://github.com/andrewjrae/kyria-keymap`) has advanced QMK ideas: custom userspace leader, case modes, combos, OLED display, and vim mode. It is valuable as future inspiration for leader/case modes, but too much custom surface for this first MiniDox port.
- urob's ZMK configuration remains a high-quality inspiration source for combos and smart layers, but it is ZMK-first and should not be the basis for a QMK MiniDox implementation.
- Upstream QMK `crkbd/default` is a clean small split baseline, but it is simpler than the MiniDox/GergoPlex options and less useful than Miryoku/Callum/Seniply for modern design.
- Upstream QMK `cantor/default` is too minimal to be a style basis.

## Recommendation

Primary pattern: Miryoku architecture plus upstream MiniDox visual shell.

Reason:

- Miryoku is the best conceptual match for a modern 36-key MiniDox: 5x3+3, thumb-driven layers, single-purpose layers, hidden system features, and secondary mouse/media.
- Upstream MiniDox at the pinned QMK revision is the safest presentation and compatibility basis for comments, physical layout order, and `LAYOUT_split_3x5_3`.
- This pairing lets the worker produce a modern QMK example without pretending the recovered layout is a clean-sheet Miryoku clone.

Fallback: Callum half-layer mods, with Seniply Extend as the conservative modifier/navigation fallback.

Reason:

- If home-row mod timing feels too risky or too far from the recovered behavior, Callum gives a deterministic layer-only modifier strategy.
- If even half-layer symbol mechanics feel too novel, Seniply's Extend layer and one-shot/sticky mods are the lowest-risk modern alternative.

Use Xavv1 and GergoPlex as secondary sources:

- Xavv1 for a small optional combo overlay after baseline stability.
- GergoPlex for pinned-QMK `LAYOUT_split_3x5_3` code shape and compact diagrams.

## Follow-On Implementation Constraints

- Preserve firmware-level Colemak. Do not switch to host Colemak. Do not silently change recovered Colemak to Colemak-DH, Miryoku default alphas, or Seniply default alphas.
- Keep the recovered `BASE` as the authoritative starting point unless the user explicitly approves alpha changes.
- Redo the `NUMBERS` layer so the same physical placeholders currently holding numbers become `KC_1` at the left-most number position through `KC_0` at the right-most number position. The current source has numbers at `/git/github.com/LiGoldragon/kibord/maple_computing/minidox/LiGoldragon/keymap.c:42-46`; the worker should reorder only those number-bearing positions unless also changing the layer architecture.
- Preserve `QK_LEAD` access and `leader r e s e t` behavior. Current implementation is at `keymap.c:68-70` and must remain functionally equivalent.
- Preserve direct `QK_BOOT` fallback on a hidden/system layer. Current positions are at `keymap.c:49-53`.
- Keep build-only/no flash. Verification should be `nix build .#minidox` or equivalent build-only check.
- Avoid copying personal macros, send strings, emails, RGB/app shortcuts, or large combo dictionaries from examples.
- Keep mouse/debug secondary. Do not let mouse layers or debug controls dominate the port.
- Be cautious with AVR firmware size. Leader is already enabled; adding combos, tap dance, mouse keys, repeat/caps-word, or custom state machines should be incremental and build-checked.
- Prefer local QMK `LT()` and `update_tri_layer_state()` style over older upstream MiniDox custom layer keycodes unless there is a concrete compatibility reason.
- If adding combos, start with a tiny delimiter/punctuation set and enable `COMBO_ENABLE = yes` only after checking firmware size.

## Checks Not Run

- I did not run `nix build .#minidox`; this task was comparison scouting, and previous reports already show build-only checks for related states.
- I did not clone external repositories.
- I did not inspect every keymap under every candidate keyboard. I sampled source-level examples most relevant to MiniDox, compact splits, and the prior research report.
- I did not query, flash, reset, or inspect hardware.
