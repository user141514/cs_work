import chalk from "chalk";
import { getAgentDir } from "../config.js";
import { DefaultPackageManager } from "../core/package-manager.js";
import { type PackageSource, SettingsManager } from "../core/settings-manager.js";

type PackageCommand = "install" | "remove" | "update" | "list";

interface PackageCommandOptions {
	command: PackageCommand;
	source?: string;
	local: boolean;
}

function parsePackageCommand(args: string[]): PackageCommandOptions | undefined {
	const [command, ...rest] = args;
	if (command !== "install" && command !== "remove" && command !== "update" && command !== "list") {
		return undefined;
	}

	let local = false;
	const sources: string[] = [];
	for (const arg of rest) {
		if (arg === "-l" || arg === "--local") {
			local = true;
			continue;
		}
		sources.push(arg);
	}

	return { command, source: sources[0], local };
}

function getPackageSourceString(pkg: PackageSource): string {
	return typeof pkg === "string" ? pkg : pkg.source;
}

function updatePackageSources(
	settingsManager: SettingsManager,
	packageManager: DefaultPackageManager,
	source: string,
	local: boolean,
	action: "add" | "remove",
): void {
	const currentSettings = local ? settingsManager.getProjectSettings() : settingsManager.getGlobalSettings();
	const currentPackages = currentSettings.packages ?? [];
	const scope = local ? "project" : "user";
	const settingsSource = packageManager.getSourceForSettings(source, scope);

	let nextPackages: PackageSource[];
	if (action === "add") {
		const exists = currentPackages.some((existing) =>
			packageManager.packageSourcesMatch(getPackageSourceString(existing), settingsSource, scope),
		);
		nextPackages = exists ? currentPackages : [...currentPackages, settingsSource];
	} else {
		nextPackages = currentPackages.filter(
			(existing) => !packageManager.packageSourcesMatch(getPackageSourceString(existing), settingsSource, scope),
		);
	}

	if (local) {
		settingsManager.setProjectPackages(nextPackages);
	} else {
		settingsManager.setPackages(nextPackages);
	}
}

export async function handlePackageCommand(args: string[]): Promise<boolean> {
	const options = parsePackageCommand(args);
	if (!options) {
		return false;
	}

	const cwd = process.cwd();
	const agentDir = getAgentDir();
	const settingsManager = SettingsManager.create(cwd, agentDir);
	const packageManager = new DefaultPackageManager({ cwd, agentDir, settingsManager });

	packageManager.setProgressCallback((event) => {
		if (event.type === "start") {
			process.stdout.write(chalk.dim(`${event.message}\n`));
		} else if (event.type === "error") {
			console.error(chalk.red(`Error: ${event.message}`));
		}
	});

	if (options.command === "install") {
		if (!options.source) {
			console.error(chalk.red("Missing install source."));
			process.exit(1);
		}
		await packageManager.install(options.source, { local: options.local });
		updatePackageSources(settingsManager, packageManager, options.source, options.local, "add");
		console.log(chalk.green(`Installed ${options.source}`));
		return true;
	}

	if (options.command === "remove") {
		if (!options.source) {
			console.error(chalk.red("Missing remove source."));
			process.exit(1);
		}
		await packageManager.remove(options.source, { local: options.local });
		updatePackageSources(settingsManager, packageManager, options.source, options.local, "remove");
		console.log(chalk.green(`Removed ${options.source}`));
		return true;
	}

	if (options.command === "list") {
		const globalPackages = settingsManager.getGlobalSettings().packages ?? [];
		const projectPackages = settingsManager.getProjectSettings().packages ?? [];

		if (globalPackages.length === 0 && projectPackages.length === 0) {
			console.log(chalk.dim("No packages installed."));
			return true;
		}

		const formatPackage = (pkg: PackageSource, scope: "user" | "project") => {
			const source = getPackageSourceString(pkg);
			const display = typeof pkg === "object" ? `${source} (filtered)` : source;
			console.log(`  ${display}`);
			const path = packageManager.getInstalledPath(source, scope);
			if (path) {
				console.log(chalk.dim(`    ${path}`));
			}
		};

		if (globalPackages.length > 0) {
			console.log(chalk.bold("User packages:"));
			for (const pkg of globalPackages) {
				formatPackage(pkg, "user");
			}
		}

		if (projectPackages.length > 0) {
			if (globalPackages.length > 0) console.log();
			console.log(chalk.bold("Project packages:"));
			for (const pkg of projectPackages) {
				formatPackage(pkg, "project");
			}
		}

		return true;
	}

	await packageManager.update(options.source);
	if (options.source) {
		console.log(chalk.green(`Updated ${options.source}`));
	} else {
		console.log(chalk.green("Updated packages"));
	}
	return true;
}
