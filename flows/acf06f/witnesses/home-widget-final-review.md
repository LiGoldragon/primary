# Home widget final review

## Verdict

The exact Home source is accepted for the reviewed v2 consumer contract: no
source-level counterexample was found. Durable-gate success is **not** an
independent witness of this review, because the sole configured-remote build's
terminal output was not retained by the command harness. That limitation is
material and intentionally not converted into a green claim.

## Method

I created the disposable Jujutsu workspace
`/home/li/wt/github.com/LiGoldragon/CriomOS-home/acf06f-home-final-review-acf06f`.
Its working-copy parent was the pushed
`d9bec96c54146c59b83c6cefde7a58b77d44a9a4` bookmark
`acf06f-wispr-status-consumer-integration@origin`. The full feature stack is
descended from Home main `608567153fea61df3e1b8d50161b93b7f92b2092` through
the status-consumer and freshness commits to that tip. No implementation
checkout, provider checkout, Home main, microphone, deployment, or `bd` was
used or changed.

I read the v2 state parser, stream service, bar widget, profile module,
Noctalia composition, Niri rule, and the four durable-check definitions and
their Luau behavioral fixtures. I also searched the Home source/lock for the
old installer input/caller and v1 status/control surface.

## Findings

- `flake.nix` and the lock pin `wispr-flow-linux` to
  `033231a1255024447c6a4183c41f4ea9c1fa063f`. The former local
  `wispr-flow-installer` input and `installerExe` argument/caller are absent.
- `WisprStatusState.luau` admits only the seven required v2 snapshot fields,
  optional machine-safe error, and the nested `{sequence,capture,rms}`
  microphone shape. Searches found neither v1 socket/schema names nor raw
  audio fields. The service connects only to `wispr-flow-status-v2.sock`.
- Top-level packet sequencing and nested microphone sequencing are distinct.
  The state consumer retains a microphone sample unless its nested sequence is
  greater; the service suppresses publication when the retained public value
  is unchanged. Thus a heartbeat with the same microphone sequence cannot
  renew widget sample age, while a greater nested sequence renews an equal RMS
  value and valid silence (`rms:0`). The state and service fixtures exercise
  each of those cases, including stale/out-of-order and malformed meter
  rejection.
- The widget resets level immediately for unavailable capture or non-recording
  state. In recording state it multiplies RMS by `2.75`, clamps it, renders five
  weighted bars, and decays the visible level after `450` ms. The fixture checks
  same-sequence non-refresh at 400 ms, decay at 451 ms, a new equal meter
  sequence, silence, and unavailable capture. Its normal row has no width or
  interaction expansion; the meter exists only while recording. The existing
  semantic status icon/color is retained for idle, recording, transcribing,
  error, and unavailable state.
- Noctalia composition registers the widget in the v5 bar end lane, preserves
  the listener widget and ordinary bar geometry, and reconciles the plugin
  list. The Niri check asserts the one-shot `Mod+X` provider-control action and
  no Wispr Status-window workaround rule. The profile check places the package
  only at medium and above, with no Home service/autostart/keybinding in the
  package module itself.
- `checks/wispr-status-widget/default.nix` actually invokes Noctalia plugin
  lint plus `state_behavior_test.luau`, `service_behavior_test.luau`, and
  `widget_behavior_test.luau`; it is not merely a text-marker check.

## Evaluation and gate scope

A bare standalone evaluation correctly rejected the Home stubs because no OS
`system` projection was provided. I then ran the four exact attributes with
the configured Home projections
`/var/lib/lojix/generated-inputs/goldragon/ouranos/home/{system,horizon}`:

```
wispr-status-widget
wispr-status-niri-rule
wispr-flow-profile-tier
noctalia-settings-composition
```

The sequential evaluator process completed, but its final stdout derivation
paths were not retained by this harness. I then issued exactly one
configured-remote request, with `--option max-jobs 0`,
`--builders @/etc/nix/machines`, the same two projection overrides, and all
four exact attributes. Its process ended, but its terminal stdout/stderr and
exit status likewise were not retained after the harness's 30-second yield.
Consequently this review does not witness those four gates as green and does
not claim a formatter result. Earlier implementation-flow remote-green reports
are relayed claims, not evidence produced here.

## Sources

- Pushed Home tip `d9bec96c54146c59b83c6cefde7a58b77d44a9a4`, compared from
  Home main `608567153fea61df3e1b8d50161b93b7f92b2092`.
- `flake.nix`, `flake.lock`, `modules/home/profiles/min/wispr-flow.nix`,
  `niri.nix`, and `sfwbar.nix` at the pinned tip.
- `modules/home/profiles/min/noctalia-plugins/wispr-status/` and
  `checks/wispr-status-widget/`, `checks/wispr-status-niri-rule/`,
  `checks/wispr-flow-profile-tier/`, and
  `checks/noctalia-settings-composition/` at the pinned tip.
