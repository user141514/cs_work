import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, relative, sep } from "node:path";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { handlePackageCommand } from "../src/cli/package-command.js";

function settingsRelative(baseDir: string, target: string): string {
	const path = relative(baseDir, target) || ".";
	return path.startsWith(".") ? path : `.${sep}${path}`;
}

function readPackages(settingsPath: string): unknown[] {
	const settings = JSON.parse(readFileSync(settingsPath, "utf-8")) as { packages?: unknown[] };
	return settings.packages ?? [];
}

describe("local package CLI", () => {
	let tempDir: string;
	let agentDir: string;
	const originalCwd = process.cwd();
	const originalAgentDir = process.env.PI_CODING_AGENT_DIR;

	beforeEach(() => {
		tempDir = join(tmpdir(), `package-cli-test-${Date.now()}-${Math.random().toString(36).slice(2)}`);
		agentDir = join(tempDir, "agent");
		mkdirSync(agentDir, { recursive: true });
		process.env.PI_CODING_AGENT_DIR = agentDir;
	});

	afterEach(() => {
		process.chdir(originalCwd);
		if (originalAgentDir === undefined) {
			delete process.env.PI_CODING_AGENT_DIR;
		} else {
			process.env.PI_CODING_AGENT_DIR = originalAgentDir;
		}
		vi.restoreAllMocks();
		rmSync(tempDir, { recursive: true, force: true });
	});

	async function runPi(args: string[], cwd: string): Promise<string> {
		const previousCwd = process.cwd();
		const output: string[] = [];
		vi.spyOn(console, "log").mockImplementation((...values: unknown[]) => {
			output.push(values.map(String).join(" "));
		});
		process.chdir(cwd);
		try {
			expect(await handlePackageCommand(args)).toBe(true);
		} finally {
			process.chdir(previousCwd);
			vi.restoreAllMocks();
		}
		return output.join("\n");
	}

	it("installs, lists, deduplicates, and removes a user local directory in place", async () => {
		const invocationDir = join(tempDir, "workspace");
		const otherDir = join(tempDir, "other");
		const sourceDir = join(tempDir, "sources", "local-package");
		const extensionPath = join(sourceDir, "extensions", "local.ts");
		mkdirSync(invocationDir, { recursive: true });
		mkdirSync(otherDir, { recursive: true });
		mkdirSync(join(sourceDir, "extensions"), { recursive: true });
		writeFileSync(extensionPath, "export default function() {}\n");
		writeFileSync(join(sourceDir, "package.json"), JSON.stringify({ dependencies: { ignored: "1.0.0" } }));

		const inputPath = relative(invocationDir, sourceDir);
		await runPi(["install", inputPath], invocationDir);

		const settingsPath = join(agentDir, "settings.json");
		const storedPath = settingsRelative(agentDir, sourceDir);
		expect(readPackages(settingsPath)).toEqual([storedPath]);
		expect(existsSync(join(sourceDir, "node_modules"))).toBe(false);

		await runPi(["install", sourceDir], otherDir);
		expect(readPackages(settingsPath)).toEqual([storedPath]);

		const listed = await runPi(["list"], otherDir);
		expect(listed).toContain("User packages:");
		expect(listed).toContain(sourceDir);

		await runPi(["remove", sourceDir], otherDir);
		expect(readPackages(settingsPath)).toEqual([]);
		expect(readFileSync(extensionPath, "utf-8")).toBe("export default function() {}\n");
		expect(existsSync(join(sourceDir, "node_modules"))).toBe(false);
	});

	it("uses project settings for a project-local file", async () => {
		const projectDir = join(tempDir, "project");
		const sourcePath = join(projectDir, "extensions", "local.ts");
		mkdirSync(join(projectDir, "extensions"), { recursive: true });
		writeFileSync(sourcePath, "export default function() {}\n");

		await runPi(["install", "./extensions/local.ts", "-l"], projectDir);

		const settingsPath = join(projectDir, ".pi", "settings.json");
		const storedPath = settingsRelative(join(projectDir, ".pi"), sourcePath);
		expect(readPackages(settingsPath)).toEqual([storedPath]);
		expect(existsSync(join(agentDir, "settings.json"))).toBe(false);

		await runPi(["install", sourcePath, "--local"], projectDir);
		expect(readPackages(settingsPath)).toEqual([storedPath]);

		const listed = await runPi(["list"], projectDir);
		expect(listed).toContain("Project packages:");
		expect(listed).toContain(sourcePath);

		await runPi(["remove", sourcePath, "-l"], projectDir);
		expect(readPackages(settingsPath)).toEqual([]);
		expect(readFileSync(sourcePath, "utf-8")).toBe("export default function() {}\n");
	});
});
