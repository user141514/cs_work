/**
 * Message Signals Extension
 *
 * Starts an agent turn with a hidden custom message, then reacts to exact
 * marker lines in completed assistant messages.
 *
 * Usage:
 *   /start [task] - Start a signal-driven task (or continue the current task)
 *
 * The model can end a response with:
 *   [[PI_EXTENSION_INPUT]] - Ask the extension to collect user input
 *   [[PI_EXTENSION_DONE]]  - Tell the extension the task is complete
 */

import type { AssistantMessage } from "@mariozechner/pi-ai";
import type { ExtensionAPI, ExtensionContext } from "@mariozechner/pi-coding-agent";

const CUSTOM_MESSAGE_TYPE = "message-signals";
const WIDGET_KEY = "message-signals";
const INPUT_SIGNAL = "[[PI_EXTENSION_INPUT]]";
const DONE_SIGNAL = "[[PI_EXTENSION_DONE]]";

type Signal = "input" | "done";

function getAssistantText(message: AssistantMessage): string {
	let text = "";
	for (const block of message.content) {
		if (block.type !== "text") continue;
		if (text) text += "\n";
		text += block.text;
	}
	return text;
}

function getSignal(text: string): Signal | undefined {
	let sawDone = false;
	let lineStart = 0;

	for (let index = 0; index <= text.length; index++) {
		if (index < text.length && text[index] !== "\n") continue;

		const line = text.slice(lineStart, index).trim();
		if (line === INPUT_SIGNAL) return "input";
		if (line === DONE_SIGNAL) sawDone = true;
		lineStart = index + 1;
	}

	return sawDone ? "done" : undefined;
}

function setWorkflowWidget(ctx: ExtensionContext, text: string): void {
	if (!ctx.hasUI) return;
	ctx.ui.setWidget(WIDGET_KEY, [ctx.ui.theme.fg("accent", text)], { placement: "aboveEditor" });
}

function clearWorkflowWidget(ctx: ExtensionContext): void {
	if (!ctx.hasUI) return;
	ctx.ui.setWidget(WIDGET_KEY, undefined);
}

function buildStartMessage(task: string): string {
	const goal = task || "Continue the current task or conversation.";
	return `You are running under a message-signal protocol controlled by a pi extension.

Task:
${goal}

Follow these rules until the task ends:
- Work normally, including using tools when needed.
- If you cannot continue without user input, ask one clear question, make the final non-empty line exactly ${INPUT_SIGNAL}, and end the response immediately.
- After ${INPUT_SIGNAL}, do not continue the task, call tools, or emit ${DONE_SIGNAL}. Wait for the extension to send the user's answer in a new turn.
- When the task is fully complete, make the final non-empty line exactly ${DONE_SIGNAL}
- Emit at most one signal per response.
- Never quote, explain, or place a signal inside a code block.
- Do not emit ${DONE_SIGNAL} while tool calls or other work remain.`;
}

export default function messageSignals(pi: ExtensionAPI) {
	let active = false;
	let awaitingInput = false;

	pi.registerCommand("start", {
		description: "Start a task controlled by hidden message signals",
		handler: async (args, ctx) => {
			if (!ctx.hasUI) {
				ctx.ui.notify("The message-signals example requires interactive mode", "error");
				return;
			}
			if (!ctx.isIdle()) {
				ctx.ui.notify("Wait for the current turn to finish before using /start", "warning");
				return;
			}

			active = true;
			awaitingInput = false;
			setWorkflowWidget(ctx, "Signal task active: waiting for the model");

			pi.sendMessage(
				{
					customType: CUSTOM_MESSAGE_TYPE,
					content: buildStartMessage(args.trim()),
					display: false,
				},
				{ triggerTurn: true },
			);
		},
	});

	pi.on("message_end", async (event, ctx) => {
		if (!active || awaitingInput || event.message.role !== "assistant") return;

		const message = event.message as AssistantMessage;
		if (message.stopReason !== "stop") return;

		const signal = getSignal(getAssistantText(message));
		if (!signal) return;

		if (signal === "done") {
			active = false;
			clearWorkflowWidget(ctx);
			ctx.ui.notify("Signal task complete", "info");
			return;
		}

		awaitingInput = true;
		setWorkflowWidget(ctx, "Signal task paused: waiting for your input");
		const answer = await ctx.ui.input("Agent requested input", "Type a response");
		awaitingInput = false;

		if (!answer?.trim()) {
			active = false;
			clearWorkflowWidget(ctx);
			ctx.ui.notify("Signal task stopped because no input was provided", "warning");
			return;
		}

		setWorkflowWidget(ctx, "Signal task active: waiting for the model");
		pi.sendMessage(
			{
				customType: CUSTOM_MESSAGE_TYPE,
				content: `The user answered your input request:\n\n${answer.trim()}\n\nContinue the task under the same message-signal protocol.`,
				display: false,
			},
			{ triggerTurn: true, deliverAs: "followUp" },
		);
	});

	pi.on("session_switch", async (_event, ctx) => {
		active = false;
		awaitingInput = false;
		clearWorkflowWidget(ctx);
	});
}
