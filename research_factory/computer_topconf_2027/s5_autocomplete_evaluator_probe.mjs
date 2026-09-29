import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

const modulePath = process.argv[2];
if (!modulePath) {
  console.error("usage: node --import tsx s5_autocomplete_evaluator_probe.mjs <autocomplete.ts>");
  process.exit(2);
}

const mod = await import(pathToFileURL(resolve(modulePath)).href);
const Provider = mod.CombinedAutocompleteProvider;
if (typeof Provider !== "function") {
  console.error(JSON.stringify({ error: "CombinedAutocompleteProvider export missing" }));
  process.exit(2);
}

const provider = new Provider([], process.cwd(), null);

function apply(line, item, prefix) {
  return provider.applyCompletion([line], 0, line.length, item, prefix);
}

const dirInput = "@s";
const dirValue = "@src/";
const dir = apply(dirInput, { value: dirValue, label: "src/" }, dirInput);
const dirLine = dir?.lines?.[0] ?? "";

const fileInput = "@R";
const fileValue = "@README.md";
const file = apply(fileInput, { value: fileValue, label: "README.md" }, fileInput);
const fileLine = file?.lines?.[0] ?? "";

const result = {
  dirNoTrailingSpace:
    dirLine === dirValue &&
    dir.cursorLine === 0 &&
    dir.cursorCol === dirValue.length,
  dirMarker:
    dirLine.endsWith("/") &&
    !dirLine.endsWith("/ "),
  fileTerminates:
    fileLine === fileValue + " " &&
    file.cursorLine === 0 &&
    file.cursorCol === (fileValue + " ").length,
  observed: {
    dirLine,
    dirCursorCol: dir.cursorCol,
    fileLine,
    fileCursorCol: file.cursorCol,
  },
};

console.log(JSON.stringify(result));
process.exit(result.dirNoTrailingSpace && result.dirMarker && result.fileTerminates ? 0 : 1);
