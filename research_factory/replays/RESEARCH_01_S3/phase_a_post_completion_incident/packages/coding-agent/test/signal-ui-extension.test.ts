import { describe, expect, it, vi } from "vitest";
import signalUiExtension, {
	CLOSE_SIGNAL,
	CONTROL_MESSAGE_TYPE,
	OPEN_SIGNAL,
} from "../../../.pi/extensions/signal-ui.js";
import type { MessageEndEvent } from "../src/core/extensions/types.js";
import type {
	ExtensionAPI,
	ExtensionCommandContext,
	ExtensionContext,
	ExtensionHandler,
	ExtensionUIContext,
	RegisteredCommand,
} from "../src/index.js";

type MessageEndHandler = ExtensionHandler<MessageEndEvent>;
type CommandOptions = Omit<RegisteredCommand, "name">;

function assistantMessageEnd(text: string): MessageEndEvent {
	return {
		type: "message_end",
		message: {
			role: "assistant",
			content: [{ type: "text", text }],
		} as MessageEndEvent["message"],
	};
}

function createHarness() {
	let messageEndHandler: MessageEndHandler | undefined;
	let uiOpen = false;
	let editorInputAvailable = true;

	const commands = new Map<string, CommandOptions>();
	const sendMessage = vi.fn();
	const notify = vi.fn();
	const custom = vi.fn(
		(
			factory: (
				tui: never,
				theme: never,
				keybindings: never,
				done: (result: void) => void,
			) => unknown,
		): Promise<void> =>
			new Promise<void>((resolve) => {
				editorInputAvailable = false;
				factory(
					undefined as never,
					{ fg: (_color: string, text: string) => text } as never,
					undefined as never,
					() => {
						uiOpen = false;
						editorInputAvailable = true;
						resolve();
					},
				);
				uiOpen = true;
			}),
	);
	const setWidget = vi.fn((_key: string, content: string[] | undefined) => {
		uiOpen = content !== undefined;
	});

	const api = {
		registerCommand: (name: string, options: CommandOptions) => commands.set(name, options),
		on: (event: string, handler: MessageEndHandler) => {
			if (event === "message_end") messageEndHandler = handler;
		},
		sendMessage,
	} as unknown as ExtensionAPI;

	const context = {
		hasUI: true,
		ui: { custom, notify, setWidget } as unknown as ExtensionUIContext,
	} as unknown as ExtensionCommandContext;

	signalUiExtension(api);

	return {
		commands,
		context,
		custom,
		isEditorInputAvailable: () => editorInputAvailable,
		getMessageEndHandler: () => {
			if (!messageEndHandler) throw new Error("message_end handler was not registered");
			return messageEndHandler;
		},
		isUiOpen: () => uiOpen,
		sendMessage,
		setWidget,
	};
}

async function start(harness: ReturnType<typeof createHarness>): Promise<void> {
	const command = harness.commands.get("start");
	if (!command) throw new Error("/start command was not registered");
	await command.handler("", harness.context);
}

describe("signal UI extension", () => {
	it("starts the protocol with one hidden custom message", async () => {
		const harness = createHarness();

		await start(harness);

		expect(harness.sendMessage).toHaveBeenCalledOnce();
		expect(harness.sendMessage).toHaveBeenCalledWith(
			{
				customType: CONTROL_MESSAGE_TYPE,
				content: expect.stringContaining(OPEN_SIGNAL),
				display: false,
			},
		);
		const [{ content }] = harness.sendMessage.mock.calls[0] as [{ content: string }];
		expect(content).toContain(CLOSE_SIGNAL);
		expect(content).toContain("Never emit both signals in the same response");
	});

	it("keeps editor input available while separate exact signals open and close the UI", async () => {
		const harness = createHarness();
		const handleMessageEnd = harness.getMessageEndHandler();

		await start(harness);
		await handleMessageEnd(assistantMessageEnd(`${OPEN_SIGNAL}\n${CLOSE_SIGNAL}`), harness.context as ExtensionContext);
		expect(harness.custom).not.toHaveBeenCalled();
		expect(harness.setWidget).not.toHaveBeenCalled();

		await handleMessageEnd(assistantMessageEnd(OPEN_SIGNAL), harness.context as ExtensionContext);
		expect(harness.custom).not.toHaveBeenCalled();
		expect(harness.setWidget).toHaveBeenCalledOnce();
		expect(harness.isUiOpen()).toBe(true);
		expect(harness.isEditorInputAvailable()).toBe(true);
		const [widgetKey] = harness.setWidget.mock.calls[0] as [string, string[]];

		await handleMessageEnd(assistantMessageEnd(`still working; ${CLOSE_SIGNAL}`), harness.context as ExtensionContext);
		expect(harness.isUiOpen()).toBe(true);
		expect(harness.isEditorInputAvailable()).toBe(true);

		await handleMessageEnd(assistantMessageEnd(CLOSE_SIGNAL), harness.context as ExtensionContext);
		expect(harness.isUiOpen()).toBe(false);
		expect(harness.isEditorInputAvailable()).toBe(true);
		expect(harness.setWidget).toHaveBeenLastCalledWith(widgetKey, undefined);
	});

	it("ignores a close signal until the UI has been opened", async () => {
		const harness = createHarness();
		const handleMessageEnd = harness.getMessageEndHandler();

		await start(harness);
		await handleMessageEnd(assistantMessageEnd(CLOSE_SIGNAL), harness.context as ExtensionContext);

		expect(harness.custom).not.toHaveBeenCalled();
		expect(harness.setWidget).not.toHaveBeenCalled();
		expect(harness.isUiOpen()).toBe(false);
		expect(harness.isEditorInputAvailable()).toBe(true);
	});
});
