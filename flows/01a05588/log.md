# Flow 01a05588

Continue flow `01a0539e` through realization. Determine whether the installed proprietary Wispr Desktop exposes a supported local IPC, deeplink, or process boundary that Listener can use as an authenticated proxy, without reading session contents, modifying the bundle, or contacting the backend.

Remembered: 01a0539e — depth 1. The earlier flow implemented and deployed Listener-facing UI work, proved isolated Wispr requests fail without yielding a transcript, retained production Listener 0.14.0, and left supported local Desktop reuse as the next read-only question. Its last response asked the living for three no-speech UI witnesses; those remain unanswered, but the flow redirected the realization toward Listener.

Settled: two independent read-only inspections found no supported/public local authenticated transcription proxy in Wispr Desktop 1.6.7. The live process exposes no TCP/UDP listener. Its sole listening Unix socket is Electron's private single-instance socket; helper channels are internal parent-child pipes. Declared `wispr-flow:` deeplinks start/stop hands-free mode, switch microphones, or navigate, but do not submit audio or return transcripts. The Desktop launcher has no transcription CLI, DBus service, native-messaging host, or advertised HTTP/socket API. No session contents were read, no endpoint was contacted, and no process or bundle was changed.

Open: realization through the installed Desktop is blocked unless Wispr supplies an official local/API integration contract, or the living explicitly opens a different round involving private backend/protocol reuse and its licensing and secret boundary. Production Listener remains unchanged.

The living then explicitly opened private API reverse engineering, stating that they have Wispr's implicit permission. Work is tracked as `wispr-flow-linux-5v0`. Static protocol archaeology and analysis of the two prior redacted failures are in progress. The authenticated session remains behind a secret-preserving program boundary; no new billable transcription call will be made until static evidence identifies what that call must discriminate.
