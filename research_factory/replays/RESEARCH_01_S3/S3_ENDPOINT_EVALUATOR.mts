import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

const target = process.argv[2];
if (!target) {
  console.error("usage: bun S3_ENDPOINT_EVALUATOR.mts <extension.ts>");
  process.exit(64);
}

const handlers = new Map<string, Function[]>();
const commands = new Map<string, any>();
const sentMessages: any[] = [];
let registeredTools = 0;

let editorInputAvailable = true;
let uiVisible = false;
let customCalls = 0;
let widgetSetCalls = 0;
let widgetClearCalls = 0;
const widgets = new Map<string, unknown>();

const ui = {
  notify: (_message: string, _kind?: string) => {},
  setWidget: (key: string, content: unknown) => {
    if (content === undefined) {
      widgetClearCalls++;
      widgets.delete(key);
      if (widgets.size === 0) uiVisible = false;
    } else {
      widgetSetCalls++;
      widgets.set(key, content);
      uiVisible = true;
    }
  },
  custom: (factory: Function) => {
    customCalls++;
    editorInputAvailable = false;
    let settled = false;
    let resolvePromise!: () => void;
    const promise = new Promise<void>((resolvePromiseArg) => {
      resolvePromise = resolvePromiseArg;
    });
    const done = () => {
      if (settled) return;
      settled = true;
      uiVisible = false;
      editorInputAvailable = true;
      resolvePromise();
    };
    factory(undefined, { fg: (_kind: string, text: string) => text }, undefined, done);
    uiVisible = true;
    return promise;
  },
};

const ctx: any = { hasUI: true, ui };
const pi: any = {
  registerCommand: (name: string, options: any) => commands.set(name, options),
  registerTool: (_tool: unknown) => { registeredTools++; },
  sendMessage: (message: unknown, options?: unknown) => sentMessages.push({ message, options }),
  on: (event: string, handler: Function) => {
    const list = handlers.get(event) ?? [];
    list.push(handler);
    handlers.set(event, list);
  },
};

const mod = await import(pathToFileURL(resolve(target)).href + "?endpoint=" + Date.now());
if (typeof mod.default !== "function") {
  console.log(JSON.stringify({ pass: false, error: "NO_DEFAULT_EXTENSION" }, null, 2));
  process.exit(2);
}
await mod.default(pi);

async function fire(event: string, payload: any) {
  for (const handler of handlers.get(event) ?? []) await handler(payload, ctx);
}

function assistant(text: string) {
  return { role: "assistant", content: [{ type: "text", text }] };
}

async function end(text: string) {
  await fire("message_end", { message: assistant(text) });
}

async function update(fullText: string, delta: string) {
  await fire("message_update", {
    message: assistant(fullText),
    assistantMessageEvent: { type: "text_delta", delta },
  });
}

const OPEN = String(mod.OPEN_SIGNAL ?? "[[SIGNAL_UI_OPEN]]");
const CLOSE = String(mod.CLOSE_SIGNAL ?? "[[SIGNAL_UI_CLOSE]]");

const checks: Record<string, boolean> = {};

checks.command_registered = commands.has("start");
const beforeInactiveOps = customCalls + widgetSetCalls + widgetClearCalls;
await end(OPEN);
checks.inactive_no_reaction = (customCalls + widgetSetCalls + widgetClearCalls) === beforeInactiveOps && !uiVisible;

const start = commands.get("start");
if (start?.handler) await start.handler("", ctx);
checks.hidden_protocol =
  sentMessages.length === 1 &&
  sentMessages[0]?.message?.display === false &&
  String(sentMessages[0]?.message?.content ?? "").includes(OPEN) &&
  String(sentMessages[0]?.message?.content ?? "").includes(CLOSE);

await end(OPEN + "\n" + CLOSE);
checks.combined_signal_ignored = !uiVisible;

await end("prefix " + OPEN);
checks.embedded_open_ignored = !uiVisible;

await end(OPEN);
checks.open_visible = uiVisible;
const opsAfterOpen = customCalls + widgetSetCalls + widgetClearCalls;
checks.editor_available_while_open = editorInputAvailable;
checks.open_uses_nonblocking_projection = customCalls === 0 && widgetSetCalls === 1;

await end(OPEN);
checks.repeated_open_idempotent = (customCalls + widgetSetCalls + widgetClearCalls) === opsAfterOpen;

let stream = "";
for (let i = 0; i < 64; i++) {
  const delta = "x";
  stream += delta;
  await update(stream, delta);
}
checks.streaming_updates_do_not_recreate_ui = (customCalls + widgetSetCalls + widgetClearCalls) === opsAfterOpen;
checks.editor_available_during_streaming = editorInputAvailable && uiVisible;

await end("still working " + CLOSE);
checks.embedded_close_ignored = uiVisible;

await end(CLOSE);
checks.close_hides_ui = !uiVisible;
checks.editor_available_after_close = editorInputAvailable;
checks.no_tool_registration = registeredTools === 0;

const publicKeys = [
  "command_registered",
  "inactive_no_reaction",
  "hidden_protocol",
  "combined_signal_ignored",
  "embedded_open_ignored",
  "open_visible",
  "repeated_open_idempotent",
  "embedded_close_ignored",
  "close_hides_ui",
  "no_tool_registration",
];
const lifecycleKeys = [
  "editor_available_while_open",
  "open_uses_nonblocking_projection",
  "streaming_updates_do_not_recreate_ui",
  "editor_available_during_streaming",
  "editor_available_after_close",
];

const result = {
  target: resolve(target),
  pass: Object.values(checks).every(Boolean),
  public_behavior_pass: publicKeys.every((key) => checks[key]),
  lifecycle_pass: lifecycleKeys.every((key) => checks[key]),
  checks,
  counters: { customCalls, widgetSetCalls, widgetClearCalls, registeredTools },
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.pass ? 0 : 2);
