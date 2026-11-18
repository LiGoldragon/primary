# Proposal 2 bounded lifetime-test corrections

Authority: Opus ogme and Core 1ty3 supersede the twelve-finding hold.
Only findings 1–3 are corrected; findings 4–12 are waived for this bounded test,
not claimed fixed. The original 942913e8 sealed archive remains untouched.

1. RequestIds/control IDs are exactly four lowercase ASCII base36 characters;
   the negative unknown is valid and excludes known request/control IDs.
2. Native and CLI Result/Done accepted receipts must name the exact answered
   invocation ID. Initial and carry checks share the same verifier.
3. One grouped exact decoder validates all delivery-state variants and their
   pinned nested payloads. Decoded Retryable/Failed stop the matrix.

Changed code/fixtures: driver/{controller,matrix,test_controller,test_matrix}.py.
Worker disposition: /tmp/proposal2-lifetime-123.uwRbfIDd/report.md.

## Actual synthetic test result

Core 1ty3 authorized local own-driver synthetic tests for at most five minutes,
without provider/service/auth/native/network actions. The exact final command:

```sh
cd /home/li/primary/flows/1bd07a/driver
timeout 300s python3 -B -m unittest -v test_controller test_bootstrap test_orchestration test_matrix test_wiring
```

58 tests passed in 0.026 seconds, exit 0. Log and exit receipt:
/tmp/proposal2-fixtures-123-89ad44.txZ17VMN/{unittest-final.log,exit.txt}.
The fixtures use synthetic files, pipes and fakes; no provider, service,
production credential, native flow or network action was invoked.
Rust fe5a6930871707a7086c9a647867a519734220ef and accepted packages are unchanged.
Field owns the approved 20-minute/two-Luna/12-instructed-turn matrix, using the
Field-captured own-session reply naming the delivered ID as t39d's witness.
Native success, activation and final a8fa acceptance are not claimed here.
