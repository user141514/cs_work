import type { AgentMessage } from "@mariozechner/pi-agent-core";
import type { AssistantMessage, TextContent } from "@mariozechner/pi-ai";
import type {
	ExtensionAPI,
	ExtensionContext,
} from "@mariozechner/pi-coding-agent";

export const INPUT_SIGNAL = "[[SIGNAL_INPUT]]";
export const DONE_SIGNAL = "[[SIGNAL_DONE]]";

const CONTROL_MESSAGE_TYPE = "signal-ui-control";
const WIDGET_KEY = "signal-ui";
const WIDGET_LINES = [
	"Signal active - the editor remains available for input.",
];
const CONTROL_MESSAGE = `Signal UI protocol (session control):
- On the first assistant response after this message, emit ${INPUT_SIGNAL} exactly once.
- Keep the signal open while work continues across later turns.
- When the work is complete, emit ${DONE_SIGNAL} exactly once in a later assistant response.
- Never emit both signals in the same assistant response. A response containing both is invalid and ignored.
- Do not quote, explain, or alter the signal tokens.`;

type ProtocolSignal = "input" | "done";

export function readProtocolSignal(text: string): ProtocolSignal | undefined {
	const hasInput = text.includes(INPUT_SIGNAL);
	const hasDone = text.includes(DONE_SIGNAL);
	if (hasInput === hasDone) return undefined;
	return hasInput ? "input" : "done";
}

function getAssistantText(message: AgentMessage): string | undefined {
	if (message.role !== "assistant") return undefined;
	const assistantMessage = message as AssistantMessage;
	return assistantMessage.content
		.filter((block): block is TextContent => block.type === "text")
		.map((block) => block.text)
		.join("\n");
}

function reduceOpenState(open: boolean, text: string): boolean {
	const signal = readProtocolSignal(text);
	if (signal === "input") return true;
	if (signal === "done") return false;
	return open;
}

export default function signalUIExtension(pi: ExtensionAPI): void {
	let activated = false;
	let signalOpen = false;

	const projectSignal = (ctx: ExtensionContext, open: boolean): void => {
		if (!ctx.hasUI) return;
		ctx.ui.setWidget(WIDGET_KEY, open ? WIDGET_LINES : undefined, {
			placement: "aboveEditor",
		});
	};

	const observeAssistantMessage = (
		message: AgentMessage,
		ctx: ExtensionContext,
	): void => {
		if (!activated) return;
		const text = getAssistantText(message);
		if (text === undefined) return;

		const nextOpen = reduceOpenState(signalOpen, text);
		if (nextOpen === signalOpen) return;

		signalOpen = nextOpen;
		projectSignal(ctx, signalOpen);
	};

	const restoreSessionState = (ctx: ExtensionContext): void => {
		let restoredActivated = false;
		let restoredOpen = false;

		for (const entry of ctx.sessionManager.getBranch()) {
			if (
				entry.type === "custom_message" &&
				entry.customType === CONTROL_MESSAGE_TYPE
			) {
				restoredActivated = true;
				restoredOpen = false;
				continue;
			}
			if (!restoredActivated || entry.type !== "message") continue;
			const text = getAssistantText(entry.message);
			if (text !== undefined)
				restoredOpen = reduceOpenState(restoredOpen, text);
		}

		activated = restoredActivated;
		signalOpen = restoredOpen;
		projectSignal(ctx, signalOpen);
	};

	pi.registerCommand("start", {
		description: "Activate the hidden signal UI protocol for this session",
		handler: async (_args, ctx) => {
			if (activated) {
				ctx.ui.notify("Signal UI protocol is already active.", "info");
				return;
			}

			activated = true;
			signalOpen = false;
			pi.sendMessage(
				{
					customType: CONTROL_MESSAGE_TYPE,
					content: CONTROL_MESSAGE,
					display: false,
				},
				{ triggerTurn: false },
			);
			ctx.ui.notify("Signal UI protocol activated.", "info");
		},
	});

	pi.on("message_end", (event, ctx) => {
		observeAssistantMessage(event.message, ctx);
	});

	pi.on("session_start", (_event, ctx) => {
		restoreSessionState(ctx);
	});

	pi.on("session_switch", (_event, ctx) => {
		restoreSessionState(ctx);
	});

	pi.on("session_fork", (_event, ctx) => {
		restoreSessionState(ctx);
	});

	pi.on("session_tree", (_event, ctx) => {
		restoreSessionState(ctx);
	});
}
