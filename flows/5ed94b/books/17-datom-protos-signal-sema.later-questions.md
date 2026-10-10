Presentation.{ «Datom, Protos, Signal and Sema, later questions» }

5. **Where Signal goes beyond our own machines.** On 10 September Signal was "portable rkyv + whatever protocol we decide to standardize". On 13 August you named the router "routable signal then", while a universal Signal stayed with CapnProto for other platforms. Is CapnProto out of Signal entirely? Yes or no.

6. **Is a stream its own kind?** On 6 August: "I think we make stream a forest kind", heard as "fourth kind". On 7 August a stream was "a section inside the object". Is a stream only a section of an interface (yes), or also a fourth kind of object beside the others (no)?

7. **One datom tool for agents.** On 14 September, as a question: "Basically, you could almost just make it a single field and use Datom to contain all the data, so it's the most simple MCP server ever. It's just a string." Today agents call each command in the shell. Should agents reach every Nexus through one tool that takes and returns a single datom string? Yes or no.

8. **A path inside a datom.** On 29 September you weighed letting a datom name a file in place of its payload, and said: "It's a fairly deep modification of the datom language. Not necessarily the worst approach but I don't think it's very pure. Using paths is very setup-dependent so it's not a very good idea for a system that wants to be correct." Is that option dropped for good? Yes or no.

9. **Datom in every machine prompt.** On 19 September: "You just have a small description, a limited-size description, and then the models are reminded if they break protocol, but we can adjust and just truncate the description and mark it as oversized, right?" Should the oversized mark be a variant on every free-text description in our types now (yes), or wait until the system prompt itself is written in datom (no)?

10. **Who knows the caller.** On 28 September: "Maybe eventually the CLI talks to one of the nexuses, like Flow or something, so that Flow can tell it which flow that process is." Should every Nexus ask Flow who called it (1), or should each Nexus check the calling process itself (2)?

11. **A Signal skill.** On 15 September you asked: "Do we have a skill for signal? Maybe we should." None exists yet. Should one be written now, holding the simple-form standard and the request-and-response shape? Yes or no.

12. **Reading Ethos as datom.** Your reviewed vision leaves open whether Ethos could be read as datom in one pass, and sets it aside. Should it stay set aside until Ethos produces working Rust on its own? Yes or no.
