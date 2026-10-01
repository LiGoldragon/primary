# Flow lifecycle

## A replaced flow left open is woken by messages; that is really bad

Context: The old Psyche Fable flow had not been closed after its replacement was started; the messenger registry was broken.

> You forgot: your sub-agent didn't close the old Fable so you're wasting your time going back and forth. ... The old one's still open and I bet if somebody tries to message people, they'll wake the old flow up. That's really bad.

-- psyche, typed. 2026-09-29 16:44 UTC, 183ae0, PsycheV2 Opus (session 183ae001, line 1088). Reconstructed by fe945a from transcript.
