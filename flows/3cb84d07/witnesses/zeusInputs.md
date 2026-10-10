# Zeus retained inputs

Method: probe `find /var/lib/lojix/generated-inputs/goldragon/zeus -type f
-printf '%TY-%Tm-%TdT%TH:%TM:%TS %s %p\\n'`; `find
/var/lib/lojix/audits -maxdepth 1`; and `sed` the generated `flake.nix` stubs.

Observed:

- Retained materialization shapes include `full-os`, `complete-host`, and
  `user-environment`.
- Their latest observed materialization times are 2026-07-02 (`full-os`),
  2026-07-25 (`complete-host`), and 2026-07-29 (`user-environment`).
- The generated stubs select `x86_64-linux`; host shapes carry
  `includeHome = true` and `includeAllFirmware = true`.
- Two local audit links named for Bird/Zeus point to Home Manager store
  outputs from 2026-07-28. No current Zeus target link was observed.

Inference: these are retained managed-output artifacts from earlier work, not
evidence of a current Zeus profile or a current proposal evaluation. Encrypted
secret files are present in the retained input trees; their contents were not
read or reported.
