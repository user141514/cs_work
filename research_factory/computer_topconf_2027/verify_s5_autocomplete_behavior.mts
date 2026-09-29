import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const repo = process.argv[2];
if (!repo) throw new Error("usage: tsx verify_s5_autocomplete_behavior.mts <repo>");

const modulePath = resolve(repo, "packages/tui/src/autocomplete.ts");
const mod = await import(pathToFileURL(modulePath).href);
const Provider = mod.CombinedAutocompleteProvider;
if (typeof Provider !== "function") {
  throw new Error("CombinedAutocompleteProvider export missing");
}

const sandbox = mkdtempSync(join(tmpdir(), "s5-autocomplete-"));
try {
  mkdirSync(join(sandbox, "nested"));
  writeFileSync(join(sandbox, "nested", "child.txt"), "");
  writeFileSync(join(sandbox, "file.txt"), "");

  const provider = new Provider([], sandbox);

  const rootSuggestions = provider.getForceFileSuggestions(["@"], 0, 1);
  const dirItem = rootSuggestions?.items?.find(
    (item: { value?: string }) => item.value === "@nested/",
  );
  const fileItem = rootSuggestions?.items?.find(
    (item: { value?: string }) => item.value === "@file.txt",
  );

  const directoryMarker = Boolean(dirItem);
  const fileMarker = Boolean(fileItem);

  let directoryNoTrailingSpace = false;
  let directoryContinues = false;
  if (dirItem) {
    const applied = provider.applyCompletion(["@"], 0, 1, dirItem, "@");
    directoryNoTrailingSpace =
      applied.lines[0] === "@nested/" &&
      applied.cursorCol === "@nested/".length;

    const child = provider.getForceFileSuggestions(
      applied.lines,
      applied.cursorLine,
      applied.cursorCol,
    );
    directoryContinues = Boolean(
      child?.items?.some(
        (item: { value?: string }) => item.value === "@nested/child.txt",
      ),
    );
  }

  let fileTerminatesWithSpace = false;
  if (fileItem) {
    const applied = provider.applyCompletion(["@"], 0, 1, fileItem, "@");
    fileTerminatesWithSpace =
      applied.lines[0] === "@file.txt " &&
      applied.cursorCol === "@file.txt ".length;
  }

  const result = {
    directoryMarker,
    fileMarker,
    directoryNoTrailingSpace,
    directoryContinues,
    fileTerminatesWithSpace,
    u7Pass:
      directoryMarker &&
      directoryNoTrailingSpace &&
      directoryContinues &&
      fileTerminatesWithSpace,
  };
  console.log(JSON.stringify(result));
} finally {
  rmSync(sandbox, { recursive: true, force: true });
}
