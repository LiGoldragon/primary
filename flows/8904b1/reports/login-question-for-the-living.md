# How should a test seat get its login?

A test of the newer Flow needs to start three small, disposable Claude seats in
an isolated place, with a scratch home of their own. A seat started there finds
no login, because your login lives under your real home. There are two ways to
give it one. Three flows are waiting on the choice, and I will not make it,
because your own words and a written rule point in different directions.

**Way one: copy.** Your credentials file is copied into a fresh, disposable
configuration directory, and the rest of the configuration is generated. The
test seat never touches your own directory.

**Way two: share.** The test seat is pointed at your own configuration
directory. Nothing is copied. The seat finds your login the way every real seat
does, and writes there what any seat writes: its history and its transcript.

What you said on 26 September, in order:

> I don't know. Should we use the logins in place? Is that better? Maybe.

And about twenty minutes later:

> I think the best would be to copy the login credentials and then generate all
> the configuration details that work for our test sandbox.

Earlier, on 14 September:

> …a light sandbox, which is basically a sandbox of my home environment, and it
> can reuse my login, but with a different user environment.

What stands against the copy:

- The rule on secrets, as written, forbids carrying a secret in a temporary
  file. A copy that is deleted when the test ends is one.
- One thing nobody knows: if a test seat using the copy renews the login, the
  renewed login is written to the copy and not to your own file. If your own
  file is then left holding a login that no longer works, every real seat would
  lose its login at its next renewal. No one has established whether that
  happens. The copy has never been used to start a seat.

What stands against sharing:

- It is not full isolation. The test seats write into the directory your real
  seats use.
- It is not what you said last.
- One flow reports that Herdr, the terminal manager the seats run in, writes its
  own hooks and settings into the configuration directory it is pointed at. If
  so, sharing could change your own settings, which every real seat reads when
  it starts. Whether it has done so is being checked, by file names and times
  only.

What is known of each in practice: sharing has started test seats twice, on
26 September, with no trouble recorded. The copy exists as code that has never
started a seat.

I ruled for sharing at first, from the rule on secrets, without having looked
for your words. That was my error. I have withdrawn the ruling. Both ways are
held, and nothing has been started.

**The question:** copy, or share? And if copy: does your word stand as the
authorization to set up credentials for this test, knowing the one thing nobody
knows?

## Sources

- The living, 2026-09-26 ~13:25, STT — `flows/e167d8/log.md`: "I don't know.
  Should we use the logins in place? Is that better? Maybe."
- The living, 2026-09-26 ~13:45, STT — `flows/e167d8/vision/testRepos.md`,
  "Copy only the login credentials; generate the sandbox's configuration":
  "I think the best would be to copy the login credentials and then generate all
  the configuration details that work for our test sandbox."
- The living, 2026-09-14, STT — `flows/6cc91b/vision/sandbox.md`, "A light
  sandbox of my home environment, reusing my login with a different user
  environment": "We have a sandbox test version of this, a light sandbox, which
  is basically a sandbox of my home environment, and it can reuse my login, but
  with a different user environment. …"
- All three checked verbatim against the records in the primary checkout on
  2026-09-27; each matched with no correction needed.
- Everything not quoted above is this seat's own composition, including the
  Herdr point, which relays another flow's in-progress report.
