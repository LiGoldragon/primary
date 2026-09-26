# Wi-Fi password: where it lives and how to see it

Read-only, no secret value touched or displayed.

**1. Where it lives.** `goldragon` repo, sops-encrypted file:
`/git/github.com/LiGoldragon/goldragon/secrets/routerWifiSaePasswords.sops`.
Its only cleartext field is `data` (one ENC string) — `.sops.age[0].recipient`
is `age1wgftrgvjduazn8rrz024zj8gpn82cgmm53nmn63uhtaysyk3w3fszqrg3d`, also
listed as a PGP recipient (fp `CAE31…0CF6`).

**2. Command to display it, and what unlocks it.**
- From his own machine (ouranos), with the encrypted source file:
  `sops -d --extract '["data"]' /git/github.com/LiGoldragon/goldragon/secrets/routerWifiSaePasswords.sops`
  Unlocks with an age private key matching that recipient (default
  `~/.config/sops/age/keys.txt` or `$SOPS_AGE_KEY_FILE`), or a GPG key with
  that fingerprint — whichever he holds. No passphrase is declared by sops
  itself; his key file/GPG key may prompt on its own.
- Simpler, on Prometheus itself (the deployed host): sops-nix decrypts this
  automatically at boot using the host's own SSH host key, no manual unlock
  needed — `cat /run/secrets/routerWifiSaePasswords` as root.

**3. One password or several.** The sops document has exactly one key,
`data`. Its decrypted content is fed to hostapd as `saePasswordsFile`
(`CriomOS/modules/nixos/router/default.nix`), a format that *can* hold
several `sae_password=...` lines (optionally scoped by peer/identifier) —
which is likely why the name is plural — but the ciphertext alone doesn't
say how many lines are inside. Key names only, as asked: just `data`.

**4. Device requirements.** hostapd is configured `mode = "wpa3-sae"`
(SAE only, not a WPA2/WPA3 mixed "transition" network). A modern phone or
laptop (iOS 13+/Android 10+, current Windows/macOS/Linux) needs only the
SSID `goldragon.criome` and the password — WPA3-SAE personal needs no
certs or extra config. A WPA2-only device will still see the SSID in scans
but cannot associate: SAE-only APs don't fall back to WPA2, so it fails at
authentication.
