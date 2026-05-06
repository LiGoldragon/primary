# Skill — system specialist

*Maintaining the operating-system layer underneath the workspace.*

---

## What this skill is for

Use this skill when the work is about making the operator's system run:
CriomOS, CriomOS-home, lojix deployment, horizon projection, desktop
runtime, user services, input devices, Niri, Noctalia, and system/home
interfaces.

The system specialist is a capability, not a primary-workspace lock role.
Do not claim the `operator` role merely because this skill is active. Follow
whatever coordination protocol the current workspace uses, but keep the
concept separate: this skill is about OS/platform work.

---

## Owned area

The system specialist knows how these pieces fit:

- **CriomOS**: NixOS host platform, system modules, device access, groups,
  udev, kernel modules, and the `nixosConfigurations.target` surface.
- **CriomOS-home**: Home Manager profile, Niri bindings, Noctalia, user
  packages, user services, and desktop tools such as Whisrs.
- **lojix-cli**: deploy/build/activate entry point that projects cluster
  proposals into the inputs CriomOS and CriomOS-home consume.
- **horizon-rs**: typed projection/schema source for horizon fields.
- **goldragon**: the cluster proposal data used by lojix for Li's machines.

When a task crosses system and home boundaries, preserve ownership. Example:
Whisrs packaging, keybindings, tray state, clipboard recovery, and transcript
history live in CriomOS-home; `/dev/uinput` group/module/udev access lives in
CriomOS.

---

## Working pattern

Start by reading the relevant repo's `AGENTS.md`, `ARCHITECTURE.md`, and
`skills.md`. For CriomOS and CriomOS-home, also run `bd list --status open`
and read `docs/ROADMAP.md`.

Prefer the existing deployment path over one-off commands:

- Home activation goes through lojix `HomeOnly ... Activate`.
- System builds/switches go through lojix-projected CriomOS inputs.
- Build pushed origin with `--refresh` before trusting the result.
- Keep store paths in shell variables, not prose.
- Do not signal niri.

Secrets stay out of Nix and broad process environments. For paid cloud
inference, follow the repo rule: local model first, then ask before using a
paid key unless the user explicitly authorized that call in the current task.

---

## Runtime interfaces

The system specialist gives the user working interfaces, not just packages:

- keybindings that work in Niri;
- visible status for long-running actions;
- user services that restart through Home Manager activation;
- recovery paths for fragile desktop input;
- logs that expose operational state without leaking private content.

For STT prompts and likely transcription mistakes, read this workspace's
`skills/stt-interpreter.md`.

---

## See also

- CriomOS's `skills.md`
- CriomOS-home's `skills.md`
- this workspace's `skills/stt-interpreter.md`
- this workspace's `skills/autonomous-agent.md`
- lore's `AGENTS.md`
