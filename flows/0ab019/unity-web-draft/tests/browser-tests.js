import { createHttpAdapter, createSyntheticAdapter, createUnityClient } from "../app.js";

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
      provenance_status: "backend-supplied-provenance",
    });
    return conversation;
  };
  const client = createUnityClient({ root, adapter });
  await client.ready;
  const entry = root.querySelector('[data-entry-id="synthetic:unrecognized"]');
  assert(entry, "An unrecognized source kind must remain visible.");
  equal(entry.querySelector(".message-source").textContent, "Origin unknown", "Unrecognized kinds must not infer a living origin.");
  equal(entry.querySelector(".provenance").textContent, "backend-supplied-provenance", "Supplied provenance should remain visible.");
});

test("keeps provisional HTTP routes same-origin and relative", async () => {
  const calls = [];
  const fetchImpl = async (url, options) => {
    calls.push({ url, options });
    return { ok: true, json: async () => ({}) };
  };
  const adapter = createHttpAdapter({ fetchImpl });
  await adapter.getRoster();
  await adapter.getConversation("flow id");
  await adapter.send({ request_id: "request-1", flow_id: "flow-1", text: "raw" });
  equal(calls.map((call) => call.url).join(","), "/mentci/v1/roster,/mentci/v1/conversation?flow_id=flow%20id,/mentci/v1/send", "HTTP routes must stay on the current origin.");
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
