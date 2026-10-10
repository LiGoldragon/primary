import { createSignalAdapter, createSyntheticAdapter, createUnityClient } from "../app.js";

const results = document.querySelector("#test-results");
const summary = document.querySelector("#test-summary");
const fixtures = document.querySelector("#test-fixtures");
const tests = [];

function test(name, run) {
  tests.push({ name, run });
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function equal(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(`${message}\nExpected: ${String(expected)}\nActual: ${String(actual)}`);
  }
}

function createRoot() {
  const root = document.createElement("div");
  fixtures.append(root);
  return root;
}

function input(node, value) {
  node.value = value;
  node.dispatchEvent(new Event("input", { bubbles: true }));
}

function submit(node) {
  node.closest("form").dispatchEvent(new SubmitEvent("submit", { bubbles: true, cancelable: true }));
}

function until(predicate, target = document) {
  if (predicate()) return Promise.resolve();
  return new Promise((resolve, reject) => {
    const observer = new MutationObserver(() => {
      if (!predicate()) return;
      observer.disconnect();
      clearTimeout(timeout);
      resolve();
    });
    const timeout = setTimeout(() => {
      observer.disconnect();
      reject(new Error("Timed out waiting for a DOM state change."));
    }, 2000);
    observer.observe(target, { childList: true, subtree: true, characterData: true, attributes: true });
  });
}

test("observes once on load, once on Refresh, and labels the fixture honestly", async () => {
  const root = createRoot();
  const adapter = createSyntheticAdapter();
  let rosterReads = 0;
  let conversationReads = 0;
  const originalGetRoster = adapter.getRoster;
  const originalGetConversation = adapter.getConversation;
  adapter.getRoster = (...args) => {
    rosterReads += 1;
    return originalGetRoster(...args);
  };
  adapter.getConversation = (...args) => {
    conversationReads += 1;
    return originalGetConversation(...args);
  };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  equal(rosterReads, 1, "Initial rendering should make exactly one roster request.");
  equal(conversationReads, 1, "Initial rendering should make exactly one selected-conversation request.");
  equal(root.querySelectorAll(".flow-card").length, 2, "Both fixture flows should render.");
  assert(root.querySelector(".mode-badge").textContent.includes("Synthetic demo"), "Demo mode should be labelled.");
  assert(root.querySelector(".demo-notice").textContent.includes("Nothing on this page is live"), "The demo notice should deny live status.");
  const refresh = root.querySelector("button[aria-label^='Refresh roster']");
  refresh.click();
  await until(() => rosterReads === 2 && conversationReads === 2 && !refresh.disabled, root);
  equal(rosterReads, 2, "One explicit Refresh should add exactly one roster request.");
  equal(conversationReads, 2, "One explicit Refresh should add exactly one selected-conversation request.");
});

test("orders eligible entries oldest first and preserves unknown origin", async () => {
  const root = createRoot();
  const client = createUnityClient({ root, adapter: createSyntheticAdapter() });
  await client.ready;
  const sequences = [...root.querySelectorAll(".message")].map((node) => Number(node.dataset.sequence));
  equal(sequences.join(","), "10,20,30", "Conversation entries should be oldest first.");
  equal(root.querySelectorAll(".message-source")[2].textContent, "Origin unknown", "Unknown origin must remain explicit.");
});

test("renders uncorrelated and unavailable Herdr seats without inventing flow IDs", async () => {
  const root = createRoot();
  const adapter = createSyntheticAdapter();
  const base = adapter.getRoster;
  adapter.getRoster = async () => {
    const roster = await base();
    roster.flows.push({ flow_id: null, name: "Uncorrelated seat", seat: "claude",
      state: "done", pane_id: "synthetic:p3", terminal_id: "synthetic:t3",
      correlation_status: "unknown" });
    roster.flows.push({ flow_id: null, name: "Unavailable seat", seat: "claude",
      state: "done", pane_id: "synthetic:p4", terminal_id: "synthetic:t4",
      correlation_status: "unavailable" });
    return roster;
  };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  const cards = [...root.querySelectorAll(".flow-card")];
  equal(cards.length, 4, "Every observed seat should render.");
  assert(cards[2].disabled && cards[3].disabled, "Uncorrelated seats cannot fetch or send.");
  assert(cards[2].textContent.includes("uncorrelated synthetic:p3"), "Unknown seat must show pane identity, not a fake flow ID.");
  assert(cards[3].textContent.includes("unavailable"), "Unavailable correlation must remain distinct.");
});

