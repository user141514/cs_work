import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";

export const OPEN_SIGNAL = "[[SIGNAL_UI_OPEN]]";
export const CLOSE_SIGNAL = "[[SIGNAL_UI_CLOSE]]";
export const CONTROL_MESSAGE_TYPE = "signal-ui-control";

const CONTROL_MESSAGE = `## Signal UI protocol

For the next multi-turn task, coordinate with the signal UI using these exact signals:

- On the first assistant turn, emit ${OPEN_SIGNAL} as the entire textual content of the response. You may call a tool in that response to continue the task.
- On the final assistant turn, emit ${CLOSE_SIGNAL} as the entire textual content of the response.
- Keep working normally between those turns.

Never emit both signals in the same response. Do not quote, wrap, explain, or combine a signal with other text.`;

type Signal = "open" | "close";

function getSignal(message: { role: string; content?: unknown }): Signal | undefined {
	if (message.role !== "assistant" || !Array.isArray(message.content)) return undefined;

	const text = message.content
		.filter((block): block is { type: "text"; text: string } => {
			if (typeof block !== "object" || block === null) return false;
			return "type" in block && block.type === "text" && "text" in block && typeof block.text === "string";
		})
		.map((block) => block.text)
		.join("")
		.trim();

	if (text === OPEN_SIGNAL) return "open";
	if (text === CLOSE_SIGNAL) return "close";
	return undefined;
}

export default function signalUiExtension(pi: ExtensionAPI) {
	let active = false;
	let dismissUi: (() => void) | undefined;

	const closeUi = () => {
		const dismiss = dismissUi;
		dismissUi = undefined;
		dismiss?.();
	};

	pi.registerCommand("start", {
		description: "Start the signal-driven UI test",
		handler: async (_args, ctx) => {
			if (!ctx.hasUI) {
				ctx.ui.notify("Signal UI test requires interactive mode", "error");
				return;
			}

			closeUi();
			active = true;
			pi.sendMessage({
				customType: CONTROL_MESSAGE_TYPE,
				content: CONTROL_MESSAGE,
				display: false,
			});
		},
	});

	pi.on("message_end", async (event, ctx) => {
		if (!active) return;

		const signal = getSignal(event.message);
		if (signal === "open" && !dismissUi) {
			let thisUiDismiss: (() => void) | undefined;
			const uiClosed = ctx.ui.custom<void>((_tui, theme, _keybindings, done) => {
				thisUiDismiss = () => done();
				dismissUi = thisUiDismiss;

				return {
					render: () => [
						theme.fg("accent", "Signal UI is open"),
						theme.fg("dim", `Waiting for signal: ${CLOSE_SIGNAL}`),
					],
					invalidate: () => {},
				};
			});

			void uiClosed.then(
				() => {
					if (dismissUi === thisUiDismiss) dismissUi = undefined;
				},
				() => {
					if (dismissUi === thisUiDismiss) dismissUi = undefined;
					active = false;
				},
			);
			return;
		}

		if (signal === "close" && dismissUi) {
			active = false;
			closeUi();
		}
	});
}
