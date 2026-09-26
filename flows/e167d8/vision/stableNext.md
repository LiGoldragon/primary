# Stable and next services

## Every service runs a stable and a next side by side on different sockets; rolling migration

> It probably would be a good practice for a lot of these to have a stable package in [CriomOS] and then a next package, in the same way that we do the remote server.
>
> Maybe we can even create a reusable code pattern there in Next or something, or put it in a skill so these services can have a Next component that has a different socket. Then you can run both side by side when you do a migration. You can start into the Next service and then the stable version becomes the same as the Next and that would be the next step. The services can move to the stable socket on the next chance they get and then the Next socket, when it's free, becomes available again for another update. We have this rolling mechanism to keep updating.

-- psyche, STT, 2026-09-26 ~11:55, to e167d8, on deploying Flow/Message 0.16. Transcription corrected: "KaliOS" → "CriomOS".