test("loads older pages only on click and exposes complete snapshot coverage", async () => {
  const root = createRoot();
  const adapter = createSyntheticAdapter();
  const base = adapter.getConversation;
  const cursor = { native_session_id: "synthetic-full-uuid", file_device: "1", file_inode: "2",
    snapshot_bytes: "200", before_byte: "100" };
  const calls = [];
  adapter.getConversation = async (flowId, suppliedCursor = null) => {
    calls.push(suppliedCursor);
    const page = await base(flowId);
    page.snapshot_bytes = "200";
    page.current_bytes = "200";
    page.window_start = suppliedCursor ? "0" : "100";
    page.window_end = suppliedCursor ? "100" : "200";
    page.source_status = suppliedCursor ? "complete" : "partial";
    page.older_cursor = suppliedCursor ? null : cursor;
    if (suppliedCursor) page.entries = [{ entry_id: "synthetic:older", sequence: 1,
      source_ordinal: "1", occurred_at: "2026-09-18T22:00:00Z", text: "Older synthetic entry",
      source_kind: "user-input", provenance: "Unknown" }];
    return page;
  };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  equal(calls.length, 1, "Onload fetches latest once, never older automatically.");
  assert(!client.elements.olderButton.hidden, "Partial snapshot should offer Load older.");
  client.elements.olderButton.click();
  await until(() => root.querySelector('[data-entry-id="synthetic:older"]'), root);
  equal(calls.length, 2, "One click fetches exactly one older page.");
  equal(client.state.conversation.source_status, "complete", "Covered fixed snapshot becomes complete.");
  assert(client.elements.olderButton.hidden, "No cursor means no further automatic or manual page.");
});

test("renders unrecognized source kinds as unknown without losing provenance", async () => {
  const root = createRoot();
  const adapter = createSyntheticAdapter();
  const originalGetConversation = adapter.getConversation;
  adapter.getConversation = async (flowId) => {
    const conversation = await originalGetConversation(flowId);
    conversation.entries.push({
      entry_id: "synthetic:unrecognized",
      sequence: 25,
      occurred_at: "2026-09-18T22:09:30Z",
      text: "An adapter supplied a newer source kind.",
      source_kind: "backend-new-kind",
      attributed_actor: "Unverified claim",
      provenance: "Machine",
    });
    return conversation;
  };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  const entry = root.querySelector('[data-entry-id="synthetic:unrecognized"]');
  assert(entry, "An unrecognized source kind must remain visible.");
  equal(entry.querySelector(".message-source").textContent, "Origin unknown", "Unrecognized kinds must not infer a living origin.");
  equal(entry.querySelector(".provenance").textContent, "unknown · Machine", "Supplied provenance should remain visible beside unknown source kind.");
});

test("Signal bridge sends only codec-produced binary frames", async () => {
  const sent = [];
  let recordedId;
  const codec = {
    encode_observe_roster: (id) => {
      recordedId = id;
      return new Uint8Array([0, 0, 0, 1, 42]);
    },
    decode_roster_observed: () => ({
      request_id: recordedId,
      observed_at_nanos: "1789769640000000000",
      source_status: "complete",
      flows: [],
    }),
  };
  const adapter = createSignalAdapter({
    loadCodec: async () => codec,
    openSocket: () => {
      const listeners = new Map();
      const socket = {
        addEventListener: (name, callback) => listeners.set(name, callback),
        close: () => {},
        send: (frame) => {
          sent.push(frame);
          listeners.get("message")({ data: new Uint8Array([0, 0, 0, 1, 99]).buffer });
        },
      };
      queueMicrotask(() => listeners.get("open")());
      return socket;
    },
  });
  const roster = await adapter.getRoster();
  equal(roster.source_status, "complete", "A typed complete status should reach the view adapter.");
  assert(sent[0] instanceof Uint8Array, "The bridge must send binary codec output, never JSON.");
  equal(sent[0].join(","), "0,0,0,1,42", "The socket must receive the codec frame unchanged.");
});

