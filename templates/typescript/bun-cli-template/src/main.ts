#!/usr/bin/env bun
import { parseArgs } from "util";
import { loadConfig, resolveConfig } from "./config.js";
import { run } from "./commands/run.js";

const { values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    config: { type: "string", short: "c" },
    verbose: { type: "boolean", short: "v" },
    "log-level": { type: "string" },
    help: { type: "boolean", short: "h" },
  },
  strict: true,
  allowPositionals: true,
});

if (values.help) {
  console.log(`Usage: __SERVICE__ [options]

Options:
  -c, --config <path>    Config file (default: ~/.__SERVICE__.json)
  -v, --verbose          Enable verbose output
  --log-level <level>    Log level: debug, info, warn, error
  -h, --help             Show this help`);
  process.exit(0);
}

const fileConfig = loadConfig(values.config);
const config = resolveConfig(fileConfig, {
  verbose: values.verbose,
  logLevel: values["log-level"],
});

await run(config);