test("typed Signal unavailability is not rendered as an empty roster", async () => {
  let request;
  const adapter = createSignalAdapter({
    loadCodec: async () => ({
      encode_observe_roster: (id) => { request = id; return new Uint8Array([0, 0, 0, 1, 7]); },
      decode_roster_observed: () => ({
        request_id: request,
        source_status: "unavailable",
        reason: "PersonaUnavailable",
      }),
    }),
    openSocket: () => {
      const listeners = new Map();
      const socket = {
        addEventListener: (name, callback) => listeners.set(name, callback),
        close: () => {},
        send: () => listeners.get("message")({ data: new Uint8Array([0, 0, 0, 1, 7]).buffer }),
      };
      queueMicrotask(() => listeners.get("open")());
      return socket;
    },
  });
  const root = createRoot();
  const client = createUnityClient({ root, adapter });
  await client.ready;
  assert(client.elements.observationStatus.textContent.includes("PersonaUnavailable"), "Typed unavailability must remain visible.");
  assert(!root.querySelector(".roster-list").textContent.includes("No flows were present"), "Unavailable is not empty success.");
});

test("fetches once on selection and retains a separate draft per flow", async () => {
  const root = createRoot();
  const adapter = createSyntheticAdapter();
  const selected = [];
  const originalGetConversation = adapter.getConversation;
  adapter.getConversation = (flowId) => {
    selected.push(flowId);
    return originalGetConversation(flowId);
  };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  input(client.elements.textarea, "Draft for Fable");
  root.querySelector('[data-flow-id="field02"]').click();
  await until(() => root.querySelector(".conversation-title").textContent === "Field", root);
  input(client.elements.textarea, "Draft for Field");
  root.querySelector('[data-flow-id="fable01"]').click();
  await until(() => root.querySelector(".conversation-title").textContent === "Fable", root);
  equal(client.elements.textarea.value, "Draft for Fable", "Returning to a flow should restore its draft.");
  equal(selected.join(","), "fable01,field02,fable01", "Each initial or selected flow should be fetched exactly once.");
});

test("sends only the three request fields and never inserts an optimistic entry", async () => {
  const root = createRoot();
  const adapter = createSyntheticAdapter();
  const baseSend = adapter.send;
  let releaseSend;
  adapter.send = (payload) => new Promise((resolve) => {
    releaseSend = async () => resolve(await baseSend(payload));
  });
  const client = createUnityClient({ root, adapter });
  await client.ready;
  const before = root.querySelectorAll(".message").length;
  input(client.elements.textarea, "  A bounded synthetic request  \n");
  submit(client.elements.textarea);
  await until(() => client.elements.receipt.textContent.includes("Sending"), root);
  equal(root.querySelectorAll(".message").length, before, "Pending send must not add a conversation entry.");
  assert(client.elements.textarea.disabled, "Composer should be disabled while the receipt is pending.");
  await releaseSend();
  await until(() => client.elements.receipt.textContent.includes("Accepted"), root);
  equal(Object.keys(adapter.requests[0]).sort().join(","), "flow_id,request_id,text", "The transport payload must contain only request_id, flow_id, and text.");
  equal(adapter.requests[0].text, "  A bounded synthetic request  \n", "Non-empty text must be sent byte-for-byte as entered.");
  equal(root.querySelectorAll(".message").length, before, "Accepted send must not add an optimistic entry.");
  equal(client.elements.textarea.value, "", "An accepted receipt should clear that flow's draft.");
});

test("treats a send transport failure as client unavailable and preserves the draft", async () => {
  const root = createRoot();
  const adapter = createSyntheticAdapter();
  adapter.send = async () => { throw new Error("Browser transport offline"); };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  input(client.elements.textarea, "Keep this draft");
  submit(client.elements.textarea);
  await until(() => client.elements.receipt.textContent.includes("Browser transport offline"), root);
  assert(client.elements.receipt.textContent.includes("Client unavailable"), "Transport failure should be presented as a client error.");
  assert(!client.elements.receipt.textContent.includes("Rejected"), "Transport failure must not invent a backend rejected receipt.");
  equal(client.elements.textarea.value, "Keep this draft", "Transport failure must preserve the draft.");
});

for (const disposition of ["held", "rejected"]) {
  test(`renders ${disposition} receipts and preserves the draft`, async () => {
    const root = createRoot();
    const client = createUnityClient({ root, adapter: createSyntheticAdapter({ disposition }) });
    await client.ready;
    input(client.elements.textarea, `${disposition} draft`);
    submit(client.elements.textarea);
    await until(() => client.elements.receipt.textContent.toLowerCase().includes(disposition), root);
    equal(client.elements.textarea.value, `${disposition} draft`, `${disposition} should preserve the draft for retry or review.`);
  });
}

test("shows an honest unavailable state without substituting demo data", async () => {
  const root = createRoot();
  const adapter = {
    mode: "live",
    getRoster: async () => { throw new Error("Test transport unavailable"); },
    getConversation: async () => { throw new Error("Unexpected conversation request"); },
    send: async () => { throw new Error("Unexpected send request"); },
  };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  equal(root.querySelector(".mode-badge").textContent, "Live adapter", "Live mode should be named explicitly.");
  assert(client.elements.observationStatus.textContent.includes("Test transport unavailable"), "Adapter errors should remain visible.");
  equal(root.querySelectorAll(".flow-card").length, 0, "A failed live adapter must not fall back to fixture flows.");
  equal(root.querySelectorAll(".demo-notice").length, 0, "Live mode must not show a synthetic demo notice.");
});

test("renders selected-conversation failure as unavailable", async () => {
  const root = createRoot();
  const adapter = createSyntheticAdapter();
  adapter.getConversation = async () => { throw new Error("Conversation transport offline"); };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  assert(root.querySelector(".conversation-list").textContent.includes("Conversation unavailable"), "Conversation failures need an explicit unavailable state.");
  assert(root.querySelector(".conversation-list").textContent.includes("Conversation transport offline"), "Conversation failures should retain their error detail.");
  assert(!root.querySelector(".conversation-list").textContent.includes("No eligible entries"), "Failure must not be rendered as an empty conversation.");
});

test("exposes labelled controls and a 44px minimum target", async () => {
  const root = createRoot();
  const client = createUnityClient({ root, adapter: createSyntheticAdapter() });
  await client.ready;
  equal(root.querySelector('label[for="unity-compose"]').textContent, "Message selected flow", "The composer needs a programmatic label.");
  assert(root.querySelector("button[aria-label^='Refresh roster']"), "Refresh needs a keyboard-readable label.");
  equal(root.querySelector(".roster-list").tagName, "UL", "The roster should use a native list.");
  assert([...root.querySelector(".roster-list").children].every((node) => node.tagName === "LI"), "Native list items should wrap roster buttons.");
  assert([...root.querySelectorAll(".flow-card")].every((node) => !node.hasAttribute("role")), "Buttons should retain native button semantics.");
  const sendHeight = Number.parseFloat(getComputedStyle(client.elements.sendButton).minHeight);
  assert(sendHeight >= 44, "Interactive buttons should have at least a 44px minimum height.");
});

let passed = 0;
for (const { name, run } of tests) {
  const item = document.createElement("li");
  try {
    await run();
    item.className = "test-pass";
    item.textContent = `PASS — ${name}`;
    passed += 1;
  } catch (error) {
    item.className = "test-fail";
    item.textContent = `FAIL — ${name}\n${error instanceof Error ? error.message : String(error)}`;
  }
  results.append(item);
}

const failed = tests.length - passed;
summary.textContent = `${passed} passed, ${failed} failed`;
document.body.dataset.testStatus = failed === 0 ? "passed" : "failed";
document.title = failed === 0 ? "PASS — Unity Web DOM tests" : "FAIL — Unity Web DOM tests";
